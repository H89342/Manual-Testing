# 06 — Reports (Reference Only)

> **This folder does not store report files.**
> Test execution summary reports save directly inside the project folder, per `CLAUDE.md` save rule.

---

## Where artifacts are saved

| Artifact | Save to |
|---|---|
| Test Execution Summary Report | `[Project-Folder]/report-[feature]_[YYYY-MM-DD].md` |

**Examples:**
```
Telemax/report-battery-prediction_2026-05-17.md
```

---

## Naming convention

```
report-[feature-name]_[YYYY-MM-DD].md
```

---

## Minimum content per report

Per `TESTCASE_RULES_SHARED.md §12`:

- Build version and environment tested
- Execution Summary table (Status Counts, Derived Metrics, Priority Breakdown)
- Defect summary by severity (Open / Fixed & Retested / Deferred)
- Outstanding risks and blocked TCs
- Sign-off recommendation: `PASS` / `CONDITIONAL PASS` / `FAIL`
- Sign-off: Tester name and date

---

## Sign-off recommendation guide

| Verdict | Condition |
|---|---|
| `PASS` | All Critical/High defects resolved. Ready to release. |
| `CONDITIONAL PASS` | Known risks accepted by named stakeholder. Proceed with monitoring. |
| `FAIL` | Critical/High defects unresolved. Do not release. |

---

## Trigger

Produced at the end of every `/06-execute` cycle.
