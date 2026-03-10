---
name: widget-pipeline
description: Automated end-to-end workflow for widget integration in Quarto lectures. Analyzes .qmd files, creates top 3 recommended widgets, saves them to /widgets directory, and integrates iframe codes into the source file. Orchestrates widget-analyzer, html-builder, and file editing in one streamlined process. Use when the user requests complete widget automation like "automatische Widget-Integration", "kompletter Widget-Workflow", or "analysiere und baue Widgets ein".
---

# Widget Pipeline Skill

## Purpose
Fully automated workflow that takes a Quarto .qmd file and:
1. Analyzes it for widget opportunities (widget-analyzer)
2. Creates the top 3 recommended widgets (html-builder)
3. Saves widgets to organized directory structure
4. Integrates iframe codes into the .qmd file
5. Provides summary report

## Workflow Steps

### Step 1: Analysis Phase
Use **widget-analyzer** skill to:
- Read the complete .qmd file
- Identify widget opportunities
- Generate prioritized specifications
- Extract top 3 high-priority recommendations

**Internal processing only** - Don't show full analysis to user yet.

### Step 2: Widget Creation Phase
For each of the top 3 widget specifications:
- Use **html-builder** skill to create the widget
- Follow exact specifications from analyzer
- Ensure THWS branding consistency
- Create production-ready HTML files

### Step 3: File Organization Phase
**Directory Structure:**
```
[qmd-directory]/
└── widgets/
    └── kapitel-XX/
        ├── widget-[name-1].html
        ├── widget-[name-2].html
        └── widget-[name-3].html
```

**Rules:**
- Extract chapter number from .qmd filename (e.g., `kap-03-...qmd` → `kapitel-03`)
- Use descriptive, lowercase, dash-separated names
- Save widgets to `widgets/kapitel-XX/` **relative to the .qmd file's directory**
- Verify each file is saved successfully

### Step 4: Integration Phase
**For each widget:**
1. Locate the specified insertion point in .qmd
2. Add contextual intro text (1-2 sentences in document language)
3. Insert wrapped in the `.widget` Div — this is mandatory for PDF compatibility:
```markdown
::: {.widget}
<iframe src="widgets/kapitel-XX/widget-[name].html"
        width="100%" height="[appropriate-height]px" frameborder="0"
        title="[Accessible title in document language]">
</iframe>
:::
```
4. Add blank line after the closing `:::` for readability
5. Use `str_replace` to make precise, surgical edits

**Why `.widget`?** The quarto-lecture skill uses Lua filters that turn `.widget` divs into contained boxes in PDF output. Bare `<iframe>` tags in .qmd files break PDF rendering.

**Integration Strategy:**
- Identify unique text anchors near insertion points
- Use str_replace for each widget insertion separately
- Preserve all existing content and formatting
- Maintain document flow and structure

### Step 5: Verification & Summary
Create a summary report for the user:

```markdown
# Widget Pipeline: Abgeschlossen

## Verarbeitete Datei
- **Quelldatei:** [filename.qmd]
- **Kapitel:** [chapter number/title]
- **Sprache:** [Deutsch/English]

## Erstellte Widgets
1. **[Widget 1 Name]**
   - Datei: `widgets/kapitel-XX/widget-name-1.html`
   - Kategorie: [Prozesse/Zusammenhänge/Parametervariationen]
   - Eingefügt: [nach Abschnitt/vor Überschrift]

2. **[Widget 2 Name]**
   - Datei: `widgets/kapitel-XX/widget-name-2.html`
   - Kategorie: [...]
   - Eingefügt: [...]

3. **[Widget 3 Name]**
   - Datei: `widgets/kapitel-XX/widget-name-3.html`
   - Kategorie: [...]
   - Eingefügt: [...]

## Dateipfade
- Widgets: `[qmd-directory]/widgets/kapitel-XX/`
- Aktualisierte .qmd: [filepath]

## Nächste Schritte
✅ Widgets wurden erstellt und integriert
→ Prüfen Sie die .qmd Datei und Widget-Funktionalität
→ Kopieren Sie die Widgets in Ihr Projekt-Repository
```

## Error Handling

### If widget-analyzer finds <3 high-priority opportunities:
- Use all available high-priority widgets
- If <3 total: supplement with medium-priority
- Inform user about adjusted widget count

### If widget creation fails:
- Skip that widget
- Continue with remaining widgets
- Note failure in summary report

### If integration fails:
- Provide widget files anyway
- Show intended insertion points
- Let user integrate manually

## Output Destinations

**Always use these paths:**
- Widgets: `[qmd-directory]/widgets/kapitel-XX/*.html` (relative to the .qmd file's location)
- Modified .qmd: Keep in original location (use str_replace)

**Then use `present_files` if available:**
```
present_files([
  "[qmd-directory]/widgets/kapitel-XX/widget-1.html",
  "[qmd-directory]/widgets/kapitel-XX/widget-2.html",
  "[qmd-directory]/widgets/kapitel-XX/widget-3.html",
  "[original-qmd-path]"
])
```

## Quality Assurance

Before presenting results, verify:
- ✅ All 3 widget HTML files exist and are valid
- ✅ Each widget follows THWS design system
- ✅ Iframe codes are correctly inserted in .qmd
- ✅ Document language is consistent throughout
- ✅ No content was accidentally removed from .qmd
- ✅ File paths in iframes match actual file locations

## Orchestration Logic

```
INPUT: .qmd filepath

↓
STEP 1: widget-analyzer(.qmd)
↓
EXTRACT: Top 3 specifications
↓
STEP 2: FOR EACH spec:
          html-builder(spec) → .html file
          SAVE to /widgets/kapitel-XX/
↓
STEP 3: FOR EACH widget:
          CONSTRUCT iframe code
          LOCATE insertion point in .qmd
          str_replace to integrate
↓
STEP 4: GENERATE summary report
↓
OUTPUT: Summary + present_files()
```

## Usage Examples

### Example 1: Standard Usage
```
User: "Widget-Pipeline für kapitel-03-bilanzanalyse.qmd"

Claude:
1. [Internally runs widget-analyzer]
2. [Creates 3 widgets via html-builder]
3. [Saves to widgets/kapitel-03/]
4. [Integrates iframes into .qmd]
5. [Shows summary report]
6. [Presents all files]
```

### Example 2: Explicit Request
```
User: "Analysiere diese Datei und baue automatisch die Top 3 Widgets ein"

Claude: [Runs complete pipeline as above]
```

### Example 3: With Uploaded File
```
User: [uploads .qmd file] "Automatische Widget-Integration"

Claude: [Detects file, runs pipeline]
```

## Integration with Existing Skills

**Dependencies:**
- Requires: widget-analyzer, html-builder
- Outputs compatible with: quarto-lecture (for further editing)

**Skill Coordination:**
- widget-analyzer: Used in silent mode, output not shown to user
- html-builder: Used for actual widget creation
- str_replace: Direct tool use for .qmd integration

## Notes for Claude

When executing this pipeline:

1. **Be efficient:** Don't show intermediate analysis steps to user
2. **Be surgical:** Use precise str_replace operations, never rewrite entire files
3. **Be thorough:** Verify each step before proceeding
4. **Be informative:** Final summary should be clear and actionable
5. **Detect language:** Maintain German/English consistency from source .qmd
6. **Prioritize quality:** Better to deliver 2 excellent widgets than 3 mediocre ones

## Trigger Phrases

Use this skill when user requests:
- "Widget-Pipeline für diese Datei"
- "Automatische Widget-Integration"
- "Analysiere und baue Top 3 Widgets ein"
- "Kompletter Widget-Workflow"
- "End-to-end Widget-Erstellung"
- "Widgets automatisch erstellen und einbinden"

## Performance Target

Complete pipeline execution should:
- Analyze .qmd in <30 seconds
- Create 3 widgets in <90 seconds total
- Integrate iframes in <20 seconds
- **Total runtime target: <3 minutes**