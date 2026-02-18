#!/usr/bin/env python3
"""
Main Event Loop for VESC CAN System
Central controller that manages CAN interface and provides access to VESC data.
"""

import time
import signal
import sys
import threading
from typing import Dict, Any, Optional
from core.vesc_interface import VESCInterface


class VESCSystemManager:
    """Main system manager for VESC CAN interface"""
    
    def __init__(self, can_channel: str = 'can0', quiet: bool = True):
        self.can_channel = can_channel
        self.interface = VESCInterface(can_channel)
        self.running = False
        self.main_thread = None
        self.quiet = quiet  # Suppress statistics printing (default: True)
        
        # Known controllers (can be dynamically discovered)
        self.controllers: Dict[int, Dict[str, Any]] = {}
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\\nReceived signal {signum}, shutting down...")
        self.stop()
    
    def start(self) -> bool:
        """Start the VESC system"""
        print("Starting VESC CAN System...")
        
        # Connect to CAN interface
        if not self.interface.connect():
            print("Failed to connect to CAN interface")
            return False
        
        self.running = True
        
        # Start main processing thread
        self.main_thread = threading.Thread(target=self._main_loop, daemon=True)
        self.main_thread.start()
        
        print("VESC CAN System started successfully")
        return True
    
    def stop(self):
        """Stop the VESC system"""
        print("Stopping VESC CAN System...")
        
        self.running = False
        
        if self.main_thread:
            self.main_thread.join(timeout=2.0)
        
        self.interface.disconnect()
        
        print("VESC CAN System stopped")
    
    def _main_loop(self):
        """Main processing loop - non-blocking"""
        print("Main processing loop started")
        
        last_stats_time = time.time()
        last_discovery_time = time.time()
        
        while self.running:
            try:
                current_time = time.time()
                
                # Update controller discovery every 5 seconds
                if current_time - last_discovery_time >= 5.0:
                    self._update_controller_discovery()
                    last_discovery_time = current_time
                
                # Print statistics every 10 seconds (unless quiet mode)
                if not self.quiet and current_time - last_stats_time >= 10.0:
                    self._print_statistics()
                    last_stats_time = current_time
                
                # Main loop runs at 10Hz (non-blocking)
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(0.1)
        
        print("Main processing loop stopped")
    
    def _update_controller_discovery(self):
        """Discover and update known controllers"""
        # Check for controllers that have sent data recently
        for controller_id in range(1, 256):  # Check reasonable controller ID range
            data = self.interface.get_live_data(controller_id)
            if data and 'last_update' in data:
                last_update = data['last_update']
                if time.time() - last_update < 5.0:  # Active within last 5 seconds
                    if controller_id not in self.controllers:
                        print(f"Discovered VESC controller: {controller_id}")
                        self.controllers[controller_id] = {
                            'first_seen': time.time(),
                            'last_seen': last_update,
                            'message_types': set()
                        }
                    
                    # Update controller info
                    self.controllers[controller_id]['last_seen'] = last_update
                    self.controllers[controller_id]['message_types'].update(data.keys())
    
    def _print_statistics(self):
        """Print system statistics"""
        stats = self.interface.get_statistics()
        print(f"\\nSystem Statistics:")
        print(f"  Active Controllers: {len(self.controllers)}")
        print(f"  Messages Received: {stats['messages_received']}")
        print(f"  Messages Parsed: {stats['messages_parsed']}")
        print(f"  Commands Sent: {stats['commands_sent']}")
        print(f"  Commands Successful: {stats['commands_successful']}")
        print(f"  Commands Timeout: {stats['commands_timeout']}")
        print(f"  Parse Errors: {stats['parse_errors']}")
        
        # Print controller info
        for controller_id in sorted(self.controllers.keys()):
            controller = self.controllers[controller_id]
            age = time.time() - controller['last_seen']
            print(f"  Controller {controller_id}: {len(controller['message_types'])} msg types, last seen {age:.1f}s ago")
    
    def get_controller_ids(self) -> list:
        """Get list of discovered controller IDs"""
        return list(self.controllers.keys())
    
    def get_interface(self) -> VESCInterface:
        """Get the VESC interface for direct access"""
        return self.interface
    
    def is_running(self) -> bool:
        """Check if system is running"""
        return self.running
    
    def wait_for_shutdown(self):
        """Wait for system shutdown"""
        try:
            while self.running:
                time.sleep(1.0)
        except KeyboardInterrupt:
            self.stop()


def main():
    """Main entry point"""
    print("VESC CAN System - Raspberry Pi Interface")
    print("=" * 50)
    
    # Create system manager
    system = VESCSystemManager()
    
    # Start system
    if not system.start():
        print("Failed to start system")
        sys.exit(1)
    
    try:
        # Keep system running
        print("System running. Press Ctrl+C to stop.")
        system.wait_for_shutdown()
        
    except KeyboardInterrupt:
        print("\\nInterrupted by user")
        system.stop()
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        system.stop()
        sys.exit(1)
    
    print("System shutdown complete")


if __name__ == "__main__":
    main()