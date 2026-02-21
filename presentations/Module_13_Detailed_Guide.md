# MODULE 13
Building a Forward Collision Warning System
A Practical ADAS Implementation
Lectec PEV AI Curriculum
Day 13 of 14

## STYLE MANIFESTO: BLUEPRINT FUTURISM
- **Color Palette:** STRICT White background, Solid Black text, Electric Blue (#44B6E5) accents.
- **Typography:** Space Grotesk (Display sizes for headers).
- **Imagery:** 3D Isometric Technical Renders. Monochromatic clay-render style with #44B6E5 "energy glows" on highlights.
- **Background:** Faint, thin-line isometric white grid.

---

## TEACHER'S GUIDE: MODULE 13 OVERVIEW

**Module Goal:** To guide students through the process of integrating all previously learned concepts (CAN data, AI detection, GPIO alerts, ADAS theory) into a single, functional Forward Collision Warning (FCW) system. This is the implementation phase of the ADAS module.

**Lesson Structure:**
- **(5 min) Introduction:** Start with the goal: "Today, we build the complete system." Show a live demo of the final FCW system in action, emphasizing the multi-level alerts.
- **(10 min) Lecture:** Briefly walk through the system architecture and integration challenges slides. This recap solidifies the plan before they dive into code.
- **(25 min) Workshop:** This is the most code-heavy day. Students work through the `Student_Notebook_13.ipynb`, integrating the functions they built in Module 12 into a complete, real-time loop.
- **(5 min) Testing & Wrap-up:** Guide students through the safe testing protocol and discuss the results.

---

## SLIDE 1: Title Slide
**Visual Design**
- A large, isometric blueprint of the complete FCW system logic, showing data flowing from sensors to a final "ALERT" output.
- The entire flowchart glows with a subtle Electric Blue (#44B6E5) light.
- Faint isometric grid background.

**Text Content**
- **DISPLAY HEADER:** MODULE 13: ADAS IMPLEMENTATION
- **SUBTEXT:** Building a Forward Collision Warning System
- **BOTTOM FOOTER:** Lectec PEV AI Curriculum | Day 13 of 14

---

## SLIDE 2: TODAY'S GOAL
**Visual Design**
- A 3D isometric scene depicting the full system in action.
- The Lectec skateboard is moving towards a person-shaped figure.
- A holographic overlay shows the AI's "thinking": a bounding box, a distance estimation ("Est. 3m"), the vehicle's speed ("15 km/h"), and the final calculation: "TTC: 0.7s - CRITICAL ALERT".
- The "CRITICAL ALERT" text is rendered in a flashing Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** THE COMPLETE SYSTEM
- **BODY:**
  - Today, you will combine everything.
  - You will build a real ADAS feature that detects objects, estimates distance, reads your speed, calculates Time-to-Collision, and issues multi-level alerts.
- **CALLOUT:** "In 40 minutes, you will have built a functional Forward Collision Warning system."

---

## SLIDE 3: Review: The Components
**Visual Design**
- A grid of five monochromatic icons, representing the system components.
- 1. AI Camera (Detection)
- 2. Ruler/Caliper (Distance Estimation)
- 3. Speedometer (Speed Sensing)
- 4. Calculator (TTC Algorithm)
- 5. Speaker/Buzzer (Alerting)

**Text Content**
- **DISPLAY HEADER:** THE BUILDING BLOCKS
- **BODY:**
  - We have already built every piece of this system. Today, we assemble them.
  - **Detection + Distance + Speed + TTC Logic + Alerts**

---

## SLIDE 4: System Architecture
**Visual Design**
- The complete, detailed system flowchart from the previous lesson, now shown as a polished blueprint.
- Each stage is clearly labeled, and the flow of data is visualized with Electric Blue (#44B6E5) arrows.
- **(AI Camera) -> Detections -> [Filter for 'Person'] -> Bounding Box -> Distance Est. -> (TTC CALC) <- Speed <- (VESC)**
- **(TTC CALC) -> TTC Value -> [Alert Logic] -> Beep Pattern -> (Buzzer)**

**Text Content**
- **DISPLAY HEADER:** THE DATA PIPELINE
- **BODY:**
  - This is the complete flow of data and logic for our FCW system.
  - Our main Python script will execute this pipeline on a continuous loop.
- **JUPYTER TRANSITION:** Section 2 - Component Integration.

---

## SLIDE 5: Integration Challenges
**Visual Design**
- Three icons representing challenges.
- 1. A clock with multiple, unsynced hands (Timing).
- 2. A "NULL" or "None" text symbol (Missing Data).
- 3. A CPU icon with a loading bar (Performance).

**Text Content**
- **DISPLAY HEADER:** ENGINEERING CHALLENGES
- **BODY:**
  - **Timing:** The camera and VESC provide data at different rates.
  - **Data Freshness:** We must handle cases where a sensor temporarily fails to provide a reading (`None`).
  - **Performance:** Running all this code in a real-time loop requires efficiency.

---

## SLIDE 6: Alert Escalation
**Visual Design**
- A visual representation of the TTC thresholds.
- A timeline shows a car approaching an obstacle.
- **TTC > 3s:** A green "SAFE" zone.
- **1s < TTC < 3s:** A yellow "WARNING" zone with a single beep icon.
- **TTC < 1s:** A red "CRITICAL" zone with three loud beep icons.

**Text Content**
- **DISPLAY HEADER:** RESPONSE LEVELS
- **BODY:**
  - Our system will have three distinct alert levels based on the calculated TTC.
  - This ensures the alert is proportional to the danger, reducing unnecessary noise.

---

## SLIDE 7: Visual Feedback
**Visual Design**
- A 3D isometric render of the Jupyter notebook output, showing a clean, text-based dashboard.
- The dashboard displays all the critical FCW values in real-time.
- `STATUS: WARNING | TTC: 2.1s | DIST: 5.2m | SPEED: 10km/h`
- The "STATUS" text changes color (Green/Yellow/Red) based on the alert level.

**Text Content**
- **DISPLAY HEADER:** THE FCW DASHBOARD
- **BODY:**
  - To debug and validate our system, we need to see what it's thinking.
  - We will build a live dashboard that shows the status and all key variables in our loop.

---

## SLIDE 8: Audio Feedback
**Visual Design**
- A simple table mapping alert levels to beep patterns.
- **SAFE:** No icon.
- **WARNING:** A single musical note icon in Electric Blue (#44B6E5).
- **CRITICAL:** Three rapid musical note icons in Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** AUDITORY ALERTS
- **BODY:**
  - The buzzer will provide immediate, unmistakable feedback.
  - We will create a different beep pattern for each alert level.
- **JUPYTER TRANSITION:** Section 3 - Complete FCW System.

---

## SLIDE 9: Edge Cases
**Visual Design**
- Three small scenarios illustrated with simple icons.
- 1. An empty road (No Detections).
- 2. A skateboard at rest (Stationary).
- 3. A person detected extremely close but the board is moving slowly (Very Close / Low Speed).

**Text Content**
- **DISPLAY HEADER:** HANDLING THE UNEXPECTED
- **BODY:**
  - A robust system must handle edge cases gracefully.
  - What should happen if...
    - ...no objects are detected? (System should be silent).
    - ...the vehicle is not moving? (System should be silent).
    - ...TTC is near zero? (Trigger a maximum-level alert).

---

## SLIDE 10: Testing Protocol
**Visual Design**
- A simple checklist with three items, rendered in the blueprint style.
- 1. Secure the vehicle on a test stand.
- 2. Test with a stationary object at a known distance.
- 3. Test with a moving object (e.g., a person walking towards the camera).

**Text Content**
- **DISPLAY HEADER:** SAFE VALIDATION
- **BODY:**
  - **CRITICAL:** All testing must be done on a secure bench with the wheels off the ground.
  - We will follow a safe, structured protocol to validate that our system works as expected.
- **JUPYTER TRANSITION:** Section 4 - Testing.

---

## SLIDE 11: Real FCW Comparison
**Visual Design**
- A side-by-side comparison.
- **Left:** A screenshot of a professional car review showing the FCW settings on a car's infotainment screen (e.g., "Early, Medium, Late").
- **Right:** Our Jupyter notebook code showing the TTC threshold variables.

**Text Content**
- **DISPLAY HEADER:** JUST LIKE THE PROS
- **BODY:**
  - The thresholds you are setting in your code are the same settings a driver can configure in a real car.
  - You are engineering a real ADAS feature.

---

## SLIDE 12: Your Turn
**Visual Design**
- A final, heroic isometric shot of the complete Lectec system.
- The camera, VESC, and Raspberry Pi are all interconnected with glowing Electric Blue (#44B6E5) data lines, forming a complete, intelligent system.

**Text Content**
- **DISPLAY HEADER:** BUILD YOUR FCW
- **BODY:**
  - Assemble the components from the previous lessons.
  - Build your complete Forward Collision Warning system.
- **MISSION:** Section 5 - Knowledge Check.
