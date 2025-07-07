#!/usr/bin/env python3
"""
Enhanced Live VESC Monitor - Real-time telemetry display
Shows Duty, RPM, Current, Temperature, Motor Current, Battery Current
Updates in place without scrolling. Press Ctrl+C to exit.
"""

import time
import sys
import signal
import logging
from threading import Lock, Thread
from enhanced_decoder import EnhancedVESCDecoder, CompleteVESCData
from vesc_interface import VESCInterface

class EnhancedLiveMonitor:
    """Enhanced live VESC data monitor with all telemetry fields"""
    
    def __init__(self):
        self.running = False
        self.vesc = None
        self.decoder = EnhancedVESCDecoder()
        self.monitor_thread = None
        self.lock = Lock()
        
        # Setup signal handler for graceful exit
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Statistics
        self.stats = {
            'total_messages': 0,
            'decoded_messages': 0,
            'start_time': time.time()
        }
    
    def _signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print("\n\n🛑 Shutting down monitor...")
        self.running = False
    
    def _clear_line(self):
        """Clear current line and return cursor to beginning"""
        sys.stdout.write('\r\033[K')
        sys.stdout.flush()
    
    def _print_header(self):
        """Print header information"""
        print("🔥 Enhanced Live VESC Monitor")
        print("=" * 90)
        print("📊 Real-time telemetry display with all available data")
        print("🛑 Press Ctrl+C to exit")
        print("-" * 90)
        print("Connecting to VESC...")
    
    def _format_value(self, value, unit, width=8, precision=1):
        """Format a value with unit, handling None values"""
        if value is None:
            return f"{'N/A':<{width-len(unit)}}{unit}"
        
        if precision == 0:
            return f"{value:{width-len(unit)}.0f}{unit}"
        else:
            return f"{value:{width-len(unit)}.{precision}f}{unit}"
    
    def _monitor_can_data(self):
        """Monitor CAN data in background thread"""
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
            
            except Exception as e:
                # Silently continue on errors
                time.sleep(0.1)
    
    def run(self):
        """Main monitoring loop"""
        self._print_header()
        
        try:
            # Initialize VESC interface
            self.vesc = VESCInterface()
            
            # Start background monitoring
            self.running = True
            self.monitor_thread = Thread(target=self._monitor_can_data, daemon=True)
            self.monitor_thread.start()
            
            # Wait a moment for data
            time.sleep(2)
            
            print("✅ Connected! Starting live monitor...")
            print("-" * 90)
            
            update_count = 0
            last_data_time = 0
            
            while self.running:
                # Get latest decoded data
                latest_data = self.decoder.get_latest_data()
                
                # Check if we have recent data
                data_age = time.time() - latest_data.timestamp if latest_data.timestamp > 0 else float('inf')
                has_fresh_data = data_age < 2.0
                
                if has_fresh_data:
                    # Format all available values
                    temp_str = self._format_value(latest_data.temperature_c, '°C', 8, 1)
                    volt_str = self._format_value(latest_data.voltage_v, 'V', 7, 1)
                    duty_str = self._format_value(latest_data.duty_cycle_percent, '%', 7, 1)
                    rpm_str = self._format_value(latest_data.rpm, '', 6, 0)
                    motor_i_str = self._format_value(latest_data.motor_current_a, 'A', 7, 1)
                    batt_i_str = self._format_value(latest_data.battery_current_a, 'A', 7, 1)
                    
                    # Get message rate
                    with self.lock:
                        uptime = time.time() - self.stats['start_time']
                        msg_rate = self.stats['total_messages'] / uptime if uptime > 0 else 0
                        decode_rate = (self.stats['decoded_messages'] / self.stats['total_messages'] * 100) if self.stats['total_messages'] > 0 else 0
                    
                    # Create display line
                    display_line = (
                        f"🌡️ FET: {temp_str} | "
                        f"⚡ Batt: {volt_str} | "
                        f"🔄 Duty: {duty_str} | "
                        f"🔧 RPM: {rpm_str} | "
                        f"⚙️ Motor: {motor_i_str} | "
                        f"🔋 Current: {batt_i_str} | "
                        f"📡 {msg_rate:.0f}msg/s ({decode_rate:.0f}%)"
                    )
                    
                    # Clear line and print new data
                    self._clear_line()
                    sys.stdout.write(display_line)
                    sys.stdout.flush()
                    
                    update_count += 1
                
                else:
                    # No fresh data available
                    with self.lock:
                        total_msgs = self.stats['total_messages']
                    
                    self._clear_line()
                    sys.stdout.write(f"⏳ Waiting for data... (age: {data_age:.1f}s, msgs: {total_msgs})")
                    sys.stdout.flush()
                
                time.sleep(0.1)  # Update 10 times per second
        
        except KeyboardInterrupt:
            pass  # Handled by signal handler
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        finally:
            self.running = False
            
            # Wait for monitor thread
            if self.monitor_thread and self.monitor_thread.is_alive():
                self.monitor_thread.join(timeout=1.0)
            
            # Shutdown VESC interface
            if self.vesc:
                self.vesc.shutdown()
            
            if self.running or True:  # Always show final stats
                print("\n\n📊 Final Statistics:")
                with self.lock:
                    uptime = time.time() - self.stats['start_time']
                    print(f"   Runtime: {uptime:.1f}s")
                    print(f"   Total messages: {self.stats['total_messages']}")
                    print(f"   Decoded messages: {self.stats['decoded_messages']}")
                    print(f"   Message rate: {self.stats['total_messages']/uptime:.1f} msg/s")
                    print(f"   Decode rate: {self.stats['decoded_messages']/self.stats['total_messages']*100:.1f}%" if self.stats['total_messages'] > 0 else "   Decode rate: 0%")
                
                # Show final data values
                final_data = self.decoder.get_latest_data()
                print(f"\n📋 Final Values:")
                print(f"   Temperature: {final_data.temperature_c:.1f}°C" if final_data.temperature_c else "   Temperature: N/A")
                print(f"   Voltage: {final_data.voltage_v:.1f}V" if final_data.voltage_v else "   Voltage: N/A")
                print(f"   Duty Cycle: {final_data.duty_cycle_percent:.1f}%" if final_data.duty_cycle_percent else "   Duty Cycle: N/A")
                print(f"   RPM: {final_data.rpm:.0f}" if final_data.rpm else "   RPM: N/A")
                print(f"   Motor Current: {final_data.motor_current_a:.1f}A" if final_data.motor_current_a else "   Motor Current: N/A")
                print(f"   Battery Current: {final_data.battery_current_a:.1f}A" if final_data.battery_current_a else "   Battery Current: N/A")
                
                print("\n👋 Monitor stopped.")

def main():
    """Main entry point"""
    # Reduce logging noise
    logging.basicConfig(level=logging.ERROR)
    
    monitor = EnhancedLiveMonitor()
    monitor.run()

if __name__ == "__main__":
    main()