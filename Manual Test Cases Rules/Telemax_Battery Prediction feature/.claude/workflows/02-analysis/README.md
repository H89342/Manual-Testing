# 02 — Analysis & Q&A (Reference Only)

> **This folder does not store artifacts.**
> Analysis and Q&A files save directly inside the project folder, per `CLAUDE.md` save rule.

---

## Where artifacts are saved

| Artifact | Save to |
|---|---|
| Requirement analysis | `[Project-Folder]/analysis-[feature]_v1.md` |
| Q&A checklist | `[Project-Folder]/qa-[feature]_v1.md` |

**Examples:**
```
Telemax/analysis-battery-prediction_v1.md
Telemax/qa-battery-prediction_v1.md
```

---

## Naming convention

| File | Format |
|---|---|
| Analysis | `analysis-[feature-name]_v[N].md` |
| Q&A | `qa-[feature-name]_v[N].md` |

Version starts at `v1`. Increment when requirements change significantly after answers are received.

---

## Status line — add at top of every Q&A file

```
**Status:** OPEN | IN REVIEW | RESOLVED
```

- `OPEN` — questions sent, waiting for answers
- `IN REVIEW` — answers received, being validated
- `RESOLVED` — all CRITICAL questions answered, ready to write test cases

---

## Next step

When all CRITICAL Q&A questions are resolved → run `/04-create-tc`
