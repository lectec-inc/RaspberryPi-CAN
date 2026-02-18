# Module 2: CAN Fundamentals - Detailed Guide

## 🎯 End Goal
Students will master all 18 data points available from the VESC motor controller, learning how to interpret, categorize, and act on real-time vehicle telemetry.

---

## 📽️ PowerPoint Slide Detailed Guide (12 Slides)

### Slide 1: Complete Vehicle Telemetry Mastery
- **Instructor Action:** Open the lesson with high energy. The PEV isn't just a motor; it's a mobile data station.
- **Key Point:** Every internal thought of the skateboard is shared over one single wire (the CAN bus).

### Slide 2: TODAY'S GOAL
- **Live Demo:** Run the `get_all_telemetry()` cell in the instructor notebook.
- **Instructor Script:** "You're seeing a wall of data. By the end of this hour, you'll be able to read this like a mechanic reads a dashboard."

### Slide 3: Review: Your First Connection
- **Check-in:** Ensure everyone's board is on and the green "Connected" status is visible from Module 1.
- **Recap:** API = Menu, VESC = Chef.

### Slide 4: The 18 Data Points
- **Visual:** Show a 3x6 grid of the values.
- **Categorization:** Group them into Motor, Power, Temperature, and Sensor data.

### Slide 5: Motor Data
- **Definitions:** 
    - **RPM:** Rotations per minute.
    - **Current:** The "push" or torque.
    - **Duty Cycle:** What percentage of the time the motor is actually getting power.

### Slide 6: Understanding Direction
- **Concept:** Positive vs. Negative values.
- **Interaction:** "If the wheel spins forward, RPM is positive. If you roll backward, it's negative. Same for energy!"

### Slide 7: Power Data
- **Definitions:** 
    - **Voltage:** The "pressure" in your battery tank.
    - **Input Current:** Total flow from the battery.

### Slide 8: Temperature Data
- **Safety Focus:** Explain "Thermal Throttling."
- **Thresholds:** MOSFETs (FETs) are the high-power switches. If they get too hot, the VESC limits power to save itself.

### Slide 9: Energy Tracking
- **The Odometer:** Amp-hours (Ah) and Watt-hours (Wh).
- **Regen:** Explain how `watt_hours_charged` increases during braking.

### Slide 10: The Magic Function
- **Python Concept:** The Dictionary (`dict`).
- **Analogy:** `telemetry['motor']['rpm']` is like looking in a filing cabinet labeled 'Motor' for a folder labeled 'RPM'.

### Slide 11: When Data is Zero
- **Troubleshooting:** "My RPM is 0!" -> "Is the wheel moving?" 
- **Learning:** Sensors only report what's happening. No movement = 0 speed.

### Slide 12: Your Turn
- **Transition:** Students open `Student_Notebook_02.ipynb`.

---

## 📓 Jupyter Notebook Structure

### Section 1: Your Mission
- Markdown checklist of all 18 telemetry points to "check off" as they find them.

### Section 2: Motor Data (Logic Challenges)
- **Exercise 1:** Read RPM and Current while hand-spinning.
- **Code Challenge:** Fill in the logic to check direction:
  ```python
  if rpm > 0: print("Rolling Forward")
  elif rpm < 0: print("Rolling Backward")
  else: print("Stationary")
  ```

### Section 3: Power and Temperature (Safety Logic)
- **Exercise 2:** Read Voltage and FET Temp.
- **Calculation:** `power = voltage * input_current`.
- **Safety Challenge:** Create the "Software Thermal Fuse":
  ```python
  if fet_temp > 50: print("⚠️ WARNING: Controller Overheating!")
  ```

### Section 4: Master Function
- **Exercise 3:** Call `get_all_telemetry()`.
- **Extraction Challenge:** Locate and print specific nested values from the dictionary.

### Section 5: Knowledge Check
- Interactive cell with Base64 encoded answers.
- Question: "Why is current negative during braking?" (Energy recovery/Regeneration).
