# Using This Workflow in the Native Claude.ai App

> Claude.ai cannot read the `.claude/` folder directly.
> The equivalent feature is **Claude.ai Projects**.

```
Claude.ai → Projects → Create Project
         → Add files (upload your SKILL.md / templates)
         → Set instructions (reference the skills by name)
```

---

## What you copy vs. what you just read

| Section | Action |
|---|---|
| Introduction (this page) | Read only — no copy needed |
| Step 1 — Create Project | Do in Claude.ai UI |
| Step 2 — Upload files | Do in Claude.ai UI |
| **Step 3 — Project Instructions** | **Copy the code block → paste into Claude.ai** |
| Step 4 — Natural language table | Your cheat sheet when chatting — do not copy into Claude.ai |
| Saving outputs | Your reminder for file naming — do not copy into Claude.ai |

---

## Step 1 — Create a Project in Claude.ai

> **Action: do in Claude.ai UI**

1. Go to [claude.ai](https://claude.ai) → **Projects** → **New Project**
2. Name it to match your project, e.g. `Manual Testing — Telemax`

---

## Step 2 — Upload skill files to the Project knowledge

> **Action: upload these files from the repo into Claude.ai Project knowledge**

```
.claude/skills/tester-intro/SKILL.md
.claude/skills/analyze-requirements/SKILL.md
.claude/skills/review-test-cases/SKILL.md
.claude/skills/execute-tests/SKILL.md
.claude/workflows/01-requirements/req-template.md
.claude/workflows/03-test-cases/TESTCASE_RULES_SHARED.md
.claude/workflows/03-test-cases/TESTCASE_RULES_UI.md
.claude/workflows/03-test-cases/TESTCASE_RULES_API.md
```

> Re-upload any file when it is updated in the repo.

---

## Step 3 — Set the Project Instructions

> **Action: copy the block below → paste into Claude.ai → Edit project instructions**
>
> This is the only block you paste into Claude.ai. Steps 4 and the saving outputs section are for your own reference — they do not go here.

```
You are an expert SDET assistant for this project.

## Role
Act as a senior SDET engineer. Apply quality-first thinking, risk-based
prioritisation, and strict traceability to requirements at all times.

## Skills — follow when invoked
- "intro" or "tester intro"        → follow tester-intro skill
- "analyze this requirement"       → follow analyze-requirements skill
- "review test cases"              → follow review-test-cases skill
- "execute tests"                  → follow execute-tests skill

## Test case rules — apply automatically
- Always apply TESTCASE_RULES_SHARED to every test case
- Apply TESTCASE_RULES_UI for UI / web test cases
- Apply TESTCASE_RULES_API for API test cases

## Requirement intake
When starting a new requirement, always use req-template.md as the structure.

## Workflow order — never skip or reorder steps
1. Read & intake the requirement
2. Analyze the requirement
3. Generate Q&A checklist — resolve all CRITICAL questions before step 4
4. Create test cases
5. Review test cases
6. Execute tests
7. Report bugs
8. Convert to automation script
```

---

## Step 4 — Your cheat sheet when chatting

> **For your reference only — do not copy into Claude.ai**
> Use these phrases when chatting inside the Project instead of slash commands.

| Claude Code command | Say this in Claude.ai chat |
|---|---|
| `/01-read-requirements` | `"Read this requirement and give me an intake summary"` |
| `/02-analyze` | `"Analyze this requirement"` |
| `/03-qa` | `"Generate a Q&A checklist"` |
| `/04-create-tc` | `"Create test cases for this feature"` |
| `/05-review-tc` | `"Review these test cases"` |
| `/06-execute` | `"Guide me through test execution"` |
| `/07-report-bug` | `"Help me log this defect"` |
| `/08-automate` | `"Convert this test case to a [framework] script"` |

---

## Saving outputs

> **For your reference only — do not copy into Claude.ai**
> Claude.ai cannot write files to your computer. After each step, copy the output from chat and save it locally.

| Step | Save to |
|---|---|
| Requirement intake | `.claude/workflows/01-requirements/[project]/req-[feature]_v1.md` |
| Analysis + Q&A | `.claude/workflows/02-analysis/[project]/` |
| Test cases + review | `.claude/workflows/03-test-cases/[project]/` |
| Execution log | `.claude/workflows/04-execution/[project]/` |
| Defect reports | `.claude/workflows/05-defects/[project]/` |
| Summary report | `.claude/workflows/06-reports/[project]/` |
| Automation scripts | `.claude/workflows/07-automation/[framework]/` |
