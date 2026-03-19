---
name: slides-to-notes
description: Generate Quarto lecture notes (QMD, handout-typst format) from MARP slides — a full companion textbook (Begleitband/Skriptum). Expands slide bullet points into textbook-style prose, converts inline *(Author, Year)* citations to proper BibTeX, validates and auto-fetches missing sources via CrossRef/arxiv API, and creates or updates a .bib file. Use when the user wants a companion reader for a MARP presentation, asks to "write lecture notes for these slides", "erstelle ein Skript zu diesen Folien", "Begleitband schreiben", "Vorlesungsnotizen", "Notes zu den Folien", or wants to turn slide content into academic prose. Also trigger when the user has a .md slides file and wants a QMD output, or mentions handout-typst + slides in the same breath.
---

# Slides to Notes

You turn MARP presentation slides into a polished, textbook-style Quarto lecture document (Begleitband). The reader of this document should be able to follow the lecture without having attended it — it is a proper academic companion, not a transcript.

## What you need from the user

Before starting, make sure you have:

1. **Path to the MARP slides file** (.md). If not given, ask.
2. **Path to an existing .bib file** (optional). If not given, you'll create `references.bib` in the same directory as the slides.
3. **Author name and date** — take from the slides YAML if present; otherwise use `Prof. Dr. Christian Kraus` and today's date.

If the slides file is open in the IDE or mentioned in context, use that. Do not ask for a path the user has already provided.

---

## Step 1: Read the slides

Read the MARP .md file. Extract:
- **YAML header**: title, subtitle, author, date, language (lang)
- **Slide structure**: each `---` delimited slide with its `<!-- _class: ... -->` directive and content
- **All inline citations**: every `*(Author, Year)*` or `*(Author, Year, Venue)*` pattern — collect them as a list

Also read the existing .bib file if it exists.

---

## Step 2: Resolve citations

For each extracted citation, determine if it is already covered in the .bib file (match by author name + year, fuzzy is fine).

For **missing** citations, look for metadata in this priority order:

**Priority 1 — Context folder**: Before making any external API calls, check if a `Context/` directory exists next to the slides file. Research documents there (e.g., a Perplexity export, a literature overview, a `Find peer-reviewed research...` file) often already contain the exact URLs, DOIs, or footnotes for the cited papers. This is faster and more reliable than API calls — and avoids hallucinated metadata from LLM-based fetch tools. Parse any footnote links (`[^N]: https://...`) that correspond to the cited papers.

**Priority 2 — arxiv API**: If an arxiv ID like `2403.13690` appears in the citation or nearby in the slide text, fetch from:
  `https://export.arxiv.org/abs/{id}` — parse the returned XML for title, authors, year, abstract.
  ⚠️ Important: Verify that the returned paper matches the description in the slides. LLM-based fetch tools can hallucinate paper titles. If there's any doubt, flag the match as uncertain.
- **DOI**: If a DOI appears, fetch from:
  `https://api.crossref.org/works/{doi}` — parse the returned JSON for bibliographic data.
- **General search**: If neither is available, construct a `@misc` stub:
  ```bibtex
  @misc{AuthorYear,
    author    = {Author},
    year      = {Year},
    title     = {{NEEDS VERIFICATION}},
    note      = {Cited in slides as *(Author, Year)*. Metadata could not be auto-fetched — please verify.}
  }
  ```

Assign citekeys in the format `AuthorYear` (e.g., `Loewenstein2003`, `Kleinberg2021`, `DEplain2022`). If the same author+year appears multiple times, add a letter suffix (`Stajner2022a`, `Stajner2022b`).

After resolution, **update the .bib file** (create if it does not exist, append new entries if it does).

---

## Step 2b: Validate venue and year claims

While building the .bib, also flag **venue or year mismatches** between what the slides claim and what you found:

- E.g., slide says "NeurIPS 2022" but the paper was published at ACL 2022 → flag this explicitly in the .bib `note` field and in the Step 5 report
- E.g., slide says "2022" but the DOI shows 2020 → flag the year discrepancy
- Do NOT silently correct — always report what the slide says vs. what the source says, so the author can decide

These discrepancies are valuable findings: the author probably wants to know about them before publishing or teaching.

---

## Step 3: Map slide citations to citekeys

Build a mapping: every `*(Author, Year)*` occurrence in the slides → its resolved `[@citekey]` in Pandoc format. You'll use this when writing the QMD.

If citations in the slides are now properly resolved, and the slides file is the user's own file, **note at the end of your response** which slide citations could be updated to use the citekey format — but do NOT modify the slides file unless the user asks you to.

---

## Step 4: Write the QMD

### YAML header

Use this template exactly — populate from slide metadata:

```yaml
---
title: "..."
subtitle: "..."           # omit if no subtitle in slides
author: "Prof. Dr. Christian Kraus"
date: "YYYY-MM-DD"
lang: de                  # or en, matching the slides language
format: handout-typst
bibliography: references.bib
csl: apa.csl
---
```

### Document body

Work through the slides in order:

**Title slide** → skip (covered by YAML)

**Agenda slide** → Write a brief 2–3 sentence introduction to the lecture topic and what the reader will encounter in this document. Do NOT reproduce the agenda as a list.

**Lernziele slide** → Render as a Quarto callout block:
```markdown
::: {.callout-note title="Lernziele"}
After working through this material, you will be able to:

- ...
- ...
:::
```

**Structural/transition slides** (e.g., "Teil 1 — Das Empathieproblem") → Use as a `##` section heading in the QMD. Add 1–2 sentences of framing prose to orient the reader.

**Content slides** → This is the heart of the document. For each content slide:

1. Use the slide heading as a `###` subheading (or `##` if appropriate for the structure)
2. Expand every bullet point into 2–4 full sentences of textbook prose. Explain concepts, provide context, show relationships between ideas.
3. If the slide had a table, reproduce it in Markdown and add a sentence explaining what it shows.
4. If the slide had a `→ **Folge:**` or `→ **Fazit:**` consequence arrow, integrate it as a logical conclusion paragraph: "This leads to the conclusion that..." / "Daraus folgt, dass..."
5. If the slide had a `# <!-- fit -->` provocation, render it as a blockquote and then unpack the provocative claim in 3–5 sentences.
6. Replace every `*(Author, Year)*` citation with `[@citekey]` using your mapping from Step 3.

**Pause/discussion slides** → Include as a Quarto callout:
```markdown
::: {.callout-tip title="Reflexionsfrage"}
[The discussion question from the slide]
:::
```

**Final slide (Literatur/References)** → Skip — Pandoc will auto-generate the bibliography from the .bib file.

### Writing style

- Formal academic German (or English, matching the slides language)
- Use "Sie" in German; active voice preferred
- Avoid bullet lists in the notes — convert everything to prose
- Transitions between paragraphs should feel natural, like a textbook chapter
- Appropriate density: roughly 3–5× the word count of the corresponding slide content

---

## Step 5: Report

After writing the QMD and .bib, give the user a brief report:

```
## Ergebnis

**QMD gespeichert:** path/to/notes.qmd
**BibTeX gespeichert:** path/to/references.bib

### Zitationsauflösung
| Zitation (Folie) | Citekey | Status |
|---|---|---|
| *(Loewenstein & Ariely, ~2003)* | Loewenstein2003 | ✅ auto-fetched via CrossRef |
| *(DEplain, ACL Findings 2022)* | Stajner2022 | ✅ found in existing .bib |
| *(MotorEase, CHI 2023)* | Zhang2023 | ⚠️ stub entry created — needs manual verification |

### Folien-Hinweise
The following slides have inline citations that could be updated to BibTeX format — let me know if you want me to update the slides file:
- Folie 8: *(DEplain, ACL Findings 2022)* → `[@Stajner2022]`
- Folie 11: *(CHI 2023)* → `[@Zhang2023]`
```

---

## File naming convention

- QMD: same name as the slides file, with `.qmd` extension (e.g., `KI_Empathie_Inklusion.qmd`)
- .bib: `references.bib` in the same directory, unless the user specifies otherwise
- Place both in the same directory as the input slides file

---

## Important constraints

- **Never invent content** — only expand what is actually on the slides
- **Never invent citations** — if a source cannot be resolved, create a stub and say so clearly
- **Never modify the slides file** unless explicitly asked
- The QMD must be renderable by Quarto — use only valid Quarto/Pandoc Markdown
