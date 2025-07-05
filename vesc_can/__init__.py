"""
VESC CAN Communication Library for Raspberry Pi

This library provides a simple Python interface for communicating with VESC motor
controllers via CAN bus. It's designed for high school students with minimal
programming experience.

Basic Usage:
    import vesc_can
    
    # Connect to VESC
    vesc = vesc_can.VESC()
    
    # Read data (instant - from cache)
    duty = vesc.get_duty()
    rpm = vesc.get_rpm()
    current = vesc.get_current()
    
    # Control motor
    vesc.set_duty(0.5)      # 50% duty cycle
    vesc.set_rpm(1000)      # 1000 RPM
    vesc.set_current(5.0)   # 5 Amperes
    
    # Get network info
    active_vescs = vesc.get_active_vescs()
"""

import time
import atexit
from typing import Optional, Dict, List, Any, Union

# Import all the modules
from .datatypes import *
from .protocol import VESCProtocol
from .can_interface import VESCCANInterface
from .can_service import VESCCANService, start_can_service, stop_can_service, get_can_service
from .node_manager import get_node_manager, get_network_stats

# Version info
__version__ = "1.0.0"
__author__ = "VESC CAN Team"

class VESC:
    """
    Simple VESC interface for students
    
    This class provides easy-to-use functions for communicating with VESC motor
    controllers over CAN bus. It automatically handles all the complex networking
    in the background.
    """
    
    def __init__(
        self,
        can_interface: str = 'can0',
        bitrate: int = 500000,
        vesc_id: Optional[int] = None,
        auto_start: bool = True
    ):
        """
        Initialize VESC connection
        
        Args:
            can_interface: CAN interface name (default: 'can0')
            bitrate: CAN bus speed (default: 500000)
            vesc_id: Specific VESC ID to connect to (None for auto-detect)
            auto_start: Automatically start background service
        """
        self.can_interface = can_interface
        self.bitrate = bitrate
        self.target_vesc_id = vesc_id
        self.auto_discovered_vesc_id: Optional[int] = None
        self.service: Optional[VESCCANService] = None
        self.protocol = VESCProtocol()
        
        if auto_start:
            self.connect()
    
    def connect(self) -> bool:
        """
        Connect to VESC network
        
        Returns:
            True if connection successful
        """
        try:
            # Start the global CAN service
            success = start_can_service(self.can_interface, self.bitrate)
            
            if success:
                self.service = get_can_service()
                
                # If no specific VESC ID was given, try to auto-detect
                if self.target_vesc_id is None:
                    self._auto_detect_vesc()
                
                return True
            else:
                print(f"Failed to start CAN service on {self.can_interface}")
                return False
                
        except Exception as e:
            print(f"Error connecting to VESC: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from VESC network"""
        # Note: We don't stop the global service as other VESC instances might be using it
        self.service = None
    
    def _auto_detect_vesc(self):
        """Try to automatically detect a VESC on the network"""
        if not self.service:
            return
        
        # Wait a moment for discovery
        time.sleep(0.5)
        
        # Get active VESCs
        vescs = self.get_active_vescs()
        
        if vescs:
            # Use the first VESC we find
            self.auto_discovered_vesc_id = min(vescs.keys())
            print(f"Auto-detected VESC with ID {self.auto_discovered_vesc_id}")
        else:
            print("No VESCs detected on network")
    
    def _get_vesc_id(self) -> Optional[int]:
        """Get the VESC ID to use for commands"""
        if self.target_vesc_id is not None:
            return self.target_vesc_id
        
        if self.auto_discovered_vesc_id is not None:
            return self.auto_discovered_vesc_id
        
        # Try auto-detection again
        self._auto_detect_vesc()
        return self.auto_discovered_vesc_id
    
    def _get_cached_value(self, key: str, default: Any = 0.0) -> Any:
        """Get value from status cache"""
        if not self.service:
            return default
        
        vesc_id = self._get_vesc_id()
        if vesc_id is None:
            return default
        
        status = self.service.get_cached_status(vesc_id)
        return status.get(key, default)
    
    def _send_can_command(self, command: VESCCANCommands, data: bytes = b'') -> bool:
        """Send CAN command to VESC"""
        if not self.service:
            return False
        
        vesc_id = self._get_vesc_id()
        if vesc_id is None:
            return False
        
        return self.service.send_can_command(vesc_id, command, data)
    
    def _send_uart_request(self, command: VESCCommands, data: bytes = b'', timeout: float = 2.0) -> Optional[Dict]:
        """Send UART request to VESC"""
        if not self.service:
            return None
        
        vesc_id = self._get_vesc_id()
        if vesc_id is None:
            return None
        
        return self.service.send_uart_request(vesc_id, command, data, timeout)
    
    # Reading functions (from cache - instant response)
    
    def get_duty(self) -> float:
        """Get current duty cycle (-1.0 to 1.0)"""
        return self._get_cached_value('duty', 0.0)
    
    def get_rpm(self) -> float:
        """Get current RPM"""
        return self._get_cached_value('rpm', 0.0)
    
    def get_current(self) -> float:
        """Get motor current in Amperes"""
        return self._get_cached_value('current', 0.0)
    
    def get_current_in(self) -> float:
        """Get input current in Amperes"""
        return self._get_cached_value('current_in', 0.0)
    
    def get_voltage(self) -> float:
        """Get input voltage"""
        return self._get_cached_value('v_in', 0.0)
    
    def get_temp_motor(self) -> float:
        """Get motor temperature in Celsius"""
        return self._get_cached_value('temp_motor', 0.0)
    
    def get_temp_fet(self) -> float:
        """Get FET temperature in Celsius"""
        return self._get_cached_value('temp_fet', 0.0)
    
    def get_amp_hours(self) -> float:
        """Get amp hours consumed"""
        return self._get_cached_value('amp_hours', 0.0)
    
    def get_amp_hours_charged(self) -> float:
        """Get amp hours charged"""
        return self._get_cached_value('amp_hours_charged', 0.0)
    
    def get_watt_hours(self) -> float:
        """Get watt hours consumed"""
        return self._get_cached_value('watt_hours', 0.0)
    
    def get_watt_hours_charged(self) -> float:
        """Get watt hours charged"""
        return self._get_cached_value('watt_hours_charged', 0.0)
    
    def get_tachometer(self) -> int:
        """Get tachometer value"""
        return int(self._get_cached_value('tachometer', 0))
    
    def get_position(self) -> float:
        """Get motor position in degrees"""
        return self._get_cached_value('position', 0.0)
    
    def get_fault_code(self) -> str:
        """Get current fault code as string"""
        fault_code = VESCFaultCode(int(self._get_cached_value('fault_code', 0)))
        return get_fault_string(fault_code)
    
    def has_fault(self) -> bool:
        """Check if VESC has any fault"""
        fault_code = int(self._get_cached_value('fault_code', 0))
        return fault_code != VESCFaultCode.NONE
    
    # Motor control functions (immediate CAN commands)
    
    def set_duty(self, duty: float) -> bool:
        """
        Set motor duty cycle
        
        Args:
            duty: Duty cycle (-1.0 to 1.0)
            
        Returns:
            True if command sent successfully
        """
        try:
            can_id, data = self.protocol.create_can_set_duty(duty, self._get_vesc_id() or 0)
            return self._send_can_command(VESCCANCommands.SET_DUTY, data)
        except Exception as e:
            print(f"Error setting duty: {e}")
            return False
    
    def set_current(self, current: float) -> bool:
        """
        Set motor current
        
        Args:
            current: Current in Amperes
            
        Returns:
            True if command sent successfully
        """
        try:
            can_id, data = self.protocol.create_can_set_current(current, self._get_vesc_id() or 0)
            return self._send_can_command(VESCCANCommands.SET_CURRENT, data)
        except Exception as e:
            print(f"Error setting current: {e}")
            return False
    
    def set_current_brake(self, current: float) -> bool:
        """
        Set brake current
        
        Args:
            current: Brake current in Amperes (positive value)
            
        Returns:
            True if command sent successfully
        """
        try:
            can_id, data = self.protocol.create_can_set_current_brake(current, self._get_vesc_id() or 0)
            return self._send_can_command(VESCCANCommands.SET_CURRENT_BRAKE, data)
        except Exception as e:
            print(f"Error setting brake current: {e}")
            return False
    
    def set_rpm(self, rpm: int) -> bool:
        """
        Set motor RPM
        
        Args:
            rpm: RPM value
            
        Returns:
            True if command sent successfully
        """
        try:
            can_id, data = self.protocol.create_can_set_rpm(rpm, self._get_vesc_id() or 0)
            return self._send_can_command(VESCCANCommands.SET_RPM, data)
        except Exception as e:
            print(f"Error setting RPM: {e}")
            return False
    
    def set_position(self, position: float) -> bool:
        """
        Set motor position
        
        Args:
            position: Position in degrees
            
        Returns:
            True if command sent successfully
        """
        try:
            can_id, data = self.protocol.create_can_set_position(position, self._get_vesc_id() or 0)
            return self._send_can_command(VESCCANCommands.SET_POS, data)
        except Exception as e:
            print(f"Error setting position: {e}")
            return False
    
    def set_handbrake(self, current: float) -> bool:
        """
        Set handbrake current
        
        Args:
            current: Handbrake current in Amperes
            
        Returns:
            True if command sent successfully
        """
        try:
            can_id, data = self.protocol.create_can_set_handbrake(current, self._get_vesc_id() or 0)
            return self._send_can_command(VESCCANCommands.SET_CURRENT_HANDBRAKE, data)
        except Exception as e:
            print(f"Error setting handbrake: {e}")
            return False
    
    def stop_motor(self) -> bool:
        """
        Stop the motor (set duty cycle to 0)
        
        Returns:
            True if command sent successfully
        """
        return self.set_duty(0.0)
    
    def coast_motor(self) -> bool:
        """
        Coast the motor (no active braking)
        
        Returns:
            True if command sent successfully
        """
        return self.set_current(0.0)
    
    # Advanced reading functions (on-demand UART requests)
    
    def get_motor_config(self) -> Optional[Dict]:
        """Get motor configuration (takes ~100ms)"""
        response = self._send_uart_request(VESCCommands.GET_MCCONF)
        return response.get('data') if response else None
    
    def get_app_config(self) -> Optional[Dict]:
        """Get app configuration (takes ~100ms)"""
        response = self._send_uart_request(VESCCommands.GET_APPCONF)
        return response.get('data') if response else None
    
    def get_decoded_ppm(self) -> Optional[float]:
        """Get decoded PPM value (takes ~50ms)"""
        response = self._send_uart_request(VESCCommands.GET_DECODED_PPM)
        if response and 'data' in response:
            try:
                data = response['data'].get('raw_data', b'')
                return self.protocol.parse_uart_decoded_ppm(data)['ppm_value']
            except Exception:
                return None
        return None
    
    def get_decoded_adc(self) -> Optional[Dict]:
        """Get decoded ADC values (takes ~50ms)"""
        response = self._send_uart_request(VESCCommands.GET_DECODED_ADC)
        if response and 'data' in response:
            try:
                data = response['data'].get('raw_data', b'')
                return self.protocol.parse_uart_decoded_adc(data)
            except Exception:
                return None
        return None
    
    def get_decoded_nunchuck(self) -> Optional[float]:
        """Get decoded nunchuck value (takes ~50ms)"""
        response = self._send_uart_request(VESCCommands.GET_DECODED_CHUK)
        if response and 'data' in response:
            try:
                data = response['data'].get('raw_data', b'')
                return self.protocol.parse_uart_decoded_chuk(data)
            except Exception:
                return None
        return None
    
    def get_imu_data(self) -> Optional[VESCIMUValues]:
        """Get IMU data (takes ~50ms)"""
        response = self._send_uart_request(VESCCommands.GET_IMU_DATA)
        # TODO: Parse IMU response when needed
        return None
    
    def get_stats(self) -> Optional[VESCStatValues]:
        """Get statistics (takes ~50ms)"""
        response = self._send_uart_request(VESCCommands.GET_STATS)
        # TODO: Parse stats response when needed
        return None
    
    def get_firmware_version(self) -> Optional[str]:
        """Get firmware version (takes ~100ms)"""
        response = self._send_uart_request(VESCCommands.FW_VERSION)
        if response and 'data' in response:
            try:
                data = response['data'].get('raw_data', b'')
                fw_params = self.protocol.parse_uart_fw_version(data)
                return f"{fw_params.major}.{fw_params.minor} - {fw_params.hw}"
            except Exception:
                return None
        return None
    
    def send_terminal_command(self, command: str) -> bool:
        """
        Send terminal command to VESC
        
        Args:
            command: Terminal command string
            
        Returns:
            True if command sent successfully
        """
        try:
            response = self._send_uart_request(VESCCommands.TERMINAL_CMD, command.encode('utf-8'))
            return response is not None
        except Exception as e:
            print(f"Error sending terminal command: {e}")
            return False
    
    # Network information functions
    
    def get_active_vescs(self) -> Dict[int, Dict[str, Any]]:
        """
        Get all active VESCs on the network
        
        Returns:
            Dictionary mapping VESC ID to VESC information
        """
        if not self.service:
            return {}
        
        all_status = self.service.get_all_cached_status()
        network_nodes = get_network_stats()
        
        # Combine status data with network info
        active_vescs = {}
        for vesc_id, status in all_status.items():
            node_info = network_nodes.get('used_ids', {})
            active_vescs[vesc_id] = {
                'status': status,
                'last_seen': status.get('timestamp', 0),
                'responding': True
            }
        
        return active_vescs
    
    def get_network_info(self) -> Dict[str, Any]:
        """Get information about the CAN network"""
        stats = get_network_stats()
        
        if self.service:
            service_stats = self.service.get_service_statistics()
            stats.update({
                'service_running': service_stats['is_running'],
                'service_uptime': service_stats['uptime'],
                'messages_received': service_stats['can_interface_stats']['messages_received'],
                'messages_sent': service_stats['can_interface_stats']['messages_sent'],
            })
        
        return stats
    
    def get_my_node_id(self) -> int:
        """Get this Raspberry Pi's node ID"""
        return get_node_manager().get_node_id()
    
    # Utility functions
    
    def wait_for_vesc(self, timeout: float = 5.0) -> bool:
        """
        Wait for a VESC to appear on the network
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if VESC found, False if timeout
        """
        start_time = time.time()
        
        while (time.time() - start_time) < timeout:
            vescs = self.get_active_vescs()
            if vescs:
                if self.target_vesc_id is None:
                    self.auto_discovered_vesc_id = min(vescs.keys())
                return True
            time.sleep(0.1)
        
        return False
    
    def is_connected(self) -> bool:
        """Check if connected to a VESC"""
        return self._get_vesc_id() is not None and self.service is not None
    
    def get_all_data(self) -> Dict[str, Any]:
        """
        Get all cached data in one call
        
        Returns:
            Dictionary with all current values
        """
        return {
            'duty': self.get_duty(),
            'rpm': self.get_rpm(),
            'current': self.get_current(),
            'current_in': self.get_current_in(),
            'voltage': self.get_voltage(),
            'temp_motor': self.get_temp_motor(),
            'temp_fet': self.get_temp_fet(),
            'amp_hours': self.get_amp_hours(),
            'amp_hours_charged': self.get_amp_hours_charged(),
            'watt_hours': self.get_watt_hours(),
            'watt_hours_charged': self.get_watt_hours_charged(),
            'tachometer': self.get_tachometer(),
            'position': self.get_position(),
            'fault_code': self.get_fault_code(),
            'has_fault': self.has_fault(),
            'vesc_id': self._get_vesc_id(),
            'timestamp': time.time()
        }
    
    def print_status(self):
        """Print current VESC status (useful for debugging)"""
        data = self.get_all_data()
        
        print("VESC Status:")
        print(f"  ID: {data['vesc_id']}")
        print(f"  Duty: {data['duty']:.3f}")
        print(f"  RPM: {data['rpm']:.0f}")
        print(f"  Current: {data['current']:.2f} A")
        print(f"  Voltage: {data['voltage']:.2f} V")
        print(f"  Temp Motor: {data['temp_motor']:.1f} °C")
        print(f"  Temp FET: {data['temp_fet']:.1f} °C")
        print(f"  Fault: {data['fault_code']}")
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()

# Convenience functions for students

def connect_to_vesc(
    can_interface: str = 'can0',
    vesc_id: Optional[int] = None,
    wait_timeout: float = 5.0
) -> Optional[VESC]:
    """
    Simple function to connect to a VESC
    
    Args:
        can_interface: CAN interface name
        vesc_id: Specific VESC ID (None for auto-detect)
        wait_timeout: Time to wait for VESC to appear
        
    Returns:
        VESC object or None if connection failed
    """
    try:
        vesc = VESC(can_interface=can_interface, vesc_id=vesc_id)
        
        if vesc.wait_for_vesc(wait_timeout):
            print(f"Connected to VESC ID {vesc._get_vesc_id()}")
            return vesc
        else:
            print("No VESC found on network")
            return None
            
    except Exception as e:
        print(f"Error connecting to VESC: {e}")
        return None

def list_active_vescs(can_interface: str = 'can0') -> List[int]:
    """
    Get list of active VESC IDs on the network
    
    Args:
        can_interface: CAN interface name
        
    Returns:
        List of VESC IDs
    """
    try:
        vesc = VESC(can_interface=can_interface)
        time.sleep(1.0)  # Wait for discovery
        vescs = vesc.get_active_vescs()
        return sorted(vescs.keys())
    except Exception:
        return []

def get_network_status(can_interface: str = 'can0') -> Dict[str, Any]:
    """
    Get CAN network status
    
    Args:
        can_interface: CAN interface name
        
    Returns:
        Network status information
    """
    try:
        vesc = VESC(can_interface=can_interface)
        return vesc.get_network_info()
    except Exception:
        return {}

# Clean shutdown on exit
def _cleanup():
    """Clean up resources on exit"""
    try:
        stop_can_service()
    except Exception:
        pass

atexit.register(_cleanup)

# Export main classes and functions
__all__ = [
    'VESC',
    'VESCError',
    'VESCTimeoutError', 
    'VESCProtocolError',
    'VESCCANError',
    'VESCFaultCode',
    'VESCValues',
    'connect_to_vesc',
    'list_active_vescs',
    'get_network_status',
    'get_fault_string'
]