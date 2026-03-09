---
name: case-builder
description: Create pedagogically rigorous business case studies following "The Ultimate Case Guide" methodology (Kupp & Mueller). This skill guides you through the structured "Case Development Funnel" to produce teaching cases that effectively combine compelling narratives (Lead) with specific learning objectives (Need). Output is a `.qmd` file ready for Quarto Single Source Publishing. Works in both German and English. Use this skill whenever the user mentions case studies, Fallstudien, teaching cases, business cases for classroom use, Kupp & Mueller, case method, case development, or wants to create narrative-driven learning materials about a company or business situation. Also trigger when the user wants to write a case for exam preparation, classroom discussion, or executive education, even if they don't explicitly say "case study".
---

## Core Philosophy

A good case study works like two-component epoxy adhesive — it only functions when two elements are firmly bonded:

1. **The Lead (Die Geschichte)**: A compelling event, person, or company — the narrative hook
2. **The Need (Der Bildungsbedarf)**: The specific learning objective (theory, concept, framework) to be taught

Without the Lead, it's a dry textbook exercise. Without the Need, it's just a newspaper article. The case only works when both are present and tightly connected.

Two concepts are easy to confuse but must stay distinct throughout:

- **Immediate Issue**: The concrete, urgent decision the protagonist faces *right now* — the narrative hook
- **Underlying Issue**: The theoretical concept students should learn by analyzing that decision — the actual learning objective

## Phase 1: Exploration Interview

Before writing a single word of text, clarify these four foundations. Ask them together in one message — don't trickle them out one by one.

1. **Educational Need (Underlying Issue)**: Which theoretical concept should students learn? Be specific. Not "innovation" but "Disruptive Innovation nach Christensen" or "Blue Ocean Strategy nach Kim/Mauborgne".

2. **Case Lead**: What's the story? Company, situation, context. A rich real-world scenario works best.

3. **Strategic decisions** to settle:
   - *Protagonist*: Who is the central character? Must be a real, named person the target audience can identify with — not "the management".
   - *Cut-off Point*: When does the case end? Ideally just *before* a critical decision is made, not after.
   - *Immediate Issue*: What specific, time-pressured decision does the protagonist face at that cut-off point?
   - *Target Audience*: Bachelor, Master/MBA, or Executive Education? This determines depth, vocabulary, and theoretical rigor.

4. **Sources & Release**: Is this based on a real, identifiable company? Does the user have internal data or does it rely on public sources? Will case release (company approval) be needed?

Wait for answers before starting Phase 2. A case built on vague foundations cannot be fixed in editing.

## Phase 2: Drafting

### Writing Rules

- **Tense**: Past tense throughout — this is a story, not a report
- **Perspective**: Third person, close to the protagonist's viewpoint. Never "I". Never "the company should".
- **Tone**: Neutral, descriptive, never prescriptive. The case asks questions; it never teaches solutions. A case that reveals the "right answer" has failed.
- **Length**: Typically 1,500–3,000 words for the main text. Executive cases can run longer; exam cases shorter.

### Structure

1. **Opening Paragraph** — the most critical part of the entire case. Must contain: protagonist by name, organization, specific point in time, and the immediate issue. Max 200 words. If this paragraph doesn't hook the reader, the case is dead.

2. **Company Background**: Relevant history, business model, key figures. Only what's needed to understand the decision — not a Wikipedia summary.

3. **External Context** *(if relevant)*: Industry dynamics, competitive landscape, regulatory environment. Serves to sharpen the decision's stakes.

4. **The Core Problem Area**: The section that develops the underlying issue without naming it explicitly. This is where analytical depth lives.

5. **The Decision**: The options available to the protagonist at the cut-off point. Present them fairly — the case must allow multiple defensible positions.

6. **Closing Paragraph**: Returns to the protagonist and the immediate issue. Creates urgency. Often ends mid-thought, with a question hanging in the air, or the protagonist staring at an email they haven't yet answered.

### Quarto File Template

```qmd
---
title: "[Case Title: Punchy Subtitle]"
subtitle: "Teaching Case"
author: "[Author Name]"
date: "[YYYY-MM-DD]"
lang: de
format:
  html:
    embed-resources: true
    toc: true
    toc-depth: 2
  pdf:
    documentclass: article
    geometry: "margin=2.5cm"
    toc: false
---

# [Case Title]

[Opening Paragraph – max 200 words. Protagonist + organization + time point + immediate issue. Hook the reader immediately.]

## Unternehmenshintergrund

[Relevant history and business model — only what informs the decision.]

## Markt- und Wettbewerbsumfeld

[External context if needed to sharpen the stakes.]

## [Specific Section Title — name it after the problem domain, not "The Problem"]

[The analytical core. Develops the underlying issue implicitly through facts and narrative.]

## Die Entscheidung

[Options available to the protagonist. Fair, balanced, no thumb on the scale.]

## [Closing — no section header needed, or use protagonist's name]

[Returns to immediate issue. Time pressure. Leave the reader hanging.]
```

### Exhibits (Anlagen)

Exhibits are not decoration — they are evidence. Include them when the narrative references data that students need to analyze. Common types:

**Financial table:**
```markdown
## Anlage 1: Umsatzentwicklung 2019–2023

| Jahr | Umsatz (Mio. €) | EBITDA-Marge | Mitarbeiter |
|------|-----------------|--------------|-------------|
| 2019 | 142             | 18,3 %       | 1.240       |
| 2020 | 128             | 14,1 %       | 1.180       |
| 2021 | 157             | 19,7 %       | 1.390       |
```

**Timeline:**
```markdown
## Anlage 2: Unternehmenschronologie

| Jahr | Ereignis |
|------|----------|
| 2005 | Gründung durch [Name] in [Stadt] |
| 2012 | Markteintritt DACH |
| 2018 | Börsengang SDAX |
```

Place exhibits after the closing paragraph, clearly numbered. Reference them inline in the text: *(vgl. Anlage 1)*.

## Phase 3: Gap Analysis

After completing the draft, run through this checklist before presenting to the user:

- Does the opening paragraph contain all four required elements (protagonist, organization, time, immediate issue)?
- Is the cut-off point clearly defined — does the case end *before* the decision?
- Are immediate issue and underlying issue clearly distinct, and does the case never explicitly name the underlying issue?
- Does the protagonist feel like a real person with real stakes, or like a placeholder?
- Are there gaps in the narrative that should become exhibits?
- Does the closing paragraph create genuine urgency?

Flag anything missing and propose additions.

## Phase 4: Teaching Note

After the case draft is approved, offer to create the Teaching Note. This is a separate `.qmd` file — confidential, for the instructor only, never distributed to students.

A Teaching Note makes the difference between a case that gets used once and one that becomes a course staple. It answers: "How do I actually run this in class?"

### Teaching Note Structure

```qmd
---
title: "Teaching Note: [Case Title]"
subtitle: "Vertraulich – nur für Lehrende"
author: "[Author]"
date: "[YYYY-MM-DD]"
lang: de
format:
  html:
    embed-resources: true
    toc: true
  pdf:
    documentclass: article
    geometry: "margin=2.5cm"
---

# Lernziele

Nach der Diskussion sollen Studierende in der Lage sein:

1. [Lernziel 1 — konkret und messbar formuliert]
2. [Lernziel 2]
3. [Lernziel 3]

# Synopsis

[2–3 Sätze: Worum geht es im Fall? Welches theoretische Konzept steht im Zentrum?]

# Theoretischer Rahmen

**Underlying Issue:** [Name des Konzepts]

[Kurze Darstellung des theoretischen Frameworks, das Studierende anwenden sollen. Literaturhinweise.]

# Diskussionsplan

## Einstieg (ca. 10 Min.)

**Einstiegsfrage:** [Offene Frage, die zur Story einlädt — nicht zur Theorie]

*Erwartete Antworten / Leitpunkte:*
- [Punkt 1]
- [Punkt 2]

## Vertiefung (ca. 25 Min.)

**Frage 2:** [Führt in den analytischen Kern]

*Erwartete Antworten:*
- [Punkt 1]

**Frage 3:** [Baut Brücke zur Theorie]

*Erwartete Antworten:*
- [Punkt 1]

## Theoriebrücke (ca. 10 Min.)

**Frage:** Wie erklärt [Theoretisches Konzept] das, was wir gerade analysiert haben?

*Ziel: Studierende benennen das Underlying Issue selbst.*

## Synthese & Abschluss (ca. 10 Min.)

**Schlussfrage:** Was würden Sie dem Protagonisten jetzt raten — und warum?

# Tafelbild (Board Plan)

[Skizze oder Beschreibung, wie das Tafelbild am Ende der Diskussion aussehen soll. Welche Konzepte, Argumente, Entscheidungsoptionen landen wo?]

# Zeitplanung

| Phase | Dauer | Aktivität |
|-------|-------|-----------|
| Einstieg | 10 Min. | Einstiegsfrage, Überblick |
| Vertiefung | 25 Min. | Analytische Diskussion |
| Theoriebrücke | 10 Min. | Konzept benennen |
| Synthese | 10 Min. | Handlungsempfehlung |
| Puffer | 5 Min. | — |

# Anlagen-Guide

[Für jede Anlage: Wann im Diskussionsverlauf einsetzen? Was sollen Studierende darin erkennen?]
```

## Best Practices

**What separates a strong case from a weak one:** The strong case has a protagonist who feels trapped — the decision is genuinely hard, the stakes are real, and there is no obvious right answer. Students should be able to argue multiple positions and all of them should be defensible.

**The most common failure mode:** The case teaches instead of provoking. Phrases like "this shows that...", "the correct approach would be...", "management made the mistake of..." — all of these destroy the case method. Cut them without mercy.

**The second most common failure mode:** The immediate issue and underlying issue get conflated. The protagonist deciding whether to launch a product in China is an immediate issue. Porter's Five Forces applied to the Chinese market is the underlying issue. The case presents the former; students discover the latter.

## Output

Save both the case study and (if created) the Teaching Note to `/sessions/elegant-festive-brown/mnt/outputs/` and present links to the user via the `present_files` tool.

File naming convention:
- Case: `fallstudie_[unternehmensname]_[jahr].qmd`
- Teaching Note: `teaching_note_[unternehmensname]_[jahr].qmd`
