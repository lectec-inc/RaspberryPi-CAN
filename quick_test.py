#!/usr/bin/env python3
"""
VESC CAN Library Quick Test Script

Run this script to quickly identify any major issues with the library.
Reports results in a clear format for debugging.
"""

import sys
import traceback

def test_section(name):
    print(f"\n{'='*50}")
    print(f"Testing: {name}")
    print('='*50)

def test_result(name, success, error=None):
    if success:
        print(f"✅ {name}: OK")
    else:
        print(f"❌ {name}: {error}")

def main():
    print("🧪 VESC CAN Library Quick Test")
    print("This script will test the basic functionality of the library")
    
    results = []
    
    # Test 1: Python Environment
    test_section("Python Environment")
    
    try:
        print(f"Python version: {sys.version}")
        print(f"Python path: {sys.executable}")
        test_result("Python version", True)
        results.append(("Python", True, None))
    except Exception as e:
        test_result("Python version", False, e)
        results.append(("Python", False, str(e)))
    
    # Test 2: Core Dependencies
    test_section("Core Dependencies")
    
    # Test python-can
    try:
        import can
        print(f"python-can version: {can.__version__}")
        test_result("python-can import", True)
        results.append(("python-can", True, None))
    except Exception as e:
        test_result("python-can import", False, e)
        results.append(("python-can", False, str(e)))
        print("💡 Fix: pip3 install python-can")
    
    # Test 3: Library Structure
    test_section("Library Module Imports")
    
    modules_to_test = [
        "vesc_can.datatypes",
        "vesc_can.protocol", 
        "vesc_can.node_manager",
        "vesc_can.can_interface",
        "vesc_can.can_service",
        "vesc_can"
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            test_result(f"{module} import", True)
            results.append((module, True, None))
        except Exception as e:
            test_result(f"{module} import", False, e)
            results.append((module, False, str(e)))
            print(f"💡 Error details: {traceback.format_exc()}")
    
    # Test 4: CAN Interface Availability
    test_section("CAN Interface Detection")
    
    try:
        import subprocess
        result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True, timeout=5)
        
        if 'can0' in result.stdout:
            test_result("can0 interface exists", True)
            results.append(("can0 exists", True, None))
            
            # Check if it's up
            if 'state UP' in result.stdout and 'can0' in result.stdout:
                test_result("can0 interface is UP", True)
                results.append(("can0 UP", True, None))
            else:
                test_result("can0 interface is DOWN", False, "Interface exists but is DOWN")
                results.append(("can0 UP", False, "Interface DOWN"))
                print("💡 Fix: sudo ip link set can0 up type can bitrate 500000")
        else:
            test_result("can0 interface exists", False, "Interface not found")
            results.append(("can0 exists", False, "Not found"))
            print("💡 Check: ip link show | grep can")
            
    except Exception as e:
        test_result("CAN interface check", False, e)
        results.append(("CAN check", False, str(e)))
    
    # Test 5: CAN Communication
    test_section("CAN Communication Test")
    
    try:
        import can
        bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)
        test_result("CAN bus creation", True)
        results.append(("CAN bus", True, None))
        
        # Try to send a test message
        msg = can.Message(arbitration_id=0x123, data=[1,2,3,4], is_extended_id=False)
        bus.send(msg)
        test_result("CAN message send", True)
        results.append(("CAN send", True, None))
        
        bus.shutdown()
        
    except Exception as e:
        test_result("CAN communication", False, e)
        results.append(("CAN comm", False, str(e)))
        if "No such device" in str(e):
            print("💡 Fix: Set up CAN interface first")
        elif "Permission denied" in str(e):
            print("💡 Fix: sudo usermod -a -G dialout $USER (then logout/login)")
    
    # Test 6: Library Components
    test_section("Library Component Testing")
    
    try:
        from vesc_can.protocol import VESCProtocol
        protocol = VESCProtocol()
        
        # Test packet creation
        can_id, data = protocol.create_can_set_duty(0.1, 0)
        test_result("Protocol packet creation", True)
        results.append(("Protocol", True, None))
        print(f"  Sample packet - ID: 0x{can_id:X}, Data: {data.hex()}")
        
    except Exception as e:
        test_result("Protocol testing", False, e)
        results.append(("Protocol", False, str(e)))
    
    try:
        from vesc_can.node_manager import VESCNodeManager
        nm = VESCNodeManager()
        node_id = nm.get_node_id()
        test_result("Node manager", True)
        results.append(("Node manager", True, None))
        print(f"  Assigned node ID: {node_id}")
        
    except Exception as e:
        test_result("Node manager", False, e)
        results.append(("Node manager", False, str(e)))
    
    # Test 7: High-Level API
    test_section("High-Level API Testing")
    
    try:
        import vesc_can
        
        # Test network status (should work even without VESC)
        network = vesc_can.get_network_status('can0')
        test_result("Network status", True)
        results.append(("Network status", True, None))
        print(f"  My node ID: {network.get('my_node_id', 'Unknown')}")
        
    except Exception as e:
        test_result("Network status", False, e)
        results.append(("Network status", False, str(e)))
    
    try:
        import vesc_can
        
        # Test VESC object creation (without connection)
        vesc = vesc_can.VESC('can0', auto_start=False)
        test_result("VESC object creation", True)
        results.append(("VESC object", True, None))
        
    except Exception as e:
        test_result("VESC object creation", False, e)
        results.append(("VESC object", False, str(e)))
    
    # Summary
    test_section("Test Summary")
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    print(f"Success rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("🎉 All tests passed! Library appears to be working correctly.")
    else:
        print("\n❌ Issues found:")
        for name, success, error in results:
            if not success:
                print(f"  - {name}: {error}")
        
        print("\n🔧 Next steps:")
        print("1. Fix the failed tests above")
        print("2. Run this script again to verify fixes")
        print("3. Try connecting to real VESC hardware")
        print("4. Run the example scripts in vesc_can/examples/")
    
    print("\n📋 Detailed Results:")
    for name, success, error in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {name:20s} : {status}")
        if error and not success:
            print(f"    └─ Error: {error}")

if __name__ == "__main__":
    main()