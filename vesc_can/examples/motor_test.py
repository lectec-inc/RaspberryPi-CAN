#!/usr/bin/env python3
"""
VESC Motor Test Example

This example provides comprehensive motor testing functionality.
Includes safety checks, different control modes, and performance measurement.
"""

import vesc_can
import time
import math

def main():
    print("VESC Motor Test Suite")
    print("=" * 40)
    
    # Connect to VESC
    print("Connecting to VESC...")
    vesc = vesc_can.connect_to_vesc()
    
    if not vesc:
        print("❌ Could not connect to VESC!")
        return
    
    print("✅ Connected to VESC!")
    
    try:
        # Pre-test safety checks
        if not safety_check(vesc):
            print("❌ Safety check failed! Aborting tests.")
            return
        
        print("✅ Safety check passed!")
        
        # Run test menu
        while True:
            print("\n" + "=" * 50)
            print("VESC Motor Test Menu")
            print("=" * 50)
            print("1. Basic Movement Test")
            print("2. Speed Ramp Test")
            print("3. Current Control Test")
            print("4. Sine Wave Test")
            print("5. Performance Measurement")
            print("6. Emergency Stop Test")
            print("7. Show Status")
            print("8. Exit")
            
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                basic_movement_test(vesc)
            elif choice == '2':
                speed_ramp_test(vesc)
            elif choice == '3':
                current_control_test(vesc)
            elif choice == '4':
                sine_wave_test(vesc)
            elif choice == '5':
                performance_measurement(vesc)
            elif choice == '6':
                emergency_stop_test(vesc)
            elif choice == '7':
                show_detailed_status(vesc)
            elif choice == '8':
                break
            else:
                print("Invalid choice! Please enter 1-8.")
            
            input("\nPress Enter to continue...")
        
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during tests: {e}")
    finally:
        # Always stop motor
        print("🛑 Ensuring motor is stopped...")
        vesc.stop_motor()
        time.sleep(0.5)

def safety_check(vesc):
    """Perform comprehensive safety checks before testing"""
    print("\n🔍 Performing safety checks...")
    
    # Check for existing faults
    if vesc.has_fault():
        print(f"   ❌ VESC has fault: {vesc.get_fault_code()}")
        return False
    
    # Check voltage
    voltage = vesc.get_voltage()
    if voltage < 5.0:
        print(f"   ❌ Input voltage too low: {voltage:.2f}V (minimum 5V)")
        return False
    
    if voltage > 60.0:
        print(f"   ⚠️  High voltage detected: {voltage:.2f}V - Be careful!")
    
    # Check temperatures
    temp_motor = vesc.get_temp_motor()
    temp_fet = vesc.get_temp_fet()
    
    if temp_motor > 80.0:
        print(f"   ❌ Motor temperature too high: {temp_motor:.1f}°C")
        return False
    
    if temp_fet > 80.0:
        print(f"   ❌ FET temperature too high: {temp_fet:.1f}°C")
        return False
    
    # Check if motor is already spinning
    rpm = abs(vesc.get_rpm())
    if rpm > 100:
        print(f"   ❌ Motor already spinning: {rpm:.0f} RPM - Stop motor first!")
        return False
    
    print(f"   ✅ Voltage: {voltage:.2f}V")
    print(f"   ✅ Motor temp: {temp_motor:.1f}°C")
    print(f"   ✅ FET temp: {temp_fet:.1f}°C")
    print(f"   ✅ Motor stopped: {rpm:.0f} RPM")
    
    return True

def basic_movement_test(vesc):
    """Test basic motor movement in both directions"""
    print("\n🔄 Basic Movement Test")
    print("   Testing basic forward and reverse movement...")
    
    try:
        # Forward movement
        print("   ➡️  Forward movement (10% duty)...")
        vesc.set_duty(0.1)
        monitor_for_duration(vesc, 3.0)
        
        # Stop
        print("   ⏸️  Stopping...")
        vesc.stop_motor()
        time.sleep(1)
        
        # Reverse movement
        print("   ⬅️  Reverse movement (-10% duty)...")
        vesc.set_duty(-0.1)
        monitor_for_duration(vesc, 3.0)
        
        # Stop
        print("   ⏹️  Final stop...")
        vesc.stop_motor()
        
        print("   ✅ Basic movement test completed!")
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        vesc.stop_motor()

def speed_ramp_test(vesc):
    """Test ramping speed up and down"""
    print("\n📈 Speed Ramp Test")
    print("   Ramping speed from 0 to 1000 RPM and back...")
    
    try:
        max_rpm = 1000
        ramp_time = 10.0  # 10 seconds up, 10 seconds down
        steps = 50
        
        print("   📈 Ramping up...")
        for i in range(steps):
            rpm = (i / (steps - 1)) * max_rpm
            vesc.set_rpm(int(rpm))
            
            current_rpm = vesc.get_rpm()
            current = vesc.get_current()
            
            print(f"   Target: {rpm:4.0f} RPM  Actual: {current_rpm:6.0f} RPM  Current: {current:5.2f}A")
            time.sleep(ramp_time / steps)
        
        print("   📉 Ramping down...")
        for i in range(steps):
            rpm = max_rpm * (1 - (i / (steps - 1)))
            vesc.set_rpm(int(rpm))
            
            current_rpm = vesc.get_rpm()
            current = vesc.get_current()
            
            print(f"   Target: {rpm:4.0f} RPM  Actual: {current_rpm:6.0f} RPM  Current: {current:5.2f}A")
            time.sleep(ramp_time / steps)
        
        vesc.stop_motor()
        print("   ✅ Speed ramp test completed!")
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        vesc.stop_motor()

def current_control_test(vesc):
    """Test current control mode"""
    print("\n⚡ Current Control Test")
    print("   Testing precise current control...")
    
    try:
        currents = [0.5, 1.0, 1.5, 2.0, 1.5, 1.0, 0.5, 0.0]
        
        for target_current in currents:
            print(f"   Setting current to {target_current:.1f}A...")
            vesc.set_current(target_current)
            
            # Monitor for 2 seconds
            for _ in range(10):
                actual_current = vesc.get_current()
                rpm = vesc.get_rpm()
                voltage = vesc.get_voltage()
                power = voltage * actual_current
                
                print(f"   Target: {target_current:.1f}A  Actual: {actual_current:.2f}A  "
                      f"RPM: {rpm:5.0f}  Power: {power:5.1f}W")
                time.sleep(0.2)
        
        vesc.stop_motor()
        print("   ✅ Current control test completed!")
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        vesc.stop_motor()

def sine_wave_test(vesc):
    """Test sine wave duty cycle control"""
    print("\n🌊 Sine Wave Test")
    print("   Running sine wave duty cycle pattern...")
    
    try:
        duration = 20.0  # 20 seconds
        frequency = 0.2  # 0.2 Hz (5 second period)
        amplitude = 0.15  # ±15% duty cycle
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            
            # Calculate sine wave duty cycle
            duty = amplitude * math.sin(2 * math.pi * frequency * elapsed)
            vesc.set_duty(duty)
            
            # Monitor
            actual_duty = vesc.get_duty()
            rpm = vesc.get_rpm()
            current = vesc.get_current()
            
            print(f"   Time: {elapsed:5.1f}s  Target Duty: {duty:6.3f}  "
                  f"Actual: {actual_duty:6.3f}  RPM: {rpm:6.0f}  Current: {current:5.2f}A")
            
            time.sleep(0.1)
        
        vesc.stop_motor()
        print("   ✅ Sine wave test completed!")
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        vesc.stop_motor()

def performance_measurement(vesc):
    """Measure motor and controller performance"""
    print("\n📊 Performance Measurement")
    print("   Measuring efficiency and performance...")
    
    try:
        test_currents = [0.5, 1.0, 2.0, 3.0, 5.0]
        results = []
        
        for test_current in test_currents:
            print(f"\n   Testing at {test_current:.1f}A...")
            vesc.set_current(test_current)
            
            # Let it stabilize
            time.sleep(2.0)
            
            # Collect data for 5 seconds
            samples = []
            for _ in range(25):  # 5 seconds at 5Hz
                data = {
                    'current_motor': vesc.get_current(),
                    'current_in': vesc.get_current_in(),
                    'voltage': vesc.get_voltage(),
                    'rpm': vesc.get_rpm(),
                    'temp_motor': vesc.get_temp_motor(),
                    'temp_fet': vesc.get_temp_fet(),
                    'duty': vesc.get_duty()
                }
                samples.append(data)
                time.sleep(0.2)
            
            # Calculate averages
            avg_data = {}
            for key in samples[0].keys():
                avg_data[key] = sum(sample[key] for sample in samples) / len(samples)
            
            # Calculate performance metrics
            power_in = avg_data['voltage'] * avg_data['current_in']
            power_motor = avg_data['voltage'] * avg_data['current_motor']
            efficiency = (power_motor / power_in * 100) if power_in > 0 else 0
            
            result = {
                'test_current': test_current,
                'actual_current': avg_data['current_motor'],
                'input_current': avg_data['current_in'],
                'voltage': avg_data['voltage'],
                'rpm': avg_data['rpm'],
                'power_in': power_in,
                'power_motor': power_motor,
                'efficiency': efficiency,
                'temp_motor': avg_data['temp_motor'],
                'temp_fet': avg_data['temp_fet']
            }
            
            results.append(result)
            
            print(f"   Actual Current: {result['actual_current']:.2f}A")
            print(f"   RPM: {result['rpm']:.0f}")
            print(f"   Power In: {result['power_in']:.1f}W")
            print(f"   Power Motor: {result['power_motor']:.1f}W")
            print(f"   Efficiency: {result['efficiency']:.1f}%")
            print(f"   Motor Temp: {result['temp_motor']:.1f}°C")
            print(f"   FET Temp: {result['temp_fet']:.1f}°C")
        
        vesc.stop_motor()
        
        # Print summary
        print("\n📋 Performance Summary:")
        print("   Current  RPM     Power   Efficiency  Temp_M  Temp_F")
        print("   -------  ------  ------  ----------  ------  ------")
        for r in results:
            print(f"   {r['actual_current']:5.1f}A  {r['rpm']:6.0f}  {r['power_motor']:5.1f}W  "
                  f"{r['efficiency']:8.1f}%  {r['temp_motor']:5.1f}°C  {r['temp_fet']:5.1f}°C")
        
        print("   ✅ Performance measurement completed!")
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        vesc.stop_motor()

def emergency_stop_test(vesc):
    """Test emergency stop functionality"""
    print("\n🚨 Emergency Stop Test")
    print("   Testing emergency stop response...")
    
    try:
        # Start motor spinning
        print("   Starting motor at 20% duty...")
        vesc.set_duty(0.2)
        time.sleep(2)
        
        print("   Motor should be spinning now...")
        rpm_before = vesc.get_rpm()
        print(f"   RPM before stop: {rpm_before:.0f}")
        
        # Emergency stop
        print("   🛑 EMERGENCY STOP!")
        stop_time = time.time()
        vesc.stop_motor()
        
        # Monitor how quickly it stops
        print("   Monitoring stop time...")
        while True:
            elapsed = time.time() - stop_time
            rpm = abs(vesc.get_rpm())
            
            print(f"   Stop time: {elapsed:.2f}s  RPM: {rpm:.0f}")
            
            if rpm < 10 or elapsed > 10:  # Stopped or timeout
                break
            
            time.sleep(0.1)
        
        final_rpm = vesc.get_rpm()
        total_stop_time = time.time() - stop_time
        
        print(f"   ✅ Motor stopped in {total_stop_time:.2f}s")
        print(f"   Final RPM: {final_rpm:.0f}")
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        vesc.stop_motor()

def show_detailed_status(vesc):
    """Show detailed VESC status"""
    print("\n📊 Detailed VESC Status")
    print("=" * 50)
    
    # Basic status
    data = vesc.get_all_data()
    
    print("Motor Status:")
    print(f"  RPM: {data['rpm']:.0f}")
    print(f"  Duty Cycle: {data['duty']:.3f} ({data['duty']*100:.1f}%)")
    print(f"  Position: {data['position']:.2f}°")
    print(f"  Tachometer: {data['tachometer']}")
    
    print("\nElectrical:")
    print(f"  Motor Current: {data['current']:.2f} A")
    print(f"  Input Current: {data['current_in']:.2f} A")
    print(f"  Input Voltage: {data['voltage']:.2f} V")
    print(f"  Power: {data['voltage'] * data['current_in']:.1f} W")
    
    print("\nEnergy:")
    print(f"  Amp Hours: {data['amp_hours']:.3f} Ah")
    print(f"  Amp Hours Charged: {data['amp_hours_charged']:.3f} Ah")
    print(f"  Watt Hours: {data['watt_hours']:.2f} Wh")
    print(f"  Watt Hours Charged: {data['watt_hours_charged']:.2f} Wh")
    
    print("\nTemperatures:")
    print(f"  Motor: {data['temp_motor']:.1f}°C")
    print(f"  FET: {data['temp_fet']:.1f}°C")
    
    print("\nFaults:")
    if data['has_fault']:
        print(f"  ⚠️  FAULT: {data['fault_code']}")
    else:
        print("  ✅ No faults")
    
    # Network status
    print("\nNetwork:")
    network = vesc.get_network_info()
    print(f"  My Node ID: {network['my_node_id']}")
    print(f"  Active VESCs: {len(vesc.get_active_vescs())}")
    
    # Try to get additional info
    try:
        fw_version = vesc.get_firmware_version()
        if fw_version:
            print(f"  Firmware: {fw_version}")
    except:
        pass

def monitor_for_duration(vesc, duration):
    """Monitor VESC for specified duration"""
    start_time = time.time()
    
    while time.time() - start_time < duration:
        elapsed = time.time() - start_time
        data = vesc.get_all_data()
        
        print(f"   [{elapsed:4.1f}s] RPM:{data['rpm']:6.0f}  Current:{data['current']:5.2f}A  "
              f"Voltage:{data['voltage']:5.2f}V  Duty:{data['duty']:6.3f}")
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()