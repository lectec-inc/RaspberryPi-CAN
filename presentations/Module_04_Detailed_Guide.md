# MODULE 4
Taking Control: Commanding Your Motor
Safety-First Motor Control
Lectec PEV AI Curriculum
Day 4 of 14

## STYLE MANIFESTO: BLUEPRINT FUTURISM
- **Color Palette:** STRICT White background, Solid Black text, Electric Blue (#44B6E5) accents.
- **Typography:** Space Grotesk (Display sizes for headers).
- **Imagery:** 3D Isometric Technical Renders. Monochromatic clay-render style with #44B6E5 "energy glows" on highlights.
- **Background:** Faint, thin-line isometric white grid.

---

## TEACHER'S GUIDE: MODULE 4 OVERVIEW

**Module Goal:** To teach students how to safely control the VESC motor using the `student_api`. This lesson is the most safety-critical of the CAN-bus section. The primary focus must be on process and safety, not just results.

**Lesson Structure:**
- **(10 min) SAFETY FIRST Briefing:** This is the most important part of the lesson. Use the slides to walk through every safety rule. Ensure every student understands the emergency stop command (`set_duty_cycle(0)`) and the physical setup (vehicle on a secure stand).
- **(10 min) Lecture:** Explain the three control methods, focusing on Duty Cycle and Regenerative Braking.
- **(20 min) Workshop:** Students work through the `Student_Notebook_04.ipynb` exercises. Circulate to ensure they are following the safety checklist and understanding the code.
- **(5 min) Wrap-up:** Review the concept of a smooth acceleration sequence and its real-world parallels.

---

## SLIDE 1: Title Slide
**Visual Design**
- A 3D isometric render of the VESC controller.
- A bold, Electric Blue (#44B6E5) arrow representing a "command" flows from a representation of code into the VESC's control port.
- Faint isometric grid background.

**Text Content**
- **DISPLAY HEADER:** MODULE 4: MOTOR CONTROL
- **SUBTEXT:** Commanding Your Vehicle
- **BOTTOM FOOTER:** Lectec PEV AI Curriculum | Day 4 of 14

---

## SLIDE 2: TODAY'S GOAL
**Visual Design**
- A simple, clean animation concept showing a motor's RPM smoothly ramping up, holding steady, and ramping back down to zero.
- The motion is represented by a clean line graph where the line is a glowing Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** CONTROLLED MOTION
- **BODY:**
  - Today, you will command the motor to move for the first time.
  - You will learn to safely start it, control its speed, and bring it to a stop using a smooth, software-controlled sequence.
- **CALLOUT:** "In 40 minutes, you will write the code that makes it spin."

---

## SLIDE 3: SAFETY FIRST
**Visual Design**
- A large, bold "WARNING" icon (a triangle with an exclamation mark) rendered in the blueprint style.
- The icon is highlighted with an Electric Blue (#44B6E5) outline.

**Text Content**
- **DISPLAY HEADER:** CRITICAL SAFETY PROTOCOLS
- **BODY:**
  - **THE VEHICLE MUST BE ON A SECURE TEST STAND.**
  - Wheels must be completely off the ground.
  - Keep hands, hair, and loose clothing away from all moving parts.
- **CRITICAL:** Failure to follow these rules can result in injury.

---

## SLIDE 4: Three Control Methods
**Visual Design**
- A grid of three monochromatic icons.
- **Icon 1:** A throttle or slider (Duty Cycle).
- **Icon 2:** A lightning bolt with an arrow (Current Control).
- **Icon 3:** A brake pedal icon (Braking).

**Text Content**
- **DISPLAY HEADER:** METHODS OF CONTROL
- **BODY:**
  - We have three primary ways to command the VESC:
    - **Duty Cycle:** Like a throttle percentage.
    - **Current Control:** Commanding a specific amount of torque.
    - **Brake Current:** Using the motor itself to brake (Regenerative Braking).

---

## SLIDE 5: Duty Cycle Control
**Visual Design**
- A horizontal slider bar from -1.0 to +1.0. A marker is shown at +0.25.
- An arrow points from the marker to text that reads "25% Forward Throttle".
- The slider bar is Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** DUTY CYCLE: THE THROTTLE
- **BODY:**
  - `set_duty_cycle(value)`
  - The value is a percentage from -1.0 (-100% reverse) to 1.0 (100% forward).
  - `0.0` is neutral (stop).
  - This is the simplest and safest way to control speed.
- **JUPYTER TRANSITION:** Section 2 - Duty Cycle Control.

---

## SLIDE 6: Current Control
**Visual Design**
- An isometric view of the motor with a large arrow pushing against the wheel, labeled "Torque".
- The arrow is glowing Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** CURRENT: THE FORCE
- **BODY:**
  - `set_current(amps)`
  - This commands the motor to apply a specific amount of rotational force (torque).
  - Useful for holding a position or applying consistent force, but more advanced than duty cycle.

---

## SLIDE 7: Regenerative Braking
**Visual Design**
- An animation concept. The motor is spinning.
- The `set_brake_current()` command is called.
- The motor is shown slowing down, and an Electric Blue (#44B6E5) energy flow is visualized going from the motor *back* to the battery icon.

**Text Content**
- **DISPLAY HEADER:** REGENERATIVE BRAKING
- **BODY:**
  - `set_brake_current(amps)`
  - This turns the spinning motor into a generator.
  - It uses the motor's own resistance to slow the vehicle down.
  - The energy generated is sent back to recharge the battery!

---

## SLIDE 8: The Safety Flag
**Visual Design**
- A simple code block showing an `if` statement.
- `if MOTOR_CONTROL_ENABLED == True:`
- The `True` value is highlighted in Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** THE INTENTIONAL STEP
- **BODY:**
  - Before running any motor commands, you must explicitly enable them in your code.
  - This prevents accidental motor activation.
  - It's a digital "safety switch" you must flip before proceeding.

---

## SLIDE 9: Command Sequence
**Visual Design**
- A clean, four-stage flowchart.
- 1. Check Safety -> 2. Send Command -> 3. Verify (Read RPM) -> 4. Send Stop Command.
- The arrows connecting the stages are Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** THE CONTROL LOOP
- **BODY:**
  - Always follow a safe command sequence:
    1.  **Check:** Ensure the system is ready and safe.
    2.  **Command:** Send a single, small motor command.
    3.  **Verify:** Read telemetry to see if the motor responded as expected.
    4.  **Stop:** Always end your sequence with a command to stop the motor.

---

## SLIDE 10: Emergency Stop
**Visual Design**
- A large, red, hexagonal "STOP" sign.
- Inside the sign, the code `set_duty_cycle(0)` is written in bold, white text.

**Text Content**
- **DISPLAY HEADER:** THE MOST IMPORTANT COMMAND
- **BODY:**
  - `set_duty_cycle(0)`
  - This is your emergency stop. It immediately commands the motor to go to a neutral state.
  - Memorize this command. It is the first thing you should do if the motor behaves unexpectedly.

---

## SLIDE 11: Real Car Comparison
**Visual Design**
- A simple diagram showing a foot pressing a car's accelerator pedal.
- The pedal's position is mapped to a percentage (e.g., "30% throttle").
- This is linked to our `set_duty_cycle(0.3)` command.

**Text Content**
- **DISPLAY HEADER:** DRIVE-BY-WIRE
- **BODY:**
  - Modern cars work the same way. Your accelerator pedal isn't directly connected to the engine.
  - It's an electronic sensor that tells a computer what "duty cycle" to apply.
  - You are learning the fundamentals of modern vehicle control.

---

## SLIDE 12: Your Turn (CAREFULLY)
**Visual Design**
- An isometric render of the test bench setup.
- The skateboard is securely fastened, and a student's hands are shown on a laptop nearby, NOT touching the vehicle.
- The laptop screen shows a Jupyter notebook.

**Text Content**
- **DISPLAY HEADER:** CAREFUL EXECUTION
- **BODY:**
  - Open `Student_Notebook_04.ipynb`.
  - Complete the mandatory safety checklist.
  - Build your first smooth acceleration sequence.
- **MISSION:** Section 4 - Knowledge Check.
