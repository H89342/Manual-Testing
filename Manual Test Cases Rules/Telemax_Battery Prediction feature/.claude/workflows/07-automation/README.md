# 07 — Automation (Reference Only)

> **This folder does not store automation scripts.**
> Automation scripts save directly inside the project folder, per `CLAUDE.md` save rule.

---

## Where artifacts are saved

| Artifact | Save to |
|---|---|
| UI automation script | `[Project-Folder]/auto_[module]_[scenario].[ext]` |
| API automation (Postman JSON) | `[Project-Folder]/postman_[module]_v[N].json` |

**Examples:**
```
Telemax/auto_battery-prediction_level-updates-on-charge.spec.ts
Telemax/auto_battery-prediction_null-offline-state.spec.ts
Telemax/postman_battery-prediction-api_v1.json
```

---

## Naming convention

| File type | Format | Extension |
|---|---|---|
| Playwright | `auto_[module]_[scenario].spec.ts` | `.spec.ts` |
| Cypress | `auto_[module]_[scenario].cy.js` | `.cy.js` |
| pytest | `auto_[module]_[scenario].py` | `.py` |
| Selenium (Java) | `Auto[Module][Scenario].java` | `.java` |
| Postman | `postman_[module]_v[N].json` | `.json` |

---

## Rules before saving a script

- [ ] Script is linked to its manual TC ID in a comment: `// BATTERY-001`
- [ ] Script passes locally before saving
- [ ] Test data is externalized — no hardcoded credentials or magic values
- [ ] Locators use stable selectors: `data-testid` > `aria-label` > `ID` > CSS (no positional XPath)
- [ ] Test is independent — no dependency on execution order
- [ ] Update the TC record: change `Automation Candidate: Yes` → `Automated`

---

## Trigger

Run `/08-automate` to convert an approved, passing manual TC to an automation script.
Only automate TCs with `Status: PASS` and `Automation Candidate: Yes`.
