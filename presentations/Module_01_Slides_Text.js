const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        AlignmentType, LevelFormat, HeadingLevel,
        BorderStyle, WidthType, ShadingType, PageBreak } = require('docx');
const fs = require('fs');

// Colors
const LECTEC_BLUE = "2196F3";
const DARK_BLUE = "1976D2";
const LECTEC_BLACK = "1A1A1A";
const SUCCESS_GREEN = "4CAF50";
const GRAY = "666666";
const LIGHT_GRAY = "F5F5F5";

// Helper functions
function slideTitle(num, title) {
  return new Paragraph({
    spacing: { before: 400, after: 200 },
    shading: { fill: LECTEC_BLUE, type: ShadingType.CLEAR },
    children: [
      new TextRun({ text: `SLIDE ${num}: `, bold: true, size: 32, color: "FFFFFF", font: "Arial" }),
      new TextRun({ text: title, bold: true, size: 32, color: "FFFFFF", font: "Arial" })
    ]
  });
}

function heading(text) {
  return new Paragraph({
    spacing: { before: 200, after: 100 },
    children: [new TextRun({ text, bold: true, size: 28, color: DARK_BLUE, font: "Arial" })]
  });
}

function subheading(text) {
  return new Paragraph({
    spacing: { before: 150, after: 80 },
    children: [new TextRun({ text, bold: true, size: 24, color: LECTEC_BLACK, font: "Arial" })]
  });
}

function para(text, options = {}) {
  return new Paragraph({
    spacing: { before: 60, after: 60 },
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

function bullet(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "bullets", level },
    spacing: { before: 40, after: 40 },
    children: [new TextRun({ text, size: 22, color: LECTEC_BLACK, font: "Arial" })]
  });
}

function numbered(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "numbers", level },
    spacing: { before: 40, after: 40 },
    children: [new TextRun({ text, size: 22, color: LECTEC_BLACK, font: "Arial" })]
  });
}

function codeBlock(code) {
  const border = { style: BorderStyle.SINGLE, size: 1, color: "444444" };
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: [
      new TableRow({
        children: [
          new TableCell({
            borders: { top: border, bottom: border, left: border, right: border },
            shading: { fill: "2D2D2D", type: ShadingType.CLEAR },
            margins: { top: 150, bottom: 150, left: 200, right: 200 },
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

function notebookActivity(text) {
  const border = { style: BorderStyle.SINGLE, size: 1, color: SUCCESS_GREEN };
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: [
      new TableRow({
        children: [
          new TableCell({
            borders: { top: border, bottom: border, left: { style: BorderStyle.SINGLE, size: 24, color: SUCCESS_GREEN }, right: border },
            shading: { fill: "E8F5E9", type: ShadingType.CLEAR },
            margins: { top: 120, bottom: 120, left: 200, right: 200 },
            children: [
              new Paragraph({
                spacing: { after: 80 },
                children: [new TextRun({ text: "NOTEBOOK ACTIVITY", bold: true, size: 24, color: SUCCESS_GREEN, font: "Arial" })]
              }),
              new Paragraph({
                children: [new TextRun({ text, size: 22, color: LECTEC_BLACK, font: "Arial" })]
              })
            ]
          })
        ]
      })
    ]
  });
}

function spacer() {
  return new Paragraph({ spacing: { before: 100, after: 100 }, children: [] });
}

// Create the document
const doc = new Document({
  styles: {
    default: {
      document: { run: { font: "Arial", size: 22 } }
    }
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
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } }
        ] }
    ]
  },
  sections: [{
    properties: {
      page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } }
    },
    children: [
      // ========== TITLE ==========
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 800, after: 200 },
        children: [new TextRun({ text: "MODULE 1: SLIDE TEXT CONTENT", bold: true, size: 48, color: LECTEC_BLUE, font: "Arial" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 400 },
        children: [new TextRun({ text: "Welcome to Your PEV Brain", size: 32, color: GRAY, font: "Arial" })]
      }),
      para("This document contains ONLY the text that should appear on each slide. Use this as your reference when creating the PowerPoint.", { italics: true, color: GRAY }),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 1 ==========
      slideTitle(1, "Title Slide"),
      spacer(),
      para("MODULE 1", { italics: true }),
      para("Welcome to Your PEV Brain", { bold: true, size: 36 }),
      para("Introduction to CAN Bus Communication"),
      spacer(),
      para("Lectec PEV AI Curriculum"),
      para("Day 1 of 14"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 2 ==========
      slideTitle(2, "The Hook"),
      spacer(),
      heading("What If Your PEV Could Think?"),
      spacer(),
      para("Imagine riding down the street and your PEV automatically:"),
      bullet("Spots a pedestrian stepping into your path"),
      bullet("Warns you with a beep before you even see them"),
      bullet("Logs the near-miss for your safety review"),
      spacer(),
      para("By Day 14, YOU will build this system!", { bold: true }),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 3 ==========
      slideTitle(3, "Real-World Technology"),
      spacer(),
      heading("This Tech Powers Real Vehicles"),
      spacer(),
      subheading("Tesla Autopilot"),
      para("Uses CAN bus to read 8 cameras, 12 ultrasonic sensors, and control steering"),
      spacer(),
      subheading("Waymo Robotaxi"),
      para("Fully autonomous vehicles using the same CAN protocol you'll learn today"),
      spacer(),
      subheading("Your Lectec PEV"),
      para("Same technology, your hands, real learning - starting today!"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 4 ==========
      slideTitle(4, "Learning Objectives"),
      spacer(),
      heading("Today's Mission"),
      para("What you'll accomplish in this module", { italics: true }),
      spacer(),
      numbered("Explain what CAN bus is"),
      para("Understand the 'nervous system' of your PEV", { italics: true }),
      spacer(),
      numbered("Identify the three main hardware components"),
      para("Raspberry Pi Zero 2W, VESC Controller, AI Camera", { italics: true }),
      spacer(),
      numbered("Learn to use Jupyter Notebooks"),
      para("Run code, stop code, and understand cells", { italics: true }),
      spacer(),
      numbered("Read real data from your PEV using Python"),
      para("Voltage, RPM, temperature - live and instant!", { italics: true }),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 5 ==========
      slideTitle(5, "System Analogy"),
      spacer(),
      heading("Your PEV Has a Nervous System"),
      spacer(),
      subheading("Human Body"),
      bullet("Brain = Processes information"),
      bullet("Nerves = Carry signals"),
      bullet("Eyes = See the world"),
      bullet("Muscles = Take action"),
      spacer(),
      subheading("Your PEV"),
      bullet("Raspberry Pi = The brain"),
      bullet("CAN Bus = The nerves"),
      bullet("AI Camera = The eyes"),
      bullet("VESC Motor = The muscles"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 6 ==========
      slideTitle(6, "Hardware Overview"),
      spacer(),
      heading("Meet Your Hardware Team"),
      spacer(),
      subheading("THE BRAIN: Raspberry Pi Zero 2W"),
      bullet("1GHz quad-core processor"),
      bullet("512MB RAM"),
      bullet("Runs Python code"),
      bullet("WiFi built-in"),
      spacer(),
      subheading("THE MUSCLES: VESC Motor Controller"),
      bullet("Controls motor speed"),
      bullet("Reports RPM, voltage, temp"),
      bullet("CAN bus interface"),
      bullet("Real-time telemetry"),
      spacer(),
      subheading("THE EYES: Sony IMX500 AI Camera"),
      bullet("AI built INTO the chip!"),
      bullet("Detects 80 object types"),
      bullet("30 FPS processing"),
      bullet("Low power consumption"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 7 ==========
      slideTitle(7, "CAN Bus Explained"),
      spacer(),
      heading("CAN Bus: Controller Area Network"),
      para("The universal language of vehicles", { italics: true }),
      spacer(),
      subheading("Key Facts"),
      bullet("Invented in 1986 by Bosch - originally for cars, now everywhere"),
      bullet("Used in every modern vehicle - cars, trucks, tractors, boats, planes"),
      bullet("Why it matters for YOU - industry-standard skill, real job applications"),
      spacer(),
      subheading("How It Works"),
      bullet("Two wires: CAN High + CAN Low"),
      bullet("All devices share one 'conversation'"),
      bullet("Messages have IDs for routing"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 8 ==========
      slideTitle(8, "System Architecture"),
      spacer(),
      heading("How It All Connects"),
      para("Your PEV's complete nervous system", { italics: true }),
      spacer(),
      para("Raspberry Pi Zero 2W <---> IMX500 AI Camera (via CSI Cable)"),
      para("         |"),
      para("         |"),
      para("    CAN BUS (2-Wire Network)"),
      para("         |"),
      para("         |"),
      para("VESC Motor Controller"),
      para("(Reports: Speed, RPM, Voltage, Temp)"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 9 ==========
      slideTitle(9, "Safety Rules"),
      spacer(),
      heading("Safety First!"),
      para("Essential guidelines for working with your PEV", { italics: true }),
      spacer(),
      numbered("NEVER ride during coding - PEV must be on a stand or stationary"),
      numbered("Check battery before starting - Ensure above 20% for lab work"),
      numbered("Don't touch hot components - Motor and controller get warm"),
      numbered("Always call stop() when done - Clean shutdown protects hardware"),
      numbered("Ask before motor commands - Reading is safe, moving needs approval"),
      numbered("Report any strange behavior - Weird sounds/smells? Tell teacher!"),
      spacer(),
      para("Safety first = more fun with code later!", { bold: true }),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 10 ==========
      slideTitle(10, "Jupyter Introduction"),
      spacer(),
      heading("What is a Jupyter Notebook?"),
      para("Your interactive coding environment", { italics: true }),
      spacer(),
      para("A Jupyter Notebook is like a smart document where you can:"),
      bullet("Write and run Python code"),
      bullet("See results immediately below your code"),
      bullet("Add notes and explanations"),
      bullet("Save your work and come back later"),
      spacer(),
      subheading("Interface Elements"),
      bullet("Cells = Individual boxes of code or text"),
      bullet("Run button = Play button that executes code"),
      bullet("Stop button = Square that stops running code"),
      bullet("Output area = Where results appear"),
      spacer(),
      para("Think of it like a recipe book where you can actually cook each step and see the result!", { italics: true }),
      spacer(),
      notebookActivity("Open your Jupyter Notebook now! Find the file called 'Module_01_PEV_Brain.ipynb'"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 11 ==========
      slideTitle(11, "Running Code"),
      spacer(),
      heading("How to Run a Cell"),
      spacer(),
      subheading("Step 1: Click on a cell"),
      para("The cell will get a blue or green border when selected"),
      spacer(),
      subheading("Step 2: Run using ONE of these methods:"),
      bullet("Click the Run button (play triangle) in the toolbar"),
      bullet("Press Shift + Enter on your keyboard"),
      bullet("Press Ctrl + Enter (runs but stays on same cell)"),
      spacer(),
      subheading("Step 3: Watch for the output"),
      para("Results appear directly below the cell"),
      para("The [ ] shows [*] while running, then [1], [2], etc. when done"),
      spacer(),
      notebookActivity("Go to Section A, Cell 1. Click on it and press Shift+Enter. You should see 'Welcome to Jupyter!' appear below."),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 12 ==========
      slideTitle(12, "Stopping Code"),
      spacer(),
      heading("Stopping Code That Won't Stop"),
      para("Sometimes code runs forever - here's how to stop it!", { italics: true }),
      spacer(),
      subheading("Why Code Might Run Forever"),
      bullet("Loops that never end (while True:)"),
      bullet("Waiting for something that never happens"),
      bullet("Accidentally created infinite loop"),
      spacer(),
      subheading("How to Stop"),
      bullet("Method 1: Click the Stop button (black square) in the toolbar"),
      bullet("Method 2: Press the 'I' key twice quickly (I, I)"),
      bullet("Method 3: Go to Kernel -> Interrupt (menu bar)"),
      spacer(),
      subheading("Signs Code is Still Running"),
      bullet("The cell shows [*] instead of a number"),
      bullet("You can't run other cells"),
      bullet("The circle in the top right is filled (busy)"),
      spacer(),
      notebookActivity("Go to Section A, Cell 2. This cell counts forever! Run it, watch it count for a few seconds, then STOP it using the Stop button."),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 13 ==========
      slideTitle(13, "What is an API?"),
      spacer(),
      heading("What is an API?"),
      para("Application Programming Interface", { italics: true }),
      spacer(),
      subheading("The Restaurant Analogy"),
      para("Imagine you're at a restaurant:"),
      bullet("You (the customer) = Your Python code"),
      bullet("The Waiter = The API"),
      bullet("The Kitchen = The VESC motor controller"),
      bullet("The Menu = Available functions you can call"),
      spacer(),
      subheading("How It Works"),
      numbered("You look at the menu and tell the waiter what you want"),
      numbered("The waiter goes to the kitchen and places your order"),
      numbered("The kitchen prepares your food"),
      numbered("The waiter brings it back to you"),
      spacer(),
      para("You don't need to know HOW the kitchen makes the food."),
      para("You just need to know WHAT to ask for!", { bold: true }),
      spacer(),
      para("KEY INSIGHT: An API is a 'menu' of commands. You pick what you want, and the API handles all the complicated stuff behind the scenes.", { bold: true }),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 14 ==========
      slideTitle(14, "The VESCStudentAPI"),
      spacer(),
      heading("Meet Your API: VESCStudentAPI"),
      para("Your menu of commands for talking to the VESC", { italics: true }),
      spacer(),
      subheading("Read Functions - Get info FROM the VESC"),
      bullet("get_input_voltage() - Battery voltage"),
      bullet("get_rpm() - Motor speed"),
      bullet("get_motor_current() - Electricity to motor"),
      bullet("get_fet_temperature() - Controller temp"),
      bullet("get_motor_temperature() - Motor temp"),
      bullet("...and more!"),
      spacer(),
      subheading("Control Functions - Send commands TO the VESC"),
      para("(Teacher approval required!)", { italics: true }),
      bullet("set_duty_cycle() - Control motor speed"),
      bullet("set_current() - Control motor torque"),
      bullet("set_brake_current() - Apply brakes"),
      spacer(),
      subheading("System Functions - Manage the connection"),
      bullet("start() - Connect to the VESC"),
      bullet("stop() - Disconnect safely"),
      bullet("is_connected() - Check if working"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 15 ==========
      slideTitle(15, "Connecting to VESC"),
      spacer(),
      heading("Let's Connect to the VESC!"),
      spacer(),
      subheading("The Connection Code"),
      codeBlock("from student_api import VESCStudentAPI\n\nvesc_api = VESCStudentAPI()\nvesc_api.start()\n\nvesc = vesc_api.get_controller(74)"),
      spacer(),
      subheading("Line-by-Line Explanation"),
      bullet("Line 1: Import the API (get the menu ready)"),
      bullet("Line 3: Create our API helper"),
      bullet("Line 4: Start the connection (walk into the restaurant)"),
      bullet("Line 6: Get access to controller #74 (our specific VESC)"),
      spacer(),
      subheading("Expected Output"),
      para("Connected to VESC controller! Battery: XX.X V", { color: SUCCESS_GREEN }),
      spacer(),
      subheading("If You See an Error"),
      para("Check that the PEV is powered ON and the cable is connected"),
      spacer(),
      notebookActivity("Go to Section C in your notebook. Run the connection cell. Raise your hand when you see the battery voltage!"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 16 ==========
      slideTitle(16, "Reading Battery Voltage"),
      spacer(),
      heading("Your First Data Read: Battery Voltage"),
      spacer(),
      subheading("The Code"),
      codeBlock("voltage = vesc.get_input_voltage()\nprint(f\"Battery Voltage: {voltage} V\")"),
      spacer(),
      subheading("What This Does"),
      numbered("Asks the VESC: 'What's the battery voltage right now?'"),
      numbered("VESC responds over CAN bus with the number"),
      numbered("We store it in a variable called 'voltage'"),
      numbered("We display it using print()"),
      spacer(),
      subheading("Understanding the Reading"),
      bullet("36V+ = Fully charged (10S battery)"),
      bullet("33-36V = Good charge remaining"),
      bullet("30-33V = Getting low, consider charging"),
      bullet("Below 30V = Low battery warning!"),
      spacer(),
      notebookActivity("In Section D, Cell 1, write your own code to read voltage. Fill in the blank: voltage = vesc.________()"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 17 ==========
      slideTitle(17, "Reading RPM - Part 1"),
      spacer(),
      heading("Reading Motor Speed (RPM)"),
      para("RPM = Revolutions Per Minute", { italics: true }),
      spacer(),
      subheading("The Code"),
      codeBlock("rpm = vesc.get_rpm()\nprint(f\"Motor RPM: {rpm}\")"),
      spacer(),
      subheading("When motor is NOT spinning:"),
      para("Output: Motor RPM: 0"),
      para("This is normal! No movement = 0 RPM"),
      spacer(),
      subheading("When motor IS spinning:"),
      para("Output: Motor RPM: 2847 (or some number)"),
      para("Positive = Forward direction"),
      para("Negative = Reverse direction"),
      spacer(),
      para("KEY POINT: The RPM reading is INSTANT - it shows what's happening RIGHT NOW.", { bold: true }),
      spacer(),
      notebookActivity("In Section D, Cell 2, run the RPM code with the motor NOT spinning. Write down: ______ RPM"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 18 ==========
      slideTitle(18, "Reading RPM - Part 2 (The Proof!)"),
      spacer(),
      heading("Proving It's Real-Time!"),
      para("Let's see the data change instantly", { italics: true }),
      spacer(),
      subheading("The Experiment"),
      spacer(),
      para("Step 1: Run the code with motor stopped", { bold: true }),
      para("Expected result: 0 RPM"),
      para("Write it down: ______ RPM"),
      spacer(),
      para("Step 2: Gently spin the wheel BY HAND", { bold: true }),
      para("Keep it spinning slowly and safely"),
      spacer(),
      para("Step 3: While spinning, run the code AGAIN", { bold: true }),
      para("Expected result: A number OTHER than 0!"),
      para("Write it down: ______ RPM"),
      spacer(),
      para("The code reads what's happening RIGHT NOW!", { bold: true }),
      para("This is called REAL-TIME DATA - instant feedback from your PEV."),
      spacer(),
      notebookActivity("Run RPM cell, write number. GENTLY spin wheel by hand and run AGAIN while spinning. Write both numbers!"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 19 ==========
      slideTitle(19, "Fill-in-the-Blank: Temperature"),
      spacer(),
      heading("Your Turn: Read the Temperature!"),
      spacer(),
      subheading("The Challenge"),
      para("Fill in the blanks to read the controller (FET) temperature:"),
      spacer(),
      codeBlock("temp = vesc.get_____temperature()\nprint(f\"Controller Temperature: {____} C\")"),
      spacer(),
      subheading("Hints"),
      bullet("Hint 1: The FET is the electronic part of the controller"),
      bullet("Hint 2: Look at the API list - what function reads FET temp?"),
      bullet("Hint 3: The second blank should be the variable name"),
      spacer(),
      subheading("Answer Check"),
      para("Your output should look like: Controller Temperature: XX.X C"),
      para("Normal reading: 20-50C when idle"),
      spacer(),
      notebookActivity("Go to Section E, Cell 1. Fill in the blanks and run. Write your temperature: ______ C"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 20 ==========
      slideTitle(20, "Matching Challenge"),
      spacer(),
      heading("Match the Component to the Function!"),
      spacer(),
      subheading("What do you want to know?"),
      numbered("How fast is the motor spinning?"),
      numbered("How much battery do I have?"),
      numbered("Is the controller getting hot?"),
      numbered("How much electricity is the motor using?"),
      numbered("How hot is the motor itself?"),
      spacer(),
      subheading("Which function to use?"),
      para("A. get_motor_temperature()"),
      para("B. get_rpm()"),
      para("C. get_input_voltage()"),
      para("D. get_motor_current()"),
      para("E. get_fet_temperature()"),
      spacer(),
      para("Answers: 1-B, 2-C, 3-E, 4-D, 5-A", { italics: true, color: GRAY }),
      spacer(),
      notebookActivity("Complete the matching exercise in Section F of your notebook. Run the 'check answers' cell!"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 21 ==========
      slideTitle(21, "Summary"),
      spacer(),
      heading("What You Learned Today"),
      spacer(),
      subheading("Achievement Checklist"),
      bullet("[DONE] CAN bus is the 'nervous system' of vehicles"),
      bullet("[DONE] Three components: Pi (brain), VESC (muscles), Camera (eyes)"),
      bullet("[DONE] How to use Jupyter Notebooks (run, stop, restart)"),
      bullet("[DONE] What an API is and why we use one"),
      bullet("[DONE] Connected to your PEV with Python"),
      bullet("[DONE] Read real voltage, RPM, and temperature data"),
      bullet("[DONE] Proved that the data is REAL-TIME"),
      spacer(),
      subheading("Key Terms"),
      bullet("CAN Bus - Controller Area Network, the two-wire communication system"),
      bullet("VESC - Motor speed controller that reports telemetry"),
      bullet("API - Application Programming Interface, your 'menu' of commands"),
      bullet("Telemetry - Data sent from the VESC (voltage, RPM, temp, etc.)"),
      bullet("Real-Time - Data that reflects what's happening RIGHT NOW"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SLIDE 22 ==========
      slideTitle(22, "Coming Up Next"),
      spacer(),
      heading("COMING UP IN MODULE 2"),
      spacer(),
      para("Building a Live Dashboard", { bold: true, size: 32 }),
      para("Real-time data visualization with continuous updates", { italics: true }),
      spacer(),
      subheading("Preview"),
      bullet("Continuous monitoring loops"),
      bullet("Updating displays"),
      bullet("Data logging"),
      spacer(),
      para("Great job today!", { bold: true }),
      para("You've taken your first step into vehicle communication"),
      para("Today you asked single questions. Tomorrow, you'll have a continuous conversation!"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== JUPYTER NOTEBOOK CONTENT ==========
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 400, after: 200 },
        children: [new TextRun({ text: "JUPYTER NOTEBOOK CONTENT", bold: true, size: 48, color: LECTEC_BLUE, font: "Arial" })]
      }),
      para("The following sections detail the exact content for each cell in the companion Jupyter Notebook."),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SECTION A ==========
      heading("Section A: Jupyter Basics"),
      spacer(),
      subheading("Cell A.1 - Welcome (Markdown)"),
      codeBlock("# Welcome to Jupyter Notebooks!\n\nThis is your interactive coding environment. Let's learn how to use it!"),
      spacer(),
      subheading("Cell A.2 - First Code Cell"),
      codeBlock("# Your first code cell!\n# Click on this cell, then press Shift+Enter to run it\n\nprint(\"Welcome to Jupyter!\")\nprint(\"If you can see this, you ran the cell successfully!\")"),
      spacer(),
      subheading("Cell A.3 - Counting Forever (Stop Practice)"),
      codeBlock("# This code counts forever - you'll need to STOP it!\nimport time\n\ncounter = 1\nwhile True:\n    print(f\"Counting: {counter}\")\n    counter = counter + 1\n    time.sleep(0.5)"),
      spacer(),
      subheading("Cell A.4 - Simple Math"),
      codeBlock("# Python can do math!\n\napples = 5\noranges = 3\ntotal_fruit = apples + oranges\n\nprint(f\"I have {apples} apples\")\nprint(f\"I have {oranges} oranges\")\nprint(f\"Total fruit: {total_fruit}\")"),
      spacer(),
      subheading("Cell A.5 - Variables Practice"),
      codeBlock("# YOUR TURN: Change the values below and run again!\n\nmy_name = \"Student\"  # Change to your name!\nmy_age = 15          # Change to your age!\n\nprint(f\"Hello, my name is {my_name}\")\nprint(f\"I am {my_age} years old\")"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SECTION B ==========
      heading("Section B: Functions Practice"),
      spacer(),
      subheading("Cell B.1 - Functions Introduction"),
      codeBlock("# Functions are like recipes\n\ndef say_hello(name):\n    print(f\"Hello, {name}!\")\n    print(\"Welcome to the PEV coding class!\")\n\nsay_hello(\"Everyone\")"),
      spacer(),
      subheading("Cell B.2 - Function with Return"),
      codeBlock("# Some functions give you a value back\n\ndef add_numbers(a, b):\n    result = a + b\n    return result\n\nmy_sum = add_numbers(10, 25)\nprint(f\"10 + 25 = {my_sum}\")"),
      spacer(),
      subheading("Cell B.3 - Practice (Fill in Blank)"),
      codeBlock("# Fill in the blank: multiply two numbers\n\ndef multiply_numbers(a, b):\n    result = a _____ b  # What goes here?\n    return result\n\nproduct = multiply_numbers(6, 7)\nprint(f\"6 x 7 = {product}\")  # Should print 42"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SECTION C ==========
      heading("Section C: Connecting to VESC"),
      spacer(),
      subheading("Cell C.1 - Header (Markdown)"),
      codeBlock("# Connecting to Your PEV\n\nNow we'll connect to real hardware! Make sure your PEV is powered ON."),
      spacer(),
      subheading("Cell C.2 - Connect Code"),
      codeBlock("import sys, os, time\nsys.path.append(os.path.dirname(os.path.dirname(os.path.abspath('__file__'))))\n\nfrom student_api import VESCStudentAPI\n\nvesc_api = VESCStudentAPI()\n\nif vesc_api.start():\n    print(\"Starting connection...\")\n    time.sleep(6)\n    \n    connected = vesc_api.get_connected_controllers()\n    vesc = vesc_api.get_controller(74)\n    \n    if 74 in connected and vesc.is_connected():\n        voltage = vesc.get_input_voltage()\n        print(f\"Connected to VESC controller!\")\n        print(f\"Battery Voltage: {voltage:.1f}V\")\n    else:\n        print(\"VESC not found! Is the PEV powered ON?\")\nelse:\n    print(\"Failed to start VESC system\")"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SECTION D ==========
      heading("Section D: Reading Telemetry"),
      spacer(),
      subheading("Cell D.1 - Read Voltage (Fill in Blank)"),
      codeBlock("# Fill in the blank to read voltage\n\nvoltage = vesc._________________()  # Fill this in!\nprint(f\"Battery Voltage: {voltage} V\")\n\n# Answer: get_input_voltage"),
      spacer(),
      subheading("Cell D.2 - Read RPM"),
      codeBlock("# Read motor RPM\n\nrpm = vesc.get_rpm()\nprint(f\"Motor RPM: {rpm}\")\n\n# RECORD RESULTS:\n# Motor NOT spinning: ______ RPM\n# Motor spinning: ______ RPM"),
      spacer(),
      subheading("Cell D.3 - Read Current"),
      codeBlock("# Read motor current\n\ncurrent = vesc.get_motor_current()\nprint(f\"Motor Current: {current} A\")\n\n# Will be 0 when motor isn't running - normal!"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SECTION E ==========
      heading("Section E: Fill-in-the-Blank Challenges"),
      spacer(),
      subheading("Cell E.1 - FET Temperature"),
      codeBlock("# CHALLENGE: Read controller (FET) temperature\n\ntemp = vesc.get_____temperature()  # 3 letters\nprint(f\"Controller Temperature: {____} C\")\n\n# Answers: get_fet_temperature(), temp"),
      spacer(),
      subheading("Cell E.2 - Motor Temperature"),
      codeBlock("# CHALLENGE: Read MOTOR temperature\n\nmotor_temp = vesc.get_____________()\nprint(f\"Motor Temperature: {motor_temp} C\")\n\n# Answer: get_motor_temperature"),
      spacer(),
      subheading("Cell E.3 - Multiple Readings"),
      codeBlock("# BOSS CHALLENGE: Read THREE values!\n\nvoltage = vesc.____________()\nrpm = vesc.____________()\nfet_temp = vesc.____________()\n\nprint(\"=== PEV Status ===\")\nprint(f\"Battery: {voltage} V\")\nprint(f\"Speed: {rpm} RPM\")\nprint(f\"Controller Temp: {fet_temp} C\")\n\n# Answers: get_input_voltage, get_rpm, get_fet_temperature"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SECTION F ==========
      heading("Section F: Matching Exercise"),
      spacer(),
      subheading("Cell F.1 - Instructions (Markdown)"),
      codeBlock("## Matching Challenge!\n\n1. How fast is the motor spinning?\n2. How much battery do I have?\n3. Is the controller getting hot?\n4. How much electricity is the motor using?\n5. How hot is the motor itself?\n\nFunctions:\nA. get_motor_temperature()\nB. get_rpm()\nC. get_input_voltage()\nD. get_motor_current()\nE. get_fet_temperature()"),
      spacer(),
      subheading("Cell F.2 - Student Answers"),
      codeBlock("# Enter your answers (letters)\n\nanswer_1 = \"___\"\nanswer_2 = \"___\"\nanswer_3 = \"___\"\nanswer_4 = \"___\"\nanswer_5 = \"___\"\n\nprint(\"Answers recorded! Run next cell to check.\")"),
      spacer(),
      subheading("Cell F.3 - Check Answers"),
      codeBlock("correct = {1: \"B\", 2: \"C\", 3: \"E\", 4: \"D\", 5: \"A\"}\nscore = 0\nfor i in range(1, 6):\n    student = eval(f\"answer_{i}\").upper()\n    if student == correct[i]:\n        print(f\"Question {i}: Correct!\")\n        score += 1\n    else:\n        print(f\"Question {i}: Wrong. Your: {student}, Correct: {correct[i]}\")\nprint(f\"\\nScore: {score}/5\")"),

      new Paragraph({ children: [new PageBreak()] }),

      // ========== SECTION G ==========
      heading("Section G: Wrap-Up"),
      spacer(),
      subheading("Cell G.1 - Clean Shutdown"),
      codeBlock("# Always clean up when done!\n\nvesc_api.stop()\nprint(\"VESC connection closed safely\")\nprint(\"Great job today! See you in Module 2!\")"),
      spacer(),
      subheading("Cell G.2 - Summary (Markdown)"),
      codeBlock("## Module 1 Complete!\n\nWhat you learned:\n- How to use Jupyter Notebooks\n- How to run and stop code\n- What an API is\n- How to connect to the VESC\n- How to read voltage, RPM, and temperature\n- That the data is REAL-TIME!\n\nComing up in Module 2:\n- Building a live dashboard\n- Continuous data monitoring\n- Data logging"),

    ]
  }]
});

// Generate the document
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("Module_01_Slides_Text.docx", buffer);
  console.log("Module 1 Slides Text document created successfully!");
});
