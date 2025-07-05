#!/usr/bin/env python3
"""
Basic VESC Control Example

This example shows how to connect to a VESC and perform basic motor control.
Great starting point for high school students learning VESC programming.
"""

import sys
sys.path.insert(0, '/home/pi/RaspberryPi-CAN')

import vesc_can
import time

def main():
    print("VESC Basic Control Example")
    print("=" * 40)
    
    # Connect to VESC (automatically finds the first VESC on network)
    print("Connecting to VESC...")
    vesc = vesc_can.connect_to_vesc()
    
    if not vesc:
        print("❌ Could not connect to VESC!")
        print("Make sure:")
        print("  - CAN interface is up (sudo ip link set can0 up type can bitrate 500000)")
        print("  - VESC is connected and powered on")
        print("  - CAN cables are connected correctly")
        return
    
    print("✅ Connected to VESC!")
    print(f"   VESC ID: {vesc.get_my_node_id()}")
    
    try:
        # Read current status
        print("\n📊 Current Status:")
        vesc.print_status()
        
        # Check for faults
        if vesc.has_fault():
            print(f"⚠️  WARNING: VESC has fault: {vesc.get_fault_code()}")
            print("   Please fix the fault before continuing")
            return
        
        print("\n🎮 Starting motor control demo...")
        
        # Demo 1: Duty cycle control
        print("\n1️⃣  Duty Cycle Control")
        print("   Setting 10% duty cycle for 2 seconds...")
        vesc.set_duty(10.0)  # 10% duty cycle
        time.sleep(2)
        
        print("   Setting -5% duty cycle (reverse) for 2 seconds...")
        vesc.set_duty(-5.0)  # -5% duty cycle (reverse)
        time.sleep(2)
        
        print("   Stopping motor...")
        vesc.stop_motor()
        time.sleep(1)
        
        # Demo 2: Current control
        print("\n2️⃣  Current Control")
        print("   Setting 1A current for 2 seconds...")
        vesc.set_current(1.0)  # 1 Ampere
        time.sleep(2)
        
        print("   Setting brake current (2A) for 1 second...")
        vesc.set_current_brake(2.0)  # 2 Ampere brake
        time.sleep(1)
        
        print("   Coasting motor...")
        vesc.coast_motor()
        time.sleep(1)
        
        # Demo 3: RPM control
        print("\n3️⃣  RPM Control")
        print("   Setting 500 RPM for 3 seconds...")
        vesc.set_rpm(500)  # 500 RPM
        time.sleep(3)
        
        print("   Setting -300 RPM (reverse) for 2 seconds...")
        vesc.set_rpm(-300)  # -300 RPM (reverse)
        time.sleep(2)
        
        print("   Stopping motor...")
        vesc.stop_motor()
        
        # Demo 4: Read values while motor is running
        print("\n4️⃣  Reading Values During Operation")
        print("   Starting motor and reading values for 5 seconds...")
        
        vesc.set_duty(5.0)  # 5% duty cycle
        
        for i in range(10):  # Read for 5 seconds (0.5s intervals)
            data = vesc.get_all_data()
            print(f"   RPM: {data['rpm']:6.0f}  Current: {data['current']:5.2f}A  "
                  f"Voltage: {data['voltage']:5.2f}V  Temp: {data['temp_motor']:4.1f}°C")
            time.sleep(0.5)
        
        print("   Stopping motor...")
        vesc.stop_motor()
        
        print("\n✅ Demo completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
    finally:
        # Always stop the motor at the end
        print("🛑 Ensuring motor is stopped...")
        vesc.stop_motor()
        time.sleep(0.5)
        
        # Show final status
        print("\n📊 Final Status:")
        vesc.print_status()

if __name__ == "__main__":
    main()