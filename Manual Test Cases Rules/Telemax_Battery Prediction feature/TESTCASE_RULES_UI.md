# TESTCASE_RULES_UI.md
> UI / Mobile test case rules — templates, examples, and Excel export conventions.
> **Read `TESTCASE_RULES_SHARED.md` first.** This file adds UI/mobile-specific content only.

---

## Table of Contents

1. [Blank Test Case Template](#1-blank-test-case-template)
2. [Full Example Test Case](#2-full-example-test-case)
3. [UI-Specific Checklist Additions](#3-ui-specific-checklist-additions)
4. [Mobile-Specific Writing Notes](#4-mobile-specific-writing-notes)

---

## 1. Blank Test Case Template

> Copy this block in full every time you write a new UI or mobile test case.
> Replace all `[placeholder]` text. Never delete a field — write N/A only if truly not applicable.

```markdown
### ModuleName-NNN: [Verify the expected result of — what is being tested]

**Priority:** High | Medium | Low
**Type:** Functional | Negative | Edge Case | UI | Regression | Performance | Security
**Environment:** Web (Chrome 120+ / Firefox 121+ / Safari 17+) | Mobile (iOS 17+ / Android 13+)

**Preconditions:**
- [Precondition 1]
- [Precondition 2]

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | [Action the user/system takes] | [Specific expected outcome] |
| 2 | [Next action] | [Next expected outcome] |
| 3 | [Continue as needed] | [Outcome] |

#### Test Data

​```
field_name:  value
field_name:  value
​```

**Postconditions:**
- [System/DB state after test passes — be specific]
- [e.g. Record created with status = X]

**Status:** Not Run
**Notes:** [Optional — known bugs, platform quirks, scope limits. Leave blank if none.]

---
```

---

## 2. Full Example Test Case

> Use this as a reference for what a correctly written UI TC looks like.

### CHECKOUT-001: Verify submitting checkout form successfully with valid credit card on web

**Priority:** High
**Type:** Functional
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)

**Preconditions:**
- User is logged in with a verified account
- Cart contains at least 1 item
- Shipping address is pre-saved in user profile
- Test environment: Staging with Stripe sandbox enabled

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Navigate to `/cart` | Cart page loads with correct items and total |
| 2 | Click "Proceed to Checkout" | Checkout page renders; billing form is visible |
| 3 | Verify pre-filled shipping address | Correct address is populated from user profile |
| 4 | Select "Credit Card" as payment method | Card input fields appear: number, expiry, CVV |
| 5 | Enter valid card details (see Test Data) | Card type icon (Visa) appears; fields accept input |
| 6 | Click "Place Order" | Button disables immediately; loading spinner appears |
| 7 | Wait for API response (~2s) | Redirected to `/order-confirmation` |
| 8 | Verify confirmation page | Order ID displayed; total matches cart amount |

#### Test Data

```
card_number:  4111 1111 1111 1111
expiry:       12/28
cvv:          123
card_name:    John Demo
email:        testuser@demo.com
```

**Postconditions:**
- Order record created in DB with `status = PAID`
- Inventory decremented for all purchased items
- Confirmation email sent to `testuser@demo.com` within 2 minutes
- Stripe sandbox dashboard shows successful charge

**Status:** Not Run
**Notes:** Run on all 3 browsers. Verify email delivery via Mailtrap sandbox.

---

## 3. UI-Specific Checklist Additions

> Add these checks on top of the shared Pre-Submit Checklist (Section 10 in TESTCASE_RULES_SHARED.md).

### Per test case — UI additions

- [ ] Steps start from the entry point of the feature (e.g. "Navigate to /login", "Tap 'Start Setup'")
- [ ] Every error message in Expected Result is quoted verbatim (exact text, not paraphrase)
- [ ] Mobile TCs specify gesture type: Tap / Swipe / Long-press / Pinch — never "click"
- [ ] Screenshots or Figma frame references are noted in Notes if the TC covers a visual state

### Excel export — Clarify Requirements sheet

- [ ] The `Clarify Requirements` sheet is always included in the Excel export alongside the TC sheet
- [ ] Every PENDING TC row is filled with orange (`#FFC000`) and the Notes cell references the CQ ID
- [ ] No PENDING row is exported without a corresponding CQ entry in the Clarify Requirements sheet

---

## 4. Mobile-Specific Writing Notes

### Gesture vocabulary

Use these exact terms in the Steps Action column for mobile TCs:

| Gesture | Term to use |
|---------|-------------|
| Finger contact on element | `Tap` |
| Horizontal drag across screen | `Swipe left` / `Swipe right` |
| Vertical drag across screen | `Scroll up` / `Scroll down` |
| Two-finger spread | `Pinch out` |
| Two-finger squeeze | `Pinch in` |
| Hold finger on element | `Long-press` |
| Drag element to a position | `Drag [element] to [target]` |

> Never use "click" for mobile steps. Click implies a mouse interaction.

### Device and OS in Preconditions

Always state the device type and OS version. Examples:

```
- Device: iPhone 14 / iOS 17.2
- Device: Samsung Galaxy S23 / Android 14
- App version: 2.4.1 (build 412)
- Network: WiFi — 4G LTE — Offline (as appropriate to the TC)
```

### Offline / degraded network TCs

- State the exact network condition in Preconditions: `Network: Airplane mode` or `Network: Throttled to 3G via dev tools`
- State whether the app should degrade gracefully or show an error — never leave it implied
- If the expected offline behaviour is not defined in Figma or the User Story, log a CQ (see TESTCASE_RULES_SHARED.md §13.2) and mark the TC PENDING

### App state in Preconditions

For mobile TCs, always state the app state at the start of the test:

```
- App is freshly installed (no cached data)
- App is in the foreground with the user logged in
- App has been backgrounded for more than 5 minutes (session may have expired)
- Push notification permissions: Granted / Denied
```
