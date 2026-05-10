# Requirement Summary Review & Test Case Gap Analysis

## Overview
This document reviews the current BATT test cases, identifies requirement-summary corrections, and highlights coverage gaps. It is formatted for easy reading and PDF export.

## 1. Current Test Case Inventory
| TC ID | Section | What It Tests |
|------|---------|---------------|
| BATT-001 | §3.1 REST | 30 pts (≥12.70 V) |
| BATT-002 | §3.1 REST | 15 pts fallback (missing data) |
| BATT-003 | §3.1 REST | 0 pts (<12.00 V) |
| BATT-004 | §3.2 CRANK | 25 pts (≥10.0 V) |
| BATT-005 | §3.2 CRANK | Temperature compensation |
| BATT-006 | §3.2 CRANK | Fallback using REST when no cranks |
| BATT-007 | §3.2 CRANK | 0 pts (<8.0 V) + ×0.5 modifier |
| BATT-008 | §3.3 TREND | 12 pts (≥−0.003 V/day) |
| BATT-009 | §3.3 TREND | 9 pts (between −0.003 and −0.008 V/day) |
| BATT-010 | §3.3 TREND | 0 pts (<−0.015 V/day) |
| BATT-011 | §3.4 DECAY | 13 pts (≤0.003 V/hr) |
| BATT-012 | §3.4 DECAY | Data cleanup rules (exclude <6 hr parks, >13.5 V start) |
| BATT-013 | §3.4 DECAY | 0 pts (>0.015 V/hr) + ×0.7 modifier |
| BATT-014 | §3.5 CHARGE | 10 pts (abs ≥95%, short <50%) |
| BATT-015 | §3.5 CHARGE | 7 pts (abs ≥90%, short <70%) |
| BATT-016 | §3.5 CHARGE | 4 pts (abs ≥80%) |
| BATT-017 | §3.5 CHARGE | 0 pts (abs <80%) |
| BATT-018 | §3.6 LATEST | 10 pts (≥12.50 V) |
| BATT-019 | §3.6 LATEST | 0 pts (<11.90 V) |
| BATT-020 | §4 Forecast | Base projection formula |
| BATT-021 | §4 Forecast | Flat/positive slope → 90 days |
| BATT-022 | §4 Forecast | Modifier compounding + redundancy guard |
| BATT-023 | §4 Forecast | 14-day floor + Critical override |
| BATT-024 | §4 Forecast | Battery replacement override (reset to 90 d) |
| BATT-025 | §4 + §5 | Perfect 100 score end-to-end |
| BATT-026 | §4 Forecast | Negative forecast clamped to 0 |
| BATT-027 | §5 Bands | Excellent (95) vs Good (94) boundary |
| BATT-028 | §5 Bands | Most-restrictive rule (score=Good, forecast=Poor → Poor) |
| BATT-029 | §5 Bands | Fair band (score 72, forecast 38 d) |
| BATT-030 | §5 Bands | Poor band (score 57, forecast >30 d) |
| BATT-031 | §5 Bands | Critical band (score <50) |
| BATT-032 | §2 Formula | Score formula sum = 100 |
| BATT-033 | §2 Formula | v2.2 regression (v2.1 vs v2.2 weightings) |
| BATT-034 | §2 Formula | MURANO real-world score drop |
| BATT-035 | §3.2 CRANK | Calculator config fix (min_active=0) |
| BATT-036 | §3.3 TREND | Regression x-axis fix (midpoint, not timestamp) |
| BATT-037 | §3.1 REST | Score boundary (12.70 V = 30 pts, 12.69 V = 25 pts) |
| BATT-038 | §3.2 CRANK | Score + modifier boundary (9.5 V = 20 pts, 9.4 V = 13 pts + ×0.5) |
| BATT-039 | §3.3 TREND | Score boundaries (−0.003, −0.008 V/day) |
| BATT-040 | §3.4 DECAY | Negative slope clamped to zero |
| BATT-041 | §3.1 REST | Forecast modifier threshold (11.79 V vs 11.80 V) |
| BATT-042 | §3.6 LATEST | Score boundaries (12.20 V = 7 pts, 11.90 V = 4 pts) |
| BATT-043 | §4 Forecast | Deep discharge modifier (×0.7) |
| BATT-044 | §4 Forecast | Alternator failure modifier (×0.6) |
| BATT-045 | §3.1 REST | Forecast reference voltage fallback (no live voltage) |
| BATT-046 | §3.5 CHARGE | Speed filter (>5 km/h only) |
| BATT-047 | §3.2 CRANK | Temperature baseline check (25°C → zero adjustment) |
| BATT-048 | §3.4 DECAY | Score boundary tiers (0.003, 0.006, 0.015 V/hr) |
| BATT-049 | UI Display | All 6 signal scores visible without scrolling |
| BATT-050 | UI Display | Colour-coded status badges (all 4 tiers) |
| BATT-051 | UI Display | Forecast shown as relative days not calendar date |
| BATT-052 | UI Display | Signal scores match calculator data source |
| BATT-053 | §3.1 REST | Good tier (25 pts) and Fair tier (19 pts) |
| BATT-054 | §3.2 CRANK | Poor tier (6 pts, 8.0–8.9 V) |

---

## 2. Requirement Summary Corrections

### 2.1 §3.1 REST Signal (30 pts max)
- **Issue:** BATT-001 references only the top REST tier and omits the full tier structure.
- **Correction:** Update the requirement summary to state:
  - "The REST signal scores on five tiers: ≥12.70 V → 30 pts, ≥12.50 V → 25 pts, ≥12.30 V → 19 pts, ≥12.00 V → 10 pts, <12.00 V → 0 pts, missing → 15 pts neutral. The signal carries 30% of the total score and is also used as the reference voltage in the forecast when live voltage is unavailable."

### 2.2 §3.4 DECAY Signal (spec vs doc inconsistency)
- **Issue:** §3.2 still contains a legacy 15-point DECAY table from v2.1.
- **Correction:** Update §3.2 to match v2.2:
  - ≤0.003 → 13 pts
  - ≤0.006 → 10 pts
  - ≤0.010 → 7 pts
  - ≤0.015 → 3 pts
  - >0.015 → 0 pts
  - missing → 7 pts neutral

### 2.3 §3.5 CHARGE Signal — Neutral Fallback
- **Issue:** BATT-014 through BATT-017 do not reference the CHARGE neutral fallback.
- **Correction:** Add a dedicated test case and summary for:
  - "No trips in window → 5 pts neutral. This applies to newly onboarded vehicles and vehicles parked for 30+ days."

---

## 3. Coverage Gaps by Signal

### 3.1 REST Signal
| Tier | Score | Covered |
|------|-------|---------|
| ≥12.70 V | 30 pts | ✅ BATT-001 |
| ≥12.50 V | 25 pts | ✅ BATT-053 (partial) |
| ≥12.30 V | 19 pts | ✅ BATT-053 (partial) |
| ≥12.00 V | 10 pts | ❌ Missing |
| <12.00 V | 0 pts | ✅ BATT-003 |
| missing | 15 pts neutral | ✅ BATT-002 |

> The 10-pt tier is operationally significant and currently untested.

### 3.2 CRANK Signal
| Tier | Score | Covered |
|------|-------|---------|
| ≥10.0 V (compensated) | 25 pts | ✅ BATT-004 |
| ≥9.5 V | 20 pts | ✅ BATT-038 (boundary only) |
| ≥9.0 V | 13 pts | ❌ Missing |
| ≥8.0 V | 6 pts | ✅ BATT-054 |
| <8.0 V | 0 pts | ✅ BATT-007 |
| missing | proportional to REST | ✅ BATT-006 |

> Missing the 13-pt "Marginal" CRANK band.

### 3.3 TREND Signal
| Tier | Score | Covered |
|------|-------|---------|
| ≥−0.003 V/day | 12 pts | ✅ BATT-008 |
| ≥−0.008 V/day | 9 pts | ✅ BATT-009 |
| ≥−0.015 V/day | 5 pts | ❌ Missing |
| <−0.015 V/day | 0 pts | ✅ BATT-010 |
| missing | 6 pts neutral | ❌ Missing |

> The 5-pt tier and the neutral TREND fallback are both untested.

### 3.4 DECAY Signal
| Tier | Score | Covered |
|------|-------|---------|
| ≤0.003 V/hr | 13 pts | ✅ BATT-011 |
| ≤0.006 V/hr | 10 pts | ✅ BATT-048 (boundary) |
| ≤0.010 V/hr | 7 pts | ❌ Missing |
| ≤0.015 V/hr | 3 pts | ✅ BATT-048 (boundary) |
| >0.015 V/hr | 0 pts | ✅ BATT-013 |
| missing | 7 pts neutral | ❌ Missing |

> The 7-pt DECAY tier and the neutral fallback need coverage.

### 3.5 CHARGE Signal
| Tier | Score | Covered |
|------|-------|---------|
| abs ≥95% and short <50% | 10 pts | ✅ BATT-014 |
| abs ≥90% and short <70% | 7 pts | ✅ BATT-015 |
| abs ≥80% | 4 pts | ✅ BATT-016 |
| abs <80% | 0 pts | ✅ BATT-017 |
| no trips in window | 5 pts neutral | ❌ Missing |

> The CHARGE neutral fallback is missing and should be added.

### 3.6 LATEST Signal
| Tier | Score | Covered |
|------|-------|---------|
| ≥12.50 V | 10 pts | ✅ BATT-018 |
| ≥12.20 V | 7 pts | ✅ BATT-042 |
| ≥11.90 V | 4 pts | ✅ BATT-042 |
| <11.90 V | 0 pts | ✅ BATT-019 |
| missing | 5 pts neutral | ❌ Missing |

> The LATEST neutral fallback is currently untested.

---

## 4. Additional Requirement Areas Without Coverage

### 4.1 Status Column / Badge Display
Missing coverage for:
- Pill ordering: red before amber before green
- Maximum 3 pills + "+N more" overflow
- Always show at least one pill (HEALTHY when nothing else fires)
- DEEP DISCHARGE badge trigger
- ALTERNATOR badge trigger
- TREND↓ badge trigger
- CHARGE↓ badge trigger
- SHORT↓ badge trigger
- REPLACE badge trigger
- HEALTHY badge when no other badges fire
- Plain-English summary line logic for all 9 combinations
- Backwards compatibility mapping
- Column sortability by worst severity
- Mobile / narrow-column behaviour (<600 px)

### 4.2 Health Score Tooltip
Missing coverage for:
- Tooltip renders on hover and closes on blur/mouseleave/Escape
- Six sub-signal rows show friendly labels (not raw values or formula weights)
- Dot colour rules: ≥80% green, 40–79% amber, <40% red
- Band label colour coding by hex value
- Formula weights are NOT displayed
- Raw numeric readings are NOT displayed
- One-line summary matches Status column summary
- Mobile tap-to-open modal (<480 px)
- Keyboard accessibility: `tabindex=0`, `aria-describedby`, `role="tooltip"`
- Tooltip opens on focus as well as mouseenter

### 4.3 Forecast Modifier — Low CRANK (<9.5 V, ×0.5)
- BATT-007 validates the 0-pt CRANK state, but not forecast modifier activation at <9.5 V.
- A compensated crank of 9.0 V should score 13 pts and still trigger ×0.5.

### 4.4 Forecast Modifier — Low REST (<11.8 V, ×0.5)
- BATT-041 tests the REST 0-pt boundary, but not the separate forecast modifier boundary.
- The 11.8–12.0 V range is untested.

### 4.5 Good Band Forecast Override
- BATT-028 covers Good + Poor → Poor, but not Good + forecast 30–44 d → Fair.

### 4.6 CHARGE Signal — SHORT↓ Badge Interaction
- No test covers absorption ≥95% while SHORT↓ fires because >70% of trips are short.

### 4.7 DECAY Neutral Fallback
- No test covers 7 pts when no qualifying parks exist in the 30-day window.

### 4.8 TREND Neutral Fallback
- No test covers 6 pts when there is insufficient data for regression.

### 4.9 CRANK Fallback Formula Verification
- BATT-006 covers fallback existence, but not the exact formula `round(25 × rest_pts / 30)`.

### 4.10 WeatherAPI Temperature Fallback
Missing scenarios:
- No GPS fix
- Malformed lat/lon
- No fix within 7 days

---

## 5. Recommended New Test Cases
| Priority | Area | Suggested Test Case Title |
|----------|------|---------------------------|
| High | REST | 10 pts tier (12.00 V ≤ voltage < 12.30 V) |
| High | CRANK | 13 pts tier (9.0 V ≤ compensated < 9.5 V) |
| High | TREND | 5 pts tier (−0.015 V/day ≤ slope < −0.008 V/day) |
| High | DECAY | 7 pts tier (0.006 V/hr < slope ≤ 0.010 V/hr) |
| High | Forecast | CRANK ×0.5 modifier fires at <9.5 V (not <8.0 V) |
| High | Bands | Good score + forecast 30–44 d → Fair band |
| Medium | CHARGE | Neutral fallback (5 pts, no trips in window) |
| Medium | LATEST | Neutral fallback (5 pts, no telemetry) |
| Medium | TREND | Neutral fallback (6 pts, insufficient data) |
| Medium | DECAY | Neutral fallback (7 pts, no qualifying parks) |
| Medium | CHARGE | SHORT↓ badge fires even when absorption ≥95% |
| Medium | Status | All 8 badge triggers (DEEP DISCHARGE, ALTERNATOR, PARK DRAIN, TREND↓, CHARGE↓, SHORT↓, REPLACE, HEALTHY) |
| Medium | Status | Multi-badge pill ordering and "+N more" overflow |
| Medium | Status | All 9 plain-English summary line combinations |
| Medium | Status | Mobile behaviour (<600 px, summary hidden) |
| Medium | Tooltip | 6-row sub-signal dot colour thresholds (80%/40% rules) |
| Medium | Tooltip | Formula weights and raw values NOT displayed |
| Medium | Tooltip | Band label colour coding per band |
| Medium | Tooltip | Mobile tap-to-open modal (<480 px) |
| Medium | Tooltip | Keyboard accessibility (tabindex, aria-describedby) |
| Low | CRANK | Exact proportional formula `round(25 × rest_pts / 30)` |
| Low | WeatherAPI | Temperature fallback when no GPS fix |
| Low | WeatherAPI | Temperature fallback when no fix within 7 days |

---

## 6. Review Notes
- Use the above structure for PDF export: headings, tables, and bullet lists.
- Keep the requirement summaries concise and business-focused.
- Confirm that each new test case maps directly to the requirement tier or fallback.
