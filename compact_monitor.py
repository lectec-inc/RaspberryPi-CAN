#!/usr/bin/env python3
"""
VESC Compact Monitor - Single line real-time display
Shows: Duty, RPM, Current, Temperature, Motor Current, Battery Current
Press Ctrl+C to exit
"""

import time
import sys
import signal
import logging
from threading import Lock, Thread
from enhanced_decoder import EnhancedVESCDecoder
from vesc_interface import VESCInterface

class CompactVESCMonitor:
    """Compact single-line VESC monitor"""
    
    def __init__(self):
        self.running = False
        self.vesc = None
        self.decoder = EnhancedVESCDecoder()
        self.monitor_thread = None
        self.lock = Lock()
        
        # Setup signal handler for Ctrl+C
        signal.signal(signal.SIGINT, self._signal_handler)
        
        # Statistics
        self.stats = {
            'total_messages': 0,
            'decoded_messages': 0,
            'start_time': time.time()
        }
    
    def _signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print("\n\nStopping monitor...")
        self.running = False
    
    def _format_value(self, value, unit, width=6):
        """Format a value with proper spacing"""
        if value is None:
            return f"{'N/A':<{width}}"
        
        if unit == '':
            return f"{value:>{width}.0f}"
        else:
            return f"{value:>{width-1}.1f}{unit}"
    
    def _monitor_can_data(self):
        """Background thread to monitor CAN data"""
        while self.running:
            try:
                msg = self.vesc.receive_can_message(timeout=0.1)
                if msg:
                    with self.lock:
                        self.stats['total_messages'] += 1
                    
                    decoded = self.decoder.decode_message(msg.arbitration_id, msg.data)
                    if decoded:
                        with self.lock:
                            self.stats['decoded_messages'] += 1
            
            except Exception:
                time.sleep(0.1)
    
    def run(self):
        """Main monitoring loop"""
        # Suppress logging
        logging.basicConfig(level=logging.ERROR)
        
        print("VESC Monitor - Press Ctrl+C to exit")
        print("Duty%  RPM    FET-C  Batt-V  Mot-A  Bat-A  Rate")
        print("-" * 50)
        
        try:
            # Initialize
            self.vesc = VESCInterface()
            self.running = True
            self.monitor_thread = Thread(target=self._monitor_can_data, daemon=True)
            self.monitor_thread.start()
            
            # Wait for initial data
            time.sleep(2)
            
            while self.running:
                # Get latest data
                data = self.decoder.get_latest_data()
                data_age = time.time() - data.timestamp if data.timestamp > 0 else float('inf')
                
                if data_age < 2.0:  # Fresh data
                    # Format all values compactly
                    duty = self._format_value(data.duty_cycle_percent, '%', 5)
                    rpm = self._format_value(data.rpm, '', 6)
                    temp = self._format_value(data.temperature_c, 'C', 6)
                    volt = self._format_value(data.voltage_v, 'V', 6)
                    motor_i = self._format_value(data.motor_current_a, 'A', 6)
                    batt_i = self._format_value(data.battery_current_a, 'A', 6)
                    
                    # Get message rate
                    with self.lock:
                        uptime = time.time() - self.stats['start_time']
                        msg_rate = self.stats['total_messages'] / uptime if uptime > 0 else 0
                    
                    # Create compact status line
                    status_line = f"{duty} {rpm} {temp} {volt} {motor_i} {batt_i} {msg_rate:4.0f}"
                    
                    # Update display on same line - clear line first then write
                    sys.stdout.write(f'\r{status_line:<60}')
                    sys.stdout.flush()
                
                else:
                    # No fresh data
                    sys.stdout.write(f'\rWaiting for data... (age: {data_age:.1f}s){" " * 20}')
                    sys.stdout.flush()
                
                time.sleep(0.1)
        
        except Exception as e:
            print(f"\nError: {e}")
        
        finally:
            self.running = False
            
            # Cleanup
            if self.monitor_thread and self.monitor_thread.is_alive():
                self.monitor_thread.join(timeout=1.0)
            
            if self.vesc:
                self.vesc.shutdown()
            
            # Show final summary on new line
            print("\n\nFinal values:")
            final_data = self.decoder.get_latest_data()
            
            if final_data.timestamp > 0:
                print(f"  Duty: {final_data.duty_cycle_percent:.1f}%")
                print(f"  RPM: {final_data.rpm:.0f}")
                print(f"  FET Temp: {final_data.temperature_c:.1f}C")
                print(f"  Battery: {final_data.voltage_v:.1f}V")
                print(f"  Motor Current: {final_data.motor_current_a:.1f}A")
                print(f"  Battery Current: {final_data.battery_current_a:.1f}A")
            
            with self.lock:
                runtime = time.time() - self.stats['start_time']
                print(f"\nMessages: {self.stats['total_messages']} in {runtime:.1f}s ({self.stats['total_messages']/runtime:.1f}/s)")
            
            print("Monitor stopped.")

def main():
    """Main entry point"""
    monitor = CompactVESCMonitor()
    monitor.run()

if __name__ == "__main__":
    main()