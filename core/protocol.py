"""
VESC CAN Protocol Parser
Parses CAN status messages 1-6 based on VESC firmware reference files.
"""

import struct
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import IntEnum


class CANPacketType(IntEnum):
    """CAN packet types from VESC firmware"""
    CAN_PACKET_STATUS = 0x9
    CAN_PACKET_STATUS_2 = 0xE
    CAN_PACKET_STATUS_3 = 0xF
    CAN_PACKET_STATUS_4 = 0x10
    CAN_PACKET_STATUS_5 = 0x1B
    CAN_PACKET_STATUS_6 = 0x3A


@dataclass
class VESCStatus1:
    """Status 1: RPM, Current, Duty Cycle"""
    rpm: float
    current: float
    duty_cycle: float
    
    
@dataclass
class VESCStatus2:
    """Status 2: Amp Hours"""
    amp_hours: float
    amp_hours_charged: float
    
    
@dataclass
class VESCStatus3:
    """Status 3: Watt Hours"""
    watt_hours: float
    watt_hours_charged: float
    
    
@dataclass
class VESCStatus4:
    """Status 4: Temperatures, Input Current, PID Position"""
    temp_fet: float
    temp_motor: float
    current_in: float
    pid_pos_now: float
    
    
@dataclass
class VESCStatus5:
    """Status 5: Tachometer, Input Voltage"""
    tacho_value: int
    v_in: float
    
    
@dataclass
class VESCStatus6:
    """Status 6: ADC Voltages, PPM"""
    adc_1: float
    adc_2: float
    adc_3: float
    ppm: float


class VESCProtocolParser:
    """Parser for VESC CAN protocol messages"""
    
    def __init__(self):
        self.controller_id_mask = 0xFF
        
    def extract_controller_id(self, can_id: int) -> int:
        """Extract controller ID from CAN ID"""
        return can_id & self.controller_id_mask
        
    def extract_packet_type(self, can_id: int) -> int:
        """Extract packet type from CAN ID"""
        return (can_id >> 8) & 0xFF
        
    def parse_status_1(self, data: bytes) -> VESCStatus1:
        """Parse Status 1: RPM, Current, Duty Cycle"""
        if len(data) < 8:
            raise ValueError("Status 1 packet too short")
            
        # RPM: bytes 0-3 (32-bit signed, big-endian)
        rpm = struct.unpack('>i', data[0:4])[0]
        
        # Current: bytes 4-5 (16-bit signed, big-endian, scale /10.0)
        current_raw = struct.unpack('>h', data[4:6])[0]
        current = current_raw / 10.0
        
        # Duty Cycle: bytes 6-7 (16-bit signed, big-endian, scale /1000.0)
        duty_raw = struct.unpack('>h', data[6:8])[0]
        duty_cycle = duty_raw / 1000.0
        
        return VESCStatus1(rpm=rpm, current=current, duty_cycle=duty_cycle)
        
    def parse_status_2(self, data: bytes) -> VESCStatus2:
        """Parse Status 2: Amp Hours"""
        if len(data) < 8:
            raise ValueError("Status 2 packet too short")
            
        # Amp Hours: bytes 0-3 (32-bit signed, big-endian, scale /10000.0)
        amp_hours_raw = struct.unpack('>i', data[0:4])[0]
        amp_hours = amp_hours_raw / 10000.0
        
        # Amp Hours Charged: bytes 4-7 (32-bit signed, big-endian, scale /10000.0)
        amp_hours_charged_raw = struct.unpack('>i', data[4:8])[0]
        amp_hours_charged = amp_hours_charged_raw / 10000.0
        
        return VESCStatus2(amp_hours=amp_hours, amp_hours_charged=amp_hours_charged)
        
    def parse_status_3(self, data: bytes) -> VESCStatus3:
        """Parse Status 3: Watt Hours"""
        if len(data) < 8:
            raise ValueError("Status 3 packet too short")
            
        # Watt Hours: bytes 0-3 (32-bit signed, big-endian, scale /10000.0)
        watt_hours_raw = struct.unpack('>i', data[0:4])[0]
        watt_hours = watt_hours_raw / 10000.0
        
        # Watt Hours Charged: bytes 4-7 (32-bit signed, big-endian, scale /10000.0)
        watt_hours_charged_raw = struct.unpack('>i', data[4:8])[0]
        watt_hours_charged = watt_hours_charged_raw / 10000.0
        
        return VESCStatus3(watt_hours=watt_hours, watt_hours_charged=watt_hours_charged)
        
    def parse_status_4(self, data: bytes) -> VESCStatus4:
        """Parse Status 4: Temperatures, Input Current, PID Position"""
        if len(data) < 8:
            raise ValueError("Status 4 packet too short")
            
        # FET Temperature: bytes 0-1 (16-bit signed, big-endian, scale /10.0)
        temp_fet_raw = struct.unpack('>h', data[0:2])[0]
        temp_fet = temp_fet_raw / 10.0
        
        # Motor Temperature: bytes 2-3 (16-bit signed, big-endian, scale /10.0)
        temp_motor_raw = struct.unpack('>h', data[2:4])[0]
        temp_motor = temp_motor_raw / 10.0
        
        # Input Current: bytes 4-5 (16-bit signed, big-endian, scale /10.0)
        current_in_raw = struct.unpack('>h', data[4:6])[0]
        current_in = current_in_raw / 10.0
        
        # PID Position: bytes 6-7 (16-bit signed, big-endian, scale /50.0)
        pid_pos_raw = struct.unpack('>h', data[6:8])[0]
        pid_pos_now = pid_pos_raw / 50.0
        
        return VESCStatus4(temp_fet=temp_fet, temp_motor=temp_motor, 
                          current_in=current_in, pid_pos_now=pid_pos_now)
        
    def parse_status_5(self, data: bytes) -> VESCStatus5:
        """Parse Status 5: Tachometer, Input Voltage"""
        if len(data) < 6:
            raise ValueError("Status 5 packet too short")
            
        # Tachometer Value: bytes 0-3 (32-bit signed, big-endian)
        tacho_value = struct.unpack('>i', data[0:4])[0]
        
        # Input Voltage: bytes 4-5 (16-bit signed, big-endian, scale /10.0)
        v_in_raw = struct.unpack('>h', data[4:6])[0]
        v_in = v_in_raw / 10.0
        
        return VESCStatus5(tacho_value=tacho_value, v_in=v_in)
        
    def parse_status_6(self, data: bytes) -> VESCStatus6:
        """Parse Status 6: ADC Voltages, PPM"""
        if len(data) < 8:
            raise ValueError("Status 6 packet too short")
            
        # ADC 1: bytes 0-1 (16-bit signed, big-endian, scale /1000.0)
        adc_1_raw = struct.unpack('>h', data[0:2])[0]
        adc_1 = adc_1_raw / 1000.0
        
        # ADC 2: bytes 2-3 (16-bit signed, big-endian, scale /1000.0)
        adc_2_raw = struct.unpack('>h', data[2:4])[0]
        adc_2 = adc_2_raw / 1000.0
        
        # ADC 3: bytes 4-5 (16-bit signed, big-endian, scale /1000.0)
        adc_3_raw = struct.unpack('>h', data[4:6])[0]
        adc_3 = adc_3_raw / 1000.0
        
        # PPM: bytes 6-7 (16-bit signed, big-endian, scale /1000.0)
        ppm_raw = struct.unpack('>h', data[6:8])[0]
        ppm = ppm_raw / 1000.0
        
        return VESCStatus6(adc_1=adc_1, adc_2=adc_2, adc_3=adc_3, ppm=ppm)
        
    def parse_message(self, can_id: int, data: bytes) -> Optional[Dict[str, Any]]:
        """Parse any VESC CAN message and return structured data"""
        controller_id = self.extract_controller_id(can_id)
        packet_type = self.extract_packet_type(can_id)
        
        try:
            if packet_type == CANPacketType.CAN_PACKET_STATUS:
                status = self.parse_status_1(data)
                return {
                    'controller_id': controller_id,
                    'type': 'status_1',
                    'data': status
                }
            elif packet_type == CANPacketType.CAN_PACKET_STATUS_2:
                status = self.parse_status_2(data)
                return {
                    'controller_id': controller_id,
                    'type': 'status_2',
                    'data': status
                }
            elif packet_type == CANPacketType.CAN_PACKET_STATUS_3:
                status = self.parse_status_3(data)
                return {
                    'controller_id': controller_id,
                    'type': 'status_3',
                    'data': status
                }
            elif packet_type == CANPacketType.CAN_PACKET_STATUS_4:
                status = self.parse_status_4(data)
                return {
                    'controller_id': controller_id,
                    'type': 'status_4',
                    'data': status
                }
            elif packet_type == CANPacketType.CAN_PACKET_STATUS_5:
                status = self.parse_status_5(data)
                return {
                    'controller_id': controller_id,
                    'type': 'status_5',
                    'data': status
                }
            elif packet_type == CANPacketType.CAN_PACKET_STATUS_6:
                status = self.parse_status_6(data)
                return {
                    'controller_id': controller_id,
                    'type': 'status_6',
                    'data': status
                }
            else:
                # Unknown packet type
                return None
                
        except Exception as e:
            print(f"Error parsing CAN message {can_id:08X}: {e}")
            return None