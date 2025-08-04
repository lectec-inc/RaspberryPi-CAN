# VESC Motor Controller - Python API

A simple Python library that lets you **talk to** and **control** VESC motor controllers from a Raspberry Pi. Perfect for learning about electric motors, building robots, or creating your own electric vehicle projects!

## What is This?

This project lets you:
- **Read information** from a VESC motor controller (like speed, temperature, battery voltage)
- **Control the motor** safely (start, stop, set speed, brake)
- **See live data** with graphs and dashboards
- **Learn about electric motors** through hands-on examples

Think of it like having a conversation with your motor controller - you can ask it questions ("How fast are you spinning?") and give it commands ("Speed up to 50%").

## Features

- **🎓 Student-Friendly** - Written for beginners, no complex setup needed
- **📊 Real-Time Data** - See motor speed, power usage, temperatures, and more
- **🔒 Safety First** - Built-in protections to prevent accidents
- **📓 Learning Materials** - Complete with Jupyter notebooks and examples
- **⚡ Ready to Use** - Works out of the box on Raspberry Pi

## Quick Start Guide

### Step 1: Basic Connection

```python
from student_api import VESCStudentAPI
import time

# Create API instance
vesc_api = VESCStudentAPI()

# Start the VESC system
if vesc_api.start():
    print("VESC system started successfully!")
    
    # Get controller for VESC ID 74 (as specified in README)
    vesc = vesc_api.get_controller(74)
    
    if vesc:
        print("Connected to VESC controller!")
    else:
        print("Failed to get VESC controller")
else:
    print("Failed to start VESC system")
```

### Step 2: Read Motor Information

```python
# Get motor information
rpm = vesc.get_rpm()                    # How fast is the motor spinning?
current = vesc.get_motor_current()      # How much electricity is it using?
voltage = vesc.get_input_voltage()      # What's the battery voltage?
temperature = vesc.get_motor_temperature()  # How hot is the motor?

print(f"Motor Speed: {rpm} RPM")
print(f"Power Usage: {current} A")
print(f"Battery: {voltage} V")
print(f"Temperature: {temperature}°C")
```

### Step 3: Try the Dashboard

See live data updating in real-time:

```bash
python examples/dashboard.py
```

### Step 4: Learn with Jupyter Notebooks

Open these notebooks to learn step-by-step:
- **`examples/fundamentals_intro.ipynb`** - Perfect for beginners! Learn the basics
- **`examples/basic_usage_example.ipynb`** - Simple examples to get started
- **`examples/realtime_visualization.ipynb`** - See data as live graphs
- **`examples/dashboard_notebook.ipynb`** - Interactive dashboard in your browser
- **`examples/advanced_control_example.ipynb`** - Advanced features and data logging

**📓 Important:** Each notebook has a setup cell at the top that must be run first - it configures the Python path to find the student_api.

## What Can You Do? (Available Functions)

### 📖 Reading Information from the VESC

These functions let you **ask questions** to the VESC and get answers:

```python
# 🏃 Motor Speed and Power
vesc.get_rpm()                    # How fast is motor spinning? (RPM)
vesc.get_motor_current()          # How much power is motor using? (Amperes)
vesc.get_duty_cycle()             # What's the throttle setting? (0 to 100%)

# 🔋 Battery and Energy Information
vesc.get_input_voltage()          # What's the battery voltage? (Volts)
vesc.get_input_current()          # How much power from battery? (Amperes)
vesc.get_amp_hours_consumed()     # How much energy used? (Amp Hours)
vesc.get_amp_hours_charged()      # How much energy recovered? (Amp Hours)
vesc.get_watt_hours_consumed()    # How much power used? (Watt Hours)
vesc.get_watt_hours_charged()     # How much power recovered? (Watt Hours)

# 🌡️ Temperature Monitoring (Important for Safety!)
vesc.get_fet_temperature()        # How hot is the controller? (°C)
vesc.get_motor_temperature()      # How hot is the motor? (°C)

# 📊 Advanced Sensors (These may show 0 if nothing is connected)
vesc.get_tachometer_value()       # Total rotations (like odometer)
vesc.get_pid_position()           # Precise position control
vesc.get_adc_voltage_ext()        # Extra sensor 1 voltage
vesc.get_adc_voltage_ext2()       # Extra sensor 2 voltage  
vesc.get_adc_voltage_ext3()       # Extra sensor 3 voltage
vesc.get_servo_value()            # Remote control input

# 🎯 Get Everything at Once (Super Convenient!)
vesc.get_all_telemetry()          # Returns all data organized in groups
```

### 🎮 Controlling the Motor (Be Careful!)

These functions let you **give commands** to the VESC:

```python
# ⚠️ ONLY use these when it's safe for the motor to move!

vesc.set_duty_cycle(0.1)          # Set speed (10% forward)
vesc.set_duty_cycle(-0.1)         # Set speed (10% backward)  
vesc.set_duty_cycle(0)            # STOP the motor

vesc.set_current(2.0)             # Set force/torque (2 Amperes)
vesc.set_brake_current(1.0)       # Apply regenerative braking (1 Ampere)
```

### 🔧 Getting More Information (For Advanced Users)

```python
# Show detailed system information (for debugging)
vesc_api = VESCStudentAPI(quiet=False)
```

## How It Works (System Overview)

This project has several parts that work together:

- **`student_api.py`** - The main file you use (this talks to students!)
- **`main.py`** - Manages the system and keeps everything running  
- **`vesc_interface.py`** - Handles communication with the VESC
- **`protocol.py`** - Understands the VESC's language (message parsing)
- **`commands.py`** - Knows how to send motor control commands
- **`dashboard.py`** - Creates the live data dashboard
- **Jupyter Notebooks** - Interactive learning materials

## Hardware Setup (Already Done for You!)

Your Raspberry Pi comes pre-configured with:
- **Raspberry Pi Zero 2W** - The computer that runs this code
- **CAN Interface** - Set up to talk to VESC at 500kbps (that's the communication speed)
- **VESC Controller** - The motor controller (ID: 74)
- **VESC-Express ESP32** - Additional controller (ID: 2)

**If you ever need to fix the CAN setup:**
```bash
sudo ip link set can0 down                    # Turn off CAN
sudo ip link set can0 type can bitrate 500000 # Set speed to 500k
sudo ip link set can0 up                      # Turn on CAN
candump can0                                   # Watch CAN messages
```

## Testing Your Setup

Make sure everything works by running these tests:

```bash
# Test individual parts
python tests/unit_tests.py          

# Test the whole system  
python tests/integration_test.py    

# See live data
python examples/dashboard.py           

# Check connections
python examples/diagnostic_check.py
```

## 🔒 SAFETY FIRST! (Very Important!)

**Before you control any motor, always remember:**

### ⚠️ Safety Rules:
1. **Make sure it's safe** - Nothing should be able to get hurt if the motor moves
2. **Start small** - Begin with very low power settings (like 10% or less)
3. **Know how to stop** - Always use `vesc.set_duty_cycle(0)` to stop immediately
4. **Watch temperatures** - If things get too hot (over 80°C), stop and let them cool down
5. **Secure the motor** - Make sure it can't move anything dangerous

### 🛑 Emergency Stop:
```python
# Use this to stop everything immediately
vesc.set_duty_cycle(0)      # Stop throttle
vesc.set_current(0)         # Stop current
vesc.set_brake_current(0)   # Stop braking
```

### 🌡️ Temperature Safety:
- **Controller over 80°C** = Stop and let it cool down
- **Motor over 100°C** = Stop immediately and let it cool down

The system has built-in safety features, but **you** are the most important safety feature!

## What's in This Project? (File Overview)

```
RaspberryPi-CAN/
├── 🎯 student_api.py                 # ← START HERE! Main API for students
├── 📖 README.md                      # This file!
│
├── 📁 examples/                      # All example files
│   ├── 📊 dashboard.py               # Real-time data dashboard
│   ├── 🩺 diagnostic_check.py        # Check connections
│   ├── 📓 fundamentals_intro.ipynb   # Perfect for beginners!
│   ├── 📓 basic_usage_example.ipynb  # Simple examples  
│   ├── 📓 realtime_visualization.ipynb # Live graphs and charts
│   ├── 📓 dashboard_notebook.ipynb   # Interactive dashboard
│   └── 📓 advanced_control_example.ipynb # Advanced features
│
├── 📁 core/                          # Core system files
│   ├── 🔧 main.py                    # System manager
│   ├── 🔧 vesc_interface.py          # CAN communication
│   ├── 🔧 protocol.py                # Message parsing
│   └── 🔧 commands.py                # Motor commands
│
├── 📁 tests/                         # Test files
│   ├── 🧪 unit_tests.py              # Test individual functions
│   └── 🧪 integration_test.py        # Test complete system
│
└── 📁 ai_camera/                     # Future AI camera files
    └── (ready for Sony IMX500 files)
```

## Learning Path (Where to Start)

**New to electric motors?** Follow this path:
1. 📖 Read this README (you're doing it!)
2. 📓 Open `examples/fundamentals_intro.ipynb` - Learn the basics
3. 📓 Try `examples/basic_usage_example.ipynb` - Simple examples
4. 📊 Run `python examples/dashboard.py` - See live data
5. 📓 Explore `examples/realtime_visualization.ipynb` - Cool graphs!
6. 📓 Advanced: Try `examples/advanced_control_example.ipynb`

**Just want to see data?** 
- Run `python examples/dashboard.py` or open `examples/dashboard_notebook.ipynb`

**Something not working?**
- Run `python examples/diagnostic_check.py` to troubleshoot

## How It Really Works (Technical Details)

The VESC motor controller sends out information 50 times per second (that's 50Hz!) using something called "Status Messages." Think of it like the VESC is constantly broadcasting on a radio station, telling everyone what's happening with the motor.

Our Python code "listens" to this radio station and organizes all the information so you can easily ask questions like "What's the motor speed?" and get instant answers.

When you want to control the motor, our code sends special command messages back to the VESC, like tuning into the VESC's control frequency and saying "Please speed up to 20%."

All of this happens through a **CAN bus** - which is like a special computer network that's really good at handling lots of messages very quickly and reliably. It's the same technology used in cars, robots, and other places where safety and speed are important.

## 🚀 How to Run Examples

**✅ IMPORTANT: Always run from the main project directory!**

```bash
# ✅ Correct way (from RaspberryPi-CAN/ folder):
python examples/dashboard.py
python examples/diagnostic_check.py
python tests/unit_tests.py

# For Jupyter notebooks, you can run them from anywhere:
jupyter notebook examples/fundamentals_intro.ipynb
# OR
cd examples && jupyter notebook fundamentals_intro.ipynb

# ❌ Wrong way for Python files (don't do this):
cd examples && python dashboard.py  # Won't work - can't find student_api
```

**Why?** 
- **Python files** need to import `student_api.py` from the main directory, so run them from the root
- **Jupyter notebooks** have a setup cell that automatically configures the path, so they work from anywhere!

## Need Help?

**First, try these:**
- Run `python examples/diagnostic_check.py` to check your connections
- Make sure the VESC is powered on
- Check that you're using the right VESC ID (74)

**Still having trouble?** Look at the error messages carefully - they usually tell you exactly what's wrong!

**Want to learn more?** The Jupyter notebooks have tons of examples and explanations written just for students.

---

**Have fun learning about electric motors! 🚗⚡**