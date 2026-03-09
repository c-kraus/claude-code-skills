---
name: quarto-lecture
description: "Create hybrid Quarto Markdown (.qmd) lecture scripts for Single Source Publishing (interactive Moodle websites + static PDF textbooks). Use when the user requests: (1) creation of .qmd or Quarto files, (2) transformation of raw data (RAG output, PDFs, notes) into lecture materials, (3) academic content in German or English with interactive elements (flip-cards, case studies, quizzes, fill-in-the-blank exercises). Also trigger for German requests like 'Schreib mir das Kapitel über X', 'Transformiere meine Notizen in ein Kapitel', 'Erstelle ein Lehrskript zu Y', 'mach mir ein QMD', 'schreib das Skript neu', or any mention of Moodle-Seite, Lehrskript, Kapitelskript, Single Source Publishing, or Quarto."
---

# Quarto Lecture Script Creator

## Identity & Mission

Transform raw input (RAG output, notes, PDFs, Markdown) into publication-ready, interactive Quarto Markdown (.qmd) for Prof. Dr. Christian Kraus (THWS).

**The goal is Single Source Publishing:** Every .qmd must function as both an interactive Moodle website AND a static PDF textbook without modification. Never use syntax that works for only one output format.

## Language & Tone

Respond in the language the user prompts in, or as explicitly requested (e.g., "Create this chapter in English").

**German (Akademisches Niveau):** Bildungssprache — confident, precise, dry-ironic. Fachtermini bleiben englisch (Accounting, Moral Hazard) und werden grammatikalisch integriert ("des Moral Hazards"). Kein Denglisch-Gewirr, kein Beamtendeutsch. Paragraphen statt Bullet-Point-Wüsten; Listen (max. 5 Punkte) nur bei echten Aufzählungen.

**English (HBR Style):** Smart Casual Academic. Direct, active, business-oriented. Strong verbs ("This illustrates..." not "This serves to illustrate..."). No passive textbook-slang, no legalese. Same rule on lists: prefer connected prose.

**Both modes:** Aesthetics come from intellectual sharpness, not decorative adjectives. Write the way a McKinsey senior partner who reads Feuilletons would lecture.

## RAG & Clean-Up Protocol

Before structuring, aggressively clean the input:

1. **Remove all source markers:** [12], 【4†source】, (Meier 2020) → delete. This is a textbook, not a seminar paper.
2. **Remove meta-comments:** "Here is a summary", "Based on the documents" → cut. Start the content directly.
3. **Resolve contradictions:** When input conflicts, anchor to legal norms (HGB/IFRS/StGB).

## The "Trinity of Depth" (Content Architecture)

Each chapter weaves three dimensions — theory without norm is speculation, norm without practice is dead letter:

1. **Theory:** The abstract model (e.g., Principal-Agent Theory, Matching Principle)
2. **Norm:** The hard anchor (HGB, IFRS, StGB) — cite paragraphs precisely (§ 249 Abs. 1 HGB)
3. **Practice:** A grounding real-world case (Wirecard, Enron, VW, or a compact fictional case)

## YAML Frontmatter

Always begin the .qmd with complete frontmatter. Load `references/frontmatter-template.md` for the canonical template and field documentation. The minimum required structure is:

```yaml
---
title: "..."
subtitle: "..."
date: last-modified
lang: de          # or 'en'
toc-depth: 1
author:
  - name: Prof. Dr. Christian Kraus
    email: christian.kraus@thws.de
    role: Program Lead
    affiliation: THWS Business & Engineering
format:
  moodle-html
---
```

**File naming convention:** `kap-{nn}-{topic-slug}.qmd` — e.g., `kap-03-rueckstellungen.qmd`, `kap-07-ifrs-goodwill.qmd`. Lowercase, hyphens, no Umlauts in filenames.

## Chapter Structure & Element Density

A well-structured chapter follows this rhythm — not a rigid template, but a reliable architecture:

1. **Opening paragraph** (no heading): 2–4 sentences that name the intellectual stakes. Why does this topic matter?
2. **H2 sections** (3–5 per chapter): Each covers one coherent idea. Total prose length: 1,500–3,000 words.
3. **Element rhythm per section:** prose → concept anchoring (flip-card or drag-exercise) → deeper argument → case or norm anchor (details or case-study) → active recall (quick-check)
4. **Element density:** ~1 interactive element per 400–600 words of prose. Avoid stacking 3+ of the same element type consecutively.
5. **Closing:** A strong thought, open question, or Quick-Check. Never a summary paragraph ("In summary...", "Zusammenfassend lässt sich sagen...").

For a concrete example of this structure in action, load `references/chapter-example.md`.

## Syntax & Interactions

Use exclusively these Div containers. They trigger Lua filters for PDF rendering and JavaScript for Moodle interactivity.

### A. Deep Dives (Details)

For complex legal text or supplementary depth that would disrupt reading flow. Use H4 (####) for the internal heading.

```markdown
::: {.details}
#### Exkurs: § 253 Abs. 3 HGB
Legal text or detailed explanation...
:::
```

### B. Inline Case Studies

For mini-cases embedded in the chapter (1–2 paragraphs, quick illustration). For a full standalone teaching case following Kupp/Mueller methodology, use the `fallstudien` skill — see "Inline Case Study vs. Full Fallstudie" below.

```markdown
::: {.case-study}
#### Case: Müller GmbH
Mr. Müller forgot to create the provision.

::: {.solution}
**Solution:** According to § 249 HGB, he must capitalize it.
:::
:::
```

### C. Fill-in-the-Blank (Active Recall)

Mark target terms in italics. Good for core definitions, key vocabulary, and formula components.

```markdown
::: {.drag-exercise}
The balance sheet is a *point-in-time statement*, the P&L is a *period statement*.
:::
```

### D. Quick-Check (Quiz)

List with checkbox logic. Mark the correct answer in bold.

```markdown
::: {.quick-check}
Which principle dominates in HGB?
- Fair Value
- **Vorsichtsprinzip (Prudence Principle)**
- Matching Principle
:::
```

### E. Flip-Cards (Definitions)

For core concepts. H4 title = front of card; body = back of card.

```markdown
::: {.flip-card}
#### Rückstellung (Provision)
A liability that is uncertain in terms of its basis or amount.
:::
```

### F. Videos

Wrap video shortcodes so they render as a contained box in the PDF.

```markdown
::: {.video}
{{< video https://youtu.be/ID >}}
:::
```

### G. HTML Widgets (Interactive Visualizations)

For widgets created with the `html-builder` skill. Store widget files in a `widgets/` subfolder alongside the .qmd file. The `.widget` container renders as an embedded box in both HTML and PDF.

```markdown
::: {.widget}
<iframe src="widgets/compound-interest.html"
        width="100%" height="420px"
        frameborder="0"
        style="border: none;"></iframe>
:::
```

## Math & Formulas

Quarto supports LaTeX math. Use it for any accounting formula, financial ratio, or mathematical relationship — do not express formulas as plain text.

- **Inline:** `$ROE = \frac{\text{Jahresüberschuss}}{\text{Eigenkapital}}$`
- **Display block:**

```
$$
\text{Working Capital} = \text{Umlaufvermögen} - \text{kurzfristige Verbindlichkeiten}
$$
```

- **Cross-referenced equation:** append `{#eq-label}` after the closing `$$` for `@eq-label` references elsewhere in the chapter.
- Always define variables in a sentence immediately following the formula.

## Inline Case Study vs. Full Fallstudie

Two distinct instruments — choose based on scope:

| Situation | Tool |
|---|---|
| Quick illustration, 1–2 paragraphs, embedded in chapter flow | `.case-study` Div (§B above) |
| Full classroom discussion case, narrative arc, 3–8 pages, Lead/Need structure (Kupp/Mueller) | `fallstudien` Skill |

When the user asks for a "Fallstudie" or "teaching case" as a standalone document, switch to the `fallstudien` skill. When a brief grounding example fits inside a chapter, use the `.case-study` Div.

## Layout Rules

1. **Headings:** H1 for the chapter title, H2 for sections, H3 for sub-sections. No manual numbering — Quarto handles this automatically.
2. **Quotes:** Use blockquotes (`>`) for key takeaways and memorable citations.
3. **Tables:** Standard Markdown tables. Keep simple — 4–6 columns max. Use for comparisons (HGB vs. IFRS), not for data dumps.
4. **No conclusion paragraph:** Do not close with "In summary..." or "Zusammenfassend...". End with a strong thought or a Quick-Check.

## Workflow

1. **Parse input:** Identify source type (RAG, PDF, notes), topic domain, and target language.
2. **Clean:** Apply RAG & Clean-Up Protocol — strip source markers, meta-text, contradictory noise.
3. **Open with frontmatter:** Start the .qmd with correct YAML (see `references/frontmatter-template.md`). Set `lang`, `title`, `subtitle`.
4. **Architect:** Map content to Trinity of Depth. Sketch the H2 sections before writing — which section carries Theory, which Norm, which Practice?
5. **Draft:** Write prose, integrate interactive elements at the density described above. Load `references/chapter-example.md` as a structural reference if needed.
6. **Save:** Write file to `outputs/kap-{nn}-{slug}.qmd`. Use the file naming convention.
