# Curriculum Master Challenge Answers

This file centralizes challenge/blank answers across all curriculum modules.
Open-ended capstones include reference criteria and starter templates instead of a single fixed answer.

## Module 01 - System Introduction

### E.1 - FET Temp Challenge
- `fet_temp = vesc.get_fet_temperature()`

### E.2 - The PEV Dashboard
- `rpm = vesc.get_rpm()`
- `current = vesc.get_motor_current()`
- `fet_temp = vesc.get_fet_temperature()`

### F.1 - Knowledge Check
- Question 1: `C`
- Question 2: `A`
- Question 3: `B`

## Module 02 - CAN Fundamentals

### 3.2 - Direction Checker
- `if rpm > 0:`
- `elif rpm < 0:`

### 4.2 - Thermal Protection
- `if temp > 50:`

### 5.2 - Dictionary Extraction
- `extracted_rpm = all_data['motor']['rpm']`

### Section 6 - Knowledge Check
- Question 1: `B`
- Question 2: `A`
- Question 3: `C`

## Module 03 - Data Visualization

### 2.x - Update Every 0.5 Seconds (reference)
```python
try:
    for i in range(10):
        clear_output(wait=True)
        voltage = vesc.get_input_voltage()
        print(f'Reading {i+1}/10: Voltage = {voltage:.2f} V')
        time.sleep(0.5)
except NameError:
    print("Connection not established. Please run the connection cell above first.")
```

### 2.x - Add Temperature on Same Line (reference)
```python
try:
    for i in range(10):
        clear_output(wait=True)
        voltage = vesc.get_input_voltage()
        temp = vesc.get_fet_temperature()
        print(f'Reading {i+1}/10: Voltage = {voltage:.2f} V | FET Temp = {temp:.1f} C')
        time.sleep(0.5)
except NameError:
    print("Connection not established. Please run the connection cell above first.")
```

### 3.x - Add Motor Current Panel (reference)
```python
try:
    for i in range(20):
        clear_output(wait=True)

        voltage = vesc.get_input_voltage()
        temp = vesc.get_fet_temperature()
        rpm = vesc.get_rpm()
        current = vesc.get_motor_current()

        temp_color = get_temp_color(temp)

        voltage_str = f'{voltage:.1f}V' if voltage is not None else 'N/A'
        temp_str = f'{temp:.1f}C' if temp is not None else 'N/A'
        rpm_str = f'{int(rpm)}' if rpm is not None else 'N/A'
        current_str = f'{current:.1f}A' if current is not None else 'N/A'

        html_out = f"""
        <div style="border: 2px solid #44B6E5; padding: 10px; font-family: 'Space Grotesk', monospace; background-color: #f0f0f0;">
            <h2 style="margin: 0; padding: 0;">LIVE VEHICLE DASHBOARD</h2>
            <div style="display: flex; justify-content: space-around; font-size: 24px; text-align: center;">
                <p><strong>VOLTAGE:</strong><br>{voltage_str}</p>
                <p style="color: {temp_color};"><strong>TEMP:</strong><br>{temp_str}</p>
                <p><strong>RPM:</strong><br>{rpm_str}</p>
                <p><strong>CURRENT:</strong><br>{current_str}</p>
            </div>
        </div>
        """

        display(HTML(html_out))
        time.sleep(0.5)
except NameError:
    print("Connection not established. Please run the connection cell above first.")
```

### 4.x - Plot RPM and Motor Current (reference)
```python
import matplotlib.pyplot as plt

rpm_data = []
current_data = []
time_data = []
start_time = time.time()

try:
    while time.time() - start_time < 10:
        rpm = vesc.get_rpm()
        current = vesc.get_motor_current()
        if rpm is not None and current is not None:
            rpm_data.append(rpm)
            current_data.append(current)
            time_data.append(time.time() - start_time)
        time.sleep(0.1)

    plt.figure(figsize=(10, 5))
    plt.plot(time_data, rpm_data, label='RPM', color='#44B6E5')
    plt.plot(time_data, current_data, label='Motor Current (A)', color='orange')
    plt.title('RPM and Motor Current over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Value')
    plt.grid(True, linestyle='--')
    plt.legend()
    plt.show()
except NameError:
    print("Connection not established. Please run the connection cell above first.")
```

### Section 5 - Fill in the Blanks (reference)
```python
try:
    voltage = vesc.get_input_voltage()
    temp = vesc.get_fet_temperature()
    rpm = vesc.get_rpm()
    current = vesc.get_motor_current()

    voltage_str = f'{voltage:.1f}V' if voltage is not None else 'N/A'
    temp_str = f'{temp:.1f}C' if temp is not None else 'N/A'
    rpm_str = f'{int(rpm)}' if rpm is not None else 'N/A'
    current_str = f'{current:.1f}A' if current is not None else 'N/A'

    html_out = f"""
    <div style="border: 2px solid #44B6E5; padding: 10px; font-family: 'Space Grotesk', monospace; background-color: #f0f0f0;">
        <h2 style="margin: 0; padding: 0;">LIVE VEHICLE DASHBOARD</h2>
        <div style="display: flex; justify-content: space-around; font-size: 24px; text-align: center;">
            <p><strong>VOLTAGE:</strong><br>{voltage_str}</p>
            <p><strong>TEMP:</strong><br>{temp_str}</p>
            <p><strong>RPM:</strong><br>{rpm_str}</p>
            <p><strong>CURRENT:</strong><br>{current_str}</p>
        </div>
    </div>
    """

    display(HTML(html_out))
except NameError:
    print("Connection not established.")
```

### Section 5 - Short Answer
- A color dashboard makes safety state instantly readable; warning colors are faster to interpret than raw numbers.

## Module 04 - Brake Control

### 2.x - First Brake Sequence (reference)
```python
if vesc:
    ok = vesc.set_brake_current(2.0, 5.0)
    print('Brake command sent:', ok)
```

### 2.2A - Telemetry-Gated Intervention Pseudocode (reference)
```text
READ rpm
READ fet_temp
IF abs(rpm) > 150 AND fet_temp < 70:
    APPLY bounded brake sequence (3.0A, 4.0s)
ELSE:
    PRINT "Gate conditions not met"
```

### 2.2B - Pseudocode to Python (reference)
```python
if vesc:
    rpm = vesc.get_rpm() or 0
    fet_temp = vesc.get_fet_temperature() or 0
    if abs(rpm) > 150 and fet_temp < 70:
        print(f'Applying brake at RPM {rpm:.0f}, FET {fet_temp:.1f}C')
        print('Result:', vesc.set_brake_current(3.0, 4.0))
    else:
        print('Gate conditions not met.')
else:
    print('Connection not established.')
```

### 3.1 - Profile Tuning (reference)
```python
profiles = [(2.0, 6.0), (4.0, 5.0), (6.0, 3.5)]
for current_a, ramp_time_s in profiles:
    print(vesc.set_brake_current(current_a, ramp_time_s))
    time.sleep(1.2)
```

### 3.2 - Cooldown Validation (reference)
```python
if vesc:
    first = vesc.set_brake_current(3.0, 3.0)
    second = vesc.set_brake_current(3.0, 3.0)
    print('first call:', first)
    print('second call:', second)
else:
    print('Connection not established.')
```

### 4.1 - Fill in the Blanks (reference)
```python
if vesc:
    rpm = vesc.get_rpm() or 0

    if abs(rpm) > 120:
        current_a = 3.0
        ramp_time_s = 4.0
        result = vesc.set_brake_current(current_a, ramp_time_s)
        print('Brake result:', result)
    else:
        print('RPM too low for intervention test.')
```

### Section 4 - Short Answer
- Ramp time spreads force application over time, reducing abrupt transients and improving stability.

## Module 05 - CAN Capstone

### Answer Key Status
- Open-ended capstone: no single fixed answer.

### Minimum Completion Checklist
- Option A: monitor voltage/current/Ah, compute `remaining_pct = max(0, 100 * (1 - ah_used / 5.0))`, and implement low-voltage alert behavior.
- Option B: log RPM/current/voltage for 15s, stop motor, compute peak/average metrics, plot RPM.
- Option C: run duty loop, monitor FET temp, warn at warning threshold, throttle at critical threshold.
- All options: include safe `finally` cleanup (API stop plus bounded intervention usage).

## Module 06 - AI Introduction

### 3.x - Filter by Confidence (reference)
```python
CONFIDENCE_THRESHOLD = 0.7

print(f"Detections with confidence > {CONFIDENCE_THRESHOLD}:")
for detection in detections:
    label = detection[0]
    confidence = detection[1]
    if confidence > CONFIDENCE_THRESHOLD:
        print(f'- {label} ({confidence:.2f})')
```

### 3.x - Reusable Filter Function (reference)
```python
def filter_detections(all_detections, threshold):
    filtered_list = []
    for label, confidence in all_detections:
        if confidence > threshold:
            filtered_list.append((label, confidence))
    return filtered_list
```

### 4.x - Bounding Box Width/Height (reference)
```python
x_min = bounding_box[0]
y_min = bounding_box[1]
x_max = bounding_box[2]
y_max = bounding_box[3]

width = x_max - x_min
height = y_max - y_min

print(f"The box is {width} pixels wide and {height} pixels tall.")
```

### 4.x - Bounding Box Area (reference)
```python
area = width * height
print(f"The area is {area} square pixels.")
```

### 5.x - Filter by Label and Confidence (reference)
```python
def filter_by_label_and_confidence(all_detections, target_label, threshold):
    out = []
    for label, confidence in all_detections:
        if label == target_label and confidence > threshold:
            out.append((label, confidence))
    return out
```

### 5.x - Short Answer
- A confidence of 0.65 means the model is moderately sure, not highly certain; treat it as tentative unless corroborated.

## Module 07 - Object Detection

### Runtime Notes (bench audit)
- `AIStudentAPI` now imports and camera startup works.
- Stream display loop import issue resolved: setup cell now imports `clear_output`.

### Section 3 Exercise - Test the Detector (factual bench capture, Feb 23 2026)
- Captured over ~20 seconds on the attached bench camera:
1. `keyboard` (`0.621`)
2. No second unique COCO object observed in this scene
3. No third unique COCO object observed in this scene
4. No fourth unique COCO object observed in this scene
5. No fifth unique COCO object observed in this scene

### Section 4 - Confidence Threshold Filtering (reference)
```python
CONFIDENCE_THRESHOLD = 0.75

try:
    while True:
        frame, detections = api.get_frame_and_detections()

        for detection in detections:
            label = detection['label']
            confidence = detection['confidence']
            box = detection['box']

            if confidence > CONFIDENCE_THRESHOLD:
                x, y, w, h = box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (4, 23, 115), 2)
                text = f'{label}: {confidence:.2f}'
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (4, 23, 115), 2)

        _, img_encoded = cv2.imencode('.jpeg', frame)
        display(Image(data=img_encoded.tobytes()))
        clear_output(wait=True)
except KeyboardInterrupt:
    print("Stream stopped.")
```

### Section 4 - Person-only Filtering (reference)
```python
CONFIDENCE_THRESHOLD = 0.75
TARGET_LABEL = 'person'

try:
    while True:
        frame, detections = api.get_frame_and_detections()

        for detection in detections:
            label = detection['label']
            confidence = detection['confidence']
            box = detection['box']

            if confidence > CONFIDENCE_THRESHOLD and label == TARGET_LABEL:
                x, y, w, h = box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (4, 23, 115), 2)
                text = f'{label}: {confidence:.2f}'
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (4, 23, 115), 2)

        _, img_encoded = cv2.imencode('.jpeg', frame)
        display(Image(data=img_encoded.tobytes()))
        clear_output(wait=True)
except KeyboardInterrupt:
    print("Stream stopped.")
```

### Section 5 - Short Answers
- Three factors: poor lighting, occlusion/extreme angle, and motion blur/small object scale.
- Water bottle can fail due confidence threshold, scene conditions, or model limitations in the current frame.

## Module 08 - AI Hardware Integration

### Runtime Notes (bench audit)
- Buzzer initialization/tests run successfully.
- Camera + buzzer integration loops run successfully with finite-loop validation.

### Section 2 - Beep Three Times (reference)
```python
for i in range(3):
    buzzer.on()
    time.sleep(0.2)
    buzzer.off()
    time.sleep(0.2)
```

### Section 2 - SOS Pattern (reference)
```python
# ... --- ...
for _ in range(3):
    buzzer.on(); time.sleep(0.2); buzzer.off(); time.sleep(0.2)
for _ in range(3):
    buzzer.on(); time.sleep(0.6); buzzer.off(); time.sleep(0.2)
for _ in range(3):
    buzzer.on(); time.sleep(0.2); buzzer.off(); time.sleep(0.2)
```

### Section 3 - Cooldown Loop (reference)
```python
last_beep_time = 0
COOLDOWN_SECONDS = 5

try:
    while True:
        _, detections = api.get_frame_and_detections()

        for det in detections:
            if det['label'] == 'person' and det['confidence'] > 0.75:
                if time.time() - last_beep_time > COOLDOWN_SECONDS:
                    buzzer.beep(on_time=0.1, off_time=0.1, n=2)
                    last_beep_time = time.time()

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStream stopped.")
```

### Section 4 - Custom Pattern Loop (reference)
```python
last_beep_time = 0
COOLDOWN_SECONDS = 5

try:
    while True:
        _, detections = api.get_frame_and_detections()

        if time.time() - last_beep_time > COOLDOWN_SECONDS:
            for det in detections:
                label = det['label']
                conf = det['confidence']

                if label in BEEP_PATTERNS and conf > 0.7:
                    on_t, off_t, n = BEEP_PATTERNS[label]
                    buzzer.beep(on_time=on_t, off_time=off_t, n=n)
                    last_beep_time = time.time()
                    break

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStream stopped.")
```

### Section 5 - Full Detection + Audio Loop (reference)
```python
last_beep_time = 0
COOLDOWN_SECONDS = 5

try:
    while True:
        frame, detections = api.get_frame_and_detections()

        if time.time() - last_beep_time > COOLDOWN_SECONDS:
            for det in detections:
                label = det['label']
                conf = det['confidence']
                box = det['box']

                if label in BEEP_PATTERNS and conf > 0.7:
                    pattern = BEEP_PATTERNS[label]
                    buzzer.beep(on_time=pattern[0], off_time=pattern[1], n=pattern[2])
                    last_beep_time = time.time()

                x, y, w, h = box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (4, 23, 115), 2)
                cv2.putText(frame, f"{label}: {conf:.2f}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (4, 23, 115), 2)

        _, img_encoded = cv2.imencode('.jpeg', frame)
        display(Image(data=img_encoded.tobytes()))
        clear_output(wait=True)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Stream stopped.")
```

### Section 5 - Short Answer
- Cooldown prevents repeated per-frame alerts so operators get actionable notifications instead of constant noise.

## Module 09 - System Integration

### Runtime Notes (bench audit)
- Notebook JSON is now valid and loads.
- VESC CAN service starts; in this bench run no controllers were discovered (`controllers []`).
- Combined AI/VESC logic executes with `vesc=None` fallback.
- Combined loop import issue resolved: initialization cell now imports `clear_output`.

### Section 2 - Combined Data Loop (reference)
```python
from IPython.display import clear_output

start_time = time.time()
try:
    while time.time() - start_time < 10:
        rpm = vesc.get_rpm() if vesc else None
        _, detections = ai_api.get_frame_and_detections()

        print(f'RPM: {rpm if rpm is not None else "N/A"}, Detections: {len(detections)}')
        time.sleep(0.2)
        clear_output(wait=True)

except KeyboardInterrupt:
    print("Loop stopped.")
```

### Section 3 - Add Third Condition (reference)
```python
SPEED_THRESHOLD = 500
CONFIDENCE_THRESHOLD = 0.75
TARGET_LABEL = 'person'
MIN_VOLTAGE = 20.0

last_alert_time = 0
COOLDOWN = 5

while True:
    rpm = vesc.get_rpm() if vesc else 0
    voltage = vesc.get_input_voltage() if vesc else 0
    _, detections = ai_api.get_frame_and_detections()

    is_person_detected = any(
        det['label'] == TARGET_LABEL and det['confidence'] > CONFIDENCE_THRESHOLD
        for det in detections
    )

    if is_person_detected and rpm > SPEED_THRESHOLD and voltage is not None and voltage > MIN_VOLTAGE:
        if time.time() - last_alert_time > COOLDOWN:
            print(f"ALERT! Person detected at {rpm} RPM, voltage {voltage:.1f}V")
            buzzer.beep(0.1, 0.1, 3)
            last_alert_time = time.time()
```

### Section 3 - Three Safety Levels (reference)
```python
if is_person_detected and voltage is not None and voltage > MIN_VOLTAGE:
    if 500 <= rpm <= 1500:
        print(f"CAUTION: person detected, RPM={rpm}")
    elif 1501 <= rpm <= 3000:
        print(f"WARNING: person detected, RPM={rpm}")
        buzzer.beep(0.1, 0.1, 1)
    elif rpm > 3000:
        print(f"DANGER: person detected, RPM={rpm}")
        buzzer.beep(0.1, 0.1, 3)
```

### Section 4 - Short Answers
- Sensor fusion combines multiple sensor streams to make better decisions than either stream alone.
- Example improvement: incorporate motion direction/object distance so alerts trigger only for true closing-risk cases.

## Module 10 - AI Capstone

### Answer Key Status
- Open-ended capstone: no single fixed answer.

### Minimum Completion Checklist
- Uses both AI detections and VESC telemetry inside one decision loop.
- Implements one option fully (A/B/C) with measurable outputs.
- Handles disconnect/None edge cases.
- Uses `finally` for safe cleanup (stop motor/AI/buzzer/API).

## Module 11 - ADAS Introduction

### Categorize Features
- FCW: Warning
- AEB: Intervention
- LDW: Warning
- LKA: Intervention
- ACC: Intervention

### Classify Real Systems
- Car with only ACC: Level 1
- Tesla Autopilot (supervised hands-on): Level 2
- Waymo geofenced robotaxi: Level 4
- Module 9 skateboard project: Level 0

### Sensor Strength / Weakness Examples
- Camera: rich semantic detail / weak in poor lighting-weather
- Radar: robust range/velocity / lower classification detail
- Lidar: high-accuracy 3D geometry / higher cost and integration complexity

### Research Question (reference)
- Vision-only reduces hardware cost and system complexity, while lidar+radar stacks prioritize perception redundancy and edge-case robustness.

### Mapping Exercise
- AI Camera: Vision Sensor
- VESC RPM: Motion/Speed Sensor
- Raspberry Pi: Decision Engine
- Buzzer: Alert System

## Module 12 - ADAS Theory

### 2.x - Distance Estimation (reference)
```python
def estimate_distance(box_height_px):
    if box_height_px < 1:
        return float('inf')
    distance = (CALIBRATION_BOX_HEIGHT_PX / box_height_px) * CALIBRATION_DISTANCE_M
    return distance
```

### 3.x - Speed m/s from RPM (reference)
```python
def get_speed_mps(rpm):
    revolutions_per_second = rpm / 60.0
    wheel_rps = revolutions_per_second / GEAR_RATIO
    speed_mps = wheel_rps * WHEEL_CIRCUMFERENCE_M
    return speed_mps
```

### 3.x - TTC Calculation (reference)
```python
def calculate_ttc(distance_m, speed_mps):
    if speed_mps < 0.1:
        return float('inf')
    ttc = distance_m / speed_mps
    return ttc
```

### 4.x - Alert Status Thresholds (reference)
```python
def get_alert_status(ttc):
    if ttc < 1.0:
        return 'CRITICAL'
    elif ttc <= 3.0:
        return 'WARNING'
    return 'SAFE'
```

### 4.x - TTC to Brake Mapping (reference)
```python
def ttc_to_brake_time(ttc_s):
    if ttc_s <= 1.0:
        out = 3.0
    elif ttc_s < 5.0:
        out = 3.0 + (ttc_s - 1.0) * 1.75
    else:
        out = 10.0
    return max(3.0, min(10.0, out))

def ttc_to_brake_current(ttc_s):
    if ttc_s <= 1.0:
        out = 10.0
    elif ttc_s < 5.0:
        out = 10.0 - (ttc_s - 1.0) * 2.0
    else:
        out = 2.0
    return max(2.0, min(10.0, out))
```

### Section 5 - Short Answers
- False positive: warning without real risk; causes nuisance and trust erosion.
- False negative: no warning during real risk; directly safety-critical.

## Module 13 - ADAS Implementation

### Runtime Notes (bench audit)
- FCW pipeline executes end-to-end with current code structure.
- In this run, no VESC controller was discovered, so status remained SAFE.

### Section 4 - System Validation (factual bench observations, Feb 23 2026)
1. Baseline (no person): `SAFE`, TTC reported as infinite, no buzzer trigger.
2. Stationary person test: not fully completed in this run (no confirmed person detection + no VESC controller).
3. Dynamic person+motion test: not completed because no VESC controller was discovered on CAN.

### Section 5 - Three Improvements (reference)
1. Add temporal smoothing/tracking for distance and TTC to reduce jitter.
2. Prioritize the most threatening object with closing-rate logic.
3. Add sensor-health fallbacks and explicit stale-data handling.

### Section 5 - What's Next? (reference)
- Next step is bounded automatic intervention (AEB-like behavior), using `set_brake_current()` with strict timing/safety limits.

## Module 14 - ADAS Capstone

### Answer Key Status
- Open-ended capstone: no single fixed answer.

### Minimum Completion Checklist
- Implements one option with both AI and VESC data.
- Includes a clear threat/risk model and multilevel response.
- Handles edge cases and noisy detections.
- Includes real-time status output and complete cleanup in `finally`.
