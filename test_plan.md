# VESC CAN Library Testing Plan

## 🧪 Systematic Testing Approach

This document outlines a step-by-step approach to test and debug the VESC CAN library.

## Phase 1: Environment Setup Testing

### Test 1.1: Basic Python Import
```bash
cd /Users/jaredebersole/Projects/RaspberryPi-CAN
python3 -c "import sys; print('Python version:', sys.version)"
```

### Test 1.2: Dependency Check
```bash
python3 -c "import can; print('python-can version:', can.__version__)"
```
If this fails:
```bash
pip3 install python-can
```

### Test 1.3: Library Import Test
```bash
python3 -c "
try:
    import vesc_can.datatypes
    print('✅ datatypes import: OK')
except Exception as e:
    print('❌ datatypes import:', e)

try:
    import vesc_can.protocol
    print('✅ protocol import: OK')
except Exception as e:
    print('❌ protocol import:', e)

try:
    import vesc_can.node_manager
    print('✅ node_manager import: OK')
except Exception as e:
    print('❌ node_manager import:', e)

try:
    import vesc_can.can_interface
    print('✅ can_interface import: OK')
except Exception as e:
    print('❌ can_interface import:', e)

try:
    import vesc_can.can_service
    print('✅ can_service import: OK')
except Exception as e:
    print('❌ can_service import:', e)

try:
    import vesc_can
    print('✅ main vesc_can import: OK')
except Exception as e:
    print('❌ main vesc_can import:', e)
"
```

## Phase 2: CAN Interface Testing

### Test 2.1: Check CAN Interface Availability
```bash
ip link show can0
```
Expected: Interface exists (may be DOWN)

If interface doesn't exist:
```bash
# Check what CAN interfaces are available
ip link show | grep can
# Or check for USB CAN adapters
lsusb | grep -i can
```

### Test 2.2: CAN Interface Setup
```bash
# Bring up CAN interface (may need sudo)
sudo ip link set can0 up type can bitrate 500000

# Verify it's up
ip link show can0
```
Expected: State should be "UP"

### Test 2.3: Basic CAN Communication Test
```bash
# Terminal 1: Listen for CAN messages
candump can0 &

# Terminal 2: Send test message
cansend can0 123#DEADBEEF

# Check if message appears in Terminal 1
# Kill candump: kill %1
```

### Test 2.4: CAN Interface with Python
```bash
python3 -c "
import can
try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)
    print('✅ CAN interface created successfully')
    
    # Try to send a test message
    msg = can.Message(arbitration_id=0x123, data=[1,2,3,4], is_extended_id=False)
    bus.send(msg)
    print('✅ CAN message sent successfully')
    
    bus.shutdown()
except Exception as e:
    print('❌ CAN interface error:', e)
"
```

## Phase 3: Library Component Testing

### Test 3.1: Protocol Layer Testing
```bash
python3 -c "
from vesc_can.protocol import VESCProtocol
from vesc_can.datatypes import VESCCANCommands

protocol = VESCProtocol()

# Test CAN packet creation
try:
    can_id, data = protocol.create_can_set_duty(0.1, 0)
    print(f'✅ Duty packet: ID=0x{can_id:X}, Data={data.hex()}')
    
    can_id, data = protocol.create_can_ping(0)
    print(f'✅ Ping packet: ID=0x{can_id:X}, Data={data.hex()}')
    
    can_id, data = protocol.create_can_set_rpm(1000, 0)
    print(f'✅ RPM packet: ID=0x{can_id:X}, Data={data.hex()}')
    
except Exception as e:
    print('❌ Protocol error:', e)
"
```

### Test 3.2: Node Manager Testing
```bash
python3 -c "
from vesc_can.node_manager import VESCNodeManager

try:
    nm = VESCNodeManager()
    node_id = nm.get_node_id()
    print(f'✅ Node ID assigned: {node_id}')
    
    stats = nm.get_network_stats()
    print(f'✅ Network stats: {stats}')
    
except Exception as e:
    print('❌ Node manager error:', e)
"
```

### Test 3.3: CAN Interface Class Testing
```bash
python3 -c "
from vesc_can.can_interface import VESCCANInterface

try:
    can_if = VESCCANInterface('can0', 500000)
    print('✅ CAN Interface created')
    
    if can_if.connect():
        print('✅ CAN Interface connected')
        
        # Test sending a message
        success = can_if.send_message(0x123, b'\\x01\\x02\\x03\\x04')
        print(f'✅ Send message: {success}')
        
        can_if.disconnect()
        print('✅ CAN Interface disconnected')
    else:
        print('❌ CAN Interface connection failed')
        
except Exception as e:
    print('❌ CAN Interface error:', e)
"
```

## Phase 4: Background Service Testing

### Test 4.1: Service Creation and Startup
```bash
python3 -c "
from vesc_can.can_service import create_can_service, start_can_service
import time

try:
    print('Creating CAN service...')
    service = create_can_service('can0', 500000)
    print('✅ CAN service created')
    
    print('Starting CAN service...')
    success = start_can_service('can0', 500000)
    print(f'✅ CAN service started: {success}')
    
    # Let it run for a few seconds
    time.sleep(3)
    
    # Get statistics
    stats = service.get_service_statistics()
    print(f'✅ Service stats: uptime={stats[\"uptime\"]:.1f}s')
    
    service.stop()
    print('✅ Service stopped')
    
except Exception as e:
    print('❌ Service error:', e)
"
```

### Test 4.2: Network Discovery Test
```bash
python3 -c "
from vesc_can.can_service import start_can_service, get_can_service
import time

try:
    # Start service
    start_can_service('can0', 500000)
    service = get_can_service()
    
    print('Service running, performing discovery...')
    service.force_discovery()
    
    # Wait a bit for responses
    time.sleep(2)
    
    # Check for active nodes
    active_nodes = service.node_manager.get_active_nodes()
    print(f'✅ Active nodes found: {list(active_nodes.keys())}')
    
    cached_status = service.get_all_cached_status()
    print(f'✅ Cached status from {len(cached_status)} nodes')
    
    service.stop()
    
except Exception as e:
    print('❌ Discovery error:', e)
"
```

## Phase 5: Student API Testing

### Test 5.1: Basic VESC Connection
```bash
python3 -c "
import vesc_can
import time

try:
    print('Testing VESC connection...')
    
    # Test 1: Network status without VESC
    network = vesc_can.get_network_status('can0')
    print(f'✅ Network status: {network}')
    
    # Test 2: List active VESCs (should be empty without real VESC)
    vescs = vesc_can.list_active_vescs('can0')
    print(f'✅ Active VESCs: {vescs}')
    
    # Test 3: Try to connect (will timeout without real VESC)
    print('Attempting VESC connection (will timeout in 5s without real VESC)...')
    vesc = vesc_can.connect_to_vesc('can0')
    
    if vesc:
        print('✅ VESC connected!')
        print(f'✅ VESC ID: {vesc._get_vesc_id()}')
        
        # Test reading (will return defaults without real VESC)
        duty = vesc.get_duty()
        rpm = vesc.get_rpm()
        voltage = vesc.get_voltage()
        
        print(f'✅ Read test: duty={duty}, rpm={rpm}, voltage={voltage}')
        
    else:
        print('ℹ️  No VESC found (expected without real hardware)')
        
except Exception as e:
    print('❌ API error:', e)
    import traceback
    traceback.print_exc()
"
```

### Test 5.2: VESC Class Direct Testing
```bash
python3 -c "
import vesc_can
import time

try:
    print('Testing VESC class directly...')
    vesc = vesc_can.VESC('can0', auto_start=True)
    
    print('✅ VESC object created')
    
    # Test network info
    network = vesc.get_network_info()
    print(f'✅ Network info: {network}')
    
    # Test getting cached values (will be defaults)
    data = vesc.get_all_data()
    print(f'✅ Got data: {len(data)} fields')
    
    # Print status
    print('Status:')
    vesc.print_status()
    
except Exception as e:
    print('❌ VESC class error:', e)
    import traceback
    traceback.print_exc()
"
```

## Phase 6: Integration Testing with Real VESC

### Test 6.1: VESC Detection Test
**Run this with VESC connected and powered:**

```bash
python3 -c "
import vesc_can
import time

print('Testing with real VESC hardware...')
print('Make sure VESC is connected and powered on!')

try:
    # Try to connect with longer timeout
    vesc = vesc_can.connect_to_vesc(wait_timeout=10.0)
    
    if vesc:
        print('🎉 REAL VESC DETECTED!')
        
        # Read actual values
        print('Real VESC data:')
        vesc.print_status()
        
        # Check for faults
        if vesc.has_fault():
            print(f'⚠️  VESC has fault: {vesc.get_fault_code()}')
        else:
            print('✅ No faults detected')
            
        # Test very gentle movement (1% duty for 1 second)
        print('Testing gentle movement (1% duty)...')
        vesc.set_duty(0.01)
        time.sleep(1)
        vesc.stop_motor()
        print('✅ Movement test completed')
        
    else:
        print('❌ No VESC detected - check connections')
        
except Exception as e:
    print('❌ Real VESC test error:', e)
    import traceback
    traceback.print_exc()
"
```

## Phase 7: Example Script Testing

### Test 7.1: Basic Control Example
```bash
cd vesc_can/examples
python3 basic_control.py
```

### Test 7.2: Sensor Reading Example  
```bash
cd vesc_can/examples
python3 read_sensors.py
```

### Test 7.3: Motor Test Example
```bash
cd vesc_can/examples  
python3 motor_test.py
```

## 🐛 Common Issues and Fixes

### Issue: Import Errors
**Fix**: Add project to Python path:
```bash
export PYTHONPATH="/Users/jaredebersole/Projects/RaspberryPi-CAN:$PYTHONPATH"
```

### Issue: Permission Denied on CAN
**Fix**: Add user to dialout group:
```bash
sudo usermod -a -G dialout $USER
# Log out and back in
```

### Issue: CAN Interface Not Found
**Fix**: Check available interfaces:
```bash
ip link show | grep can
# Or use virtual CAN for testing:
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

### Issue: python-can Import Error
**Fix**: Install dependencies:
```bash
pip3 install python-can
# Or with socketcan support:
pip3 install python-can[socketcan]
```

## 📝 Testing Results Template

When you run the tests, report results like this:

```
Phase 1 Results:
✅ Test 1.1: Python import - OK
❌ Test 1.2: python-can missing
✅ Test 1.3: Library imports - OK

Phase 2 Results:
❌ Test 2.1: can0 interface not found
...

Issues Found:
1. Missing python-can dependency  
2. No CAN interface available
3. Import error in datatypes.py line 45

Next Steps:
1. Install python-can
2. Set up virtual CAN interface for testing
3. Fix datatypes.py syntax error
```

## 🚀 Quick Test Script

Here's a single script to run the most important tests:

```bash
python3 << 'EOF'
print("🧪 VESC CAN Library Quick Test")
print("=" * 40)

# Test 1: Basic imports
try:
    import vesc_can
    print("✅ vesc_can import: OK")
except Exception as e:
    print(f"❌ vesc_can import: {e}")

# Test 2: python-can
try:
    import can
    print(f"✅ python-can: {can.__version__}")
except Exception as e:
    print(f"❌ python-can: {e}")

# Test 3: CAN interface
try:
    import can
    bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)
    print("✅ CAN interface: OK")
    bus.shutdown()
except Exception as e:
    print(f"❌ CAN interface: {e}")

# Test 4: Network status
try:
    import vesc_can
    status = vesc_can.get_network_status('can0')
    print(f"✅ Network status: {status['my_node_id']}")
except Exception as e:
    print(f"❌ Network status: {e}")

print("\n🏁 Quick test completed!")
EOF
```

Run this script first to get a quick overview of what's working!