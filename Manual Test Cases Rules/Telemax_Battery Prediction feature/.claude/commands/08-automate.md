# Step 8 — Convert to Automation Script

You are acting as an expert SDET converting a verified manual test case into an automation script. Only automate test cases that have PASSED manual execution and are marked as "Automation Candidate: Yes".

## Pre-condition check:
- Confirm the test case has passed manual execution
- Confirm the test case is stable and repeatable
- Confirm the automation framework and language for this project

## Your job in this step:

### 1. Identify the automation framework
Ask the user (or infer from project context):
- Web UI: Playwright / Selenium / Cypress / WebdriverIO
- Mobile: Appium / Espresso / XCTest
- API: RestAssured / Postman/Newman / pytest + requests / Karate
- Unit: JUnit / pytest / Jest

### 2. Map manual test case to automation structure

For each manual step, identify:
- **Locator strategy** (for UI): ID > data-testid > aria-label > CSS > XPath (prefer stable, not positional)
- **Assertion type**: exact match / contains / status code / schema validation
- **Test data handling**: hardcoded / parameterized / fixture / factory

### 3. Write the automation script following these rules:
- Use Page Object Model (POM) for UI tests — separate locators from test logic
- One test = one scenario (no chaining unrelated assertions)
- Use descriptive test names matching the original test case title
- Parameterize test data — no magic strings in test body
- Include setup (beforeEach/fixture) and teardown (afterEach) explicitly
- Add a comment linking back to the manual test case ID: `// TC-NNN`

### 4. Script template by framework:

#### Playwright (TypeScript)
```typescript
// TC-NNN: [Test case title]
// Requirement: REQ-NNN
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test.describe('[Feature Name]', () => {
  test('[test case title]', async ({ page }) => {
    const loginPage = new LoginPage(page);
    // Arrange
    await loginPage.navigate();
    // Act
    await loginPage.enterCredentials('[email]', '[password]');
    await loginPage.submit();
    // Assert
    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByText('Welcome')).toBeVisible();
  });
});
```

#### pytest (Python)
```python
# TC-NNN: [Test case title]
# Requirement: REQ-NNN
import pytest

def test_[feature]_[scenario](setup_fixture):
    # Arrange
    # Act
    # Assert
    assert actual == expected
```

#### REST API (pytest + requests)
```python
# TC-NNN: [Test case title]
# Requirement: REQ-NNN
def test_[endpoint]_[scenario](api_client):
    response = api_client.post('/endpoint', json={...})
    assert response.status_code == 200
    assert response.json()['field'] == 'expected_value'
```

### 5. Automation checklist before committing:
- [ ] Script linked to manual TC ID in comment
- [ ] Locators use stable attributes (not positional XPath)
- [ ] Test data externalized (not hardcoded in test body)
- [ ] Assertions are specific (not just "element exists")
- [ ] Test is independent (no dependency on execution order)
- [ ] Script runs green locally before pushing to CI

### 6. Save automation script to: `[Project-Folder]/auto_[feature]_[scenario].[ext]`

### 7. Update the test case record:
- Change "Automation Candidate" → "Automated"
- Add: "Automation Script: `[Project-Folder]/auto_[feature]_[scenario].[ext]`"
