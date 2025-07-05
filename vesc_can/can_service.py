"""
VESC CAN Background Service

This module provides the background service that handles automatic CAN network
participation including ping/pong responses, status message caching, heartbeat
transmission, and network discovery.
"""

import time
import threading
import queue
from typing import Dict, Any, Optional, Callable, List
from collections import defaultdict, deque
import weakref

from .datatypes import *
from .protocol import VESCProtocol
from .can_interface import VESCCANInterface, CANMessage
from .node_manager import VESCNodeManager, get_node_manager

class VESCCANService:
    """
    Background CAN service for VESC communication
    
    This service runs continuously and handles:
    - Automatic ping/pong responses
    - Status message parsing and caching
    - Heartbeat transmission
    - Network discovery
    - Node conflict detection
    """
    
    def __init__(
        self,
        can_interface: VESCCANInterface,
        node_manager: Optional[VESCNodeManager] = None
    ):
        """
        Initialize CAN service
        
        Args:
            can_interface: CAN interface to use
            node_manager: Node manager (uses global if None)
        """
        self.can_interface = can_interface
        self.node_manager = node_manager or get_node_manager()
        self.protocol = VESCProtocol()
        
        # Service state
        self.is_running = False
        self._stop_event = threading.Event()
        
        # Worker threads
        self.message_thread: Optional[threading.Thread] = None
        self.heartbeat_thread: Optional[threading.Thread] = None
        self.discovery_thread: Optional[threading.Thread] = None
        
        # Status message cache - stores latest values from each VESC
        self.status_cache: Dict[int, Dict[str, Any]] = defaultdict(dict)
        self.status_history: Dict[int, deque] = defaultdict(lambda: deque(maxlen=CAN_STATUS_MSGS_TO_STORE))
        self.cache_lock = threading.RLock()
        
        # UART forwarding for on-demand requests
        self.uart_responses: Dict[int, queue.Queue] = {}  # Request ID -> Response queue
        self.uart_request_id = 0
        self.uart_lock = threading.Lock()
        
        # Statistics
        self.stats = {
            'ping_received': 0,
            'pong_sent': 0,
            'status_messages_parsed': 0,
            'heartbeats_sent': 0,
            'uart_requests_forwarded': 0,
            'uart_responses_received': 0,
            'service_start_time': 0.0,
            'last_heartbeat_time': 0.0,
            'last_discovery_time': 0.0,
            'active_vescs': set(),
        }
        
        # Callbacks
        self.status_callbacks: List[Callable[[int, Dict[str, Any]], None]] = []
        self.node_discovery_callbacks: List[Callable[[int, Dict[str, Any]], None]] = []
        self.error_callbacks: List[Callable[[Exception], None]] = []
        
        # Timing configuration
        self.heartbeat_interval = 5.0  # Send heartbeat every 5 seconds (much slower)
        self.discovery_interval = 60.0  # 60 seconds
        self.status_cache_timeout = 2.0  # 2 seconds
    
    def start(self) -> bool:
        """
        Start the background service
        
        Returns:
            True if started successfully
        """
        if self.is_running:
            return True
        
        if not self.can_interface.is_connected:
            if not self.can_interface.connect():
                return False
        
        self.is_running = True
        self._stop_event.clear()
        self.stats['service_start_time'] = time.time()
        
        # Set up CAN interface message callback
        self.can_interface.set_message_callback(self._handle_can_message)
        
        # Start worker threads
        self._start_threads()
        
        return True
    
    def stop(self):
        """Stop the background service"""
        self.is_running = False
        self._stop_event.set()
        
        # Stop threads
        self._stop_threads()
        
        # Clear message callback
        self.can_interface.set_message_callback(None)
    
    def _start_threads(self):
        """Start worker threads"""
        # Message processing thread
        self.message_thread = threading.Thread(
            target=self._message_worker,
            name="VESCCANMessageWorker",
            daemon=True
        )
        self.message_thread.start()
        
        # Heartbeat thread
        self.heartbeat_thread = threading.Thread(
            target=self._heartbeat_worker,
            name="VESCCANHeartbeat",
            daemon=True
        )
        self.heartbeat_thread.start()
        
        # Discovery thread
        self.discovery_thread = threading.Thread(
            target=self._discovery_worker,
            name="VESCCANDiscovery",
            daemon=True
        )
        self.discovery_thread.start()
    
    def _stop_threads(self):
        """Stop worker threads"""
        threads = [self.message_thread, self.heartbeat_thread, self.discovery_thread]
        
        for thread in threads:
            if thread and thread.is_alive():
                thread.join(timeout=1.0)
        
        self.message_thread = None
        self.heartbeat_thread = None
        self.discovery_thread = None
    
    def _handle_can_message(self, message: CANMessage):
        """Handle incoming CAN message (called from CAN interface)"""
        try:
            # Parse message using protocol
            parsed = self.protocol.parse_can_message(message.arbitration_id, message.data)
            
            if parsed:
                command = parsed['command']
                node_id = parsed['node_id']
                
                # Handle different message types
                if command == VESCCANCommands.PING:
                    self._handle_ping(node_id, message)
                elif command == VESCCANCommands.PONG:
                    self._handle_pong(node_id, message)
                elif command in STATUS_COMMANDS:
                    self._handle_status_message(node_id, command, parsed, message)
                else:
                    # Other command types - check if it's a UART response
                    self._handle_other_message(node_id, command, parsed, message)
                
                # Update node registry
                self.node_manager.register_node(node_id, {
                    'last_command': command.value,
                    'device_type': 'vesc_or_other'
                })
                
        except Exception as e:
            self._handle_error(e)
    
    def _handle_ping(self, sender_node_id: int, message: CANMessage):
        """Handle ping message"""
        try:
            # DON'T respond to pings for now - causes issues with VESC Tool
            # The ping-pong mechanism is too complex and crashes the system
            # Just log that we received it
            
            self.stats['ping_received'] += 1
            # Don't send pong response to avoid corrupting VESC Tool
            
        except Exception as e:
            self._handle_error(e)
    
    def _handle_pong(self, sender_node_id: int, message: CANMessage):
        """Handle pong message"""
        # Register that we received a pong from this node
        self.node_manager.register_node(sender_node_id, {
            'device_type': 'vesc_or_other',
            'responds_to_ping': True
        })
        
        # Call discovery callbacks
        for callback in self.node_discovery_callbacks:
            try:
                callback(sender_node_id, {'event': 'pong_received'})
            except Exception as e:
                self._handle_error(e)
    
    def _handle_status_message(
        self, 
        node_id: int, 
        command: VESCCANCommands, 
        parsed_data: Dict[str, Any],
        message: CANMessage
    ):
        """Handle status message"""
        try:
            with self.cache_lock:
                # Update cache
                if node_id not in self.status_cache:
                    self.status_cache[node_id] = {}
                
                # Store parsed data
                for key, value in parsed_data.items():
                    if key not in ['command', 'node_id']:
                        self.status_cache[node_id][key] = value
                
                # Add to history
                history_entry = {
                    'timestamp': parsed_data.get('timestamp', time.time()),
                    'command': command,
                    'data': parsed_data.copy()
                }
                self.status_history[node_id].append(history_entry)
                
                # Update statistics
                self.stats['status_messages_parsed'] += 1
                self.stats['active_vescs'].add(node_id)
            
            # Call status callbacks
            for callback in self.status_callbacks:
                try:
                    callback(node_id, parsed_data)
                except Exception as e:
                    self._handle_error(e)
                    
        except Exception as e:
            self._handle_error(e)
    
    def _handle_other_message(
        self,
        node_id: int,
        command: VESCCANCommands,
        parsed_data: Dict[str, Any],
        message: CANMessage
    ):
        """Handle other (non-status, non-ping/pong) messages"""
        # Check if this is a response to a UART request we forwarded
        with self.uart_lock:
            # Look for waiting UART responses
            for request_id, response_queue in list(self.uart_responses.items()):
                try:
                    response_queue.put_nowait({
                        'node_id': node_id,
                        'command': command,
                        'data': parsed_data,
                        'raw_message': message
                    })
                    self.stats['uart_responses_received'] += 1
                except queue.Full:
                    # Queue full - remove old request
                    del self.uart_responses[request_id]
    
    def _message_worker(self):
        """Worker thread for processing CAN messages"""
        while self.is_running and not self._stop_event.is_set():
            try:
                # The actual message handling is done via callback from CAN interface
                # This thread just monitors for node conflicts and cache cleanup
                
                # Check for node ID conflicts
                if self.node_manager.detect_node_conflict():
                    self.node_manager.resolve_node_conflict()
                
                # Clean up old cache entries
                self._cleanup_status_cache()
                
                # Clean up old UART response queues
                self._cleanup_uart_responses()
                
                time.sleep(0.1)  # 100ms interval
                
            except Exception as e:
                self._handle_error(e)
    
    def _heartbeat_worker(self):
        """Worker thread for sending heartbeat messages"""
        while self.is_running and not self._stop_event.is_set():
            try:
                current_time = time.time()
                
                # Send heartbeat at configured interval
                if current_time - self.stats.get('last_heartbeat_time', 0) >= self.heartbeat_interval:
                    self._send_heartbeat()
                    self.stats['last_heartbeat_time'] = current_time
                
                time.sleep(self.heartbeat_interval / 2)  # Check at half interval
                
            except Exception as e:
                self._handle_error(e)
    
    def _discovery_worker(self):
        """Worker thread for network discovery"""
        while self.is_running and not self._stop_event.is_set():
            try:
                current_time = time.time()
                
                # Perform discovery at configured interval
                if current_time - self.stats.get('last_discovery_time', 0) >= self.discovery_interval:
                    self._perform_discovery()
                    self.stats['last_discovery_time'] = current_time
                
                time.sleep(5.0)  # Check every 5 seconds
                
            except Exception as e:
                self._handle_error(e)
    
    def _send_heartbeat(self):
        """Send heartbeat message"""
        try:
            # Disable heartbeats for now - they may interfere with VESC Tool
            # my_node_id = self.node_manager.get_node_id()
            # heartbeat_id, heartbeat_data = self.protocol.create_heartbeat_packet(my_node_id)
            # self.can_interface.send_message(heartbeat_id, heartbeat_data)
            
            self.stats['heartbeats_sent'] += 1
            
        except Exception as e:
            self._handle_error(e)
    
    def _perform_discovery(self):
        """Perform network discovery"""
        try:
            # Send broadcast ping
            my_node_id = self.node_manager.get_node_id()
            ping_id, ping_data = self.protocol.create_can_ping(0)  # Broadcast to node 0
            
            self.can_interface.send_message(ping_id, ping_data)
            
            # Clean up old nodes
            self.node_manager.cleanup_old_nodes()
            
        except Exception as e:
            self._handle_error(e)
    
    def _cleanup_status_cache(self):
        """Remove old entries from status cache"""
        current_time = time.time()
        cutoff_time = current_time - self.status_cache_timeout
        
        with self.cache_lock:
            nodes_to_remove = []
            
            for node_id, cache_data in self.status_cache.items():
                timestamp = cache_data.get('timestamp', 0)
                if timestamp < cutoff_time:
                    nodes_to_remove.append(node_id)
            
            for node_id in nodes_to_remove:
                if node_id in self.status_cache:
                    del self.status_cache[node_id]
                if node_id in self.stats['active_vescs']:
                    self.stats['active_vescs'].discard(node_id)
    
    def _cleanup_uart_responses(self):
        """Remove old UART response queues"""
        current_time = time.time()
        
        with self.uart_lock:
            expired_requests = []
            
            for request_id in list(self.uart_responses.keys()):
                # Remove requests older than 5 seconds
                if current_time - request_id > 5.0:
                    expired_requests.append(request_id)
            
            for request_id in expired_requests:
                del self.uart_responses[request_id]
    
    def _handle_error(self, error: Exception):
        """Handle service errors"""
        for callback in self.error_callbacks:
            try:
                callback(error)
            except Exception:
                pass
    
    # Public API methods
    
    def get_cached_status(self, node_id: int) -> Optional[Dict[str, Any]]:
        """
        Get cached status data for a VESC node
        
        Args:
            node_id: VESC node ID
            
        Returns:
            Cached status data or None if not available
        """
        with self.cache_lock:
            return self.status_cache.get(node_id, {}).copy()
    
    def get_all_cached_status(self) -> Dict[int, Dict[str, Any]]:
        """Get cached status data for all nodes"""
        with self.cache_lock:
            return {
                node_id: data.copy() 
                for node_id, data in self.status_cache.items()
            }
    
    def get_status_history(self, node_id: int, count: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent status history for a node
        
        Args:
            node_id: VESC node ID
            count: Number of recent entries to return
            
        Returns:
            List of recent status entries
        """
        with self.cache_lock:
            history = list(self.status_history.get(node_id, []))
            return history[-count:] if history else []
    
    def send_uart_request(
        self, 
        node_id: int, 
        command: VESCCommands, 
        data: bytes = b'',
        timeout: float = 2.0
    ) -> Optional[Dict[str, Any]]:
        """
        Send UART request to VESC and wait for response
        
        Args:
            node_id: Target VESC node ID
            command: VESC command to send
            data: Command data
            timeout: Response timeout
            
        Returns:
            Response data or None if timeout
        """
        try:
            # Create UART packet
            uart_packet = self.protocol.create_uart_packet(command, data)
            
            # Create forwarding CAN frame
            forward_id = (VESCCANCommands.FILL_RX_BUFFER.value << 8) | node_id
            
            # Split UART packet into CAN frames if needed
            packet_len = len(uart_packet)
            frames_needed = (packet_len + 7) // 8  # Round up to number of 8-byte frames
            
            with self.uart_lock:
                # Create response queue
                request_id = time.time()  # Use timestamp as request ID
                response_queue = queue.Queue()
                self.uart_responses[request_id] = response_queue
            
            try:
                # Send UART packet in CAN frames
                for i in range(frames_needed):
                    start_idx = i * 8
                    end_idx = min(start_idx + 8, packet_len)
                    frame_data = uart_packet[start_idx:end_idx]
                    
                    if i == 0:
                        # First frame - use FILL_RX_BUFFER
                        can_id = forward_id
                    else:
                        # Subsequent frames - use FILL_RX_BUFFER_LONG
                        can_id = (VESCCANCommands.FILL_RX_BUFFER_LONG.value << 8) | node_id
                    
                    self.can_interface.send_message(can_id, frame_data)
                
                # Send process command
                process_id = (VESCCANCommands.PROCESS_RX_BUFFER.value << 8) | node_id
                self.can_interface.send_message(process_id, b'')
                
                self.stats['uart_requests_forwarded'] += 1
                
                # Wait for response
                try:
                    response = response_queue.get(timeout=timeout)
                    return response
                except queue.Empty:
                    return None
                    
            finally:
                # Clean up response queue
                with self.uart_lock:
                    if request_id in self.uart_responses:
                        del self.uart_responses[request_id]
                        
        except Exception as e:
            self._handle_error(e)
            return None
    
    def send_can_command(
        self,
        node_id: int,
        command: VESCCANCommands,
        data: bytes = b''
    ) -> bool:
        """
        Send CAN command to VESC
        
        Args:
            node_id: Target VESC node ID
            command: CAN command
            data: Command data
            
        Returns:
            True if sent successfully
        """
        try:
            can_id = (command.value << 8) | node_id
            return self.can_interface.send_message(can_id, data)
        except Exception as e:
            self._handle_error(e)
            return False
    
    def add_status_callback(self, callback: Callable[[int, Dict[str, Any]], None]):
        """Add callback for status message updates"""
        self.status_callbacks.append(callback)
    
    def remove_status_callback(self, callback: Callable[[int, Dict[str, Any]], None]):
        """Remove status callback"""
        if callback in self.status_callbacks:
            self.status_callbacks.remove(callback)
    
    def add_discovery_callback(self, callback: Callable[[int, Dict[str, Any]], None]):
        """Add callback for node discovery events"""
        self.node_discovery_callbacks.append(callback)
    
    def remove_discovery_callback(self, callback: Callable[[int, Dict[str, Any]], None]):
        """Remove discovery callback"""
        if callback in self.node_discovery_callbacks:
            self.node_discovery_callbacks.remove(callback)
    
    def add_error_callback(self, callback: Callable[[Exception], None]):
        """Add callback for error events"""
        self.error_callbacks.append(callback)
    
    def remove_error_callback(self, callback: Callable[[Exception], None]):
        """Remove error callback"""
        if callback in self.error_callbacks:
            self.error_callbacks.remove(callback)
    
    def get_service_statistics(self) -> Dict[str, Any]:
        """Get service statistics"""
        current_time = time.time()
        uptime = current_time - self.stats['service_start_time']
        
        return {
            'is_running': self.is_running,
            'uptime': uptime,
            'my_node_id': self.node_manager.get_node_id(),
            'ping_received': self.stats['ping_received'],
            'pong_sent': self.stats['pong_sent'],
            'status_messages_parsed': self.stats['status_messages_parsed'],
            'heartbeats_sent': self.stats['heartbeats_sent'],
            'uart_requests_forwarded': self.stats['uart_requests_forwarded'],
            'uart_responses_received': self.stats['uart_responses_received'],
            'active_vescs': len(self.stats['active_vescs']),
            'active_vesc_list': sorted(list(self.stats['active_vescs'])),
            'cached_nodes': len(self.status_cache),
            'last_heartbeat_time': self.stats['last_heartbeat_time'],
            'last_discovery_time': self.stats['last_discovery_time'],
            'can_interface_stats': self.can_interface.get_statistics(),
            'node_manager_stats': self.node_manager.get_network_stats()
        }
    
    def force_discovery(self):
        """Force immediate network discovery"""
        self._perform_discovery()
    
    def clear_cache(self):
        """Clear all cached status data"""
        with self.cache_lock:
            self.status_cache.clear()
            self.status_history.clear()
            self.stats['active_vescs'].clear()

# Global service instance
_service_instance: Optional[VESCCANService] = None

def get_can_service() -> Optional[VESCCANService]:
    """Get the global CAN service instance"""
    return _service_instance

def create_can_service(
    interface: str = 'can0',
    bitrate: int = 500000,
    node_manager: Optional[VESCNodeManager] = None
) -> VESCCANService:
    """
    Create and configure the global CAN service
    
    Args:
        interface: CAN interface name
        bitrate: CAN bus bitrate
        node_manager: Node manager instance
        
    Returns:
        CAN service instance
    """
    global _service_instance
    
    if _service_instance and _service_instance.is_running:
        _service_instance.stop()
    
    from .can_interface import create_can_interface, VESCCANFilters
    
    # Create CAN interface with VESC filters
    can_if = create_can_interface(interface, bitrate)
    
    # Create service
    _service_instance = VESCCANService(can_if, node_manager)
    
    return _service_instance

def start_can_service(
    interface: str = 'can0',
    bitrate: int = 500000
) -> bool:
    """
    Start the global CAN service
    
    Args:
        interface: CAN interface name
        bitrate: CAN bus bitrate
        
    Returns:
        True if started successfully
    """
    global _service_instance
    
    if not _service_instance:
        _service_instance = create_can_service(interface, bitrate)
    
    return _service_instance.start()

def stop_can_service():
    """Stop the global CAN service"""
    global _service_instance
    
    if _service_instance:
        _service_instance.stop()