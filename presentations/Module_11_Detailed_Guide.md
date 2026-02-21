# MODULE 11
Advanced Driver Assistance Systems (ADAS)
Connecting Your Project to the Automotive Industry
Lectec PEV AI Curriculum
Day 11 of 14

## STYLE MANIFESTO: BLUEPRINT FUTURISM
- **Color Palette:** STRICT White background, Solid Black text, Electric Blue (#44B6E5) accents.
- **Typography:** Space Grotesk (Display sizes for headers).
- **Imagery:** 3D Isometric Technical Renders. Monochromatic clay-render style with #44B6E5 "energy glows" on highlights.
- **Background:** Faint, thin-line isometric white grid.

---

## TEACHER'S GUIDE: MODULE 11 OVERVIEW

**Module Goal:** To provide students with a comprehensive understanding of the ADAS landscape in the modern automotive industry. This module is less about coding and more about building context, understanding terminology, and seeing how their skateboard project relates to billion-dollar automotive systems.

**Lesson Structure:**
- **(5 min) Introduction:** Hook the students by showing a video of a modern ADAS system in action (like Tesla's Autopilot or Ford's BlueCruise).
- **(20 min) Lecture:** This is a content-heavy day. Use the 18 slides to walk through the history, features, SAE levels, and sensor technologies of ADAS.
- **(15 min) Workshop:** Students work through the Jupyter notebook, which focuses on research, classification, and comparison exercises.
- **(5 min) Wrap-up & Preview:** Solidify the connection between their skateboard project and real ADAS, and preview the next lesson where they will build the core algorithm for a Forward Collision Warning system.

---

## SLIDE 1: Title Slide
**Visual Design**
- A sleek, futuristic, monochromatic car rendered in the clay style.
- Lines of Electric Blue (#44B6E5) radiate from the car's sensors (windshield camera, corner radars), creating a "sensor bubble" around it.
- Faint isometric grid background.

**Text Content**
- **DISPLAY HEADER:** MODULE 11: ADAS INTRODUCTION
- **SUBTEXT:** From Skateboard to Self-Driving
- **BOTTOM FOOTER:** Lectec PEV AI Curriculum | Day 11 of 14

---

## SLIDE 2: TODAY'S GOAL
**Visual Design**
- A 3D isometric render of the Lectec skateboard.
- A dotted Electric Blue (#44B6E5) line connects it to a full-size, modern electric car.
- The text appears in the center, bridging the two vehicles.

**Text Content**
- **DISPLAY HEADER:** THE BIG PICTURE
- **BODY:**
  - Today, you will understand how the system you've built is a miniature version of the technology in a real car.
  - You will become an expert in the language of the autonomous vehicle industry.

---

## SLIDE 3: What is ADAS?
**Visual Design**
- An icon of a driver with their hands on a steering wheel, looking alert.
- A "shield" icon, glowing in Electric Blue (#44B6E5), is overlaid on the driver, symbolizing assistance and safety.

**Text Content**
- **DISPLAY HEADER:** DRIVER **ASSISTANCE**
- **BODY:**
  - **A**dvanced **D**river **A**ssistance **S**ystems.
  - Key word: **Assistance**. These systems help the driver, they do not replace the driver (at most levels).
  - Their primary goal is to increase safety and reduce driver workload.

---

## SLIDE 4: ADAS Timeline
**Visual Design**
- A horizontal timeline rendered in the blueprint style.
- **1978:** ABS icon.
- **1990s:** Cruise Control icon.
- **2010s:** Lane Keeping icon.
- **Today:** Autopilot/Self-Driving icon.
- The line connecting them is Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** A BRIEF HISTORY
- **BODY:**
  - ADAS is not new. It's been a gradual evolution of safety and convenience features over decades.
  - We are now at an inflection point where these systems are becoming truly "smart".

---

## SLIDE 5: Common ADAS Features
**Visual Design**
- A large grid of clean, monochromatic icons representing 10-15 different ADAS features (FCW, AEB, LKA, ACC, etc.).
- The grid layout is clean and technical.

**Text Content**
- **DISPLAY HEADER:** THE FEATURE SET
- **BODY:**
  - Modern cars have a huge suite of ADAS features. We will cover the most important ones.
- **JUPYTER TRANSITION:** Section 2 - ADAS Features Deep Dive.

---

## SLIDE 6: Forward Collision Warning (FCW)
**Visual Design**
- A simple animation concept. A car is driving. A second car in front of it suddenly brakes.
- A large, red "WARNING" text with a speaker icon appears on the first car's windshield.
- **This entire slide is outlined in Electric Blue (#44B6E5) to signify "We will build this!"**

**Text Content**
- **DISPLAY HEADER:** FORWARD COLLISION WARNING
- **BODY:**
  - **WHAT IT DOES:** Detects a potential collision with an object ahead and alerts the driver.
  - **RESPONSE:** Audio beep, visual warning light.
  - **This is the system you will build in this module.**

---

## SLIDE 7: Automatic Emergency Braking (AEB)
**Visual Design**
- The same scene as the previous slide, but a step later.
- After the "WARNING" appears, the car's brakes are shown engaging automatically (represented by glowing blue brake discs).

**Text Content**
- **DISPLAY HEADER:** AUTOMATIC EMERGENCY BRAKING
- **BODY:**
  - **WHAT IT DOES:** If the driver does not react to an FCW alert, the system automatically applies the brakes to prevent or lessen the impact.
  - **RESPONSE:** Active braking. This is an **intervention** system.

---

## SLIDE 8: Lane Departure Warning (LDW)
**Visual Design**
- A top-down view of a car drifting out of its lane.
- The lane line that is being crossed flashes in Electric Blue (#44B6E5). A subtle steering wheel vibration icon is shown.

**Text Content**
- **DISPLAY HEADER:** LANE DEPARTURE WARNING
- **BODY:**
  - **WHAT IT DOES:** Uses a camera to monitor lane markings and alerts the driver if the vehicle unintentionally drifts.
  - **RESPONSE:** Steering wheel vibration, audio beep.

---

## SLIDE 9: Adaptive Cruise Control (ACC)
**Visual Design**
- A top-down view of two cars. The front car is slowing down.
- The car behind is shown automatically reducing its speed to maintain a safe following distance, which is visualized as a glowing blue bar.

**Text Content**
- **DISPLAY HEADER:** ADAPTIVE CRUISE CONTROL
- **BODY:**
  - **WHAT IT DOES:** An advanced cruise control that uses radar or cameras to maintain a set speed AND a set following distance from the vehicle ahead.
  - **RESPONSE:** Automatic acceleration and braking.

---

## SLIDE 10: Blind Spot Detection
**Visual Design**
- A top-down view of a car. A second car is in its blind spot.
- A warning light icon, glowing Electric Blue (#44B6E5), is shown on the first car's side mirror.

**Text Content**
- **DISPLAY HEADER:** BLIND SPOT DETECTION
- **BODY:**
  - **WHAT IT DOES:** Uses rear-facing sensors (usually radar) to monitor the driver's blind spots and provides a warning if another vehicle is present.
  - **RESPONSE:** Warning light on the side mirror.

---

## SLIDE 11: SAE Autonomy Levels
**Visual Design**
- A large, bold graphic showing a staircase with 6 steps, labeled 0 through 5.
- The steps are rendered in the blueprint style.

**Text Content**
- **DISPLAY HEADER:** THE 6 LEVELS OF AUTONOMY
- **BODY:**
  - The Society of Automotive Engineers (SAE) created a standard scale to classify self-driving capabilities.
  - These levels provide a common language for engineers, regulators, and consumers.
- **JUPYTER TRANSITION:** Section 3 - SAE Autonomy Levels.

---

## SLIDE 12: Levels 0-2
**Visual Design**
- The staircase graphic is shown again, but only steps 0, 1, and 2 are highlighted.
- An icon of a human driver is prominently displayed above these steps, with the text "YOU ARE DRIVING".

**Text Content**
- **DISPLAY HEADER:** LEVEL 0-2: DRIVER SUPPORT
- **BODY:**
  - **LEVEL 0:** No automation.
  - **LEVEL 1:** One feature assists (e.g., ACC).
  - **LEVEL 2:** Two or more features work together (e.g., ACC + Lane Centering).
  - **CRITICAL:** In all these levels, the human is fully responsible for driving.

---

## SLIDE 13: Levels 3-5
**Visual Design**
- The staircase graphic, with steps 3, 4, and 5 highlighted.
- An icon of a computer chip, glowing Electric Blue (#44B6E5), is shown above these steps, with the text "THE CAR IS DRIVING".

**Text Content**
- **DISPLAY HEADER:** LEVEL 3-5: AUTOMATED DRIVING
- **BODY:**
  - **LEVEL 3:** The car can drive itself under specific conditions (e.g., highway), but the driver must be ready to take over.
  - **LEVEL 4:** The car can drive itself fully within a limited area (geofenced).
  - **LEVEL 5:** The car can drive itself anywhere, anytime, under any conditions. (The holy grail; does not exist yet).

---

## SLIDE 14: Where Cars Are Today
**Visual Design**
- A simple bar chart.
- Most production cars today (Tesla, Ford, GM) are shown at Level 2.
- A few, like some Mercedes models in specific regions, are at Level 3.
- Robotaxi services (Waymo) are shown at Level 4.

**Text Content**
- **DISPLAY HEADER:** THE STATE OF THE INDUSTRY
- **BODY:**
  - The vast majority of systems on the road today are **Level 2**.
  - Level 3 is emerging in limited use.
  - Level 4 is restricted to specific geofenced areas (e.g., Waymo in Phoenix).

---

## SLIDE 15: Sensors: Camera
**Visual Design**
- An isometric cutaway of a car's windshield-mounted camera module.
- The camera's cone of vision is shown, and within it, it correctly identifies a stop sign, a pedestrian, and lane lines.

**Text Content**
- **DISPLAY HEADER:** SENSORS: VISION (CAMERA)
- **BODY:**
  - **STRENGTHS:** Excellent at classification (knows a person from a pole), reads signs and traffic lights.
  - **WEAKNESSES:** Poor in bad weather (rain, fog, snow), struggles with direct sunlight/glare, poor at judging precise distance and speed.

---

## SLIDE 16: Sensors: Radar & Lidar
**Visual Design**
- Two icons side-by-side.
- **RADAR:** Emits radio waves (concentric rings).
- **LIDAR:** Emits laser beams (a dense grid of points). The laser beams are Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** SENSORS: RADAR & LIDAR
- **BODY:**
  - **RADAR:** Excellent at measuring distance and speed, works in any weather. Poor at classification.
  - **LIDAR:** Creates a precise 3D point map of the world. Excellent at detecting shape and distance. Very expensive, can be affected by weather.
- **JUPYTER TRANSITION:** Section 4 - Sensor Comparison.

---

## SLIDE 17: Company Comparison
**Visual Design**
- A two-column comparison table.
- **Left (Tesla):** An icon of a camera with the text "Vision Only".
- **Right (Waymo):** Icons for Camera + Radar + Lidar.

**Text Content**
- **DISPLAY HEADER:** TWO PHILOSOPHIES
- **BODY:**
  - **TESLA:** Believes cameras are enough, just like humans use two eyes. This is a "vision-centric" approach.
  - **WAYMO/CRUISE:** Believe in redundancy. Use cameras, radar, and lidar together so that the weakness of one sensor is covered by the strength of another.

---

## SLIDE 18: Your Skateboard = Mini ADAS
**Visual Design**
- A final isometric render of the Lectec skateboard.
- Callout lines point to the components and label them with ADAS terminology.
- **AI Camera:** "VISION SENSOR"
- **VESC RPM data:** "SPEED SENSOR"
- **Raspberry Pi:** "FUSION ENGINE"

**Text Content**
- **DISPLAY HEADER:** YOUR TEST PLATFORM
- **BODY:**
  - The system you have built is a perfect, small-scale ADAS development platform.
  - You have a vision sensor, a speed sensor, and a computer to fuse the data.
  - Now, let's build a real ADAS feature with it.
- **PREVIEW:** Tomorrow, we build a Time-to-Collision calculator.
