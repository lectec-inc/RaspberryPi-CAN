#!/usr/bin/env python3
"""
Live VESC Data Monitor
Single line display that updates in place - Press Ctrl+C to exit
"""

import time
import sys
import signal
import logging
from threading import Thread, Lock
from enhanced_decoder import EnhancedVESCDecoder
from vesc_interface import VESCInterface

def main():
    # Suppress all logging
    logging.basicConfig(level=logging.CRITICAL)
    
    # Setup variables
    running = True
    decoder = EnhancedVESCDecoder()
    vesc = None
    lock = Lock()
    msg_count = 0
    start_time = time.time()
    
    def stop_handler(signum, frame):
        nonlocal running
        print("\nExiting...")
        running = False
    
    def monitor_can():
        nonlocal msg_count
        while running:
            try:
                msg = vesc.receive_can_message(timeout=0.1)
                if msg:
                    with lock:
                        msg_count += 1
                    decoder.decode_message(msg.arbitration_id, msg.data)
            except:
                time.sleep(0.1)
    
    # Setup signal handler
    signal.signal(signal.SIGINT, stop_handler)
    
    print("VESC Live Data - Press Ctrl+C to exit")
    print("Duty%   RPM  FET°C  Volts  MotA  BatA  Rate")
    
    try:
        # Initialize VESC
        vesc = VESCInterface()
        
        # Start background monitoring
        Thread(target=monitor_can, daemon=True).start()
        time.sleep(1)
        
        while running:
            data = decoder.get_latest_data()
            age = time.time() - data.timestamp if data.timestamp > 0 else 999
            
            if age < 2:
                with lock:
                    rate = msg_count / (time.time() - start_time)
                
                # Format compact display
                line = (f"{data.duty_cycle_percent or 0:5.1f} "
                       f"{data.rpm or 0:5.0f} "
                       f"{data.temperature_c or 0:5.1f} "
                       f"{data.voltage_v or 0:5.1f} "
                       f"{data.motor_current_a or 0:4.1f} "
                       f"{data.battery_current_a or 0:4.1f} "
                       f"{rate:4.0f}")
            else:
                line = "Waiting..."
            
            # Update same line
            print(f"\r{line:<45}", end="", flush=True)
            time.sleep(0.2)
    
    except Exception as e:
        print(f"\nError: {e}")
    
    finally:
        running = False
        if vesc:
            vesc.shutdown()
        
        # Show final values
        data = decoder.get_latest_data()
        if data.timestamp > 0:
            print(f"\nFinal: {data.duty_cycle_percent:.1f}% {data.rpm:.0f}rpm {data.temperature_c:.1f}°C {data.voltage_v:.1f}V")

if __name__ == "__main__":
    main()