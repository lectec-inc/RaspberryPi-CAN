const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        Header, Footer, AlignmentType, LevelFormat, HeadingLevel,
        BorderStyle, WidthType, ShadingType, PageNumber, PageBreak } = require('docx');
const fs = require('fs');

// Lectec Brand Colors (from PDF analysis)
const colors = {
  lectecBlue: "2196F3",
  lectecYellow: "FFCA28", 
  lectecBlack: "1A1A1A",
  lectecDarkBlue: "1976D2",
  lectecLightBlue: "E3F2FD",
  white: "FFFFFF",
  gray100: "F5F5F5",
  gray200: "EEEEEE",
  gray300: "E0E0E0",
  gray600: "757575",
  gray800: "424242",
  success: "4CAF50",
  warning: "FF9800",
  danger: "F44336"
};

const border = { style: BorderStyle.SINGLE, size: 1, color: colors.gray300 };
const borders = { top: border, bottom: border, left: border, right: border };
const thickLeftBorder = { style: BorderStyle.SINGLE, size: 16, color: colors.lectecBlue };

// Numbering configuration
const numberingConfig = [
  { reference: "bullets", levels: [
    { level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT, 
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
    { level: 1, format: LevelFormat.BULLET, text: "\u25E6", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 1080, hanging: 360 } } } }
  ]},
  { reference: "numbers", levels: [
    { level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } } }
  ]}
];

// Helper functions
function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 400, after: 200 },
    children: [new TextRun({ text, bold: true, size: 40, color: colors.lectecBlue, font: "Arial" })]
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 350, after: 150 },
    children: [new TextRun({ text, bold: true, size: 32, color: colors.lectecDarkBlue, font: "Arial" })]
  });
}

function heading3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 280, after: 120 },
    children: [new TextRun({ text, bold: true, size: 26, color: colors.lectecBlack, font: "Arial" })]
  });
}

function heading4(text) {
  return new Paragraph({
    spacing: { before: 200, after: 100 },
    children: [new TextRun({ text, bold: true, size: 22, color: colors.gray800, font: "Arial" })]
  });
}

function para(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 120 },
    children: [new TextRun({ text, size: 22, font: "Arial", ...opts })]
  });
}

function bullet(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "bullets", level },
    spacing: { after: 80 },
    children: [new TextRun({ text, size: 22, font: "Arial" })]
  });
}

function spacer(size = 200) {
  return new Paragraph({ spacing: { after: size }, children: [] });
}

function colorSwatch(name, hex, usage) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    columnWidths: [1500, 2000, 5860],
    rows: [new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 1500, type: WidthType.DXA },
          shading: { fill: hex, type: ShadingType.CLEAR },
          margins: { top: 100, bottom: 100, left: 100, right: 100 },
          children: [new Paragraph({ children: [] })]
        }),
        new TableCell({
          borders,
          width: { size: 2000, type: WidthType.DXA },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          children: [
            new Paragraph({ children: [new TextRun({ text: name, bold: true, size: 20, font: "Arial" })] }),
            new Paragraph({ children: [new TextRun({ text: "#" + hex, size: 18, font: "Courier New", color: colors.gray600 })] })
          ]
        }),
        new TableCell({
          borders,
          width: { size: 5860, type: WidthType.DXA },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          children: [new Paragraph({ children: [new TextRun({ text: usage, size: 20, font: "Arial" })] })]
        })
      ]
    })]
  });
}

function simpleTable(headers, rows, colWidths) {
  const headerRow = new TableRow({
    children: headers.map((h, i) => new TableCell({
      borders,
      width: { size: colWidths[i], type: WidthType.DXA },
      shading: { fill: colors.lectecLightBlue, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      children: [new Paragraph({ children: [new TextRun({ text: h, bold: true, size: 20, font: "Arial" })] })]
    }))
  });
  
  const dataRows = rows.map((row, idx) => new TableRow({
    children: row.map((cell, i) => new TableCell({
      borders,
      width: { size: colWidths[i], type: WidthType.DXA },
      shading: { fill: idx % 2 === 1 ? colors.gray100 : colors.white, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      children: [new Paragraph({ children: [new TextRun({ text: String(cell), size: 19, font: "Arial" })] })]
    }))
  }));
  
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    columnWidths: colWidths,
    rows: [headerRow, ...dataRows]
  });
}

function specTable(title, specs) {
  const rows = specs.map((s, idx) => new TableRow({
    children: [
      new TableCell({
        borders: { ...borders, left: thickLeftBorder },
        width: { size: 2500, type: WidthType.DXA },
        shading: { fill: idx % 2 === 0 ? colors.white : colors.gray100, type: ShadingType.CLEAR },
        margins: { top: 60, bottom: 60, left: 120, right: 80 },
        children: [new Paragraph({ children: [new TextRun({ text: s.label, bold: true, size: 18, font: "Arial", color: colors.gray800 })] })]
      }),
      new TableCell({
        borders,
        width: { size: 6860, type: WidthType.DXA },
        shading: { fill: idx % 2 === 0 ? colors.white : colors.gray100, type: ShadingType.CLEAR },
        margins: { top: 60, bottom: 60, left: 120, right: 120 },
        children: [new Paragraph({ children: [new TextRun({ text: s.value, size: 18, font: "Arial" })] })]
      })
    ]
  }));
  
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    columnWidths: [2500, 6860],
    rows: [
      new TableRow({
        children: [new TableCell({
          borders: { ...borders, left: thickLeftBorder },
          columnSpan: 2,
          width: { size: 9360, type: WidthType.DXA },
          shading: { fill: colors.lectecLightBlue, type: ShadingType.CLEAR },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          children: [new Paragraph({ children: [new TextRun({ text: title, bold: true, size: 20, font: "Arial", color: colors.lectecDarkBlue })] })]
        })]
      }),
      ...rows
    ]
  });
}

function slideHeader(num, title) {
  return new Paragraph({
    spacing: { before: 300, after: 150 },
    shading: { fill: colors.lectecBlue, type: ShadingType.CLEAR },
    children: [new TextRun({ text: `  SLIDE ${num}: ${title}  `, bold: true, size: 24, font: "Arial", color: colors.white })]
  });
}

function speakerNotesBox(notes) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    columnWidths: [9360],
    rows: [new TableRow({
      children: [new TableCell({
        borders: { top: border, bottom: border, right: border, left: { style: BorderStyle.SINGLE, size: 12, color: colors.lectecYellow } },
        width: { size: 9360, type: WidthType.DXA },
        shading: { fill: "FFFDE7", type: ShadingType.CLEAR },
        margins: { top: 100, bottom: 100, left: 150, right: 150 },
        children: notes.map(n => new Paragraph({
          numbering: { reference: "bullets", level: 0 },
          spacing: { after: 60 },
          children: [new TextRun({ text: n, size: 18, font: "Arial", color: colors.gray800 })]
        }))
      })]
    })]
  });
}

function imagePromptBox(promptId, dimensions, prompt) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    columnWidths: [9360],
    rows: [new TableRow({
      children: [new TableCell({
        borders,
        width: { size: 9360, type: WidthType.DXA },
        shading: { fill: colors.gray100, type: ShadingType.CLEAR },
        margins: { top: 100, bottom: 100, left: 150, right: 150 },
        children: [
          new Paragraph({ spacing: { after: 60 }, children: [
            new TextRun({ text: promptId, bold: true, size: 18, font: "Arial", color: colors.lectecDarkBlue }),
            new TextRun({ text: ` (${dimensions})`, size: 18, font: "Arial", color: colors.gray600 })
          ]}),
          new Paragraph({ children: [new TextRun({ text: prompt, size: 17, font: "Arial", italics: true })] })
        ]
      })]
    })]
  });
}

// Build content array
const content = [];

// ===== TITLE PAGE =====
content.push(
  new Paragraph({ spacing: { before: 1800 }, children: [] }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "LECTEC", bold: true, size: 72, font: "Arial", color: colors.lectecBlue })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 300 },
    children: [new TextRun({ text: "POWERPOINT DESIGN GUIDE", bold: true, size: 48, font: "Arial", color: colors.lectecBlack })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [new TextRun({ text: "Complete Slide Specifications for the", size: 26, font: "Arial", color: colors.gray600 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 400 },
    children: [new TextRun({ text: "PEV AI & CAN Communication Curriculum", size: 28, font: "Arial", color: colors.lectecDarkBlue })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "14 Modules \u2022 200+ Slides \u2022 Full Specifications", size: 22, font: "Arial", color: colors.gray600 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 1000 },
    children: [new TextRun({ text: "Including Nano Banana Image Prompts & Animation Sequences", size: 20, font: "Arial", color: colors.gray600 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Version 1.0", size: 20, font: "Arial", color: colors.gray600, italics: true })]
  })
);

// ===== TABLE OF CONTENTS =====
content.push(
  new Paragraph({ children: [new PageBreak()] }),
  heading1("Table of Contents"),
  spacer(100),
  para("PART 1: BRAND & DESIGN STANDARDS", { bold: true, color: colors.lectecBlue }),
  bullet("1.1 Brand Color Palette"),
  bullet("1.2 Typography System"),
  bullet("1.3 Slide Dimensions & Safe Zones"),
  bullet("1.4 Master Slide Templates (7 templates)"),
  bullet("1.5 Animation Standards"),
  bullet("1.6 Image Guidelines & Prompt Structure"),
  spacer(100),
  para("PART 2: MODULE SPECIFICATIONS (Modules 1-14)", { bold: true, color: colors.lectecBlue }),
  bullet("Complete slide-by-slide content for all 14 modules"),
  bullet("Exact text, positioning, animations, speaker notes"),
  bullet("Image placement coordinates and references"),
  spacer(100),
  para("PART 3: NANO BANANA IMAGE PROMPT APPENDIX", { bold: true, color: colors.lectecBlue }),
  bullet("All image generation prompts organized by module"),
  bullet("Exact dimensions for each image"),
  bullet("Consistent style guidelines")
);

// ===== PART 1: BRAND STANDARDS =====
content.push(
  new Paragraph({ children: [new PageBreak()] }),
  heading1("PART 1: Brand & Design Standards"),
  para("This section establishes the visual identity for all Lectec curriculum PowerPoints. Strict adherence ensures brand consistency across all 14 modules."),
  para('TERMINOLOGY NOTE: Throughout this document, "PEV" (Personal Electric Vehicle) refers to both skateboards and scooters.', { bold: true, color: colors.lectecDarkBlue })
);

// 1.1 Color Palette
content.push(
  new Paragraph({ children: [new PageBreak()] }),
  heading2("1.1 Brand Color Palette"),
  para("The Lectec color system derived from official brand materials. All hex codes are exact."),
  spacer(150),
  heading3("Primary Brand Colors"),
  spacer(80),
  colorSwatch("Lectec Blue", colors.lectecBlue, "Primary brand color. Headers, buttons, links, key UI elements."),
  spacer(80),
  colorSwatch("Lectec Yellow", colors.lectecYellow, "Secondary accent. Highlights, callouts, energy, CTAs."),
  spacer(80),
  colorSwatch("Lectec Black", colors.lectecBlack, "Primary text. Body copy, headlines on light backgrounds."),
  spacer(150),
  heading3("Extended Palette"),
  spacer(80),
  colorSwatch("Dark Blue", colors.lectecDarkBlue, "Hover states, secondary headers, depth."),
  spacer(80),
  colorSwatch("Light Blue", colors.lectecLightBlue, "Background tint, callout boxes, table headers."),
  spacer(80),
  colorSwatch("White", colors.white, "Primary slide background."),
  spacer(150),
  heading3("Semantic Colors"),
  spacer(80),
  colorSwatch("Success Green", colors.success, "Correct answers, safe conditions, positive states."),
  spacer(80),
  colorSwatch("Warning Orange", colors.warning, "Caution, attention needed, safety warnings."),
  spacer(80),
  colorSwatch("Danger Red", colors.danger, "Errors, unsafe conditions, critical alerts.")
);

// 1.2 Typography
content.push(
  new Paragraph({ children: [new PageBreak()] }),
  heading2("1.2 Typography System"),
  para("Consistent typography creates visual hierarchy and improves readability."),
  spacer(150),
  heading3("Font Families"),
  simpleTable(
    ["Usage", "Primary Font", "Fallback"],
    [
      ["Headlines & Titles", "Montserrat Bold", "Arial Bold"],
      ["Subheadings", "Montserrat SemiBold", "Arial Bold"],
      ["Body Text", "Open Sans Regular", "Arial Regular"],
      ["Code & Technical", "Fira Code", "Consolas"],
      ["Accent/Italics", "Montserrat Italic", "Arial Italic"]
    ],
    [3000, 3500, 2860]
  ),
  spacer(200),
  heading3("Type Scale (PowerPoint Points)"),
  simpleTable(
    ["Element", "Size", "Weight", "Line Height", "Color"],
    [
      ["Slide Title", "44pt", "Bold", "1.2", "#1A1A1A"],
      ["Section Header", "36pt", "Bold", "1.2", "#2196F3"],
      ["Subsection", "28pt", "SemiBold", "1.3", "#1976D2"],
      ["Body Text", "24pt", "Regular", "1.5", "#1A1A1A"],
      ["Bullet Points", "22pt", "Regular", "1.4", "#1A1A1A"],
      ["Captions", "18pt", "Regular", "1.4", "#757575"],
      ["Code", "20pt", "Mono", "1.3", "#1A1A1A"],
      ["Footer", "14pt", "Regular", "1.0", "#757575"]
    ],
    [2200, 1000, 1200, 1400, 3560]
  )
);

// 1.3 Slide Dimensions
content.push(
  new Paragraph({ children: [new PageBreak()] }),
  heading2("1.3 Slide Dimensions & Safe Zones"),
  para("All slides use 16:9 widescreen format (1920\u00d71080 pixels)."),
  spacer(150),
  heading3("Canvas Specifications"),
  simpleTable(
    ["Property", "Value", "Notes"],
    [
      ["Aspect Ratio", "16:9", "Widescreen standard"],
      ["Dimensions", "1920 \u00d7 1080 px", "Full HD"],
      ["PowerPoint Size", '13.333" \u00d7 7.5"', "When using inches"],
      ["DPI", "96", "Screen resolution"]
    ],
    [3000, 2500, 3860]
  ),
  spacer(200),
  heading3("Safe Zones & Margins"),
  simpleTable(
    ["Zone", "Position (px)", "Size", "Purpose"],
    [
      ["Top Margin", "Y: 0-80", "80px", "Header/logo area"],
      ["Bottom Margin", "Y: 1000-1080", "80px", "Footer/page number"],
      ["Left Margin", "X: 0-80", "80px", "Breathing room"],
      ["Right Margin", "X: 1840-1920", "80px", "Breathing room"],
      ["Title Zone", "Y: 80-200", "120px", "Slide title placement"],
      ["Content Area", "X: 80-1840, Y: 200-1000", "1760\u00d7800px", "Main content"]
    ],
    [2000, 2000, 1200, 4160]
  ),
  spacer(200),
  heading3("12-Column Grid"),
  para("Use a 12-column grid for consistent layouts:"),
  bullet("Full width: 1760px (12 columns)"),
  bullet("Half width: 860px (6 columns)"),
  bullet("Third width: 560px (4 columns)"),
  bullet("Quarter width: 420px (3 columns)"),
  bullet("Gutter width: 20px between columns")
);

// 1.4 Master Slides
content.push(
  new Paragraph({ children: [new PageBreak()] }),
  heading2("1.4 Master Slide Templates"),
  para("Seven master templates cover all layout needs. Each module uses these consistently."),
  spacer(150),
  
  heading3("Template 1: Title Slide"),
  specTable("Title Slide Specifications", [
    { label: "Use Case", value: "First slide of each module" },
    { label: "Background", value: "White (#FFFFFF) with subtle 5% opacity grid pattern" },
    { label: "Logo", value: "Lectec logo, top-left, X: 80px, Y: 40px, 200\u00d760px" },
    { label: "Module Badge", value: "Top-right, 'Module X of 14', Blue (#2196F3), 24pt" },
    { label: "Title", value: "Centered, Y: 400px, Black, Montserrat Bold, 56pt" },
    { label: "Subtitle", value: "Centered, Y: 500px, Gray (#757575), 28pt" },
    { label: "Accent Bar", value: "Yellow (#FFCA28), centered, Y: 580px, 200\u00d76px" }
  ]),
  spacer(200),
  
  heading3("Template 2: Goal/Demo Slide"),
  specTable("Goal Slide Specifications", [
    { label: "Use Case", value: "'BY THE END OF THIS LESSON...' slides" },
    { label: "Background", value: "Light blue (#E3F2FD) with subtle diagonal pattern" },
    { label: "Target Icon", value: "Centered, Y: 150px, 80\u00d780px" },
    { label: "Goal Header", value: "'BY THE END OF THIS LESSON, YOU WILL HAVE:', centered, Y: 260px, 32pt" },
    { label: "Goal Text", value: "Centered, Y: 350px, max-width 1400px, Black, 28pt" },
    { label: "Highlight Box", value: "Yellow (#FFCA28) at 15% opacity behind text, 3px blue border" }
  ]),
  spacer(200),
  
  heading3("Template 3: Content - Text Only"),
  specTable("Text Content Specifications", [
    { label: "Use Case", value: "Explanations, bullet lists, definitions" },
    { label: "Header Bar", value: "Blue (#2196F3), Y: 0-80px, full width" },
    { label: "Logo in Header", value: "White Lectec logo, X: 80px, Y: 20px, 120\u00d736px" },
    { label: "Slide Title", value: "X: 80px, Y: 100px, Black, 44pt bold" },
    { label: "Body Area", value: "X: 80px, Y: 200px, 1760\u00d7700px" },
    { label: "Footer", value: "Gray line at Y: 1000px, module name left, slide # right" }
  ]),
  spacer(200),
  
  heading3("Template 4: Split Layout (Text + Image)"),
  specTable("Split Layout Specifications", [
    { label: "Use Case", value: "Concept with supporting visual" },
    { label: "Left Column", value: "X: 80px, Width: 860px (text content)" },
    { label: "Right Column", value: "X: 980px, Width: 860px (image)" },
    { label: "Image Area", value: "X: 980px, Y: 180px, 860\u00d7720px, 8px rounded corners" },
    { label: "Caption", value: "Centered below image, Y: 920px, Gray, 16pt" }
  ])
);

content.push(
  new Paragraph({ children: [new PageBreak()] }),
  heading3("Template 5: Full Image"),
  specTable("Full Image Specifications", [
    { label: "Use Case", value: "Diagrams, architecture, photos needing full attention" },
    { label: "Title", value: "X: 80px, Y: 100px, 36pt (smaller to maximize image)" },
    { label: "Image Area", value: "X: 80px, Y: 180px, 1760\u00d7780px" },
    { label: "Image Style", value: "8px rounded corners, subtle drop shadow" }
  ]),
  spacer(200),
  
  heading3("Template 6: Two-Column Comparison"),
  specTable("Comparison Specifications", [
    { label: "Use Case", value: "Before/after, A vs B comparisons" },
    { label: "Left Header", value: "X: 80px, Y: 180px, Blue, 28pt bold" },
    { label: "Left Content", value: "X: 80px, Y: 240px, Width: 840px" },
    { label: "Divider", value: "Vertical line at X: 960px, Gray (#E0E0E0)" },
    { label: "VS Badge", value: "Optional yellow circle at X: 960px, Y: 450px" },
    { label: "Right Header", value: "X: 1000px, Y: 180px, Blue, 28pt bold" },
    { label: "Right Content", value: "X: 1000px, Y: 240px, Width: 840px" }
  ]),
  spacer(200),
  
  heading3("Template 7: Section Header"),
  specTable("Section Header Specifications", [
    { label: "Use Case", value: "Transition between major sections" },
    { label: "Background", value: "Solid Lectec Blue (#2196F3)" },
    { label: "Icon", value: "Centered, Y: 280px, 150\u00d7150px, white outline style" },
    { label: "Title", value: "Centered, Y: 450px, White, 52pt bold" },
    { label: "Subtitle", value: "Centered, Y: 550px, White at 80%, 28pt" }
  ])
);

// 1.5 Animation Standards
content.push(
  new Paragraph({ children: [new PageBreak()] }),
  heading2("1.5 Animation Standards"),
  para("Consistent animations create polish. All animations enhance comprehension, not distract."),
  spacer(150),
  
  heading3("Slide Transitions"),
  simpleTable(
    ["Transition", "Duration", "Use Case"],
    [
      ["Fade", "0.5s", "Default between all slides"],
      ["Push Left", "0.4s", "Moving forward in sequence"],
      ["Morph", "0.7s", "Between related diagrams"],
      ["None", "0s", "Rapid-fire sequences only"]
    ],
    [2500, 1500, 5360]
  ),
  spacer(200),
  
  heading3("Element Animations"),
  simpleTable(
    ["Element", "Animation", "Duration", "Trigger"],
    [
      ["Slide Title", "Fade + Float Up", "0.4s", "On load"],
      ["Bullet Points", "Fade + Float Up", "0.3s each", "On click (sequential)"],
      ["Images", "Fade + Scale 95%\u2192100%", "0.5s", "On load or click"],
      ["Code Blocks", "Fade", "0.3s", "On click"],
      ["Callout Boxes", "Fade + Float Up", "0.4s", "On click"],
      ["Numbers/Stats", "Count Up", "0.8s", "On click"]
    ],
    [2200, 2200, 1400, 3560]
  ),
  spacer(200),
  
  heading3("Animation Rules"),
  bullet("Delay between sequential bullets: 0.1s"),
  bullet("Maximum 2 animation types per slide"),
  bullet("Safety information: NO delays (appears immediately)"),
  bullet("Never use: Bounce, Spin, Swivel, or novelty effects"),
  bullet("Never exceed 1s for any single animation")
);

// 1.6 Image Guidelines  
content.push(
  new Paragraph({ children: [new PageBreak()] }),
  heading2("1.6 Image Guidelines"),
  para("High-quality imagery reinforces the Lectec brand and improves learning."),
  spacer(150),
  
  heading3("Image Types"),
  simpleTable(
    ["Type", "Style", "Use Case"],
    [
      ["Hardware Photos", "Photorealistic, clean background", "Actual PEV components"],
      ["Concept Diagrams", "Flat illustration, Lectec colors", "Abstract concepts"],
      ["System Architecture", "Clean lines, labeled boxes", "Data flow, relationships"],
      ["Icons", "Outline style, 3px stroke", "Bullet accents, features"],
      ["Screenshots", "Actual Jupyter output", "Expected code results"],
      ["People", "Diverse, safety gear, engaged", "PEV use in classroom"]
    ],
    [2500, 3000, 3860]
  ),
  spacer(200),
  
  heading3("Standard Dimensions"),
  simpleTable(
    ["Placement", "Dimensions", "Notes"],
    [
      ["Full slide image", "1760\u00d7780 px", "Below title, full width"],
      ["Split layout (right)", "860\u00d7720 px", "Right column"],
      ["Hero image", "1400\u00d7600 px", "Centered, prominent"],
      ["Grid item (3-up)", "540\u00d7350 px", "Project previews"],
      ["Icon", "64\u00d764 or 128\u00d7128 px", "Square graphics"]
    ],
    [2500, 2000, 4860]
  ),
  spacer(200),
  
  heading3("Image Treatment"),
  bullet("All images: 8px rounded corners"),
  bullet("Drop shadow: 0px X, 4px Y, 10px blur, 10% black opacity"),
  bullet("Photos color-corrected to match Lectec blue tones"),
  bullet("Alt-text required for accessibility")
);

// ===== PART 2: MODULE SPECIFICATIONS =====
content.push(
  new Paragraph({ children: [new PageBreak()] }),
  heading1("PART 2: Module Slide Specifications"),
  para("Complete specifications for every slide in all 14 modules. Each entry includes exact text, layout, animations, speaker notes, and image references."),
  spacer(100),
  para("Note: All content uses 'PEV' (Personal Electric Vehicle) as the agnostic term for skateboard/scooter.", { bold: true, color: colors.lectecDarkBlue })
);

// ===== MODULE 1 COMPLETE =====
content.push(
  new Paragraph({ children: [new PageBreak()] }),
  heading2("MODULE 1: System Introduction"),
  para("15 slides \u2022 45 minutes \u2022 Day 1 of 14"),
  spacer(100),
  specTable("Module Overview", [
    { label: "Learning Goal", value: "Connect to the PEV motor controller and read live vehicle data" },
    { label: "End Result", value: "Working VESC connection displaying real battery voltage" },
    { label: "Vocabulary", value: "CAN bus, VESC, Telemetry, Raspberry Pi, Controller" },
    { label: "Notebook", value: "01_System_Introduction.ipynb" }
  ]),
  spacer(200)
);

// Module 1, Slide 1
content.push(
  slideHeader(1, "Title Slide"),
  specTable("Slide Specifications", [
    { label: "Template", value: "Title Slide" },
    { label: "Duration", value: "30 seconds" },
    { label: "Transition In", value: "Fade (0.5s)" }
  ]),
  spacer(100),
  heading4("Content"),
  para("TITLE: System Introduction", { bold: true }),
  para("SUBTITLE: Your First Connection to an Intelligent Vehicle"),
  para("FOOTER: Module 1 of 14 | PEV AI & CAN Curriculum"),
  spacer(100),
  heading4("Animation Sequence"),
  bullet("0.0s: Logo fades in"),
  bullet("0.3s: Title fades up from below"),
  bullet("0.6s: Subtitle fades in"),
  bullet("0.9s: Yellow accent bar grows from center"),
  spacer(100),
  heading4("Speaker Notes"),
  speakerNotesBox([
    "Welcome students to Day 1 of the PEV curriculum",
    "Build excitement: 'Today you connect to a REAL electric vehicle'",
    "This is the same technology in Teslas, e-bikes, and scooters",
    "Keep this slide brief - 30 seconds max"
  ]),
  spacer(200)
);

// Module 1, Slide 2
content.push(
  slideHeader(2, "Today's Goal"),
  specTable("Slide Specifications", [
    { label: "Template", value: "Goal/Demo Slide" },
    { label: "Duration", value: "2 minutes (CRITICAL)" },
    { label: "Background", value: "Light blue (#E3F2FD)" }
  ]),
  spacer(100),
  heading4("Content"),
  para("ICON: Target emoji or graphic, centered top"),
  para("HEADER: BY THE END OF THIS LESSON, YOU WILL HAVE:", { bold: true }),
  para("BODY TEXT:"),
  para('"A working connection to a real motor controller on an electric vehicle. You will read live battery voltage data from the actual PEV and understand how the entire system communicates. This is your first step toward building an intelligent vehicle system!"'),
  spacer(100),
  heading4("Image Placement"),
  simpleTable(
    ["Element", "Position", "Size"],
    [
      ["Demo Screenshot", "Right side, X: 1000px, Y: 350px", "800\u00d7400px"],
      ["Shows successful voltage reading", "Jupyter notebook output", "IMG_01_02"]
    ],
    [3000, 3500, 2860]
  ),
  spacer(100),
  heading4("Animation Sequence"),
  bullet("0.0s: Target icon drops in with bounce"),
  bullet("0.3s: Header text fades up"),
  bullet("0.6s: Body text fades in"),
  bullet("1.0s: Screenshot fades in from right"),
  spacer(100),
  heading4("Speaker Notes"),
  speakerNotesBox([
    "THIS IS THE MOST IMPORTANT SLIDE - spend 2 full minutes here",
    "If possible, run a LIVE DEMO showing actual voltage reading",
    "Say: 'See this? 25.2 volts. Real data from a real vehicle.'",
    "Say: 'In 40 minutes, you will do this yourself.'",
    "Let students ask questions - build genuine excitement",
    "This creates the 'end in mind' motivation for the entire lesson"
  ]),
  spacer(200)
);

// Module 1, Slide 3
content.push(
  slideHeader(3, "What You Will Build This Course"),
  specTable("Slide Specifications", [
    { label: "Template", value: "Full Image" },
    { label: "Duration", value: "1.5 minutes" },
    { label: "Layout", value: "3-image grid showing final projects" }
  ]),
  spacer(100),
  heading4("Content"),
  para("TITLE: What You Will Build This Course", { bold: true }),
  para("SUBTITLE: Three major projects showcasing progressively advanced skills"),
  spacer(80),
  para("IMAGE GRID (3 columns):"),
  bullet("Left: Project 1 - CAN Dashboard (Day 5)"),
  bullet("Center: Project 2 - AI Safety System (Day 10)"),
  bullet("Right: Project 3 - ADAS Feature (Day 14)"),
  spacer(100),
  heading4("Image Placement"),
  simpleTable(
    ["Image", "Position", "Size", "Reference"],
    [
      ["Dashboard screenshot", "X: 80px, Y: 200px", "540\u00d7350px", "IMG_01_03a"],
      ["AI detection overlay", "X: 660px, Y: 200px", "540\u00d7350px", "IMG_01_03b"],
      ["ADAS alert system", "X: 1240px, Y: 200px", "540\u00d7350px", "IMG_01_03c"]
    ],
    [2500, 2500, 1800, 2560]
  ),
  spacer(100),
  heading4("Speaker Notes"),
  speakerNotesBox([
    "Show the big picture - where this 14-day journey leads",
    "Point to each project briefly: 'Day 5... Day 10... Day 14'",
    "Emphasize: 'By Day 14, you build tech similar to modern cars'",
    "This roadmap helps students see the full progression"
  ]),
  spacer(200)
);

// Module 1, Slide 4
content.push(
  slideHeader(4, "The Complete PEV System"),
  specTable("Slide Specifications", [
    { label: "Template", value: "Full Image" },
    { label: "Duration", value: "2 minutes" },
    { label: "Image", value: "Annotated photo of complete PEV" }
  ]),
  spacer(100),
  heading4("Content"),
  para("TITLE: The Complete PEV System", { bold: true }),
  para("SUBTITLE: Your Personal Electric Vehicle contains five major components"),
  spacer(80),
  para("LABELED COMPONENTS (animated callouts):"),
  bullet("1. Raspberry Pi - The brain"),
  bullet("2. AI Camera - The eyes"),
  bullet("3. VESC Controller - The muscle controller"),
  bullet("4. Motor - The muscle"),
  bullet("5. Battery - The energy source"),
  spacer(100),
  heading4("Image Placement"),
  simpleTable(
    ["Element", "Position", "Size"],
    [
      ["Main PEV photo", "X: 80px, Y: 180px", "1760\u00d7700px"],
      ["Component labels", "Animated callout boxes", "Blue bg, white text"],
      ["Arrows", "Point from labels to components", "Blue (#2196F3)"]
    ],
    [3000, 3000, 3360]
  ),
  spacer(100),
  heading4("Animation Sequence"),
  bullet("0.0s: Full system image fades in"),
  bullet("On click: Each label appears one at a time (0.3s each)"),
  bullet("Labels appear in order: 1, 2, 3, 4, 5"),
  spacer(100),
  heading4("Speaker Notes"),
  speakerNotesBox([
    "Use this as an orientation - students understand the physical system",
    "Click through labels one at a time, explaining each briefly",
    "If hardware available, point to actual components",
    "Key message: 'All parts COMMUNICATE - that makes it intelligent'"
  ]),
  spacer(200)
);

// Module 1, Slide 5
content.push(
  slideHeader(5, "The Raspberry Pi"),
  specTable("Slide Specifications", [
    { label: "Template", value: "Split Layout (Text + Image)" },
    { label: "Duration", value: "1.5 minutes" },
    { label: "Image", value: "Product photo of Pi Zero 2W" }
  ]),
  spacer(100),
  heading4("Content"),
  para("TITLE: The Raspberry Pi: Your Vehicle's Brain", { bold: true }),
  spacer(80),
  para("BULLET POINTS:"),
  bullet("A complete computer smaller than a credit card"),
  bullet("Runs Python code and Jupyter notebooks"),
  bullet("Connects to sensors, cameras, and controllers"),
  bullet("Processes data and makes decisions"),
  bullet("Cost: ~$15 (Pi Zero 2W)"),
  spacer(100),
  heading4("Image Placement"),
  simpleTable(
    ["Element", "Position", "Size"],
    [
      ["Pi Zero 2W photo", "X: 1000px, Y: 200px", "800\u00d7600px"],
      ["Clean white background", "Product photography style", "IMG_01_05"]
    ],
    [3000, 3000, 3360]
  ),
  spacer(100),
  heading4("Speaker Notes"),
  speakerNotesBox([
    "Compare to phones: 'This tiny computer does many things your phone does'",
    "Emphasize: It runs REAL Python - same language professionals use",
    "The Pi is the BRAIN - doesn't move anything, but controls everything",
    "If you have a spare Pi, carefully pass it around"
  ]),
  spacer(200)
);

// Module 1, Slide 6
content.push(
  slideHeader(6, "The VESC Controller"),
  specTable("Slide Specifications", [
    { label: "Template", value: "Split Layout (Text + Image)" },
    { label: "Duration", value: "1.5 minutes" },
    { label: "Image", value: "Product photo of VESC board" }
  ]),
  spacer(100),
  heading4("Content"),
  para("TITLE: The VESC: Your Motor's Controller", { bold: true }),
  spacer(80),
  para("BULLET POINTS:"),
  bullet("VESC = Vedder Electronic Speed Controller"),
  bullet("Controls how fast the motor spins"),
  bullet("Monitors battery voltage and temperature"),
  bullet("Reports data back to the Raspberry Pi"),
  bullet("Used in real electric vehicles worldwide"),
  spacer(100),
  heading4("Image Placement"),
  simpleTable(
    ["Element", "Position", "Size"],
    [
      ["VESC controller photo", "X: 1000px, Y: 200px", "800\u00d7600px"],
      ["Shows PCB with components", "Professional product photo", "IMG_01_06"]
    ],
    [3000, 3000, 3360]
  ),
  spacer(100),
  heading4("Speaker Notes"),
  speakerNotesBox([
    "Analogy: 'If the Pi is the brain, the VESC is the muscle controller'",
    "The Pi decides WHAT to do, the VESC makes it HAPPEN",
    "The VESC knows everything about the motor - speed, power, temperature",
    "Today we will READ data FROM the VESC"
  ]),
  spacer(200)
);

// Module 1, Slide 7
content.push(
  slideHeader(7, "What is CAN Bus?"),
  specTable("Slide Specifications", [
    { label: "Template", value: "Split Layout (Text + Image)" },
    { label: "Duration", value: "2 minutes" },
    { label: "Image", value: "CAN bus diagram" }
  ]),
  spacer(100),
  heading4("Content"),
  para("TITLE: What is CAN Bus?", { bold: true }),
  spacer(80),
  para("DEFINITION BOX (highlighted):"),
  para("CAN = Controller Area Network", { bold: true, color: colors.lectecBlue }),
  spacer(80),
  para("BULLET POINTS:"),
  bullet("A communication system invented in the 1980s for cars"),
  bullet("Allows multiple devices to talk on the same wire"),
  bullet("Used in EVERY modern car, truck, and bus"),
  bullet("Extremely reliable - designed for noisy environments"),
  bullet("Your PEV uses the exact same protocol as a Tesla!"),
  spacer(100),
  heading4("Image Placement"),
  simpleTable(
    ["Element", "Position", "Size"],
    [
      ["CAN diagram", "X: 1000px, Y: 250px", "800\u00d7500px"],
      ["Shows Pi and VESC connected", "Flat illustration style", "IMG_01_07"]
    ],
    [3000, 3000, 3360]
  ),
  spacer(100),
  heading4("Speaker Notes"),
  speakerNotesBox([
    "This is a KEY concept - spend time here",
    "Analogy: 'CAN bus is like a group chat where everyone sees all messages'",
    "Draw on board if helpful: Pi <-> CAN <-> VESC",
    "Fun fact: A modern car has 70+ devices all talking on CAN"
  ]),
  spacer(200)
);

// Module 1, Slide 8
content.push(
  slideHeader(8, "Why CAN Bus?"),
  specTable("Slide Specifications", [
    { label: "Template", value: "Two-Column Comparison" },
    { label: "Duration", value: "1.5 minutes" },
    { label: "Layout", value: "Before/After comparison" }
  ]),
  spacer(100),
  heading4("Content"),
  para("TITLE: Why CAN Bus?", { bold: true }),
  spacer(80),
  para("LEFT COLUMN - 'WITHOUT CAN':"),
  bullet("Separate wire for each device"),
  bullet("Complex wiring (70+ wires!)"),
  bullet("Hard to add new devices"),
  bullet("Interference causes errors"),
  spacer(80),
  para("RIGHT COLUMN - 'WITH CAN':"),
  bullet("Single pair of wires for everything"),
  bullet("Simple, clean wiring"),
  bullet("Easy to add new devices"),
  bullet("Built-in error checking"),
  spacer(100),
  heading4("Image Placement"),
  simpleTable(
    ["Element", "Position", "Size"],
    [
      ["Messy wiring illustration", "Left column, Y: 400px", "400\u00d7300px (IMG_01_08a)"],
      ["Clean wiring illustration", "Right column, Y: 400px", "400\u00d7300px (IMG_01_08b)"],
      ["VS badge (optional)", "Center, Y: 350px", "60\u00d760px yellow circle"]
    ],
    [3000, 3000, 3360]
  ),
  spacer(100),
  heading4("Speaker Notes"),
  speakerNotesBox([
    "Visual comparison makes the benefit obvious",
    "Point out: 'Your PEV uses just TWO wires to connect everything'",
    "This is why CAN became the universal standard in vehicles"
  ]),
  spacer(200)
);

// Module 1, Slides 9-15 (abbreviated format)
content.push(
  slideHeader(9, "The AI Camera (Preview)"),
  specTable("Slide Specifications", [
    { label: "Template", value: "Split Layout" },
    { label: "Duration", value: "1 minute" },
    { label: "Purpose", value: "Brief preview - build anticipation for AI section" }
  ]),
  spacer(100),
  heading4("Content"),
  para("TITLE: The AI Camera (Preview)", { bold: true }),
  para("BULLETS: Sony IMX500 - AI on sensor | 80 object types | No cloud needed | Coming Day 6!"),
  para("BADGE: 'Coming Day 6' yellow badge on image"),
  para("IMAGE: IMX500 camera module, 800\u00d7600px, right column (IMG_01_09)"),
  spacer(100),
  heading4("Speaker Notes"),
  speakerNotesBox([
    "Brief preview only - build anticipation",
    "Key point: 'The AI runs ON the camera - that makes it special'",
    "Don't go deep - plant the seed of excitement"
  ]),
  spacer(200),

  slideHeader(10, "How It All Connects"),
  specTable("Slide Specifications", [
    { label: "Template", value: "Full Image" },
    { label: "Duration", value: "2 minutes" },
    { label: "Purpose", value: "System architecture overview" }
  ]),
  spacer(100),
  heading4("Content"),
  para("TITLE: How It All Connects", { bold: true }),
  para("DIAGRAM: System architecture showing Battery \u2192 VESC \u2194 CAN \u2194 Pi \u2190 Camera"),
  para("ARROWS: Animated data flow with blue glow"),
  para("SIZE: 1760\u00d7700px (IMG_01_10)"),
  spacer(100),
  heading4("Speaker Notes"),
  speakerNotesBox([
    "This is the 'aha' moment - show how everything fits",
    "Trace data flow: 'Motor sends \u2192 VESC reads \u2192 CAN carries \u2192 Pi receives \u2192 You see!'",
    "Bidirectional: 'Data flows BOTH ways - we can read AND send commands'"
  ]),
  spacer(200),

  slideHeader(11, "Safety First"),
  specTable("Slide Specifications", [
    { label: "Template", value: "Section Header" },
    { label: "Duration", value: "30 seconds" },
    { label: "Background", value: "Warning Orange (#FF9800)" }
  ]),
  spacer(100),
  heading4("Content"),
  para("TITLE: \u26A0\uFE0F SAFETY FIRST", { bold: true }),
  para("SUBTITLE: Before we touch any equipment..."),
  para("ICON: Warning triangle, white, 100\u00d7100px centered"),
  spacer(100),
  heading4("Speaker Notes"),
  speakerNotesBox([
    "Pause here - change tone to serious",
    "Say: 'Before we connect, we need to talk about safety'",
    "This transition signals importance of what follows"
  ]),
  spacer(200),

  slideHeader(12, "Safety Rules"),
  specTable("Slide Specifications", [
    { label: "Template", value: "Text Only" },
    { label: "Duration", value: "2 minutes" },
    { label: "Animation", value: "Each rule appears on click" }
  ]),
  spacer(100),
  heading4("Content"),
  para("TITLE: Five Safety Rules", { bold: true }),
  para("RULE 1: \uD83D\uDD0B BATTERIES - Never puncture, crush, or short-circuit. Report damage."),
  para("RULE 2: \u26A1 ELECTRICITY - Check connections before power. Never touch exposed wires."),
  para("RULE 3: \uD83D\uDD27 MOVING PARTS - Keep fingers away from motors during operation."),
  para("RULE 4: \uD83D\uDEE1\uFE0F TESTING - Always test with PEV secured on stand, not ground."),
  para("RULE 5: \uD83C\uDD98 EMERGENCY - Know the power switch. When in doubt, POWER OFF.", { bold: true }),
  para("(Rule 5 has yellow highlight background)"),
  spacer(100),
  heading4("Speaker Notes"),
  speakerNotesBox([
    "Read each rule aloud, have students repeat key points",
    "Ask: 'Where is the power switch?' - ensure everyone knows",
    "Rule 4 critical for today - we WILL run motor code",
    "Consider safety agreement signatures"
  ]),
  spacer(200),

  slideHeader(13, "Jupyter Notebooks"),
  specTable("Slide Specifications", [
    { label: "Template", value: "Split Layout" },
    { label: "Duration", value: "1.5 minutes" },
    { label: "Image", value: "Annotated Jupyter interface screenshot" }
  ]),
  spacer(100),
  heading4("Content"),
  para("TITLE: Working with Jupyter Notebooks", { bold: true }),
  para("BULLETS: Interactive text+code | Run one cell at a time | See results immediately | Auto-saves | Shift+Enter to run"),
  para("IMAGE: Screenshot with numbered callouts (1-cell, 2-run, 3-output), 860\u00d7650px (IMG_01_13)"),
  spacer(100),
  heading4("Speaker Notes"),
  speakerNotesBox([
    "Assume some students never used Jupyter",
    "Demo on screen: show cell, run it, show output",
    "Emphasize Shift+Enter - used hundreds of times"
  ]),
  spacer(200),

  slideHeader(14, "Your First Connection"),
  specTable("Slide Specifications", [
    { label: "Template", value: "Full Image" },
    { label: "Duration", value: "1.5 minutes" },
    { label: "Image", value: "Code screenshot with highlighted output" }
  ]),
  spacer(100),
  heading4("Content"),
  para("TITLE: Your First Connection: What to Expect", { bold: true }),
  para("CODE SHOWN: from student_api import VESCStudentAPI / vesc = VESCStudentAPI() / voltage = vesc.get_input_voltage() / print(f'Battery: {voltage}V')"),
  para("OUTPUT: 'Battery: 25.2V' with yellow glow highlight"),
  para("IMAGE SIZE: 1400\u00d7500px, centered (IMG_01_14)"),
  spacer(100),
  heading4("Speaker Notes"),
  speakerNotesBox([
    "Preview what students will do",
    "Point to code: 'Just 3 lines - import, connect, read'",
    "Point to output: 'Real voltage from real battery'",
    "Build confidence: 'See a number like this = success!'"
  ]),
  spacer(200),

  slideHeader(15, "Let's Go!"),
  specTable("Slide Specifications", [
    { label: "Template", value: "Section Header" },
    { label: "Duration", value: "30 seconds" },
    { label: "Background", value: "Lectec Blue (#2196F3)" }
  ]),
  spacer(100),
  heading4("Content"),
  para("TITLE: \uD83D\uDE80 YOUR TURN!", { bold: true }),
  para("SUBTITLE: Open 01_System_Introduction.ipynb and follow along"),
  para("ANIMATION: Rocket icon animates upward"),
  spacer(100),
  heading4("Speaker Notes"),
  speakerNotesBox([
    "Energy transition - get students excited",
    "Say: 'Notebooks open! Let's make this connection happen!'",
    "Begin circulating to help",
    "Refer back to Slide 2 (Goal) if students need motivation"
  ]),
  spacer(200)
);

// ===== MODULES 2-14 SUMMARY =====
content.push(
  new Paragraph({ children: [new PageBreak()] }),
  heading2("MODULES 2-14: Specification Summary"),
  para("The following modules follow the same detailed format as Module 1. Each slide includes: exact text content, image placement, animation sequence, and speaker notes."),
  spacer(150),

  heading3("Module 2: CAN Fundamentals (12 slides)"),
  simpleTable(
    ["Slide", "Title", "Template", "Key Content"],
    [
      ["1", "Title Slide", "Title", "CAN Fundamentals: Complete Telemetry Mastery"],
      ["2", "Today's Goal", "Goal", "Master all 18 data values from VESC"],
      ["3", "Review", "Split", "Quick recap of Day 1 connection"],
      ["4", "The 18 Data Points", "Full Image", "Category table: Motor, Power, Temp, Sensors"],
      ["5", "Motor Data", "Split", "RPM, current, duty cycle explained"],
      ["6", "Understanding Direction", "Comparison", "+/- values meaning"],
      ["7", "Power Data", "Split", "Voltage, current, energy tracking"],
      ["8", "Temperature Data", "Split", "FET/motor temps, safety thresholds"],
      ["9", "Advanced Sensors", "Text", "Tachometer, ADC, servo (reference)"],
      ["10", "The Magic Function", "Full Image", "get_all_telemetry() demo"],
      ["11", "When Data is Zero", "Split", "Why readings show 0, voltage always works"],
      ["12", "Your Turn", "Section Header", "Transition to notebook"]
    ],
    [700, 2200, 1300, 5160]
  ),
  spacer(200),

  heading3("Module 3: Data Visualization (10 slides)"),
  simpleTable(
    ["Slide", "Title", "Template", "Key Content"],
    [
      ["1", "Title Slide", "Title", "Building Your Vehicle Dashboard"],
      ["2", "Today's Goal", "Goal", "Custom real-time dashboard with warnings"],
      ["3", "Why Visualize?", "Split", "Numbers vs graphs, pattern recognition"],
      ["4", "Real-Time Updates", "Split", "clear_output() technique"],
      ["5", "Dashboard Design", "Full Image", "Layout principles, info hierarchy"],
      ["6", "Color Coding", "Text", "Green/yellow/red semantic colors"],
      ["7", "HTML in Jupyter", "Split", "display(HTML()) for formatting"],
      ["8", "Time-Series Graphs", "Split", "Matplotlib basics, live plots"],
      ["9", "Car Dashboard", "Full Image", "Real vehicle dashboard comparison"],
      ["10", "Your Turn", "Section Header", "Build your dashboard"]
    ],
    [700, 2200, 1300, 5160]
  ),
  spacer(200),

  heading3("Module 4: Motor Control (12 slides)"),
  simpleTable(
    ["Slide", "Title", "Template", "Key Content"],
    [
      ["1", "Title Slide", "Title", "Taking Control: Commanding Your Motor"],
      ["2", "Today's Goal", "Goal", "Smooth acceleration/deceleration sequence"],
      ["3", "SAFETY FIRST", "Section (Orange)", "Critical safety review"],
      ["4", "Three Control Methods", "Text", "Duty, current, brake overview"],
      ["5", "Duty Cycle Control", "Split", "Throttle %, -1.0 to 1.0 range"],
      ["6", "Current Control", "Split", "Torque control in amps"],
      ["7", "Regenerative Braking", "Split", "Motor as generator"],
      ["8", "Safety Flag", "Text", "MOTOR_CONTROL_ENABLED pattern"],
      ["9", "Command Sequence", "Full Image", "Check\u2192Command\u2192Verify\u2192Stop flowchart"],
      ["10", "Emergency Stop", "Text (highlighted)", "set_duty_cycle(0) critical"],
      ["11", "Real Car Comparison", "Split", "Cruise control, ABS parallels"],
      ["12", "Your Turn", "Section Header", "Careful! Hands-on control"]
    ],
    [700, 2200, 1300, 5160]
  )
);

content.push(
  new Paragraph({ children: [new PageBreak()] }),
  heading3("Module 5: CAN Capstone Project (8 slides)"),
  simpleTable(
    ["Slide", "Title", "Template", "Key Content"],
    [
      ["1", "Title Slide", "Title", "CAN Capstone Project"],
      ["2", "Your Challenge", "Goal", "Design a CAN-based project"],
      ["3", "Project Options", "Text", "Battery monitor, Performance analyzer, Temp safety"],
      ["4", "Requirements", "Text", "Minimum requirements checklist"],
      ["5", "Rubric", "Full Image", "Scoring table (100 points)"],
      ["6", "Development Tips", "Text", "Incremental building approach"],
      ["7", "Documentation", "Text", "Template sections"],
      ["8", "Present", "Section Header", "Presentation expectations"]
    ],
    [700, 2200, 1300, 5160]
  ),
  spacer(200),

  heading3("Module 6: AI Introduction (15 slides)"),
  simpleTable(
    ["Slide", "Title", "Template", "Key Content"],
    [
      ["1", "Title Slide", "Title", "Introduction to Artificial Intelligence"],
      ["2", "Today's Goal", "Goal", "Build AI confidence interpreter"],
      ["3", "AI Everywhere", "Full Image", "Daily life examples"],
      ["4", "Code vs AI", "Comparison", "Rules vs learning"],
      ["5", "How Humans See", "Split", "Vision analogy"],
      ["6", "How AI Sees", "Full Image", "Pixels to labels pipeline"],
      ["7", "Neural Networks", "Split", "Simple layer explanation"],
      ["8", "Training AI", "Split", "Learning from examples"],
      ["9", "IMX500 Camera", "Split", "Edge AI capabilities"],
      ["10", "Edge AI Advantage", "Text", "Speed, privacy, efficiency"],
      ["11", "Confidence Scores", "Full Image", "0.0-1.0 scale visual"],
      ["12", "Interpreting Confidence", "Text", "High/medium/low thresholds"],
      ["13", "Why Confidence Matters", "Split", "Filtering false positives"],
      ["14", "Bounding Boxes", "Split", "X,Y,W,H coordinates"],
      ["15", "Your Turn", "Section Header", "Transition to notebook"]
    ],
    [700, 2200, 1300, 5160]
  ),
  spacer(200),

  heading3("Module 7: Object Detection (12 slides)"),
  simpleTable(
    ["Slide", "Title", "Template", "Key Content"],
    [
      ["1", "Title Slide", "Title", "Live Object Detection"],
      ["2", "Today's Goal", "Goal", "Live multi-object detector"],
      ["3", "COCO Dataset", "Full Image", "80 objects grid"],
      ["4", "Categories", "Full Image", "Visual by category"],
      ["5", "Starting Camera", "Split", "Video pipeline"],
      ["6", "Detection Pipeline", "Full Image", "Camera\u2192AI\u2192Results\u2192Display"],
      ["7", "Reading Results", "Split", "Label + confidence + bbox"],
      ["8", "Accuracy Factors", "Comparison", "Lighting, distance, angle"],
      ["9", "Limitations", "Text", "What it can't detect"],
      ["10", "Filtering", "Split", "Threshold selection"],
      ["11", "Try These", "Text", "Classroom objects to test"],
      ["12", "Your Turn", "Section Header", "Live detection!"]
    ],
    [700, 2200, 1300, 5160]
  ),
  spacer(200),

  heading3("Module 8: AI + Hardware (12 slides)"),
  simpleTable(
    ["Slide", "Title", "Template", "Key Content"],
    [
      ["1", "Title Slide", "Title", "AI + Physical Response"],
      ["2", "Today's Goal", "Goal", "Detection-triggered alerts"],
      ["3", "GPIO Intro", "Split", "Pin basics"],
      ["4", "The Buzzer", "Split", "Wiring diagram"],
      ["5", "GPIO Control", "Text", "High/Low states"],
      ["6", "Detection + Action", "Split", "If detected AND confident \u2192 beep"],
      ["7", "Spam Problem", "Split", "Continuous detection issue"],
      ["8", "Cooldown Logic", "Full Image", "Rate limiting flowchart"],
      ["9", "Custom Patterns", "Text", "Object-specific sounds"],
      ["10", "Complete Pipeline", "Full Image", "Detection\u2192Filter\u2192Cooldown\u2192Alert"],
      ["11", "Real World", "Split", "Security, accessibility examples"],
      ["12", "Your Turn", "Section Header", "Build alert system"]
    ],
    [700, 2200, 1300, 5160]
  )
);

content.push(
  new Paragraph({ children: [new PageBreak()] }),
  heading3("Module 9: System Integration (12 slides)"),
  simpleTable(
    ["Slide", "Title", "Template", "Key Content"],
    [
      ["1", "Title Slide", "Title", "AI Meets Motor Control"],
      ["2", "Today's Goal", "Goal", "Smart safety monitor"],
      ["3", "What We Have", "Comparison", "Two data streams"],
      ["4", "Why Combine?", "Split", "Context from both sources"],
      ["5", "Example Scenario", "Split", "Person + moving = danger"],
      ["6", "Sensor Fusion", "Full Image", "Multi-sensor concept"],
      ["7", "How Cars Do It", "Split", "Tesla, Waymo fusion"],
      ["8", "Architecture", "Full Image", "Combined data flow"],
      ["9", "Conditional Logic", "Text", "IF person AND rpm>1000 THEN alert"],
      ["10", "Safety Levels", "Text", "Level 1-3 escalation"],
      ["11", "Data Freshness", "Split", "Handling stale data"],
      ["12", "Your Turn", "Section Header", "Build safety monitor"]
    ],
    [700, 2200, 1300, 5160]
  ),
  spacer(200),

  heading3("Module 10: AI Capstone Project (8 slides)"),
  simpleTable(
    ["Slide", "Title", "Template", "Key Content"],
    [
      ["1", "Title Slide", "Title", "AI Capstone Project"],
      ["2", "Your Challenge", "Goal", "Integrated AI+CAN project"],
      ["3", "Project Options", "Text", "Safety assistant, Parking helper, Traffic monitor"],
      ["4", "Requirements", "Text", "Integration requirements"],
      ["5", "Rubric", "Full Image", "Scoring (100 points)"],
      ["6", "Development Tips", "Text", "Testing both systems"],
      ["7", "Documentation", "Text", "Architecture diagram required"],
      ["8", "Present", "Section Header", "Demo expectations"]
    ],
    [700, 2200, 1300, 5160]
  ),
  spacer(200),

  heading3("Module 11: ADAS Introduction (18 slides)"),
  simpleTable(
    ["Slide", "Title", "Template", "Key Content"],
    [
      ["1", "Title Slide", "Title", "Advanced Driver Assistance Systems"],
      ["2", "Today's Goal", "Goal", "ADAS feature comparison chart"],
      ["3", "What is ADAS?", "Split", "Definition and scope"],
      ["4", "Timeline", "Full Image", "ABS to autonomy history"],
      ["5-10", "Feature Deep Dives", "Split (each)", "FCW, AEB, LDW, ACC, BSD, Parking"],
      ["11", "SAE Levels Overview", "Full Image", "Levels 0-5 diagram"],
      ["12", "Levels 0-2", "Text", "Driver assistance"],
      ["13", "Levels 3-5", "Text", "Automated driving"],
      ["14", "Current State", "Split", "Where cars are today"],
      ["15", "Sensors: Camera", "Split", "Vision systems"],
      ["16", "Sensors: Radar/Lidar", "Comparison", "Non-vision sensors"],
      ["17", "Company Compare", "Full Image", "Tesla vs Waymo vs Mobileye"],
      ["18", "Your PEV = Mini ADAS", "Split", "Mapping to real features"]
    ],
    [700, 2200, 1300, 5160]
  ),
  spacer(200),

  heading3("Module 12: ADAS Theory (15 slides)"),
  simpleTable(
    ["Slide", "Title", "Template", "Key Content"],
    [
      ["1", "Title Slide", "Title", "The Math Behind Safety"],
      ["2", "Today's Goal", "Goal", "TTC calculator"],
      ["3", "FCW Overview", "Split", "What it does"],
      ["4", "Core Problem", "Split", "Distance + closing speed"],
      ["5", "Distance Estimation", "Split", "Bounding box as proxy"],
      ["6", "Speed Conversion", "Split", "RPM to m/s"],
      ["7", "TTC Formula", "Full Image", "TTC = Distance / Speed"],
      ["8", "TTC Example", "Full Image", "Worked calculation"],
      ["9", "Alert Thresholds", "Full Image", "TTC-based levels"],
      ["10", "Sensor Fusion", "Split", "Why combine data"],
      ["11", "Fusion Benefits", "Comparison", "Camera vs motor data"],
      ["12", "False Positives", "Split", "Alert when no danger"],
      ["13", "False Negatives", "Split", "No alert when danger"],
      ["14", "The Tradeoff", "Full Image", "Sensitivity vs specificity"],
      ["15", "Your Turn", "Section Header", "Build calculator"]
    ],
    [700, 2200, 1300, 5160]
  )
);

content.push(
  new Paragraph({ children: [new PageBreak()] }),
  heading3("Module 13: ADAS Implementation (12 slides)"),
  simpleTable(
    ["Slide", "Title", "Template", "Key Content"],
    [
      ["1", "Title Slide", "Title", "Building Forward Collision Warning"],
      ["2", "Today's Goal", "Goal", "Complete FCW system"],
      ["3", "Components Review", "Text", "Detection+Distance+Speed+TTC+Alert"],
      ["4", "System Architecture", "Full Image", "Complete FCW pipeline"],
      ["5", "Integration Challenges", "Split", "Timing, synchronization"],
      ["6", "Alert Escalation", "Full Image", "Green\u2192Yellow\u2192Red"],
      ["7", "Visual Feedback", "Split", "Dashboard design"],
      ["8", "Audio Feedback", "Split", "Beep patterns"],
      ["9", "Edge Cases", "Text", "No detection, stopped, very close"],
      ["10", "Testing Protocol", "Text", "Safe FCW testing"],
      ["11", "Real FCW Comparison", "Comparison", "Our system vs commercial"],
      ["12", "Your Turn", "Section Header", "Build complete FCW"]
    ],
    [700, 2200, 1300, 5160]
  ),
  spacer(200),

  heading3("Module 14: ADAS Capstone Project (8 slides)"),
  simpleTable(
    ["Slide", "Title", "Template", "Key Content"],
    [
      ["1", "Title Slide", "Title", "ADAS Capstone Project"],
      ["2", "Your Challenge", "Goal", "Advanced ADAS feature"],
      ["3", "Project Options", "Text", "Enhanced FCW, Multi-object, Speed zones"],
      ["4", "Requirements", "Text", "ADAS authenticity requirements"],
      ["5", "Rubric", "Full Image", "Scoring (100 points)"],
      ["6", "Development Tips", "Text", "Real-world research"],
      ["7", "Presentation Format", "Text", "8-10 minute pitch structure"],
      ["8", "Final Showcase", "Section Header", "Celebration!"]
    ],
    [700, 2200, 1300, 5160]
  )
);

// ===== PART 3: IMAGE PROMPT APPENDIX =====
content.push(
  new Paragraph({ children: [new PageBreak()] }),
  heading1("PART 3: Nano Banana Image Prompt Appendix"),
  para("All image generation prompts organized by module. Each prompt includes exact dimensions and consistent style guidelines."),
  spacer(100),
  
  heading2("Prompt Structure"),
  para("All prompts follow: [Style], [Subject], [Context], [Composition], [Lighting], [Colors]. Dimensions in pixels."),
  spacer(200),

  heading2("Module 1 Image Prompts"),
  spacer(100),

  imagePromptBox("IMG_01_02", "800\u00d7400px",
    "Clean screenshot of Jupyter notebook interface showing Python code cell with successful VESC connection, output displaying 'Battery: 25.2V' in green text, dark theme IDE, the voltage output highlighted with subtle yellow glow, professional software interface aesthetic"),
  spacer(150),

  imagePromptBox("IMG_01_03a", "540\u00d7350px",
    "Screenshot of vehicle telemetry dashboard interface showing real-time gauges for speed RPM voltage and temperature, dark theme with blue (#2196F3) accent colors, modern flat design, circular gauges and line graphs, professional IoT dashboard"),
  spacer(150),

  imagePromptBox("IMG_01_03b", "540\u00d7350px",
    "Camera view with AI object detection bounding boxes overlaid, person detected with green rectangle and 0.94 confidence label, outdoor setting, realistic computer vision output, blue (#2196F3) UI elements"),
  spacer(150),

  imagePromptBox("IMG_01_03c", "540\u00d7350px",
    "Forward collision warning interface showing distance indicator, time-to-collision counter, alert level bar, automotive HUD style, warning colors yellow and orange, dark background, professional ADAS display"),
  spacer(150),

  imagePromptBox("IMG_01_04", "1760\u00d7700px",
    "Clean product photography of electric skateboard and electric scooter side by side on white background, all components visible including Raspberry Pi computer, camera module, motor controller, battery, motor, professional studio lighting, space for annotation labels, educational diagram style"),
  spacer(150),

  imagePromptBox("IMG_01_05", "800\u00d7600px",
    "Photorealistic product photo of Raspberry Pi Zero 2W single board computer on clean white surface, GPIO pins and processor visible, soft studio lighting with blue accent from left, macro photography style"),
  spacer(150),

  imagePromptBox("IMG_01_06", "800\u00d7600px",
    "Photorealistic product photo of VESC electronic speed controller board, power transistors and capacitors visible, clean white surface, professional studio lighting, technical product photography showing PCB detail"),
  spacer(150),

  imagePromptBox("IMG_01_07", "800\u00d7500px",
    "Flat design technical diagram showing CAN bus communication, Raspberry Pi icon and VESC icon connected by single line, bidirectional arrows for data flow, blue (#2196F3) and yellow (#FFCA28) colors, white background, educational illustration"),
  spacer(150),

  imagePromptBox("IMG_01_08a", "400\u00d7300px",
    "Illustration of chaotic messy wiring with many tangled cables connecting devices, spaghetti wire design, muted gray and red colors, representing complexity, flat illustration style"),
  spacer(150),

  imagePromptBox("IMG_01_08b", "400\u00d7300px",
    "Illustration of clean simple wiring with two wires connecting multiple devices in daisy chain, organized cable routing, blue and green colors, flat illustration style, minimal aesthetic"),
  spacer(150),

  imagePromptBox("IMG_01_09", "800\u00d7600px",
    "Product photo of Sony IMX500 AI camera module for Raspberry Pi, sensor board with ribbon cable, clean white surface, studio lighting with blue accent, showing lens and processing chip"),
  spacer(150),

  imagePromptBox("IMG_01_10", "1760\u00d7700px",
    "System architecture diagram showing: Battery connects to VESC, VESC bidirectional to Pi via CAN bus, Camera to Pi, Motor to VESC, data flow arrows, blue primary with yellow accents, labeled boxes, professional engineering diagram"),
  spacer(150),

  imagePromptBox("IMG_01_13", "860\u00d7650px",
    "Screenshot of Jupyter notebook interface with numbered annotations: (1) code cell, (2) run button, (3) output area, dark theme, Python code visible, blue numbered circles for callouts"),
  spacer(150),

  imagePromptBox("IMG_01_14", "1400\u00d7500px",
    "Jupyter notebook screenshot showing VESC connection code and output 'Battery: 25.2V', dark theme, syntax highlighting, the voltage value highlighted with yellow glow effect")
);

content.push(
  new Paragraph({ children: [new PageBreak()] }),
  heading2("Module 2 Image Prompts"),
  spacer(100),

  imagePromptBox("IMG_02_02", "800\u00d7450px",
    "Screenshot of get_all_telemetry() output as formatted Python dictionary, nested structure showing motor, power, temperatures sections, dark theme syntax highlighting"),
  spacer(150),

  imagePromptBox("IMG_02_04", "1600\u00d7600px",
    "Infographic table of 18 VESC data points in 4 color-coded columns: Motor (blue), Power (green), Temperature (orange), Sensors (purple), modern flat design, white background"),
  spacer(150),

  imagePromptBox("IMG_02_05", "800\u00d7500px",
    "Motor cross-section diagram showing rotation direction with +RPM and -RPM labels, curved arrows for clockwise/counterclockwise, blue for positive, orange for negative, educational style"),
  spacer(150),

  imagePromptBox("IMG_02_07", "800\u00d7500px",
    "Power flow diagram for electric vehicle: battery with voltage, VESC with current arrows, amp-hours and watt-hours displays, regenerative braking reverse arrow, blue/green colors"),
  spacer(150),

  imagePromptBox("IMG_02_08", "600\u00d7400px",
    "Vertical thermometer infographic with zones: green 0-40\u00b0C Normal, yellow 40-60\u00b0C Warm, orange 60-80\u00b0C Warning, red 80\u00b0C+ Danger, temperature scale, safety infographic style"),
  spacer(150),

  imagePromptBox("IMG_02_11", "800\u00d7400px",
    "Side-by-side comparison: left shows stationary motor with zeros (RPM:0, Current:0), right shows spinning motor with motion blur and values (RPM:2500, Current:3.2A), flat design"),
  spacer(200),

  heading2("Module 6 Image Prompts"),
  spacer(100),

  imagePromptBox("IMG_06_04", "1600\u00d7600px",
    "Split comparison: left 'Traditional Code' with complex tangled flowchart in gray/red, right 'AI Learning' with clean neural network diagram learning from images in blue/green, educational infographic"),
  spacer(150),

  imagePromptBox("IMG_06_06", "1600\u00d7500px",
    "AI vision pipeline: Camera icon \u2192 Pixel grid \u2192 Neural network layers \u2192 'Dog 94%' label output, arrows connecting stages, blue accent, white background, technical illustration"),
  spacer(150),

  imagePromptBox("IMG_06_11", "1400\u00d7400px",
    "Confidence score scale 0.0 to 1.0: red zone 0-0.5 'Low-Ignore', yellow 0.5-0.8 'Medium-Verify', green 0.8-1.0 'High-Trust', gradient bar, tick marks, modern infographic"),
  spacer(150),

  imagePromptBox("IMG_06_14", "800\u00d7600px",
    "Bounding box explanation diagram: image with rectangle, labeled corners showing x,y coordinates, width/height arrows, center point marked, coordinate overlay, educational style"),
  spacer(200),

  heading2("Module 7 Image Prompts"),
  spacer(100),

  imagePromptBox("IMG_07_03", "1760\u00d7700px",
    "Grid of 80 simple icons for COCO dataset objects organized by category: people, vehicles, animals, household, electronics, food, sports, consistent blue (#2196F3) color, white background, labeled rows"),
  spacer(150),

  imagePromptBox("IMG_07_06", "1600\u00d7500px",
    "Object detection pipeline: Camera \u2192 IMX500 AI chip \u2192 Results box (label,confidence,bbox) \u2192 Display with bounding boxes, '30ms' timing indicator, flat design, blue accents"),
  spacer(150),

  imagePromptBox("IMG_07_08", "1600\u00d7600px",
    "4-panel comparison showing detection factors: good lighting/clear detection, poor lighting/failed, close distance/high confidence, far distance/low confidence, same coffee mug in each, educational comparison")
);

content.push(
  new Paragraph({ children: [new PageBreak()] }),
  heading2("ADAS Module Image Prompts (11-14)"),
  spacer(100),

  imagePromptBox("IMG_11_05", "1760\u00d7800px",
    "ADAS features infographic grid with 12 icons and labels: FCW (car+warning), AEB (brake), LDW (lanes), ACC (speedometer), BSD (mirror), Parking (sensors), TSR (stop sign), Pedestrian (person), Cross Traffic (intersection), Night Vision (moon), Driver Monitor (eye), 360 Camera, blue color scheme, automotive style"),
  spacer(150),

  imagePromptBox("IMG_11_11", "1600\u00d7700px",
    "SAE autonomy levels stepped diagram: Level 0-5 ascending, each with description and human/computer control ratio icon, gradient from red (human) to blue (computer), automotive infographic"),
  spacer(150),

  imagePromptBox("IMG_11_15", "1600\u00d7600px",
    "3-column sensor comparison: Camera (strengths: color/detail/signs, weaknesses: dark/weather), Radar (all weather/speed, no color/limited detail), Lidar (3D mapping/precision, expensive/weather), color-coded columns"),
  spacer(150),

  imagePromptBox("IMG_12_07", "1400\u00d7500px",
    "TTC formula diagram: car icon left, person icon right, distance 'd' labeled between, closing speed 'v' arrow, 'TTC = d/v' formula prominent, example '10m / 5m/s = 2s' below, educational math diagram"),
  spacer(150),

  imagePromptBox("IMG_12_09", "1400\u00d7400px",
    "TTC alert levels timeline: green 'TTC>3s Safe' right, yellow '1-3s Warning' middle, red 'TTC<1s Critical' left, car icons getting closer, alert icons for each zone, safety infographic"),
  spacer(150),

  imagePromptBox("IMG_13_04", "1760\u00d7700px",
    "FCW system architecture: AI Camera \u2192 Detection \u2192 Distance Est \u2192 FCW Logic central box, VESC \u2192 Speed Calc \u2192 also to FCW Logic, outputs to Alert System (buzzer+display icons), TTC in center, data flow arrows, blue primary with orange alerts"),
  spacer(200),

  heading2("Quick Reference: All Image Dimensions"),
  simpleTable(
    ["Reference", "Dimensions", "Module", "Description"],
    [
      ["IMG_01_02", "800\u00d7400px", "1", "Goal slide voltage reading"],
      ["IMG_01_03a/b/c", "540\u00d7350px", "1", "Project preview grid"],
      ["IMG_01_04", "1760\u00d7700px", "1", "Complete PEV system"],
      ["IMG_01_05/06/09", "800\u00d7600px", "1", "Component product photos"],
      ["IMG_01_07", "800\u00d7500px", "1", "CAN bus diagram"],
      ["IMG_01_08a/b", "400\u00d7300px", "1", "Wiring comparison"],
      ["IMG_01_10", "1760\u00d7700px", "1", "System architecture"],
      ["IMG_01_13", "860\u00d7650px", "1", "Jupyter interface"],
      ["IMG_01_14", "1400\u00d7500px", "1", "Connection code"],
      ["IMG_02_*", "600-1600px", "2", "Telemetry visuals"],
      ["IMG_06_*", "800-1600px", "6", "AI concept diagrams"],
      ["IMG_07_*", "1600-1760px", "7", "Detection visuals"],
      ["IMG_11-13_*", "1400-1760px", "11-13", "ADAS diagrams"]
    ],
    [1800, 1500, 1000, 5060]
  )
);

// ===== FINAL SECTION =====
content.push(
  new Paragraph({ children: [new PageBreak()] }),
  heading1("Quick Reference Summary"),
  spacer(100),
  
  heading2("Color Codes"),
  simpleTable(
    ["Name", "Hex", "RGB", "Use"],
    [
      ["Lectec Blue", "#2196F3", "33,150,243", "Primary, headers"],
      ["Lectec Yellow", "#FFCA28", "255,202,40", "Accents, CTAs"],
      ["Lectec Black", "#1A1A1A", "26,26,26", "Body text"],
      ["Dark Blue", "#1976D2", "25,118,210", "Hover, depth"],
      ["Light Blue", "#E3F2FD", "227,242,253", "Backgrounds"],
      ["Success", "#4CAF50", "76,175,80", "Positive"],
      ["Warning", "#FF9800", "255,152,0", "Caution"],
      ["Danger", "#F44336", "244,67,54", "Error"]
    ],
    [2000, 1500, 2000, 3860]
  ),
  spacer(200),
  
  heading2("Typography"),
  simpleTable(
    ["Element", "Font", "Size", "Weight"],
    [
      ["Slide Title", "Montserrat/Arial", "44pt", "Bold"],
      ["Section Header", "Montserrat/Arial", "36pt", "Bold"],
      ["Body Text", "Open Sans/Arial", "24pt", "Regular"],
      ["Bullets", "Open Sans/Arial", "22pt", "Regular"],
      ["Code", "Fira Code/Consolas", "20pt", "Regular"],
      ["Footer", "Open Sans/Arial", "14pt", "Regular"]
    ],
    [2500, 2500, 1500, 2860]
  ),
  spacer(200),
  
  heading2("Slide Dimensions"),
  para("Canvas: 1920\u00d71080px (16:9) | Margins: 80px all sides | Content area: 1760\u00d7800px"),
  spacer(200),
  
  heading2("Templates"),
  para("1. Title Slide | 2. Goal/Demo | 3. Text Only | 4. Split (Text+Image) | 5. Full Image | 6. Comparison | 7. Section Header"),
  spacer(400),
  
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "\u2014 End of Document \u2014", size: 20, font: "Arial", color: colors.gray600, italics: true })]
  }),
  spacer(100),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "Lectec PEV Curriculum \u2022 PowerPoint Design Guide v1.0", size: 18, font: "Arial", color: colors.gray600 })]
  })
);

// Create document
const doc = new Document({
  numbering: { config: numberingConfig },
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 40, bold: true, font: "Arial", color: colors.lectecBlue },
        paragraph: { spacing: { before: 400, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial", color: colors.lectecDarkBlue },
        paragraph: { spacing: { before: 350, after: 150 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial", color: colors.lectecBlack },
        paragraph: { spacing: { before: 280, after: 120 }, outlineLevel: 2 } }
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
          children: [new TextRun({ text: "Lectec PowerPoint Design Guide", italics: true, size: 18, font: "Arial", color: colors.gray600 })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Page ", size: 18, font: "Arial", color: colors.gray600 }),
            new TextRun({ children: [PageNumber.CURRENT], size: 18, font: "Arial", color: colors.gray600 }),
            new TextRun({ text: " of ", size: 18, font: "Arial", color: colors.gray600 }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 18, font: "Arial", color: colors.gray600 })
          ]
        })]
      })
    },
    children: content
  }]
});

// Generate
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/sessions/beautiful-brave-hopper/mnt/RaspberryPi-CAN/Lectec_PowerPoint_Design_Guide.docx", buffer);
  console.log("Document created successfully: Lectec_PowerPoint_Design_Guide.docx");
}).catch(err => {
  console.error("Error:", err);
});
