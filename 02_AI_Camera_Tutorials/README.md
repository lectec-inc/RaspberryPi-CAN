# 🤖 AI Camera IMX500 - Student Introduction to Artificial Intelligence

Welcome to your journey into the world of **Artificial Intelligence and Computer Vision**! This educational series will take you from complete beginner to building real AI-powered applications using the Sony IMX500 AI Camera.

## 🎯 What You'll Learn

By the end of this course, you'll understand:
- How AI cameras work and what makes them "intelligent"
- Real-time object detection and computer vision
- Integrating AI with hardware (buzzers, motors, sensors)
- Building practical AI applications for safety and automation
- Optimizing AI performance on embedded systems

## 🔧 Hardware Requirements

- **Raspberry Pi Zero 2W** (or Pi 4/5)
- **Sony IMX500 AI Camera** (Raspberry Pi AI Camera)
- **Buzzer** connected to GPIO pin 17
- **VESC motor controller** (for advanced lessons)
- **CAN interface** (for motor integration)

## 📚 Learning Path - 5 Progressive Levels

### 🏁 **Level 1: Getting Started** (Foundation)
**Learn the basics of AI cameras and computer vision**

- `Camera_Preview.ipynb` - Your first camera experience
- `What_is_AI_Camera.ipynb` - Understanding intelligent vision
- `Camera_Setup_Check.ipynb` - Hardware verification and diagnostics

**Learning Goals**: Understand what makes cameras "AI-powered", set up hardware, capture your first images

---

### 🧠 **Level 2: First AI Detection** (Core AI)
**Experience real-time object detection for the first time**

- `Basic_Object_Detection.ipynb` - Your first AI detection experience
- `Understanding_Results.ipynb` - Confidence scores and bounding boxes
- `Detection_Experiments.ipynb` - Hands-on testing and exploration
- `Object_Types_Guide.ipynb` - What can the AI detect?

**Learning Goals**: Run object detection, understand AI results, experiment with different objects

---

### 🔊 **Level 3: Interactive AI** (Responsive Systems)
**Make AI respond to the world with sound and alerts**

- `AI_with_Buzzer_Alerts.ipynb` - Combine AI detection with audio alerts
- `Custom_Alert_Patterns.ipynb` - Different sounds for different objects
- `Detection_Counters.ipynb` - Count and track objects over time
- `Smart_Notifications.ipynb` - Conditional alerts and logic

**Learning Goals**: Integrate GPIO hardware, create responsive AI systems, build conditional logic

---

### 🚗 **Level 4: Smart Integration** (Multi-sensor Systems)
**Combine AI vision with motor data for intelligent systems**

- `AI_Plus_Motor_Data.ipynb` - Integrate camera AI with VESC motor data
- `Safety_Systems.ipynb` - Stop sign detection with speed monitoring
- `Smart_Braking.ipynb` - Automatic safety responses
- `Environmental_Awareness.ipynb` - Multi-sensor fusion

**Learning Goals**: Sensor fusion, safety systems, real-world AI applications

---

### 🏆 **Level 5: Real World Projects** (Applied AI)
**Build complete AI applications for real problems**

- `Autonomous_Safety_Assistant.ipynb` - Complete vehicle safety system
- `Smart_Parking_Helper.ipynb` - AI-powered parking assistance
- `Traffic_Monitor.ipynb` - Count and classify vehicles
- `Custom_AI_Builder.ipynb` - Design your own AI application

**Learning Goals**: Complete applications, project design, real-world problem solving

---

## 🚀 Quick Start Guide

### Step 1: Hardware Setup
1. Connect Sony IMX500 AI Camera to your Raspberry Pi
2. Connect buzzer to GPIO pin 17 (positive to pin 17, negative to ground)
3. Ensure Pi is running Raspberry Pi OS Lite (64-bit) for best performance

### Step 2: Software Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install python3-opencv python3-numpy python3-matplotlib
sudo pip3 install jupyter ipywidgets

# Enable camera
sudo raspi-config  # Interface Options -> Camera -> Enable
```

### Step 3: Start Learning
```bash
# Navigate to lessons
cd /home/pi/RaspberryPi-CAN/AI_Camera_IMX500

# Start with Level 1
cd 01_Getting_Started
jupyter notebook Camera_Preview.ipynb
```

## 💡 Important Notes for SSH/Headless Use

This course is designed for **headless operation via SSH**:
- All camera displays appear **inline in notebooks**
- No desktop environment required
- Images are displayed directly in Jupyter cells
- Optimized for Pi Zero 2W performance

### Accessing Notebooks via SSH
```bash
# Start Jupyter on Pi (SSH session)
jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root

# Then access from your computer's browser:
http://[PI_IP_ADDRESS]:8888
```

## 🔒 Safety and Best Practices

### Hardware Safety
- Always verify GPIO connections before powering on
- Use appropriate resistors for LEDs and buzzers
- Keep camera lens clean for best AI detection
- Monitor Pi temperature during intensive AI processing

### AI Safety
- Understand AI limitations - it's not 100% accurate
- Always have manual overrides for safety-critical applications
- Test thoroughly before deploying in real scenarios
- Consider edge cases and failure modes

## 📊 Performance Optimization for Pi Zero 2W

### Recommended Settings
```python
# Optimal for Pi Zero 2W
resolution = (1280, 720)    # HD instead of Full HD
framerate = 20              # 20fps instead of 30fps
detection_interval = 0.5    # Check every 500ms for multi-sensor apps
```

### Resource Management
- Use Pi OS Lite (not Desktop version)
- Close unnecessary processes
- Monitor CPU temperature
- Consider passive cooling for sustained operation

## 🆘 Troubleshooting

### Camera Issues
```bash
# Check camera detection
rpicam-hello --list-cameras

# Test basic camera
rpicam-hello -t 5000

# Test AI detection
rpicam-hello -t 5000 --post-process-file /usr/share/rpi-camera-assets/imx500_mobilenet_ssd.json
```

### GPIO Issues
```bash
# Test buzzer
sudo gpioset gpiochip0 17=1  # On
sudo gpioset gpiochip0 17=0  # Off
```

### Performance Issues
- Lower resolution and framerate
- Use Pi OS Lite instead of Desktop
- Add passive cooling
- Check for thermal throttling: `vcgencmd measure_temp`

## 📈 Learning Progression

**Beginner** (Levels 1-2): 2-4 hours
- Basic camera operation
- First AI detection experience
- Understanding computer vision concepts

**Intermediate** (Level 3): 2-3 hours
- GPIO integration
- Interactive AI systems
- Custom alert patterns

**Advanced** (Levels 4-5): 4-6 hours
- Multi-sensor integration
- Complete AI applications
- Real-world problem solving

## 🎓 Assessment and Certification

Complete the challenges in each level to master the concepts:
- **Level 1**: Successfully capture and display camera images
- **Level 2**: Detect and identify 10+ different objects
- **Level 3**: Create custom buzzer patterns for different objects
- **Level 4**: Build a working safety system with stop sign detection
- **Level 5**: Design and implement your own AI application

## 🔗 Additional Resources

- [Sony IMX500 Documentation](https://developer.aitrios.sony-semicon.com/en/raspberrypi-ai-camera/)
- [Raspberry Pi AI Camera Guide](https://www.raspberrypi.com/documentation/accessories/ai-camera.html)
- [Computer Vision Fundamentals](resources/AI_Concepts_Guide.md)
- [Hardware Setup Guide](resources/Hardware_Setup.md)

## 🤝 Getting Help

If you get stuck:
1. Check the troubleshooting section above
2. Review the concepts in `resources/AI_Concepts_Guide.md`
3. Try the solutions in `solutions/Exercise_Solutions.ipynb`
4. Ask your instructor or study group

---

**Ready to dive into the fascinating world of AI? Let's start with Level 1!** 🚀

*This course was designed to be practical, hands-on, and fun. Every lesson builds on the previous one, so take your time and enjoy the journey into artificial intelligence!*