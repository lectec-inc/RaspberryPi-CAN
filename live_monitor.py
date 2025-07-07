#!/usr/bin/env python3
"""
Live VESC Monitor - Real-time telemetry display
Shows Duty, RPM, Current, Temperature, Motor Current, Battery Current
Updates in place without scrolling. Press Ctrl+C to exit.
"""

import time
import sys
import signal
from working_student_api import WorkingVESCController

class LiveMonitor:
    """Live VESC data monitor with in-place updates"""
    
    def __init__(self):
        self.running = False
        self.vesc = None
        
        # Setup signal handler for graceful exit
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
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
        print("🔥 Live VESC Monitor")
        print("=" * 80)
        print("📊 Real-time telemetry display")
        print("🛑 Press Ctrl+C to exit")
        print("-" * 80)
        print("Connecting to VESC...")
    
    def _format_value(self, value, unit, width=8):
        """Format a value with unit, handling None values"""
        if value is None:
            return f"{'N/A':<{width-len(unit)}}{unit}"
        return f"{value:{width-len(unit)}.1f}{unit}"
    
    def run(self):
        """Main monitoring loop"""
        self._print_header()
        
        try:
            with WorkingVESCController() as vesc:
                self.vesc = vesc
                
                # Wait for connection
                if not vesc.wait_for_connection(timeout=10.0):
                    print("❌ Failed to connect to VESC")
                    return
                
                print("✅ Connected! Starting live monitor...")
                print("-" * 80)
                
                self.running = True
                update_count = 0
                
                while self.running:
                    # Get current status
                    status = vesc.get_status()
                    
                    if status.is_connected and status.is_data_fresh:
                        # For now, we only have temperature and voltage from the real decoder
                        # The other values would need additional protocol analysis
                        temp = status.temperature_celsius
                        voltage = status.voltage_volts
                        
                        # Create display line with available data
                        display_line = (
                            f"🌡️ FET Temp: {self._format_value(temp, '°C')} | "
                            f"⚡ Battery: {self._format_value(voltage, 'V')} | "
                            f"🔄 Duty: {self._format_value(None, '%')} | "
                            f"🔧 RPM: {self._format_value(None, '')} | "
                            f"⚙️ Motor I: {self._format_value(None, 'A')} | "
                            f"🔋 Batt I: {self._format_value(None, 'A')} | "
                            f"📡 Updates: {update_count}"
                        )
                        
                        # Clear line and print new data
                        self._clear_line()
                        sys.stdout.write(display_line)
                        sys.stdout.flush()
                        
                        update_count += 1
                    
                    else:
                        # No data available
                        self._clear_line()
                        sys.stdout.write(f"⏳ Waiting for data... (age: {status.data_age_seconds:.1f}s)")
                        sys.stdout.flush()
                    
                    time.sleep(0.1)  # Update 10 times per second
        
        except KeyboardInterrupt:
            pass  # Handled by signal handler
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        finally:
            if self.running:
                print("\n\n👋 Monitor stopped.")

def main():
    """Main entry point"""
    monitor = LiveMonitor()
    monitor.run()

if __name__ == "__main__":
    main()