# MODULE 9
System Integration
AI Meets Motor Control
Lectec PEV AI Curriculum
Day 9 of 14

## STYLE MANIFESTO: BLUEPRINT FUTURISM
- **Color Palette:** STRICT White background, Solid Black text, Electric Blue (#44B6E5) accents.
- **Typography:** Space Grotesk (Display sizes for headers).
- **Imagery:** 3D Isometric Technical Renders. Monochromatic clay-render style with #44B6E5 "energy glows" on highlights.
- **Background:** Faint, thin-line isometric white grid.

---

## SLIDE 1: Title Slide
**Visual Design**
- A central, glowing Electric Blue (#44B6E5) "plus" symbol.
- On the left, a monochromatic icon representing the CAN bus (a network diagram).
- On the right, a monochromatic icon representing AI vision (a camera with a neural network inside).
- Faint isometric grid background.

**Text Content**
- **DISPLAY HEADER:** MODULE 9: SYSTEM INTEGRATION
- **SUBTEXT:** Creating a Truly Smart System
- **BOTTOM FOOTER:** Lectec PEV AI Curriculum | Day 9 of 14

---

## SLIDE 2: TODAY'S GOAL
**Visual Design**
- An isometric animation concept.
- **Scene 1:** AI camera detects a person, but the skateboard is stationary (RPM=0). No alert and bounded brake intervention is shown.
- **Scene 2:** The skateboard is moving fast (RPM=3000), but no person is detected. No alert and bounded brake intervention is shown.
- **Scene 3:** The skateboard is moving fast AND the camera detects a person. A large, Electric Blue (#44B6E5) "ALERT!" text appears.

**Text Content**
- **DISPLAY HEADER:** THE SMART SAFETY MONITOR
- **BODY:**
  - Today, you will build a system that understands context.
  - It will only trigger an alert and bounded brake intervention when a potential hazard is detected **AND** the vehicle is in motion.
- **CALLOUT:** "In 40 minutes, you will build a system that makes intelligent decisions."

---

## SLIDE 3: Review: What We Have
**Visual Design**
- A two-column layout.
- **Left Column:** A 3D render of the VESC, labeled "CAN SYSTEM" with a sub-label "Knows: HOW FAST".
- **Right Column:** A 3D render of the AI Camera, labeled "AI SYSTEM" with a sub-label "Knows: WHAT is there".

**Text Content**
- **DISPLAY HEADER:** TWO DATA STREAMS
- **BODY:**
  - We have mastered two independent systems:
    - **CAN Bus:** Provides precise, high-speed motor and power data.
    - **AI Vision:** Provides rich, contextual data about the environment.

---

## SLIDE 4: Why Combine?
**Visual Design**
- A simple illustration showing a person standing in front of a parked car. The scene is labeled "SAFE".
- Another illustration shows a person walking in front of a moving car. The scene is labeled "DANGEROUS".
- The "DANGEROUS" label is highlighted in Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** CONTEXT IS EVERYTHING
- **BODY:**
  - Neither data stream alone can tell the whole story.
  - A person detected nearby is not a threat if the vehicle is parked.
  - A moving vehicle is not a threat if the path is clear.
  - **Danger = Hazard + Motion**

---

## SLIDE 5: Sensor Fusion
**Visual Design**
- A diagram showing two data streams (one from a camera, one from a motor) flowing into a central "Logic Core" block.
- From the Logic Core, a single, refined "Decision" stream flows out.
- The Logic Core block is glowing Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** SENSOR FUSION
- **BODY:**
  - This is the engineering term for combining data from multiple sensors to make a better decision than any single sensor could alone.
  - It's the fundamental principle behind all modern autonomous systems.

---

## SLIDE 6: How Cars Do It
**Visual Design**
- An isometric cutaway of a modern car (like a Tesla).
- It shows multiple sensor inputs: Cameras (vision), Radar (radio waves), and Lidar (lasers).
- All sensor data streams are shown converging on a central computer labeled "FUSION ENGINE".

**Text Content**
- **DISPLAY HEADER:** AUTOMOTIVE-GRADE FUSION
- **BODY:**
  - Real self-driving systems fuse data from many sensors:
    - **CAMERAS:** To see *what* an object is.
    - **RADAR:** To see *how fast* it's moving.
    - **LIDAR:** To see its exact *shape and distance*.
  - We are doing the same thing, but with a camera and telemetry-driven control logic.

---

## SLIDE 7: Integration Architecture
**Visual Design**
- A Python-centric flowchart.
- **Block 1:** `vesc_api = VESCStudentAPI()`
- **Block 2:** `ai_api = AIStudentAPI()`
- Both point to a central `while True:` loop block.
- Inside the loop: `rpm = vesc.get_rpm()`, `detections = ai.get_detections()`
- These point to the final `if rpm > 1000 and 'person' in detections:` logic block.

**Text Content**
- **DISPLAY HEADER:** THE COMBINED SCRIPT
- **BODY:**
  - Our code will now have two API objects.
  - Inside our main loop, we will query both systems.
  - The core of our program will be a multi-condition `if` statement.
- **JUPYTER TRANSITION:** Section 2 - Combining Data.

---

## SLIDE 8: Conditional Logic
**Visual Design**
- A simple, bold representation of the core `if` statement.
- `IF ( 'person' is detected ) AND ( rpm > 1000 ):`
- The `AND` is rendered in a large, Electric Blue (#44B6E5) font.

**Text Content**
- **DISPLAY HEADER:** THE `AND` OPERATOR
- **BODY:**
  - This is the key to our system.
  - The `and` keyword in Python ensures that the code inside the `if` block *only* runs when **both** conditions are true.
- **JUPYTER TRANSITION:** Section 3 - Conditional Safety Logic.

---

## SLIDE 9: Safety Levels
**Visual Design**
- A three-level pyramid.
- **Base (Widest):** "Level 1: Monitor" (Low Speed)
- **Middle:** "Level 2: Warning" (Medium Speed)
- **Top (Narrowest):** "Level 3: Critical Alert" (High Speed)
- The "Level 3" block has an Electric Blue (#44B6E5) glow.

**Text Content**
- **DISPLAY HEADER:** ESCALATING RESPONSE
- **BODY:**
  - A single alert and bounded brake intervention isn't enough. The response should match the risk level.
  - **LOW SPEED + PERSON:** A quiet visual alert and bounded brake intervention on a dashboard.
  - **HIGH SPEED + PERSON:** A loud, insistent audio alarm.

---

## SLIDE 10: Data Freshness
**Visual Design**
- A timeline graphic.
- At T=0, the camera detects a person.
- At T=1, the motor RPM is read.
- The graphic shows that by the time the RPM is read, the person may have moved. A "stale data" icon (a clock with an X) is shown next to the T=0 detection.

**Text Content**
- **DISPLAY HEADER:** TIMING CHALLENGES
- **BODY:**
  - Our two systems run at different speeds.
  - It's possible to get a detection from a fraction of a second before you get the RPM reading.
  - For our system, this is okay. For a real car at 70 mph, this is a major engineering challenge.

---

## SLIDE 11: Real Car Comparison
**Visual Design**
- A diagram of a car's AEB (Automatic Emergency Braking) system.
- It shows the system detecting a pedestrian and automatically applying the brakes.
- The logic is shown as: `IF (pedestrian) AND (speed > 20mph) AND (driver_not_braking) THEN apply_brakes()`.

**Text Content**
- **DISPLAY HEADER:** AUTOMATIC EMERGENCY BRAKING
- **BODY:**
  - The logic you are building is the core of a real AEB system.
  - Cars use the exact same multi-condition checks before taking control from the driver.

---

## SLIDE 12: Your Turn
**Visual Design**
- A final isometric render of the full skateboard system.
- Both the CAN bus wires and the AI Camera lens are glowing in Electric Blue (#44B6E5), with their glow merging at the Raspberry Pi.

**Text Content**
- **DISPLAY HEADER:** BUILD YOUR SMART MONITOR
- **BODY:**
  - Complete the exercises in your notebook.
  - You will initialize both APIs and create a true sensor fusion system.
- **MISSION:** Section 5 - Knowledge Check.
