# MODULE 4
Brake Control: Safe Intervention Engineering
Bounded Brake Sequences and Telemetry-Gated Control
Lectec PEV AI Curriculum

## SLIDE 1:
**Visual Design**
- Isometric VESC + wheel with Electric Blue control waveform.

**Text Content**
- **DISPLAY HEADER:** MODULE 4: BRAKE CONTROL
- **SUBTEXT:** Safe Intervention Engineering
- **BOTTOM FOOTER:** Lectec PEV AI Curriculum | Day 4 of 14

---

## SLIDE 2:
**Visual Design**
- Two line plots: brake current ramp-up and automatic release ramp-down.

**Text Content**
- **DISPLAY HEADER:** CONTROLLED BRAKING
- **BODY:**
  - Build safe intervention logic with bounded values.
  - Validate behavior with live telemetry.
  - Tune profiles for smooth response.

---

## SLIDE 3:
**Visual Design**
- A work bench with an electric skateboard upside down laying flat and an electric scooter upside down with the handle hanging off the table edge towards the ground plane. The two vehicles are next to each other on the workbench.

**Text Content**
- **DISPLAY HEADER:** MANDATORY BENCH SETUP
- **BODY:**
  - Vehicle secured on stand.
  - Hand-spin validation only.
  - One operator, one observer.
  - Keep all limbs and loose clothing clear.

---

## SLIDE 4: 
**Visual Design**
- Blueprint callout box showing API signature.

**Text Content**
- **DISPLAY HEADER:** STANDARD CONTROL INTERFACE
- **BODY:**
  - `set_brake_current(current_a, ramp_time_s)`
  - `current_a`: `0.0` to `10.0` A
  - `ramp_time_s`: `3.0` to `10.0` s
  - Built-in cooldown + automatic release ramp

---

## SLIDE 5: 
**Visual Design**
- Compare two curves: sudden step vs smooth ramp.

**Text Content**
- **DISPLAY HEADER:** What would happen if it went from 0-100% brake instantly?
- **BODY:**
  - Ramping limits are the solution to abrupt torque changes.
  - Smoother force profile improves stability and student safety.
  - Predictable behavior is easier to validate in class.

---

## SLIDE 6:
**Visual Design**
- Flowchart: `Read RPM + Temp -> Check Thresholds -> Apply Brake`.

**Text Content**
- **DISPLAY HEADER:** INTERVENE ONLY WHEN NEEDED
- **BODY:**
  - Gate by RPM threshold.
  - Gate by temperature and controller availability.
  - Skip intervention when guard conditions fail.

---

## SLIDE 7:
**Visual Design**
- Split panel: left side plain-language logic bullets, right side simple flowchart.

**Text Content**
- **DISPLAY HEADER:** DESIGN THE LOGIC BEFORE CODING
- **BODY:**
  - Write pseudocode live with the teacher for telemetry-gated intervention.
  - Required gates: `abs(rpm) > 150` and `fet_temp < 70`.
  - Outcome A: apply bounded brake sequence.
  - Outcome B: no intervention.
- **JUPYTER:** Exercise 2.2A in Module 4 notebook is intentionally blank for student-authored pseudocode.

---

## SLIDE 8:
**Visual Design**
- Progression graphic: student-authored pseudocode transforms into a blank Python implementation cell.

**Text Content**
- **DISPLAY HEADER:** TRANSLATE LOGIC INTO CODE
- **BODY:**
  - Move line-by-line from student-authored pseudocode to executable Python.
  - Keep gate checks explicit and readable.
  - Use target intervention profile: `set_brake_current(3.0, 4.0)`.
- **JUPYTER:** Exercise 2.2B blank implementation cell (students fill from scratch).

---

## SLIDE 9:
**Visual Design**
- Timeline showing two calls; second blocked during cooldown.

**Text Content**
- **DISPLAY HEADER:** SPAM PREVENTION
- **BODY:**
  - Cooldown avoids repeated intervention bursts.
  - Improves system stability and readability.
  - Encourages deliberate control-loop design.

---

## SLIDE 10:
**Visual Design**
- Table of profiles (A, s) and expected feel.

**Text Content**
- **DISPLAY HEADER:** PARAMETER TUNING
- **BODY:**
  - Example profiles: `(2A, 6s)`, `(4A, 5s)`, `(6A, 3.5s)`.
  - Compare response smoothness and stopping behavior.
  - Document observations in notebook.

---

## SLIDE 11: 
**Visual Design**
- 4-step checklist with blue checkboxes.

**Text Content**
- **DISPLAY HEADER:** VERIFY EVERY RUN
- **BODY:**
  1. Confirm connection and telemetry.
  2. Run one bounded brake profile.
  3. Verify release ramp and cooldown.
  4. Log results and anomalies.

---

## SLIDE 12:
**Visual Design**
- Notebook dashboard mock showing RPM, temp, profile, and result.

**Text Content**
- **DISPLAY HEADER:** OBSERVE -> DECIDE -> INTERVENE
- **BODY:**
  - Strong control systems are data-first.
  - Interventions must be bounded and explainable.
  - Every actuation should be justified by telemetry.

---

## SLIDE 13: 
**Visual Design**
- Isometric laptop on bench with `04_Brake_Control.ipynb` open.

**Text Content**
- **DISPLAY HEADER:** BUILD THE BRAKE CONTROL LOOP
- **BODY:**
  - Complete safety checklist.
  - Run first sequence.
  - Complete Exercise 2.2A pseudocode and Exercise 2.2B implementation, then validate cooldown behavior.
- **MISSION:** Section 4 Knowledge Check.

---

## SLIDE 14:
**Visual Design**
- Summary blueprint with three tags: Bounded, Smooth, Verified.

**Text Content**
- **DISPLAY HEADER:** CORE TAKEAWAY
- **BODY:**
  - Safe intervention = bounded parameters + smooth ramps + validation.
