---
name: qmd-corrector
description: "Audit and fix existing Quarto lecture files (.qmd) for YAML and Div syntax errors. Use this skill whenever the user wants to check, validate, lint, or correct a .qmd file — even if they just say 'schau mal drüber', 'prüf das mal', 'fix the formatting', or 'something looks broken'. Also trigger when the user pastes a .qmd path and asks if it's correct, or when quarto render fails. The skill reads the file, systematically checks every element type, fixes all violations in-place, saves the corrected file, and outputs a structured Quality Report showing exactly what was wrong and what was fixed."
---

# QMD Corrector

A surgical audit-and-fix skill for Quarto lecture files. The goal is zero silent failures: broken Div syntax won't throw an error in the editor, but it will silently break the Moodle Lua filter or the PDF renderer. This skill catches and fixes those problems before they reach students.

## What This Skill Does

1. **Read** the target .qmd file
2. **Audit** every element type against canonical rules (see checklists below)
3. **Fix** each violation in-place — don't just report, actually correct the file
4. **Save** the corrected file (overwrite original, or save as `*-corrected.qmd` if the user prefers)
5. **Report** what was found and fixed in a structured Quality Report

## Intake

The user provides a file path. If none is given, ask for one. Check that the file exists before proceeding.

Optional: the user may specify `--save-as <path>` to save the corrected version separately, preserving the original.

---

## Audit Checklists

Work through these in order. For each element, scan the entire file for all instances of that type before moving on.

### 1. YAML Frontmatter

The frontmatter block sits between the two `---` lines at the very top. Check that all required fields are present and correctly formatted.

**Required fields:**

```yaml
---
title: "..."          # must be a quoted string
subtitle: "..."       # must be a quoted string
date: last-modified   # use last-modified for living docs; fixed ISO date for archived
lang: de              # or 'en' — controls Quarto hyphenation and Moodle localization
toc-depth: 1          # or 2 for long chapters with H3 sub-sections
author:
  - name: Prof. Dr. Christian Kraus
    email: christian.kraus@thws.de
    role: Program Lead
    affiliation: THWS Business & Engineering
format:
  moodle-html
---
```

**Common YAML errors and fixes:**

| Problem | Fix |
|---|---|
| `format: moodle-html` written as plain string instead of block key | Rewrite as `format:\n  moodle-html` |
| Missing `subtitle` | Add with a descriptive placeholder: `subtitle: "..."` |
| `author` written as plain string instead of list | Rewrite using the `-` list form above |
| Missing `toc-depth` | Add `toc-depth: 1` |
| `lang` missing | Infer from content language and add |
| `date: today` or hardcoded date on a living doc | Replace with `date: last-modified` |

---

### 2. Flip-Cards

Pattern: `::: {.flip-card}` ... `:::`

The H4 heading is the **front** of the card (the term); the body paragraph is the **back** (the definition). The Lua filter depends on the heading being the very first content inside the div, immediately followed by the body on the next line — no gap.

**Rules:**
- Heading must be H4 (`####`) — not H3, H2, or bold text
- **No blank line between `####` and body text** — the filter breaks silently if there is one
- Body is one concise definition paragraph — no sub-headings, no lists inside
- Multiple flip-cards for related concepts: separate divs, not nested

```
✓ CORRECT:
::: {.flip-card}
#### Moral Hazard
Risiko, dass der Agent nach Vertragsschluss Handlungen vornimmt, die der Prinzipal nicht beobachten kann.
:::

✗ WRONG — blank line breaks the filter:
::: {.flip-card}
#### Moral Hazard

Risiko, dass der Agent...
:::

✗ WRONG — wrong heading level:
::: {.flip-card}
### Moral Hazard
Risiko...
:::
```

**How to fix:**
- Remove blank lines between `####` and body
- Upgrade `###` to `####`
- Convert bold-text "headings" (`**Term**`) into proper `####` headings

---

### 3. Drag-Exercises

Pattern: `::: {.drag-exercise}` ... `:::`

This is a fill-in-the-blank element. Students drag the italicized terms into blanks. It must be 1–2 flowing sentences — no heading, no list.

**Rules:**
- No heading (`####` or `###`) inside — the div body is just sentence text
- 1–2 sentences max
- Fill-in terms are marked with `*italics*` (single asterisks)
- No bullet lists inside

```
✓ CORRECT:
::: {.drag-exercise}
Der Erfüllungsbetrag ist der Betrag, der zur *Erfüllung der Verpflichtung* voraussichtlich *aufgewendet* werden muss.
:::

✗ WRONG — heading inside:
::: {.drag-exercise}
#### Lückentext
Der Erfüllungsbetrag ist der Betrag, der zur *Erfüllung* aufgewendet werden muss.
:::

✗ WRONG — list format:
::: {.drag-exercise}
- Der *Erfüllungsbetrag* ist...
- Das *Vorsichtsprinzip* ist...
:::
```

**How to fix:**
- Delete any heading line inside the div
- Convert list items to a flowing sentence
- If no terms are italicized, mark the 2–4 most important subject-specific terms with `*term*`

---

### 4. Case Studies

Pattern: `::: {.case-study}` ... `:::`

Every case-study must contain a nested `.solution` block. Without it, the Moodle filter renders the solution inline and unprotected — students see the answer immediately.

**Rules:**
- H4 heading required: `#### Case: [Title]`
- Must contain a nested `::: {.solution}` ... `:::` block
- Solution block contains a bolded lead: `**Lösung:**` or `**Solution:**`

```
✓ CORRECT:
::: {.case-study}
#### Case: Müller GmbH
Sachverhalt...

::: {.solution}
**Lösung:** Erklärung...
:::
:::

✗ WRONG — no solution block:
::: {.case-study}
#### Case: Müller GmbH
Sachverhalt...
Lösung: Erklärung direkt im Text.
:::
```

**How to fix:**
- If solution text exists inline after the case narrative: wrap it in `::: {.solution}` ... `:::`
- If no solution exists at all: add a placeholder `::: {.solution}\n**Lösung:** TODO\n:::`

---

### 5. Other Div Containers

**Details/Exkurs:**
```
::: {.details}
#### Exkurs: [Title]
Content...
:::
```
- Requires H4 heading starting with "Exkurs:"
- Fix: Add `#### Exkurs: ` if heading is missing or wrong level

**Quick-Check:**
```
::: {.quick-check}
Question text?

- Wrong answer
- **Correct answer** (bold = correct)
- Wrong answer
:::
```
- Correct answer must be in `**bold**`
- Fix: if no bold answer, bold the most plausible one and flag it in the report for human review

**Video:**
```
::: {.video}
{{< video https://youtu.be/ID >}}
:::
```
- Must use Quarto shortcode, not a raw `<iframe>` or HTML `<video>` tag
- Fix: convert raw YouTube URLs to shortcode format

**Widget:**
```
::: {.widget}
<iframe src="widgets/kapitel-NN/widget-name.html"
        width="100%" height="[N]px" frameborder="0"
        title="[Accessible description]">
</iframe>
:::
```
See section 6 for iframe-specific rules.

---

### 6. Widget IFrame Syntax

For every `<iframe>` found in the document:

**Rules:**
- `src` must be a **relative path** — no `http://`, no absolute filesystem paths
- `width="100%"` required
- `height` must be set (e.g., `height="420px"`)
- `frameborder="0"` required
- `title` attribute required (accessibility + PDF rendering)
- Must be wrapped in `::: {.widget}` ... `:::`

```
✓ CORRECT:
::: {.widget}
<iframe src="widgets/kapitel-03/widget-zinseszins.html"
        width="100%" height="420px" frameborder="0"
        title="Zinseszins-Rechner interaktiv">
</iframe>
:::

✗ WRONG — absolute path, missing title, wrong wrapper:
<iframe src="/Users/kraus/project/widgets/zinseszins.html" width="800px">
</iframe>
```

**How to fix:**
- Strip absolute path to relative: extract filename/subfolder part
- Add missing attributes
- Wrap bare iframes in `::: {.widget}` ... `:::`

---

## Quality Report Format

After all fixes, output this report before saving:

```
## QMD Corrector — Quality Report
**File:** [filename]
**Date:** [today]

### Summary
- Issues found: N
- Issues fixed: N
- Issues requiring manual review: N

### Fixed Automatically
| # | Element | Location | Problem | Fix Applied |
|---|---|---|---|---|
| 1 | flip-card | §2 "Moral Hazard" | Blank line after #### | Removed blank line |
| 2 | drag-exercise | §3 | Heading inside div | Deleted #### line |
| ... | | | | |

### Requires Manual Review
| # | Element | Location | Problem | Recommendation |
|---|---|---|---|---|
| 1 | quick-check | §4 | No bold answer — bolded most likely candidate | Verify correct answer |

### No Issues Found
- YAML frontmatter ✓
- Widget iframes ✓
```

If the file has no issues, say so clearly — a clean bill of health is valuable feedback too.

---

## Workflow

1. Read the file with the Read tool
2. Work through each checklist (YAML → flip-cards → drag-exercises → case-studies → details → quick-checks → videos → widgets)
3. For each violation: note it, apply the fix to the content string in memory
4. After all checks: output the Quality Report
5. Save the corrected file (use Edit for targeted fixes, or Write if changes are extensive)
6. Confirm to the user: "Saved. N issues fixed. See report above."

If the file is clean, still output the Quality Report showing all elements checked with ✓.

## Notes

- Prefer surgical edits over rewriting whole sections — the goal is to fix formatting, not rewrite content
- If the content itself seems wrong (e.g., a case-study with no solution text at all, just a placeholder), fix the syntax and flag for manual review
- Preserve all original content text exactly — only change structural/syntactic elements
- If you're unsure whether something is a violation or an intentional stylistic choice, flag it under "Requires Manual Review" rather than auto-fixing
