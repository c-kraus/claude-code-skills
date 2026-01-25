# HTML-Builder Skill

## Purpose
Create standalone HTML/JS widgets for academic visualization, embedded via IFRAME in lecture notes. Generates interactive visualizations, educational widgets, demonstrations, simulations, or any standalone HTML-based academic content with THWS branding.

## When to Use
Trigger when the user requests:
- "create an HTML widget"
- "build an interactive visualization"
- "make an IFRAME-embeddable demo"
- "HTML for lecture notes"
- Any request for educational web-based interactivity
- Interactive demonstrations for teaching
- Visualizations for German-speaking academic contexts

## THWS Brand Guidelines

### Colors
```css
/* Primary THWS Colors */
--thws-blue: #005b9c;
--thws-lightblue: #0088cc;
--thws-grey: #6e6e6e;
--thws-lightgrey: #d9d9d9;
--thws-white: #ffffff;
--thws-black: #2d2d2d;

/* Accent Colors */
--thws-green: #7ab51d;
--thws-orange: #f39200;
--thws-red: #e30613;
```

### Typography
- **Headings**: Arial, sans-serif, bold
- **Body text**: Arial, sans-serif, regular
- **Code/Mono**: 'Courier New', monospace

### Logo Usage
- THWS logo should appear subtly (top-right or bottom-right corner)
- Logo URL: Use text "THWS" in brand blue if image not available
- Always include "Technische Hochschule Würzburg-Schweinfurt" in footer

## Technical Requirements

### Structure
1. **Standalone HTML file** - everything in one file
2. **No external dependencies** where possible
3. **Responsive design** - works on mobile and desktop
4. **IFRAME-safe** - designed to be embedded
5. **German language** by default (unless specified otherwise)

### Template Structure
```html
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Widget Title]</title>
    <style>
        /* THWS Brand Styles */
        :root {
            --thws-blue: #005b9c;
            --thws-lightblue: #0088cc;
            /* ... other colors ... */
        }
        
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #ffffff;
            color: var(--thws-black);
        }
        
        .thws-header {
            border-bottom: 3px solid var(--thws-blue);
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        
        .thws-footer {
            margin-top: 30px;
            padding-top: 10px;
            border-top: 1px solid var(--thws-lightgrey);
            font-size: 0.8em;
            color: var(--thws-grey);
            text-align: center;
        }
        
        /* Widget-specific styles here */
    </style>
</head>
<body>
    <div class="thws-header">
        <h1>[Widget Title]</h1>
    </div>
    
    <div class="widget-content">
        <!-- Interactive content here -->
    </div>
    
    <div class="thws-footer">
        <p>Technische Hochschule Würzburg-Schweinfurt | Prof. Dr. Christian Kraus</p>
    </div>
    
    <script>
        // Widget functionality here
    </script>
</body>
</html>
```

### Best Practices
1. **Interactivity**: Use vanilla JavaScript (no frameworks needed for small widgets)
2. **Accessibility**: Include ARIA labels, keyboard navigation
3. **Performance**: Optimize for quick loading in iframes
4. **Comments**: German comments in code for student reference
5. **Educational value**: Code should be readable and serve as learning example

## Common Widget Types

### 1. Data Visualization
- Charts and graphs (use Canvas API or SVG)
- Interactive timelines
- Network diagrams
- Statistical demonstrations

### 2. Conceptual Demonstrations
- Algorithm visualizations
- Process flows
- System models
- Interactive diagrams

### 3. Calculators & Tools
- Financial calculators
- Unit converters
- Formula demonstrations
- Interactive worksheets

### 4. Simulations
- Economic models
- Physical systems
- Business scenarios
- Game theory demonstrations

## External Libraries (if needed)
When vanilla JS is insufficient, prefer CDN-hosted libraries:
- **Chart.js** for charts: `https://cdn.jsdelivr.net/npm/chart.js`
- **D3.js** for complex visualizations: `https://d3js.org/d3.v7.min.js`
- **Plotly** for scientific plots: `https://cdn.plot.ly/plotly-latest.min.js`
- **MathJax** for formulas: `https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js`

## Workflow

### Step 1: Understand Requirements
- What concept/data should be visualized?
- What interaction is needed?
- Target audience level?
- Language (German default)?

### Step 2: Design Approach
- Sketch the layout
- Identify data structures
- Plan interactivity
- Choose technologies

### Step 3: Implement
- Create HTML structure with THWS branding
- Add interactive JavaScript
- Style with CSS following brand guidelines
- Test in browser

### Step 4: Deliver
- Save as `.html` file
- Provide embedding instructions
- Include usage documentation if complex

## Output Format

Always save the widget to `/mnt/user-data/outputs/[descriptive-name].html`

After creating the widget, provide:
1. **File download link**
2. **Brief usage instructions**
3. **Embedding code** for iframe:
```html
<iframe src="[widget-name].html" width="100%" height="600px" frameborder="0"></iframe>
```

## Examples of Past Widgets

### Example 1: Interactive Timeline
- Displays historical events
- Click events for details
- Smooth scrolling
- German annotations

### Example 2: Financial Calculator
- Compound interest visualization
- Input sliders for parameters
- Real-time graph updates
- Explanatory tooltips

### Example 3: Process Flowchart
- Interactive node selection
- Animated transitions
- Detailed explanations per step
- Export to PNG option

## Quality Checklist
- [ ] THWS branding applied correctly
- [ ] Responsive design (mobile + desktop)
- [ ] All text in German (unless specified)
- [ ] Code is commented and educational
- [ ] No console errors
- [ ] Accessible (keyboard navigation, ARIA)
- [ ] Loads quickly in iframe
- [ ] Footer includes THWS attribution

## Notes
- Widgets should be **pedagogically valuable** - code quality matters for student reference
- Keep file size reasonable (< 500KB ideally)
- Test in multiple browsers if using advanced features
- Consider providing a "How it works" section in the widget itself
- Always include source code comments in German for educational transparency

## Error Handling
- Graceful degradation if browser doesn't support features
- Clear error messages in German
- Fallback for missing data or user errors

## Version Control
- Include version number and date in footer
- Comment major changes in code
- Keep changelog if widget is updated frequently
