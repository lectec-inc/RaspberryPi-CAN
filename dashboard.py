#!/usr/bin/env python3
"""
VESC Real-time Dashboard
Displays live telemetry data from VESC motor controllers in a clean, organized format.
"""

import time
import sys
import os
import signal
from datetime import datetime
from student_api import VESCStudentAPI


class VESCDashboard:
    """Real-time dashboard for VESC telemetry data"""
    
    def __init__(self):
        self.api = VESCStudentAPI()
        self.running = False
        self.update_interval = 0.2  # 5Hz update rate
        
        # Setup signal handler for clean shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle Ctrl+C and other termination signals"""
        print(f"\n🛑 Received signal {signum}, shutting down dashboard...")
        self.running = False
        
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def format_value(self, value, unit="", decimals=2):
        """Format a value with proper handling of None"""
        if value is None:
            return "---"
        
        if isinstance(value, (int, float)):
            if decimals == 0:
                return f"{int(value)}{unit}"
            else:
                return f"{value:.{decimals}f}{unit}"
        return str(value) + unit
    
    def draw_header(self):
        """Draw the dashboard header"""
        print("=" * 80)
        print("🚗 VESC MOTOR CONTROLLER DASHBOARD")
        print("=" * 80)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Press Ctrl+C to exit")
        print()
    
    def draw_controller_info(self, controller_id, controller):
        """Draw information for a single controller"""
        # Check connection status
        connected = controller.is_connected()
        status_icon = "🟢" if connected else "🔴"
        status_text = "CONNECTED" if connected else "DISCONNECTED"
        
        print(f"📟 CONTROLLER {controller_id} {status_icon} {status_text}")
        print("-" * 80)
        
        if not connected:
            print("   No data available - controller not responding")
            print()
            return
        
        # Get all telemetry data
        try:
            telemetry = controller.get_all_telemetry()
        except Exception as e:
            print(f"   Error getting telemetry: {e}")
            print()
            return
        
        # Motor status section
        print("🔧 MOTOR STATUS:")
        motor = telemetry.get('motor', {})
        print(f"   RPM:          {self.format_value(motor.get('rpm'), ' rpm', 0):>12}")
        print(f"   Current:      {self.format_value(motor.get('current'), ' A'):>12}")
        duty_cycle = motor.get('duty_cycle')
        if duty_cycle is not None:
            duty_percent = duty_cycle * 100  # Convert to percentage
            print(f"   Duty Cycle:   {self.format_value(duty_percent, ' %', 1):>12}")
        else:
            print(f"   Duty Cycle:   {self.format_value(None, ' %', 1):>12}")
        print()
        
        # Power system section
        print("⚡ POWER SYSTEM:")
        power = telemetry.get('power', {})
        print(f"   Input Voltage:    {self.format_value(power.get('input_voltage'), ' V'):>12}")
        print(f"   Input Current:    {self.format_value(power.get('input_current'), ' A'):>12}")
        print(f"   Amp Hours Used:   {self.format_value(power.get('amp_hours_consumed'), ' Ah'):>12}")
        print(f"   Amp Hours Regen:  {self.format_value(power.get('amp_hours_charged'), ' Ah'):>12}")
        print(f"   Watt Hours Used:  {self.format_value(power.get('watt_hours_consumed'), ' Wh'):>12}")
        print(f"   Watt Hours Regen: {self.format_value(power.get('watt_hours_charged'), ' Wh'):>12}")
        print()
        
        # Temperature section
        print("🌡️  TEMPERATURES:")
        temps = telemetry.get('temperatures', {})
        fet_temp = temps.get('fet')
        motor_temp = temps.get('motor')
        
        # Add temperature status indicators
        fet_status = self.get_temp_status(fet_temp, 80, 90)  # Warning at 80°C, critical at 90°C
        motor_status = self.get_temp_status(motor_temp, 100, 120)  # Warning at 100°C, critical at 120°C
        
        print(f"   FET Temperature:    {self.format_value(fet_temp, ' °C'):>12} {fet_status}")
        print(f"   Motor Temperature:  {self.format_value(motor_temp, ' °C'):>12} {motor_status}")
        print()
        
        # Sensors section
        print("📊 SENSORS:")
        sensors = telemetry.get('sensors', {})
        print(f"   Tachometer:   {self.format_value(sensors.get('tachometer'), '', 0):>12}")
        print(f"   PID Position: {self.format_value(sensors.get('pid_position'), ' °'):>12}")
        print(f"   ADC EXT:      {self.format_value(sensors.get('adc_ext'), ' V'):>12}")
        print(f"   ADC EXT2:     {self.format_value(sensors.get('adc_ext2'), ' V'):>12}")
        print(f"   ADC EXT3:     {self.format_value(sensors.get('adc_ext3'), ' V'):>12}")
        print(f"   Servo/PPM:    {self.format_value(sensors.get('servo_value'), ''):>12}")
        print()
        
        # Data freshness indicator
        timestamp = telemetry.get('timestamp', 0)
        if timestamp > 0:
            age = time.time() - timestamp
            freshness = "🟢 FRESH" if age < 1.0 else "🟡 STALE" if age < 5.0 else "🔴 OLD"
            print(f"📡 DATA: {freshness} (age: {age:.2f}s)")
        print()
    
    def get_temp_status(self, temp, warning_thresh, critical_thresh):
        """Get temperature status indicator"""
        if temp is None:
            return ""
        
        if temp >= critical_thresh:
            return "🔴 CRITICAL"
        elif temp >= warning_thresh:
            return "🟡 WARNING"
        else:
            return "🟢 OK"
    
    def draw_system_stats(self):
        """Draw system statistics"""
        try:
            interface = self.api.system_manager.get_interface()
            stats = interface.get_statistics()
            
            print("📈 SYSTEM STATISTICS:")
            print(f"   Messages Received: {stats['messages_received']:,}")
            print(f"   Messages Parsed:   {stats['messages_parsed']:,}")
            print(f"   Parse Errors:      {stats['parse_errors']:,}")
            print(f"   Commands Sent:     {stats['commands_sent']:,}")
            print(f"   Commands Success:  {stats['commands_successful']:,}")
            print(f"   Commands Timeout:  {stats['commands_timeout']:,}")
            
            # Calculate message rate
            if hasattr(self, 'last_msg_count') and hasattr(self, 'last_msg_time'):
                current_time = time.time()
                msg_diff = stats['messages_received'] - self.last_msg_count
                time_diff = current_time - self.last_msg_time
                
                if time_diff > 0:
                    msg_rate = msg_diff / time_diff
                    print(f"   Message Rate:      {msg_rate:.1f} msg/s")
            
            self.last_msg_count = stats['messages_received']
            self.last_msg_time = time.time()
            
        except Exception as e:
            print(f"📈 SYSTEM STATISTICS: Error - {e}")
        
        print()
    
    def draw_controls_help(self):
        """Draw control instructions"""
        print("🎮 CONTROLS:")
        print("   Ctrl+C: Exit dashboard")
        print("   The dashboard updates every 200ms")
        print()
    
    def run(self):
        """Run the dashboard"""
        print("Starting VESC Dashboard...")
        
        # Start the API
        if not self.api.start():
            print("❌ Failed to start VESC system")
            return
        
        print("✅ VESC system started, waiting for controllers...")
        time.sleep(3.0)  # Give time for controller discovery
        
        self.running = True
        
        try:
            while self.running:
                # Clear screen and redraw
                self.clear_screen()
                
                # Draw header
                self.draw_header()
                
                # Get connected controllers
                controllers = self.api.get_connected_controllers()
                
                if not controllers:
                    print("⚠️  No VESC controllers detected")
                    print("   - Check CAN connections")
                    print("   - Verify VESC is powered on")
                    print("   - Ensure CAN messages are enabled in VESC configuration")
                    print()
                else:
                    # Display each controller
                    for controller_id in sorted(controllers):
                        controller = self.api.get_controller(controller_id)
                        self.draw_controller_info(controller_id, controller)
                
                # Draw system statistics
                self.draw_system_stats()
                
                # Draw controls help
                self.draw_controls_help()
                
                # Footer
                print("=" * 80)
                
                # Wait for next update (make it interruptible)
                sleep_time = self.update_interval
                start_sleep = time.time()
                while self.running and (time.time() - start_sleep) < sleep_time:
                    time.sleep(0.05)  # Small sleep intervals to allow interruption
                
        except KeyboardInterrupt:
            print("\n🛑 Dashboard stopped by user", flush=True)
        except Exception as e:
            print(f"\n❌ Dashboard error: {e}", flush=True)
        finally:
            print("Cleaning up...", flush=True)
            self.stop()
    
    def stop(self):
        """Stop the dashboard"""
        self.running = False
        if hasattr(self, 'api'):
            self.api.stop()
        print("Dashboard shutdown complete", flush=True)


def main():
    """Main entry point"""
    # Check if we're on a terminal that supports clearing
    if not sys.stdout.isatty():
        print("Warning: Dashboard works best in an interactive terminal")
    
    dashboard = VESCDashboard()
    dashboard.run()


if __name__ == "__main__":
    main()