# MODULE 8
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
- A monochromatic 3D render of the Raspberry Pi Zero 2W.
- An Electric Blue (#44B6E5) "energy pulse" originates from the GPIO pins and travels outwards, transforming into a soundwave icon.
- Faint isometric grid background.

**Text Content**
- **DISPLAY HEADER:** MODULE 8: AI + HARDWARE
- **SUBTEXT:** From Detection to Physical Action

---

## SLIDE 2: 
**Visual Design**
- A 3D isometric scene showing the AI camera detecting a "person".
- A data line flows from the camera to the Raspberry Pi's GPIO pins.
- From the GPIO pins, a wire connects to a circular buzzer, which is emitting visible, concentric soundwave rings in Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** THE ALERT SYSTEM
- **BODY:**
  - Today, you will make your AI interact with the real world.
  - You will build a system that sounds an alarm when it detects a specific object.

---

## SLIDE 3:
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

## SLIDE 4:
**Visual Design**
- A simple, clean isometric render of a small black piezo buzzer.
- A wiring diagram is shown next to it: one wire to a GPIO pin, the other to a Ground (GND) pin on the Pi.
- The wires are rendered in the blueprint style.

**Text Content**
- **DISPLAY HEADER:** THE ACTUATOR
- **BODY:**
  - A simple electronic component that makes noise when it receives power.
  - We will connect it directly to the GPIO pins.
- **JUPYTER:** Section 2 - GPIO Basics.

---

## SLIDE 5:
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

## SLIDE 6:
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
- **JUPYTER:** Section 3 - Detection Alerts.

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

## SLIDE 8:
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

## SLIDE 9:
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
- **JUPYTER:** Section 4 - Custom Patterns.

---

## SLIDE 10:
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

## SLIDE 11:
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

## SLIDE 12:
**Visual Design**
- An isometric render of the full skateboard system.
- The buzzer is glowing with Electric Blue (#44B6E5) soundwaves, and the AI camera is actively scanning.
- The entire system is presented as a complete, functioning device.

**Text Content**
- **DISPLAY HEADER:** BUILD YOUR ALERT SYSTEM
- **BODY:**
  - Complete the exercises in your notebook.
  - Create your own custom alert patterns for different objects.
- **Jupyter:** Section 5 - Knowledge Check.
