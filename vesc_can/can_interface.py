"""
VESC CAN Interface

This module provides low-level CAN bus communication functionality for VESC systems.
It wraps the python-can library and provides VESC-specific functionality.
"""

import can
import time
import threading
import queue
from typing import Optional, Callable, Union, List, Any
from dataclasses import dataclass
from .datatypes import *

@dataclass
class CANMessage:
    """Wrapper for CAN messages with timestamps"""
    arbitration_id: int
    data: bytes
    timestamp: float
    is_extended_id: bool = False
    is_error_frame: bool = False
    is_remote_frame: bool = False
    channel: Optional[str] = None

class VESCCANInterface:
    """
    Low-level CAN interface for VESC communication
    
    This class handles the actual CAN bus communication, message sending/receiving,
    and basic error handling. It's designed to be used by the higher-level service layer.
    """
    
    def __init__(
        self,
        interface: str = 'can0',
        bitrate: int = 500000,
        bustype: str = 'socketcan',
        timeout: float = 0.1
    ):
        """
        Initialize CAN interface
        
        Args:
            interface: CAN interface name (e.g., 'can0')
            bitrate: CAN bus bitrate (default: 500000)
            bustype: CAN bus type (default: 'socketcan' for Linux)
            timeout: Default timeout for operations
        """
        self.interface = interface
        self.bitrate = bitrate
        self.bustype = bustype
        self.timeout = timeout
        
        self.bus: Optional[can.BusABC] = None
        self.is_connected = False
        self.is_running = False
        
        # Message queues
        self.receive_queue = queue.Queue(maxsize=1000)
        self.send_queue = queue.Queue(maxsize=100)
        
        # Threading
        self.receive_thread: Optional[threading.Thread] = None
        self.send_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        
        # Statistics
        self.stats = {
            'messages_sent': 0,
            'messages_received': 0,
            'send_errors': 0,
            'receive_errors': 0,
            'queue_overflows': 0,
            'connected_time': 0.0,
            'last_message_time': 0.0
        }
        
        # Error handling
        self.error_callback: Optional[Callable[[Exception], None]] = None
        self.message_callback: Optional[Callable[[CANMessage], None]] = None
        
        # Bus error recovery
        self.max_consecutive_errors = 10
        self.consecutive_errors = 0
        self.last_error_time = 0.0
        self.reconnect_delay = 1.0
    
    def connect(self) -> bool:
        """
        Connect to the CAN bus
        
        Returns:
            True if connection successful, False otherwise
        """
        if self.is_connected:
            return True
        
        try:
            # Create CAN bus instance
            self.bus = can.interface.Bus(
                channel=self.interface,
                bustype=self.bustype,
                bitrate=self.bitrate
            )
            
            self.is_connected = True
            self.is_running = True
            self.consecutive_errors = 0
            self.stats['connected_time'] = time.time()
            
            # Start worker threads
            self._start_threads()
            
            return True
            
        except Exception as e:
            self._handle_error(e)
            return False
    
    def disconnect(self):
        """Disconnect from the CAN bus"""
        self.is_running = False
        self._stop_event.set()
        
        # Stop threads
        self._stop_threads()
        
        # Close bus
        if self.bus:
            try:
                self.bus.shutdown()
            except Exception:
                pass
            self.bus = None
        
        self.is_connected = False
        self._stop_event.clear()
    
    def _start_threads(self):
        """Start worker threads"""
        if self.receive_thread is None or not self.receive_thread.is_alive():
            self.receive_thread = threading.Thread(
                target=self._receive_worker,
                name="VESCCANReceive",
                daemon=True
            )
            self.receive_thread.start()
        
        if self.send_thread is None or not self.send_thread.is_alive():
            self.send_thread = threading.Thread(
                target=self._send_worker,
                name="VESCCANSend",
                daemon=True
            )
            self.send_thread.start()
    
    def _stop_threads(self):
        """Stop worker threads"""
        if self.receive_thread and self.receive_thread.is_alive():
            self.receive_thread.join(timeout=1.0)
        
        if self.send_thread and self.send_thread.is_alive():
            self.send_thread.join(timeout=1.0)
        
        self.receive_thread = None
        self.send_thread = None
    
    def _receive_worker(self):
        """Worker thread for receiving CAN messages"""
        while self.is_running and not self._stop_event.is_set():
            try:
                if not self.bus:
                    time.sleep(0.1)
                    continue
                
                # Receive message with timeout
                msg = self.bus.recv(timeout=0.1)
                
                if msg is not None:
                    # Convert to our message format
                    can_msg = CANMessage(
                        arbitration_id=msg.arbitration_id,
                        data=msg.data,
                        timestamp=msg.timestamp if msg.timestamp else time.time(),
                        is_extended_id=msg.is_extended_id,
                        is_error_frame=msg.is_error_frame,
                        is_remote_frame=msg.is_remote_frame,
                        channel=getattr(msg, 'channel', self.interface)
                    )
                    
                    # Update statistics
                    self.stats['messages_received'] += 1
                    self.stats['last_message_time'] = can_msg.timestamp
                    self.consecutive_errors = 0
                    
                    # Queue message
                    try:
                        self.receive_queue.put_nowait(can_msg)
                    except queue.Full:
                        # Queue overflow - drop oldest message
                        try:
                            self.receive_queue.get_nowait()
                            self.receive_queue.put_nowait(can_msg)
                            self.stats['queue_overflows'] += 1
                        except queue.Empty:
                            pass
                    
                    # Call message callback if set
                    if self.message_callback:
                        try:
                            self.message_callback(can_msg)
                        except Exception as e:
                            self._handle_error(e)
                
            except Exception as e:
                self._handle_receive_error(e)
    
    def _send_worker(self):
        """Worker thread for sending CAN messages"""
        while self.is_running and not self._stop_event.is_set():
            try:
                # Get message from send queue
                try:
                    msg = self.send_queue.get(timeout=0.1)
                except queue.Empty:
                    continue
                
                if not self.bus:
                    continue
                
                # Send message
                try:
                    self.bus.send(msg)
                    self.stats['messages_sent'] += 1
                    self.consecutive_errors = 0
                except Exception as e:
                    self.stats['send_errors'] += 1
                    self._handle_send_error(e)
                
            except Exception as e:
                self._handle_error(e)
    
    def send_message(
        self,
        arbitration_id: int,
        data: bytes = b'',
        is_extended_id: bool = False,
        timeout: Optional[float] = None
    ) -> bool:
        """
        Send a CAN message
        
        Args:
            arbitration_id: CAN arbitration ID
            data: Message data (0-8 bytes)
            is_extended_id: Whether to use extended ID format
            timeout: Send timeout (uses default if None)
            
        Returns:
            True if message was queued successfully
        """
        if not self.is_connected or not self.bus:
            return False
        
        if len(data) > 8:
            raise VESCCANError(f"CAN data too long: {len(data)} bytes (max 8)")
        
        # Create CAN message
        msg = can.Message(
            arbitration_id=arbitration_id,
            data=data,
            is_extended_id=is_extended_id
        )
        
        # Queue for sending
        try:
            send_timeout = timeout if timeout is not None else self.timeout
            self.send_queue.put(msg, timeout=send_timeout)
            return True
        except queue.Full:
            return False
    
    def receive_message(self, timeout: Optional[float] = None) -> Optional[CANMessage]:
        """
        Receive a CAN message
        
        Args:
            timeout: Receive timeout (uses default if None)
            
        Returns:
            CANMessage or None if timeout
        """
        if not self.is_connected:
            return None
        
        try:
            recv_timeout = timeout if timeout is not None else self.timeout
            return self.receive_queue.get(timeout=recv_timeout)
        except queue.Empty:
            return None
    
    def receive_messages(self, count: int, timeout: float = 1.0) -> List[CANMessage]:
        """
        Receive multiple CAN messages
        
        Args:
            count: Maximum number of messages to receive
            timeout: Total timeout for operation
            
        Returns:
            List of received messages
        """
        messages = []
        start_time = time.time()
        
        while len(messages) < count and (time.time() - start_time) < timeout:
            remaining_time = timeout - (time.time() - start_time)
            msg = self.receive_message(timeout=min(remaining_time, 0.1))
            
            if msg:
                messages.append(msg)
            elif remaining_time <= 0:
                break
        
        return messages
    
    def flush_receive_queue(self):
        """Clear all messages from receive queue"""
        while True:
            try:
                self.receive_queue.get_nowait()
            except queue.Empty:
                break
    
    def flush_send_queue(self):
        """Clear all messages from send queue"""
        while True:
            try:
                self.send_queue.get_nowait()
            except queue.Empty:
                break
    
    def get_queue_sizes(self) -> tuple:
        """Get current queue sizes (receive, send)"""
        return self.receive_queue.qsize(), self.send_queue.qsize()
    
    def _handle_error(self, error: Exception):
        """Handle general errors"""
        self.consecutive_errors += 1
        self.last_error_time = time.time()
        
        if self.error_callback:
            try:
                self.error_callback(error)
            except Exception:
                pass
        
        # Auto-reconnect on too many consecutive errors
        if self.consecutive_errors >= self.max_consecutive_errors:
            self._attempt_reconnect()
    
    def _handle_receive_error(self, error: Exception):
        """Handle receive-specific errors"""
        self.stats['receive_errors'] += 1
        self._handle_error(error)
    
    def _handle_send_error(self, error: Exception):
        """Handle send-specific errors"""
        self.stats['send_errors'] += 1
        self._handle_error(error)
    
    def _attempt_reconnect(self):
        """Attempt to reconnect to CAN bus"""
        if not self.is_running:
            return
        
        try:
            # Disconnect first
            old_bus = self.bus
            self.bus = None
            self.is_connected = False
            
            if old_bus:
                try:
                    old_bus.shutdown()
                except Exception:
                    pass
            
            # Wait before reconnecting
            time.sleep(self.reconnect_delay)
            
            if self.is_running:  # Check if we're still supposed to be running
                # Reconnect
                self.bus = can.interface.Bus(
                    channel=self.interface,
                    bustype=self.bustype,
                    bitrate=self.bitrate
                )
                
                self.is_connected = True
                self.consecutive_errors = 0
                
        except Exception as e:
            # Reconnection failed
            self._handle_error(e)
    
    def get_statistics(self) -> dict:
        """Get interface statistics"""
        current_time = time.time()
        uptime = current_time - self.stats['connected_time'] if self.is_connected else 0
        
        return {
            'is_connected': self.is_connected,
            'interface': self.interface,
            'bitrate': self.bitrate,
            'uptime': uptime,
            'messages_sent': self.stats['messages_sent'],
            'messages_received': self.stats['messages_received'],
            'send_errors': self.stats['send_errors'],
            'receive_errors': self.stats['receive_errors'],
            'queue_overflows': self.stats['queue_overflows'],
            'consecutive_errors': self.consecutive_errors,
            'last_message_time': self.stats['last_message_time'],
            'receive_queue_size': self.receive_queue.qsize(),
            'send_queue_size': self.send_queue.qsize(),
            'messages_per_second': self._calculate_message_rate()
        }
    
    def _calculate_message_rate(self) -> float:
        """Calculate messages per second"""
        if not self.is_connected:
            return 0.0
        
        uptime = time.time() - self.stats['connected_time']
        if uptime <= 0:
            return 0.0
        
        return self.stats['messages_received'] / uptime
    
    def set_error_callback(self, callback: Optional[Callable[[Exception], None]]):
        """Set callback for error notifications"""
        self.error_callback = callback
    
    def set_message_callback(self, callback: Optional[Callable[[CANMessage], None]]):
        """Set callback for incoming messages"""
        self.message_callback = callback
    
    def is_healthy(self) -> bool:
        """Check if the interface is healthy"""
        if not self.is_connected:
            return False
        
        # Check for too many consecutive errors
        if self.consecutive_errors >= self.max_consecutive_errors:
            return False
        
        # Check if we've received messages recently (within last 10 seconds)
        if self.stats['last_message_time'] > 0:
            time_since_last = time.time() - self.stats['last_message_time']
            if time_since_last > 10.0:
                return False
        
        return True
    
    def reset_statistics(self):
        """Reset interface statistics"""
        self.stats = {
            'messages_sent': 0,
            'messages_received': 0,
            'send_errors': 0,
            'receive_errors': 0,
            'queue_overflows': 0,
            'connected_time': time.time() if self.is_connected else 0.0,
            'last_message_time': 0.0
        }
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()

class VESCCANFilters:
    """
    Helper class for creating CAN filters for VESC communication
    """
    
    @staticmethod
    def create_vesc_filter(node_id: Optional[int] = None) -> List[dict]:
        """
        Create filter to receive VESC messages
        
        Args:
            node_id: Specific node ID to filter for (None for all)
            
        Returns:
            List of CAN filters
        """
        filters = []
        
        if node_id is not None:
            # Filter for specific node
            for cmd in STATUS_COMMANDS:
                can_id = (cmd.value << 8) | node_id
                filters.append({
                    'can_id': can_id,
                    'can_mask': 0xFFFF,  # Exact match
                    'extended': False
                })
        else:
            # Filter for all VESC status messages
            for cmd in STATUS_COMMANDS:
                can_id = cmd.value << 8
                filters.append({
                    'can_id': can_id,
                    'can_mask': 0xFF00,  # Match command, any node
                    'extended': False
                })
        
        # Always include ping/pong messages
        filters.extend([
            {
                'can_id': VESCCANCommands.PING.value << 8,
                'can_mask': 0xFF00,
                'extended': False
            },
            {
                'can_id': VESCCANCommands.PONG.value << 8,
                'can_mask': 0xFF00,
                'extended': False
            }
        ])
        
        return filters
    
    @staticmethod
    def create_node_filter(node_id: int) -> List[dict]:
        """
        Create filter to receive messages for specific node
        
        Args:
            node_id: Node ID to filter for
            
        Returns:
            List of CAN filters
        """
        return [{
            'can_id': node_id,
            'can_mask': 0xFF,  # Match only node ID
            'extended': False
        }]

def create_can_interface(
    interface: str = 'can0',
    bitrate: int = 500000,
    filters: Optional[List[dict]] = None
) -> VESCCANInterface:
    """
    Factory function to create a configured CAN interface
    
    Args:
        interface: CAN interface name
        bitrate: CAN bus bitrate
        filters: CAN filters to apply
        
    Returns:
        Configured VESCCANInterface
    """
    can_if = VESCCANInterface(interface=interface, bitrate=bitrate)
    
    # Apply filters if provided
    if filters and can_if.connect():
        try:
            if hasattr(can_if.bus, 'set_filters'):
                can_if.bus.set_filters(filters)
        except Exception:
            # Filter setting failed - not critical
            pass
    
    return can_if