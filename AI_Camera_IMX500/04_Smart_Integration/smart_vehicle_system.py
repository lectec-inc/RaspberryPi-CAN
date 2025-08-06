"""
Smart Vehicle System Integration
Combines IMX500 AI Camera with VESC Motor Controller

This module provides the bridge between AI vision detection and motor control,
enabling intelligent vehicle safety and automation systems.

Author: AI Camera IMX500 Course
Level: 4 - Smart Integration
"""

import sys
import os
import time
import threading
import logging
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

# Add core VESC modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

try:
    from student_api import VESCStudentAPI
except ImportError:
    print("⚠️ VESC Student API not found. Ensure core/ directory contains VESC modules.")
    VESCStudentAPI = None

# AI Camera imports
import subprocess
import json

# Optional imports with fallbacks for Jupyter environment
try:
    import cv2
except ImportError:
    print("⚠️ OpenCV not available - image processing will be limited")
    cv2 = None

try:
    import numpy as np
except ImportError:
    print("⚠️ NumPy not available - numerical processing will be limited")
    np = None

try:
    from IPython.display import display, Image
except ImportError:
    print("⚠️ IPython not available - display functions will be limited")
    display = lambda x: print(x)
    Image = None

class SafetyLevel(Enum):
    """Safety levels for intelligent decision making"""
    SAFE = "safe"
    CAUTION = "caution" 
    WARNING = "warning"
    EMERGENCY = "emergency"

class DetectionPriority(Enum):
    """Priority levels for different detected objects"""
    CRITICAL = 1    # Stop signs, traffic lights, barriers
    HIGH = 2        # Pedestrians, cyclists, vehicles
    MEDIUM = 3      # Animals, obstacles
    LOW = 4         # Background objects

@dataclass
class DetectionData:
    """Structured detection information from AI camera"""
    object_name: str
    confidence: float
    bbox: Tuple[int, int, int, int]  # x, y, width, height
    priority: DetectionPriority
    timestamp: float

@dataclass
class MotorData:
    """Motor status information from VESC"""
    speed_kmh: float
    motor_current: float
    battery_voltage: float
    temperature: float
    fault_code: int
    timestamp: float

@dataclass
class SafetyDecision:
    """Safety system decision output"""
    action: str
    reason: str
    safety_level: SafetyLevel
    brake_force: float  # 0.0 to 1.0
    speed_limit: Optional[float]
    timestamp: float

class SmartVehicleSystem:
    """
    🚗 Smart Vehicle System - Level 4 Integration
    
    Combines IMX500 AI camera detection with VESC motor control
    for intelligent vehicle safety and automation systems.
    
    Features:
    - Real-time object detection with motor context
    - Speed-aware AI decision making  
    - Automatic safety responses
    - Multi-sensor data fusion
    - Professional logging and monitoring
    """
    
    def __init__(self, enable_motor=True, debug=False):
        """
        Initialize smart vehicle system
        
        Args:
            enable_motor: Enable actual VESC motor control (False for simulation)
            debug: Enable detailed debug logging
        """
        self.enable_motor = enable_motor
        self.debug = debug
        self.running = False
        
        # Initialize logging
        self._setup_logging()
        
        # Initialize subsystems
        self._init_motor_system()
        self._init_camera_system()
        self._init_safety_system()
        
        # Data storage
        self.recent_detections: List[DetectionData] = []
        self.recent_motor_data: List[MotorData] = []
        self.safety_decisions: List[SafetyDecision] = []
        
        # Configuration
        self.max_history = 100
        self.detection_confidence_threshold = 0.7
        self.emergency_brake_objects = ['stop sign', 'person', 'bicycle']
        self.speed_limits = {
            'person': 10.0,      # km/h - slow near pedestrians
            'bicycle': 15.0,     # km/h - careful around cyclists  
            'stop sign': 0.0,    # km/h - full stop
            'traffic light': 20.0 # km/h - reduced speed
        }
        
        self.logger.info("🚗 Smart Vehicle System initialized")
    
    def _setup_logging(self):
        """Setup professional logging system"""
        self.logger = logging.getLogger('SmartVehicleSystem')
        if self.debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
            
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def _init_motor_system(self):
        """Initialize VESC motor control system"""
        if self.enable_motor and VESCStudentAPI:
            try:
                self.vesc = VESCStudentAPI()
                self.motor_available = True
                self.logger.info("✅ VESC motor system connected")
            except Exception as e:
                self.logger.warning(f"⚠️ VESC connection failed: {e}")
                self.motor_available = False
                self.vesc = None
        else:
            self.motor_available = False
            self.vesc = None
            self.logger.info("🔧 Motor system disabled (simulation mode)")
    
    def _init_camera_system(self):
        """Initialize AI camera system"""
        self.camera_available = True
        self.ai_model_path = "/usr/share/rpi-camera-assets/imx500_mobilenet_ssd.json"
        
        # Verify AI model exists
        if not os.path.exists(self.ai_model_path):
            self.logger.warning("⚠️ AI model file not found - install imx500-models")
            self.camera_available = False
        else:
            self.logger.info("✅ AI camera system ready")
    
    def _init_safety_system(self):
        """Initialize safety monitoring system"""
        self.safety_active = True
        self.emergency_brake_active = False
        self.last_emergency_time = 0
        self.emergency_cooldown = 2.0  # seconds
        
        self.logger.info("✅ Safety system active")
    
    def get_motor_data(self) -> Optional[MotorData]:
        """
        Get current motor status data
        
        Returns:
            MotorData object with current motor status, or None if unavailable
        """
        if not self.motor_available:
            # Simulate motor data for testing
            return MotorData(
                speed_kmh=15.5,
                motor_current=2.3,
                battery_voltage=42.1,
                temperature=35.2,
                fault_code=0,
                timestamp=time.time()
            )
        
        try:
            # Get real VESC data
            status = self.vesc.get_status()
            return MotorData(
                speed_kmh=status.get('speed_kmh', 0.0),
                motor_current=status.get('motor_current', 0.0),
                battery_voltage=status.get('voltage', 0.0),
                temperature=status.get('temperature', 0.0),
                fault_code=status.get('fault_code', 0),
                timestamp=time.time()
            )
        except Exception as e:
            self.logger.error(f"❌ Motor data error: {e}")
            return None
    
    def get_ai_detections(self) -> List[DetectionData]:
        """
        Get current AI detection results
        
        Returns:
            List of DetectionData objects for current frame
        """
        if not self.camera_available:
            # Simulate detections for testing
            return [
                DetectionData(
                    object_name="person",
                    confidence=0.89,
                    bbox=(320, 180, 120, 200),
                    priority=DetectionPriority.HIGH,
                    timestamp=time.time()
                )
            ]
        
        # TODO: Implement real AI detection
        # This would integrate with the IMX500 camera system
        # For now, return empty list
        return []
    
    def classify_detection_priority(self, object_name: str) -> DetectionPriority:
        """
        Classify detection priority based on object type
        
        Args:
            object_name: Name of detected object
            
        Returns:
            DetectionPriority enum value
        """
        critical_objects = ['stop sign', 'traffic light', 'barrier']
        high_priority = ['person', 'bicycle', 'car', 'truck', 'motorcycle']
        medium_priority = ['dog', 'cat', 'obstacle']
        
        if object_name.lower() in critical_objects:
            return DetectionPriority.CRITICAL
        elif object_name.lower() in high_priority:
            return DetectionPriority.HIGH
        elif object_name.lower() in medium_priority:
            return DetectionPriority.MEDIUM
        else:
            return DetectionPriority.LOW
    
    def make_safety_decision(self, detections: List[DetectionData], 
                           motor_data: Optional[MotorData]) -> SafetyDecision:
        """
        Core intelligence: Make safety decision based on AI and motor data
        
        Args:
            detections: List of current AI detections
            motor_data: Current motor status data
            
        Returns:
            SafetyDecision with recommended action
        """
        current_time = time.time()
        current_speed = motor_data.speed_kmh if motor_data else 0.0
        
        # Default safe state
        decision = SafetyDecision(
            action="continue",
            reason="No hazards detected",
            safety_level=SafetyLevel.SAFE,
            brake_force=0.0,
            speed_limit=None,
            timestamp=current_time
        )
        
        # Analyze high-priority detections
        critical_detections = [d for d in detections 
                             if d.priority == DetectionPriority.CRITICAL and 
                             d.confidence > self.detection_confidence_threshold]
        
        high_priority_detections = [d for d in detections 
                                  if d.priority == DetectionPriority.HIGH and
                                  d.confidence > self.detection_confidence_threshold]
        
        # Emergency braking logic
        for detection in critical_detections:
            if detection.object_name.lower() == 'stop sign':
                if current_speed > 5.0:  # Moving towards stop sign
                    return SafetyDecision(
                        action="emergency_brake",
                        reason=f"Stop sign detected with {detection.confidence:.1%} confidence",
                        safety_level=SafetyLevel.EMERGENCY,
                        brake_force=0.8,
                        speed_limit=0.0,
                        timestamp=current_time
                    )
                else:
                    return SafetyDecision(
                        action="full_stop",
                        reason="At stop sign - full stop required",
                        safety_level=SafetyLevel.WARNING,
                        brake_force=1.0,
                        speed_limit=0.0,
                        timestamp=current_time
                    )
        
        # Pedestrian safety logic
        for detection in high_priority_detections:
            if detection.object_name.lower() == 'person':
                # Calculate distance approximation from bbox size
                person_size = detection.bbox[2] * detection.bbox[3]
                if person_size > 15000:  # Large bbox = close person
                    return SafetyDecision(
                        action="slow_down",
                        reason=f"Pedestrian detected close by ({detection.confidence:.1%} confidence)",
                        safety_level=SafetyLevel.WARNING,
                        brake_force=0.3,
                        speed_limit=10.0,
                        timestamp=current_time
                    )
                elif current_speed > 20.0:  # Too fast near pedestrians
                    return SafetyDecision(
                        action="reduce_speed",
                        reason=f"Pedestrian detected - reducing speed ({detection.confidence:.1%} confidence)",
                        safety_level=SafetyLevel.CAUTION,
                        brake_force=0.1,
                        speed_limit=15.0,
                        timestamp=current_time
                    )
        
        return decision
    
    def execute_safety_action(self, decision: SafetyDecision):
        """
        Execute safety decision using motor control
        
        Args:
            decision: SafetyDecision to execute
        """
        if not self.motor_available:
            self.logger.info(f"🔧 SIMULATION: Would execute {decision.action} - {decision.reason}")
            return
        
        try:
            if decision.action == "emergency_brake":
                self.vesc.set_brake(decision.brake_force)
                self.emergency_brake_active = True
                self.last_emergency_time = time.time()
                self.logger.warning(f"🚨 EMERGENCY BRAKE: {decision.reason}")
                
            elif decision.action == "full_stop":
                self.vesc.set_brake(1.0)
                self.logger.warning(f"🛑 FULL STOP: {decision.reason}")
                
            elif decision.action == "slow_down":
                self.vesc.set_brake(decision.brake_force)
                self.logger.info(f"⚠️ SLOWING DOWN: {decision.reason}")
                
            elif decision.action == "reduce_speed":
                # Implement speed limiting logic here
                self.logger.info(f"🐌 SPEED REDUCTION: {decision.reason}")
                
        except Exception as e:
            self.logger.error(f"❌ Safety action failed: {e}")
    
    def process_intelligent_frame(self) -> SafetyDecision:
        """
        Main processing loop: Get data, analyze, decide, act
        
        Returns:
            SafetyDecision made for this frame
        """
        # Get current sensor data
        detections = self.get_ai_detections()
        motor_data = self.get_motor_data()
        
        # Store in history
        self.recent_detections.extend(detections)
        if motor_data:
            self.recent_motor_data.append(motor_data)
        
        # Trim history
        if len(self.recent_detections) > self.max_history:
            self.recent_detections = self.recent_detections[-self.max_history:]
        if len(self.recent_motor_data) > self.max_history:
            self.recent_motor_data = self.recent_motor_data[-self.max_history:]
        
        # Make intelligent decision
        decision = self.make_safety_decision(detections, motor_data)
        
        # Store decision
        self.safety_decisions.append(decision)
        if len(self.safety_decisions) > self.max_history:
            self.safety_decisions = self.safety_decisions[-self.max_history:]
        
        # Execute action
        if decision.safety_level != SafetyLevel.SAFE:
            self.execute_safety_action(decision)
        
        return decision
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get comprehensive system status
        
        Returns:
            Dictionary with system status information
        """
        return {
            'motor_available': self.motor_available,
            'camera_available': self.camera_available,
            'safety_active': self.safety_active,
            'emergency_brake_active': self.emergency_brake_active,
            'recent_detections_count': len(self.recent_detections),
            'recent_decisions_count': len(self.safety_decisions),
            'last_motor_data': self.recent_motor_data[-1] if self.recent_motor_data else None,
            'last_decision': self.safety_decisions[-1] if self.safety_decisions else None
        }
    
    def start_intelligent_monitoring(self, duration=30):
        """
        Start intelligent monitoring loop
        
        Args:
            duration: How long to run monitoring (seconds)
        """
        self.logger.info(f"🚀 Starting intelligent monitoring for {duration} seconds")
        self.running = True
        
        start_time = time.time()
        frame_count = 0
        
        try:
            while self.running and (time.time() - start_time) < duration:
                decision = self.process_intelligent_frame()
                frame_count += 1
                
                # Log significant decisions
                if decision.safety_level != SafetyLevel.SAFE:
                    self.logger.info(f"📊 Frame {frame_count}: {decision.action} - {decision.reason}")
                
                time.sleep(0.1)  # 10 FPS processing
                
        except KeyboardInterrupt:
            self.logger.info("⏹️ Monitoring stopped by user")
        finally:
            self.running = False
            
        self.logger.info(f"✅ Monitoring complete: {frame_count} frames processed")
    
    def stop_monitoring(self):
        """Stop intelligent monitoring"""
        self.running = False
        self.logger.info("⏹️ Stopping intelligent monitoring")
    
    def cleanup(self):
        """Cleanup system resources"""
        self.stop_monitoring()
        if self.motor_available and self.vesc:
            try:
                self.vesc.stop()
                self.logger.info("✅ Motor system cleaned up")
            except:
                pass
        self.logger.info("✅ Smart Vehicle System cleanup complete")