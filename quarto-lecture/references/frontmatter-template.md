# Canonical Frontmatter Template

Use this as the starting point for every new `.qmd` file. Adjust `title`, `subtitle`, `lang`, and `date` per chapter. Do not omit fields — they are required by the Moodle output pipeline.

```yaml
---
title: "Accounting"                        # Chapter or module title
subtitle: "Financial Statement Analysis"   # Subtitle or topic focus
date: last-modified                        # Auto-updates on save. For archived/exam materials use fixed: "2025-10-15"
lang: en                                   # 'de' for German, 'en' for English — controls hyphenation, labels, Moodle localization
toc-depth: 1                               # TOC shows H2 only. Use 2 for long documents with H3 sub-sections.

author:
  - name: Prof. Dr. Christian Kraus
    email: christian.kraus@thws.de
    role: Program Lead
    affiliation: THWS Business & Engineering

format:
  moodle-html
---
```

## Field notes

- **`lang`** controls Quarto's automatic labels ("Figure" vs. "Abbildung"), hyphenation engine, and Moodle interface localization. Always set this — wrong lang causes broken PDF hyphenation.
- **`toc-depth: 1`** is correct for single chapters (shows H2 sections only). For textbook-length compilations with H3 sub-sections, use `2`.
- **`date: last-modified`** is preferred for living lecture materials. Use a fixed ISO date for stable exam handouts or archived versions.
- **`author`** uses a YAML sequence (note the `-` prefix) to allow multiple authors if needed. Do not simplify to a plain string — downstream templates depend on the structured form.
- **`format: moodle-html`** activates the custom Quarto extension that runs Lua filters for Div container rendering and injects Moodle-compatible JavaScript for interactive elements.