# MODULE 7
Live Object Detection
Activating the AI Camera
Lectec PEV AI Curriculum
Day 7 of 14

## STYLE MANIFESTO: BLUEPRINT FUTURISM
- **Color Palette:** STRICT White background, Solid Black text, Electric Blue (#44B6E5) accents.
- **Typography:** Space Grotesk (Display sizes for headers).
- **Imagery:** 3D Isometric Technical Renders. Monochromatic clay-render style with #44B6E5 "energy glows" on highlights.
- **Background:** Faint, thin-line isometric white grid.

---

## SLIDE 1: Title Slide
**Visual Design**
- A high-detail, monochromatic 3D render of the IMX500 AI camera.
- A cone of light, made of faint isometric grid lines, projects from the lens.
- Inside the cone, simple wireframe cubes are visible, representing "detected objects". The wireframes are Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** MODULE 7: OBJECT DETECTION
- **SUBTEXT:** Activating Your AI Vision
- **BOTTOM FOOTER:** Lectec PEV AI Curriculum | Day 7 of 14

---

## SLIDE 2: TODAY'S GOAL
**Visual Design**
- A 3D isometric render of a live video feed, as if projected from the Jupyter notebook.
- The video shows a classroom scene.
- An Electric Blue (#44B6E5) bounding box is drawn around a person, with the label "person: 0.96". Another is drawn around a "cell phone: 0.89".

**Text Content**
- **DISPLAY HEADER:** THE WORLD, LABELED
- **BODY:**
  - Today, you will activate your AI camera for the first time.
  - You will build a system that sees the world, identifies objects, and draws boxes around them in real-time.
- **CALLOUT:** "In 40 minutes, your machine will see."

---

## SLIDE 3: The COCO Dataset
**Visual Design**
- A large, clean grid of 80 monochromatic icons, representing the objects in the COCO dataset (e.g., person, car, dog, stop sign).
- The entire grid is presented as a "blueprint" or technical chart.

**Text Content**
- **DISPLAY HEADER:** THE AI'S ENCYCLOPEDIA
- **BODY:**
  - Our AI was trained on the **COCO Dataset**.
  - It contains 80 common object categories.
  - If an object is not in this dataset, the AI cannot recognize it. This is a critical limitation.

---

## SLIDE 4: Object Categories
**Visual Design**
- A simplified version of the grid from the previous slide, but organized into categories.
- Categories are labeled: "People", "Vehicles", "Animals", "Household Items", etc.
- Each category title has an Electric Blue (#44B6E5) underline.

**Text Content**
- **DISPLAY HEADER:** CATEGORICAL VISION
- **BODY:**
  - The 80 objects are grouped logically.
  - This helps us filter for specific types of objects, like looking only for "vehicles" or only for "people".

---

## SLIDE 5: Starting the Camera
**Visual Design**
- An isometric cutaway of the Raspberry Pi.
- A data path is shown from the CSI camera connector to the CPU/VPU.
- The path is a glowing Electric Blue (#44B6E5) line labeled "Video Pipeline".

**Text Content**
- **DISPLAY HEADER:** THE VIDEO PIPELINE
- **BODY:**
  - We will use a Python library to initialize the camera.
  - This creates a high-speed data stream from the camera sensor to the processor.
- **JUPYTER TRANSITION:** Section 2 - Camera Setup.

---

## SLIDE 6: Detection Pipeline
**Visual Design**
- A clean, four-stage flowchart.
- 1. Camera Icon -> 2. AI Chip Icon -> 3. "Results" Text Box -> 4. Display Icon.
- Electric Blue (#44B6E5) arrows connect the stages, showing the flow of data.

**Text Content**
- **DISPLAY HEADER:** FROM PHOTONS TO PREDICTIONS
- **BODY:**
  - **CAPTURE:** The camera sensor captures an image.
  - **PROCESS:** The onboard AI chip analyzes the image.
  - **OUTPUT:** The AI returns a list of detected objects.
  - **DISPLAY:** We draw the results onto the video feed.

---

## SLIDE 7: Reading the Results
**Visual Design**
- An isometric render of a Python dictionary or JSON object.
- It has three key-value pairs highlighted:
  - `"label": "person"`
  - `"confidence": 0.96` (value glows in Electric Blue)
  - `"box": [x, y, w, h]`

**Text Content**
- **DISPLAY HEADER:** STRUCTURED DATA
- **BODY:**
  - For each object found, the AI gives us three key pieces of information:
    - **LABEL:** What it is (e.g., "person").
    - **CONFIDENCE:** How sure it is (e.g., 0.96).
    - **BOUNDING BOX:** Where it is.
- **JUPYTER TRANSITION:** Section 3 - Live Detection.

---

## SLIDE 8: Factors Affecting Accuracy
**Visual Design**
- A series of four small scenes.
- 1. An object in dim light vs. bright light.
- 2. An object far away vs. close up.
- 3. An object viewed from the front vs. a weird angle.
- 4. An object partially hidden (occluded) behind another.

**Text Content**
- **DISPLAY HEADER:** REAL-WORLD CHALLENGES
- **BODY:**
  - AI vision is not perfect. Accuracy depends on:
    - **Lighting:** Too dark or too bright can hide features.
    - **Distance & Size:** Small or distant objects are harder to see.
    - **Angle:** Unusual viewpoints can confuse the model.
    - **Occlusion:** Partially hidden objects are difficult to identify.

---

## SLIDE 9: What It Can't Detect
**Visual Design**
- A clear image of a water bottle, but the AI detection overlay shows a box with a question mark "?".
- The question mark is Electric Blue (#44B6E5).

**Text Content**
- **DISPLAY HEADER:** THE LIMITS OF TRAINING
- **BODY:**
  - Remember the COCO dataset?
  - A standard water bottle is **not** one of the 80 objects.
  - The AI has no "encyclopedia" entry for it, so it cannot be detected.
  - It might misclassify it (e.g., "cup"), or it might see nothing at all.

---

## SLIDE 10: Confidence Filtering
**Visual Design**
- A two-panel "Before/After" comparison of a video feed.
- **Before:** The feed is cluttered with many faint, incorrect bounding boxes (e.g., a chair leg labeled "person: 0.15").
- **After:** The feed is clean, showing only one strong, correct bounding box with a high confidence score.

**Text Content**
- **DISPLAY HEADER:** REDUCING THE NOISE
- **BODY:**
  - The AI will constantly make low-confidence guesses.
  - By applying a **confidence threshold**, we ignore these "false positives."
  - This is the single most important step for building a reliable system.
- **JUPYTER TRANSITION:** Section 4 - Filtering.

---

## SLIDE 11: Try These Objects
**Visual Design**
- A simple grid of monochromatic icons for objects commonly found in a classroom.
- Icons: Person, Laptop, Book, Cell Phone, Chair.
- Each icon has a subtle Electric Blue (#44B6E5) outline.

**Text Content**
- **DISPLAY HEADER:** TEST YOUR DETECTOR
- **BODY:**
  - Point your camera at these objects. Do they detect correctly?
    - A person (yourself!)
    - A cell phone
    - A laptop
    - A chair
    - A book

---

## SLIDE 12: Your Turn
**Visual Design**
- A final isometric view of the skateboard with the AI camera mounted.
- The camera is projecting a wide, glowing Electric Blue (#44B6E5) cone of vision, encompassing several objects in front of it.

**Text Content**
- **DISPLAY HEADER:** BECOME THE SUPERVISOR
- **BODY:**
  - Complete the exercises in your notebook.
  - You are now the supervisor of an AI. It's your job to test it, understand its limits, and use its output wisely.
- **MISSION:** Section 5 - Knowledge Check.
