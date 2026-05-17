# 01 — Requirements

This folder is the entry point of the SDET workflow. Every feature you test must start here before any analysis or test case is written.

---

## What goes here

| File type | Description |
|---|---|
| `req-[feature]_v1.md` | Requirement intake filled from the template |
| `req-[feature]_v2.md` | Updated intake when requirement changes after v1 |
| `brd-[feature].md` | Pasted BRD or spec excerpt (raw, unedited) |
| `ux-[feature].md` | UX/design notes, screen names, flow references |

> **Rule:** Never write test cases without a completed intake file in this folder.

---

## Naming convention

```
req-[feature-name]_v[N].md
```

| Part | Description | Example |
|---|---|---|
| `req-` | prefix — always required | `req-` |
| `[feature-name]` | kebab-case short name | `user-login`, `payment-checkout` |
| `_v[N]` | version, starts at v1 | `_v1`, `_v2` |

**Examples:**
- `req-user-login_v1.md`
- `req-payment-checkout_v2.md`
- `brd-user-login.md`

---

## Folder structure (when multiple features in progress)

```
01-requirements/
├── README.md
├── req-template.md              ← copy this for every new feature
├── req-user-login_v1.md
├── req-user-login_v2.md         ← updated after Q&A feedback
├── req-payment-checkout_v1.md
└── brd-payment-checkout.md      ← raw BRD paste for reference
```

---

## Requirement version rules

- Start at `v1` for every new feature
- Create a new version (`v2`, `v3`) when:
  - Acceptance criteria change after Q&A
  - Scope is added or removed mid-cycle
  - Stakeholder changes the requirement after test cases are drafted
- **Never overwrite** an existing version — always create a new file
- Add a `## Change Log` section to each new version explaining what changed and why

---

## Status tracking

Add this status line at the top of every intake file:

```
**Status:** Draft | In Review | Confirmed | Superseded by v[N]
```

---

## Workflow

```
Receive requirement
       ↓
Copy req-template.md → fill it in
       ↓
Run /01-read-requirements   (AI-assisted intake summary)
       ↓
Save completed file here as req-[feature]_v1.md
       ↓
Run /02-analyze             (deep analysis)
       ↓
Run /03-qa                  (Q&A checklist)
```

---

## Next step

Once intake is complete → run `/02-analyze`
