# Step 1 — Read Requirements

You are acting as an expert SDET. Follow these steps exactly.

---

## Step 1A: Identify the project

Ask the user:
> "Which project folder are you working in? (e.g. Telemax, Test case omrom)"

Use the exact folder name as `[Project-Folder]` for the rest of this command.
All artifacts are saved flat inside that folder at the repo root — not inside `.claude/`.

---

## Step 1B: Confirm the project folder exists

Check if `[Project-Folder]/` exists at the repo root.
- If it does not exist → tell the user:
  > "The folder `[Project-Folder]/` does not exist at the project root. Please create it first."
- If it exists → confirm:
  > "Saving all artifacts to: `[Project-Folder]/`"

---

## Step 1C: Ask for the requirement

Ask the user to paste or describe the requirement (user story, BRD excerpt, acceptance criteria, or screen description).

---

## Step 1D: Produce the intake summary

Read and parse the requirement carefully. Then produce a structured intake summary:

```
## Requirement Intake Summary
**Project:** [project-name]
**Feature Name:** [name]
**File to create:** [Project-Folder]/req-[feature-name]_v1.md
**Source:** [BRD section / User Story ID / Screen name]
**Date:** [today]
**Status:** Draft

### What is being built:
[1–2 sentences plain English — no jargon]

### Primary Users:
[list roles/personas]

### Business Goal:
[1 sentence — what problem does this solve?]

### Key Screens / Flows Referenced:
[list any mentioned screens, flows, diagrams, sections]

### Does this affect existing features?
[ ] Yes — [describe]
[ ] No

### Initial Observations & Risks:
[anything immediately unclear, missing, ambiguous, or risky — flag it here]
[If nothing — write "None at this stage"]
```

---

## Step 1E: Save the file

Tell the user:
> "Save your completed intake as:
> `[Project-Folder]/req-[feature-name]_v1.md`
>
> Copy `.claude/workflows/01-requirements/req-template.md` as the base — do not edit the master template."

---

## Step 1F: Handoff

Tell the user:
> "Intake complete. Run `/02-analyze` to proceed with deep requirement analysis."
