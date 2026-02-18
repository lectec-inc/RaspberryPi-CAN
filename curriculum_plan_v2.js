const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, LevelFormat, HeadingLevel,
        BorderStyle, WidthType, ShadingType, PageNumber, PageBreak } = require('docx');
const fs = require('fs');

// Color palette
const colors = {
  primary: "1E3A5F",
  secondary: "2E7D32",
  accent: "E65100",
  light: "F5F5F5",
  headerBg: "1E3A5F",
  tableBorder: "CCCCCC",
  tableHeader: "E8EEF4",
  tableAlt: "F8FAFB",
  warningBg: "FFF3E0",
  successBg: "E8F5E9",
  infoBg: "E3F2FD",
  adasBg: "F3E5F5"
};

const border = { style: BorderStyle.SINGLE, size: 1, color: colors.tableBorder };
const borders = { top: border, bottom: border, left: border, right: border };

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

const endGoalBox = (title, content) => {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    columnWidths: [9360],
    rows: [
      new TableRow({
        children: [
          new TableCell({
            borders: { 
              top: { style: BorderStyle.SINGLE, size: 2, color: colors.secondary },
              bottom: { style: BorderStyle.SINGLE, size: 2, color: colors.secondary },
              left: { style: BorderStyle.SINGLE, size: 2, color: colors.secondary },
              right: { style: BorderStyle.SINGLE, size: 2, color: colors.secondary }
            },
            width: { size: 9360, type: WidthType.DXA },
            shading: { fill: colors.successBg, type: ShadingType.CLEAR },
            margins: { top: 120, bottom: 120, left: 200, right: 200 },
            children: [
              new Paragraph({
                spacing: { after: 80 },
                children: [new TextRun({ text: "🎯 " + title, bold: true, size: 24, font: "Arial", color: colors.secondary })]
              }),
              new Paragraph({
                children: [new TextRun({ text: content, size: 21, font: "Arial" })]
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

// Create numbered list references for each module
const numberingConfig = [
  { reference: "bullets", levels: [
    { level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
    { level: 1, format: LevelFormat.BULLET, text: "\u25E6", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1080, hanging: 360 } } } }
  ]},
  { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
];

// Add numbered references for each module
for (let i = 1; i <= 14; i++) {
  numberingConfig.push({
    reference: `lesson${i}`,
    levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }]
  });
}

// Document content
const doc = new Document({
  numbering: { config: numberingConfig },
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
          children: [new TextRun({ text: "Lectec Electric Skateboard Curriculum Plan v2.0", italics: true, size: 18, font: "Arial", color: "666666" })]
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
      // ============ TITLE PAGE ============
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
        children: [new TextRun({ text: "CAN Network Communication, AI Vision Systems & ADAS", size: 28, font: "Arial", color: "555555" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 600 },
        children: [new TextRun({ text: "Raspberry Pi + IMX500 AI Camera + VESC Motor Controller", size: 24, font: "Arial", color: "777777" })]
      }),
      spacer(),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "A Comprehensive 14-Day Course for High School Students", size: 24, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "10 Core Modules + 4-Day ADAS Bonus Module", size: 22, font: "Arial", color: "666666" })]
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
      
      // ============ EXECUTIVE SUMMARY ============
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Executive Summary"),
      para("This document outlines a comprehensive restructuring of the Lectec Electric Skateboard educational curriculum. The redesign transforms the existing Jupyter notebook tutorials into a cohesive 14-day course with professional PowerPoint presentations, interactive student notebooks, three capstone projects, and a complete ADAS (Advanced Driver Assistance Systems) bonus module."),
      spacer(),
      
      heading2("Design Philosophy: Start with the End in Mind"),
      calloutBox("Core Principle",
        "Every single lesson begins by showing students WHAT THEY WILL BUILD by the end of that lesson. Before any theory or concepts, students see a compelling demonstration or description of their end goal. This creates motivation, provides context for learning, and gives students a clear target to work toward.",
        colors.infoBg),
      spacer(),
      
      para("This approach is based on proven educational research showing that students learn better when they:"),
      bulletPoint("Understand WHY they are learning something before HOW"),
      bulletPoint("Can visualize the end result before starting the journey"),
      bulletPoint("Have a concrete goal that makes abstract concepts tangible"),
      bulletPoint("Feel excited about what they will accomplish"),
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
          ["Motivation", "Lessons start with theory instead of showing the goal", "Students don't know WHY they're learning concepts"],
          ["Progression", "No clear bridge between CAN fundamentals and AI integration", "Students struggle to connect concepts"],
          ["Teacher Support", "No presentation materials for classroom instruction", "Teachers must create their own content"],
          ["Assessment", "No structured quizzes or knowledge checks", "No way to verify student understanding"],
          ["Project Guidance", "Capstone projects provide only empty scaffolding", "Students overwhelmed by blank slate approach"],
          ["ADAS Coverage", "No coverage of automotive industry applications", "Missed opportunity for real-world context"]
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
      
      // ============ COURSE OVERVIEW ============
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Course Overview"),
      
      heading2("Target Audience"),
      bulletPoint("Age: High School students (14-18 years)"),
      bulletPoint("Prerequisites: Basic Python syntax (quick reference provided, not taught)"),
      bulletPoint("Setting: Structured classroom with teacher-led instruction"),
      bulletPoint("Hardware: Raspberry Pi Zero 2W with IMX500 AI Camera on electric skateboard/scooter"),
      spacer(),
      
      heading2("Course Structure: 14 Days"),
      createTable(
        ["Day", "Module", "End Goal (What Students Build)", "Focus Area"],
        [
          ["1", "System Introduction", "Working connection to motor controller", "Hardware, safety, first data"],
          ["2", "CAN Fundamentals", "Read ALL motor telemetry values", "Complete telemetry mastery"],
          ["3", "Data Visualization", "Custom real-time dashboard", "Graphs and displays"],
          ["4", "Motor Control", "Safe motor control sequence", "Duty cycle, current, braking"],
          ["5", "CAN Capstone", "COMPLETE CAN PROJECT", "Open-ended project #1"],
          ["6", "AI Introduction", "AI confidence interpreter", "Neural networks, confidence"],
          ["7", "Object Detection", "Live multi-object detector", "Bounding boxes, COCO"],
          ["8", "AI + Hardware", "Detection-triggered alert system", "GPIO, buzzer integration"],
          ["9", "System Integration", "Smart safety monitor", "AI + CAN combined"],
          ["10", "AI Capstone", "COMPLETE INTEGRATED PROJECT", "Open-ended project #2"],
          ["11", "ADAS Introduction", "ADAS feature comparison chart", "Industry, SAE levels"],
          ["12", "ADAS Theory", "Time-to-collision calculator", "FCW, sensor fusion"],
          ["13", "ADAS Implementation", "Forward Collision Warning system", "Complete FCW build"],
          ["14", "ADAS Capstone", "COMPLETE ADAS PROJECT", "Open-ended project #3"]
        ],
        [600, 1800, 3500, 3460]
      ),
      spacer(),
      
      heading2("Time Allocation per Lesson"),
      createTable(
        ["Segment", "Duration", "Purpose"],
        [
          ["Hook: Show the End Goal", "5 minutes", "Demonstrate what students will build TODAY"],
          ["Teacher Presentation", "12 minutes", "Introduce concepts using PowerPoint slides"],
          ["Guided Practice", "20 minutes", "Students work through Jupyter notebook exercises"],
          ["Knowledge Check", "5 minutes", "Fill-in-the-blank code and reflection questions"],
          ["Wrap-up / Preview", "3 minutes", "Summary and exciting preview of next lesson"]
        ],
        [2500, 1500, 5360]
      ),
      spacer(),
      
      calloutBox("The 5-Minute Hook",
        "Every lesson begins with a 5-minute demonstration or description of exactly what students will accomplish by the end of class. For example, Day 7 starts with the teacher showing a live object detection feed with bounding boxes - then says 'In 40 minutes, you will build this yourself.' This creates immediate engagement and motivation.",
        colors.successBg),
      
      // ============ MODULE 1 ============
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 1: System Introduction"),
      boldPara("Day: ", "1 of 14"),
      boldPara("Duration: ", "45 minutes"),
      boldPara("Prerequisites: ", "None"),
      spacer(),
      
      endGoalBox("BY THE END OF THIS LESSON, YOU WILL HAVE:",
        "A working connection to a real motor controller on an electric skateboard. You will read live battery voltage data from the actual vehicle and understand how the entire system communicates. This is your first step toward building an intelligent vehicle system!"),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this lesson, students will be able to:"),
      numberedPoint("Identify the major hardware components of the Lectec electric skateboard system", "lesson1"),
      numberedPoint("Explain the role of the Raspberry Pi as the central controller", "lesson1"),
      numberedPoint("Describe what a CAN bus is and why it is used in vehicles", "lesson1"),
      numberedPoint("Successfully connect to the VESC motor controller and verify communication", "lesson1"),
      numberedPoint("Apply safety protocols when working with electric vehicle systems", "lesson1"),
      spacer(),
      
      heading2("PowerPoint Slide Outline (15 slides)"),
      createTable(
        ["Slide #", "Title", "Content"],
        [
          ["1", "Title Slide", "Your First Intelligent Vehicle System"],
          ["2", "TODAY'S GOAL", "Demo: Show live voltage reading from skateboard - 'You'll do this in 40 min!'"],
          ["3", "What You Will Build This Course", "Video/images of final projects: safety systems, ADAS features"],
          ["4", "The Complete System", "Photo of skateboard with all components labeled"],
          ["5", "The Raspberry Pi", "Mini-computer explanation, why we use it, specifications"],
          ["6", "The VESC Controller", "Motor brain, controls speed/power, communicates over CAN"],
          ["7", "What is CAN Bus?", "Controller Area Network, used in EVERY modern car"],
          ["8", "Why CAN Bus?", "Reliability, noise immunity, multiple devices on one wire"],
          ["9", "The AI Camera (Preview)", "IMX500 sensor - we'll use this starting Day 6!"],
          ["10", "How It All Connects", "System diagram showing data flow between components"],
          ["11", "Safety First", "Electrical safety, moving parts, battery handling"],
          ["12", "Safety Rules", "5 key rules students must follow (with icons)"],
          ["13", "Jupyter Notebooks", "What they are, how to use them, cell types explained"],
          ["14", "Let's Connect!", "Preview of what students will do in the notebook"],
          ["15", "Your Turn", "Transition to hands-on notebook work"]
        ],
        [1000, 2500, 5860]
      ),
      spacer(),
      
      heading2("Jupyter Notebook Structure"),
      heading3("Section 1: Your Mission (2 cells)"),
      bulletPoint("Markdown: YOUR GOAL TODAY - Read live data from a real electric vehicle!"),
      bulletPoint("Markdown: What success looks like (expected output shown)"),
      spacer(),
      
      heading3("Section 2: Connect to the System (4 cells)"),
      bulletPoint("Markdown: Step-by-step connection instructions"),
      bulletPoint("Code: Import and initialize VESCStudentAPI"),
      bulletPoint("Code: Wait for connection with status messages"),
      bulletPoint("EXERCISE: Predict - How long will discovery take? (Answer: ~6 seconds)"),
      spacer(),
      
      heading3("Section 3: Your First Real Data (5 cells)"),
      bulletPoint("Code: Read battery voltage - THIS ALWAYS WORKS!"),
      bulletPoint("Markdown: Celebrate! You just read real vehicle data!"),
      bulletPoint("EXERCISE: What voltage did you get? Write it down: _____V"),
      bulletPoint("Code: Read RPM (will be 0 if motor not moving)"),
      bulletPoint("EXERCISE: Why is RPM zero? Multiple choice question"),
      spacer(),
      
      heading3("Section 4: Knowledge Check (3 cells)"),
      bulletPoint("EXERCISE: Fill in the missing code to read motor temperature"),
      bulletPoint("EXERCISE: Match component to function (5 items)"),
      bulletPoint("Markdown: CONGRATULATIONS! Preview of Day 2"),
      
      // ============ MODULE 2 ============
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 2: CAN Fundamentals"),
      boldPara("Day: ", "2 of 14"),
      boldPara("Duration: ", "45 minutes"),
      boldPara("Prerequisites: ", "Module 1 completed"),
      spacer(),
      
      endGoalBox("BY THE END OF THIS LESSON, YOU WILL HAVE:",
        "Complete mastery of ALL 18 data values available from the motor controller. You will be able to read speed, power, temperature, energy consumption, and more - everything the skateboard knows about itself, you will know too!"),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this lesson, students will be able to:"),
      numberedPoint("Read all 18 available telemetry values from the VESC controller", "lesson2"),
      numberedPoint("Explain the difference between motor data, power data, and temperature data", "lesson2"),
      numberedPoint("Interpret positive and negative values (RPM direction, current flow)", "lesson2"),
      numberedPoint("Use the get_all_telemetry() function to retrieve structured data", "lesson2"),
      numberedPoint("Identify which readings require motor movement vs. which are always available", "lesson2"),
      spacer(),
      
      heading2("PowerPoint Slide Outline (12 slides)"),
      createTable(
        ["Slide #", "Title", "Content"],
        [
          ["1", "Title Slide", "Complete Vehicle Telemetry Mastery"],
          ["2", "TODAY'S GOAL", "Demo: Show get_all_telemetry() output - 'You'll read ALL of this!'"],
          ["3", "Review: Your First Connection", "Quick recap, celebrate yesterday's success"],
          ["4", "The 18 Data Points", "Complete list organized by category"],
          ["5", "Motor Data", "RPM, current, duty cycle - what each means"],
          ["6", "Understanding Direction", "Positive/negative values, forward/reverse"],
          ["7", "Power Data", "Voltage, current flow, energy tracking"],
          ["8", "Temperature Data", "FET and motor temps, why they matter for safety"],
          ["9", "Energy Tracking", "Amp-hours, watt-hours, consumed vs. recovered"],
          ["10", "The Magic Function", "get_all_telemetry() returns EVERYTHING at once"],
          ["11", "When Data is Zero", "Motor not moving = most readings are 0"],
          ["12", "Your Turn", "Transition to reading ALL the data yourself"]
        ],
        [1000, 2500, 5860]
      ),
      spacer(),
      
      heading2("Jupyter Notebook Structure"),
      heading3("Section 1: Your Mission (2 cells)"),
      bulletPoint("Markdown: TODAY - Master all 18 telemetry values!"),
      bulletPoint("Markdown: Checklist of all values you'll read today"),
      spacer(),
      
      heading3("Section 2: Motor Data (5 cells)"),
      bulletPoint("Code: Read RPM, current, duty cycle"),
      bulletPoint("EXERCISE: Spin motor by hand - which values change?"),
      bulletPoint("EXERCISE: Spin in reverse - what happens to RPM sign?"),
      bulletPoint("Code: Display motor data with labels"),
      bulletPoint("EXERCISE: Fill in code to check if motor is moving (RPM != 0)"),
      spacer(),
      
      heading3("Section 3: Power and Temperature (5 cells)"),
      bulletPoint("Code: Voltage, input current, amp-hours, watt-hours"),
      bulletPoint("Code: FET and motor temperature"),
      bulletPoint("EXERCISE: Write code that warns if temp > 50C"),
      bulletPoint("EXERCISE: Calculate power (voltage × current)"),
      bulletPoint("Code: All temperature readings with safety thresholds"),
      spacer(),
      
      heading3("Section 4: Master Function (3 cells)"),
      bulletPoint("Code: get_all_telemetry() complete demonstration"),
      bulletPoint("EXERCISE: Extract motor.rpm from the dictionary"),
      bulletPoint("Markdown: Complete reference table of all 18 functions"),
      spacer(),
      
      heading3("Section 5: Knowledge Check (2 cells)"),
      bulletPoint("EXERCISE: Match function to measurement (8 items)"),
      bulletPoint("EXERCISE: Why might input_current be negative?"),
      
      // ============ MODULE 3 ============
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 3: Data Visualization"),
      boldPara("Day: ", "3 of 14"),
      boldPara("Duration: ", "45 minutes"),
      boldPara("Prerequisites: ", "Modules 1-2 completed"),
      spacer(),
      
      endGoalBox("BY THE END OF THIS LESSON, YOU WILL HAVE:",
        "A custom real-time dashboard that displays live vehicle data with color-coded warnings. Your dashboard will update continuously, showing voltage, temperature, and speed - just like the instrument panel in a car!"),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this lesson, students will be able to:"),
      numberedPoint("Create real-time updating displays using clear_output()", "lesson3"),
      numberedPoint("Build a live dashboard showing multiple data streams", "lesson3"),
      numberedPoint("Plot time-series data using matplotlib", "lesson3"),
      numberedPoint("Implement color-coded warnings based on data thresholds", "lesson3"),
      numberedPoint("Explain why visualization helps identify patterns and problems", "lesson3"),
      spacer(),
      
      heading2("PowerPoint Slide Outline (10 slides)"),
      createTable(
        ["Slide #", "Title", "Content"],
        [
          ["1", "Title Slide", "Building Your Vehicle Dashboard"],
          ["2", "TODAY'S GOAL", "Demo: Show completed dashboard with live updating data"],
          ["3", "Why Visualize?", "Numbers vs. graphs, pattern recognition"],
          ["4", "Real-Time Updates", "clear_output() technique explained"],
          ["5", "Dashboard Design", "What info matters, layout principles"],
          ["6", "Color Coding", "Green = good, yellow = warning, red = danger"],
          ["7", "HTML in Jupyter", "display(HTML(...)) for formatting"],
          ["8", "Time-Series Graphs", "Matplotlib basics for live plots"],
          ["9", "Car Dashboard Comparison", "Photo of real car dashboard - same concept!"],
          ["10", "Your Turn", "Build your own dashboard!"]
        ],
        [1000, 2500, 5860]
      ),
      spacer(),
      
      heading2("Jupyter Notebook Structure"),
      heading3("Section 1: Your Mission (2 cells)"),
      bulletPoint("Markdown: TODAY - Build a live vehicle dashboard!"),
      bulletPoint("Markdown: Screenshot of final dashboard you'll create"),
      spacer(),
      
      heading3("Section 2: Live Updates (4 cells)"),
      bulletPoint("Code: Simple loop with clear_output() showing voltage"),
      bulletPoint("EXERCISE: Modify to update every 0.5 seconds instead of 1"),
      bulletPoint("EXERCISE: Add temperature to the display"),
      bulletPoint("Code: Multi-value live display"),
      spacer(),
      
      heading3("Section 3: Color-Coded Dashboard (5 cells)"),
      bulletPoint("Code: Color function for temperature thresholds"),
      bulletPoint("Code: HTML dashboard template"),
      bulletPoint("EXERCISE: Change warning threshold from 50C to 45C"),
      bulletPoint("EXERCISE: Add a new row for motor current"),
      bulletPoint("Code: Complete dashboard with all values"),
      spacer(),
      
      heading3("Section 4: Graphing (3 cells)"),
      bulletPoint("Code: Collect data for 15 seconds, plot result"),
      bulletPoint("EXERCISE: Plot voltage AND temperature on same graph"),
      bulletPoint("EXERCISE: Add a title and axis labels to your graph"),
      spacer(),
      
      heading3("Section 5: Knowledge Check (2 cells)"),
      bulletPoint("EXERCISE: Fill in code for 4-panel dashboard"),
      bulletPoint("EXERCISE: Why are dashboards important for vehicle safety?"),
      
      // ============ MODULE 4 ============
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 4: Motor Control"),
      boldPara("Day: ", "4 of 14"),
      boldPara("Duration: ", "45 minutes"),
      boldPara("Prerequisites: ", "Modules 1-3 completed"),
      spacer(),
      
      calloutBox("Safety Note",
        "This lesson involves active motor control. Motors must be on secure test stands. Review all safety protocols before ANY motor control code is executed.",
        colors.warningBg),
      spacer(),
      
      endGoalBox("BY THE END OF THIS LESSON, YOU WILL HAVE:",
        "Complete control over the motor - starting it, controlling its speed, and stopping it safely using regenerative braking. You will create a smooth acceleration sequence that gradually speeds up and slows down, just like a real vehicle!"),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this lesson, students will be able to:"),
      numberedPoint("Explain the difference between duty cycle control and current control", "lesson4"),
      numberedPoint("Safely start and stop a motor using set_duty_cycle()", "lesson4"),
      numberedPoint("Apply regenerative braking using set_brake_current()", "lesson4"),
      numberedPoint("Implement proper safety checks before and after motor commands", "lesson4"),
      numberedPoint("Create a controlled acceleration/deceleration sequence", "lesson4"),
      spacer(),
      
      heading2("PowerPoint Slide Outline (12 slides)"),
      createTable(
        ["Slide #", "Title", "Content"],
        [
          ["1", "Title Slide", "Taking Control: Commanding Your Motor"],
          ["2", "TODAY'S GOAL", "Demo: Smooth acceleration sequence - motor speeds up, holds, slows down"],
          ["3", "SAFETY FIRST", "Critical safety rules review, emergency stop procedure"],
          ["4", "Three Control Methods", "Duty cycle, Current, Brake - overview"],
          ["5", "Duty Cycle Control", "Throttle percentage, -1.0 to 1.0 range"],
          ["6", "Current Control", "Force/torque control, measured in Amperes"],
          ["7", "Regenerative Braking", "Motor becomes generator, recovers energy!"],
          ["8", "The Safety Flag", "MOTOR_CONTROL_ENABLED pattern explained"],
          ["9", "Command Sequence", "Flowchart: Check → Command → Verify → Stop"],
          ["10", "Emergency Stop", "set_duty_cycle(0) - memorize this!"],
          ["11", "Real Car Comparison", "How cruise control and ABS work similarly"],
          ["12", "Your Turn (CAREFULLY)", "Build your acceleration sequence"]
        ],
        [1000, 2500, 5860]
      ),
      spacer(),
      
      heading2("Jupyter Notebook Structure"),
      heading3("Section 1: Safety Checklist (3 cells)"),
      bulletPoint("Markdown: MANDATORY safety checklist - must check all boxes"),
      bulletPoint("Code: Verify connection and read initial state"),
      bulletPoint("EXERCISE: Write code to verify motor is stopped before proceeding"),
      spacer(),
      
      heading3("Section 2: Duty Cycle Control (5 cells)"),
      bulletPoint("Markdown: What duty cycle means (throttle percentage)"),
      bulletPoint("Code: set_duty_cycle(0.1) - very slow test"),
      bulletPoint("EXERCISE: Predict RPM before running, then compare"),
      bulletPoint("Code: Read RPM during operation, then stop"),
      bulletPoint("EXERCISE: Modify to 0.15 duty cycle, predict new RPM"),
      spacer(),
      
      heading3("Section 3: Smooth Acceleration (4 cells)"),
      bulletPoint("Markdown: Why gradual acceleration matters"),
      bulletPoint("Code: 5-step acceleration: 0.1 → 0.15 → 0.2 → 0.15 → 0"),
      bulletPoint("EXERCISE: Add two more steps for smoother transition"),
      bulletPoint("EXERCISE: Create deceleration using brake current"),
      spacer(),
      
      heading3("Section 4: Knowledge Check (2 cells)"),
      bulletPoint("EXERCISE: Fill in safety-checked control sequence"),
      bulletPoint("EXERCISE: Why use regenerative braking instead of just stopping?"),
      
      // ============ MODULE 5 ============
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 5: CAN Capstone Project"),
      boldPara("Day: ", "5 of 14"),
      boldPara("Duration: ", "45 minutes (may extend)"),
      boldPara("Prerequisites: ", "Modules 1-4 completed"),
      spacer(),
      
      calloutBox("CAPSTONE PROJECT #1",
        "Students design and implement an open-ended project using CAN bus communication with the VESC motor controller. This demonstrates mastery of everything learned in Days 1-4.",
        colors.infoBg),
      spacer(),
      
      endGoalBox("BY THE END OF THIS LESSON, YOU WILL HAVE:",
        "A complete, working project that YOU designed using motor telemetry data. This could be a battery health monitor, performance analyzer, temperature safety system, or your own creative idea. You will demonstrate it to the class!"),
      spacer(),
      
      heading2("Project Options"),
      heading3("Option A: Battery Health Monitor"),
      para("Monitor voltage, current, and energy consumption. Calculate remaining capacity. Alert when battery is low."),
      bulletPoint("Required: get_input_voltage(), get_input_current(), get_amp_hours_consumed()"),
      spacer(),
      
      heading3("Option B: Performance Analyzer"),
      para("Log motor performance over time. Calculate statistics (average speed, peak current, efficiency)."),
      bulletPoint("Required: get_rpm(), get_motor_current(), get_watt_hours_consumed()"),
      spacer(),
      
      heading3("Option C: Temperature Safety System"),
      para("Monitor temperatures and reduce motor power if overheating is detected."),
      bulletPoint("Required: get_fet_temperature(), get_motor_temperature(), set_duty_cycle()"),
      spacer(),
      
      heading3("Option D: Custom Project"),
      para("Design your own! Must use at least 3 VESC functions and include output/display."),
      spacer(),
      
      heading2("Evaluation Rubric"),
      createTable(
        ["Criteria", "Points", "Description"],
        [
          ["Functionality", "30", "Project works as intended without errors"],
          ["Code Quality", "20", "Clean code with comments, proper variable names"],
          ["Error Handling", "15", "Gracefully handles edge cases"],
          ["Creativity", "15", "Original approach or extension beyond minimum"],
          ["Documentation", "20", "Clear explanation of how it works"]
        ],
        [2500, 1000, 5860]
      ),
      
      // ============ MODULE 6 ============
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 6: AI Introduction"),
      boldPara("Day: ", "6 of 14"),
      boldPara("Duration: ", "45 minutes"),
      boldPara("Prerequisites: ", "Modules 1-5 completed"),
      spacer(),
      
      endGoalBox("BY THE END OF THIS LESSON, YOU WILL HAVE:",
        "A working AI confidence interpreter that you built! You will understand how AI 'thinks,' what confidence scores mean, and why an AI might say it's '87% sure' something is a dog. You'll filter fake detections from real ones using confidence thresholds."),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this lesson, students will be able to:"),
      numberedPoint("Define artificial intelligence and explain how it differs from traditional programming", "lesson6"),
      numberedPoint("Describe how neural networks process visual information (conceptual level)", "lesson6"),
      numberedPoint("Explain what a confidence score represents and interpret different levels", "lesson6"),
      numberedPoint("Filter detection results based on confidence thresholds", "lesson6"),
      numberedPoint("Identify the key components of the IMX500 AI camera system", "lesson6"),
      spacer(),
      
      heading2("PowerPoint Slide Outline (15 slides)"),
      createTable(
        ["Slide #", "Title", "Content"],
        [
          ["1", "Title Slide", "Introduction to Artificial Intelligence"],
          ["2", "TODAY'S GOAL", "Demo: AI detecting objects with confidence scores displayed"],
          ["3", "AI is Everywhere", "Examples: phones, cars, games, recommendations"],
          ["4", "Traditional Code vs AI", "If-then rules vs learning from examples"],
          ["5", "How Humans See", "Eyes → Brain → Recognition"],
          ["6", "How AI Sees", "Pixels → Neural Network → Labels"],
          ["7", "Neural Networks", "Layers that transform data (simple visual)"],
          ["8", "Training AI", "Learning from thousands of examples"],
          ["9", "The IMX500 Camera", "AI processing ON the sensor - no cloud needed!"],
          ["10", "Edge AI Advantage", "Fast, private, low power"],
          ["11", "Confidence Scores", "0.0 to 1.0 scale - how sure is the AI?"],
          ["12", "Interpreting Confidence", "High (0.8+), Medium (0.5-0.8), Low (<0.5)"],
          ["13", "Why Confidence Matters", "Filter out false positives"],
          ["14", "Bounding Boxes", "How AI shows WHERE objects are"],
          ["15", "Your Turn", "Build your confidence interpreter!"]
        ],
        [1000, 2500, 5860]
      ),
      spacer(),
      
      heading2("Jupyter Notebook Structure"),
      heading3("Section 1: Your Mission (2 cells)"),
      bulletPoint("Markdown: TODAY - Understand how AI thinks!"),
      bulletPoint("Markdown: What is a confidence score? Preview"),
      spacer(),
      
      heading3("Section 2: AI vs Traditional Code (3 cells)"),
      bulletPoint("EXERCISE: Write if-then rules to detect a cat (realize it's impossible!)"),
      bulletPoint("Markdown: This is why we need AI - it learns patterns"),
      bulletPoint("EXERCISE: List 3 things that make cats hard to describe with rules"),
      spacer(),
      
      heading3("Section 3: Confidence Scores (5 cells)"),
      bulletPoint("Code: Simulated detections with different confidences"),
      bulletPoint("EXERCISE: Which detections should we trust? (given list)"),
      bulletPoint("Code: Filter detections below 0.5 confidence"),
      bulletPoint("EXERCISE: Change threshold to 0.7, count remaining detections"),
      bulletPoint("EXERCISE: Why might we want different thresholds for different uses?"),
      spacer(),
      
      heading3("Section 4: Bounding Boxes (3 cells)"),
      bulletPoint("Markdown: How bounding boxes work (x, y, width, height)"),
      bulletPoint("Code: Calculate center point of a bounding box"),
      bulletPoint("EXERCISE: Calculate area of a bounding box"),
      spacer(),
      
      heading3("Section 5: Knowledge Check (2 cells)"),
      bulletPoint("EXERCISE: Fill in code to filter by confidence AND object type"),
      bulletPoint("EXERCISE: What does 0.85 confidence mean in plain English?"),
      
      // ============ MODULE 7 ============
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 7: Object Detection"),
      boldPara("Day: ", "7 of 14"),
      boldPara("Duration: ", "45 minutes"),
      boldPara("Prerequisites: ", "Modules 1-6 completed"),
      spacer(),
      
      endGoalBox("BY THE END OF THIS LESSON, YOU WILL HAVE:",
        "A live object detection system running on YOUR camera! You will see bounding boxes appear around objects in real-time, with labels and confidence scores. You'll detect people, phones, chairs, and more from the 80-object COCO dataset."),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this lesson, students will be able to:"),
      numberedPoint("Start a live camera feed from the IMX500 AI camera", "lesson7"),
      numberedPoint("Run real-time object detection with bounding box visualization", "lesson7"),
      numberedPoint("Identify which of the 80 COCO objects the camera can detect", "lesson7"),
      numberedPoint("Filter detection results by confidence threshold", "lesson7"),
      numberedPoint("Understand factors affecting detection accuracy (lighting, distance, angle)", "lesson7"),
      spacer(),
      
      heading2("PowerPoint Slide Outline (12 slides)"),
      createTable(
        ["Slide #", "Title", "Content"],
        [
          ["1", "Title Slide", "Live Object Detection"],
          ["2", "TODAY'S GOAL", "LIVE DEMO: Teacher shows detection running - 'You'll build this!'"],
          ["3", "The COCO Dataset", "80 objects: people, animals, vehicles, household items"],
          ["4", "Object Categories", "Visual grid of detectable objects by category"],
          ["5", "Starting the Camera", "How the video pipeline works"],
          ["6", "Detection Pipeline", "Camera → AI Chip → Results → Display"],
          ["7", "Reading Results", "Object name + confidence + bounding box"],
          ["8", "Factors Affecting Accuracy", "Lighting, distance, angle, occlusion"],
          ["9", "What It Can't Detect", "Objects not in COCO (important limitation!)"],
          ["10", "Confidence Filtering", "Remove low-confidence false positives"],
          ["11", "Try These Objects", "List of classroom objects to test"],
          ["12", "Your Turn", "Build your own detector!"]
        ],
        [1000, 2500, 5860]
      ),
      spacer(),
      
      heading2("Jupyter Notebook Structure"),
      heading3("Section 1: Your Mission (2 cells)"),
      bulletPoint("Markdown: TODAY - Live object detection!"),
      bulletPoint("Markdown: Objects you'll detect today (with images)"),
      spacer(),
      
      heading3("Section 2: Camera Setup (3 cells)"),
      bulletPoint("Code: Start camera feed with stop button"),
      bulletPoint("EXERCISE: How long until the image appears? Time it!"),
      bulletPoint("Code: Verify camera is working"),
      spacer(),
      
      heading3("Section 3: Live Detection (5 cells)"),
      bulletPoint("Code: Complete detection with bounding boxes (WORKING CODE)"),
      bulletPoint("EXERCISE: Point at 5 different objects, record what was detected"),
      bulletPoint("EXERCISE: Find something that IS in COCO but wasn't detected well"),
      bulletPoint("EXERCISE: Find something NOT in COCO (AI can't detect it)"),
      bulletPoint("Code: Print detection details (label, confidence, coordinates)"),
      spacer(),
      
      heading3("Section 4: Filtering (3 cells)"),
      bulletPoint("Code: Show all detections vs. filtered (>0.7 confidence)"),
      bulletPoint("EXERCISE: Test threshold of 0.5 vs 0.8 - count difference"),
      bulletPoint("EXERCISE: Filter to show only 'person' detections"),
      spacer(),
      
      heading3("Section 5: Knowledge Check (2 cells)"),
      bulletPoint("EXERCISE: Complete table - object, detected?, confidence"),
      bulletPoint("EXERCISE: What conditions make detection more reliable?"),
      
      // ============ MODULE 8 ============
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 8: AI + Hardware Integration"),
      boldPara("Day: ", "8 of 14"),
      boldPara("Duration: ", "45 minutes"),
      boldPara("Prerequisites: ", "Modules 1-7 completed"),
      spacer(),
      
      endGoalBox("BY THE END OF THIS LESSON, YOU WILL HAVE:",
        "An alert system that BEEPS when AI detects specific objects! When a person walks in front of the camera, your buzzer sounds. Different objects trigger different beep patterns. This is your first AI-controlled physical response!"),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this lesson, students will be able to:"),
      numberedPoint("Control a buzzer using GPIO pins on the Raspberry Pi", "lesson8"),
      numberedPoint("Trigger hardware alerts based on AI detection events", "lesson8"),
      numberedPoint("Implement cooldown logic to prevent alert spam", "lesson8"),
      numberedPoint("Create custom alert patterns for different object types", "lesson8"),
      numberedPoint("Build a complete detection-to-alert pipeline", "lesson8"),
      spacer(),
      
      heading2("PowerPoint Slide Outline (12 slides)"),
      createTable(
        ["Slide #", "Title", "Content"],
        [
          ["1", "Title Slide", "AI + Physical Response"],
          ["2", "TODAY'S GOAL", "Demo: Buzzer beeps when person detected!"],
          ["3", "GPIO Introduction", "General Purpose Input/Output pins"],
          ["4", "The Buzzer", "How it works, wiring diagram"],
          ["5", "Basic GPIO Control", "High = On, Low = Off"],
          ["6", "Detection + Action", "If detected AND confident → BEEP"],
          ["7", "The Spam Problem", "Same object every frame = constant noise!"],
          ["8", "Cooldown Logic", "Only alert once per N seconds"],
          ["9", "Custom Patterns", "Person = 2 beeps, Car = 3 beeps"],
          ["10", "Complete Pipeline", "Detection → Filter → Cooldown → Alert"],
          ["11", "Real World Examples", "Security systems, accessibility aids"],
          ["12", "Your Turn", "Build your alert system!"]
        ],
        [1000, 2500, 5860]
      ),
      spacer(),
      
      heading2("Jupyter Notebook Structure"),
      heading3("Section 1: Your Mission (2 cells)"),
      bulletPoint("Markdown: TODAY - Make AI trigger physical alerts!"),
      bulletPoint("Markdown: What your system will do (flowchart)"),
      spacer(),
      
      heading3("Section 2: GPIO Basics (4 cells)"),
      bulletPoint("Code: Simple buzzer on/off test"),
      bulletPoint("EXERCISE: Make it beep 3 times with 0.5s gaps"),
      bulletPoint("EXERCISE: Create SOS pattern (short-short-short, long-long-long, short-short-short)"),
      bulletPoint("Code: Beep pattern function"),
      spacer(),
      
      heading3("Section 3: Detection Alerts (5 cells)"),
      bulletPoint("Code: Complete detection + alert system (WORKING CODE)"),
      bulletPoint("EXERCISE: Change target from 'person' to 'cell phone'"),
      bulletPoint("EXERCISE: Lower confidence threshold to 0.6"),
      bulletPoint("Code: Add cooldown to prevent spam"),
      bulletPoint("EXERCISE: Change cooldown from 3 seconds to 5 seconds"),
      spacer(),
      
      heading3("Section 4: Custom Patterns (3 cells)"),
      bulletPoint("Code: Dictionary mapping objects to beep patterns"),
      bulletPoint("EXERCISE: Add your own object with custom pattern"),
      bulletPoint("EXERCISE: Add a 'warning' pattern for low-confidence detections"),
      spacer(),
      
      heading3("Section 5: Knowledge Check (2 cells)"),
      bulletPoint("EXERCISE: Fill in complete alert system code"),
      bulletPoint("EXERCISE: Why is cooldown important for usability?"),
      
      // ============ MODULE 9 ============
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 9: System Integration"),
      boldPara("Day: ", "9 of 14"),
      boldPara("Duration: ", "45 minutes"),
      boldPara("Prerequisites: ", "Modules 1-8 completed"),
      spacer(),
      
      endGoalBox("BY THE END OF THIS LESSON, YOU WILL HAVE:",
        "A smart safety monitor that combines EVERYTHING - AI detection AND motor data! Your system will only alert when BOTH a person is detected AND the skateboard is moving fast. This is real sensor fusion, just like in autonomous vehicles!"),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this lesson, students will be able to:"),
      numberedPoint("Combine VESC telemetry with AI object detection in one system", "lesson9"),
      numberedPoint("Create conditional logic using BOTH data sources", "lesson9"),
      numberedPoint("Build a safety system responding to speed AND visual detection", "lesson9"),
      numberedPoint("Understand multi-sensor fusion concepts", "lesson9"),
      numberedPoint("Handle timing between different data sources", "lesson9"),
      spacer(),
      
      heading2("PowerPoint Slide Outline (12 slides)"),
      createTable(
        ["Slide #", "Title", "Content"],
        [
          ["1", "Title Slide", "System Integration: AI Meets Motor Control"],
          ["2", "TODAY'S GOAL", "Demo: Alert ONLY when person detected AND moving fast"],
          ["3", "Review: What We Have", "CAN (motor) + AI (vision) - two data streams"],
          ["4", "Why Combine?", "Neither alone tells the whole story"],
          ["5", "Example Scenario", "Person + Moving = DANGER. Person + Stopped = OK"],
          ["6", "Sensor Fusion", "Combining multiple sensors for better decisions"],
          ["7", "How Cars Do It", "Tesla/Waymo use cameras + radar + lidar together"],
          ["8", "Integration Architecture", "Diagram: Both data streams → Logic → Response"],
          ["9", "Conditional Logic", "IF person AND rpm > 1000 THEN alert"],
          ["10", "Safety Levels", "Level 1: Alert, Level 2: Slow, Level 3: Stop"],
          ["11", "Data Freshness", "What if data is old/stale?"],
          ["12", "Your Turn", "Build your smart safety monitor!"]
        ],
        [1000, 2500, 5860]
      ),
      spacer(),
      
      heading2("Jupyter Notebook Structure"),
      heading3("Section 1: Your Mission (2 cells)"),
      bulletPoint("Markdown: TODAY - Combine AI + Motor data!"),
      bulletPoint("Markdown: Logic diagram of what you'll build"),
      spacer(),
      
      heading3("Section 2: Combining Data (4 cells)"),
      bulletPoint("Code: Initialize BOTH VESC API and camera"),
      bulletPoint("Code: Read motor speed AND detection in same loop"),
      bulletPoint("EXERCISE: Print 'Speed: X RPM, Objects: Y' each cycle"),
      bulletPoint("EXERCISE: Add voltage to the combined display"),
      spacer(),
      
      heading3("Section 3: Conditional Safety Logic (5 cells)"),
      bulletPoint("Markdown: Multi-condition logic explained"),
      bulletPoint("Code: Alert only if person AND moving (RPM > 500)"),
      bulletPoint("EXERCISE: Add third condition - only if battery > 20V"),
      bulletPoint("Code: Three safety levels based on speed"),
      bulletPoint("EXERCISE: Customize speed thresholds for each level"),
      spacer(),
      
      heading3("Section 4: Complete System (3 cells)"),
      bulletPoint("Code: Full smart safety monitor with dashboard"),
      bulletPoint("EXERCISE: Add temperature to the safety checks"),
      bulletPoint("EXERCISE: Add manual override using keyboard input"),
      spacer(),
      
      heading3("Section 5: Knowledge Check (2 cells)"),
      bulletPoint("EXERCISE: Fill in conditional logic for 3-level system"),
      bulletPoint("EXERCISE: What other sensors could improve this?"),
      
      // ============ MODULE 10 ============
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 10: AI Capstone Project"),
      boldPara("Day: ", "10 of 14"),
      boldPara("Duration: ", "45 minutes (may extend)"),
      boldPara("Prerequisites: ", "Modules 1-9 completed"),
      spacer(),
      
      calloutBox("CAPSTONE PROJECT #2",
        "Students design and implement a project integrating AI camera detection with CAN bus motor communication. This demonstrates mastery of the complete integrated system.",
        colors.infoBg),
      spacer(),
      
      endGoalBox("BY THE END OF THIS LESSON, YOU WILL HAVE:",
        "A complete integrated project that YOU designed, combining AI vision with motor data. This could be a safety assistant, parking helper, traffic monitor, or your own creative idea. You will demonstrate it to the class!"),
      spacer(),
      
      heading2("Project Options"),
      heading3("Option A: Autonomous Safety Assistant"),
      para("Detect hazards (people, vehicles) and adjust behavior based on speed and confidence."),
      spacer(),
      
      heading3("Option B: Smart Parking Helper"),
      para("Detect obstacles and provide audio feedback based on estimated distance (bounding box size)."),
      spacer(),
      
      heading3("Option C: Traffic Monitor"),
      para("Count and classify detected objects while logging motor performance data."),
      spacer(),
      
      heading3("Option D: Custom Integrated Project"),
      para("Design your own! Must meaningfully combine AI detection with motor data."),
      spacer(),
      
      heading2("Evaluation Rubric"),
      createTable(
        ["Criteria", "Points", "Description"],
        [
          ["Integration Quality", "30", "AI and CAN systems work together meaningfully"],
          ["Functionality", "25", "Project works as intended"],
          ["Code Quality", "15", "Clean code, good structure"],
          ["Error Handling", "15", "Handles disconnections, edge cases"],
          ["Documentation", "15", "Clear explanation, diagram"]
        ],
        [2500, 1000, 5860]
      ),
      
      // ============ ADAS INTRODUCTION ============
      new Paragraph({ children: [new PageBreak()] }),
      heading1("BONUS MODULE: ADAS"),
      new Paragraph({
        spacing: { after: 200 },
        shading: { fill: colors.adasBg, type: ShadingType.CLEAR },
        children: [new TextRun({ text: "Advanced Driver Assistance Systems - 4-Day Deep Dive", size: 26, font: "Arial", color: colors.primary, bold: true })]
      }),
      spacer(),
      
      para("This bonus module provides comprehensive coverage of Advanced Driver Assistance Systems (ADAS), connecting the skateboard project to real automotive technology. Students will learn industry standards, implement a Forward Collision Warning system, and complete a third capstone project."),
      spacer(),
      
      heading2("ADAS Module Overview"),
      createTable(
        ["Day", "Unit", "End Goal", "Focus"],
        [
          ["11", "ADAS Introduction", "Complete ADAS feature comparison chart", "Industry context, SAE levels, sensor types"],
          ["12", "ADAS Theory", "Working time-to-collision calculator", "FCW theory, sensor fusion, algorithms"],
          ["13", "ADAS Implementation", "Forward Collision Warning system", "Complete FCW with alerts"],
          ["14", "ADAS Capstone", "COMPLETE ADAS PROJECT", "Open-ended project #3"]
        ],
        [600, 2000, 3200, 3560]
      ),
      
      // ============ MODULE 11 ============
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 11: ADAS Introduction"),
      boldPara("Day: ", "11 of 14 (ADAS Day 1)"),
      boldPara("Duration: ", "45 minutes"),
      boldPara("Prerequisites: ", "Modules 1-10 completed"),
      spacer(),
      
      endGoalBox("BY THE END OF THIS LESSON, YOU WILL HAVE:",
        "A comprehensive understanding of ADAS technology used in modern vehicles. You will create a comparison chart of ADAS features, understand SAE autonomy levels 0-5, and know how Tesla, Waymo, and other companies implement these systems. You'll see exactly how YOUR skateboard project relates to real autonomous vehicles!"),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this lesson, students will be able to:"),
      numberedPoint("Define ADAS and list at least 10 common ADAS features", "lesson11"),
      numberedPoint("Explain all 6 SAE autonomy levels (0-5) with examples", "lesson11"),
      numberedPoint("Compare sensors used in automotive ADAS (camera, radar, lidar, ultrasonic)", "lesson11"),
      numberedPoint("Describe how major companies (Tesla, Waymo, Mobileye) implement ADAS", "lesson11"),
      numberedPoint("Map the skateboard system capabilities to real ADAS features", "lesson11"),
      spacer(),
      
      heading2("PowerPoint Slide Outline (18 slides)"),
      createTable(
        ["Slide #", "Title", "Content"],
        [
          ["1", "Title Slide", "Advanced Driver Assistance Systems (ADAS)"],
          ["2", "TODAY'S GOAL", "Understand how YOUR project connects to real autonomous vehicles"],
          ["3", "What is ADAS?", "Definition: Systems that help drivers, not replace them"],
          ["4", "ADAS Timeline", "History: ABS (1978) → Cruise Control → Today's autonomy"],
          ["5", "Common ADAS Features", "List of 15+ features with icons"],
          ["6", "Forward Collision Warning", "Detects imminent crash, alerts driver (we'll build this!)"],
          ["7", "Automatic Emergency Braking", "Takes action if driver doesn't respond"],
          ["8", "Lane Departure Warning", "Alerts when drifting out of lane"],
          ["9", "Adaptive Cruise Control", "Maintains distance from car ahead"],
          ["10", "Blind Spot Detection", "Monitors areas driver can't see"],
          ["11", "SAE Autonomy Levels", "Overview of Levels 0-5"],
          ["12", "Level 0-2", "Driver in control, system assists"],
          ["13", "Level 3-5", "System takes control, driver monitors or not"],
          ["14", "Where Cars Are Today", "Most are Level 2, some Level 3"],
          ["15", "Sensors: Camera", "How cameras work, strengths/weaknesses"],
          ["16", "Sensors: Radar & Lidar", "How they work, cost vs capability"],
          ["17", "Company Comparison", "Tesla vs Waymo vs Mobileye approaches"],
          ["18", "Your Skateboard = Mini ADAS", "How our system maps to real features"]
        ],
        [1000, 2800, 5560]
      ),
      spacer(),
      
      heading2("Jupyter Notebook Structure"),
      heading3("Section 1: Your Mission (2 cells)"),
      bulletPoint("Markdown: TODAY - Become an ADAS expert!"),
      bulletPoint("Markdown: What you'll know by the end (preview)"),
      spacer(),
      
      heading3("Section 2: ADAS Features Deep Dive (5 cells)"),
      bulletPoint("Markdown: Complete list of 15 ADAS features with descriptions"),
      bulletPoint("EXERCISE: Categorize features (Warning vs. Intervention)"),
      bulletPoint("EXERCISE: Which features does your family car have?"),
      bulletPoint("Code: Create ADAS feature dictionary with descriptions"),
      bulletPoint("EXERCISE: Add 3 more features to the dictionary"),
      spacer(),
      
      heading3("Section 3: SAE Autonomy Levels (4 cells)"),
      bulletPoint("Markdown: Detailed breakdown of Levels 0-5"),
      bulletPoint("Code: SAE level classifier - input features, output level"),
      bulletPoint("EXERCISE: What level is Tesla Autopilot? Waymo?"),
      bulletPoint("EXERCISE: What level is our skateboard system?"),
      spacer(),
      
      heading3("Section 4: Sensor Comparison (4 cells)"),
      bulletPoint("Markdown: Camera vs Radar vs Lidar vs Ultrasonic"),
      bulletPoint("Code: Sensor comparison table generator"),
      bulletPoint("EXERCISE: Fill in strengths/weaknesses for each sensor"),
      bulletPoint("EXERCISE: Why does Tesla use cameras only? Why does Waymo use lidar?"),
      spacer(),
      
      heading3("Section 5: Knowledge Check (3 cells)"),
      bulletPoint("EXERCISE: Create your ADAS comparison chart (10 features minimum)"),
      bulletPoint("EXERCISE: Map our skateboard capabilities to ADAS features"),
      bulletPoint("EXERCISE: Short answer - Why is Level 5 autonomy so hard?"),
      
      // ============ MODULE 12 ============
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 12: ADAS Theory"),
      boldPara("Day: ", "12 of 14 (ADAS Day 2)"),
      boldPara("Duration: ", "45 minutes"),
      boldPara("Prerequisites: ", "Module 11 completed"),
      spacer(),
      
      endGoalBox("BY THE END OF THIS LESSON, YOU WILL HAVE:",
        "A working Time-to-Collision (TTC) calculator! You will understand the math behind Forward Collision Warning systems, learn how sensor fusion works, and calculate exactly when a collision would occur based on speed and distance. This is real engineering!"),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this lesson, students will be able to:"),
      numberedPoint("Explain the Forward Collision Warning (FCW) algorithm", "lesson12"),
      numberedPoint("Calculate Time-to-Collision (TTC) given speed and distance", "lesson12"),
      numberedPoint("Describe sensor fusion and why multiple sensors are combined", "lesson12"),
      numberedPoint("Understand false positive/negative tradeoffs in safety systems", "lesson12"),
      numberedPoint("Design alert thresholds for different TTC values", "lesson12"),
      spacer(),
      
      heading2("PowerPoint Slide Outline (15 slides)"),
      createTable(
        ["Slide #", "Title", "Content"],
        [
          ["1", "Title Slide", "ADAS Theory: The Math Behind Safety"],
          ["2", "TODAY'S GOAL", "Build a Time-to-Collision calculator"],
          ["3", "Forward Collision Warning", "What it does, when it activates"],
          ["4", "The Core Problem", "How far away is that object? How fast are we closing?"],
          ["5", "Distance Estimation", "Using bounding box size as proxy for distance"],
          ["6", "Speed: We Know This!", "Our VESC gives us exact RPM → speed"],
          ["7", "Time-to-Collision Formula", "TTC = Distance / Closing Speed"],
          ["8", "TTC Example", "Object 10m away, closing at 5 m/s = 2 seconds to impact"],
          ["9", "Alert Thresholds", "TTC > 3s: Monitor, 1-3s: Warning, <1s: CRITICAL"],
          ["10", "Sensor Fusion Concept", "Why combine camera + speed data?"],
          ["11", "Fusion Benefits", "Camera: WHAT is there. Motor: HOW FAST we're moving"],
          ["12", "False Positives", "Alert when no danger - annoying, reduces trust"],
          ["13", "False Negatives", "No alert when danger exists - DANGEROUS"],
          ["14", "The Tradeoff", "Sensitivity vs. Specificity, finding the balance"],
          ["15", "Your Turn", "Build your TTC calculator!"]
        ],
        [1000, 2800, 5560]
      ),
      spacer(),
      
      heading2("Jupyter Notebook Structure"),
      heading3("Section 1: Your Mission (2 cells)"),
      bulletPoint("Markdown: TODAY - Calculate Time-to-Collision!"),
      bulletPoint("Markdown: The formula you'll implement"),
      spacer(),
      
      heading3("Section 2: Distance Estimation (4 cells)"),
      bulletPoint("Markdown: How bounding box size relates to distance"),
      bulletPoint("Code: Calibration - known distances vs box sizes"),
      bulletPoint("EXERCISE: Create distance estimation function from box height"),
      bulletPoint("Code: Test estimation with sample bounding boxes"),
      spacer(),
      
      heading3("Section 3: Time-to-Collision (5 cells)"),
      bulletPoint("Markdown: TTC formula explained with diagrams"),
      bulletPoint("Code: Speed calculation from RPM (need wheel circumference)"),
      bulletPoint("Code: TTC calculation function"),
      bulletPoint("EXERCISE: Calculate TTC for 5 different scenarios"),
      bulletPoint("EXERCISE: What happens to TTC if we double our speed?"),
      spacer(),
      
      heading3("Section 4: Alert Thresholds (4 cells)"),
      bulletPoint("Markdown: Why different TTC values need different responses"),
      bulletPoint("Code: Multi-level alert system based on TTC"),
      bulletPoint("EXERCISE: Design your own threshold levels with justification"),
      bulletPoint("EXERCISE: What TTC threshold would you use for a skateboard vs a car?"),
      spacer(),
      
      heading3("Section 5: Knowledge Check (3 cells)"),
      bulletPoint("EXERCISE: Complete TTC calculator with all components"),
      bulletPoint("EXERCISE: Explain false positive vs false negative in your own words"),
      bulletPoint("EXERCISE: Why is sensor fusion better than single sensors?"),
      
      // ============ MODULE 13 ============
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 13: ADAS Implementation"),
      boldPara("Day: ", "13 of 14 (ADAS Day 3)"),
      boldPara("Duration: ", "45 minutes"),
      boldPara("Prerequisites: ", "Modules 11-12 completed"),
      spacer(),
      
      endGoalBox("BY THE END OF THIS LESSON, YOU WILL HAVE:",
        "A COMPLETE Forward Collision Warning system running on your skateboard! Your system will detect people, estimate distance, read your speed, calculate time-to-collision, and issue appropriate alerts. This is a real ADAS feature that you built yourself!"),
      spacer(),
      
      heading2("Learning Objectives"),
      para("By the end of this lesson, students will be able to:"),
      numberedPoint("Integrate all FCW components into a working system", "lesson13"),
      numberedPoint("Implement multi-level alerts (informational, warning, critical)", "lesson13"),
      numberedPoint("Handle edge cases (no detection, stationary, very close)", "lesson13"),
      numberedPoint("Display real-time FCW status on a dashboard", "lesson13"),
      numberedPoint("Test and validate the FCW system under various conditions", "lesson13"),
      spacer(),
      
      heading2("PowerPoint Slide Outline (12 slides)"),
      createTable(
        ["Slide #", "Title", "Content"],
        [
          ["1", "Title Slide", "Building Forward Collision Warning"],
          ["2", "TODAY'S GOAL", "Demo: Complete FCW system in action!"],
          ["3", "Review: Components", "Detection + Distance + Speed + TTC + Alert"],
          ["4", "System Architecture", "Complete flowchart of FCW pipeline"],
          ["5", "Integration Challenges", "Timing, data freshness, synchronization"],
          ["6", "Alert Escalation", "Green (safe) → Yellow (caution) → Red (danger)"],
          ["7", "Visual Feedback", "Dashboard showing TTC, distance, speed"],
          ["8", "Audio Feedback", "Different beep patterns for different levels"],
          ["9", "Edge Cases", "No person detected, already stopped, very close"],
          ["10", "Testing Protocol", "How to safely test your FCW"],
          ["11", "Real FCW Comparison", "How does ours compare to Tesla's?"],
          ["12", "Your Turn", "Build your complete FCW!"]
        ],
        [1000, 2800, 5560]
      ),
      spacer(),
      
      heading2("Jupyter Notebook Structure"),
      heading3("Section 1: Your Mission (2 cells)"),
      bulletPoint("Markdown: TODAY - Complete FCW system!"),
      bulletPoint("Markdown: System diagram of what you'll build"),
      spacer(),
      
      heading3("Section 2: Component Integration (5 cells)"),
      bulletPoint("Code: Import all required modules (VESC, camera, GPIO)"),
      bulletPoint("Code: Distance estimation function (from Day 12)"),
      bulletPoint("Code: TTC calculation function (from Day 12)"),
      bulletPoint("Code: Alert level determination function"),
      bulletPoint("EXERCISE: Modify alert thresholds for your preference"),
      spacer(),
      
      heading3("Section 3: Complete FCW System (5 cells)"),
      bulletPoint("Code: COMPLETE FCW system with all components (WORKING CODE)"),
      bulletPoint("EXERCISE: Add a fourth alert level (CRITICAL+)"),
      bulletPoint("Code: Add dashboard display showing all values"),
      bulletPoint("EXERCISE: Add a \"system healthy\" indicator"),
      bulletPoint("EXERCISE: Add data logging to CSV for later analysis"),
      spacer(),
      
      heading3("Section 4: Testing (3 cells)"),
      bulletPoint("Markdown: Safe testing protocol"),
      bulletPoint("EXERCISE: Test at 3 different speeds, record TTC accuracy"),
      bulletPoint("EXERCISE: Document any false positives/negatives observed"),
      spacer(),
      
      heading3("Section 5: Knowledge Check (2 cells)"),
      bulletPoint("EXERCISE: List 5 improvements you would make to this FCW"),
      bulletPoint("EXERCISE: How would you add Automatic Emergency Braking?"),
      
      // ============ MODULE 14 ============
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Module 14: ADAS Capstone Project"),
      boldPara("Day: ", "14 of 14 (ADAS Day 4)"),
      boldPara("Duration: ", "45 minutes (may extend)"),
      boldPara("Prerequisites: ", "Modules 11-13 completed"),
      spacer(),
      
      calloutBox("CAPSTONE PROJECT #3",
        "Students design and implement an advanced ADAS feature. This is the most challenging project, requiring integration of everything learned throughout the entire course.",
        colors.adasBg),
      spacer(),
      
      endGoalBox("BY THE END OF THIS LESSON, YOU WILL HAVE:",
        "A complete, advanced ADAS feature that YOU designed! This could be an enhanced FCW, a blind spot monitor, a speed limit enforcer, or your own creative ADAS innovation. You will present it as if pitching to an automotive company!"),
      spacer(),
      
      heading2("Project Options"),
      heading3("Option A: Enhanced FCW with Predictive Alerts"),
      para("Extend the basic FCW to predict object movement and provide earlier warnings. Consider object trajectory, not just current position."),
      bulletPoint("Required: Motion tracking, trajectory prediction, enhanced TTC"),
      spacer(),
      
      heading3("Option B: Multi-Object Threat Assessment"),
      para("Monitor multiple detected objects simultaneously and prioritize which is the greatest threat based on distance, size, and closing speed."),
      bulletPoint("Required: Multi-object tracking, threat scoring, priority alerts"),
      spacer(),
      
      heading3("Option C: Speed Limit Zone Enforcement"),
      para("Detect stop signs or specific markers and enforce speed limits when entering zones. Alert if traveling too fast for the zone."),
      bulletPoint("Required: Sign detection, zone tracking, speed monitoring"),
      spacer(),
      
      heading3("Option D: Custom ADAS Feature"),
      para("Design your own ADAS feature! Must include detection, decision logic, and appropriate alerts/responses."),
      spacer(),
      
      heading2("Project Requirements"),
      bulletPoint("Must implement a complete ADAS feature (not just detection)"),
      bulletPoint("Must include multi-level response (at least 3 levels)"),
      bulletPoint("Must handle edge cases gracefully"),
      bulletPoint("Must include a real-time status dashboard"),
      bulletPoint("Must document the algorithm with a flowchart"),
      bulletPoint("Must compare to real automotive implementation"),
      spacer(),
      
      heading2("Evaluation Rubric"),
      createTable(
        ["Criteria", "Points", "Description"],
        [
          ["ADAS Authenticity", "25", "Feature resembles real automotive ADAS"],
          ["Technical Implementation", "25", "All components work correctly"],
          ["Innovation", "20", "Creative approach or novel improvements"],
          ["Edge Case Handling", "15", "System handles unusual situations"],
          ["Documentation & Presentation", "15", "Clear explanation, professional presentation"]
        ],
        [2500, 1000, 5860]
      ),
      spacer(),
      
      heading2("Presentation Format"),
      para("Each student presents their ADAS project as if pitching to an automotive company:"),
      bulletPoint("2 minutes: Problem statement - What safety issue does this solve?"),
      bulletPoint("2 minutes: Solution overview - How does your ADAS feature work?"),
      bulletPoint("2 minutes: Live demonstration"),
      bulletPoint("2 minutes: Future improvements - How could this be enhanced?"),
      bulletPoint("2 minutes: Q&A from class"),
      
      // ============ IMPLEMENTATION GUIDE ============
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Implementation Guide"),
      
      heading2("File Structure"),
      para("The complete curriculum should be organized as follows:"),
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
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "  01_System_Introduction/", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "    Teacher_Slides_01.pptx", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "    Student_Notebook_01.ipynb", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "    Answer_Key_01.ipynb", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "  02_CAN_Fundamentals/ ... (same pattern)", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "  ...", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "  10_AI_Capstone/", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "  11_ADAS_Introduction/", bold: true, size: 20, font: "Courier New", color: colors.primary })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "  12_ADAS_Theory/", bold: true, size: 20, font: "Courier New", color: colors.primary })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "  13_ADAS_Implementation/", bold: true, size: 20, font: "Courier New", color: colors.primary })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "  14_ADAS_Capstone/", bold: true, size: 20, font: "Courier New", color: colors.primary })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "  Resources/", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "    ADAS_Feature_Reference.pdf", size: 20, font: "Courier New" })] }),
                  new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: "    SAE_Levels_Guide.pdf", size: 20, font: "Courier New" })] }),
                  new Paragraph({ children: [new TextRun({ text: "    TTC_Calculation_Guide.pdf", size: 20, font: "Courier New" })] }),
                ]
              })
            ]
          })
        ]
      }),
      spacer(),
      
      heading2("The 'End in Mind' Approach - Implementation"),
      para("Every lesson MUST begin with these elements:"),
      spacer(),
      
      heading3("PowerPoint: First 2 Slides"),
      bulletPoint("Slide 1: Title slide with exciting hook"),
      bulletPoint("Slide 2: 'TODAY'S GOAL' - Live demo or compelling description of end result"),
      spacer(),
      
      heading3("Notebook: First 2 Cells"),
      bulletPoint("Cell 1: YOUR MISSION TODAY - Bold, exciting statement of what they'll build"),
      bulletPoint("Cell 2: What success looks like - Expected output, screenshot, or diagram"),
      spacer(),
      
      heading3("Teacher Script"),
      para("Teachers should spend the first 5 minutes demonstrating the end result before any instruction. Example script:"),
      bulletPoint("'Before we learn anything today, let me show you what you'll build.'"),
      bulletPoint("[Run the demo/show the result]"),
      bulletPoint("'In 40 minutes, you will have built this yourself. Let's learn how!'"),
      spacer(),
      
      heading2("Assessment Summary"),
      createTable(
        ["Assessment", "Day", "Points", "Type"],
        [
          ["Daily notebook exercises", "1-14", "10 each", "Formative"],
          ["CAN Capstone Project", "5", "100", "Summative"],
          ["AI Capstone Project", "10", "100", "Summative"],
          ["ADAS Capstone Project", "14", "100", "Summative"],
          ["TOTAL POSSIBLE", "", "440", ""]
        ],
        [3500, 1500, 1500, 2860]
      ),
      
      // ============ FINAL PAGE ============
      new Paragraph({ children: [new PageBreak()] }),
      heading1("Next Steps"),
      para("This curriculum plan provides the complete structure for a 14-day course. Implementation should proceed as follows:"),
      spacer(),
      
      numberedPoint("Create Python Quick Reference notebook (Module 00)"),
      numberedPoint("Create Module 1 as template (all components)"),
      numberedPoint("Create Modules 2-5 (CAN section + Capstone 1)"),
      numberedPoint("Create Modules 6-10 (AI section + Capstone 2)"),
      numberedPoint("Create Modules 11-14 (ADAS section + Capstone 3)"),
      numberedPoint("Create all answer keys"),
      numberedPoint("Create supplementary resource PDFs"),
      numberedPoint("Pilot test and gather feedback"),
      numberedPoint("Revise and finalize"),
      spacer(),
      
      calloutBox("Ready to Implement",
        "Upon approval of this plan, implementation can begin immediately. Each module requires approximately 2-3 hours to fully develop with all components (slides, notebook, answer key). The ADAS modules may require additional time due to their technical depth.",
        colors.successBg),
      spacer(),
      
      heading2("Key Design Principles Summary"),
      bulletPoint("START WITH THE END IN MIND: Every lesson shows the goal FIRST"),
      bulletPoint("ACTIVE LEARNING: 6-10 exercises per lesson, not passive reading"),
      bulletPoint("COMPLETE CODE: All code works - no undefined functions"),
      bulletPoint("REAL-WORLD CONTEXT: Connect to actual automotive ADAS"),
      bulletPoint("THREE CAPSTONES: Progressive complexity, open-ended creativity"),
      bulletPoint("TEACHER SUPPORT: Full PowerPoints with speaker notes"),
      spacer(),
      spacer(),
      
      para("Document prepared for Lectec Electric Skateboard Educational Program.", { italics: true, color: "666666" }),
      para("Version 2.0 - Includes ADAS Bonus Module and 'End in Mind' Restructuring", { italics: true, color: "666666" }),
    ]
  }]
});

// Generate document
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/sessions/beautiful-brave-hopper/mnt/RaspberryPi-CAN/Lectec_Curriculum_Plan_v2.docx", buffer);
  console.log("Document created successfully: Lectec_Curriculum_Plan_v2.docx");
});
