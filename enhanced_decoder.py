#!/usr/bin/env python3
"""
Enhanced VESC Decoder - Extract more telemetry fields
Analyzes CAN data to find RPM, Current, Duty Cycle, etc.
"""

import struct
import time
from dataclasses import dataclass
from typing import Optional

@dataclass
class CompleteVESCData:
    """Complete VESC telemetry data structure"""
    temperature_c: Optional[float] = None
    voltage_v: Optional[float] = None
    duty_cycle_percent: Optional[float] = None
    rpm: Optional[float] = None
    motor_current_a: Optional[float] = None
    battery_current_a: Optional[float] = None
    timestamp: float = 0.0
    raw_data: dict = None
    
    def __post_init__(self):
        if self.raw_data is None:
            self.raw_data = {}

class EnhancedVESCDecoder:
    """Enhanced decoder to extract all available VESC data"""
    
    def __init__(self):
        self.latest_data = CompleteVESCData()
        
    def _try_decode_values(self, data: bytes, scale_factors: list) -> list:
        """Try to decode data with different scale factors"""
        values = []
        
        # Try 16-bit values at different offsets
        for offset in range(0, len(data)-1, 2):
            if offset + 2 <= len(data):
                raw_val = struct.unpack('>H', data[offset:offset+2])[0]
                for scale in scale_factors:
                    scaled_val = raw_val / scale
                    values.append((offset, scaled_val, scale, 'uint16'))
        
        # Try 32-bit values at different offsets
        for offset in range(0, len(data)-3, 4):
            if offset + 4 <= len(data):
                try:
                    # Try as 32-bit integer
                    raw_val = struct.unpack('>I', data[offset:offset+4])[0]
                    for scale in scale_factors:
                        scaled_val = raw_val / scale
                        values.append((offset, scaled_val, scale, 'uint32'))
                except:
                    pass
                
                try:
                    # Try as 32-bit signed integer
                    raw_val = struct.unpack('>i', data[offset:offset+4])[0]
                    for scale in scale_factors:
                        scaled_val = raw_val / scale
                        values.append((offset, scaled_val, scale, 'int32'))
                except:
                    pass
                
                try:
                    # Try as float
                    float_val = struct.unpack('>f', data[offset:offset+4])[0]
                    values.append((offset, float_val, 1.0, 'float'))
                except:
                    pass
        
        return values
    
    def decode_message(self, can_id: int, data: bytes) -> Optional[CompleteVESCData]:
        """Decode a CAN message and extract all possible values"""
        
        result = CompleteVESCData()
        result.timestamp = time.time()
        result.raw_data = {'can_id': can_id, 'data': data.hex()}
        
        # Known decodings from previous analysis
        if can_id == 0x702:
            # Voltage data
            if len(data) >= 2:
                voltage_raw = struct.unpack('>H', data[:2])[0]
                result.voltage_v = voltage_raw / 1000.0
                self.latest_data.voltage_v = result.voltage_v
                self.latest_data.timestamp = result.timestamp
                return result
                
        elif can_id == 0x54A:
            # Temperature data and potentially other values
            if len(data) >= 4:
                # Known temperature locations
                for offset in [2, 4, 6]:
                    if offset + 2 <= len(data):
                        temp_raw = struct.unpack('>H', data[offset:offset+2])[0]
                        temp_c = temp_raw / 1000.0
                        
                        if 10.0 <= temp_c <= 50.0:
                            result.temperature_c = temp_c
                            self.latest_data.temperature_c = temp_c
                            self.latest_data.timestamp = result.timestamp
                            break
                
                # Try to find other values in this message
                all_values = self._try_decode_values(data, [1, 10, 100, 1000, 10000])
                
                for offset, value, scale, data_type in all_values:
                    # Look for reasonable RPM values (0-10000)
                    if 0 <= value <= 10000 and scale in [1, 10]:
                        if not self.latest_data.rpm or abs(value) > 10:  # Prefer non-zero values
                            result.rpm = value
                            self.latest_data.rpm = value
                    
                    # Look for reasonable duty cycle (0-100%)
                    if 0 <= value <= 100 and scale in [100, 1000]:
                        result.duty_cycle_percent = value
                        self.latest_data.duty_cycle_percent = value
                    
                    # Look for reasonable current values (-50A to 50A)
                    if -50 <= value <= 50 and scale in [100, 1000]:
                        if not self.latest_data.motor_current_a:
                            result.motor_current_a = value
                            self.latest_data.motor_current_a = value
                        elif not self.latest_data.battery_current_a:
                            result.battery_current_a = value
                            self.latest_data.battery_current_a = value
                
                return result
        
        elif can_id == 0x74A:
            # Analyze this ID for additional data
            all_values = self._try_decode_values(data, [1, 10, 100, 1000])
            
            for offset, value, scale, data_type in all_values:
                # Look for RPM in this message
                if 0 <= value <= 10000 and scale in [1, 10]:
                    result.rpm = value
                    self.latest_data.rpm = value
                    self.latest_data.timestamp = result.timestamp
                    return result
        
        elif can_id == 0x502:
            # Analyze ESP32 data - might contain some motor data
            all_values = self._try_decode_values(data, [1, 10, 100, 1000])
            
            for offset, value, scale, data_type in all_values:
                # Look for duty cycle or current values
                if 0 <= value <= 100 and scale == 100:
                    if not self.latest_data.duty_cycle_percent:
                        result.duty_cycle_percent = value
                        self.latest_data.duty_cycle_percent = value
                        self.latest_data.timestamp = result.timestamp
                        return result
        
        return None
    
    def get_latest_data(self) -> CompleteVESCData:
        """Get the latest combined data"""
        return self.latest_data

def test_enhanced_decoder():
    """Test the enhanced decoder with live data"""
    print("🔍 Testing Enhanced VESC Decoder...")
    print("-" * 60)
    
    from vesc_interface import VESCInterface
    
    decoder = EnhancedVESCDecoder()
    
    with VESCInterface() as vesc:
        print("Analyzing CAN data for all telemetry values...")
        
        for i in range(100):
            msg = vesc.receive_can_message(timeout=1.0)
            if msg:
                decoded = decoder.decode_message(msg.arbitration_id, msg.data)
                
                if decoded or i % 10 == 0:  # Show progress every 10 messages
                    latest = decoder.get_latest_data()
                    
                    temp_str = f"{latest.temperature_c:.1f}°C" if latest.temperature_c else "N/A"
                    volt_str = f"{latest.voltage_v:.1f}V" if latest.voltage_v else "N/A"
                    duty_str = f"{latest.duty_cycle_percent:.1f}%" if latest.duty_cycle_percent else "N/A"
                    rpm_str = f"{latest.rpm:.0f}" if latest.rpm else "N/A"
                    motor_i_str = f"{latest.motor_current_a:.1f}A" if latest.motor_current_a else "N/A"
                    batt_i_str = f"{latest.battery_current_a:.1f}A" if latest.battery_current_a else "N/A"
                    
                    print(f"Sample {i+1:3d}: "
                          f"Temp: {temp_str:7s} | "
                          f"Volt: {volt_str:7s} | "
                          f"Duty: {duty_str:7s} | "
                          f"RPM: {rpm_str:6s} | "
                          f"Motor I: {motor_i_str:7s} | "
                          f"Batt I: {batt_i_str:7s}")
        
        # Final summary
        final_data = decoder.get_latest_data()
        print(f"\nFinal Decoded Values:")
        print(f"  Temperature: {final_data.temperature_c:.1f}°C" if final_data.temperature_c else "  Temperature: Not found")
        print(f"  Voltage: {final_data.voltage_v:.1f}V" if final_data.voltage_v else "  Voltage: Not found")
        print(f"  Duty Cycle: {final_data.duty_cycle_percent:.1f}%" if final_data.duty_cycle_percent else "  Duty Cycle: Not found")
        print(f"  RPM: {final_data.rpm:.0f}" if final_data.rpm else "  RPM: Not found")
        print(f"  Motor Current: {final_data.motor_current_a:.1f}A" if final_data.motor_current_a else "  Motor Current: Not found")
        print(f"  Battery Current: {final_data.battery_current_a:.1f}A" if final_data.battery_current_a else "  Battery Current: Not found")

if __name__ == "__main__":
    test_enhanced_decoder()