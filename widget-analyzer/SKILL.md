---
name: widget-analyzer
description: Analyze Quarto lecture chapters (.qmd files) to identify didactically valuable opportunities for interactive HTML widgets. Generate concrete widget specifications that can be implemented using the html-builder skill and integrated via iframe. Use when the user requests widget analysis, asks to identify visualization opportunities, or wants to enhance lecture content with interactive elements. Trigger phrases include "Analysiere für Widget-Potenziale", "identify widget opportunities", "wo könnte ich interaktive Elemente einbauen".
---




# Widget Analyzer Skill

## Purpose
Analyze Quarto lecture chapters (.qmd files) to identify didactically valuable opportunities for interactive HTML widgets. Generate concrete widget specifications that can be implemented using the html-builder skill and integrated via iframe.

## Context
- Target audience: Bachelor-level students in business and engineering at THWS
- Content follows "Trinity of Depth" pedagogy (theory, norms, practice)
- Language: German OR English (detect from .qmd content, match in all outputs)
- THWS branding requirements apply
- Widgets should enhance understanding, not just decoration

## Widget Categories

**Important:** Flip-cards, progressive disclosure, and quiz/self-tests are already natively available through the quarto-lecture skill. Do NOT propose these as HTML widgets.

### 1. Prozesse/Abläufe (Processes/Workflows)
**Purpose:** Visualize sequential steps, temporal progressions, or procedural knowledge
**Examples:** 
- Accounting transaction flows (Buchungssätze)
- Business process steps
- Decision trees
- Algorithm execution

**Widget Types:**
- Step-by-step animations with navigation
- Timeline visualizations
- Interactive flowcharts

**Interaction Patterns:**
- Forward/backward navigation
- Step highlighting

### 2. Zusammenhänge/Abhängigkeiten (Relationships/Dependencies)
**Purpose:** Show interconnections, causal relationships, or systemic effects
**Examples:**
- Balance sheet relationships (Aktiva/Passiva)
- Profit vs. cashflow dependencies
- Market equilibrium dynamics
- System feedback loops

**Widget Types:**
- Interactive network diagrams
- Sankey flow diagrams
- Dynamic connection visualizations

**Interaction Patterns:**
- Hover for details
- Click to expand/collapse
- Highlight paths

### 3. Parametervariationen (Parameter Variations)
**Purpose:** Demonstrate how changes in variables affect outcomes
**Examples:**
- ROI calculations with varying interest rates
- Break-even analysis with cost variations
- NPV sensitivity analysis
- Formula demonstrations

**Widget Types:**
- Slider controls + live charts
- What-if scenario calculators
- Interactive formulas

**Interaction Patterns:**
- Adjust sliders/inputs
- Real-time result updates
- Compare scenarios

## Text Pattern Recognition

### Indicators for Prozesse/Abläufe
Look for these patterns in the text:
- Sequential markers: "Schritt 1, 2, 3...", "zunächst... dann... schließlich..."
- Process language: "Der Ablauf ist...", "Das Verfahren umfasst...", "Die Reihenfolge..."
- Temporal connectors: "anschließend", "danach", "im nächsten Schritt"
- Instructional verbs: "wird durchgeführt", "erfolgt", "wird vorgenommen"

### Indicators for Zusammenhänge/Abhängigkeiten
Look for these patterns:
- Causal language: "beeinflusst", "wirkt sich aus auf", "führt zu", "bewirkt"
- Relational terms: "steht in Beziehung zu", "hängt ab von", "korreliert mit"
- Conditional statements: "Je mehr X, desto...", "wenn... dann...", "bei steigendem..."
- System descriptions: "das System besteht aus", "die Komponenten interagieren"

### Indicators for Parametervariationen
Look for these patterns:
- Variable mentions: "bei unterschiedlichen Werten", "variiert zwischen... und..."
- Hypothetical scenarios: "Angenommen der Zinssatz beträgt...", "Bei einem Wert von..."
- Formula presentations: mathematical expressions with variables
- Sensitivity language: "reagiert empfindlich auf", "ist abhängig von"
- Range specifications: "zwischen X und Y", "von... bis..."

## Analysis Workflow

### Phase 1: Content Scanning
1. Read the complete .qmd chapter
2. Identify section structure and learning objectives
3. Map content to Trinity of Depth (theory/norms/practice)
4. Note existing visual elements (tables, figures)

### Phase 2: Pattern Detection
For each content section:
1. Scan for text patterns matching the three widget categories
2. Assess complexity: Is the concept difficult to grasp from text alone?
3. Evaluate pedagogical value: Would visualization significantly enhance understanding?
4. Consider cognitive load: Does it simplify or complicate?

### Phase 3: Widget Specification
For each identified opportunity, create:

```markdown
## Widget [N]: [Descriptive Title]

**Location:** [Section/paragraph identifier from .qmd]
**Category:** [Prozesse | Zusammenhänge | Parametervariationen]
**Priority:** [High | Medium | Low]

**Didactic Goal:**
[1-2 sentences: What should students understand through this widget?]

**Widget Concept:**
[2-3 sentences: What does the widget show and how does it work?]

**Key Features:**
- Main interaction: [e.g., "Slider adjusts interest rate, chart updates"]
- Data shown: [e.g., "ROI values from 0-20%"]
- Visual type: [e.g., "Line chart" or "Network diagram"]

**Integration:**
- Filename: `widgets/kapitel-XX/widget-[name].html`
- Placement: [Before/after which heading]
- Intro text: "[1-2 sentences introducing the widget in the document's language]"

**iframe:**
```html
<iframe src="widgets/kapitel-XX/widget-[name].html" 
        width="100%" height="[height]px" frameborder="0"
        title="[Accessible title in document language]">
</iframe>
```
```

### Phase 4: Prioritization
Rate each widget proposal:
- **High Priority:** Core concept, high didactic value, clear interaction pattern
- **Medium Priority:** Helpful but not essential, or technically complex
- **Low Priority:** Nice-to-have, marginal improvement over text

## Output Format

Generate a structured analysis report:

```markdown
# Widget-Analyse: [Chapter Title]

## Zusammenfassung
- Kapitel: [Title and number]
- Analysierte Abschnitte: [count]
- Identifizierte Widget-Potenziale: [count]
- Empfohlene Umsetzungen: [High priority count]

## Widget-Vorschläge

[List all widget proposals in order of priority]

## Implementierungs-Roadmap
1. [High priority widget 1]
2. [High priority widget 2]
...

## Technische Hinweise
[Any cross-cutting technical considerations]
```

## Integration with Other Skills

### With html-builder Skill
The widget-analyzer produces specifications that are passed to html-builder for implementation:
1. Widget-analyzer identifies opportunities and creates specs
2. User reviews and approves specs
3. html-builder implements the approved widgets with THWS branding
4. Widgets are saved to appropriate directory structure

### With quarto-lecture Skill
After widgets are built:
1. Add iframe code at specified locations in .qmd
2. Add context text in the document's language (German or English)
3. Ensure narrative flow is maintained

## Quality Criteria

A good widget proposal should:
- ✅ Address a genuine comprehension challenge
- ✅ Add interactivity that text/static images cannot provide
- ✅ Be technically feasible within HTML/CSS/JavaScript
- ✅ Fit naturally into the narrative flow
- ✅ Respect cognitive load principles (don't overwhelm)
- ✅ Work across devices (responsive design)
- ✅ Include accessible fallback content

## Anti-Patterns to Avoid

- ❌ Widgets for decoration without pedagogical value
- ❌ Over-complicated interactions that confuse rather than clarify
- ❌ Redundant widgets that merely repeat text content
- ❌ Breaking narrative flow with jarring interruptions
- ❌ Technology showcase without learning objective
- ❌ Widgets that work only on specific browsers/devices

## Example Use Cases

### Economics: Visualizing Market Equilibrium
**Pattern detected:** "Je höher der Preis, desto geringer die Nachfrage" + "Das Gleichgewicht entsteht bei..."
**Widget category:** Parametervariationen
**Proposal:** Interactive supply-demand slider showing equilibrium point adjustment

### Accounting: Buchungssatz Flow
**Pattern detected:** "Zunächst wird die Geschäftsvorfall analysiert... dann erfolgt die Kontenzuordnung..."
**Widget category:** Prozesse/Abläufe
**Proposal:** Step-by-step animation of transaction analysis to journal entry

### Mechatronics: Sensor Network Dependencies
**Pattern detected:** "Die Sensoren beeinflussen sich gegenseitig... das System reagiert auf..."
**Widget category:** Zusammenhänge/Abhängigkeiten
**Proposal:** Interactive network diagram showing sensor interactions

## Notes for Claude

When using this skill:
1. **Detect document language** from the .qmd content (German or English)
2. Provide ALL outputs (specs, intro texts, iframe titles) in the detected language
3. Always read the complete chapter before making recommendations
4. Consider the target audience's prior knowledge
5. Balance interactivity with simplicity
6. Prioritize high-impact widgets over quantity
7. Provide complete specifications ready for html-builder implementation
8. Think about both web (interactive) and PDF (static) outputs

## Trigger Phrases

Use this skill when the user requests:
- "Analysiere dieses Kapitel für Widget-Potenziale"
- "Wo könnte ich interaktive Elemente einbauen"
- "Welche Konzepte brauchen Visualisierung"
- "Identifiziere didaktisch sinnvolle Widgets"
- "Schlage HTML-Widgets für diese Vorlesung vor"
