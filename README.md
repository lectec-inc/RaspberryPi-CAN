# VESC CAN Library for Raspberry Pi

A simple Python library for communicating with VESC motor controllers via CAN bus on Raspberry Pi. Designed specifically for high school students with minimal programming experience.

## 🚀 Quick Start

```python
import vesc_can

# Connect to VESC (automatically finds first one on network)
vesc = vesc_can.connect_to_vesc()

# Read data (instant response from cache)
duty = vesc.get_duty()        # Current duty cycle
rpm = vesc.get_rpm()          # Current RPM  
current = vesc.get_current()  # Motor current
voltage = vesc.get_voltage()  # Input voltage
temp = vesc.get_temp_motor()  # Motor temperature

# Control motor
vesc.set_duty(0.5)            # 50% duty cycle
vesc.set_rpm(1000)            # 1000 RPM
vesc.set_current(5.0)         # 5 Amperes
vesc.stop_motor()             # Emergency stop
```

## 📋 Features

### ✅ What This Library Does
- **Automatic Network Participation**: Responds to VESC Tool pings, sends heartbeats
- **Real-time Data**: 50Hz status updates cached automatically  
- **Complete VESC Support**: Every VESC Tool command available
- **Multi-Pi Networks**: Automatic unique node ID assignment
- **Student-Friendly**: Simple functions, clear error messages
- **Background Service**: Handles all CAN networking automatically
- **Hybrid Data Access**: Fast cached data + on-demand requests

### 🎯 Perfect For
- High school robotics projects
- VESC motor controller learning
- Raspberry Pi CAN bus education
- Electric vehicle prototypes
- Motor testing and characterization

## 🛠️ Installation

### 1. System Setup (Raspberry Pi)

```bash
# Install system dependencies
sudo apt update
sudo apt install can-utils python3-dev python3-pip

# Set up CAN interface (add to /etc/rc.local or systemd)
sudo ip link set can0 up type can bitrate 500000

# Verify CAN interface
ip link show can0
```

### 2. Install Python Library

```bash
# Install from requirements file
pip install -r requirements.txt

# Or install python-can directly
pip install python-can>=4.0.0
```

### 3. Test Installation

```python
import vesc_can

# Check network status
status = vesc_can.get_network_status()
print(f"My node ID: {status['my_node_id']}")
print(f"Active VESCs: {vesc_can.list_active_vescs()}")
```

## 📖 Usage Guide

### Basic Connection

```python
import vesc_can

# Method 1: Auto-detect first VESC
vesc = vesc_can.connect_to_vesc()

# Method 2: Connect to specific VESC ID
vesc = vesc_can.VESC(vesc_id=0)

# Method 3: Custom CAN interface
vesc = vesc_can.VESC(can_interface='can1', bitrate=1000000)
```

### Reading Data

```python
# Fast cached data (updated at 50Hz automatically)
duty = vesc.get_duty()           # -1.0 to 1.0
rpm = vesc.get_rpm()             # RPM
current = vesc.get_current()     # Motor current (A)  
current_in = vesc.get_current_in()  # Input current (A)
voltage = vesc.get_voltage()     # Input voltage (V)
temp_motor = vesc.get_temp_motor()  # Motor temp (°C)
temp_fet = vesc.get_temp_fet()   # FET temp (°C)
position = vesc.get_position()   # Position (degrees)
fault = vesc.get_fault_code()    # Fault description

# Energy data
amp_hours = vesc.get_amp_hours()
watt_hours = vesc.get_watt_hours()
tachometer = vesc.get_tachometer()

# Check for problems
if vesc.has_fault():
    print(f"VESC fault: {vesc.get_fault_code()}")

# Get all data at once
data = vesc.get_all_data()
```

### Controlling Motor

```python
# Duty cycle control (-1.0 to 1.0)
vesc.set_duty(0.5)        # 50% forward
vesc.set_duty(-0.2)       # 20% reverse
vesc.set_duty(0.0)        # Stop

# Current control (Amperes)
vesc.set_current(3.0)     # 3A forward
vesc.set_current(-2.0)    # 2A reverse

# Speed control (RPM)
vesc.set_rpm(1000)        # 1000 RPM
vesc.set_rpm(-500)        # 500 RPM reverse

# Position control (degrees)
vesc.set_position(90.0)   # Rotate to 90°

# Braking
vesc.set_current_brake(5.0)  # 5A brake current
vesc.set_handbrake(2.0)      # 2A handbrake

# Safety functions
vesc.stop_motor()         # Emergency stop (duty = 0)
vesc.coast_motor()        # Coast (current = 0)
```

### Advanced Data Access

```python
# On-demand data (slower, requires CAN request)
motor_config = vesc.get_motor_config()      # ~100ms
app_config = vesc.get_app_config()          # ~100ms  
ppm_value = vesc.get_decoded_ppm()          # ~50ms
adc_values = vesc.get_decoded_adc()         # ~50ms
fw_version = vesc.get_firmware_version()    # ~100ms

# Send terminal commands
vesc.send_terminal_command("help")
vesc.send_terminal_command("hw_status")
```

### Network Information

```python
# Find all VESCs on network
active_vescs = vesc.get_active_vescs()
print(f"Found VESCs: {list(active_vescs.keys())}")

# Network statistics  
network = vesc.get_network_info()
print(f"My node ID: {network['my_node_id']}")
print(f"Total nodes: {network['total_nodes']}")

# Get this Pi's node ID
my_id = vesc.get_my_node_id()
```

## 📁 Examples

The `examples/` directory contains complete working examples:

### `basic_control.py`
- Simple motor control demonstration
- Forward/reverse movement
- Different control modes
- Safety checks

### `read_sensors.py` 
- Comprehensive sensor reading
- Fast vs. slow data access
- Continuous monitoring
- Data logging to JSON

### `motor_test.py`
- Complete motor test suite
- Performance measurement  
- Safety checks
- Interactive test menu

Run examples:
```bash
cd vesc_can/examples/
python basic_control.py
python read_sensors.py
python motor_test.py
```

## 🏗️ Architecture

The library uses a layered architecture that handles all CAN complexity automatically:

```
Student API (vesc_can.VESC)
    ↓
Background CAN Service  
    ↓
Protocol Layer (encode/decode)
    ↓
CAN Interface (python-can)
    ↓
Linux SocketCAN
```

### Key Components

- **Background Service**: Handles ping/pong, status caching, heartbeats
- **Node Manager**: Automatic unique ID assignment for multiple Pis
- **Protocol Layer**: VESC packet encoding/decoding
- **Hybrid Data**: Fast cached status + on-demand requests
- **Error Handling**: Graceful failures with helpful messages

## 🔧 Configuration

### CAN Interface Setup

```bash
# Basic setup (500 kbps)
sudo ip link set can0 up type can bitrate 500000

# High speed (1 Mbps)  
sudo ip link set can0 up type can bitrate 1000000

# With error counters
sudo ip link set can0 up type can bitrate 500000 restart-ms 100

# Automatic startup (add to /etc/rc.local)
echo "ip link set can0 up type can bitrate 500000" | sudo tee -a /etc/rc.local
```

### Multiple CAN Interfaces

```python
# Use different CAN interface
vesc = vesc_can.VESC(can_interface='can1')

# Use USB-CAN adapter
vesc = vesc_can.VESC(can_interface='slcan0')
```

### Node ID Management

```python
# Force specific node ID (for testing)
import vesc_can.node_manager as nm
nm.get_node_manager().force_node_id(75)

# Check current node ID
my_id = vesc_can.get_network_stats()['my_node_id']
```

## 🚨 Troubleshooting

### Common Issues

**1. "Could not connect to VESC"**
```bash
# Check CAN interface is up
ip link show can0

# Bring up CAN interface
sudo ip link set can0 up type can bitrate 500000

# Check for CAN traffic
candump can0
```

**2. "No VESC found on network"**
```bash
# Send manual ping to see if VESC responds
cansend can0 1100#

# Check VESC Tool can connect
# Verify VESC CAN forwarding is enabled
```

**3. "Permission denied"**
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER

# Log out and back in
```

**4. Import errors**
```bash
# Install missing dependencies
pip install python-can

# Check Python version (3.7+ required)
python --version
```

### Debug Mode

```python
import vesc_can

# Create VESC with debug info
vesc = vesc_can.VESC()

# Show detailed status
vesc.print_status()

# Get service statistics  
if vesc.service:
    stats = vesc.service.get_service_statistics()
    print(f"Messages received: {stats['can_interface_stats']['messages_received']}")
    print(f"Active VESCs: {stats['active_vesc_list']}")
```

### CAN Bus Monitoring

```bash
# Monitor all CAN traffic
candump can0

# Monitor only VESC status messages
candump can0 | grep "09\|0E\|0F\|10\|1B"

# Send test ping
cansend can0 1100#

# Check interface statistics
ip -s link show can0
```

## 🔒 Safety

### Important Safety Guidelines

⚠️ **Always follow these safety practices:**

1. **Test with low values first** - Start with 10% duty cycle or 1A current
2. **Check for faults** - Always call `vesc.has_fault()` before operation
3. **Monitor temperatures** - Stop if motor/FET temps exceed 80°C
4. **Use emergency stops** - Always have `vesc.stop_motor()` ready
5. **Secure connections** - Ensure motor and power connections are tight
6. **Know your limits** - Check VESC and motor specifications

### Safety Checks in Code

```python
import vesc_can

vesc = vesc_can.connect_to_vesc()

# Always check for faults first
if vesc.has_fault():
    print(f"FAULT: {vesc.get_fault_code()}")
    exit()

# Check temperatures
if vesc.get_temp_motor() > 80:
    print("Motor too hot!")
    exit()

if vesc.get_temp_fet() > 80:
    print("FET too hot!")
    exit()

# Check voltage range
voltage = vesc.get_voltage()
if voltage < 5.0 or voltage > 60.0:
    print(f"Voltage out of range: {voltage}V")
    exit()

# Safe to proceed
print("✅ Safety checks passed")
```

## 📚 API Reference

### VESC Class

#### Reading Methods (Fast - from cache)
- `get_duty()` → float: Current duty cycle (-1.0 to 1.0)
- `get_rpm()` → float: Current RPM
- `get_current()` → float: Motor current (A)
- `get_current_in()` → float: Input current (A)  
- `get_voltage()` → float: Input voltage (V)
- `get_temp_motor()` → float: Motor temperature (°C)
- `get_temp_fet()` → float: FET temperature (°C)
- `get_amp_hours()` → float: Amp hours consumed
- `get_watt_hours()` → float: Watt hours consumed
- `get_position()` → float: Motor position (degrees)
- `get_tachometer()` → int: Tachometer value
- `get_fault_code()` → str: Current fault description
- `has_fault()` → bool: True if VESC has any fault

#### Control Methods (Immediate)
- `set_duty(duty: float)` → bool: Set duty cycle (-1.0 to 1.0)
- `set_current(current: float)` → bool: Set motor current (A)
- `set_current_brake(current: float)` → bool: Set brake current (A)
- `set_rpm(rpm: int)` → bool: Set motor RPM
- `set_position(position: float)` → bool: Set position (degrees)
- `set_handbrake(current: float)` → bool: Set handbrake current (A)
- `stop_motor()` → bool: Emergency stop (duty = 0)
- `coast_motor()` → bool: Coast motor (current = 0)

#### Advanced Methods (Slower - on-demand)
- `get_motor_config()` → dict: Motor configuration (~100ms)
- `get_app_config()` → dict: App configuration (~100ms)
- `get_decoded_ppm()` → float: PPM input value (~50ms)
- `get_decoded_adc()` → dict: ADC input values (~50ms)  
- `get_firmware_version()` → str: Firmware version (~100ms)
- `send_terminal_command(cmd: str)` → bool: Send terminal command

#### Network Methods
- `get_active_vescs()` → dict: Active VESCs on network
- `get_network_info()` → dict: Network status
- `get_my_node_id()` → int: This Pi's node ID

#### Utility Methods
- `get_all_data()` → dict: All cached data in one call
- `print_status()`: Print formatted status
- `is_connected()` → bool: Check if connected
- `wait_for_vesc(timeout: float)` → bool: Wait for VESC to appear

### Convenience Functions

- `connect_to_vesc(can_interface='can0', vesc_id=None)` → VESC: Simple connection
- `list_active_vescs(can_interface='can0')` → list: List of VESC IDs
- `get_network_status(can_interface='can0')` → dict: Network information

## 🤝 Contributing

This library is designed for educational use. Contributions welcome!

### Development Setup

```bash
# Clone repository
git clone <repository-url>
cd RaspberryPi-CAN

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black pylint

# Run tests
pytest

# Format code
black vesc_can/
```

### Project Structure

```
RaspberryPi-CAN/
├── vesc_can/
│   ├── __init__.py          # Main student API
│   ├── datatypes.py         # VESC constants and data structures
│   ├── protocol.py          # Packet encoding/decoding
│   ├── can_interface.py     # Low-level CAN communication
│   ├── can_service.py       # Background CAN service
│   ├── node_manager.py      # Node ID management
│   └── examples/            # Example scripts
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 📄 License

This project is open source. Please check the license file for details.

## 🙏 Acknowledgments

- Based on VESC Tool by Benjamin Vedder
- Uses python-can library for CAN communication
- Designed for educational use in high school robotics

## 📞 Support

For questions or issues:

1. Check the troubleshooting section above
2. Run the example scripts to verify setup
3. Check VESC Tool connectivity first
4. Create an issue with details about your setup

---

**Happy motor controlling! 🚗⚡**