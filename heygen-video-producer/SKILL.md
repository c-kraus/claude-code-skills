---
name: heygen-video-producer
description: "Produce HeyGen avatar videos (intro + outro) for a Quarto lecture chapter (.qmd). Use when the user requests intro/outro videos for a QMD chapter, wants to produce lecture videos, mentions HeyGen, or asks to add video bookends to a Quarto lecture. Trigger phrases: 'Erstelle ein Intro-Video für mein QMD', 'Produziere die Videos für meine Vorlesung', 'heygen intro', 'Intro und Outro für das Kapitel', 'produce lecture videos', 'add video bookends'."
---

# HeyGen Video Producer

## Identity & Mission

Given a Quarto lecture chapter (`.qmd`), produce two avatar videos via the HeyGen MCP:

1. **Intro** (~45–60 sec): Hook-first entry into the topic.
2. **Outro** (~45–60 sec): Synthesizing close with transfer impulse.

Both scripts are generated inline by Claude — no separate API calls. Videos are produced via `mcp__HeyGen__generate_avatar_video` and polled until complete.

## Defaults

```yaml
avatar_id: 1b929830392742439cfcd67fe7f7a79c
voice_id:  578c2318ebde4d989005f2e439d2c2be
```

These are the professor's own avatar and cloned voice. Override only if the user explicitly provides different values.

The HeyGen API key is NOT needed at runtime — it lives in the MCP server config (see `references/setup.md`).

## Input

The user provides a path to a `.qmd` file. If the path is ambiguous (relative, `~`, or no path given), resolve it:
- Check if a `.qmd` is currently open in the editor
- Ask the user to confirm or provide the full path

From the `.qmd`, extract:
1. **YAML frontmatter** — `title`, `description` (if present)
2. **First 500 chars of body** (after frontmatter) — for Intro
3. **Last section / last 800 chars of body** — for Outro synthesis
4. **Slug** — derived from the filename without extension, e.g. `kap-03-kostenrechnung`

## Script Generation Rules

### Shared Rules
- Language: German (default) or English — match the QMD's `lang` field or the user's prompt language
- Tone: **Smart Casual Academic** — precise, slightly ironic, no bureaucratic language, no passive-heavy academese
- Length: **exactly 110–130 words** per script (≈ 45–60 sec at normal speaking pace)
- Address form: **"Sie"** (unless the user specifies otherwise or the QMD uses "ihr")
- No filler phrases, no hedging, no "um", no nested clauses that a human would stumble over when reading aloud
- Write for the ear, not the eye: short sentences, natural rhythm, spoken German/English

### Intro Script Rules
- **Hook-first dramaturgy**: open with a concrete scenario, paradox, counterintuitive fact, or provocative question
- **NEVER start with**: "Herzlich willkommen", "In dieser Vorlesung lernen Sie", "Heute werden wir", "Welcome", "In this lecture"
- The hook must be derived from the actual content — no generic openers
- End with a sentence that creates forward momentum: what problem will be solved, what tension will be resolved

### Outro Script Rules
- **Not a summary** — no "Wir haben heute gelernt, dass..." or "As we have seen..."
- Focus on **meaning and transfer**: what does this material *mean* for practice, for the profession, for the student's future role?
- End with a **concrete transfer impulse** (a task, a real-world observation to make) or an **open follow-up question** that bridges to the next chapter

## Workflow

### Step 1 — Parse QMD

Read the file. Extract title, slug, first-500-chars body, last-800-chars body.

### Step 2 — Generate Scripts

Write both scripts following the rules above. Show them to the user in a code block before proceeding:

```
--- INTRO SCRIPT (word count: NNN) ---
[script text]

--- OUTRO SCRIPT (word count: NNN) ---
[script text]
```

Ask: **"Scripts look good? I'll proceed to produce the videos — or adjust before submitting."**

Wait for explicit confirmation (or a correction). Do not submit to HeyGen without approval.

### Step 3 — Prepare Output Directory

Ensure `assets/videos/` exists in the same directory as the `.qmd`:

```
[qmd-dir]/assets/videos/
```

Save both scripts as plain text files:
- `[qmd-dir]/assets/videos/[slug]-intro.txt`
- `[qmd-dir]/assets/videos/[slug]-outro.txt`

### Step 4 — Submit Videos to HeyGen

Submit intro first, then outro. Use `mcp__HeyGen__generate_avatar_video`:

```
avatar_id: 1b929830392742439cfcd67fe7f7a79c
voice_id:  578c2318ebde4d989005f2e439d2c2be
input_text: [script]
title: [slug]-intro   (or -outro)
```

Note both returned `video_id` values.

### Step 5 — Poll for Completion

Poll each video using `mcp__HeyGen__get_avatar_video_status`:
- Interval: **every 15 seconds**
- Timeout: **20 minutes** (80 polls)
- Poll both videos concurrently (interleave polls, don't wait for one to finish before polling the other)
- Print a one-line status update on each poll: `[slug]-intro: processing... (elapsed: Xs)`

On status `completed`: note the `video_url` from the response.
On status `failed`: report the error immediately and stop.
On timeout: report that the video is still processing and provide the HeyGen dashboard URL for manual download: `https://app.heygen.com/home`

### Step 6 — Download MP4s

For each completed video, download via HTTP GET on the `video_url` and save to:
- `[qmd-dir]/assets/videos/[slug]-intro.mp4`
- `[qmd-dir]/assets/videos/[slug]-outro.mp4`

Use the Bash tool: `curl -L -o "[output-path]" "[video_url]"`

### Step 7 — Report Output

Print a clean summary:

```
Videos produced:
  assets/videos/[slug]-intro.mp4
  assets/videos/[slug]-outro.mp4

Scripts saved:
  assets/videos/[slug]-intro.txt
  assets/videos/[slug]-outro.txt

Quarto shortcodes — copy into your .qmd:

  Intro (place before chapter body):
  ::: {.video}
  {{< video assets/videos/[slug]-intro.mp4 >}}
  :::

  Outro (place after chapter body):
  ::: {.video}
  {{< video assets/videos/[slug]-outro.mp4 >}}
  :::
```

## Interface for Orchestration (online-lecture-adapter)

When called by the `online-lecture-adapter` skill, this skill:
- **Input**: receives the absolute path to the `.qmd` file as the first argument
- **Behavior**: runs the full workflow non-interactively (skips confirmation in Step 2 when called with `--no-confirm` flag or when the orchestrator passes pre-approved scripts)
- **Output**: returns the absolute paths of the two produced MP4 files

```
[qmd-dir]/assets/videos/[slug]-intro.mp4
[qmd-dir]/assets/videos/[slug]-outro.mp4
```

The orchestrator can use these paths to insert the Quarto shortcodes into the `.qmd` programmatically.

## Error Handling

| Situation | Action |
|---|---|
| HeyGen MCP not configured | Stop. Point to `references/setup.md`. |
| QMD file not found | Ask user to confirm path. |
| Script word count outside 110–130 | Revise before showing to user. |
| Video status `failed` | Report HeyGen error message. Offer to resubmit. |
| Poll timeout (20 min) | Report video IDs. User can check `https://app.heygen.com/home`. |
| Download fails | Report URL. User can download manually. |

## Prerequisites

- HeyGen MCP server configured in `~/.claude/claude.json` (see `references/setup.md`)
- `uv` installed (`brew install uv` on macOS)
- Active HeyGen account with sufficient credits (`mcp__HeyGen__get_remaining_credits` to check)
