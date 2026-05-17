# 05 — Defects

Store all defect reports logged during execution here.

## What goes here:
- Defect reports from `/07-report-bug` → `bug-[NNN]-[short-title].md`
- Retest notes (add to the original bug file)

## Naming convention:
`bug-[NNN]-[short-title].md`
Example: `bug-042-login-submit-unresponsive-empty-password.md`

## Defect lifecycle status:
New → In Progress → Fixed → Retest → Closed / Reopened

## Severity reference:
| Severity | Definition |
|---|---|
| Critical | Crash, data loss, security breach, feature completely down |
| High | Core function broken, no workaround |
| Medium | Partial break, workaround exists |
| Low | Cosmetic, typo, minor UX |

## Next step:
After fix is deployed → retest and update bug file status to Closed or Reopened.
