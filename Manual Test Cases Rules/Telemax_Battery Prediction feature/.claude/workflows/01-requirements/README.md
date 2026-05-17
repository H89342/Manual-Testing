# 01 — Requirements

> **Artifacts do not store here.**
> Filled requirement files save directly inside the project folder, per `CLAUDE.md` save rule.
> Exception: `req-template.md` stays here permanently as the master template — never edit it directly.

---

## Where artifacts are saved

| Artifact | Save to |
|---|---|
| Requirement intake (filled) | `[Project-Folder]/req-[feature]_v1.md` |
| Updated version | `[Project-Folder]/req-[feature]_v2.md` |
| Raw BRD / spec paste | `[Project-Folder]/brd-[feature].md` |
| UX / Figma notes | `[Project-Folder]/ux-[feature].md` |

**Examples:**
```
Telemax/req-battery-prediction_v1.md
Telemax/req-battery-prediction_v2.md
Telemax/brd-battery-prediction.md
```

---

## What stays in this folder (tooling only)

| File | Purpose |
|---|---|
| `req-template.md` | Master template — copy to project folder, never edit here |
| `README.md` | This file |

---

## How to start a new requirement

```
1. Copy req-template.md → [Project-Folder]/req-[feature]_v1.md
2. Fill in your copy — never touch the master template
3. Run /01-read-requirements  (AI-assisted intake review)
4. Run /02-analyze            (deep analysis)
5. Run /03-qa                 (Q&A checklist)
```

---

## Naming convention

| Part | Rule | Example |
|---|---|---|
| `req-` | file prefix | `req-` |
| `[feature-name]` | kebab-case | `battery-prediction`, `user-login` |
| `_v[N]` | version from v1 | `_v1`, `_v2` |

---

## Version rules

- Start at `v1` for every new feature
- Create a new version (`v2`, `v3`) when requirements change after Q&A or after test cases are drafted
- Never overwrite an existing version — always create a new file
- Add a `## Change Log` entry to each new version

---

## Status line — add at top of every intake file

```
**Status:** Draft | In Review | Confirmed | Superseded by v[N]
```
