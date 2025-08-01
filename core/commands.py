"""
VESC CAN Command Encoder
Encodes commands for VESC motor controllers over CAN bus.
"""

import struct
from typing import Tuple
from enum import IntEnum


class CANCommandType(IntEnum):
    """CAN command types from VESC firmware"""
    CAN_PACKET_SET_DUTY = 0
    CAN_PACKET_SET_CURRENT = 1
    CAN_PACKET_SET_CURRENT_BRAKE = 2
    # Note: IMU data is typically requested via serial, not direct CAN


class VESCCommandEncoder:
    """Encoder for VESC CAN commands"""
    
    def __init__(self):
        pass
    
    def encode_set_duty_cycle(self, controller_id: int, duty_cycle: float) -> Tuple[int, bytes]:
        """
        Encode setDutyCycle command
        
        Args:
            controller_id: VESC controller ID (0-255)
            duty_cycle: Duty cycle from -1.0 to 1.0
            
        Returns:
            Tuple of (CAN_ID, data_bytes)
        """
        # Validate inputs
        if not 0 <= controller_id <= 255:
            raise ValueError("Controller ID must be 0-255")
        if not -1.0 <= duty_cycle <= 1.0:
            raise ValueError("Duty cycle must be -1.0 to 1.0")
        
        # Calculate CAN ID: controller_id | (packet_type << 8)
        can_id = controller_id | (CANCommandType.CAN_PACKET_SET_DUTY << 8)
        
        # Scale duty cycle: duty * 100000
        duty_scaled = int(duty_cycle * 100000)
        
        # Encode as 32-bit signed integer, big-endian
        data = struct.pack('>i', duty_scaled)
        
        return can_id, data
    
    def encode_set_current(self, controller_id: int, current: float) -> Tuple[int, bytes]:
        """
        Encode setCurrent command
        
        Args:
            controller_id: VESC controller ID (0-255)
            current: Current in amperes
            
        Returns:
            Tuple of (CAN_ID, data_bytes)
        """
        # Validate inputs
        if not 0 <= controller_id <= 255:
            raise ValueError("Controller ID must be 0-255")
        # Note: Current limits depend on VESC configuration, so we allow reasonable range
        if not -100.0 <= current <= 100.0:
            raise ValueError("Current must be -100.0 to 100.0 amperes")
        
        # Calculate CAN ID: controller_id | (packet_type << 8)
        can_id = controller_id | (CANCommandType.CAN_PACKET_SET_CURRENT << 8)
        
        # Scale current: current * 1000 (amperes to milliamperes)
        current_scaled = int(current * 1000)
        
        # Encode as 32-bit signed integer, big-endian
        data = struct.pack('>i', current_scaled)
        
        return can_id, data
    
    def encode_set_current_brake(self, controller_id: int, current: float) -> Tuple[int, bytes]:
        """
        Encode setCurrentBrake command
        
        Args:
            controller_id: VESC controller ID (0-255)
            current: Braking current in amperes (positive value)
            
        Returns:
            Tuple of (CAN_ID, data_bytes)
        """
        # Validate inputs
        if not 0 <= controller_id <= 255:
            raise ValueError("Controller ID must be 0-255")
        if not 0.0 <= current <= 100.0:
            raise ValueError("Braking current must be 0.0 to 100.0 amperes")
        
        # Calculate CAN ID: controller_id | (packet_type << 8)
        can_id = controller_id | (CANCommandType.CAN_PACKET_SET_CURRENT_BRAKE << 8)
        
        # Scale current: current * 1000 (amperes to milliamperes)
        current_scaled = int(current * 1000)
        
        # Encode as 32-bit signed integer, big-endian
        data = struct.pack('>i', current_scaled)
        
        return can_id, data
    
    def encode_get_imu_data(self, controller_id: int, mask: int = 0xFFFF) -> Tuple[int, bytes]:
        """
        Encode getImuData command
        
        Note: IMU data is typically requested via serial communication to VESC,
        not as a direct CAN packet. This method prepares the command for serial
        transmission over CAN if supported by the VESC firmware.
        
        Args:
            controller_id: VESC controller ID (0-255)
            mask: Bitmask specifying which IMU data fields to retrieve
            
        Returns:
            Tuple of (CAN_ID, data_bytes)
        """
        # Validate inputs
        if not 0 <= controller_id <= 255:
            raise ValueError("Controller ID must be 0-255")
        if not 0 <= mask <= 0xFFFF:
            raise ValueError("Mask must be 0-65535")
        
        # Note: This is a custom implementation since IMU data is typically serial
        # We'll use a custom packet type for IMU requests
        # This may need to be adjusted based on actual VESC firmware implementation
        can_id = controller_id | (0x80 << 8)  # Custom packet type for IMU
        
        # Encode command ID (65) and mask
        data = struct.pack('>BH', 65, mask)  # 1 byte command + 2 byte mask
        
        return can_id, data
    
    def validate_command_response(self, can_id: int, data: bytes, expected_controller_id: int) -> bool:
        """
        Validate that a CAN response matches the expected controller ID
        
        Args:
            can_id: Received CAN ID
            data: Received data bytes
            expected_controller_id: Expected controller ID
            
        Returns:
            True if response is valid for the controller
        """
        received_controller_id = can_id & 0xFF
        return received_controller_id == expected_controller_id


def test_command_encoding():
    """Test function to verify command encoding"""
    encoder = VESCCommandEncoder()
    
    # Test setDutyCycle
    print("Testing setDutyCycle encoding:")
    can_id, data = encoder.encode_set_duty_cycle(74, 0.5)
    print(f"  Controller 74, Duty 0.5: CAN ID = 0x{can_id:08X}, Data = {data.hex()}")
    
    can_id, data = encoder.encode_set_duty_cycle(74, -0.25)
    print(f"  Controller 74, Duty -0.25: CAN ID = 0x{can_id:08X}, Data = {data.hex()}")
    
    # Test setCurrent
    print("\nTesting setCurrent encoding:")
    can_id, data = encoder.encode_set_current(74, 10.5)
    print(f"  Controller 74, Current 10.5A: CAN ID = 0x{can_id:08X}, Data = {data.hex()}")
    
    can_id, data = encoder.encode_set_current(74, -5.0)
    print(f"  Controller 74, Current -5.0A: CAN ID = 0x{can_id:08X}, Data = {data.hex()}")
    
    # Test setCurrentBrake
    print("\nTesting setCurrentBrake encoding:")
    can_id, data = encoder.encode_set_current_brake(74, 3.0)
    print(f"  Controller 74, Brake 3.0A: CAN ID = 0x{can_id:08X}, Data = {data.hex()}")
    
    # Test getImuData
    print("\nTesting getImuData encoding:")
    can_id, data = encoder.encode_get_imu_data(74, 0xFFFF)
    print(f"  Controller 74, IMU All: CAN ID = 0x{can_id:08X}, Data = {data.hex()}")


if __name__ == "__main__":
    test_command_encoding()