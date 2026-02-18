const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, LevelFormat, HeadingLevel,
        BorderStyle, WidthType, ShadingType, PageNumber, PageBreak } = require('docx');
const fs = require('fs');

// Colors
const LECTEC_BLUE = "2196F3";
const LECTEC_YELLOW = "FFCA28";
const LECTEC_BLACK = "1A1A1A";
const DARK_BLUE = "1976D2";
const LIGHT_BLUE = "E3F2FD";
const SUCCESS_GREEN = "4CAF50";
const WARNING_ORANGE = "FF9800";
const DANGER_RED = "F44336";
const GRAY = "666666";
const LIGHT_GRAY = "F5F5F5";

// Helper functions
function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 400, after: 200 },
    children: [new TextRun({ text, bold: true, size: 48, color: LECTEC_BLUE, font: "Arial" })]
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 300, after: 150 },
    children: [new TextRun({ text, bold: true, size: 36, color: DARK_BLUE, font: "Arial" })]
  });
}

function heading3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 100 },
    children: [new TextRun({ text, bold: true, size: 28, color: LECTEC_BLACK, font: "Arial" })]
  });
}

function heading4(text) {
  return new Paragraph({
    spacing: { before: 150, after: 80 },
    children: [new TextRun({ text, bold: true, size: 24, color: GRAY, font: "Arial" })]
  });
}

function para(text, options = {}) {
  return new Paragraph({
    spacing: { before: 80, after: 80 },
    children: [new TextRun({
      text,
      size: options.size || 22,
      color: options.color || LECTEC_BLACK,
      font: "Arial",
      bold: options.bold || false,
      italics: options.italics || false
    })]
  });
}

function bulletItem(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "bullets", level },
    spacing: { before: 40, after: 40 },
    children: [new TextRun({ text, size: 22, color: LECTEC_BLACK, font: "Arial" })]
  });
}

function numberedItem(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "numbers", level },
    spacing: { before: 40, after: 40 },
    children: [new TextRun({ text, size: 22, color: LECTEC_BLACK, font: "Arial" })]
  });
}

function calloutBox(title, content, color) {
  const border = { style: BorderStyle.SINGLE, size: 1, color };
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    columnWidths: [9360],
    rows: [
      new TableRow({
        children: [
          new TableCell({
            borders: { top: border, bottom: border, left: { style: BorderStyle.SINGLE, size: 24, color }, right: border },
            shading: { fill: LIGHT_GRAY, type: ShadingType.CLEAR },
            margins: { top: 120, bottom: 120, left: 200, right: 200 },
            width: { size: 9360, type: WidthType.DXA },
            children: [
              new Paragraph({
                spacing: { after: 80 },
                children: [new TextRun({ text: title, bold: true, size: 24, color, font: "Arial" })]
              }),
              new Paragraph({
                children: [new TextRun({ text: content, size: 22, color: LECTEC_BLACK, font: "Arial" })]
              })
            ]
          })
        ]
      })
    ]
  });
}

function notebookCallout(instruction) {
  const border = { style: BorderStyle.SINGLE, size: 1, color: SUCCESS_GREEN };
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    columnWidths: [9360],
    rows: [
      new TableRow({
        children: [
          new TableCell({
            borders: { top: border, bottom: border, left: { style: BorderStyle.SINGLE, size: 24, color: SUCCESS_GREEN }, right: border },
            shading: { fill: "E8F5E9", type: ShadingType.CLEAR },
            margins: { top: 120, bottom: 120, left: 200, right: 200 },
            width: { size: 9360, type: WidthType.DXA },
            children: [
              new Paragraph({
                spacing: { after: 80 },
                children: [new TextRun({ text: "NOTEBOOK ACTIVITY", bold: true, size: 24, color: SUCCESS_GREEN, font: "Arial" })]
              }),
              new Paragraph({
                children: [new TextRun({ text: instruction, size: 22, color: LECTEC_BLACK, font: "Arial" })]
              })
            ]
          })
        ]
      })
    ]
  });
}

function codeBlock(code) {
  const border = { style: BorderStyle.SINGLE, size: 1, color: "444444" };
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    columnWidths: [9360],
    rows: [
      new TableRow({
        children: [
          new TableCell({
            borders: { top: border, bottom: border, left: border, right: border },
            shading: { fill: "2D2D2D", type: ShadingType.CLEAR },
            margins: { top: 150, bottom: 150, left: 200, right: 200 },
            width: { size: 9360, type: WidthType.DXA },
            children: [
              new Paragraph({
                children: [new TextRun({ text: code, size: 20, color: "D4D4D4", font: "Courier New" })]
              })
            ]
          })
        ]
      })
    ]
  });
}

function slideHeader(slideNum, title) {
  return [
    new Paragraph({
      shading: { fill: LECTEC_BLUE, type: ShadingType.CLEAR },
      spacing: { before: 200, after: 100 },
      children: [
        new TextRun({ text: `SLIDE ${slideNum}: `, bold: true, size: 28, color: LECTEC_YELLOW, font: "Arial" }),
        new TextRun({ text: title, bold: true, size: 28, color: "FFFFFF", font: "Arial" })
      ]
    }),
    new Paragraph({ spacing: { after: 100 }, children: [] })
  ];
}

function spacer() {
  return new Paragraph({ spacing: { before: 100, after: 100 }, children: [] });
}

// Create the document
const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: "Arial", size: 22 }
      }
    },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 48, bold: true, font: "Arial", color: LECTEC_BLUE },
        paragraph: { spacing: { before: 400, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: DARK_BLUE },
        paragraph: { spacing: { before: 300, after: 150 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: LECTEC_BLACK },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 2 } },
    ]
  },
  numbering: {
    config: [
      { reference: "bullets",
        levels: [
          { level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
          { level: 1, format: LevelFormat.BULLET, text: "\u25E6", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 1080, hanging: 360 } } } }
        ] },
      { reference: "numbers",
        levels: [
          { level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
          { level: 1, format: LevelFormat.LOWER_LETTER, text: "%2.", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 1080, hanging: 360 } } } }
        ] }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: "Lectec PEV AI Curriculum - Module 1", size: 18, color: GRAY, font: "Arial" })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Page ", size: 18, color: GRAY, font: "Arial" }),
            new TextRun({ children: [PageNumber.CURRENT], size: 18, color: GRAY, font: "Arial" })
          ]
        })]
      })
    },
    children: [
      // ========== TITLE PAGE ==========
      new Paragraph({ spacing: { before: 2000 }, children: [] }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "MODULE 1", size: 32, color: GRAY, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 200, after: 200 },
        children: [new TextRun({ text: "Welcome to Your PEV Brain", bold: true, size: 72, color: LECTEC_BLUE, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 400 },
        children: [new TextRun({ text: "Introduction to CAN Bus Communication & Jupyter Notebooks", size: 28, color: GRAY, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 200 },
        children: [new TextRun({ text: "Lectec PEV AI Curriculum", size: 24, color: LECTEC_BLACK, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "Day 1 of 14", size: 24, color: GRAY, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 600 },
        children: [new TextRun({ text: "Complete Slide & Notebook Guide", bold: true, size: 28, color: LECTEC_YELLOW, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 100 },
        children: [new TextRun({ text: "Integrated Slides + Jupyter Notebook Activities", size: 22, color: GRAY, font: "Arial" })]
      }),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== TABLE OF CONTENTS ==========
      heading1("Table of Contents"),
      spacer(),
      para("Part 1: Slide Content Specifications", { bold: true, size: 24 }),
      bulletItem("Slides 1-3: Opening & Hook (Start with the End in Mind)"),
      bulletItem("Slides 4-6: Learning Objectives & Hardware Introduction"),
      bulletItem("Slides 7-9: What is CAN Bus & System Architecture"),
      bulletItem("Slides 10-12: Introduction to Jupyter Notebooks"),
      bulletItem("Slides 13-15: What is an API & The Student API"),
      bulletItem("Slides 16-18: Hands-On - Reading Voltage & RPM"),
      bulletItem("Slides 19-21: Fill-in-the-Blank Exercises & Summary"),
      spacer(),
      para("Part 2: Jupyter Notebook Specifications", { bold: true, size: 24 }),
      bulletItem("Section A: Jupyter Basics (Run, Stop, Restart)"),
      bulletItem("Section B: Practice Code Cells (Non-VESC Examples)"),
      bulletItem("Section C: Connecting to the VESC"),
      bulletItem("Section D: Reading Telemetry Data"),
      bulletItem("Section E: Fill-in-the-Blank Challenges"),
      bulletItem("Section F: Matching Exercise"),
      spacer(),
      para("Part 3: Teacher Notes & Timing", { bold: true, size: 24 }),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== PART 1: SLIDE CONTENT ==========
      heading1("Part 1: Slide Content Specifications"),
      para("This section provides exact text, bullets, headings, and visual descriptions for each slide. Green callout boxes indicate when students should switch to their Jupyter notebooks."),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 1 ==========
      ...slideHeader(1, "Title Slide"),

      heading3("Visual Design"),
      bulletItem("Full-slide gradient background: Dark Blue (#1976D2) to Lectec Blue (#2196F3)"),
      bulletItem("Yellow accent bar at top (8px height)"),
      bulletItem("Centered content layout"),

      heading3("Text Content"),
      heading4("Small Text (Top Center)"),
      para("MODULE 1", { italics: true }),

      heading4("Main Title (Large, Centered)"),
      para("Welcome to Your PEV Brain", { bold: true, size: 28 }),

      heading4("Subtitle"),
      para("Introduction to CAN Bus Communication"),

      heading4("Decorative Element"),
      para("Yellow horizontal line (120px wide, 4px tall) centered below subtitle"),

      heading4("Bottom Text"),
      para("Lectec PEV AI Curriculum"),
      para("Day 1 of 14 (bottom right corner)"),

      heading3("Speaker Notes"),
      bulletItem("Welcome students and introduce yourself"),
      bulletItem("Set expectations: This is a hands-on coding course"),
      bulletItem("Mention: By the end of 14 days, they will have built a real safety system"),
      bulletItem("Key phrase: 'Your PEV is about to get a brain - and you're going to program it!'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 2 ==========
      ...slideHeader(2, "The Hook - What If Your PEV Could Think?"),

      heading3("Visual Design"),
      bulletItem("White background with blue header bar"),
      bulletItem("Two-column layout: Left = image placeholder, Right = text content"),
      bulletItem("Yellow callout box at bottom"),

      heading3("Header Text"),
      para("What If Your PEV Could Think?", { bold: true, size: 28 }),

      heading3("Body Content"),
      heading4("Opening Statement"),
      para("Imagine riding down the street and your PEV automatically:"),

      heading4("Bullet Points (with icons)"),
      bulletItem("Spots a pedestrian stepping into your path"),
      bulletItem("Warns you with a beep before you even see them"),
      bulletItem("Logs the near-miss for your safety review"),

      heading4("Yellow Callout Box"),
      para("By Day 14, YOU will build this system!", { bold: true }),

      heading3("Image Placeholder"),
      para("[Left side: Futuristic PEV with glowing neural network overlay - Nano Banana prompt included in appendix]", { italics: true, color: GRAY }),

      heading3("Speaker Notes"),
      bulletItem("This is the 'Start with the End in Mind' moment - show them the exciting destination"),
      bulletItem("Ask: 'How many of you have almost hit something or been hit while riding?'"),
      bulletItem("Explain: 'What if your PEV could see danger before you do?'"),
      bulletItem("Key phrase: 'This isn't science fiction - this is what you're going to build'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 3 ==========
      ...slideHeader(3, "This Tech Powers Real Vehicles"),

      heading3("Visual Design"),
      bulletItem("White background with blue header bar"),
      bulletItem("Three equal-width cards in a row"),
      bulletItem("Third card (Your PEV) highlighted in yellow"),

      heading3("Header Text"),
      para("This Tech Powers Real Vehicles", { bold: true, size: 28 }),

      heading3("Card 1: Tesla Autopilot"),
      para("Background: Light blue (#E3F2FD)"),
      para("Image: [Tesla interior with Autopilot display]"),
      para("Title: Tesla Autopilot", { bold: true }),
      para("Description: Uses CAN bus to read 8 cameras, 12 ultrasonic sensors, and control steering"),

      heading3("Card 2: Waymo Robotaxi"),
      para("Background: Light blue (#E3F2FD)"),
      para("Image: [Waymo self-driving taxi on street]"),
      para("Title: Waymo Robotaxi", { bold: true }),
      para("Description: Fully autonomous vehicles using the same CAN protocol you'll learn today"),

      heading3("Card 3: Your Lectec PEV (Highlighted)"),
      para("Background: Lectec Yellow (#FFCA28)"),
      para("Image: [Lectec PEV with Raspberry Pi visible]"),
      para("Title: Your Lectec PEV", { bold: true }),
      para("Description: Same technology, your hands, real learning - starting today!"),

      heading3("Speaker Notes"),
      bulletItem("Build credibility - this isn't toy technology"),
      bulletItem("CAN bus was invented in 1986 by Bosch for Mercedes-Benz"),
      bulletItem("Now used in EVERY modern car, truck, boat, and plane"),
      bulletItem("Key phrase: 'You're learning industry-standard skills that engineers at Tesla use every day'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 4 ==========
      ...slideHeader(4, "Today's Mission - Learning Objectives"),

      heading3("Visual Design"),
      bulletItem("White background with blue header bar"),
      bulletItem("Numbered objectives with circular number badges"),
      bulletItem("First 3 badges: Blue, Fourth badge: Yellow (highlight)"),

      heading3("Header Text"),
      para("Today's Mission", { bold: true, size: 28 }),
      para("What you'll accomplish in this module", { italics: true }),

      heading3("Objectives List"),

      heading4("Objective 1 (Blue badge)"),
      para("Main text: Explain what CAN bus is", { bold: true }),
      para("Subtext: Understand the 'nervous system' of your PEV"),

      heading4("Objective 2 (Blue badge)"),
      para("Main text: Identify the three main hardware components", { bold: true }),
      para("Subtext: Raspberry Pi Zero 2W, VESC Controller, AI Camera"),

      heading4("Objective 3 (Blue badge)"),
      para("Main text: Learn to use Jupyter Notebooks", { bold: true }),
      para("Subtext: Run code, stop code, and understand cells"),

      heading4("Objective 4 (Yellow badge - highlight)"),
      para("Main text: Read real data from your PEV using Python", { bold: true }),
      para("Subtext: Voltage, RPM, temperature - live and instant!"),

      heading3("Speaker Notes"),
      bulletItem("These are measurable outcomes - students should be able to do ALL of these by end of class"),
      bulletItem("Emphasize #4 as the exciting hands-on goal"),
      bulletItem("Key phrase: 'By the end of today, you will have talked to your PEV and it will have talked back'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 5 ==========
      ...slideHeader(5, "Your PEV Has a Nervous System"),

      heading3("Visual Design"),
      bulletItem("White background with blue header"),
      bulletItem("Two-column comparison layout"),
      bulletItem("Left column: Light blue background (Human Body)"),
      bulletItem("Right column: Yellow background (Your PEV)"),
      bulletItem("Large '=' sign between columns"),

      heading3("Header Text"),
      para("Your PEV Has a Nervous System", { bold: true, size: 28 }),

      heading3("Left Column: Human Body"),
      para("Title: Human Body", { bold: true }),
      para("Image placeholder: [Simple human nervous system diagram]"),
      bulletItem("Brain = Processes information"),
      bulletItem("Nerves = Carry signals"),
      bulletItem("Eyes = See the world"),
      bulletItem("Muscles = Take action"),

      heading3("Center"),
      para("Large '=' sign in yellow", { bold: true }),

      heading3("Right Column: Your PEV"),
      para("Title: Your PEV", { bold: true }),
      para("Image placeholder: [PEV system diagram with components labeled]"),
      bulletItem("Raspberry Pi = The brain"),
      bulletItem("CAN Bus = The nerves"),
      bulletItem("AI Camera = The eyes"),
      bulletItem("VESC Motor = The muscles"),

      heading3("Speaker Notes"),
      bulletItem("This analogy helps students understand the system architecture"),
      bulletItem("Ask: 'What happens if you cut a nerve in your body?' (Signal can't get through)"),
      bulletItem("Same thing happens if CAN bus wire is disconnected!"),
      bulletItem("Key phrase: 'Just like your brain controls your body through nerves, the Pi controls your PEV through CAN bus'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 6 ==========
      ...slideHeader(6, "Meet Your Hardware Team"),

      heading3("Visual Design"),
      bulletItem("White background with blue header"),
      bulletItem("Three vertical cards side by side"),
      bulletItem("Each card has colored header bar, image area, title, and bullet specs"),

      heading3("Header Text"),
      para("Meet Your Hardware Team", { bold: true, size: 28 }),

      heading3("Card 1: THE BRAIN"),
      para("Header bar: Lectec Blue (#2196F3)"),
      para("Header text: THE BRAIN"),
      para("Image: [Photo of Raspberry Pi Zero 2W]"),
      para("Title: Raspberry Pi Zero 2W", { bold: true }),
      para("Specifications:"),
      bulletItem("1GHz quad-core processor"),
      bulletItem("512MB RAM"),
      bulletItem("Runs Python code"),
      bulletItem("WiFi built-in"),

      heading3("Card 2: THE MUSCLES"),
      para("Header bar: Dark Blue (#1976D2)"),
      para("Header text: THE MUSCLES"),
      para("Image: [Photo of VESC motor controller]"),
      para("Title: VESC Motor Controller", { bold: true }),
      para("Specifications:"),
      bulletItem("Controls motor speed"),
      bulletItem("Reports RPM, voltage, temp"),
      bulletItem("CAN bus interface"),
      bulletItem("Real-time telemetry"),

      heading3("Card 3: THE EYES"),
      para("Header bar: Warning Orange (#FF9800)"),
      para("Card background: Yellow (#FFCA28)"),
      para("Header text: THE EYES"),
      para("Image: [Photo of Sony IMX500 AI Camera]"),
      para("Title: Sony IMX500 AI Camera", { bold: true }),
      para("Specifications:"),
      bulletItem("AI built INTO the chip!"),
      bulletItem("Detects 80 object types"),
      bulletItem("30 FPS processing"),
      bulletItem("Low power consumption"),

      heading3("Speaker Notes"),
      bulletItem("Physical show-and-tell moment - hold up each component if available"),
      bulletItem("Point out: The AI camera is special because it processes AI ON the chip, not in the cloud"),
      bulletItem("Ask: 'Why might processing AI on the chip be better than sending to the cloud?' (Speed, privacy, no internet needed)"),
      bulletItem("Key phrase: 'These three work together as a team - brain, muscles, and eyes'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 7 ==========
      ...slideHeader(7, "What is CAN Bus?"),

      heading3("Visual Design"),
      bulletItem("White background with blue header"),
      bulletItem("Two-column layout"),
      bulletItem("Left: Three stacked info boxes"),
      bulletItem("Right: Diagram area with light blue background"),

      heading3("Header Text"),
      para("CAN Bus: Controller Area Network", { bold: true, size: 28 }),
      para("The universal language of vehicles", { italics: true }),

      heading3("Left Column: Key Facts"),

      heading4("Info Box 1 (Gray background)"),
      para("Title: Invented in 1986 by Bosch", { bold: true, color: LECTEC_BLUE }),
      para("Subtext: Originally for cars, now everywhere"),

      heading4("Info Box 2 (Gray background)"),
      para("Title: Used in every modern vehicle", { bold: true, color: LECTEC_BLUE }),
      para("Subtext: Cars, trucks, tractors, boats, planes"),

      heading4("Info Box 3 (Yellow background - highlight)"),
      para("Title: Why it matters for YOU", { bold: true }),
      para("Subtext: Industry-standard skill, real job applications"),

      heading3("Right Column: How It Works Diagram"),
      para("Light blue background box"),
      para("Title: How CAN Bus Works", { bold: true }),
      para("[Diagram showing: Two parallel wires with multiple devices connected]"),
      bulletItem("Two wires: CAN High + CAN Low"),
      bulletItem("All devices share one 'conversation'"),
      bulletItem("Messages have IDs for routing"),

      heading3("Speaker Notes"),
      bulletItem("Draw the two-wire bus on the board if possible"),
      bulletItem("Analogy: 'It's like a group chat where everyone can see all messages, but you only respond to ones with your name'"),
      bulletItem("The message ID is like having your name mentioned in the group chat"),
      bulletItem("Key phrase: 'Two wires, infinite possibilities - that's the beauty of CAN bus'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 8 ==========
      ...slideHeader(8, "How It All Connects"),

      heading3("Visual Design"),
      bulletItem("White background with blue header"),
      bulletItem("Large diagram area with light gray background"),
      bulletItem("System architecture showing connections between components"),

      heading3("Header Text"),
      para("How It All Connects", { bold: true, size: 28 }),
      para("Your PEV's complete nervous system", { italics: true }),

      heading3("Diagram Components"),

      heading4("Top Row"),
      para("Blue rounded box: Raspberry Pi Zero 2W"),
      para("Yellow rounded box: IMX500 AI Camera"),
      para("Blue line connecting them labeled: CSI Cable"),

      heading4("Middle"),
      para("Large green rounded rectangle spanning width"),
      para("Label: CAN BUS (2-Wire Network)"),
      para("Vertical line from Pi down to CAN bus"),

      heading4("Bottom"),
      para("Dark blue rounded box: VESC Motor Controller"),
      para("Vertical line up to CAN bus"),
      para("Label below VESC: Speed, RPM, Voltage, Temp"),

      heading3("Speaker Notes"),
      bulletItem("Walk through the data flow: 'When you ask for the battery voltage...'"),
      bulletItem("Pi sends request over CAN bus → VESC receives → VESC responds → Pi displays"),
      bulletItem("Camera connects directly to Pi via ribbon cable (CSI), not CAN"),
      bulletItem("Key phrase: 'This is the nervous system - the Pi is the brain, CAN bus is the nerve, VESC reports the data'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 9 ==========
      ...slideHeader(9, "Safety First!"),

      heading3("Visual Design"),
      bulletItem("White background with orange header bar (#FF9800)"),
      bulletItem("Two-column layout with 6 safety rules"),
      bulletItem("Each rule has a colored left border indicating severity"),

      heading3("Header Text"),
      para("Safety Rules", { bold: true, size: 28 }),
      para("Essential guidelines for working with your PEV", { italics: true }),

      heading3("Safety Rules (2 columns, 3 rules each)"),

      heading4("Rule 1: Red border (DANGER)"),
      para("Title: NEVER ride during coding", { bold: true, color: DANGER_RED }),
      para("Description: PEV must be on a stand or stationary when running code"),

      heading4("Rule 2: Orange border (WARNING)"),
      para("Title: Check battery before starting", { bold: true, color: WARNING_ORANGE }),
      para("Description: Ensure battery is above 20% before lab work"),

      heading4("Rule 3: Orange border (WARNING)"),
      para("Title: Don't touch hot components", { bold: true, color: WARNING_ORANGE }),
      para("Description: Motor and controller get warm during operation"),

      heading4("Rule 4: Green border (GOOD PRACTICE)"),
      para("Title: Always call stop() when done", { bold: true, color: SUCCESS_GREEN }),
      para("Description: Clean shutdown protects your hardware"),

      heading4("Rule 5: Blue border (INFO)"),
      para("Title: Ask before motor commands", { bold: true, color: LECTEC_BLUE }),
      para("Description: Reading data is safe, moving motors needs teacher approval"),

      heading4("Rule 6: Blue border (INFO)"),
      para("Title: Report any strange behavior", { bold: true, color: LECTEC_BLUE }),
      para("Description: Weird sounds, smells, or errors? Tell your teacher immediately"),

      heading3("Bottom Callout (Orange background)"),
      para("Safety first = more fun with code later!", { bold: true }),

      heading3("Speaker Notes"),
      bulletItem("Go through each rule and explain WHY it matters"),
      bulletItem("Rule 1 is most critical - someone could get hurt"),
      bulletItem("Ask students to repeat back the first rule"),
      bulletItem("Key phrase: 'The VESC can make the motor spin really fast - we need to be careful'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 10 ==========
      ...slideHeader(10, "Introduction to Jupyter Notebooks"),

      heading3("Visual Design"),
      bulletItem("White background with blue header"),
      bulletItem("Screenshot or illustration of Jupyter interface"),
      bulletItem("Callout boxes explaining interface elements"),

      heading3("Header Text"),
      para("What is a Jupyter Notebook?", { bold: true, size: 28 }),
      para("Your interactive coding environment", { italics: true }),

      heading3("Key Points"),
      para("A Jupyter Notebook is like a smart document where you can:", { bold: true }),
      bulletItem("Write and run Python code"),
      bulletItem("See results immediately below your code"),
      bulletItem("Add notes and explanations"),
      bulletItem("Save your work and come back later"),

      heading3("Interface Elements to Highlight"),
      bulletItem("Cells = Individual boxes of code or text"),
      bulletItem("Run button = Play button that executes code"),
      bulletItem("Stop button = Square that stops running code"),
      bulletItem("Output area = Where results appear"),

      heading3("Analogy Box"),
      para("Think of it like a recipe book where you can actually cook each step and see the result!", { italics: true }),

      spacer(),
      notebookCallout("Open your Jupyter Notebook now! Your teacher will show you how to access it. Find the file called 'Module_01_PEV_Brain.ipynb'"),

      heading3("Speaker Notes"),
      bulletItem("Have all students open Jupyter before continuing"),
      bulletItem("Wait until everyone has the notebook open"),
      bulletItem("Walk around to help anyone having trouble"),
      bulletItem("Key phrase: 'Jupyter lets you experiment with code - if something doesn't work, just try again!'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 11 ==========
      ...slideHeader(11, "How to Run a Cell"),

      heading3("Visual Design"),
      bulletItem("White background with blue header"),
      bulletItem("Step-by-step visual guide with numbered screenshots"),

      heading3("Header Text"),
      para("Running Code in Jupyter", { bold: true, size: 28 }),

      heading3("Step-by-Step Instructions"),

      heading4("Step 1: Click on a cell"),
      para("The cell will get a blue or green border when selected"),

      heading4("Step 2: Run the cell using ONE of these methods:"),
      bulletItem("Click the Run button (play triangle) in the toolbar"),
      bulletItem("Press Shift + Enter on your keyboard"),
      bulletItem("Press Ctrl + Enter (runs but stays on same cell)"),

      heading4("Step 3: Watch for the output"),
      para("Results appear directly below the cell"),
      para("The [ ] next to the cell shows [*] while running, then [1], [2], etc. when done"),

      heading3("Visual: Show a simple cell before and after running"),
      para("Before: print('Hello PEV!')"),
      para("After: Shows 'Hello PEV!' below the cell"),

      spacer(),
      notebookCallout("Go to Section A, Cell 1 in your notebook. Click on it and press Shift+Enter. You should see 'Welcome to Jupyter!' appear below."),

      heading3("Speaker Notes"),
      bulletItem("Demo this live while students follow along"),
      bulletItem("Walk around and verify everyone sees the output"),
      bulletItem("Common issue: Students hit Enter instead of Shift+Enter (just makes new line)"),
      bulletItem("Key phrase: 'Shift+Enter is your new best friend - you'll use it hundreds of times today!'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 12 ==========
      ...slideHeader(12, "How to Stop Running Code"),

      heading3("Visual Design"),
      bulletItem("White background with orange header (warning context)"),
      bulletItem("Clear visual of stop button location"),
      bulletItem("Code example that runs forever"),

      heading3("Header Text"),
      para("Stopping Code That Won't Stop", { bold: true, size: 28 }),
      para("Sometimes code runs forever - here's how to stop it!", { italics: true }),

      heading3("Why Code Might Run Forever"),
      bulletItem("Loops that never end (while True:)"),
      bulletItem("Waiting for something that never happens"),
      bulletItem("Accidentally created infinite loop"),

      heading3("How to Stop"),
      para("Method 1: Click the Stop button (black square) in the toolbar", { bold: true }),
      para("Method 2: Press the 'I' key twice quickly (I, I)", { bold: true }),
      para("Method 3: Go to Kernel → Interrupt (menu bar)", { bold: true }),

      heading3("Signs Your Code is Still Running"),
      bulletItem("The cell shows [*] instead of a number"),
      bulletItem("You can't run other cells"),
      bulletItem("The circle in the top right is filled (busy)"),

      spacer(),
      notebookCallout("Go to Section A, Cell 2 in your notebook. This cell counts forever! Run it, watch it count for a few seconds, then STOP it using the Stop button. Try it!"),

      heading3("Speaker Notes"),
      bulletItem("This is a critical skill - students will need this when they make mistakes"),
      bulletItem("Let them see the counting for 5-10 seconds before stopping"),
      bulletItem("Celebrate when they successfully stop it!"),
      bulletItem("Key phrase: 'The stop button is your emergency brake - always know where it is'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 13 ==========
      ...slideHeader(13, "What is an API?"),

      heading3("Visual Design"),
      bulletItem("White background with blue header"),
      bulletItem("Restaurant analogy visual"),
      bulletItem("Diagram showing: You → Waiter → Kitchen → Waiter → You"),

      heading3("Header Text"),
      para("What is an API?", { bold: true, size: 28 }),
      para("Application Programming Interface", { italics: true }),

      heading3("The Restaurant Analogy"),
      para("Imagine you're at a restaurant:", { bold: true }),

      bulletItem("You (the customer) = Your Python code"),
      bulletItem("The Waiter = The API"),
      bulletItem("The Kitchen = The VESC motor controller"),
      bulletItem("The Menu = Available functions you can call"),

      heading3("How It Works"),
      numberedItem("You look at the menu and tell the waiter what you want"),
      numberedItem("The waiter goes to the kitchen and places your order"),
      numberedItem("The kitchen prepares your food"),
      numberedItem("The waiter brings it back to you"),

      heading3("In Code Terms"),
      para("You don't need to know HOW the kitchen makes the food."),
      para("You just need to know WHAT to ask for!"),

      spacer(),
      calloutBox("KEY INSIGHT", "An API is a 'menu' of commands. You pick what you want, and the API handles all the complicated stuff behind the scenes.", LECTEC_BLUE),

      heading3("Speaker Notes"),
      bulletItem("This analogy really resonates with students"),
      bulletItem("Ask: 'Do you need to know how to cook to order food?' (No!)"),
      bulletItem("Same with APIs - you don't need to know CAN bus protocols to read voltage"),
      bulletItem("Key phrase: 'The API is your menu - just pick what data you want!'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 14 ==========
      ...slideHeader(14, "The VESCStudentAPI"),

      heading3("Visual Design"),
      bulletItem("White background with blue header"),
      bulletItem("Three category boxes showing API functions"),
      bulletItem("Color-coded by function type"),

      heading3("Header Text"),
      para("Meet Your API: VESCStudentAPI", { bold: true, size: 28 }),
      para("Your menu of commands for talking to the VESC", { italics: true }),

      heading3("Category 1: Read Functions (Blue box)"),
      para("Get information FROM the VESC", { bold: true }),
      bulletItem("get_input_voltage() - Battery voltage"),
      bulletItem("get_rpm() - Motor speed"),
      bulletItem("get_motor_current() - Electricity to motor"),
      bulletItem("get_fet_temperature() - Controller temp"),
      bulletItem("get_motor_temperature() - Motor temp"),
      bulletItem("...and more!"),

      heading3("Category 2: Control Functions (Orange box)"),
      para("Send commands TO the VESC (Teacher approval required!)", { bold: true }),
      bulletItem("set_duty_cycle() - Control motor speed"),
      bulletItem("set_current() - Control motor torque"),
      bulletItem("set_brake_current() - Apply brakes"),

      heading3("Category 3: System Functions (Green box)"),
      para("Manage the connection", { bold: true }),
      bulletItem("start() - Connect to the VESC"),
      bulletItem("stop() - Disconnect safely"),
      bulletItem("is_connected() - Check if working"),

      heading3("Speaker Notes"),
      bulletItem("Today we focus on READ functions - safe and instant"),
      bulletItem("Control functions come in later modules with safety precautions"),
      bulletItem("Key phrase: 'Today we're going to READ data - this is completely safe, we're just asking questions'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 15 ==========
      ...slideHeader(15, "Connecting to Your PEV"),

      heading3("Visual Design"),
      bulletItem("White background with blue header"),
      bulletItem("Code block showing connection code"),
      bulletItem("Expected output shown below"),

      heading3("Header Text"),
      para("Let's Connect to the VESC!", { bold: true, size: 28 }),

      heading3("The Connection Code"),
      codeBlock("from student_api import VESCStudentAPI\n\nvesc_api = VESCStudentAPI()\nvesc_api.start()\n\nvesc = vesc_api.get_controller(74)"),

      heading3("Line-by-Line Explanation"),
      bulletItem("Line 1: Import the API (get the menu ready)"),
      bulletItem("Line 3: Create our API helper"),
      bulletItem("Line 4: Start the connection (walk into the restaurant)"),
      bulletItem("Line 6: Get access to controller #74 (our specific VESC)"),

      heading3("Expected Output"),
      para("✅ Connected to VESC controller! Battery: XX.X V", { color: SUCCESS_GREEN }),

      heading3("If You See an Error"),
      para("❌ VESC controller not found or not responding!", { color: DANGER_RED }),
      para("This means: Check that the PEV is powered ON and the cable is connected"),

      spacer(),
      notebookCallout("Go to Section C in your notebook. Run the connection cell. Raise your hand when you see the green checkmark and battery voltage!"),

      heading3("Speaker Notes"),
      bulletItem("This is a big moment - first time talking to the PEV!"),
      bulletItem("Walk around and verify everyone gets connected"),
      bulletItem("Troubleshoot: Power on? Cables connected? Right notebook?"),
      bulletItem("Key phrase: 'You just said hello to your PEV, and it said hello back with its battery voltage!'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 16 ==========
      ...slideHeader(16, "Reading Battery Voltage"),

      heading3("Visual Design"),
      bulletItem("White background with blue header"),
      bulletItem("Code block with explanation"),
      bulletItem("Voltage interpretation guide"),

      heading3("Header Text"),
      para("Your First Data Read: Battery Voltage", { bold: true, size: 28 }),

      heading3("The Code"),
      codeBlock("voltage = vesc.get_input_voltage()\nprint(f\"Battery Voltage: {voltage} V\")"),

      heading3("What This Does"),
      numberedItem("Asks the VESC: 'What's the battery voltage right now?'"),
      numberedItem("VESC responds over CAN bus with the number"),
      numberedItem("We store it in a variable called 'voltage'"),
      numberedItem("We display it using print()"),

      heading3("Understanding the Reading"),
      para("Voltage Interpretation Guide:", { bold: true }),
      bulletItem("36V+ = Fully charged (10S battery)"),
      bulletItem("33-36V = Good charge remaining"),
      bulletItem("30-33V = Getting low, consider charging"),
      bulletItem("Below 30V = Low battery warning!"),

      spacer(),
      notebookCallout("Now it's YOUR turn! In Section D, Cell 1, write your own code to read the voltage. Fill in the blank: voltage = vesc.________() Then print it out!"),

      heading3("Speaker Notes"),
      bulletItem("Students write their own code here - not just running pre-written code"),
      bulletItem("The blank is: get_input_voltage"),
      bulletItem("Walk around and check their work"),
      bulletItem("Key phrase: 'You just asked your PEV a question and got a real answer - that's programming!'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 17 ==========
      ...slideHeader(17, "Reading Motor RPM - Part 1"),

      heading3("Visual Design"),
      bulletItem("White background with blue header"),
      bulletItem("Two states shown: Motor stopped vs Motor spinning"),

      heading3("Header Text"),
      para("Reading Motor Speed (RPM)", { bold: true, size: 28 }),
      para("RPM = Revolutions Per Minute", { italics: true }),

      heading3("The Code"),
      codeBlock("rpm = vesc.get_rpm()\nprint(f\"Motor RPM: {rpm}\")"),

      heading3("What to Expect"),

      heading4("When motor is NOT spinning:"),
      para("Output: Motor RPM: 0"),
      para("This is normal! No movement = 0 RPM"),

      heading4("When motor IS spinning:"),
      para("Output: Motor RPM: 2847 (or some other number)"),
      para("Positive = Forward direction"),
      para("Negative = Reverse direction"),

      heading3("Key Point"),
      calloutBox("REAL-TIME DATA", "The RPM reading is INSTANT - it shows what's happening RIGHT NOW. Every time you run the code, you get the current value.", LECTEC_BLUE),

      spacer(),
      notebookCallout("In Section D, Cell 2, run the RPM code with the motor NOT spinning. Write down what you see: ______ RPM"),

      heading3("Speaker Notes"),
      bulletItem("First reading will be 0 - that's expected!"),
      bulletItem("We'll prove it's real-time in the next slide"),
      bulletItem("Key phrase: 'Zero RPM makes sense - the motor isn't moving!'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 18 ==========
      ...slideHeader(18, "Reading Motor RPM - Part 2 (The Proof!)"),

      heading3("Visual Design"),
      bulletItem("White background with green header (activity)"),
      bulletItem("Before/After comparison"),
      bulletItem("Hand-spinning illustration"),

      heading3("Header Text"),
      para("Proving It's Real-Time!", { bold: true, size: 28 }),
      para("Let's see the data change instantly", { italics: true }),

      heading3("The Experiment"),

      heading4("Step 1: Run the code with motor stopped"),
      para("Expected result: 0 RPM"),
      para("Write it down: ______ RPM"),

      heading4("Step 2: Gently spin the wheel BY HAND"),
      para("Keep it spinning slowly and safely"),

      heading4("Step 3: While spinning, run the code AGAIN"),
      para("Expected result: A number OTHER than 0!"),
      para("Write it down: ______ RPM"),

      heading3("What This Proves"),
      para("The code reads what's happening RIGHT NOW!", { bold: true }),
      para("This is called REAL-TIME DATA - instant feedback from your PEV."),

      spacer(),
      notebookCallout("Time for the experiment! Run the RPM cell, write down the number. Then GENTLY spin the wheel by hand and run it AGAIN while it's spinning. Write both numbers in your notebook!"),

      heading3("Speaker Notes"),
      bulletItem("This is an 'aha!' moment - data is live!"),
      bulletItem("Supervise the wheel spinning - gentle and safe"),
      bulletItem("Students should see different numbers"),
      bulletItem("Key phrase: 'See how it changed? That's real data from your real PEV, right now!'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 19 ==========
      ...slideHeader(19, "Fill-in-the-Blank Challenge: Temperature"),

      heading3("Visual Design"),
      bulletItem("White background with blue header"),
      bulletItem("Code block with blanks"),
      bulletItem("Hint section"),

      heading3("Header Text"),
      para("Your Turn: Read the Temperature!", { bold: true, size: 28 }),

      heading3("The Challenge"),
      para("Fill in the blanks to read the controller (FET) temperature:"),

      codeBlock("temp = vesc.get_____temperature()\nprint(f\"Controller Temperature: {____} °C\")"),

      heading3("Hints"),
      bulletItem("Hint 1: The FET is the electronic part of the controller"),
      bulletItem("Hint 2: Look at the API list from earlier - what function reads FET temp?"),
      bulletItem("Hint 3: The second blank should be the variable name"),

      heading3("Answer Check"),
      para("Your output should look like: Controller Temperature: XX.X °C"),
      para("Normal reading: 20-50°C when idle"),

      spacer(),
      notebookCallout("Go to Section E, Cell 1 in your notebook. Fill in the blanks and run the code. Write down the temperature you get: ______ °C"),

      heading3("Speaker Notes"),
      bulletItem("Give students 2-3 minutes to try"),
      bulletItem("Answer: get_fet_temperature() and temp"),
      bulletItem("Walk around and help those who are stuck"),
      bulletItem("Key phrase: 'You're not just running code anymore - you're WRITING code!'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 20 ==========
      ...slideHeader(20, "Matching Challenge: Components and Functions"),

      heading3("Visual Design"),
      bulletItem("White background with blue header"),
      bulletItem("Two-column matching exercise"),
      bulletItem("Can be done verbally as class or in notebook"),

      heading3("Header Text"),
      para("Match the Component to the Function!", { bold: true, size: 28 }),

      heading3("Left Column: What do you want to know?"),
      numberedItem("How fast is the motor spinning?"),
      numberedItem("How much battery do I have?"),
      numberedItem("Is the controller getting hot?"),
      numberedItem("How much electricity is the motor using?"),
      numberedItem("How hot is the motor itself?"),

      heading3("Right Column: Which function to use?"),
      para("A. get_motor_temperature()"),
      para("B. get_rpm()"),
      para("C. get_input_voltage()"),
      para("D. get_motor_current()"),
      para("E. get_fet_temperature()"),

      heading3("Answers (Teacher Reference)"),
      para("1-B, 2-C, 3-E, 4-D, 5-A"),

      spacer(),
      notebookCallout("Complete the matching exercise in Section F of your notebook. Then run the 'check answers' cell to see if you got them right!"),

      heading3("Speaker Notes"),
      bulletItem("Can do this as a class verbally before notebook"),
      bulletItem("Call on students to share their answers"),
      bulletItem("Discuss why each match makes sense"),
      bulletItem("Key phrase: 'Now you know which question to ask to get the answer you need!'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 21 ==========
      ...slideHeader(21, "What You Learned Today - Summary"),

      heading3("Visual Design"),
      bulletItem("White background with blue header"),
      bulletItem("Checklist format with green checkmarks"),
      bulletItem("Key terms sidebar"),

      heading3("Header Text"),
      para("What You Learned Today", { bold: true, size: 28 }),

      heading3("Achievement Checklist"),
      bulletItem("✅ CAN bus is the 'nervous system' of vehicles"),
      bulletItem("✅ Three components: Pi (brain), VESC (muscles), Camera (eyes)"),
      bulletItem("✅ How to use Jupyter Notebooks (run, stop, restart)"),
      bulletItem("✅ What an API is and why we use one"),
      bulletItem("✅ Connected to your PEV with Python"),
      bulletItem("✅ Read real voltage, RPM, and temperature data"),
      bulletItem("✅ Proved that the data is REAL-TIME"),

      heading3("Key Terms Sidebar"),
      para("CAN Bus", { bold: true }),
      para("Controller Area Network - the two-wire communication system", { size: 20 }),
      spacer(),
      para("VESC", { bold: true }),
      para("Motor speed controller that reports telemetry", { size: 20 }),
      spacer(),
      para("API", { bold: true }),
      para("Application Programming Interface - your 'menu' of commands", { size: 20 }),
      spacer(),
      para("Telemetry", { bold: true }),
      para("Data sent from the VESC (voltage, RPM, temp, etc.)", { size: 20 }),
      spacer(),
      para("Real-Time", { bold: true }),
      para("Data that reflects what's happening RIGHT NOW", { size: 20 }),

      heading3("Speaker Notes"),
      bulletItem("Review each item and ask students to explain"),
      bulletItem("Celebrate their accomplishments!"),
      bulletItem("Key phrase: 'You talked to your PEV today, and it talked back. That's real engineering!'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 22 ==========
      ...slideHeader(22, "Coming Up Next - Module 2"),

      heading3("Visual Design"),
      bulletItem("Blue gradient background (like title slide)"),
      bulletItem("Preview of next module"),
      bulletItem("Yellow accent bar at bottom"),

      heading3("Small Text (Top)"),
      para("COMING UP IN MODULE 2"),

      heading3("Main Title"),
      para("Building a Live Dashboard", { bold: true, size: 36 }),

      heading3("Subtitle"),
      para("Real-time data visualization with continuous updates"),

      heading3("Preview Boxes"),
      bulletItem("Continuous monitoring loops"),
      bulletItem("Updating displays"),
      bulletItem("Data logging"),

      heading3("Bottom Encouragement"),
      para("Great job today!", { bold: true, color: LECTEC_YELLOW }),
      para("You've taken your first step into vehicle communication"),

      heading3("Speaker Notes"),
      bulletItem("Build excitement for the next session"),
      bulletItem("Mention: Tomorrow we'll make the data update automatically"),
      bulletItem("Thank students for their focus and participation"),
      bulletItem("Key phrase: 'Today you asked single questions. Tomorrow, you'll have a continuous conversation!'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== PART 2: JUPYTER NOTEBOOK SPECIFICATIONS ==========
      heading1("Part 2: Jupyter Notebook Specifications"),
      para("This section provides the complete cell-by-cell content for the Module 1 Jupyter Notebook."),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SECTION A ==========
      heading2("Section A: Jupyter Basics"),
      para("Purpose: Teach students how to use Jupyter before introducing VESC content"),

      heading3("Cell A.1 - Welcome Message (Markdown)"),
      para("Type: Markdown"),
      para("Content:"),
      codeBlock("# Welcome to Jupyter Notebooks!\n\nThis is your interactive coding environment. Let's learn how to use it!"),

      heading3("Cell A.2 - First Code Cell"),
      para("Type: Code"),
      para("Purpose: Test that they can run a cell"),
      codeBlock("# Your first code cell!\n# Click on this cell, then press Shift+Enter to run it\n\nprint(\"Welcome to Jupyter!\")\nprint(\"If you can see this, you ran the cell successfully!\")"),
      para("Expected output: Welcome to Jupyter! / If you can see this, you ran the cell successfully!"),

      heading3("Cell A.3 - Counting Forever (For Stop Practice)"),
      para("Type: Code"),
      para("Purpose: Practice stopping code"),
      codeBlock("# This code counts forever - you'll need to STOP it!\n# Run this cell, watch it count, then click the STOP button\n\nimport time\n\ncounter = 1\nwhile True:\n    print(f\"Counting: {counter}\")\n    counter = counter + 1\n    time.sleep(0.5)  # Wait half a second"),
      para("Instructions: Run it, let it count to 10 or so, then stop it"),

      heading3("Cell A.4 - Simple Math"),
      para("Type: Code"),
      para("Purpose: Show that Python can do calculations"),
      codeBlock("# Python can do math!\n\napples = 5\noranges = 3\ntotal_fruit = apples + oranges\n\nprint(f\"I have {apples} apples\")\nprint(f\"I have {oranges} oranges\")\nprint(f\"Total fruit: {total_fruit}\")"),

      heading3("Cell A.5 - Variables Practice"),
      para("Type: Code"),
      para("Purpose: Practice creating and using variables"),
      codeBlock("# YOUR TURN: Change the values below and run again!\n\nmy_name = \"Student\"  # Change this to your name!\nmy_age = 15          # Change this to your age!\n\nprint(f\"Hello, my name is {my_name}\")\nprint(f\"I am {my_age} years old\")"),

      heading3("Cell A.6 - Check Understanding (Markdown)"),
      para("Type: Markdown"),
      para("Content:"),
      codeBlock("## Quick Check!\n\n**Answer these questions:**\n1. What keyboard shortcut runs a cell? _______________\n2. What button stops running code? _______________\n3. What does [*] mean next to a cell? _______________"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SECTION B ==========
      heading2("Section B: More Practice (Non-VESC)"),
      para("Purpose: Build confidence with Python before hardware"),

      heading3("Cell B.1 - Functions Introduction"),
      para("Type: Code"),
      codeBlock("# Functions are like recipes - they do something when you call them\n\ndef say_hello(name):\n    print(f\"Hello, {name}!\")\n    print(\"Welcome to the PEV coding class!\")\n\n# Call the function\nsay_hello(\"Everyone\")"),

      heading3("Cell B.2 - Function with Return Value"),
      para("Type: Code"),
      codeBlock("# Some functions give you a value back (return)\n\ndef add_numbers(a, b):\n    result = a + b\n    return result\n\n# Use the function\nmy_sum = add_numbers(10, 25)\nprint(f\"10 + 25 = {my_sum}\")"),

      heading3("Cell B.3 - Practice Creating a Function"),
      para("Type: Code"),
      codeBlock("# YOUR TURN: Fill in the blank to make this function work\n# The function should multiply two numbers\n\ndef multiply_numbers(a, b):\n    result = a _____ b  # What goes here? (hint: multiplication symbol)\n    return result\n\n# Test it\nproduct = multiply_numbers(6, 7)\nprint(f\"6 × 7 = {product}\")  # Should print 42"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SECTION C ==========
      heading2("Section C: Connecting to the VESC"),
      para("Purpose: Establish connection to real hardware"),

      heading3("Cell C.1 - Section Header (Markdown)"),
      para("Type: Markdown"),
      codeBlock("# 🔌 Connecting to Your PEV\n\nNow we'll connect to real hardware! Make sure your PEV is powered ON."),

      heading3("Cell C.2 - Import and Connect"),
      para("Type: Code"),
      codeBlock("# Setup and connect to the VESC\nimport sys\nimport os\nsys.path.append(os.path.dirname(os.path.dirname(os.path.abspath('__file__'))))\n\nfrom student_api import VESCStudentAPI\nimport time\n\n# Create the connection\nvesc_api = VESCStudentAPI()\n\nif vesc_api.start():\n    print(\"Starting connection...\")\n    time.sleep(6)  # Wait for discovery\n    \n    connected = vesc_api.get_connected_controllers()\n    vesc = vesc_api.get_controller(74)\n    \n    if 74 in connected and vesc.is_connected():\n        voltage = vesc.get_input_voltage()\n        print(f\"✅ Connected to VESC controller!\")\n        print(f\"📊 Battery Voltage: {voltage:.1f}V\")\n    else:\n        print(\"❌ VESC not found! Is the PEV powered ON?\")\nelse:\n    print(\"❌ Failed to start VESC system\")"),

      heading3("Cell C.3 - Checkpoint (Markdown)"),
      para("Type: Markdown"),
      codeBlock("## ✋ Checkpoint!\n\n**Did you see the green checkmark and battery voltage?**\n- YES → Great! Continue to Section D\n- NO → Raise your hand for help"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SECTION D ==========
      heading2("Section D: Reading Telemetry Data"),
      para("Purpose: Students read real data from their PEV"),

      heading3("Cell D.1 - Read Voltage (Fill in Blank)"),
      para("Type: Code"),
      codeBlock("# YOUR TURN: Fill in the blank to read the voltage\n# Hint: Look at what function we used in the connection cell\n\nvoltage = vesc._________________()  # Fill this in!\nprint(f\"Battery Voltage: {voltage} V\")\n\n# Write your reading here: ______ V"),
      para("Answer: get_input_voltage"),

      heading3("Cell D.2 - Read RPM"),
      para("Type: Code"),
      codeBlock("# Read the motor RPM (Revolutions Per Minute)\n\nrpm = vesc.get_rpm()\nprint(f\"Motor RPM: {rpm}\")\n\n# ✏️ RECORD YOUR RESULTS:\n# Motor NOT spinning: ______ RPM\n# Motor spinning (by hand): ______ RPM"),

      heading3("Cell D.3 - RPM Experiment Instructions (Markdown)"),
      para("Type: Markdown"),
      codeBlock("## 🔬 RPM Experiment\n\n1. Run the cell above with the motor NOT spinning → Write down the RPM\n2. GENTLY spin the wheel BY HAND\n3. While still spinning, run the cell AGAIN → Write down the new RPM\n4. Did the numbers change? That's REAL-TIME data!"),

      heading3("Cell D.4 - Read Motor Current"),
      para("Type: Code"),
      codeBlock("# Read how much electricity the motor is using\n\ncurrent = vesc.get_motor_current()\nprint(f\"Motor Current: {current} A\")\n\n# This will be 0 when the motor isn't running\n# That's normal!"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SECTION E ==========
      heading2("Section E: Fill-in-the-Blank Challenges"),
      para("Purpose: Students write their own code with guidance"),

      heading3("Cell E.1 - Temperature Challenge"),
      para("Type: Code"),
      codeBlock("# CHALLENGE: Read the controller (FET) temperature\n# Fill in BOTH blanks!\n\ntemp = vesc.get_____temperature()  # What type? (hint: 3 letters)\nprint(f\"Controller Temperature: {____} °C\")  # What variable?\n\n# ✏️ My temperature reading: ______ °C"),
      para("Answers: get_fet_temperature() and temp"),

      heading3("Cell E.2 - Motor Temperature Challenge"),
      para("Type: Code"),
      codeBlock("# CHALLENGE: Now read the MOTOR temperature\n\nmotor_temp = vesc.get_____________()  # What's the function name?\nprint(f\"Motor Temperature: {motor_temp} °C\")\n\n# Note: Lectec vehicles may show 0 if no motor temp sensor"),
      para("Answer: get_motor_temperature"),

      heading3("Cell E.3 - Multiple Readings Challenge"),
      para("Type: Code"),
      codeBlock("# BOSS CHALLENGE: Read THREE values at once!\n# Fill in all the blanks\n\nvoltage = vesc.____________()\nrpm = vesc.____________()\nfet_temp = vesc.____________()\n\nprint(\"=== PEV Status ===\")\nprint(f\"Battery: {voltage} V\")\nprint(f\"Speed: {rpm} RPM\")\nprint(f\"Controller Temp: {fet_temp} °C\")"),
      para("Answers: get_input_voltage, get_rpm, get_fet_temperature"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SECTION F ==========
      heading2("Section F: Matching Exercise"),
      para("Purpose: Reinforce understanding of which function gets which data"),

      heading3("Cell F.1 - Matching Instructions (Markdown)"),
      para("Type: Markdown"),
      codeBlock("## 🎯 Matching Challenge!\n\nMatch each question to the correct function.\n\n**Questions:**\n1. How fast is the motor spinning?\n2. How much battery do I have?\n3. Is the controller getting hot?\n4. How much electricity is the motor using?\n5. How hot is the motor itself?\n\n**Functions (choose from):**\n- A. get_motor_temperature()\n- B. get_rpm()\n- C. get_input_voltage()\n- D. get_motor_current()\n- E. get_fet_temperature()"),

      heading3("Cell F.2 - Student Answers"),
      para("Type: Code"),
      codeBlock("# Enter your answers below (just the letters)\n# Example: answer_1 = \"B\"\n\nanswer_1 = \"___\"  # How fast is the motor spinning?\nanswer_2 = \"___\"  # How much battery do I have?\nanswer_3 = \"___\"  # Is the controller getting hot?\nanswer_4 = \"___\"  # How much electricity is the motor using?\nanswer_5 = \"___\"  # How hot is the motor itself?\n\nprint(\"Your answers recorded! Run the next cell to check.\")"),

      heading3("Cell F.3 - Check Answers"),
      para("Type: Code"),
      codeBlock("# Check your answers!\n\ncorrect = {\n    1: \"B\",  # RPM\n    2: \"C\",  # Voltage\n    3: \"E\",  # FET temp\n    4: \"D\",  # Motor current\n    5: \"A\"   # Motor temp\n}\n\nscore = 0\nfor i in range(1, 6):\n    student = eval(f\"answer_{i}\").upper()\n    if student == correct[i]:\n        print(f\"Question {i}: ✅ Correct!\")\n        score += 1\n    else:\n        print(f\"Question {i}: ❌ Your answer: {student}, Correct: {correct[i]}\")\n\nprint(f\"\\nScore: {score}/5\")"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SECTION G ==========
      heading2("Section G: Wrap-Up"),

      heading3("Cell G.1 - Clean Shutdown"),
      para("Type: Code"),
      codeBlock("# Always clean up when you're done!\n\nvesc_api.stop()\nprint(\"✅ VESC connection closed safely\")\nprint(\"Great job today! See you in Module 2!\")"),

      heading3("Cell G.2 - Summary (Markdown)"),
      para("Type: Markdown"),
      codeBlock("## 🎉 Module 1 Complete!\n\n### What you learned:\n- ✅ How to use Jupyter Notebooks\n- ✅ How to run and stop code\n- ✅ What an API is\n- ✅ How to connect to the VESC\n- ✅ How to read voltage, RPM, and temperature\n- ✅ That the data is REAL-TIME!\n\n### Coming up in Module 2:\n- Building a live dashboard\n- Continuous data monitoring\n- Data logging"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== PART 3: TEACHER NOTES ==========
      heading1("Part 3: Teacher Notes & Timing"),

      heading2("Suggested Timing (45-minute class)"),

      para("Opening & Hook (Slides 1-3): 5 minutes", { bold: true }),
      bulletItem("Get students excited with the 'what if' scenario"),
      bulletItem("Show real-world applications to build credibility"),

      para("Objectives & Hardware (Slides 4-8): 8 minutes", { bold: true }),
      bulletItem("Clear learning objectives"),
      bulletItem("Hardware show-and-tell if possible"),
      bulletItem("System architecture overview"),

      para("Safety Rules (Slide 9): 3 minutes", { bold: true }),
      bulletItem("Critical - ensure understanding"),
      bulletItem("Have students repeat Rule 1"),

      para("Jupyter Basics (Slides 10-12 + Notebook A-B): 10 minutes", { bold: true }),
      bulletItem("Hands-on practice with run/stop"),
      bulletItem("Everyone should complete Section A before proceeding"),

      para("API & Connection (Slides 13-15 + Notebook C): 7 minutes", { bold: true }),
      bulletItem("API explanation with restaurant analogy"),
      bulletItem("Everyone should be connected before proceeding"),

      para("Reading Data (Slides 16-18 + Notebook D): 8 minutes", { bold: true }),
      bulletItem("Voltage reading"),
      bulletItem("RPM experiment with hand-spinning"),

      para("Challenges & Summary (Slides 19-22 + Notebook E-F): 4 minutes", { bold: true }),
      bulletItem("Fill-in-the-blank exercises"),
      bulletItem("Matching game"),
      bulletItem("Celebration and preview"),

      heading2("Common Issues & Solutions"),

      para("Issue: Student can't connect to VESC"),
      bulletItem("Check: Is the PEV powered ON?"),
      bulletItem("Check: Is the USB cable connected?"),
      bulletItem("Check: Is the correct notebook open?"),
      bulletItem("Try: Restart the kernel and run connection cell again"),

      para("Issue: Student accidentally closed connection"),
      bulletItem("Solution: Run the connection cell (C.2) again"),

      para("Issue: Code won't stop running"),
      bulletItem("Click Stop button OR press I,I OR Kernel → Interrupt"),
      bulletItem("If that fails: Kernel → Restart"),

      para("Issue: Student gets all zeros for readings"),
      bulletItem("This is NORMAL for RPM and current when motor isn't moving"),
      bulletItem("Voltage should always show a value - if not, check connection"),

      heading2("Key Phrases to Use"),
      bulletItem("'Your PEV is about to get a brain - and you're going to program it!'"),
      bulletItem("'The API is your menu - just pick what data you want!'"),
      bulletItem("'You talked to your PEV today, and it talked back. That's real engineering!'"),
      bulletItem("'Shift+Enter is your new best friend'"),
      bulletItem("'The stop button is your emergency brake'"),
      bulletItem("'Zero RPM makes sense - the motor isn't moving!'"),

    ]
  }]
});

// Generate the document
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("Module_01_Detailed_Guide.docx", buffer);
  console.log("Module 1 Detailed Guide created successfully!");
});
