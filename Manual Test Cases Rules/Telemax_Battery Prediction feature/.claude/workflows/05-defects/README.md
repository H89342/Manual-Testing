# 05 — Defects (Reference Only)

> **This folder does not store defect reports.**
> Bug files save directly inside the project folder, per `CLAUDE.md` save rule.

---

## Where artifacts are saved

| Artifact | Save to |
|---|---|
| Defect report | `[Project-Folder]/bug-[NNN]-[short-title].md` |

**Examples:**
```
Telemax/bug-001-battery-level-not-updating.md
Telemax/bug-002-prediction-returns-null-offline.md
```

---

## Naming convention

```
bug-[NNN]-[short-title].md
```

| Part | Rule | Example |
|---|---|---|
| `bug-` | prefix | `bug-` |
| `[NNN]` | 3-digit sequential ID | `001`, `042` |
| `[short-title]` | kebab-case description | `login-submit-unresponsive` |

Never reuse a bug ID — deleted bugs leave a gap.

---

## Defect lifecycle

`New` → `In Progress` → `Fixed` → `Retest` → `Closed` / `Reopened`

---

## Severity reference

| Severity | Definition |
|---|---|
| Critical | Crash, data loss, security breach, feature completely down |
| High | Core function broken, no workaround |
| Medium | Partial break, workaround exists |
| Low | Cosmetic, typo, minor UX |

---

## Trigger

Run `/07-report-bug` when a test case FAILs during execution.
After fix is deployed → retest and update the bug file status to `Closed` or `Reopened`.
