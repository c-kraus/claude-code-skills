# Color Palette & Brand Style — THWS

**This is the single source of truth for all colors and brand-specific styles.** Based on the THWS corporate design with `#ff6a00` (THWS Orange) as the primary brand color.

---

## Shape Colors (Semantic)

Colors encode meaning, not decoration. Each semantic purpose has a fill/stroke pair.

| Semantic Purpose | Fill | Stroke |
|------------------|------|--------|
| Primary/Neutral | `#fff0e0` | `#ff6a00` |
| Secondary | `#ffe0c2` | `#cc5500` |
| Tertiary | `#fdf2e9` | `#b34700` |
| Start/Trigger | `#fed7aa` | `#c2410c` |
| End/Success | `#a7f3d0` | `#047857` |
| Warning/Reset | `#fee2e2` | `#dc2626` |
| Decision | `#fef3c7` | `#b45309` |
| AI/LLM | `#ddd6fe` | `#6d28d9` |
| Inactive/Disabled | `#f1f5f9` | `#94a3b8` (use dashed stroke) |
| Error | `#fecaca` | `#b91c1c` |

**Rule**: Always pair a darker stroke with a lighter fill for contrast.

---

## Text Colors (Hierarchy)

Use color on free-floating text to create visual hierarchy without containers.

| Level | Color | Use For |
|-------|-------|---------|
| Title | `#cc5500` | Section headings, major labels |
| Subtitle | `#ff6a00` | Subheadings, secondary labels |
| Body/Detail | `#64748b` | Descriptions, annotations, metadata |
| On light fills | `#333333` | Text inside light-colored shapes |
| On dark fills | `#ffffff` | Text inside dark-colored shapes |

---

## Evidence Artifact Colors

Used for code snippets, data examples, and other concrete evidence inside technical diagrams.

| Artifact | Background | Text Color |
|----------|-----------|------------|
| Code snippet | `#1e293b` | Syntax-colored (language-appropriate) |
| JSON/data example | `#1e293b` | `#ff6a00` (THWS Orange) |

---

## Default Stroke & Line Colors

| Element | Color |
|---------|-------|
| Arrows | Use the stroke color of the source element's semantic purpose |
| Structural lines (dividers, trees, timelines) | Primary stroke (`#ff6a00`) or Slate (`#64748b`) |
| Marker dots (fill + stroke) | Primary fill (`#ff6a00`) |

---

## Background

| Property | Value |
|----------|-------|
| Canvas background | `#ffffff` |
