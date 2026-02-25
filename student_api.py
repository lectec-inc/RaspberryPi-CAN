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
    """High-level student API for IMX500 AI camera object detection."""

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

    _shared_buzzer = None
    _shared_buzzer_pin = None
    _shared_buzzer_lock = threading.Lock()
    _buzzer_pin = 17

    _shared_camera_started = False
    _shared_imx500 = None
    _shared_intrinsics = None
    _shared_picam2 = None
    _shared_camera_lock = threading.RLock()
    _atexit_registered = False

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
        self._lock = threading.RLock()

        # Lazy-loaded runtime objects
        self._np = None
        self._Picamera2 = None
        self._IMX500 = None
        self._NetworkIntrinsics = None

        self._imx500 = None
        self._intrinsics = None
        self._picam2 = None

        cls = type(self)
        with cls._shared_camera_lock:
            if not cls._atexit_registered:
                import atexit

                atexit.register(cls._atexit_cleanup)
                cls._atexit_registered = True

    @classmethod
    def _atexit_cleanup(cls):
        """Best-effort release for camera and buzzer on kernel exit."""
        try:
            with cls._shared_camera_lock:
                if cls._shared_picam2 is not None:
                    try:
                        cls._shared_picam2.stop()
                    except Exception:
                        pass
                cls._shared_picam2 = None
                cls._shared_imx500 = None
                cls._shared_intrinsics = None
                cls._shared_camera_started = False

            with cls._shared_buzzer_lock:
                if cls._shared_buzzer is not None:
                    try:
                        cls._shared_buzzer.off()
                    except Exception:
                        pass
                    cls._shared_buzzer.close()
                cls._shared_buzzer = None
                cls._shared_buzzer_pin = None
        except Exception:
            pass

    def _load_buzzer_class(self):
        """Import gpiozero lazily so non-GPIO lessons do not require it at import time."""
        from gpiozero import Buzzer

        return Buzzer

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

    def _clear_local_camera_refs(self):
        self._picam2 = None
        self._imx500 = None
        self._intrinsics = None
        self._started = False

    def _attach_shared_camera_refs(self):
        cls = type(self)
        self._picam2 = cls._shared_picam2
        self._imx500 = cls._shared_imx500
        self._intrinsics = cls._shared_intrinsics
        self._started = cls._shared_camera_started and cls._shared_picam2 is not None

    def _is_camera_busy_error(self, err: Exception) -> bool:
        msg = str(err).lower()
        return (
            'device or resource busy' in msg
            or 'resource busy' in msg
            or '[errno 16]' in msg
            or 'already in use' in msg
            or 'pipeline handler in use' in msg
            or 'in use by another process' in msg
        )

    def _read_cmdline(self, pid: int) -> str:
        try:
            with open(f'/proc/{pid}/cmdline', 'rb') as f:
                return f.read().decode(errors='ignore').replace('\x00', ' ').strip()
        except Exception:
            return ''

    def _terminate_pid(self, pid: int, sig: int):
        import os

        try:
            os.kill(pid, sig)
        except ProcessLookupError:
            return
        except PermissionError:
            return
        except Exception:
            return

    def _reclaim_camera_from_other_kernels(self) -> bool:
        """Release camera from other ipykernel processes to keep notebooks resilient."""
        import os
        import re
        import signal
        import subprocess

        camera_nodes = ['/dev/video0', '/dev/video1', '/dev/media0', '/dev/media3']
        pids = set()
        for node in camera_nodes:
            result = subprocess.run(
                ['fuser', node],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.stdout:
                for match in re.findall(r'\d+', result.stdout):
                    pids.add(int(match))

        current_pid = os.getpid()
        victims = []
        for pid in sorted(pids):
            if pid == current_pid:
                continue
            cmdline = self._read_cmdline(pid)
            if 'ipykernel_launcher' in cmdline:
                victims.append(pid)

        if not victims:
            return False

        if not self.quiet:
            print(f'Camera busy, reclaiming from stale kernels: {victims}')

        for pid in victims:
            self._terminate_pid(pid, signal.SIGTERM)

        deadline = time.time() + 4.0
        while time.time() < deadline:
            remaining = [pid for pid in victims if os.path.exists(f'/proc/{pid}')]
            if not remaining:
                break
            time.sleep(0.2)

        remaining = [pid for pid in victims if os.path.exists(f'/proc/{pid}')]
        for pid in remaining:
            self._terminate_pid(pid, signal.SIGKILL)

        time.sleep(0.6)
        return True

    def start_camera(self, reclaim_if_busy: bool = True) -> bool:
        """Start the AI camera and detection model."""
        cls = type(self)

        # Reuse shared camera in-process if it is already active.
        with cls._shared_camera_lock:
            if cls._shared_camera_started and cls._shared_picam2 is not None:
                self._attach_shared_camera_refs()
                return True

        for attempt in range(2):
            picam2 = None
            try:
                self._lazy_import_camera_stack()

                imx500 = self._IMX500(self.model_path)
                intrinsics = imx500.network_intrinsics or self._NetworkIntrinsics()
                intrinsics.task = 'object detection'
                intrinsics.labels = self.COCO_LABELS
                intrinsics.update_with_defaults()

                picam2 = self._Picamera2(imx500.camera_num)
                config = picam2.create_preview_configuration(
                    controls={'FrameRate': self.frame_rate},
                    buffer_count=12,
                )

                # Model boot can take several seconds on first load.
                imx500.show_network_fw_progress_bar()
                picam2.start(config, show_preview=False)

                # Let a few frames settle before reads.
                time.sleep(0.5)

                with cls._shared_camera_lock:
                    cls._shared_imx500 = imx500
                    cls._shared_intrinsics = intrinsics
                    cls._shared_picam2 = picam2
                    cls._shared_camera_started = True
                    self._attach_shared_camera_refs()
                return True

            except Exception as e:
                if picam2 is not None:
                    try:
                        picam2.stop()
                    except Exception:
                        pass

                self._clear_local_camera_refs()

                if reclaim_if_busy and self._is_camera_busy_error(e) and attempt == 0:
                    if self._reclaim_camera_from_other_kernels():
                        continue

                if not self.quiet:
                    print(f'Error starting AI camera: {e}')
                return False

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
        cls = type(self)
        with cls._shared_camera_lock:
            if (not self._started or self._picam2 is None or self._imx500 is None) and cls._shared_camera_started:
                self._attach_shared_camera_refs()

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
        cls = type(self)
        with cls._shared_camera_lock:
            if cls._shared_picam2 is not None:
                try:
                    cls._shared_picam2.stop()
                except Exception:
                    pass

            cls._shared_picam2 = None
            cls._shared_imx500 = None
            cls._shared_intrinsics = None
            cls._shared_camera_started = False
            self._clear_local_camera_refs()

    def start_buzzer(self) -> bool:
        """
        Initialize (or reuse) the shared buzzer object.

        Buzzer pin is fixed to GPIO17 for the classroom hardware.
        """
        pin = type(self)._buzzer_pin
        cls = type(self)
        with cls._shared_buzzer_lock:
            if cls._shared_buzzer is not None and cls._shared_buzzer_pin == pin:
                return True

            try:
                if cls._shared_buzzer is not None:
                    try:
                        cls._shared_buzzer.off()
                    except Exception:
                        pass
                    cls._shared_buzzer.close()

                buzzer_class = self._load_buzzer_class()
                cls._shared_buzzer = buzzer_class(pin)
                cls._shared_buzzer_pin = pin
                return True
            except Exception as e:
                if not self.quiet:
                    print(f'Error starting buzzer on GPIO{pin}: {e}')
                cls._shared_buzzer = None
                cls._shared_buzzer_pin = None
                return False

    def buzzer_on(self):
        """Turn buzzer on."""
        cls = type(self)
        with cls._shared_buzzer_lock:
            if cls._shared_buzzer is None:
                raise RuntimeError('Buzzer not started. Call start_buzzer() first.')
            cls._shared_buzzer.on()

    def buzzer_off(self):
        """Turn buzzer off."""
        cls = type(self)
        with cls._shared_buzzer_lock:
            if cls._shared_buzzer is None:
                raise RuntimeError('Buzzer not started. Call start_buzzer() first.')
            cls._shared_buzzer.off()

    def buzzer_beep(
        self,
        on_time: float = 0.1,
        off_time: float = 0.1,
        n: int = 1,
        background: bool = False,
    ):
        """Pulse the buzzer with gpiozero's built-in beep helper."""
        cls = type(self)
        with cls._shared_buzzer_lock:
            if cls._shared_buzzer is None:
                raise RuntimeError('Buzzer not started. Call start_buzzer() first.')
            cls._shared_buzzer.beep(
                on_time=on_time,
                off_time=off_time,
                n=n,
                background=background,
            )

    def stop_buzzer(self):
        """Turn off and release the shared buzzer."""
        cls = type(self)
        with cls._shared_buzzer_lock:
            if cls._shared_buzzer is None:
                return
            try:
                cls._shared_buzzer.off()
            except Exception:
                pass
            cls._shared_buzzer.close()
            cls._shared_buzzer = None
            cls._shared_buzzer_pin = None

    def shutdown_hardware(self, stop_camera: bool = True, stop_buzzer: bool = True):
        """Gracefully release AI hardware resources."""
        if stop_camera:
            self.stop_camera()
        if stop_buzzer:
            self.stop_buzzer()

    def is_running(self) -> bool:
        """Check whether camera system is currently running."""
        cls = type(self)
        with cls._shared_camera_lock:
            return cls._shared_camera_started and cls._shared_picam2 is not None


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
