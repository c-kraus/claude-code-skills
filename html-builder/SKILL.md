---
name: html-builder
description: Create standalone HTML/JS widgets for academic visualization, embedded via IFRAME in lecture notes. Use when the user requests interactive visualizations, educational widgets, demonstrations, simulations, or any standalone HTML-based academic content. Trigger phrases include "create an HTML widget", "build an interactive visualization", "make an IFRAME-embeddable demo", "HTML for lecture notes", or any request for educational web-based interactivity.
---

# HTML Builder - Academic Visualization Widgets
Create simple, focused HTML/JS widgets that complement and clarify lecture content through visualization and interaction.
Philosophy
Widgets are supplements, not replacements:

Visualize ONE concept clearly
Keep it simple and focused
No author credits, metadata, or unnecessary text
The surrounding lecture text provides context

Design System (THWS Brand)
Colors:

Primary: #ff6a00 (THWS Orange) - buttons, active states, highlights
Text: #333333 (Dark Grey)
Background: #ffffff (White)

Typography:
cssfont-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
File Structure
Single HTML file with embedded CSS and JavaScript:
html<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Short Widget Title]</title>
    <style>
        /* CSS here */
    </style>
</head>
<body>
    <!-- Content here -->
    <script>
        // JavaScript here
    </script>
</body>
</html>
Layout Requirements
Keep It Compact

Target height: 400-500px (fits well in IFRAME without scrolling)
Width: Responsive, but optimize for 700-800px

Minimal Styling
cssbody {
    margin: 0;
    padding: 20px;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    box-sizing: border-box;
}

.widget-container {
    max-width: 800px;
    margin: 0 auto;
}

button {
    background: #ff6a00;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 600;
}

button:hover {
    opacity: 0.9;
}
Content Guidelines
What to Include

✅ Interactive visualization
✅ Minimal controls (sliders, buttons)
✅ Live feedback/results
✅ Brief labels (1-3 words)

What to Exclude

❌ Long explanatory text (that's in the lecture)
❌ Author credits, copyright notices
❌ "About this widget" sections
❌ Redundant titles (the lecture heading covers it)
❌ Instructions paragraphs (if controls are self-explanatory)

Text Language

Detect from context (German or English)
Keep ALL UI text in that language
Use minimal text - let interaction speak

Widget Patterns
Pattern 1: Parameter Explorer
Purpose: Show how changing parameters affects outcomes
html<!-- Slider + Live Chart -->
<div>
    <label>Zinssatz: <span id="rate">5</span>%</label>
    <input type="range" min="0" max="20" value="5" id="rateSlider">
    <canvas id="chart"></canvas>
</div>
Pattern 2: Process Visualization
Purpose: Show steps in a sequence
html<!-- Step-by-step with navigation -->
<div id="step-display"></div>
<button onclick="prevStep()">← Zurück</button>
<button onclick="nextStep()">Weiter →</button>
Pattern 3: Interactive Diagram
Purpose: Explore relationships
html<!-- Clickable elements that highlight connections -->
<svg id="diagram"></svg>
<div id="info"></div>
Technical Requirements
JavaScript

Use vanilla JS (no frameworks)
CDN libraries only if absolutely necessary
Keep code simple and readable

Canvas/SVG

Use Canvas for charts and animations
Use SVG for diagrams and networks
No external chart libraries unless essential

Responsiveness

Works in IFRAME context
No fixed pixel widths (use %, max-width)
Touch-friendly controls (mobile)

Output Format (CRITICAL)
No Conversation

Output ONLY the HTML code
NO explanations before/after
NO "Here's the widget" or similar phrases

Single Code Block
```html
<!DOCTYPE html>
...entire widget...
</html>
```
Do NOT split the code. One continuous block from <!DOCTYPE> to </html>.
Example: Simple Widget
html<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ROI Berechnung</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: 'Inter', sans-serif;
        }
        .container {
            max-width: 700px;
            margin: 0 auto;
        }
        input[type="range"] {
            width: 100%;
            margin: 10px 0;
        }
        #result {
            font-size: 2rem;
            color: #ff6a00;
            font-weight: bold;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <label>Investition: <span id="inv">10000</span> €</label>
        <input type="range" id="invSlider" min="1000" max="50000" value="10000" step="1000">
        
        <label>Gewinn: <span id="profit">2000</span> €</label>
        <input type="range" id="profitSlider" min="0" max="10000" value="2000" step="100">
        
        <div id="result">ROI: 20%</div>
    </div>
    
    <script>
        const invSlider = document.getElementById('invSlider');
        const profitSlider = document.getElementById('profitSlider');
        const invDisplay = document.getElementById('inv');
        const profitDisplay = document.getElementById('profit');
        const result = document.getElementById('result');
        
        function calculate() {
            const inv = parseInt(invSlider.value);
            const profit = parseInt(profitSlider.value);
            const roi = ((profit / inv) * 100).toFixed(1);
            
            invDisplay.textContent = inv;
            profitDisplay.textContent = profit;
            result.textContent = `ROI: ${roi}%`;
        }
        
        invSlider.addEventListener('input', calculate);
        profitSlider.addEventListener('input', calculate);
    </script>
</body>
</html>
Quality Checklist
Before delivering a widget, verify:

✅ Compact (fits ~500px height)
✅ No author/metadata sections
✅ Minimal text (UI labels only)
✅ One clear purpose
✅ THWS orange for primary actions
✅ Single HTML file
✅ Works standalone in IFRAME

Remember
Simplicity is key. The lecture text does the teaching - the widget just makes one concept visual and interactive.