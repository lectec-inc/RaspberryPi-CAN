const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, LevelFormat, HeadingLevel,
        BorderStyle, WidthType, ShadingType, PageNumber, PageBreak } = require('docx');
const fs = require('fs');

// Color palette
const colors = {
  primary: "1E3A5F",      // Dark blue
  secondary: "2E7D32",    // Green
  accent: "E65100",       // Orange
  light: "F5F5F5",        // Light gray
  headerBg: "1E3A5F",     // Header background
  tableBorder: "CCCCCC",
  tableHeader: "E8EEF4",
  tableAlt: "F8FAFB",
  warningBg: "FFF3E0",
  successBg: "E8F5E9",
  infoBg: "E3F2FD"
};

const border = { style: BorderStyle.SINGLE, size: 1, color: colors.tableBorder };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorders = { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, 
                   left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } };

// Helper functions
const heading1 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  spacing: { before: 400, after: 200 },
  children: [new TextRun({ text, bold: true, size: 36, color: colors.primary, font: "Arial" })]
});

const heading2 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  spacing: { before: 300, after: 150 },
  children: [new TextRun({ text, bold: true, size: 28, color: colors.primary, font: "Arial" })]
});

const heading3 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_3,
  spacing: { before: 200, after: 100 },
  children: [new TextRun({ text, bold: true, size: 24, color: colors.secondary, font: "Arial" })]
});

const para = (text, options = {}) => new Paragraph({
  spacing: { after: 120 },
  children: [new TextRun({ text, size: 22, font: "Arial", ...options })]
});

const boldPara = (label, text) => new Paragraph({
  spacing: { after: 120 },
  children: [
    new TextRun({ text: label, bold: true, size: 22, font: "Arial" }),
    new TextRun({ text, size: 22, font: "Arial" })
  ]
});

const bulletPoint = (text, level = 0) => new Paragraph({
  numbering: { reference: "bullets", level },
  spacing: { after: 80 },
  children: [new TextRun({ text, size: 22, font: "Arial" })]
});

const numberedPoint = (text, ref = "numbers", level = 0) => new Paragraph({
  numbering: { reference: ref, level },
  spacing: { after: 80 },
  children: [new TextRun({ text, size: 22, font: "Arial" })]
});

const calloutBox = (title, content, bgColor) => {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    columnWidths: [9360],
    rows: [
      new TableRow({
        children: [
          new TableCell({
            borders: { 
              top: { style: BorderStyle.SINGLE, size: 1, color: colors.tableBorder },
              bottom: { style: BorderStyle.SINGLE, size: 1, color: colors.tableBorder },
              left: { style: BorderStyle.SINGLE, size: 24, color: colors.primary },
              right: { style: BorderStyle.SINGLE, size: 1, color: colors.tableBorder }
            },
            width: { size: 9360, type: WidthType.DXA },
            shading: { fill: bgColor, type: ShadingType.CLEAR },
            margins: { top: 120, bottom: 120, left: 200, right: 200 },
            children: [
              new Paragraph({
                spacing: { after: 80 },
                children: [new TextRun({ text: title, bold: true, size: 22, font: "Arial", color: colors.primary })]
              }),
              new Paragraph({
                children: [new TextRun({ text: content, size: 20, font: "Arial" })]
              })
            ]
          })
        ]
      })
    ]
  });
};

const createTable = (headers, rows, colWidths) => {
  const headerRow = new TableRow({
    children: headers.map((h, i) => new TableCell({
      borders,
      width: { size: colWidths[i], type: WidthType.DXA },
      shading: { fill: colors.tableHeader, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      children: [new Paragraph({ children: [new TextRun({ text: h, bold: true, size: 20, font: "Arial" })] })]
    }))
  });
  
  const dataRows = rows.map((row, rowIdx) => new TableRow({
    children: row.map((cell, i) => new TableCell({
      borders,
      width: { size: colWidths[i], type: WidthType.DXA },
      shading: { fill: rowIdx % 2 === 1 ? colors.tableAlt : "FFFFFF", type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      children: [new Paragraph({ children: [new TextRun({ text: cell, size: 20, font: "Arial" })] })]
    }))
  }));
  
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    columnWidths: colWidths,
    rows: [headerRow, ...dataRows]
  });
};

const spacer = () => new Paragraph({ spacing: { after: 200 }, children: [] });

// Document content
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets",
        levels: [
          { level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
          { level: 1, format: LevelFormat.BULLET, text: "\u25E6", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 1080, hanging: 360 } } } }
        ]
      },
      { reference: "numbers",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }]
      },
      { reference: "lessonnums",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }]
      },
      { reference: "lessonnums2",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }]
      },
      { reference: "lessonnums3",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }]
      },
      { reference: "lessonnums4",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }]
      },
      { reference: "lessonnums5",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }]
      }
    ]
  },
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: colors.primary },
        paragraph: { spacing: { before: 400, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: colors.primary },
        paragraph: { spacing: { before: 300, after: 150 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: colors.secondary },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 2 } },
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
          children: [new TextRun({ text: "Lectec Electric Skateboard Curriculum Plan", italics: true, size: 18, font: "Arial", color: "666666" })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Page ", size: 18, font: "Arial", color: "666666" }),
            new TextRun({ children: [PageNumber.CURRENT], size: 18, font: "Arial", color: "666666" }),
            new TextRun({ text: " of ", size: 18, font: "Arial", color: "666666" }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 18, font: "Arial", color: "666666" })
          ]
        })]
      })
    },
    children: [
      // TITLE PAGE
      new Paragraph({ spacing: { before: 2000 }, children: [] }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "LECTEC ELECTRIC SKATEBOARD", bold: true, size: 48, font: "Arial", color: colors.primary })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 400 },
        children: [new TextRun({ text: "CURRICULUM PLAN", bold: true, size: 44, font: "Arial", color: colors.secondary })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 200 },
        children: [new TextRun({ text: "CAN Network Communication & AI Vision Systems", size: 28, font: "Arial", color: "555555" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 600 },
        children: [new TextRun({ text: "Raspberry Pi + IMX500 AI Camera + VESC Motor Controller", size: 24, font: "Arial", color: "777777" })]
      }),
      spacer(),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "A Comprehensive 10-Day Course for High School Students", size: 24, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 1500 },
        children: [new TextRun({ text: "45-Minute Class Periods", size: 22, font: "Arial", color: "666666" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "Version 2.0 | Curriculum Redesign Document", size: 20, font: "Arial", color: "888888" })]
      }),
      
      // PAGE BREAK - EXECUTIVE SUMMARY
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Executive Summary"),
      para("This document outlines a comprehensive restructuring of the Lectec Electric Skateboard educational curriculum. The redesign transforms the existing Jupyter notebook tutorials into a cohesive 10-day course with professional PowerPoint presentations, interactive student notebooks, and two capstone projects."),
      spacer(),
      
      heading2("Current State Analysis"),
      para("After thorough analysis of all 15 existing Jupyter notebooks across both the CAN/VESC tutorials and AI Camera tutorials, the following critical issues were identified:"),
      spacer(),
      
      heading3("Critical Weaknesses Identified"),
      createTable(
        ["Category", "Issue", "Impact"],
        [
          ["Student Interaction", "Minimal fill-in-the-blank exercises or coding challenges", "Students passively read rather than actively learn"],
          ["Code Completeness", "Many cells reference undefined external functions", "Code fails to execute, frustrating students"],
          ["Progression", "No clear bridge between CAN fundamentals and AI integration", "Students struggle to connect concepts"],
          ["Teacher Support", "No presentation materials for classroom instruction", "Teachers must create their own content"],
          ["Assessment", "No structured quizzes or knowledge checks", "No way to verify student understanding"],
          ["Project Guidance", "Capstone projects provide only empty scaffolding", "Students overwhelmed by blank slate approach"],
          ["Error Handling", "Minimal guidance when things go wrong", "Students get stuck with no troubleshooting help"],
          ["Real-World Context", "Limited explanation of why concepts matter", "Students miss practical applications"]
        ],
        [2000, 3500, 3860]
      ),
      spacer(),
      
      heading3("Strengths to Preserve"),
      bulletPoint("Well-designed student API that abstracts complexity (VESCStudentAPI)"),
      bulletPoint("Real hardware integration with actual motor data outputs"),
      bulletPoint("Progressive difficulty structure (fundamentals to advanced)"),
      bulletPoint("Safety-first approach with repeated warnings"),
      bulletPoint("Good use of visual metaphors (car analogy for VESC)"),
      spacer(),
      
      calloutBox("Design Philosophy", 
        "Every lesson will follow a consistent structure: Teacher presents concepts (PowerPoint), students apply concepts (Jupyter notebook with guided exercises), students demonstrate understanding (fill-in-the-blank code and reflection questions). This ensures active learning rather than passive observation.",
        colors.infoBg),
      
      // PAGE BREAK - COURSE OVERVIEW
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Course Overview"),
      
      heading2("Target Audience"),
      bulletPoint("Age: High School students (14-18 years)"),
      bulletPoint("Prerequisites: Basic Python syntax (quick reference provided, not taught)"),
      bulletPoint("Setting: Structured classroom with teacher-led instruction"),
      bulletPoint("Hardware: Raspberry Pi Zero 2W with IMX500 AI Camera on electric skateboard"),
      spacer(),
      
      heading2("Course Structure"),
      createTable(
        ["Day", "Module", "Focus Area", "Deliverable"],
        [
          ["1", "Module 1: System Introduction", "Hardware overview, safety, first connection", "System connection verified"],
          ["2", "Module 2: CAN Fundamentals", "What is CAN bus, reading motor data", "Read all telemetry values"],
          ["3", "Module 3: Data Visualization", "Real-time graphs, dashboards", "Create custom dashboard"],
          ["4", "Module 4: Motor Control", "Duty cycle, current control, safety", "Control motor safely"],
          ["5", "Module 5: CAN Project Day", "CAPSTONE PROJECT 1", "Complete CAN-based project"],
          ["6", "Module 6: AI Introduction", "What is AI, how cameras see", "Understand AI confidence"],
          ["7", "Module 7: Object Detection", "Live detection, bounding boxes", "Detect and identify objects"],
          ["8", "Module 8: AI + Hardware", "Buzzer alerts, GPIO integration", "Trigger alerts on detection"],
          ["9", "Module 9: System Integration", "AI + CAN combined system", "Build safety monitor"],
          ["10", "Module 10: AI Project Day", "CAPSTONE PROJECT 2", "Complete integrated AI project"]
        ],
        [600, 2400, 3200, 3160]
      ),
      spacer(),
      
      heading2("Time Allocation per Lesson"),
      createTable(
        ["Segment", "Duration", "Purpose"],
        [
          ["Teacher Presentation", "15 minutes", "Introduce concepts using PowerPoint slides"],
          ["Guided Practice", "20 minutes", "Students work through Jupyter notebook exercises"],
          ["Knowledge Check", "5 minutes", "Fill-in-the-blank code and reflection questions"],
          ["Wrap-up / Preview", "5 minutes", "Summary and preview of next lesson"]
        ],
        [2500, 2000, 4860]
      ),
      
      // PAGE BREAK - MODULE 1
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 1: System Introduction"),
      boldPara("Day: ", "1 of 10"),
      boldPara("Duration: ", "45 minutes"),
      boldPara("Prerequisites: ", "None"),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this lesson, students will be able to:"),
      numberedPoint("Identify the major hardware components of the Lectec electric skateboard system", "lessonnums"),
      numberedPoint("Explain the role of the Raspberry Pi as the central controller", "lessonnums"),
      numberedPoint("Describe what a CAN bus is and why it is used in vehicles", "lessonnums"),
      numberedPoint("Successfully connect to the VESC motor controller and verify communication", "lessonnums"),
      numberedPoint("Apply safety protocols when working with electric vehicle systems", "lessonnums"),
      spacer(),
      
      heading2("PowerPoint Slide Outline (15 slides)"),
      createTable(
        ["Slide #", "Title", "Content"],
        [
          ["1", "Title Slide", "Lectec Electric Skateboard: Your First Embedded System"],
          ["2", "What You Will Build", "Photo of complete system, overview of capabilities"],
          ["3", "Hardware Components", "Diagram: Pi Zero 2W, IMX500 Camera, VESC, Battery, Motor"],
          ["4", "The Raspberry Pi", "Mini-computer explanation, why we use it, specifications"],
          ["5", "The VESC Controller", "Motor brain, controls speed/power, communicates over CAN"],
          ["6", "What is CAN Bus?", "Controller Area Network, used in cars, simple diagram"],
          ["7", "Why CAN Bus?", "Reliability, noise immunity, multiple devices on one wire"],
          ["8", "The AI Camera", "IMX500 sensor, on-chip AI processing, what it can detect"],
          ["9", "How It All Connects", "System diagram showing data flow between components"],
          ["10", "Safety First", "Electrical safety, moving parts, battery handling"],
          ["11", "Safety Rules", "5 key rules students must follow (with icons)"],
          ["12", "Jupyter Notebooks", "What they are, how to use them, cell types explained"],
          ["13", "Your First Connection", "Preview of what students will do in the notebook"],
          ["14", "What is Telemetry?", "Data from sensors, like a fitness tracker for motors"],
          ["15", "Summary + Next Steps", "Key takeaways, preview of Day 2"]
        ],
        [1000, 2500, 5860]
      ),
      spacer(),
      
      heading2("Jupyter Notebook Structure"),
      heading3("Section 1: Welcome and Setup (3 cells)"),
      bulletPoint("Markdown: Welcome message with learning objectives"),
      bulletPoint("Code: Import statements with explanation comments"),
      bulletPoint("Code: System connection with 6-second discovery wait"),
      spacer(),
      
      heading3("Section 2: Understanding Your Hardware (4 cells)"),
      bulletPoint("Markdown: Hardware diagram and component descriptions"),
      bulletPoint("EXERCISE: Fill-in-the-blank - match component to function"),
      bulletPoint("Code: Check connection status with is_connected()"),
      bulletPoint("Markdown: Explanation of what the code did"),
      spacer(),
      
      heading3("Section 3: Reading Your First Data (5 cells)"),
      bulletPoint("Markdown: Introduction to telemetry concept"),
      bulletPoint("Code: Read battery voltage (always returns real data)"),
      bulletPoint("EXERCISE: Predict what get_input_voltage() returns before running"),
      bulletPoint("Code: Read RPM (will be 0 if motor not moving)"),
      bulletPoint("EXERCISE: Why is RPM zero? Multiple choice question"),
      spacer(),
      
      heading3("Section 4: Knowledge Check (3 cells)"),
      bulletPoint("EXERCISE: Fill in the missing code to read motor temperature"),
      bulletPoint("EXERCISE: Short answer - What does CAN stand for and why is it used?"),
      bulletPoint("Markdown: Summary and preview of next lesson"),
      spacer(),
      
      calloutBox("Interactive Element Example",
        "Fill in the blank to read the motor temperature:\n\ntemp = vesc._____________________()  # Hint: get_motor_temperature\nprint(f\"Motor temperature: {temp} degrees Celsius\")",
        colors.successBg),
      
      // PAGE BREAK - MODULE 2
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 2: CAN Fundamentals"),
      boldPara("Day: ", "2 of 10"),
      boldPara("Duration: ", "45 minutes"),
      boldPara("Prerequisites: ", "Module 1 completed"),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this lesson, students will be able to:"),
      numberedPoint("Read all available telemetry data from the VESC controller", "lessonnums2"),
      numberedPoint("Explain the difference between motor data, power data, and temperature data", "lessonnums2"),
      numberedPoint("Interpret positive and negative values (RPM direction, current flow)", "lessonnums2"),
      numberedPoint("Use the get_all_telemetry() function to retrieve structured data", "lessonnums2"),
      numberedPoint("Identify which readings require motor movement vs. which are always available", "lessonnums2"),
      spacer(),
      
      heading2("PowerPoint Slide Outline (12 slides)"),
      createTable(
        ["Slide #", "Title", "Content"],
        [
          ["1", "Title Slide", "Reading Motor Data: Your Eyes into the System"],
          ["2", "Review: CAN Bus", "Quick recap from Day 1, answer any questions"],
          ["3", "Types of Telemetry", "Motor (speed, power), Electrical (voltage, current), Thermal"],
          ["4", "Motor Data Deep Dive", "RPM, current, duty cycle - what each means"],
          ["5", "Understanding RPM", "Rotations per minute, positive/negative = direction"],
          ["6", "Understanding Current", "Amperes, motor current vs input current, regen braking"],
          ["7", "Understanding Duty Cycle", "Throttle percentage, -1.0 to 1.0 range explained"],
          ["8", "Power Data", "Voltage, amp-hours, watt-hours, energy tracking"],
          ["9", "Temperature Data", "FET temperature, motor temperature, why they matter"],
          ["10", "The Magic Function", "get_all_telemetry() returns everything at once"],
          ["11", "When Data is Zero", "Motor not moving = most readings are 0, voltage always works"],
          ["12", "Summary + Hands-On", "Key points, transition to notebook exercise"]
        ],
        [1000, 2500, 5860]
      ),
      spacer(),
      
      heading2("Jupyter Notebook Structure"),
      heading3("Section 1: Warm-Up Review (2 cells)"),
      bulletPoint("Code: Quick connection check from yesterday"),
      bulletPoint("EXERCISE: What was the voltage reading from Day 1? Compare to today"),
      spacer(),
      
      heading3("Section 2: Motor Data Exploration (6 cells)"),
      bulletPoint("Markdown: Introduction to motor telemetry"),
      bulletPoint("Code: Read RPM with explanation"),
      bulletPoint("Code: Read motor current with explanation"),
      bulletPoint("Code: Read duty cycle with explanation"),
      bulletPoint("EXERCISE: Spin motor by hand, predict which values will change"),
      bulletPoint("EXERCISE: Fill in code to read all three motor values in one cell"),
      spacer(),
      
      heading3("Section 3: Power and Temperature (5 cells)"),
      bulletPoint("Markdown: Power monitoring introduction"),
      bulletPoint("Code: Voltage, input current, amp-hours, watt-hours"),
      bulletPoint("Markdown: Temperature monitoring and safety thresholds"),
      bulletPoint("Code: FET and motor temperature with threshold checks"),
      bulletPoint("EXERCISE: Write code that prints a warning if temperature > 50C"),
      spacer(),
      
      heading3("Section 4: All-in-One Function (3 cells)"),
      bulletPoint("Code: Demonstrate get_all_telemetry() with pretty printing"),
      bulletPoint("EXERCISE: Access specific nested values from telemetry dictionary"),
      bulletPoint("Markdown: Summary table of all 18 available functions"),
      spacer(),
      
      heading3("Section 5: Knowledge Check (2 cells)"),
      bulletPoint("EXERCISE: Match the function to what it measures (5 items)"),
      bulletPoint("EXERCISE: Short answer - Why might motor current be negative?"),
      
      // PAGE BREAK - MODULE 3
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 3: Data Visualization"),
      boldPara("Day: ", "3 of 10"),
      boldPara("Duration: ", "45 minutes"),
      boldPara("Prerequisites: ", "Modules 1-2 completed"),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this lesson, students will be able to:"),
      numberedPoint("Create real-time updating displays using HTML and clear_output()", "lessonnums3"),
      numberedPoint("Build a live dashboard showing multiple data streams simultaneously", "lessonnums3"),
      numberedPoint("Plot time-series data using matplotlib", "lessonnums3"),
      numberedPoint("Customize dashboard appearance with colors based on data values", "lessonnums3"),
      numberedPoint("Understand why visualization helps identify patterns and problems", "lessonnums3"),
      spacer(),
      
      heading2("PowerPoint Slide Outline (10 slides)"),
      createTable(
        ["Slide #", "Title", "Content"],
        [
          ["1", "Title Slide", "Seeing Your Data: Dashboards and Graphs"],
          ["2", "Why Visualize?", "Numbers vs. graphs, pattern recognition, anomaly detection"],
          ["3", "Real-Time Updates", "clear_output() technique, refresh rate concepts"],
          ["4", "Dashboard Design", "What info to show, layout principles, color coding"],
          ["5", "Color Psychology", "Green = good, yellow = warning, red = danger"],
          ["6", "HTML in Jupyter", "display(HTML(...)) for formatted output"],
          ["7", "Time-Series Graphs", "Matplotlib basics, live updating plots"],
          ["8", "Reading Graphs", "X-axis = time, Y-axis = value, interpreting trends"],
          ["9", "Building Your Dashboard", "Preview of what students will create"],
          ["10", "Summary", "Key visualization techniques, transition to hands-on"]
        ],
        [1000, 2500, 5860]
      ),
      spacer(),
      
      heading2("Jupyter Notebook Structure"),
      heading3("Section 1: Simple Live Display (4 cells)"),
      bulletPoint("Markdown: Introduction to real-time updates"),
      bulletPoint("Code: Basic loop with clear_output() showing voltage"),
      bulletPoint("EXERCISE: Modify code to also show temperature"),
      bulletPoint("EXERCISE: Add a warning message if temperature > 40C"),
      spacer(),
      
      heading3("Section 2: Building a Dashboard (5 cells)"),
      bulletPoint("Code: HTML template with placeholders"),
      bulletPoint("Code: Color-coding function for temperature"),
      bulletPoint("Code: Complete dashboard with live updates"),
      bulletPoint("EXERCISE: Add RPM to the dashboard"),
      bulletPoint("EXERCISE: Change the color thresholds for temperature"),
      spacer(),
      
      heading3("Section 3: Graphing Data (4 cells)"),
      bulletPoint("Markdown: Introduction to matplotlib time-series"),
      bulletPoint("Code: Collect data for 10 seconds, plot result"),
      bulletPoint("EXERCISE: Modify to collect for 20 seconds"),
      bulletPoint("EXERCISE: Plot two values on the same graph (voltage and current)"),
      spacer(),
      
      heading3("Section 4: Knowledge Check (2 cells)"),
      bulletPoint("EXERCISE: Fill in code to create a 4-panel dashboard"),
      bulletPoint("EXERCISE: Short answer - Why is data visualization important for safety?"),
      
      // PAGE BREAK - MODULE 4
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 4: Motor Control"),
      boldPara("Day: ", "4 of 10"),
      boldPara("Duration: ", "45 minutes"),
      boldPara("Prerequisites: ", "Modules 1-3 completed"),
      spacer(),
      
      calloutBox("Safety Note",
        "This is the first lesson involving active motor control. Ensure all safety protocols are reviewed before students run any motor control code. Motors should be secured on test stands, not on complete skateboards during this lesson.",
        colors.warningBg),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this lesson, students will be able to:"),
      numberedPoint("Explain the difference between duty cycle control and current control", "lessonnums4"),
      numberedPoint("Safely start and stop a motor using set_duty_cycle()", "lessonnums4"),
      numberedPoint("Apply regenerative braking using set_brake_current()", "lessonnums4"),
      numberedPoint("Implement proper safety checks before and after motor commands", "lessonnums4"),
      numberedPoint("Create a controlled acceleration/deceleration sequence", "lessonnums4"),
      spacer(),
      
      heading2("PowerPoint Slide Outline (12 slides)"),
      createTable(
        ["Slide #", "Title", "Content"],
        [
          ["1", "Title Slide", "Taking Control: Commanding Your Motor"],
          ["2", "Safety Review", "Critical safety rules, emergency stop procedures"],
          ["3", "Control Methods", "Overview: Duty cycle, Current, Brake current"],
          ["4", "Duty Cycle Control", "Throttle percentage, -1.0 to 1.0, fire-and-forget"],
          ["5", "Current Control", "Force/torque control, measured in Amperes"],
          ["6", "Regenerative Braking", "Motor as generator, energy recovery, safety stop"],
          ["7", "Command Rate Limiting", "Why 0.1s delay exists, CAN bus flooding prevention"],
          ["8", "Safety Flags", "MOTOR_CONTROL_ENABLED pattern, why it exists"],
          ["9", "Control Sequence", "Flowchart: Check safety, send command, verify, stop"],
          ["10", "Emergency Stop", "set_duty_cycle(0) immediately stops motor"],
          ["11", "Monitoring During Control", "Reading data while motor runs"],
          ["12", "Summary + Safety Reminder", "Key points, emphasize safety one more time"]
        ],
        [1000, 2500, 5860]
      ),
      spacer(),
      
      heading2("Jupyter Notebook Structure"),
      heading3("Section 1: Safety Checklist (3 cells)"),
      bulletPoint("Markdown: Mandatory safety checklist with checkboxes"),
      bulletPoint("Code: Connection verification and initial readings"),
      bulletPoint("EXERCISE: Fill in safety check code that verifies motor is stopped"),
      spacer(),
      
      heading3("Section 2: Duty Cycle Control (5 cells)"),
      bulletPoint("Markdown: Explanation of duty cycle concept"),
      bulletPoint("Code: set_duty_cycle(0.1) - very slow speed test"),
      bulletPoint("Code: Read RPM during operation, then stop"),
      bulletPoint("EXERCISE: Modify to use 0.2 duty cycle, predict RPM change"),
      bulletPoint("EXERCISE: Create a 5-step acceleration sequence (0.1, 0.15, 0.2, 0.15, 0)"),
      spacer(),
      
      heading3("Section 3: Current Control and Braking (4 cells)"),
      bulletPoint("Markdown: Explanation of current control"),
      bulletPoint("Code: set_current() demonstration"),
      bulletPoint("Code: set_brake_current() demonstration with monitoring"),
      bulletPoint("EXERCISE: Write code that applies brake when RPM > 1000"),
      spacer(),
      
      heading3("Section 4: Knowledge Check (2 cells)"),
      bulletPoint("EXERCISE: Fill in the blank control sequence with safety checks"),
      bulletPoint("EXERCISE: Short answer - Why do we use regenerative braking instead of just stopping?"),
      
      // PAGE BREAK - MODULE 5 (PROJECT DAY 1)
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 5: CAN Capstone Project"),
      boldPara("Day: ", "5 of 10"),
      boldPara("Duration: ", "45 minutes (may extend)"),
      boldPara("Prerequisites: ", "Modules 1-4 completed"),
      spacer(),
      
      calloutBox("Capstone Project 1",
        "Students will design and implement an open-ended project using only CAN bus communication with the VESC motor controller. This is the first of two capstone projects.",
        colors.infoBg),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this project, students will be able to:"),
      numberedPoint("Define project requirements based on available VESC functions", "lessonnums5"),
      numberedPoint("Design a solution that combines multiple data streams", "lessonnums5"),
      numberedPoint("Implement error handling for robust operation", "lessonnums5"),
      numberedPoint("Test and validate their project under different conditions", "lessonnums5"),
      numberedPoint("Document and present their project to peers", "lessonnums5"),
      spacer(),
      
      heading2("Project Options (Choose One)"),
      heading3("Option A: Battery Health Monitor"),
      para("Create a system that monitors battery voltage and current, calculates remaining capacity, and provides visual/audio alerts when battery is low."),
      bulletPoint("Required functions: get_input_voltage(), get_input_current(), get_amp_hours_charged()"),
      bulletPoint("Deliverable: Dashboard showing battery status with warnings"),
      spacer(),
      
      heading3("Option B: Performance Analyzer"),
      para("Build a data logger that records motor performance over time and generates statistics (average speed, peak current, efficiency)."),
      bulletPoint("Required functions: get_rpm(), get_motor_current(), get_watt_hours_consumed()"),
      bulletPoint("Deliverable: Graph of performance data with calculated statistics"),
      spacer(),
      
      heading3("Option C: Temperature Safety System"),
      para("Design an automatic safety system that monitors temperatures and reduces motor power if overheating is detected."),
      bulletPoint("Required functions: get_fet_temperature(), get_motor_temperature(), set_duty_cycle()"),
      bulletPoint("Deliverable: Working thermal protection with staged responses"),
      spacer(),
      
      heading3("Option D: Custom Project (Teacher Approval Required)"),
      para("Design your own project using any combination of VESC functions. Must be approved by teacher before starting."),
      spacer(),
      
      heading2("Project Requirements"),
      bulletPoint("Must use at least 3 different VESC read functions"),
      bulletPoint("Must include at least one form of output (display, buzzer, or motor control)"),
      bulletPoint("Must include error handling for disconnection scenarios"),
      bulletPoint("Must include code comments explaining each section"),
      bulletPoint("Must complete the documentation template in the notebook"),
      spacer(),
      
      heading2("Evaluation Rubric"),
      createTable(
        ["Criteria", "Points", "Description"],
        [
          ["Functionality", "30", "Project works as intended without errors"],
          ["Code Quality", "20", "Clean code with comments, proper variable names"],
          ["Error Handling", "15", "Gracefully handles edge cases and disconnections"],
          ["Creativity", "15", "Original approach or extension beyond minimum requirements"],
          ["Documentation", "20", "Complete project description, explains how it works"]
        ],
        [2500, 1000, 5860]
      ),
      
      // PAGE BREAK - MODULE 6
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 6: AI Introduction"),
      boldPara("Day: ", "6 of 10"),
      boldPara("Duration: ", "45 minutes"),
      boldPara("Prerequisites: ", "Modules 1-5 completed"),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this lesson, students will be able to:"),
      numberedPoint("Define artificial intelligence and explain how it differs from traditional programming"),
      numberedPoint("Describe how neural networks process visual information (at a conceptual level)"),
      numberedPoint("Explain what a confidence score represents and why it matters"),
      numberedPoint("Identify the key components of the IMX500 AI camera system"),
      numberedPoint("Understand the journey from light to decision (photon to action)"),
      spacer(),
      
      heading2("PowerPoint Slide Outline (15 slides)"),
      createTable(
        ["Slide #", "Title", "Content"],
        [
          ["1", "Title Slide", "Introduction to Artificial Intelligence"],
          ["2", "What is AI?", "Definition, examples in everyday life (phones, cars, games)"],
          ["3", "AI vs Traditional Code", "If-then rules vs learning from examples"],
          ["4", "How Humans See", "Eyes capture light, brain interprets, we recognize objects"],
          ["5", "How AI Sees", "Camera captures pixels, neural network processes, outputs labels"],
          ["6", "Neural Networks (Simple)", "Layers that transform data, inspired by brain neurons"],
          ["7", "Training AI", "Learning from thousands of labeled examples"],
          ["8", "The IMX500 Camera", "Special: AI processing happens ON the sensor chip"],
          ["9", "Edge AI Advantage", "Fast, private, low power - no cloud needed"],
          ["10", "What Can It Detect?", "80 object types from COCO dataset (preview)"],
          ["11", "Confidence Scores", "How sure is the AI? 0.0 to 1.0 scale"],
          ["12", "Interpreting Confidence", "High (0.8+) = reliable, Medium (0.5-0.8) = cautious, Low = ignore"],
          ["13", "Bounding Boxes", "How AI shows WHERE objects are located"],
          ["14", "From Light to Action", "Complete pipeline diagram: Light -> Sensor -> AI -> Action"],
          ["15", "Summary + Preview", "Key concepts, preview of hands-on detection tomorrow"]
        ],
        [1000, 2500, 5860]
      ),
      spacer(),
      
      heading2("Jupyter Notebook Structure"),
      heading3("Section 1: AI Concepts (4 cells)"),
      bulletPoint("Markdown: Introduction with AI examples students already use"),
      bulletPoint("EXERCISE: Match AI application to everyday device (smartphone, car, etc.)"),
      bulletPoint("Markdown: Traditional programming vs AI comparison"),
      bulletPoint("EXERCISE: Write a traditional if-then rule to detect a cat (demonstrate why AI is needed)"),
      spacer(),
      
      heading3("Section 2: Confidence Score Simulator (4 cells)"),
      bulletPoint("Markdown: Explanation of confidence scores"),
      bulletPoint("Code: Simulated detection with different confidence levels"),
      bulletPoint("EXERCISE: Predict which detections should be trusted (given confidence values)"),
      bulletPoint("EXERCISE: Fill in code to filter detections below 0.5 confidence"),
      spacer(),
      
      heading3("Section 3: Understanding Detection Results (3 cells)"),
      bulletPoint("Markdown: Bounding box coordinates explained (x, y, width, height)"),
      bulletPoint("Code: Example detection result structure (simulated)"),
      bulletPoint("EXERCISE: Calculate the center point of a bounding box given coordinates"),
      spacer(),
      
      heading3("Section 4: Knowledge Check (2 cells)"),
      bulletPoint("EXERCISE: Fill in the blank - What does a confidence score of 0.85 mean?"),
      bulletPoint("EXERCISE: Short answer - Why is edge AI (processing on camera) better for a skateboard?"),
      
      // PAGE BREAK - MODULE 7
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 7: Object Detection"),
      boldPara("Day: ", "7 of 10"),
      boldPara("Duration: ", "45 minutes"),
      boldPara("Prerequisites: ", "Modules 1-6 completed"),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this lesson, students will be able to:"),
      numberedPoint("Start a live camera feed from the IMX500 AI camera"),
      numberedPoint("Run real-time object detection and view bounding boxes"),
      numberedPoint("Identify which of the 80 COCO objects the camera can detect"),
      numberedPoint("Filter detection results by confidence threshold"),
      numberedPoint("Understand factors that affect detection accuracy (lighting, distance, angle)"),
      spacer(),
      
      heading2("PowerPoint Slide Outline (12 slides)"),
      createTable(
        ["Slide #", "Title", "Content"],
        [
          ["1", "Title Slide", "Your First Object Detection"],
          ["2", "Review: AI Concepts", "Quick recap of confidence scores and bounding boxes"],
          ["3", "The COCO Dataset", "80 objects the AI knows: people, animals, vehicles, etc."],
          ["4", "Object Categories", "People, vehicles, animals, household items, food, sports"],
          ["5", "Starting the Camera", "libcamera-vid command, video streaming basics"],
          ["6", "Detection Pipeline", "Diagram: Camera -> AI Chip -> Results -> Display"],
          ["7", "Reading Detection Results", "Object name, confidence, bounding box coordinates"],
          ["8", "Confidence Thresholds", "Filtering out low-confidence false positives"],
          ["9", "Factors Affecting Accuracy", "Lighting, distance, angle, occlusion, motion blur"],
          ["10", "Testing Different Objects", "What to try detecting in the classroom"],
          ["11", "Common Issues", "Troubleshooting: no detections, wrong labels, slow response"],
          ["12", "Summary + Hands-On", "Key points, excitement for live detection"]
        ],
        [1000, 2500, 5860]
      ),
      spacer(),
      
      heading2("Jupyter Notebook Structure"),
      heading3("Section 1: Camera Basics (3 cells)"),
      bulletPoint("Markdown: Camera setup verification"),
      bulletPoint("Code: Start camera feed with stop button"),
      bulletPoint("EXERCISE: Verify camera is working, count how long until image appears"),
      spacer(),
      
      heading3("Section 2: Live Object Detection (5 cells)"),
      bulletPoint("Markdown: Introduction to detection code"),
      bulletPoint("Code: Detection with bounding boxes (complete working code)"),
      bulletPoint("EXERCISE: Point camera at different objects, record what was detected"),
      bulletPoint("EXERCISE: Find 5 objects that ARE in the COCO dataset"),
      bulletPoint("EXERCISE: Find 3 objects that are NOT detected (understand limitations)"),
      spacer(),
      
      heading3("Section 3: Filtering Detections (4 cells)"),
      bulletPoint("Code: Show all detections with confidence scores"),
      bulletPoint("Code: Filter to only show confidence > 0.7"),
      bulletPoint("EXERCISE: Modify threshold to 0.5 and compare results"),
      bulletPoint("EXERCISE: Fill in code to only show detections of a specific object type"),
      spacer(),
      
      heading3("Section 4: Knowledge Check (2 cells)"),
      bulletPoint("EXERCISE: Complete the table - object tested, detected (Y/N), confidence"),
      bulletPoint("EXERCISE: Short answer - What conditions make detection more reliable?"),
      
      // PAGE BREAK - MODULE 8
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 8: AI + Hardware Integration"),
      boldPara("Day: ", "8 of 10"),
      boldPara("Duration: ", "45 minutes"),
      boldPara("Prerequisites: ", "Modules 1-7 completed"),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this lesson, students will be able to:"),
      numberedPoint("Control a buzzer using GPIO pins on the Raspberry Pi"),
      numberedPoint("Trigger hardware alerts based on AI detection events"),
      numberedPoint("Implement cooldown logic to prevent alert spam"),
      numberedPoint("Create custom alert patterns (beep sequences) for different objects"),
      numberedPoint("Build a complete detection-to-alert pipeline"),
      spacer(),
      
      heading2("PowerPoint Slide Outline (12 slides)"),
      createTable(
        ["Slide #", "Title", "Content"],
        [
          ["1", "Title Slide", "Making AI Physical: Hardware Alerts"],
          ["2", "GPIO Introduction", "General Purpose Input/Output pins on Pi"],
          ["3", "The Buzzer", "How it works, positive/negative, which GPIO pin"],
          ["4", "Basic GPIO Control", "RPi.GPIO library, setup, output high/low"],
          ["5", "Testing the Buzzer", "Simple on/off test before AI integration"],
          ["6", "Detection + Action", "If person detected with confidence > 0.7, beep"],
          ["7", "Alert Spam Problem", "Detecting same object every frame = constant beeping"],
          ["8", "Cooldown Logic", "Only alert once per N seconds for same object"],
          ["9", "Custom Patterns", "Different beep sequences for different objects"],
          ["10", "Complete Pipeline", "Flowchart: Detection -> Filter -> Cooldown -> Alert"],
          ["11", "Real-World Applications", "Security systems, accessibility aids, safety alerts"],
          ["12", "Summary + Hands-On", "Key concepts, preview of creating custom alerts"]
        ],
        [1000, 2500, 5860]
      ),
      spacer(),
      
      heading2("Jupyter Notebook Structure"),
      heading3("Section 1: GPIO Basics (4 cells)"),
      bulletPoint("Markdown: GPIO pin diagram and buzzer wiring"),
      bulletPoint("Code: Simple buzzer on/off test (no AI yet)"),
      bulletPoint("EXERCISE: Modify code to beep 3 times with 0.5s between"),
      bulletPoint("EXERCISE: Create a pattern (short-short-long like SOS)"),
      spacer(),
      
      heading3("Section 2: Detection-Triggered Alerts (5 cells)"),
      bulletPoint("Markdown: Connecting AI detection to buzzer"),
      bulletPoint("Code: Complete detection + alert system (single object)"),
      bulletPoint("EXERCISE: Change target object from person to cell phone"),
      bulletPoint("EXERCISE: Change confidence threshold to 0.6"),
      bulletPoint("Code: Add cooldown to prevent spam"),
      spacer(),
      
      heading3("Section 3: Custom Alert Patterns (3 cells)"),
      bulletPoint("Markdown: Different patterns for different objects"),
      bulletPoint("Code: Dictionary mapping objects to beep patterns"),
      bulletPoint("EXERCISE: Add your own object with custom pattern"),
      spacer(),
      
      heading3("Section 4: Knowledge Check (2 cells)"),
      bulletPoint("EXERCISE: Fill in the blank code for complete alert system"),
      bulletPoint("EXERCISE: Short answer - Why is cooldown logic important?"),
      
      // PAGE BREAK - MODULE 9
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 9: System Integration"),
      boldPara("Day: ", "9 of 10"),
      boldPara("Duration: ", "45 minutes"),
      boldPara("Prerequisites: ", "Modules 1-8 completed"),
      spacer(),
      
      calloutBox("Integration Module",
        "This lesson brings together everything learned: CAN bus communication with the VESC motor controller AND AI camera detection. Students will build a smart safety system.",
        colors.infoBg),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this lesson, students will be able to:"),
      numberedPoint("Combine VESC telemetry reading with AI object detection"),
      numberedPoint("Create conditional logic that uses both data sources"),
      numberedPoint("Build a safety system that responds to both speed AND visual detection"),
      numberedPoint("Understand multi-sensor fusion concepts"),
      numberedPoint("Handle timing and synchronization between different data sources"),
      spacer(),
      
      heading2("PowerPoint Slide Outline (12 slides)"),
      createTable(
        ["Slide #", "Title", "Content"],
        [
          ["1", "Title Slide", "System Integration: AI Meets Motor Control"],
          ["2", "Review: What We Have", "CAN bus (motor data) + AI camera (visual data)"],
          ["3", "Why Combine?", "Neither alone is enough - need context"],
          ["4", "Example Scenario", "Person detected + skateboard moving = danger"],
          ["5", "Integration Architecture", "Diagram showing both data streams merging"],
          ["6", "Timing Challenges", "Motor data: 10Hz, AI: 5-10fps, synchronization"],
          ["7", "Conditional Logic", "IF person detected AND RPM > 1000 THEN alert"],
          ["8", "Safety Response Levels", "Level 1: Alert only, Level 2: Slow down, Level 3: Stop"],
          ["9", "The Smart Safety System", "Complete system we will build today"],
          ["10", "Data Freshness", "Checking if data is stale (too old to trust)"],
          ["11", "Real-World Comparison", "How cars combine radar, cameras, and sensors"],
          ["12", "Summary + Hands-On", "Preparing for the integrated system build"]
        ],
        [1000, 2500, 5860]
      ),
      spacer(),
      
      heading2("Jupyter Notebook Structure"),
      heading3("Section 1: Combining Data Sources (4 cells)"),
      bulletPoint("Code: Initialize both VESC API and camera"),
      bulletPoint("Code: Read motor speed and detection results in same loop"),
      bulletPoint("EXERCISE: Print both RPM and detection count on same line"),
      bulletPoint("EXERCISE: Calculate how many detections occur per second"),
      spacer(),
      
      heading3("Section 2: Conditional Safety Logic (5 cells)"),
      bulletPoint("Markdown: Introduction to multi-condition logic"),
      bulletPoint("Code: Alert only if person detected AND moving"),
      bulletPoint("EXERCISE: Add voltage check - only alert if battery > 20V"),
      bulletPoint("Code: Implement 3 safety levels based on speed"),
      bulletPoint("EXERCISE: Customize the speed thresholds for each level"),
      spacer(),
      
      heading3("Section 3: Complete Safety System (3 cells)"),
      bulletPoint("Code: Full smart safety system with dashboard"),
      bulletPoint("EXERCISE: Add temperature monitoring to the system"),
      bulletPoint("EXERCISE: Add a manual override button using keyboard"),
      spacer(),
      
      heading3("Section 4: Knowledge Check (2 cells)"),
      bulletPoint("EXERCISE: Fill in missing conditional logic for safety system"),
      bulletPoint("EXERCISE: Short answer - What other sensors could improve this system?"),
      
      // PAGE BREAK - MODULE 10 (PROJECT DAY 2)
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 10: AI Capstone Project"),
      boldPara("Day: ", "10 of 10"),
      boldPara("Duration: ", "45 minutes (may extend)"),
      boldPara("Prerequisites: ", "Modules 1-9 completed"),
      spacer(),
      
      calloutBox("Capstone Project 2",
        "Students will design and implement an open-ended project that integrates AI camera detection with CAN bus motor communication. This is the final project demonstrating mastery of the complete system.",
        colors.infoBg),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this project, students will be able to:"),
      numberedPoint("Design a complete integrated system using AI vision and motor data"),
      numberedPoint("Implement robust error handling for multiple failure modes"),
      numberedPoint("Create user feedback through multiple channels (visual, audio, motor)"),
      numberedPoint("Test their system under realistic operating conditions"),
      numberedPoint("Document and demonstrate their complete project"),
      spacer(),
      
      heading2("Project Options (Choose One)"),
      heading3("Option A: Autonomous Safety Assistant"),
      para("Create a comprehensive safety system that detects hazards (people, vehicles, stop signs) and automatically adjusts skateboard behavior based on speed and detection confidence."),
      bulletPoint("Required: AI detection, motor speed reading, buzzer alerts, speed limiting"),
      bulletPoint("Deliverable: Working safety system with demonstration video"),
      spacer(),
      
      heading3("Option B: Smart Parking Helper"),
      para("Build a parking assist system that detects obstacles and provides audio feedback based on distance (estimated from bounding box size) while moving slowly."),
      bulletPoint("Required: Object detection, bounding box analysis, progressive alerts, low-speed monitoring"),
      bulletPoint("Deliverable: Parking assistant with proximity-based beeping"),
      spacer(),
      
      heading3("Option C: Traffic Monitor"),
      para("Create a system that counts and classifies detected objects (people, cars, bicycles) while recording motor performance data for later analysis."),
      bulletPoint("Required: Multi-object detection, counting logic, data logging, visualization"),
      bulletPoint("Deliverable: Traffic report with statistics and graphs"),
      spacer(),
      
      heading3("Option D: Custom Integrated Project (Teacher Approval Required)"),
      para("Design your own project that meaningfully combines AI detection with motor control or monitoring. Must demonstrate understanding of both systems."),
      spacer(),
      
      heading2("Project Requirements"),
      bulletPoint("Must use at least 3 AI-related functions (detection, filtering, etc.)"),
      bulletPoint("Must use at least 3 VESC functions (telemetry reads or motor control)"),
      bulletPoint("Must include meaningful conditional logic combining both data sources"),
      bulletPoint("Must include error handling for camera and CAN disconnection"),
      bulletPoint("Must include user feedback (display, buzzer, or both)"),
      bulletPoint("Must complete documentation with architecture diagram"),
      spacer(),
      
      heading2("Evaluation Rubric"),
      createTable(
        ["Criteria", "Points", "Description"],
        [
          ["Integration Quality", "30", "AI and CAN systems work together meaningfully"],
          ["Functionality", "25", "Project works as intended under test conditions"],
          ["Code Quality", "15", "Clean code, good structure, clear comments"],
          ["Error Handling", "15", "Handles disconnections, bad data, edge cases"],
          ["Documentation", "15", "Clear explanation, architecture diagram, demo"]
        ],
        [2500, 1000, 5860]
      ),
      
      // PAGE BREAK - IMPLEMENTATION GUIDE
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Implementation Guide"),
      
      heading2("File Structure"),
      para("The new curriculum should be organized as follows:"),
      spacer(),
      
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [9360],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 9360, type: WidthType.DXA },
                shading: { fill: colors.light, type: ShadingType.CLEAR },
                margins: { top: 120, bottom: 120, left: 200, right: 200 },
                children: [
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "Curriculum/", bold: true, size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "  00_Python_Reference/", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "    Python_Quick_Reference.ipynb", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "  01_System_Introduction/", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "    Teacher_Slides_01.pptx", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "    Student_Notebook_01.ipynb", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "    Answer_Key_01.ipynb", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "  02_CAN_Fundamentals/", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "    Teacher_Slides_02.pptx", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "    Student_Notebook_02.ipynb", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "    Answer_Key_02.ipynb", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "  ... (03-10 follow same pattern)", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "  Resources/", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "    Hardware_Setup_Guide.pdf", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "    Troubleshooting_Guide.pdf", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "    COCO_Object_Reference.pdf", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "    VESC_Function_Reference.pdf", size: 20, font: "Courier New" })] }),
                ]
              })
            ]
          })
        ]
      }),
      spacer(),
      
      heading2("Notebook Design Standards"),
      para("All student notebooks must follow these standards:"),
      spacer(),
      
      heading3("Cell Structure"),
      bulletPoint("Every code cell must have a preceding markdown cell explaining the purpose"),
      bulletPoint("Exercise cells clearly marked with bold EXERCISE: prefix"),
      bulletPoint("Fill-in-the-blank code uses # YOUR CODE HERE comment"),
      bulletPoint("Expected output shown in markdown after exercises"),
      spacer(),
      
      heading3("Exercise Types"),
      createTable(
        ["Type", "Frequency", "Example"],
        [
          ["Fill-in-the-blank code", "2-3 per lesson", "vesc.get_____() # Read motor temperature"],
          ["Prediction exercise", "1 per lesson", "Before running, predict what RPM will show"],
          ["Modification task", "1-2 per lesson", "Change the threshold from 0.7 to 0.5"],
          ["Short answer question", "1-2 per lesson", "Why is regenerative braking useful?"],
          ["Matching exercise", "1 per lesson", "Match function to measurement type"]
        ],
        [2500, 1500, 5360]
      ),
      spacer(),
      
      heading3("Error Handling"),
      para("All code that interacts with hardware must include try/except blocks with student-friendly error messages:"),
      spacer(),
      
      new Table({
        width: { size: 100, type: WidthType.PERCENTAGE },
        columnWidths: [9360],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 9360, type: WidthType.DXA },
                shading: { fill: colors.light, type: ShadingType.CLEAR },
                margins: { top: 120, bottom: 120, left: 200, right: 200 },
                children: [
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "try:", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "    rpm = vesc.get_rpm()", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "except ConnectionError:", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "    print(\"Oops! Lost connection to motor controller.\")", size: 20, font: "Courier New" })] }),
                  new Paragraph({ children: [new TextRun({ text: "    print(\"Check that the CAN cable is connected.\")", size: 20, font: "Courier New" })] }),
                ]
              })
            ]
          })
        ]
      }),
      spacer(),
      
      heading2("PowerPoint Design Standards"),
      bulletPoint("Maximum 15 slides per lesson (12-15 typical)"),
      bulletPoint("Consistent color scheme matching this document (blues/greens)"),
      bulletPoint("Large diagrams and visuals, minimal text bullets"),
      bulletPoint("Speaker notes for teachers in each slide"),
      bulletPoint("Discussion questions embedded to encourage participation"),
      bulletPoint("Real photos of hardware components where applicable"),
      spacer(),
      
      heading2("Assessment Strategy"),
      heading3("Formative Assessment (During Each Lesson)"),
      bulletPoint("Fill-in-the-blank exercises provide immediate feedback"),
      bulletPoint("Prediction exercises reveal misconceptions"),
      bulletPoint("Teacher can observe notebook progress in real-time"),
      spacer(),
      
      heading3("Summative Assessment (Capstone Projects)"),
      bulletPoint("Project 1 (Day 5): CAN-only project, 100 points"),
      bulletPoint("Project 2 (Day 10): Integrated AI + CAN project, 100 points"),
      bulletPoint("Optional: Written quiz at end of CAN section and end of AI section"),
      
      // PAGE BREAK - APPENDIX
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Appendix A: Complete Function Reference"),
      para("Students should have access to this reference throughout the course."),
      spacer(),
      
      heading2("VESC Controller Functions (18)"),
      createTable(
        ["Function", "Returns", "Description"],
        [
          ["get_rpm()", "Integer", "Motor rotations per minute (+ forward, - reverse)"],
          ["get_motor_current()", "Float (A)", "Current flowing through motor windings"],
          ["get_duty_cycle()", "Float (-1 to 1)", "Throttle percentage (0.5 = 50% forward)"],
          ["get_input_voltage()", "Float (V)", "Battery voltage (always returns real data)"],
          ["get_input_current()", "Float (A)", "Current from battery (- = regenerating)"],
          ["get_amp_hours_consumed()", "Float (Ah)", "Total energy used since reset"],
          ["get_amp_hours_charged()", "Float (Ah)", "Energy recovered via regeneration"],
          ["get_watt_hours_consumed()", "Float (Wh)", "Energy used in watt-hours"],
          ["get_watt_hours_charged()", "Float (Wh)", "Energy recovered in watt-hours"],
          ["get_fet_temperature()", "Float (°C)", "Power transistor temperature"],
          ["get_motor_temperature()", "Float (°C)", "Motor winding temperature"],
          ["get_tachometer()", "Integer", "Total rotations since startup"],
          ["get_pid_position()", "Float", "Current position in PID mode"],
          ["get_adc1_value()", "Float", "Analog input 1 (0.0 to 3.3)"],
          ["get_adc2_value()", "Float", "Analog input 2 (0.0 to 3.3)"],
          ["get_servo_value()", "Float", "Servo output position"],
          ["set_duty_cycle(value)", "None", "Set motor throttle (-1.0 to 1.0)"],
          ["set_current(amps)", "None", "Set motor current (-100 to 100 A)"],
          ["set_brake_current(amps)", "None", "Apply regenerative braking (0-100 A)"]
        ],
        [3000, 1500, 4860]
      ),
      spacer(),
      
      heading2("AI Camera Functions"),
      para("Functions available through the camera detection system:"),
      createTable(
        ["Concept", "Description"],
        [
          ["Detection result", "Dictionary with: label (string), confidence (float 0-1), bbox (x,y,w,h)"],
          ["Bounding box", "Rectangle showing object location: x, y, width, height in pixels"],
          ["Confidence score", "AI certainty: 0.8+ = high, 0.5-0.8 = medium, <0.5 = low"],
          ["COCO labels", "80 object types: person, car, dog, cat, chair, phone, etc."],
          ["Filtering", "Removing detections below confidence threshold"],
          ["Cooldown", "Preventing repeated alerts for same object"]
        ],
        [2500, 6860]
      ),
      spacer(),
      
      heading2("COCO Dataset Objects (80 types)"),
      para("People: person"),
      para("Vehicles: bicycle, car, motorcycle, airplane, bus, train, truck, boat"),
      para("Animals: bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe"),
      para("Accessories: backpack, umbrella, handbag, tie, suitcase"),
      para("Sports: frisbee, skis, snowboard, sports ball, kite, baseball bat, baseball glove, skateboard, surfboard, tennis racket"),
      para("Kitchen: bottle, wine glass, cup, fork, knife, spoon, bowl"),
      para("Food: banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake"),
      para("Furniture: chair, couch, potted plant, bed, dining table, toilet"),
      para("Electronics: tv, laptop, mouse, remote, keyboard, cell phone"),
      para("Household: microwave, oven, toaster, sink, refrigerator, book, clock, vase, scissors, teddy bear, hair drier, toothbrush"),
      para("Outdoor: traffic light, fire hydrant, stop sign, parking meter, bench"),
      
      // FINAL PAGE
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Next Steps"),
      para("This curriculum plan document provides the complete structure for the redesigned course. Implementation should proceed in the following order:"),
      spacer(),
      
      numberedPoint("Create Python Quick Reference notebook (Module 00)"),
      numberedPoint("Create Module 1 PowerPoint and Student Notebook as template"),
      numberedPoint("Create remaining CAN modules (2-5) including Project 1"),
      numberedPoint("Create AI modules (6-10) including Project 2"),
      numberedPoint("Create teacher answer keys for all notebooks"),
      numberedPoint("Create supplementary resource PDFs"),
      numberedPoint("Pilot test with small group, gather feedback"),
      numberedPoint("Revise based on feedback and finalize"),
      spacer(),
      
      calloutBox("Ready to Implement",
        "Upon approval of this plan, I can begin creating the actual PowerPoint slides and Jupyter notebooks following this structure. Each module will take approximately 2-3 hours to fully develop with all interactive elements, answer keys, and teacher notes.",
        colors.successBg),
      spacer(),
      
      para("Document prepared for Lectec Electric Skateboard Educational Program.", { italics: true, color: "666666" }),
    ]
  }]
});

// Generate document
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/sessions/beautiful-brave-hopper/mnt/RaspberryPi-CAN/Lectec_Curriculum_Plan.docx", buffer);
  console.log("Document created successfully!");
});
