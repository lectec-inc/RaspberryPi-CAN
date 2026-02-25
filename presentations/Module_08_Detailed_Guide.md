# MODULE 8
AI + Physical Response
Triggering Hardware with AI
Lectec PEV AI Curriculum
Day 8 of 14

## STYLE MANIFESTO: BLUEPRINT FUTURISM
- **Color Palette:** STRICT White background, Solid Black text, Electric Blue (#44B6E5) accents.
- **Typography:** Space Grotesk (Display sizes for headers).
- **Imagery:** 3D Isometric Technical Renders. Monochromatic clay-render style with #44B6E5 "energy glows" on highlights.
- **Background:** Faint, thin-line isometric white grid.

---

## SLIDE 1: Title Slide
**Visual Design**
- A central, monochromatic 3D render of the Raspberry Pi Zero 2W.
- An Electric Blue (#44B6E5) "energy pulse" originates from the GPIO pins and travels outwards, transforming into a soundwave icon.
- Faint isometric grid background.

**Text Content**
- **DISPLAY HEADER:** MODULE 8: AI + HARDWARE
- **SUBTEXT:** From Detection to Physical Action
- **BOTTOM FOOTER:** Lectec PEV AI Curriculum | Day 8 of 14

---

## SLIDE 2: TODAY'S GOAL
**Visual Design**
- A 3D isometric scene showing the AI camera detecting a "person".
- A data line flows from the camera to the Raspberry Pi's GPIO pins.
- From the GPIO pins, a wire connects to a buzzer, which is emitting visible, concentric soundwave rings in Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** THE ALERT SYSTEM
- **BODY:**
  - Today, you will make your AI interact with the real world.
  - You will build a system that sounds an alarm when it detects a specific object.
- **CALLOUT:** "In 40 minutes, your AI will have a voice."

---

## SLIDE 3: GPIO Introduction
**Visual Design**
- A close-up, high-detail isometric render of the Raspberry Pi's 40-pin GPIO header.
- Several pins are highlighted with Electric Blue (#44B6E5) and labeled (e.g., "5V", "GND", "GPIO 17").

**Text Content**
- **DISPLAY HEADER:** THE PI'S NERVOUS SYSTEM
- **BODY:**
  - **G.P.I.O.** = General Purpose Input/Output.
  - These pins are the Raspberry Pi's physical connection to the outside world.
  - We can use them to send simple "ON" or "OFF" signals to other electronics.

---

## SLIDE 4: The Buzzer
**Visual Design**
- A simple, clean isometric render of a small black piezo buzzer.
- A wiring diagram is shown next to it: one wire to a GPIO pin, the other to a Ground (GND) pin on the Pi.
- The wires are rendered in the blueprint style.

**Text Content**
- **DISPLAY HEADER:** THE ACTUATOR
- **BODY:**
  - A simple electronic component that makes noise when it receives power.
  - We will connect it directly to the GPIO pins.
- **JUPYTER TRANSITION:** Section 2 - GPIO Basics.

---

## SLIDE 5: Basic GPIO Control
**Visual Design**
- A simplified animation concept.
- A line of code `api.buzzer_on()` is shown. This triggers an isometric render of a GPIO pin to light up in Electric Blue (#44B6E5), and a connected LED to turn on.
- The next line `api.buzzer_off()` causes the light to turn off.

**Text Content**
- **DISPLAY HEADER:** DIGITAL ON/OFF
- **BODY:**
  - Controlling GPIO is like flipping a light switch in code.
  - Students should control the buzzer through `AIStudentAPI` (not direct `gpiozero.Buzzer(...)`) to avoid GPIO pin reuse errors after reruns.
  - **HIGH (ON):** Send voltage to the pin.
  - **LOW (OFF):** Stop sending voltage.
  - By turning it on and off quickly, we can create beeps.

---

## SLIDE 6: Detection + Action
**Visual Design**
- A clean flowchart representing the core logic.
- (Diamond) "Object Detected?" -> [Yes] -> (Diamond) "Confidence > 0.8?" -> [Yes] -> (Rectangle) "BEEP".
- The "BEEP" action rectangle glows in Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** CONDITIONAL LOGIC
- **BODY:**
  - The core of our system is a simple `if` statement:
  - `if object is a 'person' and confidence is high:`
  - `....trigger the buzzer`
- **JUPYTER TRANSITION:** Section 3 - Detection Alerts.

---

## SLIDE 7: The Spam Problem
**Visual Design**
- A conceptual illustration. A camera is detecting a person who is standing still.
- A rapid-fire stream of "BEEP!" text bubbles emanates from a speaker, creating a visual representation of noise and annoyance.

**Text Content**
- **DISPLAY HEADER:** THE SPAM PROBLEM
- **BODY:**
  - The camera runs at ~10 frames per second.
  - If an object is in view, it will be detected 10 times every second.
  - This will trigger the alarm 10 times per second, creating constant, useless noise.

---

## SLIDE 8: Cooldown Logic
**Visual Design**
- An animation concept showing a timeline.
- A detection event occurs at T=0, triggering a beep.
- A timer (represented by a bar that depletes) appears, glowing Electric Blue (#44B6E5), labeled "Cooldown: 3s".
- Another detection event at T=1 is shown being ignored because the cooldown is active.

**Text Content**
- **DISPLAY HEADER:** INTELLIGENT WAITING
- **BODY:**
  - We need to prevent the alarm from firing too frequently.
  - **The Logic:**
    1.  When an alert is triggered, record the current time.
    2.  Before triggering a new alert, check if enough time has passed since the last one.
- **RESULT:** One beep per event, not one beep per frame.

---

## SLIDE 9: Custom Patterns
**Visual Design**
- A Python dictionary is shown as a 3D object.
- It maps text labels to musical note icons.
- `{'person': [short, short], 'car': [long, short, long]}`
- The musical notes are rendered in Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** UNIQUE SIGNATURES
- **BODY:**
  - A single beep is good. Different patterns are better.
  - We can create unique audio signatures for different objects.
    - **Person:** Two short beeps.
    - **Car:** A long, low tone.
- **JUPYTER TRANSITION:** Section 4 - Custom Patterns.

---

## SLIDE 10: Complete Pipeline
**Visual Design**
- A final, complete flowchart combining all concepts.
- Detection -> Filter by Label -> Filter by Confidence -> Check Cooldown -> Trigger Custom Pattern.
- Each stage is a distinct, clean block in the isometric blueprint style.

**Text Content**
- **DISPLAY HEADER:** THE FULL PIPELINE
- **BODY:**
  - Our system is now robust and intelligent.
  - It filters for the right objects, checks for high confidence, respects a cooldown period, and triggers a specific, meaningful alert.

---

## SLIDE 11: Real World Examples
**Visual Design**
- A grid of two icons.
- 1. A security camera with motion detection rings.
- 2. A modern car with lines showing a blind-spot detection system.
- The detection elements (rings, lines) are Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** INDUSTRY APPLICATIONS
- **BODY:**
  - The system you built is the foundation for real-world technology:
    - **Home Security:** Alerting when a person is detected at your door.
    - **Automotive:** Blind-spot warnings that beep when a car is detected.

---

## SLIDE 12: Your Turn
**Visual Design**
- An isometric render of the full skateboard system.
- The buzzer is glowing with Electric Blue (#44B6E5) soundwaves, and the AI camera is actively scanning.
- The entire system is presented as a complete, functioning device.

**Text Content**
- **DISPLAY HEADER:** BUILD YOUR ALERT SYSTEM
- **BODY:**
  - Complete the exercises in your notebook.
  - Create your own custom alert patterns for different objects.
- **MISSION:** Section 5 - Knowledge Check.
