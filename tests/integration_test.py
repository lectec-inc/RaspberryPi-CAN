#!/usr/bin/env python3
"""
Integration Test for VESC CAN System
Tests all components together with live VESC hardware.
"""

import time
import sys
from student_vesc_api import VESCStudentAPI


def run_integration_test():
    """Run comprehensive integration test"""
    print("VESC CAN System Integration Test")
    print("=" * 40)
    
    # Initialize API
    vesc_vesc_api = VESCStudentAPI()
    
    # Test 1: System startup
    print("\n1. Testing system startup...")
    if not vesc_api.start():
        print("❌ FAILED: System startup failed")
        return False
    print("✅ PASSED: System started successfully")
    
    # Test 2: Controller discovery
    print("\n2. Testing controller discovery...")
    print("   Waiting for controller discovery (5 seconds)...")
    time.sleep(5.0)
    
    controllers = vesc_api.get_connected_controllers()
    if not controllers:
        print("❌ FAILED: No controllers discovered")
        vesc_api.stop()
        return False
    
    print(f"✅ PASSED: Discovered {len(controllers)} controller(s): {controllers}")
    
    # Use first controller for testing
    controller_id = controllers[0]
    controller = vesc_api.get_controller(controller_id)
    
    # Test 3: Connection status
    print(f"\n3. Testing controller {controller_id} connection...")
    if not controller.is_connected():
        print("❌ FAILED: Controller not connected")
        vesc_api.stop()
        return False
    print("✅ PASSED: Controller is connected")
    
    # Test 4: Telemetry readings
    print(f"\n4. Testing telemetry readings...")
    test_readings = [
        ("RPM", controller.get_rpm),
        ("Motor Current", controller.get_motor_current),
        ("Duty Cycle", controller.get_duty_cycle),
        ("Input Voltage", controller.get_input_voltage),
        ("FET Temperature", controller.get_fet_temperature),
        ("Motor Temperature", controller.get_motor_temperature),
        ("Input Current", controller.get_input_current),
        ("Amp Hours Consumed", controller.get_amp_hours_consumed),
        ("Amp Hours Charged", controller.get_amp_hours_charged),
        ("Watt Hours Consumed", controller.get_watt_hours_consumed),
        ("Watt Hours Charged", controller.get_watt_hours_charged),
        ("PID Position", controller.get_pid_position),
        ("Tachometer", controller.get_tachometer_value),
        ("ADC EXT", controller.get_adc_voltage_ext),
        ("ADC EXT2", controller.get_adc_voltage_ext2),
        ("ADC EXT3", controller.get_adc_voltage_ext3),
        ("Servo Value", controller.get_servo_value),
    ]
    
    failed_readings = []
    for name, func in test_readings:
        try:
            value = func()
            if value is not None:
                print(f"   ✅ {name}: {value}")
            else:
                print(f"   ❌ {name}: No data")
                failed_readings.append(name)
        except Exception as e:
            print(f"   ❌ {name}: Error - {e}")
            failed_readings.append(name)
    
    if failed_readings:
        print(f"❌ FAILED: {len(failed_readings)} readings failed: {failed_readings}")
    else:
        print("✅ PASSED: All telemetry readings successful")
    
    # Test 5: All telemetry function
    print(f"\n5. Testing get_all_telemetry()...")
    try:
        all_data = controller.get_all_telemetry()
        if all_data and 'controller_id' in all_data:
            print(f"   ✅ Retrieved complete telemetry data")
            print(f"   Controller ID: {all_data['controller_id']}")
            print(f"   Timestamp: {all_data['timestamp']}")
            print(f"   Categories: {list(all_data.keys())}")
        else:
            print("   ❌ Failed to retrieve complete telemetry")
    except Exception as e:
        print(f"   ❌ Error getting all telemetry: {e}")
    
    # Test 6: Data freshness
    print(f"\n6. Testing data freshness...")
    current_time = time.time()
    all_data = controller.get_all_telemetry()
    data_age = current_time - all_data['timestamp']
    
    if data_age < 1.0:
        print(f"   ✅ Data is fresh (age: {data_age:.3f} seconds)")
    else:
        print(f"   ❌ Data is stale (age: {data_age:.3f} seconds)")
    
    # Test 7: Command interface (send stop command only for safety)
    print(f"\n7. Testing command interface (stop motor)...")
    try:
        # Only send stop command for safety
        success = controller.stop_motor()
        if success:
            print("   ✅ Stop motor command sent successfully")
        else:
            print("   ❌ Stop motor command failed")
    except Exception as e:
        print(f"   ❌ Error sending stop command: {e}")
    
    # Test 8: System statistics
    print(f"\n8. Testing system statistics...")
    interface = vesc_api.system_manager.get_interface()
    stats = interface.get_statistics()
    
    print(f"   Messages received: {stats['messages_received']}")
    print(f"   Messages parsed: {stats['messages_parsed']}")
    print(f"   Parse errors: {stats['parse_errors']}")
    print(f"   Commands sent: {stats['commands_sent']}")
    
    if stats['messages_received'] > 0 and stats['messages_parsed'] > 0:
        print("   ✅ System statistics look good")
    else:
        print("   ❌ System statistics indicate problems")
    
    # Test 9: System shutdown
    print(f"\n9. Testing system shutdown...")
    vesc_api.stop()
    
    if not vesc_api.is_running():
        print("   ✅ System shutdown successful")
        return True
    else:
        print("   ❌ System shutdown failed")
        return False


def run_performance_test():
    """Run performance test"""
    print("\n" + "=" * 40)
    print("Performance Test")
    print("=" * 40)
    
    vesc_api = VESCStudentAPI()
    
    if not vesc_api.start():
        print("❌ FAILED: System startup failed")
        return False
    
    print("Waiting for controller discovery...")
    time.sleep(5.0)
    
    controllers = vesc_api.get_connected_controllers()
    if not controllers:
        print("❌ FAILED: No controllers discovered")
        vesc_api.stop()
        return False
    
    controller = vesc_api.get_controller(controllers[0])
    
    # Performance test: measure reading speed
    print(f"Testing reading performance...")
    start_time = time.time()
    readings = 0
    
    for _ in range(100):
        rpm = controller.get_rpm()
        current = controller.get_motor_current()
        voltage = controller.get_input_voltage()
        temp = controller.get_fet_temperature()
        
        if rpm is not None and current is not None and voltage is not None and temp is not None:
            readings += 4
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"   Completed {readings} readings in {total_time:.3f} seconds")
    print(f"   Reading rate: {readings/total_time:.1f} readings/second")
    
    # Performance test: measure all telemetry speed
    print(f"Testing get_all_telemetry() performance...")
    start_time = time.time()
    
    for _ in range(10):
        all_data = controller.get_all_telemetry()
        if not all_data:
            break
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print(f"   Completed 10 get_all_telemetry() calls in {total_time:.3f} seconds")
    print(f"   Rate: {10/total_time:.1f} calls/second")
    
    vesc_api.stop()
    return True


def main():
    """Main test runner"""
    print("Starting VESC CAN System Tests")
    print("Make sure VESC is connected and powered on!")
    print()
    
    # Run integration test
    if not run_integration_test():
        print("\n❌ Integration test FAILED")
        sys.exit(1)
    
    # Run performance test
    if not run_performance_test():
        print("\n❌ Performance test FAILED")
        sys.exit(1)
    
    print("\n🎉 All tests PASSED!")
    print("VESC CAN System is working correctly!")


if __name__ == "__main__":
    main()