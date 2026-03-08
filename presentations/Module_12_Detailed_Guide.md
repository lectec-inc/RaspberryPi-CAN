# MODULE 21

Style Manifesto: Professional "Blueprint Futurism" for Lectec STEM Kits. Color Palette: STRICT White background, Solid Black text, and Electric Blue (#44B6E5) for accents. No gradients, no extra colors. Typography: Space Grotesk. Use "Display" sizes for headers (very large). All body text must be aligned to a strict vertical grid. Imagery Requirements:

Subject: 3D Isometric Technical Renders.

Visual Quality: Monochromatic clay-render style with #44B6E5 "energy glows" or highlights on specific components (like a wheel or motor).

Background: A faint, thin-line isometric white grid must be visible across the entire slide.

Execution: High-end architectural visualization style. No "clipart," no photos, and strictly no logos. Slide Composition: > 

Use "Rule of Thirds": Place a large 3D component on one third of the slide, and text on the opposite third. Leave the middle third as empty white space.

Follow these slide contents exactly:

---

## SLIDE 1:
**Visual Design**
- A diagram illustrates the concept of Time to Collision (TTC) between a moving Lectec electric scooter and a stationary person. A dotted line, labeled 'DISTANCE' in text, connects the scooter and the person. The scooter is shown in motion glowing in Electric Blue (#44B6E5), with dotted line leading to a lebel 'SPEED'. The TTC formula (TTC = Distance / Speed) is displayed above the elements.
- Faint isometric grid background.

**Text Content**
- **DISPLAY HEADER:** MODULE 21: ADAS THEORY
- **SUBTEXT:** The Math Behind Safety Systems
---

## SLIDE 2: 
**Visual Design**
- A 3D isometric render of a calculator.
- The inputs are "Distance: 10m" and "Speed: 5 m/s".
- The output on the calculator's screen is "TTC: 2.0s", glowing in Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** THE COLLISION CALCULATOR
- **BODY:**
  - Today, you will build a working Time-to-Collision (TTC) calculator.
  - You will understand the core algorithm that powers every modern Forward Collision Warning system.

---

## SLIDE 3:
**Visual Design**
- A simple icon showing a car with a "!" warning symbol in front of it.
- The "!" is Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** THE OBJECTIVE
- **BODY:**
  - **GOAL:** To warn the driver of an imminent collision.
  - **CORE QUESTION:** How do we know a collision is *imminent*?
  - **ANSWER:** By calculating the Time-to-Collision.

---

## SLIDE 4:
**Visual Design**
- An illustration of a car driving towards a pedestrian.
- Two large question marks are shown. One points to the space between the car and pedestrian, labeled "DISTANCE?". The other points to the car's speedometer, labeled "SPEED?".

**Text Content**
- **DISPLAY HEADER:** THE TWO UNKNOWNS
- **BODY:**
  - To calculate TTC, we need to know two things:
    1.  How far away is the object?
    2.  How fast are we approaching it?

---

## SLIDE 5: 
**Visual Design**
- A diagram showing a person far away (small bounding box) and the same person up close (large bounding box).
- An inverse relationship is shown: "Box Height ↑, Distance ↓".
- The bounding boxes are Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** DISTANCE FROM PIXELS
- **BODY:**
  - We don't have a laser ruler. We have a camera.
  - We can **estimate** distance by using the size of the object's bounding box.
  - An object that appears larger (a taller bounding box) is closer than one that appears smaller.
- **JUPYTER:** Section 2 - Distance Estimation.

---

## SLIDE 6:
**Visual Design**
- An icon of the VESC motor controller.
- An arrow points from it to a speedometer icon, with the text "RPM -> km/h" in the middle.
- The text is highlighted in Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** SPEED FROM THE VESC
- **BODY:**
  - This is the easy part for us.
  - Our VESC gives us precise RPM data.
  - With a little math (wheel size and gear ratio), we can convert RPM to meters per second.

---

## SLIDE 7:
**Visual Design**
- The core formula presented in large, bold, blueprint-style text.
- `TTC (seconds) = Distance (meters) / Closing Speed (meters/second)`
- The entire formula is rendered in Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** THE FORMULA
- **BODY:**
  - This simple formula is the heart of our system.
  - It tells us how many seconds we have until a potential impact, assuming constant speed.
- **JUPYTER TRANSITION:** Section 3 - Time-to-Collision.

---

## SLIDE 8:
**Visual Design**
- A simple animation concept.
- A car is shown 10 meters away from an obstacle. Its speed is 5 m/s.
- The formula is shown being calculated: `10m / 5m/s = 2s`.
- A 2-second countdown timer appears.

**Text Content**
- **DISPLAY HEADER:** A PRACTICAL EXAMPLE
- **BODY:**
  - If an object is 10 meters away...
  - ...and you are approaching it at 5 meters per second...
  - ...you have **2.0 seconds** until collision.

---

## SLIDE 9:
**Visual Design**
- A "danger meter" graphic, like a tachometer's redline.
- **0-1s:** Red zone, labeled "CRITICAL".
- **1-3s:** Yellow zone, labeled "WARNING".
- **>3s:** Green zone, labeled "MONITOR".
- The needle is pointing to the Yellow zone.

**Text Content**
- **DISPLAY HEADER:** DEFINING DANGER
- **BODY:**
  - A TTC number is useless without context. We define danger zones:
    - **> 3 seconds:** Safe. Just keep monitoring.
    - **1 to 3 seconds:** High alert. A warning should be issued.
    - **< 1 second:** Critical danger. An immediate, loud alert is needed.
- **JUPYTER:** Section 4 - TTC Mapping for Brake Intervention.

---

## SLIDE 10:
**Visual Design**
- The sensor fusion diagram from Module 9 is shown again.
- Camera data and VESC data flow into the "Logic Core" where the TTC is calculated.

**Text Content**
- **DISPLAY HEADER:** SENSOR FUSION IN ACTION
- **BODY:**
  - Notice that our TTC calculation requires data from **both** sensors.
  - **Camera:** Gives us the bounding box to estimate **DISTANCE**.
  - **VESC:** Gives us the RPM to calculate **SPEED**.
  - This is a perfect example of sensor fusion.

---

## SLIDE 11:
**Visual Design**
- Two scenarios side-by-side.
- **Left:** "CAMERA ONLY" - Shows a picture of a distant car. Text: "I see a car, but is it a threat?"
- **Right:** "FUSION" - Shows the same picture, but with added data "SPEED: 50 MPH". Text: "I see a car AND we are approaching it fast. THREAT!"

**Text Content**
- **DISPLAY HEADER:** WHY FUSION IS BETTER
- **BODY:**
  - **Camera Alone:** Knows *what* is there, but not the context of your own motion.
  - **VESC Alone:** Knows *how fast* you are moving, but not *what* is in front of you.
  - **Together:** They provide the complete picture needed to assess risk.

---

## SLIDE 12:
**Visual Design**
- An illustration of a car driving towards a harmless plastic bag floating across the road.
- The car's system is shown incorrectly triggering a loud "DANGER!" alert.

**Text Content**
- **DISPLAY HEADER:** PROBLEM: FALSE POSITIVES
- **BODY:**
  - The system alerts when there is no real danger.
  - **Example:** A shadow, a plastic bag, or a poorly classified object triggers the alarm.
  - **Result:** The driver gets annoyed and learns to ignore or distrust the system.

---

## SLIDE 13:
**Visual Design**
- An illustration of a car driving towards a real pedestrian who is partially obscured by a bush.
- The car's system is shown being silent, with no alert. This is the more dangerous scenario.

**Text Content**
- **DISPLAY HEADER:** PROBLEM: FALSE NEGATIVES
- **BODY:**
  - The system fails to alert when there *is* a real danger.
  - **Example:** The camera fails to detect a pedestrian in bad lighting.
  - **Result:** A collision that could have been prevented occurs. This is a critical failure.

---

## SLIDE 14:
**Visual Design**
- A balancing scale.
- On one side is a "Warning" icon with the text "Annoying but Safe" (False Positives).
- On the other side is a "Crash" icon with the text "Quiet but Dangerous" (False Negatives).
- The scale is slightly tipped towards the "Annoying but Safe" side.

**Text Content**
- **DISPLAY HEADER:** THE ENGINEERING TRADEOFF
- **BODY:**
  - Engineers must choose a balance.
  - **Too sensitive?** You get too many false positives.
  - **Not sensitive enough?** You risk false negatives.
  - For safety systems, it is always better to err on the side of caution (more false positives).

---

## SLIDE 15:
**Visual Design**
- An isometric render of a student's hands coding the TTC formula in a Jupyter Notebook.
- The formula in the code glows Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** BUILD THE CALCULATOR
- **BODY:**
  - Open `12_ADAS_Theory.ipynb`.
  - You will implement distance, TTC, and TTC-to-brake mapping helpers.
- **JUPYTER:** Create the core FCW math and TTC-driven intervention mapping.
