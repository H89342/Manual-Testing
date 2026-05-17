# CLAUDE.md — Project-Level Rules

## Reading order
Claude Code loads CLAUDE.md files from the **root down to the current folder**.
Each folder can have its own CLAUDE.md that **extends** — never replaces — this file.

```
Manual-Testing/CLAUDE.md                                  ← loaded first (always)
Manual-Testing/Manual Test Cases Rules/.../CLAUDE.md      ← loaded second (when working in that folder)
```

Rules in a subfolder CLAUDE.md add feature-specific context.
If a subfolder rule conflicts with a root rule, the subfolder rule takes precedence for that folder only.

---

## Output Format Rule — Apply automatically, never wait to be asked

### UI Test Cases
Always produce **two outputs** when writing UI test cases:

1. **Markdown** — full test case format per `TESTCASE_RULES_SHARED.md` and `TESTCASE_RULES_UI.md`
2. **Excel-ready table** — columns in the exact order from `TESTCASE_RULES_SHARED.md §2 (Excel Export Column Order)`:

   `TC ID | Screen/Section | Requirement Summary | Title | Preconditions | Steps (Action) | Expected Result | Test Data | Postconditions | Status | Priority | Type | Environment | Notes`

   Label it clearly: `### Excel Export — copy and paste into Excel`

   Always include a **Clarify Requirements** table for any PENDING TCs, per `TESTCASE_RULES_UI.md §3` and `TESTCASE_RULES_SHARED.md §13`.

### API Test Cases
Always produce **Postman Collection JSON** alongside the markdown TC, per `TESTCASE_RULES_API.md §12`.
Never output API TCs in Excel format — Postman is the primary export.

---

## Workflow Order — Always enforce this sequence
1. Read & intake requirement → `/01-read-requirements`
2. Analyze requirement → `/02-analyze`
3. Generate Q&A — resolve all CRITICAL questions before step 4 → `/03-qa`
4. Create test cases → `/04-create-tc`
5. Review test cases → `/05-review-tc`
6. Execute tests (when requested) → `/06-execute`
7. Report bugs (when requested) → `/07-report-bug`
8. Convert to automation (when requested) → `/08-automate`

---

## Save Location
All artifacts save flat inside the project folder at the repo root.
- `Telemax/` for Telemax project
- `Test case omrom/` for Omrom project
- Never save inside `.claude/` — that folder is tooling only.
