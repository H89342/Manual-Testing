# 07 — Automation Scripts

Store automation scripts converted from manual test cases here.

## What goes here:
- Automation scripts from `/08-automate`
- Organized by framework

## Folder structure:
```
07-automation/
├── playwright/       ← TypeScript/JavaScript Playwright tests
├── selenium/         ← Java/Python Selenium tests
├── pytest/           ← Python pytest (API or UI)
├── cypress/          ← JavaScript Cypress tests
└── postman/          ← Postman collections (JSON export)
```

## Naming convention:
`test_[feature]_[scenario].[ext]`
Example: `test_login_valid_credentials.spec.ts`

## Rules before committing a script here:
- Script must be linked to its manual TC ID in a comment: `// TC-NNN`
- Script must pass locally before being saved here
- Test data must be externalized (no hardcoded credentials or magic values)
- Locators must use stable selectors (data-testid, aria-label, ID — not positional XPath)
