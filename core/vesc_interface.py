"""
VESC Interface Layer
Handles low-level CAN communication with VESC motor controllers.
"""

import can
import time
import threading
import uuid
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
from queue import Queue, Empty
from core.protocol import VESCProtocolParser
from core.commands import VESCCommandEncoder


@dataclass
class PendingCommand:
    """Represents a command waiting for response"""
    command_id: str
    timestamp: float
    controller_id: int
    command_type: str
    callback: Optional[Callable] = None
    timeout: float = 2.0
    retry_count: int = 0
    max_retries: int = 1


class VESCInterface:
    """Low-level interface to VESC motor controllers via CAN"""
    
    def __init__(self, can_channel: str = 'can0', bustype: str = 'socketcan'):
        self.can_channel = can_channel
        self.bustype = bustype
        self.bus = None
        self.parser = VESCProtocolParser()
        self.encoder = VESCCommandEncoder()
        
        # Command tracking
        self.pending_commands: Dict[str, PendingCommand] = {}
        self.command_lock = threading.Lock()
        
        # Live telemetry data
        self.live_data: Dict[int, Dict[str, Any]] = {}
        self.data_lock = threading.Lock()
        
        # Message queues
        self.telemetry_queue = Queue(maxsize=1000)
        self.response_queue = Queue(maxsize=100)
        
        # Threading
        self.running = False
        self.receive_thread = None
        self.cleanup_thread = None
        
        # Statistics
        self.stats = {
            'messages_received': 0,
            'messages_parsed': 0,
            'commands_sent': 0,
            'commands_successful': 0,
            'commands_timeout': 0,
            'parse_errors': 0
        }
    
    def connect(self) -> bool:
        """Connect to CAN bus"""
        try:
            self.bus = can.interface.Bus(channel=self.can_channel, bustype=self.bustype)
            self.running = True
            
            # Start background threads
            self.receive_thread = threading.Thread(target=self._receive_loop, daemon=True)
            self.cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
            
            self.receive_thread.start()
            self.cleanup_thread.start()
            
            print(f"Connected to CAN bus: {self.can_channel}")
            return True
            
        except Exception as e:
            print(f"Failed to connect to CAN bus: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from CAN bus"""
        self.running = False
        
        if self.receive_thread:
            self.receive_thread.join(timeout=1.0)
        
        if self.cleanup_thread:
            self.cleanup_thread.join(timeout=1.0)
            
        if self.bus:
            self.bus.shutdown()
            self.bus = None
            
        print("Disconnected from CAN bus")
    
    def _receive_loop(self):
        """Background thread for receiving CAN messages"""
        while self.running:
            try:
                message = self.bus.recv(timeout=0.1)
                if message is not None:
                    self.stats['messages_received'] += 1
                    self._process_message(message)
                    
            except Exception as e:
                if self.running:  # Only log errors if we're supposed to be running
                    print(f"Error in receive loop: {e}")
    
    def _cleanup_loop(self):
        """Background thread for cleaning up expired commands"""
        while self.running:
            try:
                current_time = time.time()
                expired_commands = []
                
                with self.command_lock:
                    for cmd_id, cmd in self.pending_commands.items():
                        if current_time - cmd.timestamp > cmd.timeout:
                            expired_commands.append(cmd_id)
                
                # Handle expired commands
                for cmd_id in expired_commands:
                    self._handle_command_timeout(cmd_id)
                
                time.sleep(0.1)  # Check every 100ms
                
            except Exception as e:
                if self.running:
                    print(f"Error in cleanup loop: {e}")
    
    def _process_message(self, message: can.Message):
        """Process incoming CAN message"""
        try:
            # Parse the message
            parsed = self.parser.parse_message(message.arbitration_id, message.data)
            
            if parsed is None:
                # Check if it's a command response
                self._check_command_response(message.arbitration_id, message.data)
                return
            
            self.stats['messages_parsed'] += 1
            
            # Update live data
            controller_id = parsed['controller_id']
            msg_type = parsed['type']
            data = parsed['data']
            
            with self.data_lock:
                if controller_id not in self.live_data:
                    self.live_data[controller_id] = {}
                
                self.live_data[controller_id][msg_type] = data
                self.live_data[controller_id]['last_update'] = time.time()
            
            # Queue for external processing
            try:
                self.telemetry_queue.put_nowait(parsed)
            except:
                pass  # Queue full, drop message
                
        except Exception as e:
            self.stats['parse_errors'] += 1
            print(f"Error processing message {message.arbitration_id:08X}: {e}")
    
    def _check_command_response(self, can_id: int, data: bytes):
        """Check if message is a response to a pending command"""
        controller_id = can_id & 0xFF
        
        with self.command_lock:
            # Look for pending commands for this controller
            for cmd_id, cmd in list(self.pending_commands.items()):
                if cmd.controller_id == controller_id:
                    # This is a simple response check - could be enhanced
                    # based on specific response patterns
                    self._handle_command_response(cmd_id, can_id, data)
                    break
    
    def _handle_command_response(self, cmd_id: str, can_id: int, data: bytes):
        """Handle response to a command"""
        with self.command_lock:
            if cmd_id in self.pending_commands:
                cmd = self.pending_commands.pop(cmd_id)
                self.stats['commands_successful'] += 1
                
                if cmd.callback:
                    try:
                        cmd.callback(True, {'can_id': can_id, 'data': data})
                    except Exception as e:
                        print(f"Error in command callback: {e}")
    
    def _handle_command_timeout(self, cmd_id: str):
        """Handle command timeout"""
        with self.command_lock:
            if cmd_id not in self.pending_commands:
                return
                
            cmd = self.pending_commands[cmd_id]
            
            # Check if we should retry
            if cmd.retry_count < cmd.max_retries:
                cmd.retry_count += 1
                cmd.timestamp = time.time()
                print(f"Retrying command {cmd_id} (attempt {cmd.retry_count + 1})")
                # Command stays in pending_commands for retry
                return
            
            # Command has timed out
            self.pending_commands.pop(cmd_id)
            self.stats['commands_timeout'] += 1
            
            if cmd.callback:
                try:
                    cmd.callback(False, {'error': 'timeout'})
                except Exception as e:
                    print(f"Error in timeout callback: {e}")
    
    def send_command(self, controller_id: int, command_type: str, value: float, 
                    callback: Optional[Callable] = None, timeout: float = 2.0, expect_response: bool = True) -> str:
        """
        Send a command to VESC controller
        
        Args:
            controller_id: Target controller ID
            command_type: Type of command ('duty', 'current', 'brake')
            value: Command value
            callback: Optional callback function for response
            timeout: Command timeout in seconds
            expect_response: Whether to wait for a response from VESC
            
        Returns:
            Command ID for tracking
        """
        if not self.bus:
            raise RuntimeError("CAN bus not connected")
        
        # Generate unique command ID
        cmd_id = str(uuid.uuid4())
        
        try:
            # Encode command
            if command_type == 'duty':
                can_id, data = self.encoder.encode_set_duty_cycle(controller_id, value)
            elif command_type == 'current':
                can_id, data = self.encoder.encode_set_current(controller_id, value)
            elif command_type == 'brake':
                can_id, data = self.encoder.encode_set_current_brake(controller_id, value)
            else:
                raise ValueError(f"Unknown command type: {command_type}")
            
            # Create CAN message
            message = can.Message(
                arbitration_id=can_id,
                data=data,
                is_extended_id=True
            )
            
            # Register pending command only if we expect a response
            if expect_response:
                with self.command_lock:
                    self.pending_commands[cmd_id] = PendingCommand(
                        command_id=cmd_id,
                        timestamp=time.time(),
                        controller_id=controller_id,
                        command_type=command_type,
                        callback=callback,
                        timeout=timeout
                    )
            
            # Send message with timeout to prevent blocking
            self.bus.send(message, timeout=0.1)
            self.stats['commands_sent'] += 1
            
            # For fire-and-forget commands, immediately call success callback
            if not expect_response and callback:
                try:
                    callback(True, {'message': 'Command sent (no response expected)'})
                except Exception as e:
                    print(f"Error in immediate callback: {e}")
            
            return cmd_id
            
        except Exception as e:
            print(f"Error sending command: {e}")
            # Remove from pending commands if it was added
            with self.command_lock:
                self.pending_commands.pop(cmd_id, None)
            raise
    
    def get_live_data(self, controller_id: int) -> Optional[Dict[str, Any]]:
        """Get latest live data for a controller"""
        with self.data_lock:
            return self.live_data.get(controller_id, {}).copy()
    
    def get_telemetry_value(self, controller_id: int, data_type: str, field: str) -> Optional[float]:
        """Get specific telemetry value"""
        with self.data_lock:
            controller_data = self.live_data.get(controller_id, {})
            status_data = controller_data.get(data_type)
            
            if status_data:
                # status_data is a dataclass instance
                try:
                    return getattr(status_data, field)
                except AttributeError:
                    return None
            return None
    
    def get_statistics(self) -> Dict[str, int]:
        """Get interface statistics"""
        return self.stats.copy()
    
    def clear_statistics(self):
        """Clear interface statistics"""
        for key in self.stats:
            self.stats[key] = 0


def test_vesc_interface():
    """Test VESC interface with live hardware"""
    interface = VESCInterface()
    
    if not interface.connect():
        print("Failed to connect to CAN bus")
        return
    
    print("Connected to VESC interface")
    print("Collecting telemetry data...")
    
    try:
        # Collect data for 5 seconds
        start_time = time.time()
        while time.time() - start_time < 5.0:
            # Get live data for controller 74
            data = interface.get_live_data(74)
            if data:
                print(f"Controller 74 data: {len(data)} message types")
                if 'status_4' in data:
                    temp = data['status_4'].temp_fet
                    voltage = data.get('status_5', {})
                    if hasattr(voltage, 'v_in'):
                        print(f"  FET temp: {temp}°C, Voltage: {voltage.v_in}V")
            
            time.sleep(1.0)
        
        # Print statistics
        stats = interface.get_statistics()
        print(f"\nStatistics: {stats}")
        
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        interface.disconnect()


if __name__ == "__main__":
    test_vesc_interface()