#!/usr/bin/env python3
"""
VESC Live Monitor - Real-time telemetry display
Shows all VESC telemetry data in a clean, updating display
Press Ctrl+C to exit
"""

import time
import sys
import signal
import logging
from threading import Lock, Thread
from enhanced_decoder import EnhancedVESCDecoder
from vesc_interface import VESCInterface

class VESCMonitor:
    """Live VESC telemetry monitor"""
    
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
        print("\n\n🛑 Shutting down...")
        self.running = False
    
    def _clear_line(self):
        """Clear current line"""
        sys.stdout.write('\r\033[K')
        sys.stdout.flush()
    
    def _format_value(self, value, unit, width=8, precision=1):
        """Format a value with proper spacing"""
        if value is None:
            return f"{'N/A':<{width-len(unit)}}{unit}"
        
        if precision == 0:
            return f"{value:{width-len(unit)}.0f}{unit}"
        else:
            return f"{value:{width-len(unit)}.{precision}f}{unit}"
    
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
        
        print("🔥 VESC Live Monitor")
        print("=" * 80)
        print("📊 Real-time telemetry | Press Ctrl+C to exit")
        print("-" * 80)
        print("Connecting...")
        
        try:
            # Initialize
            self.vesc = VESCInterface()
            self.running = True
            self.monitor_thread = Thread(target=self._monitor_can_data, daemon=True)
            self.monitor_thread.start()
            
            # Wait for initial data
            time.sleep(2)
            print("✅ Connected! Monitoring live data...\n")
            
            while self.running:
                # Get latest data
                data = self.decoder.get_latest_data()
                data_age = time.time() - data.timestamp if data.timestamp > 0 else float('inf')
                
                if data_age < 2.0:  # Fresh data
                    # Format all values
                    temp = self._format_value(data.temperature_c, '°C', 8, 1)
                    volt = self._format_value(data.voltage_v, 'V', 7, 1)
                    duty = self._format_value(data.duty_cycle_percent, '%', 7, 1)
                    rpm = self._format_value(data.rpm, '', 6, 0)
                    motor_i = self._format_value(data.motor_current_a, 'A', 7, 1)
                    batt_i = self._format_value(data.battery_current_a, 'A', 7, 1)
                    
                    # Get statistics
                    with self.lock:
                        uptime = time.time() - self.stats['start_time']
                        msg_rate = self.stats['total_messages'] / uptime if uptime > 0 else 0
                        decode_pct = (self.stats['decoded_messages'] / self.stats['total_messages'] * 100) if self.stats['total_messages'] > 0 else 0
                    
                    # Create status line
                    status_line = (
                        f"🌡️ FET: {temp} | "
                        f"⚡ Battery: {volt} | "
                        f"🔄 Duty: {duty} | "
                        f"🔧 RPM: {rpm} | "
                        f"⚙️ Motor: {motor_i} | "
                        f"🔋 Current: {batt_i} | "
                        f"📡 {msg_rate:.0f}msg/s"
                    )
                    
                    # Update display
                    self._clear_line()
                    sys.stdout.write(status_line)
                    sys.stdout.flush()
                
                else:
                    # No fresh data
                    self._clear_line()
                    sys.stdout.write(f"⏳ Waiting for data... (age: {data_age:.1f}s)")
                    sys.stdout.flush()
                
                time.sleep(0.1)
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        finally:
            self.running = False
            
            # Cleanup
            if self.monitor_thread and self.monitor_thread.is_alive():
                self.monitor_thread.join(timeout=1.0)
            
            if self.vesc:
                self.vesc.shutdown()
            
            # Show final summary
            print("\n\n📊 Session Summary:")
            final_data = self.decoder.get_latest_data()
            
            if final_data.timestamp > 0:
                print(f"   🌡️ Temperature: {final_data.temperature_c:.1f}°C")
                print(f"   ⚡ Voltage: {final_data.voltage_v:.1f}V")
                print(f"   🔄 Duty Cycle: {final_data.duty_cycle_percent:.1f}%")
                print(f"   🔧 RPM: {final_data.rpm:.0f}")
                print(f"   ⚙️ Motor Current: {final_data.motor_current_a:.1f}A")
                print(f"   🔋 Battery Current: {final_data.battery_current_a:.1f}A")
            
            with self.lock:
                runtime = time.time() - self.stats['start_time']
                print(f"\n   📈 {self.stats['total_messages']} messages in {runtime:.1f}s")
                print(f"   📈 {self.stats['total_messages']/runtime:.1f} msg/s average")
            
            print("\n👋 Monitor stopped.")

def main():
    """Main entry point"""
    monitor = VESCMonitor()
    monitor.run()

if __name__ == "__main__":
    main()