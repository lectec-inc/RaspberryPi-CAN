#!/usr/bin/env python3
"""
VESC Diagnostic Check
Quick diagnostic to troubleshoot telemetry and motor control issues
"""

from student_api import VESCStudentAPI
import time

def main():
    print("=== VESC Diagnostic Check ===\n")
    
    # Create API instance
    print("1. Creating VESC API...")
    vesc_api = VESCStudentAPI()
    
    # Start system
    print("2. Starting VESC system...")
    if not vesc_api.start():
        print("❌ Failed to start VESC system!")
        print("Check:")
        print("   - CAN interface is up: sudo ip link show can0")
        print("   - VESC is powered on and connected")
        return
    
    print("✅ VESC system started successfully")
    
    # Get controller
    print("3. Getting controller (ID 74)...")
    vesc = vesc_api.get_controller(74)
    
    if not vesc:
        print("❌ Failed to get VESC controller!")
        print("Check:")
        print("   - VESC ID is correct (should be 74)")
        print("   - VESC is sending status messages")
        print("   - CAN bus is working: candump can0")
        return
    
    print("✅ Got VESC controller")
    
    # Check connection
    print("4. Checking connection...")
    if not vesc.is_connected():
        print("❌ VESC not responding!")
        print("Check:")
        print("   - VESC is sending status messages at 50Hz")
        print("   - Run: candump can0 | grep 74")
        return
    
    print("✅ VESC is connected and responding")
    
    # Get raw live data
    print("5. Getting raw live data...")
    live_data = vesc._get_live_data()
    
    if not live_data:
        print("❌ No live data received!")
        return
    
    print("✅ Raw live data received:")
    for key, value in live_data.items():
        print(f"   {key}: {value}")
    
    # Test specific telemetry values
    print("\n6. Testing telemetry readings...")
    
    # Test each status message
    status_tests = [
        ('RPM', 'status_1', 'rpm', vesc.get_rpm),
        ('Current', 'status_1', 'current', vesc.get_motor_current),
        ('Duty Cycle', 'status_1', 'duty_cycle', vesc.get_duty_cycle),
        ('Voltage', 'status_5', 'v_in', vesc.get_input_voltage),
        ('FET Temp', 'status_4', 'temp_fet', vesc.get_fet_temperature),
        ('Motor Temp', 'status_4', 'temp_motor', vesc.get_motor_temperature),
    ]
    
    for name, status_type, field, func in status_tests:
        raw_value = vesc._get_telemetry_value(status_type, field)
        api_value = func()
        
        print(f"   {name}:")
        print(f"     Raw ({status_type}.{field}): {raw_value}")
        print(f"     API: {api_value}")
        
        if raw_value is None:
            print(f"     ❌ No {status_type} data received!")
        elif api_value is None:
            print(f"     ❌ API returned None but raw data exists!")
        else:
            print(f"     ✅ Working")
    
    # Test get_all_telemetry
    print("\n7. Testing get_all_telemetry()...")
    all_data = vesc.get_all_telemetry()
    
    if all_data:
        print("✅ get_all_telemetry() working")
        print(f"   Motor RPM: {all_data['motor']['rpm']}")
        print(f"   Input Voltage: {all_data['power']['input_voltage']}")
        print(f"   FET Temp: {all_data['temperatures']['fet']}")
    else:
        print("❌ get_all_telemetry() returned None")
    
    print("\n=== Diagnostic Complete ===")
    
    # Stop system
    vesc_api.stop()

if __name__ == "__main__":
    main()