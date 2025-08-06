"""
***DO NOT EDIT***
Student API for VESC Motor Controllers
High-level Python API for students to interact with VESC motor controllers.
***DO NOT EDIT***
"""

import time
import threading
from typing import Optional, Dict, Any
from core.main import VESCSystemManager


class VESCController:
    """High-level interface to a VESC motor controller"""
    
    def __init__(self, controller_id: int, system_manager: VESCSystemManager):
        self.controller_id = controller_id
        self.system_manager = system_manager
        self.interface = system_manager.get_interface()
        self._last_command_time = 0
        self._command_delay = 0.1  # Minimum time between commands
    
    def _check_command_rate(self):
        """Ensure commands aren't sent too frequently"""
        current_time = time.time()
        if current_time - self._last_command_time < self._command_delay:
            time.sleep(self._command_delay - (current_time - self._last_command_time))
        self._last_command_time = time.time()
    
    def _get_telemetry_value(self, data_type: str, field: str) -> Optional[float]:
        """Get a specific telemetry value"""
        return self.interface.get_telemetry_value(self.controller_id, data_type, field)
    
    def _get_live_data(self) -> Dict[str, Any]:
        """Get all live data for this controller"""
        return self.interface.get_live_data(self.controller_id) or {}
    
    # ==================== READ FUNCTIONS ====================
    
    def get_rpm(self) -> Optional[float]:
        """Get motor RPM"""
        return self._get_telemetry_value('status_1', 'rpm')
    
    def get_motor_current(self) -> Optional[float]:
        """Get motor current in amperes"""
        return self._get_telemetry_value('status_1', 'current')
    
    def get_duty_cycle(self) -> Optional[float]:
        """Get duty cycle (-1.0 to 1.0)"""
        return self._get_telemetry_value('status_1', 'duty_cycle')
    
    def get_amp_hours_consumed(self) -> Optional[float]:
        """Get amp-hours consumed"""
        return self._get_telemetry_value('status_2', 'amp_hours')
    
    def get_amp_hours_charged(self) -> Optional[float]:
        """Get amp-hours charged"""
        return self._get_telemetry_value('status_2', 'amp_hours_charged')
    
    def get_watt_hours_consumed(self) -> Optional[float]:
        """Get watt-hours consumed"""
        return self._get_telemetry_value('status_3', 'watt_hours')
    
    def get_watt_hours_charged(self) -> Optional[float]:
        """Get watt-hours charged"""
        return self._get_telemetry_value('status_3', 'watt_hours_charged')
    
    def get_fet_temperature(self) -> Optional[float]:
        """Get FET temperature in Celsius"""
        return self._get_telemetry_value('status_4', 'temp_fet')
    
    def get_motor_temperature(self) -> Optional[float]:
        """Get motor temperature in Celsius"""
        return self._get_telemetry_value('status_4', 'temp_motor')
    
    def get_input_current(self) -> Optional[float]:
        """Get input current in amperes"""
        return self._get_telemetry_value('status_4', 'current_in')
    
    def get_pid_position(self) -> Optional[float]:
        """Get PID position value"""
        return self._get_telemetry_value('status_4', 'pid_pos_now')
    
    def get_tachometer_value(self) -> Optional[int]:
        """Get tachometer value"""
        return self._get_telemetry_value('status_5', 'tacho_value')
    
    def get_input_voltage(self) -> Optional[float]:
        """Get input voltage in volts"""
        return self._get_telemetry_value('status_5', 'v_in')
    
    def get_adc_voltage_ext(self) -> Optional[float]:
        """Get ADC voltage from EXT channel"""
        return self._get_telemetry_value('status_6', 'adc_1')
    
    def get_adc_voltage_ext2(self) -> Optional[float]:
        """Get ADC voltage from EXT2 channel"""
        return self._get_telemetry_value('status_6', 'adc_2')
    
    def get_adc_voltage_ext3(self) -> Optional[float]:
        """Get ADC voltage from EXT3 channel"""
        return self._get_telemetry_value('status_6', 'adc_3')
    
    def get_servo_value(self) -> Optional[float]:
        """Get servo/PPM value"""
        return self._get_telemetry_value('status_6', 'ppm')
    
    def get_all_telemetry(self) -> Dict[str, Any]:
        """Get all telemetry data in a structured format"""
        data = self._get_live_data()
        
        telemetry = {
            'controller_id': self.controller_id,
            'timestamp': data.get('last_update', 0),
            'motor': {
                'rpm': self.get_rpm(),
                'current': self.get_motor_current(),
                'duty_cycle': self.get_duty_cycle(),
                'temperature': self.get_motor_temperature(),
            },
            'power': {
                'input_voltage': self.get_input_voltage(),
                'input_current': self.get_input_current(),
                'amp_hours_consumed': self.get_amp_hours_consumed(),
                'amp_hours_charged': self.get_amp_hours_charged(),
                'watt_hours_consumed': self.get_watt_hours_consumed(),
                'watt_hours_charged': self.get_watt_hours_charged(),
            },
            'temperatures': {
                'fet': self.get_fet_temperature(),
                'motor': self.get_motor_temperature(),
            },
            'sensors': {
                'tachometer': self.get_tachometer_value(),
                'pid_position': self.get_pid_position(),
                'adc_ext': self.get_adc_voltage_ext(),
                'adc_ext2': self.get_adc_voltage_ext2(),
                'adc_ext3': self.get_adc_voltage_ext3(),
                'servo_value': self.get_servo_value(),
            }
        }
        
        return telemetry
    
    # ==================== WRITE FUNCTIONS ====================
    
    def set_duty_cycle(self, duty_cycle: float) -> bool:
        """
        Set motor duty cycle
        
        Args:
            duty_cycle: Duty cycle from -1.0 to 1.0
            
        Returns:
            True if command sent successfully, False otherwise
        """
        if not -1.0 <= duty_cycle <= 1.0:
            raise ValueError("Duty cycle must be between -1.0 and 1.0")
        
        self._check_command_rate()
        
        try:
            result = {'success': False}
            event = threading.Event()
            
            def callback(success: bool, data: Dict[str, Any]):
                result['success'] = success
                result['data'] = data
                event.set()
            
            self.interface.send_command(
                self.controller_id, 
                'duty', 
                duty_cycle, 
                callback=callback,
                timeout=2.0
            )
            
            # Wait for response
            if event.wait(timeout=2.5):
                return result['success']
            else:
                return False
                
        except Exception as e:
            print(f"Error setting duty cycle: {e}")
            return False
    
    def set_current(self, current: float) -> bool:
        """
        Set motor current
        
        Args:
            current: Current in amperes
            
        Returns:
            True if command sent successfully, False otherwise
        """
        if not -100.0 <= current <= 100.0:
            raise ValueError("Current must be between -100.0 and 100.0 amperes")
        
        self._check_command_rate()
        
        try:
            result = {'success': False}
            event = threading.Event()
            
            def callback(success: bool, data: Dict[str, Any]):
                result['success'] = success
                result['data'] = data
                event.set()
            
            self.interface.send_command(
                self.controller_id, 
                'current', 
                current, 
                callback=callback,
                timeout=2.0
            )
            
            # Wait for response
            if event.wait(timeout=2.5):
                return result['success']
            else:
                return False
                
        except Exception as e:
            print(f"Error setting current: {e}")
            return False
    
    def set_brake_current(self, current: float) -> bool:
        """
        Set brake current
        
        Args:
            current: Brake current in amperes (positive value)
            
        Returns:
            True if command sent successfully, False otherwise
        """
        if not 0.0 <= current <= 100.0:
            raise ValueError("Brake current must be between 0.0 and 100.0 amperes")
        
        self._check_command_rate()
        
        try:
            result = {'success': False}
            event = threading.Event()
            
            def callback(success: bool, data: Dict[str, Any]):
                result['success'] = success
                result['data'] = data
                event.set()
            
            self.interface.send_command(
                self.controller_id, 
                'brake', 
                current, 
                callback=callback,
                timeout=2.0
            )
            
            # Wait for response
            if event.wait(timeout=2.5):
                return result['success']
            else:
                return False
                
        except Exception as e:
            print(f"Error setting brake current: {e}")
            return False
    
    def stop_motor(self) -> bool:
        """Stop the motor by setting duty cycle to 0"""
        return self.set_duty_cycle(0.0)
    
    def is_connected(self) -> bool:
        """Check if controller is connected and responding"""
        data = self._get_live_data()
        if not data or 'last_update' not in data:
            return False
        
        # Consider connected if we received data within last 2 seconds
        return time.time() - data['last_update'] < 2.0


class VESCStudentAPI:
    """Main student API for VESC motor controllers"""
    
    def __init__(self, can_channel: str = 'can0', quiet: bool = True):
        self.system_manager = VESCSystemManager(can_channel, quiet=quiet)
        self.controllers: Dict[int, VESCController] = {}
        self._started = False
    
    def start(self) -> bool:
        """Start the VESC system"""
        if self._started:
            return True
        
        if self.system_manager.start():
            self._started = True
            # Give system time to discover controllers
            time.sleep(2.0)
            return True
        return False
    
    def stop(self):
        """Stop the VESC system"""
        if self._started:
            self.system_manager.stop()
            self._started = False
    
    def get_controller(self, controller_id: int) -> VESCController:
        """Get a controller interface"""
        if not self._started:
            raise RuntimeError("VESC system not started. Call start() first.")
        
        if controller_id not in self.controllers:
            self.controllers[controller_id] = VESCController(controller_id, self.system_manager)
        
        return self.controllers[controller_id]
    
    def get_connected_controllers(self) -> list:
        """Get list of connected controller IDs"""
        if not self._started:
            return []
        
        return self.system_manager.get_controller_ids()
    
    def is_running(self) -> bool:
        """Check if system is running"""
        return self._started and self.system_manager.is_running()


def example_usage():
    """Example usage of the student API"""
    print("VESC Student API Example")
    print("=" * 30)
    
    # Create API instance
    api = VESCStudentAPI()
    
    # Start system
    if not api.start():
        print("Failed to start VESC system")
        return
    
    try:
        # Wait for controller discovery
        time.sleep(6.0)
        
        # Get connected controllers
        controllers = api.get_connected_controllers()
        print(f"Connected controllers: {controllers}")
        
        if not controllers:
            print("No controllers found")
            return
        
        # Use first controller
        controller_id = controllers[0]
        controller = api.get_controller(controller_id)
        
        print(f"\\nUsing controller {controller_id}")
        
        # Read telemetry
        print("\\nTelemetry readings:")
        print(f"  RPM: {controller.get_rpm()}")
        print(f"  Current: {controller.get_motor_current()} A")
        print(f"  Duty Cycle: {controller.get_duty_cycle()}")
        print(f"  Input Voltage: {controller.get_input_voltage()} V")
        print(f"  FET Temperature: {controller.get_fet_temperature()} °C")
        
        # Get all telemetry
        print("\\nAll telemetry:")
        all_data = controller.get_all_telemetry()
        for category, data in all_data.items():
            if isinstance(data, dict):
                print(f"  {category}:")
                for key, value in data.items():
                    print(f"    {key}: {value}")
            else:
                print(f"  {category}: {data}")
        
    except KeyboardInterrupt:
        print("\\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        api.stop()


if __name__ == "__main__":
    example_usage()