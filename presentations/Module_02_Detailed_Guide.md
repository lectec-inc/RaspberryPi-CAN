# MODULE 2
Complete Vehicle Telemetry Mastery
Understanding the 18 Data Points of the VESC
Lectec PEV AI Curriculum
Day 2 of 14

## STYLE MANIFESTO: BLUEPRINT FUTURISM
- **Color Palette:** STRICT White background, Solid Black text, Electric Blue (#44B6E5) accents.
- **Typography:** Space Grotesk (Display sizes for headers).
- **Imagery:** 3D Isometric Technical Renders. Monochromatic clay-render style with #44B6E5 "energy glows" on highlights.
- **Background:** Faint, thin-line isometric white grid.

---

## SLIDE 1: Title Slide
**Visual Design**
- Monochromatic clay render of the full Lectec Skateboard (isometric view).
- Faint isometric grid background.
- Electric Blue (#44B6E5) glow emanating from the VESC enclosure under the deck.

**Text Content**
- **DISPLAY HEADER:** MODULE 2: TELEMETRY MASTERY
- **SUBTEXT:** Decoding the VESC Data Stream
- **BOTTOM FOOTER:** Lectec PEV AI Curriculum | Day 2 of 14

---

## SLIDE 2: TODAY'S GOAL
**Visual Design**
- 3D Isometric technical render of a Jupyter Notebook interface floating in 3D space.
- A technical "callout" line points to a code block displaying the `get_all_telemetry()` function.
- The output of the function is shown in a clean, vertical list with Electric Blue (#44B6E5) text.

**Text Content**
- **DISPLAY HEADER:** THE FULL PICTURE
- **BODY:** 
    - Today, you will build a system that reads all 18 unique data points from your vehicle.
    - Speed, Power, Heat, and Health—all in real-time.
- **CALLOUT:** "In 40 minutes, you will know everything your skateboard knows."

---

## SLIDE 3: Review: Your First Connection
**Visual Design**
- Close-up isometric render of the Raspberry Pi Zero 2W connected to the VESC via CAN wires.
- The two CAN wires (High/Low) are highlighted in Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** RECAP: THE BRAIN LINK
- **BODY:**
    - Established connection to the VESC via the VESCStudentAPI.
    - Verified the system is alive by reading battery voltage.
- **NOTE:** Yesterday was just the handshake. Today is the conversation.

---

## SLIDE 4: The 18 Data Points
**Visual Design**
- A large, 3D isometric VESC controller centered on the slide.
- 18 thin, Electric Blue (#44B6E5) lines radiate out from the controller to a clean list of text labels.
- The labels are categorized into: MOTOR, POWER, TEMPERATURE, and SENSORS.

**Text Content**
- **DISPLAY HEADER:** DATA ARCHITECTURE
- **VERTICAL GRID LIST:**
    - **MOTOR:** RPM, Current, Duty Cycle.
    - **POWER:** Voltage, Input Current, Amp Hours, Watt Hours.
    - **TEMPERATURE:** FET Temperature, Motor Temperature.
    - **SENSORS:** Tachometer, PID Position, ADC Channels.

---

## SLIDE 5: Motor Data: The Essentials
**Visual Design**
- Isometric render of the Brushless DC Outrunner motor.
- The internal copper windings are highlighted with an Electric Blue (#44B6E5) glow.
- An arrow indicates the direction of rotation.

**Text Content**
- **DISPLAY HEADER:** MOTOR TELEMETRY
- **BODY:**
    - **RPM:** How fast the motor is spinning.
    - **MOTOR CURRENT:** The torque/force being applied (Amperes).
    - **DUTY CYCLE:** The "throttle percentage" (0.0 to 1.0).
- **JUPYTER TRANSITION:** Section 3.1 - Reading Basic Motor Telemetry.

---

## SLIDE 6: Understanding Direction
**Visual Design**
- Two identical isometric renders of the skateboard side-by-side.
- Left Skateboard: Forward arrow, label "+ RPM" in Electric Blue (#44B6E5).
- Right Skateboard: Backward arrow, label "- RPM" in Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** THE SIGN OF SPEED
- **BODY:**
    - RPM is not just a number; it's a direction.
    - **POSITIVE (+):** Forward rotation.
    - **NEGATIVE (-):** Reverse/Braking rotation.
- **JUPYTER TRANSITION:** Section 3.2 - Direction Checker Logic.

---

## SLIDE 7: Power Data: Input & Load
**Visual Design**
- Isometric render of the Lithium-Ion Battery Pack.
- The main power leads (XT60 connector) are highlighted in Electric Blue (#44B6E5).
- A transparent "pulse" effect travels from the battery toward the controller.

**Text Content**
- **DISPLAY HEADER:** POWER MONITORING
- **BODY:**
    - **INPUT VOLTAGE:** Your fuel gauge. Higher = more charge.
    - **INPUT CURRENT:** The load on the battery.
- **TECH NOTE:** High input current during a hill climb creates battery sag (voltage drop).
- **JUPYTER TRANSITION:** Section 4.1 - Reading Power Data.

---

## SLIDE 8: Temperature Data: Thermal Safety
**Visual Design**
- Close-up isometric render of the VESC MOSFETs (the small black squares on the PCB).
- These components have a subtle Electric Blue (#44B6E5) glow to indicate they are the primary source of heat.
- A "Digital Thermometer" graphic is displayed next to them.

**Text Content**
- **DISPLAY HEADER:** THERMAL BOUNDARIES
- **BODY:**
    - **FET TEMP:** The heat on the controller's "muscles."
    - **MOTOR TEMP:** Heat inside the motor windings.
- **CRITICAL:** If these values exceed 80°C, the system will automatically throttle power.
- **JUPYTER TRANSITION:** Section 4.2 - Temperature Threshold Warnings.

---

## SLIDE 9: Energy Tracking: Efficiency
**Visual Design**
- 3D Isometric "Bar Graph" rendered in the clay style, showing "Consumed" vs "Charged" energy.
- The "Charged" (Regenerated) bar is highlighted in Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** ENERGY ECONOMY
- **BODY:**
    - **AMP HOURS (Ah):** Total capacity used.
    - **WATT HOURS (Wh):** Total energy used (Ah × Voltage).
- **REGEN:** Notice "Charged" values increase when you use the brakes!

---

## SLIDE 10: The Magic Function
**Visual Design**
- A clean, monochromatic clay-render "terminal window" centered on the slide.
- It displays a snippet of code: `vesc.get_all_telemetry()`
- The text is Solid Black, but the dictionary braces `{ }` are Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** THE MASTER KEY
- **BODY:**
    - Instead of calling 18 functions, we call one.
    - `get_all_telemetry()` returns a Python Dictionary.
    - High-speed, efficient data retrieval.
- **JUPYTER TRANSITION:** Section 5.1 - The Master Function Demonstration.

---

## SLIDE 11: When Data is Zero
**Visual Design**
- Isometric render of the skateboard resting on a bench (Bench Test Stand).
- The wheels are stationary.
- A large Electric Blue (#44B6E5) "0.00" is projected above the motor.

**Text Content**
- **DISPLAY HEADER:** STATIONARY STATE
- **BODY:**
    - If the motor isn't moving, RPM and Current will be 0.
    - Voltage and Temperatures are **always** active.
- **DEBUG TIP:** If your RPM is zero, make sure the motor is plugged in.

---

## SLIDE 12: Your Turn
**Visual Design**
- Final isometric view of the full skateboard system.
- All hardware components (Pi, VESC, Motor, Battery) pulse once in Electric Blue (#44B6E5).
- Large text centered in the white space.

**Text Content**
- **DISPLAY HEADER:** DATA DOMINATION
- **BODY:**
    - Complete the Mastery Checklist in your notebook.
    - Verify every data point for your specific vehicle.
- **MISSION:** Section 6 - Knowledge Check & Summary.
