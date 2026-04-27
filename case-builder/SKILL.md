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
date: last-modified
lang: de
format:
  handout-typst
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

### Heading Hierarchy Discipline

If an H2 section contains only a single H3 subsection, the H3 level is unnecessary — promote the content to H2 and eliminate the empty nesting. A heading level is only justified when there are at least two siblings. Cases benefit from continuous narrative flow; artificial sub-divisions interrupt the reading experience without adding navigational value.

### Case Architecture for Lecture Use: Integrated Structure

The most important structural principle is **locality**: data and questions belong at the point in the text where they are needed, not in separate sections at the end.

**Why this matters in the classroom:** When a case separates narrative, exhibits, and discussion questions into three distinct blocks, students must read the whole thing, then re-read to connect questions to narrative, then flip to exhibits to find the numbers. In a lecture hall, this creates friction and breaks the discussion flow. The instructor has to say "go back to page 2" and "see exhibit 3 on page 5" — the case is fighting the teaching.

The integrated structure solves this:

```
[Sachverhalt A — narrative + any data needed for this section]

[Discussion question(s) for Sachverhalt A]

---

[Sachverhalt B — narrative + any data needed for this section]

[Discussion question(s) for Sachverhalt B]
```

This means:
- **Inline data tables**: Place tables, figures, and key numbers directly inside the narrative section they belong to — not in a separate "Exhibit" section at the end. A table appears where the protagonist encounters it, where the student needs it.
- **Questions follow their section**: Each discussion question appears immediately after the section it tests. The student reads the scenario, sees the question, and has everything in one place.

**When to still use a labeled block** (call it "Daten" or "Zahlen", not "Anlage"): If a table is large and would interrupt the narrative flow, you may place it as a labeled sub-block within the same section — still inline, just visually set off. Never put it at the end of the case.

**Exception — pure narrative/strategy cases**: If the case contains no quantitative data and the questions are open-ended strategic choices, it can work to place all questions at the end. But as soon as numbers appear, integrate them.

**Template for an integrated, quantitative case section:**

```markdown
## [Sachverhalt: descriptive title]

[Narrative: what happened, what the protagonist discovered, what the decision is]

[Data table inline, if needed:]

| Spalte A | Spalte B |
|----------|----------|
| Wert     | Wert     |

[If a note about the data is needed, place it here as a brief italic paragraph]

**Frage [N]: [Question title in bold]**

[Question text. One to three focused questions. Self-contained — the student does not need to look anything up elsewhere to answer this question.]

---
```

This `---` separator between sections is useful: it gives visual breathing room and signals "this section is complete, next section begins."

**German-language cases (THWS/IFRS context):** Use `### Aufgabe N — [Analysefeld]` for task headings and `**Anlage N: [Titel]**` (bold, not a heading) for data tables within the same section. Task titles name the analytical field, not the theory: `Aufgabe 2 — Erstbewertung und Folgebewertung` not `Aufgabe 2 — IFRS 16.26–27 anwenden`. Tasks are broad, open-ended — no a/b/c/d sub-parts that walk students through the method. Finding the method is their job.

## Phase 3: Gap Analysis

After completing the draft, run through this checklist before presenting to the user:

- Does the opening paragraph contain all four required elements (protagonist, organization, time, immediate issue)?
- Is the cut-off point clearly defined — does the case end *before* the decision?
- Are immediate issue and underlying issue clearly distinct, and does the case never explicitly name the underlying issue?
- Does the protagonist feel like a real person with real stakes, or like a placeholder?
- Does every discussion question appear immediately after the section it relates to — not batched at the end?
- Is every data table or figure placed inline at the point where it is needed in the narrative — not in a separate exhibit section?
- Can a student answer each question without having to flip to another part of the document?
- Does the closing paragraph create genuine urgency?

Flag anything missing and propose additions.

## Phase 3b: Arithmetic Quality Check (for quantitative cases)

**Do this before presenting the draft to the user.** Quantitative cases fail silently — a wrong number in the data section produces a wrong "correct answer" in the teaching note, and the error only surfaces when a student finds the inconsistency in class. That is embarrassing and undermines trust in the material.

For every number in the case, verify:

1. **Internal consistency of input data**: Do all line items in tables sum to their stated totals? Add them up explicitly — do not eyeball. If a table shows individual items and a total, the sum must match.

2. **Derivation chain**: Is every number that students are expected to calculate actually derivable from the numbers given? Work through the model solution yourself, using only the data provided in the case. If you need a number that isn't there, it must be added.

3. **Cross-reference**: Does the same number appear correctly in multiple places? (e.g., a cost figure used in the narrative, then in a table, then in the solution — all three must be identical.)

4. **Pro-rata and rounding**: For time-based calculations (monthly depreciation, partial-year charges), apply the pro-rata explicitly. State the exact rounding convention if results differ depending on rounding.

5. **Conceptual correctness**: Beyond arithmetic, check whether the numerical setup embeds the right conceptual structure. For example: if the case involves EBITDA, does the design of the numbers actually require understanding what EBITDA includes and excludes? A number that "works out" under a wrong concept is worse than a wrong number — it teaches students to apply the wrong framework.

Flag any discrepancy and resolve it in the case *before* writing the teaching note solution. A teaching note solution derived from wrong input data will itself be wrong.

## Phase 4: Teaching Note

After the case draft is approved (and the arithmetic check has passed), offer to create the Teaching Note. This is a separate `.qmd` file — confidential, for the instructor only, never distributed to students.

A Teaching Note makes the difference between a case that gets used once and one that becomes a course staple. It answers: "How do I actually run this in class?"

### Structure principle: mirror the case

The teaching note discussion plan must follow the same question order as the case itself. If the case has questions Q1–Q5 each after their section, the discussion plan covers Q1–Q5 in that order. Do not reorganize into "Einstieg / Vertiefung / Theoriebrücke" phases that cut across the question structure — this forces the instructor to mentally remap case to teaching note while standing at the board.

For each question in the case, the teaching note provides:
- The **model solution** (for quantitative questions: full worked calculation with intermediate steps)
- **Common errors** students make on this question and how to address them
- **Discussion prompts** to move the class forward if they get stuck
- **Time allocation**

### Teaching Note Template

```qmd
---
title: "Teaching Note: [Case Title]"
subtitle: "Vertraulich — nur für Lehrende"
author: "[Author]"
date: last-modified
lang: de
format:
  handout-typst
---

# Lernziele

Nach der Diskussion sollen Studierende in der Lage sein:

1. [Lernziel 1 — konkret und messbar, direkt auf eine Frage des Falls abbildbar]
2. [Lernziel 2]
3. [Lernziel 3]

# Synopsis

[2–3 Sätze: Worum geht es im Fall? Welches theoretische Konzept steht im Zentrum?]

# Theoretischer Rahmen

**Underlying Issue:** [Name des Konzepts]

[Kurze Darstellung des theoretischen Frameworks. Literaturhinweise.]

# Vollständige Lösung

## Frage [N]: [Fragetitel, identisch zum Falltext]

**Musterlösung:**

[For quantitative questions: complete worked solution showing every step.
Show the derivation chain, not just the result.
Example format:
  Rechnungsbetrag gesamt:  185.000 €
  ./. Training (IAS 16.19): (3.500) €
  ─────────────────────────────────
  Anschaffungskosten:      181.500 €
]

**Typische Fehler:**
- [Fehler 1 und warum er passiert]
- [Fehler 2]

**Diskussionsimpulse:** [What to ask if the class is stuck or going in the wrong direction]

**Zeitbedarf:** ca. [N] Min.

---

## Frage [N+1]: [Fragetitel]

[Same structure — one block per question]

---

# Diskussionsplan (Zeitübersicht)

| Frage | Inhalt | Dauer |
|-------|--------|-------|
| Einstieg | [Opening question before Q1] | 10 Min. |
| Frage 1 | [Title] | [N] Min. |
| Frage 2 | [Title] | [N] Min. |
| Synthese | Abschluss und Verbindung zum nächsten Thema | 10 Min. |
| **Gesamt** | | **[N] Min.** |

# Tafelbild (Board Plan)

[Sketch or description of how the board should look at the end of discussion. What concepts, numbers, and conclusions land where. For quantitative cases: show the final calculation structure.]

# Instructor Alerts

[2–4 numbered points flagging the hardest conceptual traps in this case — the moments where students most commonly get it wrong and why. These are the teaching moments worth preparing for explicitly.]
```

### Model solution quality for quantitative questions

The model solution is the most failure-prone part of a teaching note. To write it correctly:

- **Derive, don't assert**: Show every arithmetic step. A solution that says "Annual depreciation: €20,813" without showing `(181,500 − 15,000) ÷ 8 = 20,812.50` is not a model solution — it's a result that the instructor can't verify at a glance.
- **State what's excluded and why**: For every amount not included (e.g., training costs), give the IAS/IFRS paragraph reference. This is what the student needs to learn.
- **Show acceptable ranges for rounded results**: If a calculation involves intermediate rounding, state which values are acceptable (e.g., "€4,440–€4,442 depending on rounding").
- **Cross-check the solution against the case data before writing it**: Use only numbers that appear in the case. If you find yourself needing a number that isn't in the case, go back and add it.

## Best Practices

**What separates a strong case from a weak one:** The strong case has a protagonist who feels trapped — the decision is genuinely hard, the stakes are real, and there is no obvious right answer. Students should be able to argue multiple positions and all of them should be defensible.

**The most common failure mode:** The case teaches instead of provoking. Phrases like "this shows that...", "the correct approach would be...", "management made the mistake of..." — all of these destroy the case method. Cut them without mercy.

**The second most common failure mode:** The immediate issue and underlying issue get conflated. The protagonist deciding whether to launch a product in China is an immediate issue. Porter's Five Forces applied to the Chinese market is the underlying issue. The case presents the former; students discover the latter.

## Output

Save both files to the project's `Fallstudien/` directory (relative to the working directory), or to the path the user specifies.

File naming convention:
- Case: `fallstudie_[unternehmensname]_[jahr].qmd`
- Teaching Note: `teaching_note_[unternehmensname]_[jahr].qmd`
