# 01 — Requirements

This folder is the entry point of the SDET workflow. Every feature you test must start here before any analysis or test case is written.

---

## Folder structure

```
01-requirements/
├── README.md
├── req-template.md              ← MASTER TEMPLATE — never edit directly
├── [project-name]/              ← one subfolder per project
│   ├── req-[feature]_v1.md
│   ├── req-[feature]_v2.md
│   └── brd-[feature].md
└── [another-project]/
    └── req-[feature]_v1.md
```

> **Rule:** Every project gets its own subfolder. Copy `req-template.md` into the project subfolder — never edit the master template directly.

---

## How to start a new requirement

```
1. Create a subfolder:  01-requirements/[your-project-name]/
2. Copy the template:   req-template.md  →  [project-name]/req-[feature]_v1.md
3. Fill in the copy — never touch req-template.md
4. Run /01-read-requirements  (AI-assisted intake review)
5. Run /02-analyze            (deep analysis)
6. Run /03-qa                 (Q&A checklist)
```

---

## Naming convention

```
[project-name]/req-[feature-name]_v[N].md
```

| Part | Description | Example |
|---|---|---|
| `[project-name]/` | project subfolder | `telemax/`, `omrom/` |
| `req-` | file prefix | `req-` |
| `[feature-name]` | kebab-case short name | `user-login`, `payment-checkout` |
| `_v[N]` | version, starts at v1 | `_v1`, `_v2` |

**Examples:**
- `telemax/req-user-login_v1.md`
- `telemax/req-user-login_v2.md`  ← updated after Q&A feedback
- `omrom/req-payment-checkout_v1.md`

---

## Requirement version rules

- Start at `v1` for every new feature
- Create a new version (`v2`, `v3`) when:
  - Acceptance criteria change after Q&A
  - Scope is added or removed mid-cycle
  - Stakeholder changes the requirement after test cases are drafted
- **Never overwrite** an existing version — always create a new file
- Add a `## Change Log` entry to each new version explaining what changed and why

---

## Status tracking

Add this line at the top of every intake file:

```
**Status:** Draft | In Review | Confirmed | Superseded by v[N]
```

---

## File types

| File prefix | Purpose |
|---|---|
| `req-[feature]_vN.md` | Requirement intake (filled from template) |
| `brd-[feature].md` | Raw BRD / spec paste — unedited source |
| `ux-[feature].md` | UX notes, screen names, Figma references |
