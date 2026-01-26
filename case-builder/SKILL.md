---
name: case-study-builder
description: Create structured case studies for business and accounting education with realistic storytelling, exam-level tasks, and solutions for instructors. Generates Quarto .qmd files with student/instructor content separation. Use when the user requests case studies, practical exercises, or application-oriented learning materials. Trigger phrases include "Erstelle eine Case Study", "Create a case study", "Fallstudie generieren", "practical exercise for [topic]".
---

# Case Study Builder

Generate professional, exam-level case studies with realistic storytelling that enable students to practice applying theoretical concepts to practical situations.

## Mission

Create case studies that:
- Tell a realistic, engaging story (moderate storytelling, not overdone)
- Include exam-level tasks that test practical application
- Enable active practice of lecture concepts
- Support both student and instructor views in Quarto

## Output Format

**Always generate a complete .qmd file** with proper Quarto syntax, including:
- YAML frontmatter
- Structured case study content
- Tasks for students
- Solutions visible only to instructors via `{.content-visible when-meta="show_solutions"}`

## Difficulty Levels

### Basic
- **Target:** First introduction to concept application
- **Complexity:** Single concept, straightforward scenarios
- **Tasks:** 2-3 guided questions
- **Calculations:** Simple, one-step
- **Example:** Calculate ROI for a single investment

### Intermediate
- **Target:** Standard exam level
- **Complexity:** Multiple related concepts, realistic scenarios
- **Tasks:** 3-5 structured questions
- **Calculations:** Multi-step, requires understanding of relationships
- **Example:** Analyze depreciation impact on financial statements

### Advanced
- **Target:** Complex application, critical thinking
- **Complexity:** Multiple interrelated concepts, ambiguous situations
- **Tasks:** 4-6 questions requiring analysis and justification
- **Calculations:** Complex, requires assumptions and trade-off decisions
- **Example:** Strategic decision-making with incomplete information

## Standard Structure

Every case study follows this structure:

```markdown
## Case Study: [Descriptive Title]

**Difficulty:** [Basic | Intermediate | Advanced] | **Topic:** [Main Concept] | **Duration:** [~15-30 min]

### Context

[2-3 paragraphs of realistic storytelling that sets up the scenario. Include:
- Company/person background
- Relevant financial/business situation
- Key numbers/data
- The challenge or decision point]

### Tasks

#### Task 1: [Aspect 1]
[Clear question that tests understanding and application]

::: {.content-visible when-meta="show_solutions"}
**Solution:**

[Detailed solution with explanation]

**Grading Notes:**
- Key point 1 (X points)
- Key point 2 (X points)
:::

#### Task 2: [Aspect 2]
[Question building on Task 1]

::: {.content-visible when-meta="show_solutions"}
**Solution:**

[Solution with step-by-step reasoning]
:::

[... additional tasks ...]

### Reflection (Optional for Advanced)

[Open question for critical thinking]

::: {.content-visible when-meta="show_solutions"}
**Discussion Points:**
- [Key consideration 1]
- [Key consideration 2]
:::
```

## Content Guidelines

### Storytelling Quality

**Good storytelling:**
- ✅ Realistic company/person names and contexts
- ✅ Concrete numbers and data
- ✅ Clear business challenge or decision point
- ✅ Relevant to students' future professional contexts
- ✅ 2-3 paragraphs maximum for context

**Avoid:**
- ❌ Overly dramatic or fictional scenarios
- ❌ Irrelevant personal details
- ❌ Vague or generic situations
- ❌ Too much backstory (keep it focused)

### Task Design

**Exam-Level Criteria:**
- Tasks should be **answerable in exam conditions** (time pressure, no external resources)
- Questions should **test application**, not just recall
- Include **specific requirements** (e.g., "Calculate and explain", "Justify your decision")
- Build **progressive complexity** (Task 1 easier than Task 5)

**Task Types by Difficulty:**

**Basic:**
- Definition and identification
- Single calculations
- Direct application of formulas
- "What is...?", "Calculate..."

**Intermediate:**
- Multi-step calculations
- Comparison and analysis
- Application with explanation
- "Compare...", "Analyze the impact of...", "Prepare a..."

**Advanced:**
- Strategic decisions with justification
- Trade-off analysis
- Critical evaluation
- "Recommend...", "Evaluate alternatives...", "Discuss implications..."

### Solution Format

**Always include:**
1. **Complete answer** to the question
2. **Step-by-step explanation** or reasoning
3. **Key concepts** highlighted
4. **Grading notes** (point distribution for instructors)

**For calculations:**
```markdown
**Solution:**

Step 1: Identify given values
- Investment: €50,000
- Annual profit: €10,000

Step 2: Apply ROI formula
ROI = (Profit / Investment) × 100
ROI = (10,000 / 50,000) × 100 = 20%

**Answer:** The ROI is 20%.

**Grading Notes:**
- Correct formula identification (1 point)
- Accurate calculation (2 points)
- Proper interpretation (1 point)
```

## YAML Frontmatter Template

```yaml
---
title: "Case Study: [Title]"
subtitle: "[Topic Area]"
difficulty: "[Basic|Intermediate|Advanced]"
duration: "[15|20|30] minutes"
topics:
  - "[Main Topic]"
  - "[Related Topic]"
learning-objectives:
  - "[Objective 1]"
  - "[Objective 2]"
---
```

## Multiple Case Studies per Topic

When creating multiple case studies for one teaching unit:

1. **Vary difficulty levels** (e.g., 1 Basic, 2 Intermediate, 1 Advanced)
2. **Different contexts** (e.g., manufacturing, retail, services)
3. **Different aspects** of the same concept
4. **Progressive scenarios** (Case 2 builds on Case 1)

**Naming convention:**
- `case-study-[topic]-01-basic.qmd`
- `case-study-[topic]-02-intermediate.qmd`
- `case-study-[topic]-03-advanced.qmd`

## Integration with Quarto Lecture Content

When generating from a .qmd chapter:

1. **Identify key concepts** from the chapter
2. **Check Trinity of Depth:**
   - Theory → Conceptual understanding questions
   - Norms → Standards/rules application
   - Practice → Calculations and procedures
3. **Create scenarios** that integrate multiple concepts
4. **Match difficulty** to chapter complexity

## Language Support

**Automatic Detection:**
- Detect language from user input, .qmd source, or explicit request
- Supported languages: **German** and **English**
- Default: Match the language of the lecture content

**Language Consistency:**
- ALL content must be in the same language: context, tasks, solutions, grading notes
- Use proper business/accounting terminology for that language
  - English: "Accounts Payable", "Inventory", "Depreciation"
  - German: "Verbindlichkeiten", "Vorräte", "Abschreibung"

**YAML Frontmatter Language:**
```yaml
# English
title: "Case Study: Equipment Purchase"
subtitle: "Depreciation Methods"

# German  
title: "Fallstudie: Anschaffung von Anlagen"
subtitle: "Abschreibungsmethoden"
```

**When to use which language:**
- User requests in German → Generate German case study
- User requests in English → Generate English case study
- Based on .qmd chapter → Match chapter language
- Explicit request: "in English" or "auf Deutsch" → Use that language

## Quality Checklist

Before generating output, verify:
- ✅ Realistic, focused storytelling (2-3 paragraphs)
- ✅ Clear difficulty level stated
- ✅ 2-6 tasks depending on difficulty
- ✅ All solutions in `{.content-visible when-meta="show_solutions"}` blocks
- ✅ Grading notes included for each task
- ✅ Proper Quarto YAML frontmatter
- ✅ Exam-appropriate task complexity
- ✅ Step-by-step solutions with explanations

## Example Output Structure

```markdown
---
title: "Case Study: Equipment Purchase Decision"
subtitle: "Depreciation Methods"
difficulty: "Intermediate"
duration: "25 minutes"
topics:
  - "Depreciation"
  - "Asset Valuation"
  - "Financial Statement Impact"
learning-objectives:
  - "Apply different depreciation methods"
  - "Analyze impact on financial statements"
  - "Justify method selection"
---

## Case Study: Equipment Purchase Decision

**Difficulty:** Intermediate | **Topic:** Depreciation Methods | **Duration:** ~25 min

### Context

TechManufacture GmbH, a medium-sized production company in Munich, is considering purchasing new CNC machinery for €150,000. The equipment is expected to have a useful life of 5 years with a residual value of €10,000. The company's CFO, Maria Schmidt, needs to decide between straight-line and declining-balance depreciation methods.

The company is currently profitable (annual EBIT of €500,000) and expects stable revenue growth. Management is concerned about both tax implications and how the depreciation method will affect their financial ratios, as they plan to apply for a bank loan next year.

### Tasks

#### Task 1: Straight-Line Depreciation
Calculate the annual depreciation expense using the straight-line method for the first three years.

::: {.content-visible when-meta="show_solutions"}
**Solution:**

Step 1: Calculate depreciable amount
Depreciable amount = Purchase price - Residual value
Depreciable amount = €150,000 - €10,000 = €140,000

Step 2: Calculate annual depreciation
Annual depreciation = Depreciable amount / Useful life
Annual depreciation = €140,000 / 5 = €28,000

**Answer:** The annual depreciation expense is €28,000 for each of the first three years (and all subsequent years).

**Grading Notes:**
- Correct depreciable amount calculation (1 point)
- Correct formula application (1 point)
- Accurate result (1 point)
:::

#### Task 2: Declining-Balance Comparison
Using a declining-balance rate of 40%, calculate the depreciation expense for the first year and compare it to the straight-line method. What is the difference?

::: {.content-visible when-meta="show_solutions"}
**Solution:**

Step 1: Calculate Year 1 declining-balance depreciation
Depreciation Year 1 = Book value × Rate
Depreciation Year 1 = €150,000 × 40% = €60,000

Step 2: Compare to straight-line
Difference = €60,000 - €28,000 = €32,000

**Answer:** The declining-balance method results in €60,000 depreciation in Year 1, which is €32,000 higher than the straight-line method.

**Grading Notes:**
- Correct declining-balance calculation (2 points)
- Accurate comparison (1 point)
- Interpretation of difference (1 point)
:::

#### Task 3: Impact Analysis
Explain how choosing the declining-balance method instead of straight-line would affect TechManufacture's (a) net income in Year 1 and (b) debt-to-equity ratio when applying for the loan.

::: {.content-visible when-meta="show_solutions"}
**Solution:**

**a) Net Income Impact:**
The declining-balance method results in €32,000 higher depreciation expense in Year 1. This increases expenses, reducing EBIT from €500,000 to €468,000 (assuming all else equal). The higher expense leads to lower net income in Year 1.

**b) Debt-to-Equity Ratio Impact:**
Lower net income reduces retained earnings, which decreases equity. With lower equity in the denominator, the debt-to-equity ratio increases, potentially making the loan application less attractive to the bank.

**Grading Notes:**
- Correct identification of net income decrease (2 points)
- Understanding of expense impact on profitability (1 point)
- Explanation of equity effect (2 points)
- Connection to debt-to-equity ratio (2 points)
- Mention of loan implications (1 point)
:::

#### Task 4: Recommendation
Which depreciation method would you recommend for TechManufacture given their upcoming loan application? Justify your answer with at least two arguments.

::: {.content-visible when-meta="show_solutions"}
**Solution:**

**Recommendation:** Straight-line method

**Arguments:**

1. **Better Financial Ratios:** The straight-line method results in lower depreciation expense in Year 1, leading to higher net income and stronger equity position. This improves the debt-to-equity ratio, making the company more attractive to lenders.

2. **Income Stability:** Straight-line depreciation provides consistent expenses across years, demonstrating stable profitability. Banks prefer predictable financial performance when evaluating loan applications.

Alternative argument: The declining-balance method could be justified if tax benefits (lower taxable income in early years) outweigh the negative impact on financial ratios, but this depends on the company's tax situation and the bank's specific requirements.

**Grading Notes:**
- Clear recommendation (1 point)
- First valid argument with explanation (2 points)
- Second valid argument with explanation (2 points)
- Connection to specific case context (2 points)
- Consideration of trade-offs (bonus: 1 point)
:::

### Reflection

Consider TechManufacture's long-term strategy: If the company plans to purchase similar equipment every 2-3 years, how might this affect the depreciation method decision?

::: {.content-visible when-meta="show_solutions"}
**Discussion Points:**
- Continuous equipment purchases could smooth out the declining-balance effect over time
- Consistency in accounting methods improves comparability across periods
- Tax strategy considerations for growing vs. stable companies
- Industry norms and stakeholder expectations
:::
```

## Remember

- **Realistic but focused** storytelling
- **Exam-level** task difficulty
- **Complete solutions** with grading notes
- **Proper Quarto syntax** with content-visible blocks
- **Progressive complexity** in task sequence
- **Language consistency** throughout (German OR English, not mixed)

Create case studies that prepare students for real-world application while being assessable in exam conditions.

## Language Examples

**English Structure:**
```markdown
### Context
TechCorp purchased...

### Tasks
#### Task 1: Calculate Depreciation
Calculate the annual depreciation...

::: {.content-visible when-meta="show_solutions"}
**Solution:**
Step 1: Identify values...
:::
```

**German Structure:**
```markdown
### Kontext
Die TechCorp GmbH hat...

### Aufgaben
#### Aufgabe 1: Abschreibung berechnen
Berechnen Sie die jährliche Abschreibung...

::: {.content-visible when-meta="show_solutions"}
**Lösung:**
Schritt 1: Werte identifizieren...
:::
```