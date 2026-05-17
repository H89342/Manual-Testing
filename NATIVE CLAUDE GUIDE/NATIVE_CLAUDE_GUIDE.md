# Using This Workflow in the Native Claude.ai App

Claude.ai cannot read the `.claude/` folder directly.
The equivalent feature is **Claude.ai Projects**.

```
Claude.ai → Projects → Create Project
         → Add files (upload your SKILL.md / templates)
         → Set instructions (reference the skills by name)
```

---

## Step 1 — Create a Project in Claude.ai

1. Go to [claude.ai](https://claude.ai) → **Projects** → **New Project**
2. Name it to match your project, e.g. `Manual Testing — Telemax`

---

## Step 2 — Upload skill files to the Project knowledge

Upload these files from the repo:

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

Inside the Project → **Edit project instructions** → paste:

```
You are an expert SDET assistant for this project.

Follow these skills when invoked:
- "intro" or "tester intro"       → follow tester-intro skill
- "analyze this requirement"      → follow analyze-requirements skill
- "review test cases"             → follow review-test-cases skill
- "execute tests"                 → follow execute-tests skill

When creating test cases, apply TESTCASE_RULES_SHARED always,
plus TESTCASE_RULES_UI for UI tests and TESTCASE_RULES_API for API tests.

When starting a new requirement, always use req-template.md as the structure.

Always follow the SDET workflow in order:
read requirement → analyze → Q&A → create test cases → review → execute → report bug → automate
```

---

## Step 4 — Invoke by natural language (no slash commands)

| Claude Code command | Claude.ai equivalent phrase |
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

Claude.ai cannot write files to your computer.
After each step, **copy the output from chat** and save it in the correct workflow folder:

| Step | Save to |
|---|---|
| Requirement intake | `.claude/workflows/01-requirements/[project]/req-[feature]_v1.md` |
| Analysis + Q&A | `.claude/workflows/02-analysis/[project]/` |
| Test cases + review | `.claude/workflows/03-test-cases/[project]/` |
| Execution log | `.claude/workflows/04-execution/[project]/` |
| Defect reports | `.claude/workflows/05-defects/[project]/` |
| Summary report | `.claude/workflows/06-reports/[project]/` |
| Automation scripts | `.claude/workflows/07-automation/[framework]/` |
