#!/usr/bin/env python3
"""
VESC Sensor Reading Example

This example shows how to read all available sensor data from a VESC.
Demonstrates both fast cached data and slower on-demand data.
"""

import vesc_can
import time
import json

def main():
    print("VESC Sensor Reading Example")
    print("=" * 40)
    
    # Connect to VESC
    print("Connecting to VESC...")
    vesc = vesc_can.connect_to_vesc()
    
    if not vesc:
        print("❌ Could not connect to VESC!")
        return
    
    print("✅ Connected to VESC!")
    
    try:
        # Check network status
        print("\n🌐 Network Information:")
        network_info = vesc.get_network_info()
        print(f"   My Node ID: {network_info['my_node_id']}")
        print(f"   Total Nodes: {network_info['total_nodes']}")
        print(f"   VESC Nodes: {network_info['vesc_nodes']}")
        print(f"   Pi Nodes: {network_info['raspberry_pi_nodes']}")
        
        # Show active VESCs
        active_vescs = vesc.get_active_vescs()
        print(f"\n📡 Active VESCs: {list(active_vescs.keys())}")
        
        # Fast sensor readings (from cache - updated at 50Hz)
        print("\n⚡ Fast Sensor Readings (from cache):")
        print("   These values are updated automatically at 50Hz")
        print("   " + "-" * 60)
        
        for i in range(20):  # Read for 10 seconds
            data = vesc.get_all_data()
            
            print(f"   Time: {time.time():.2f}")
            print(f"   Motor - RPM: {data['rpm']:8.0f}  Current: {data['current']:6.2f}A  Duty: {data['duty']:6.3f}")
            print(f"   Power - Voltage: {data['voltage']:5.2f}V  Power: {data['voltage']*data['current_in']:6.1f}W")
            print(f"   Energy - Ah: {data['amp_hours']:6.3f}  Wh: {data['watt_hours']:6.2f}")
            print(f"   Temps - Motor: {data['temp_motor']:5.1f}°C  FET: {data['temp_fet']:5.1f}°C")
            print(f"   Position: {data['position']:8.2f}°  Tach: {data['tachometer']:8d}")
            
            if data['has_fault']:
                print(f"   ⚠️  FAULT: {data['fault_code']}")
            else:
                print("   ✅ No faults")
            
            print("   " + "-" * 60)
            time.sleep(0.5)
        
        # Slower on-demand readings
        print("\n🐌 On-Demand Sensor Readings:")
        print("   These require UART requests and take 50-200ms each")
        
        print("\n   Reading PPM input...")
        ppm = vesc.get_decoded_ppm()
        if ppm is not None:
            print(f"   PPM Value: {ppm:.3f}")
        else:
            print("   PPM: Not available")
        
        print("\n   Reading ADC inputs...")
        adc = vesc.get_decoded_adc()
        if adc:
            print(f"   ADC1: {adc['adc_value']:.3f} ({adc['adc_voltage']:.3f}V)")
            print(f"   ADC2: {adc['adc_value2']:.3f} ({adc['adc_voltage2']:.3f}V)")
        else:
            print("   ADC: Not available")
        
        print("\n   Reading firmware version...")
        fw_version = vesc.get_firmware_version()
        if fw_version:
            print(f"   Firmware: {fw_version}")
        else:
            print("   Firmware: Not available")
        
        # Continuous monitoring mode
        print("\n📊 Continuous Monitoring Mode")
        print("   Press Ctrl+C to stop...")
        print("   " + "=" * 80)
        
        start_time = time.time()
        
        while True:
            current_time = time.time()
            elapsed = current_time - start_time
            
            # Get all fast data
            data = vesc.get_all_data()
            
            # Create a monitoring display
            print(f"\r   [{elapsed:6.1f}s] "
                  f"RPM:{data['rpm']:6.0f} "
                  f"I:{data['current']:5.2f}A "
                  f"V:{data['voltage']:5.2f}V "
                  f"Duty:{data['duty']:6.3f} "
                  f"Tm:{data['temp_motor']:4.1f}°C "
                  f"Tf:{data['temp_fet']:4.1f}°C "
                  f"{'FAULT' if data['has_fault'] else 'OK':5s}", 
                  end='', flush=True)
            
            time.sleep(0.1)  # 10Hz update rate
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Monitoring stopped by user")
    except Exception as e:
        print(f"\n❌ Error reading sensors: {e}")
    
    print("\n✅ Sensor reading example completed!")

def save_sensor_log():
    """Bonus function: Save sensor data to a file"""
    print("\n💾 Bonus: Saving sensor data to file...")
    
    vesc = vesc_can.connect_to_vesc()
    if not vesc:
        return
    
    log_data = []
    
    try:
        print("   Collecting data for 30 seconds...")
        start_time = time.time()
        
        while time.time() - start_time < 30:
            data = vesc.get_all_data()
            log_data.append(data)
            time.sleep(0.1)  # 10Hz logging
        
        # Save to JSON file
        filename = f"vesc_log_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"   ✅ Saved {len(log_data)} data points to {filename}")
        
    except Exception as e:
        print(f"   ❌ Error saving log: {e}")

if __name__ == "__main__":
    main()
    
    # Uncomment the line below to also save a data log
    # save_sensor_log()