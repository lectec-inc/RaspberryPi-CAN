"""
***DO NOT EDIT***
Student API for VESC Motor Controllers
High-level Python API for students to interact with VESC motor controllers.
***DO NOT EDIT***
"""

import time
import threading
from typing import Optional, Dict, Any, List, Tuple
from core.main import VESCSystemManager


class VESCController:
    """High-level interface to a VESC motor controller"""
    
    def __init__(self, controller_id: int, system_manager: VESCSystemManager):
        self.controller_id = controller_id
        self.system_manager = system_manager
        self.interface = system_manager.get_interface()
        self._last_command_time = 0
        self._command_delay = 0.1  # Minimum time between commands
        self._max_safe_brake_current = 10.0
        self._min_safe_ramp_time = 3.0
        self._max_safe_ramp_time = 10.0
        self._min_brake_interval = 1.0
        self._last_brake_command_time = 0.0
    
    def _check_command_rate(self):
        """Ensure commands aren't sent too frequently"""
        current_time = time.time()
        if current_time - self._last_command_time < self._command_delay:
            time.sleep(self._command_delay - (current_time - self._last_command_time))
        self._last_command_time = time.time()
    
    def _get_telemetry_value(self, data_type: str, field: str) -> Optional[float]:
        """Get a specific telemetry value"""
        return self.interface.get_telemetry_value(self.controller_id, data_type, field)
    
    def _get_live_data(self) -> Dict[str, Any]:
        """Get all live data for this controller"""
        return self.interface.get_live_data(self.controller_id) or {}
    
    # ==================== READ FUNCTIONS ====================
    
    def get_rpm(self) -> Optional[float]:
        """Get motor RPM"""
        return self._get_telemetry_value('status_1', 'rpm')
    
    def get_motor_current(self) -> Optional[float]:
        """Get motor current in amperes"""
        return self._get_telemetry_value('status_1', 'current')
    
    def get_duty_cycle(self) -> Optional[float]:
        """Get duty cycle (-1.0 to 1.0)"""
        return self._get_telemetry_value('status_1', 'duty_cycle')
    
    def get_amp_hours_consumed(self) -> Optional[float]:
        """Get amp-hours consumed"""
        return self._get_telemetry_value('status_2', 'amp_hours')
    
    def get_amp_hours_charged(self) -> Optional[float]:
        """Get amp-hours charged"""
        return self._get_telemetry_value('status_2', 'amp_hours_charged')
    
    def get_watt_hours_consumed(self) -> Optional[float]:
        """Get watt-hours consumed"""
        return self._get_telemetry_value('status_3', 'watt_hours')
    
    def get_watt_hours_charged(self) -> Optional[float]:
        """Get watt-hours charged"""
        return self._get_telemetry_value('status_3', 'watt_hours_charged')
    
    def get_fet_temperature(self) -> Optional[float]:
        """Get FET temperature in Celsius"""
        return self._get_telemetry_value('status_4', 'temp_fet')
    
    def get_motor_temperature(self) -> Optional[float]:
        """Get motor temperature in Celsius"""
        return self._get_telemetry_value('status_4', 'temp_motor')
    
    def get_input_current(self) -> Optional[float]:
        """Get input current in amperes"""
        return self._get_telemetry_value('status_4', 'current_in')
    
    def get_pid_position(self) -> Optional[float]:
        """Get PID position value"""
        return self._get_telemetry_value('status_4', 'pid_pos_now')
    
    def get_tachometer_value(self) -> Optional[int]:
        """Get tachometer value"""
        return self._get_telemetry_value('status_5', 'tacho_value')
    
    def get_input_voltage(self) -> Optional[float]:
        """Get input voltage in volts"""
        return self._get_telemetry_value('status_5', 'v_in')
    
    def get_adc_voltage_ext(self) -> Optional[float]:
        """Get ADC voltage from EXT channel"""
        return self._get_telemetry_value('status_6', 'adc_1')
    
    def get_adc_voltage_ext2(self) -> Optional[float]:
        """Get ADC voltage from EXT2 channel"""
        return self._get_telemetry_value('status_6', 'adc_2')
    
    def get_adc_voltage_ext3(self) -> Optional[float]:
        """Get ADC voltage from EXT3 channel"""
        return self._get_telemetry_value('status_6', 'adc_3')
    
    def get_servo_value(self) -> Optional[float]:
        """Get servo/PPM value"""
        return self._get_telemetry_value('status_6', 'ppm')
    
    def get_all_telemetry(self) -> Dict[str, Any]:
        """Get all telemetry data in a structured format"""
        data = self._get_live_data()
        
        telemetry = {
            'controller_id': self.controller_id,
            'timestamp': data.get('last_update', 0),
            'motor': {
                'rpm': self.get_rpm(),
                'current': self.get_motor_current(),
                'duty_cycle': self.get_duty_cycle(),
                'temperature': self.get_motor_temperature(),
            },
            'power': {
                'input_voltage': self.get_input_voltage(),
                'input_current': self.get_input_current(),
                'amp_hours_consumed': self.get_amp_hours_consumed(),
                'amp_hours_charged': self.get_amp_hours_charged(),
                'watt_hours_consumed': self.get_watt_hours_consumed(),
                'watt_hours_charged': self.get_watt_hours_charged(),
            },
            'temperatures': {
                'fet': self.get_fet_temperature(),
                'motor': self.get_motor_temperature(),
            },
            'sensors': {
                'tachometer': self.get_tachometer_value(),
                'pid_position': self.get_pid_position(),
                'adc_ext': self.get_adc_voltage_ext(),
                'adc_ext2': self.get_adc_voltage_ext2(),
                'adc_ext3': self.get_adc_voltage_ext3(),
                'servo_value': self.get_servo_value(),
            }
        }
        
        return telemetry
    
    # ==================== WRITE FUNCTIONS ====================
    
    def set_duty_cycle(self, duty_cycle: float) -> bool:
        """Drive-by-duty commands are not part of the student brake-control API."""
        raise RuntimeError("set_duty_cycle is not available in the student brake-control API.")

    def set_current(self, current: float) -> bool:
        """Drive-current commands are not part of the student brake-control API."""
        raise RuntimeError("set_current is not available in the student brake-control API.")

    def set_rpm(self, rpm: float) -> bool:
        """RPM drive commands are not part of the student brake-control API."""
        raise RuntimeError("set_rpm is not available in the student brake-control API.")

    def set_brake_current(self, current_a: float, ramp_time_s: float) -> bool:
        """
        Apply a bounded brake sequence with smooth ramping.

        Args:
            current_a: Target brake current in amperes. Allowed range: 0.0 to 10.0.
            ramp_time_s: Ramp-up time in seconds. Allowed range: 3.0 to 10.0.

        Returns:
            True if sequence is sent successfully, False otherwise.
        """
        if not 0.0 <= current_a <= self._max_safe_brake_current:
            raise ValueError(
                f"Brake current must be between 0.0 and {self._max_safe_brake_current} amperes"
            )
        if not self._min_safe_ramp_time <= ramp_time_s <= self._max_safe_ramp_time:
            raise ValueError(
                f"Ramp time must be between {self._min_safe_ramp_time} and {self._max_safe_ramp_time} seconds"
            )

        now = time.time()
        if now - self._last_brake_command_time < self._min_brake_interval:
            return False

        self._check_command_rate()

        step_s = 0.1
        ramp_up_steps = max(1, int(round(ramp_time_s / step_s)))
        ramp_down_steps = 10  # fixed 1.0 second release ramp

        try:
            self._last_brake_command_time = now

            for i in range(1, ramp_up_steps + 1):
                level = current_a * (i / ramp_up_steps)
                self.interface.send_command(
                    self.controller_id,
                    'brake',
                    level,
                    callback=None,
                    timeout=2.0,
                    expect_response=False
                )
                time.sleep(step_s)

            for j in range(1, ramp_down_steps + 1):
                level = current_a * (1 - (j / ramp_down_steps))
                self.interface.send_command(
                    self.controller_id,
                    'brake',
                    max(0.0, level),
                    callback=None,
                    timeout=2.0,
                    expect_response=False
                )
                time.sleep(step_s)

            self.interface.send_command(
                self.controller_id,
                'brake',
                0.0,
                callback=None,
                timeout=2.0,
                expect_response=False
            )
            return True

        except Exception as e:
            print(f"Error setting brake current: {e}")
            return False

    def stop_motor(self) -> bool:
        """Request a standard safe brake sequence."""
        return self.set_brake_current(3.0, 3.0)

    def is_connected(self) -> bool:
        """Check if controller is connected and responding"""
        data = self._get_live_data()
        if not data or 'last_update' not in data:
            return False
        
        # Consider connected if we received data within last 2 seconds
        return time.time() - data['last_update'] < 2.0


class VESCStudentAPI:
    """Main student API for VESC motor controllers"""
    
    def __init__(self, can_channel: str = 'can0', quiet: bool = True):
        self.system_manager = VESCSystemManager(can_channel, quiet=quiet)
        self.controllers: Dict[int, VESCController] = {}
        self._started = False
    
    def start(self) -> bool:
        """Start the VESC system"""
        if self._started:
            return True
        
        if self.system_manager.start():
            self._started = True
            # Give system time to discover controllers
            time.sleep(2.0)
            return True
        return False
    
    def stop(self):
        """Stop the VESC system"""
        if self._started:
            self.system_manager.stop()
            self._started = False
    
    def get_controller(self, controller_id: int) -> VESCController:
        """Get a controller interface"""
        if not self._started:
            raise RuntimeError("VESC system not started. Call start() first.")
        
        if controller_id not in self.controllers:
            self.controllers[controller_id] = VESCController(controller_id, self.system_manager)
        
        return self.controllers[controller_id]
    
    def get_connected_controllers(self) -> list:
        """Get list of connected controller IDs"""
        if not self._started:
            return []
        
        return self.system_manager.get_controller_ids()
    
    def is_running(self) -> bool:
        """Check if system is running"""
        return self._started and self.system_manager.is_running()



class AIStudentAPI:
    """High-level student API for IMX500 AI camera object detection"""

    # COCO labels aligned with IMX500 MobileNet SSD output indices
    COCO_LABELS = [
        "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
        "traffic light", "fire hydrant", "", "stop sign", "parking meter", "bench", "bird", "cat",
        "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "", "backpack",
        "umbrella", "", "", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
        "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
        "tennis racket", "bottle", "", "wine glass", "cup", "fork", "knife", "spoon", "bowl",
        "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza",
        "donut", "cake", "chair", "couch", "potted plant", "bed", "", "dining table", "", "",
        "toilet", "", "tv", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave",
        "oven", "toaster", "sink", "refrigerator", "", "book", "clock", "vase", "scissors",
        "teddy bear", "hair drier", "toothbrush"
    ]

    def __init__(
        self,
        model_path: str = '/usr/share/imx500-models/imx500_network_ssd_mobilenetv2_fpnlite_320x320_pp.rpk',
        confidence_threshold: float = 0.5,
        frame_rate: int = 30,
        quiet: bool = True,
    ):
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.frame_rate = frame_rate
        self.quiet = quiet

        self._started = False
        self._lock = threading.Lock()

        # Lazy-loaded runtime objects
        self._np = None
        self._Picamera2 = None
        self._IMX500 = None
        self._NetworkIntrinsics = None

        self._imx500 = None
        self._intrinsics = None
        self._picam2 = None

    def _lazy_import_camera_stack(self):
        """Load camera dependencies only when needed."""
        if self._Picamera2 is not None:
            return

        import numpy as np
        from picamera2 import Picamera2
        from picamera2.devices import IMX500
        from picamera2.devices.imx500 import NetworkIntrinsics

        self._np = np
        self._Picamera2 = Picamera2
        self._IMX500 = IMX500
        self._NetworkIntrinsics = NetworkIntrinsics

    def start_camera(self) -> bool:
        """Start the AI camera and detection model."""
        with self._lock:
            if self._started:
                return True

            try:
                self._lazy_import_camera_stack()

                self._imx500 = self._IMX500(self.model_path)
                self._intrinsics = self._imx500.network_intrinsics or self._NetworkIntrinsics()
                self._intrinsics.task = 'object detection'
                self._intrinsics.labels = self.COCO_LABELS
                self._intrinsics.update_with_defaults()

                self._picam2 = self._Picamera2(self._imx500.camera_num)
                config = self._picam2.create_preview_configuration(
                    controls={'FrameRate': self.frame_rate},
                    buffer_count=12,
                )

                # Model boot can take several seconds on first load.
                self._imx500.show_network_fw_progress_bar()
                self._picam2.start(config, show_preview=False)

                # Let a few frames settle before reads.
                time.sleep(0.5)
                self._started = True
                return True

            except Exception as e:
                if not self.quiet:
                    print(f'Error starting AI camera: {e}')
                self.stop_camera()
                return False

    def _parse_detections(self, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Convert IMX500 inference output into notebook-friendly detection dicts."""
        np_outputs = self._imx500.get_outputs(metadata, add_batch=True)
        if np_outputs is None or len(np_outputs) < 3:
            return []

        boxes = np_outputs[0]
        scores = np_outputs[1]
        classes = np_outputs[2]

        # Remove batch dimensions if present.
        if hasattr(boxes, 'ndim') and boxes.ndim == 3:
            boxes = boxes[0]
        if hasattr(scores, 'ndim') and scores.ndim == 2:
            scores = scores[0]
        if hasattr(classes, 'ndim') and classes.ndim == 2:
            classes = classes[0]

        if self._intrinsics.bbox_normalization:
            boxes = boxes / self._imx500.get_input_size()[1]

        if getattr(self._intrinsics, 'bbox_order', None) == 'xy':
            boxes = boxes[:, [1, 0, 3, 2]]

        detections: List[Dict[str, Any]] = []
        for box, score, category in zip(boxes, scores, classes):
            confidence = float(score)
            if confidence < self.confidence_threshold:
                continue

            coords = self._imx500.convert_inference_coords(box, metadata, self._picam2)
            if not coords or len(coords) != 4:
                continue

            x, y, w, h = (int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3]))
            category_id = int(category)

            if 0 <= category_id < len(self.COCO_LABELS) and self.COCO_LABELS[category_id]:
                label = self.COCO_LABELS[category_id]
            else:
                label = f'class_{category_id}'

            detections.append({
                'label': label,
                'confidence': confidence,
                'box': [x, y, w, h],
                'category': category_id,
            })

        return detections

    def get_frame_and_detections(self) -> Tuple[Any, List[Dict[str, Any]]]:
        """
        Capture one frame and matching detections.

        Returns:
            (frame, detections)
            - frame: OpenCV-compatible ndarray
            - detections: list of {'label', 'confidence', 'box', 'category'}
        """
        if not self._started or self._picam2 is None or self._imx500 is None:
            raise RuntimeError('AI camera not started. Call start_camera() first.')

        request = self._picam2.capture_request()
        try:
            frame = request.make_array('main')
            metadata = request.get_metadata()
        finally:
            request.release()

        detections = self._parse_detections(metadata)
        return frame, detections

    def stop_camera(self):
        """Stop and release camera resources."""
        with self._lock:
            if self._picam2 is not None:
                try:
                    self._picam2.stop()
                except Exception:
                    pass

            self._picam2 = None
            self._imx500 = None
            self._intrinsics = None
            self._started = False

    def is_running(self) -> bool:
        """Check whether camera system is currently running."""
        return self._started and self._picam2 is not None

def example_usage():
    """Example usage of the student API"""
    print("VESC Student API Example")
    print("=" * 30)
    
    # Create API instance
    api = VESCStudentAPI()
    
    # Start system
    if not api.start():
        print("Failed to start VESC system")
        return
    
    try:
        # Wait for controller discovery
        time.sleep(6.0)
        
        # Get connected controllers
        controllers = api.get_connected_controllers()
        print(f"Connected controllers: {controllers}")
        
        if not controllers:
            print("No controllers found")
            return
        
        # Use first controller
        controller_id = controllers[0]
        controller = api.get_controller(controller_id)
        
        print(f"\\nUsing controller {controller_id}")
        
        # Read telemetry
        print("\\nTelemetry readings:")
        print(f"  RPM: {controller.get_rpm()}")
        print(f"  Current: {controller.get_motor_current()} A")
        print(f"  Duty Cycle: {controller.get_duty_cycle()}")
        print(f"  Input Voltage: {controller.get_input_voltage()} V")
        print(f"  FET Temperature: {controller.get_fet_temperature()} °C")
        
        # Get all telemetry
        print("\\nAll telemetry:")
        all_data = controller.get_all_telemetry()
        for category, data in all_data.items():
            if isinstance(data, dict):
                print(f"  {category}:")
                for key, value in data.items():
                    print(f"    {key}: {value}")
            else:
                print(f"  {category}: {data}")
        
    except KeyboardInterrupt:
        print("\\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        api.stop()


if __name__ == "__main__":
    example_usage()