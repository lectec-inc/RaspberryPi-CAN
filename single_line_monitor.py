#!/usr/bin/env python3
"""
VESC Single Line Monitor
Displays live telemetry on ONE line that updates in place
"""

import time
import sys
import signal
import logging
from threading import Thread, Lock
from enhanced_decoder import EnhancedVESCDecoder
from vesc_interface import VESCInterface

class SingleLineMonitor:
    def __init__(self):
        self.running = False
        self.decoder = EnhancedVESCDecoder()
        self.vesc = None
        self.lock = Lock()
        self.message_count = 0
        self.start_time = time.time()
        
        signal.signal(signal.SIGINT, self._stop)
    
    def _stop(self, signum, frame):
        print("\nStopping...")
        self.running = False
    
    def _can_monitor(self):
        """Background CAN monitoring"""
        while self.running:
            try:
                msg = self.vesc.receive_can_message(timeout=0.1)
                if msg:
                    with self.lock:
                        self.message_count += 1
                    self.decoder.decode_message(msg.arbitration_id, msg.data)
            except:
                time.sleep(0.1)
    
    def run(self):
        # Disable logging
        logging.basicConfig(level=logging.CRITICAL)
        
        print("VESC Monitor")
        print("Duty%   RPM  Temp-C  Volt  Mot-A  Bat-A  Hz")
        
        try:
            self.vesc = VESCInterface()
            self.running = True
            
            # Start background monitoring
            Thread(target=self._can_monitor, daemon=True).start()
            time.sleep(2)  # Wait for data
            
            while self.running:
                data = self.decoder.get_latest_data()
                age = time.time() - data.timestamp if data.timestamp > 0 else 999
                
                if age < 2:
                    with self.lock:
                        rate = self.message_count / (time.time() - self.start_time)
                    
                    # Format values
                    duty = f"{data.duty_cycle_percent or 0:5.1f}"
                    rpm = f"{data.rpm or 0:5.0f}"
                    temp = f"{data.temperature_c or 0:6.1f}"
                    volt = f"{data.voltage_v or 0:5.1f}"
                    mot_a = f"{data.motor_current_a or 0:5.1f}"
                    bat_a = f"{data.battery_current_a or 0:5.1f}"
                    hz = f"{rate:3.0f}"
                    
                    line = f"{duty} {rpm} {temp} {volt} {mot_a} {bat_a} {hz}"
                else:
                    line = "Waiting for data..."
                
                # Overwrite current line
                print(f"\r{line:<50}", end="", flush=True)
                time.sleep(0.2)
        
        except Exception as e:
            print(f"\nError: {e}")
        finally:
            self.running = False
            if self.vesc:
                self.vesc.shutdown()
            
            # Final summary
            data = self.decoder.get_latest_data()
            print(f"\nFinal: Duty={data.duty_cycle_percent:.1f}% RPM={data.rpm:.0f} Temp={data.temperature_c:.1f}C Volt={data.voltage_v:.1f}V")

if __name__ == "__main__":
    SingleLineMonitor().run()