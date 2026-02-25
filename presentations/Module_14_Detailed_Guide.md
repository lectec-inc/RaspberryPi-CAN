# MODULE 14
ADAS Capstone Project
Designing an Advanced ADAS Feature
Lectec PEV AI Curriculum
Day 14 of 14

## STYLE MANIFESTO: BLUEPRINT FUTURISM
- **Color Palette:** STRICT White background, Solid Black text, Electric Blue (#44B6E5) accents.
- **Typography:** Space Grotesk (Display sizes for headers).
- **Imagery:** 3D Isometric Technical Renders. Monochromatic clay-render style with #44B6E5 "energy glows" on highlights.
- **Background:** Faint, thin-line isometric white grid.

---

## TEACHER'S GUIDE: MODULE 14 OVERVIEW

**Module Goal:** This is the final capstone project. Students will design, implement, and present their own unique ADAS feature, demonstrating mastery of the entire course curriculum, from CAN bus communication to sensor fusion and AI implementation.

**Lesson Structure:**
- **(5 min) Introduction:** Frame the day as a "pitch to an automotive company." The goal is not just to build, but to present an innovative idea.
- **(5 min) Project Options Review:** Quickly go over the advanced project options to inspire students.
- **(25 min) Final Development Workshop:** Students work in their `14_ADAS_Capstone.ipynb` to complete their project and prepare their presentation.
- **(10 min) Project Presentations:** Have 3-4 students give their 2-minute "pitch" to the class. Time may require a second day for full class presentations.

---

## SLIDE 1: Title Slide
**Visual Design**
- A large, isometric render of a trophy, but styled as a technical blueprint.
- The trophy is glowing with an internal Electric Blue (#44B6E5) light.
- Faint isometric grid background.

**Text Content**
- **DISPLAY HEADER:** MODULE 14: ADAS CAPSTONE
- **SUBTEXT:** Engineer Your Own Safety Feature
- **BOTTOM FOOTER:** Lectec PEV AI Curriculum | Day 14 of 14

---

## SLIDE 2: TODAY'S GOAL
**Visual Design**
- An isometric scene of a student presenting their idea on a holographic screen to a group of engineers (represented by stylized figures).
- The presentation on the screen shows a flowchart of their custom ADAS feature.

**Text Content**
- **DISPLAY HEADER:** FROM STUDENT TO ENGINEER
- **BODY:**
  - Today, you will use the full range of your skills to design, build, and present a novel ADAS feature.
  - You will think about a real-world safety problem and engineer a creative solution.
- **CALLOUT:** "Your final project begins now."

---

## SLIDE 3: Project Options
**Visual Design**
- A grid of three advanced, monochromatic icons.
- **Icon A:** A car with predictive path lines extending forward.
- **Icon B:** Multiple objects with a "target priority" symbol on one of them.
- **Icon C:** A stop sign with a "speed limit zone" overlay.

**Text Content**
- **DISPLAY HEADER:** ADVANCED PROJECTS
- **BODY:**
  - **A. Enhanced FCW:** Use object motion to predict trajectory, not just current position.
  - **B. Multi-Object Threat Assessment:** Prioritize alerts based on which object is the biggest threat.
  - **C. Speed Limit Zone Enforcement:** Automatically suggest speed reduction when a stop sign is detected.
  - **D. Your Own ADAS Innovation:** Propose a custom feature.

---

## SLIDE 4: Project Requirements
**Visual Design**
- A blueprint-style checklist. Each item has a square checkbox.
- The checkboxes are highlighted in Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** ENGINEERING REQUIREMENTS
- **BODY:**
  - Must be a complete ADAS feature (not just detection).
  - Must include multi-level alerts and TTC-based bounded brake response policy.
  - Must handle edge cases gracefully.
  - Must include a real-time status dashboard.
  - Must be documented with a flowchart.

---

## SLIDE 5: Presentation Format
**Visual Design**
- A simple, clean timer icon with a "5 MINUTE PITCH" label.
- The label is in Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** THE PITCH
- **BODY:**
  - You have 5 minutes to present your project as if you were pitching it to automotive executives.
    - **1 min:** What is the problem?
    - **1 min:** What is your solution?
    - **2 min:** Live Demonstration.
    - **1 min:** Future Improvements.

---

## SLIDE 6: Your Turn
**Visual Design**
- An open, empty Jupyter Notebook is shown in isometric 3D, similar to Module 10 but with "ADAS Capstone" in the header.
- A blinking cursor, glowing in Electric Blue (#44B6E5), waits in the first code cell.

**Text Content**
- **DISPLAY HEADER:** FINAL BUILD
- **BODY:**
  - Open `14_ADAS_Capstone.ipynb`.
  - For buzzer alerts, use the `AIStudentAPI` buzzer helpers instead of creating raw `gpiozero.Buzzer` instances.
  - Design your system, write the code, and document your process.
- **MISSION:** Demonstrate complete mastery of the Lectec curriculum.


---

## Capstone Evaluation Addendum
- Add explicit scoring for intervention policy quality:
  - TTC mapping clarity
  - bounded parameter usage
  - cooldown and edge-case handling
