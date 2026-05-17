# Test Cases: Battery Prediction (Fleet Pulse by Telemax)

## Overview

| Field       | Value                                                                |
|-------------|----------------------------------------------------------------------|
| Author      | Hanna Lee (hanna.lee@telemax.com.au)                                 |
| Date        | 2026-05-17                                                           |
| Version     | 4.0                                                                  |
| Module      | Battery Prediction — Battery Health & Replacement Forecast (v2.2)    |
| Environment | Web (primary) + Mixed (Backend Flespi calc inspection where required) |
| Status      | In Progress                                                          |

**Source documents:**
- `red-Battery Study_v1.md` (Engineering Briefing v2.2, 28 Apr 2026)
- Battery Health & Replacement Forecast: https://flepsi-batteryhealth-replacement.netlify.app/
- Fleet Pulse: Status Column Spec: https://cosmic-brioche-eccf27.netlify.app/
- Fleet Pulse: Health Score Tooltip Spec: https://eclectic-cassata-b60697.netlify.app/

**Linked SDET workflow artifacts:**
- Step 1 analysis: `analysis-battery-prediction_v1.md`
- Step 2 Q&A: `qa-battery-prediction_v1.md`
- Carry-over CQ log: `tc-battery-prediction_v4_CQ.csv`

**Rules applied:** `TESTCASE_RULES_SHARED.md` (mandatory fields, naming, writing rules) + `TESTCASE_RULES_UI.md` (UI/mobile extension) + `.claude/commands/04-create-tc.md` (Feature / Requirement ID / Automation Candidate fields). 77 TCs total. 11 TCs flagged PENDING — blocked by Q&A items.

---

## Execution Summary

**Last updated:** 2026-05-17 by Hanna Lee  
**Test Cycle:** v4 baseline (pre-execution)

#### Status Counts

| Status        | Count | % of Total |
|---------------|-------|------------|
| Total TCs     |  77   | 100%       |
| Pass          |   0   | 0%         |
| Fail          |   0   | 0%         |
| Blocked       |   0   | 0%         |
| Skip          |   0   | 0%         |
| In Progress   |   0   | 0%         |
| Pending       |  11   | 14.3%      |
| Not Run       |  66   | 85.7%      |

#### Priority Breakdown

| Priority   | Total | Pass | Fail | Blocked | Not Run | Pass Rate % |
|------------|-------|------|------|---------|---------|-------------|
| High       |  40   |  0   |  0   |   0     |   40    |     0%      |
| Medium     |  32   |  0   |  0   |   0     |   32    |     0%      |
| Low        |   5   |  0   |  0   |   0     |    5    |     0%      |
| **Total**  |  77   |  0   |  0   |   0     |   77    |     0%      |

> High-priority share = **51.9%** (rule: ≥ 30%). ✅

---

## Table of Contents

- **REST Signal (§3.1)** — BATT-001 … BATT-008 (8 TCs)
- **CRANK Signal (§3.2)** — BATT-009 … BATT-017 (9 TCs)
- **TREND Signal (§3.3)** — BATT-018 … BATT-023 (6 TCs)
- **DECAY Signal (§3.4)** — BATT-024 … BATT-030 (7 TCs)
- **CHARGE Signal (§3.5)** — BATT-031 … BATT-037 (7 TCs)
- **LATEST Signal (§3.6)** — BATT-038 … BATT-041 (4 TCs)
- **Forecast Logic (§4)** — BATT-042 … BATT-051 (10 TCs)
- **Health Bands (§5)** — BATT-052 … BATT-057 (6 TCs)
- **Score Formula (§2 + Regression)** — BATT-058 … BATT-060 (3 TCs)
- **Status Column / Badges** — BATT-061 … BATT-067 (7 TCs)
- **Health Score Tooltip** — BATT-068 … BATT-073 (6 TCs)
- **General UI Display** — BATT-074 … BATT-075 (2 TCs)
- **WeatherAPI Temperature Fallback** — BATT-076 … BATT-077 (2 TCs)
- **Clarify Requirements log** — 12 open items

> 🟧 **PENDING** = blocked by an open CQ. Highlighted orange (#FFC000) in the Excel export. Do not execute until the linked CQ is resolved.

---

## REST Signal (§3.1)

### Test Case: BATT-001

**Title:** Verify scoring REST signal as 30 pts when 30-day mean rest_voltage_avg is ≥ 12.70 V  
**Feature:** Battery Health & Replacement Forecast (Fleet Pulse by Telemax)  
**Requirement ID:** REQ-3.1.a — traced to: red-Battery Study_v1.md §3.1 (REST Signal — Scoring thresholds table)  
**Screen / Section:** Battery Health & Replacement Forecast — §3.1 REST Signal  
**Type:** Functional  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805151)  
**Requirement Summary:** REST contributes up to 30 pts of the 100-point Health Score. The top tier (≥12.70 V mean rest voltage) maps to 30 pts (Excellent). Wrong scoring at this tier silently penalises healthy batteries and triggers false replacement forecasts.

**Preconditions:**
- Test vehicle `TLX-DEMO-001` exists in the Flespi tenant with ≥ 30 days of telemetry
- Calc 2805151 (Rest Voltage) is enabled and producing rest_voltage_avg samples
- 30-day mean rest_voltage_avg is engineered to 12.72 V (e.g. seeded sandbox data)
- Test user is logged in to Fleet Pulse with read access to the vehicle row

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open the Flespi calc 2805151 device messages for `TLX-DEMO-001` and inspect the 30-day mean | Sample count ≥ 20; visible mean reads 12.72 V (±0.01) |
| 2 | Navigate to Fleet Pulse dashboard and locate the `TLX-DEMO-001` row | Row renders with Health Score chip visible |
| 3 | Hover the Health Score chip to open the tooltip | Tooltip opens; the REST row is visible |
| 4 | Read the REST score in the tooltip | REST shows **30/30** with Excellent (green) indicator |
| 5 | Trigger a manual score recalculation (or wait for the next pipeline cycle) and re-open the tooltip | REST remains **30/30** — score is stable across recalc |

**Test Data:**

```
vehicle_id:            TLX-DEMO-001
mean_rest_voltage_30d: 12.72 V
sample_count:          24
calc_id:               2805151
```

**Post-conditions:**
- REST score persisted as 30 in `score_history`
- Overall `battery_health_score` reflects REST=30 in its breakdown payload
- No fallback flag set on this score record

**Automation Candidate:** Yes — deterministic inputs from seeded calc 2805151; idempotent dashboard read.  
**Status:** Not Run  
**Notes:** Score persistence assertion depends on recalc cadence — see Q2 (assumed ≤15 min).

---

### Test Case: BATT-002

**Title:** Verify scoring REST signal as 25 pts when 30-day mean rest_voltage_avg is in [12.50 V, 12.70 V)  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.1.a — traced to: red-Battery Study_v1.md §3.1 Good tier  
**Screen / Section:** Battery Health & Replacement Forecast — §3.1 REST Signal  
**Type:** Functional  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805151)  
**Requirement Summary:** The Good tier (≥12.50 V and <12.70 V) must score 25 pts. Confirms the tier directly below Excellent — the most common operationally healthy state.

**Preconditions:**
- Vehicle has ≥ 30 days of telemetry
- 30-day mean rest_voltage_avg engineered to 12.55 V
- User is logged in to Fleet Pulse

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm calc 2805151 reports 30-day mean = 12.55 V | Mean reads 12.55 V (±0.01) |
| 2 | Open the Health Score tooltip on the vehicle row | Tooltip opens |
| 3 | Read the REST row | REST shows **25/30** with Good (green) status |

**Test Data:**

```
mean_rest_voltage_30d: 12.55 V
```

**Post-conditions:**
- REST score persisted as 25 in `score_history`

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-003

**Title:** Verify scoring REST signal as 19 pts when 30-day mean rest_voltage_avg is in [12.30 V, 12.50 V)  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.1.a — traced to: red-Battery Study_v1.md §3.1 Fair tier  
**Screen / Section:** Battery Health & Replacement Forecast — §3.1 REST Signal  
**Type:** Functional  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805151)  
**Requirement Summary:** Fair tier (≥12.30 V and <12.50 V) scores 19 pts — the first amber tier in the REST band, indicating early degradation.

**Preconditions:**
- Vehicle has ≥ 30 days of telemetry
- 30-day mean rest_voltage_avg engineered to 12.35 V

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm 30-day mean = 12.35 V in calc 2805151 | Mean reads 12.35 V |
| 2 | Open the Health Score tooltip | Tooltip opens |
| 3 | Read the REST row | REST shows **19/30** with Fair (amber) status; tooltip dot colour is amber |

**Test Data:**

```
mean_rest_voltage_30d: 12.35 V
```

**Post-conditions:**
- REST score persisted as 19 in `score_history`; tooltip dot rendered amber

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-004

**Title:** Verify scoring REST signal as 10 pts when 30-day mean rest_voltage_avg is in [12.00 V, 12.30 V)  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.1.a — traced to: red-Battery Study_v1.md §3.1 Poor tier  
**Screen / Section:** Battery Health & Replacement Forecast — §3.1 REST Signal  
**Type:** Functional  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805151)  
**Requirement Summary:** NEW v4 coverage. Poor tier (≥12.00 V and <12.30 V) must score 10 pts. The 10-pt tier is operationally significant and was untested in v3 — review §3.1 flagged this as a High-priority gap.

**Preconditions:**
- Vehicle has ≥ 30 days of telemetry
- 30-day mean rest_voltage_avg engineered to 12.05 V
- A second seeded state at 12.00 V and a third at 11.99 V are available

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm 30-day mean = 12.05 V in calc 2805151 | Mean reads 12.05 V |
| 2 | Open the Health Score tooltip | Tooltip opens |
| 3 | Read the REST row | REST shows **10/30** with Poor (orange) status |
| 4 | Repeat at boundary value 12.00 V exactly | REST still shows **10/30** (≥12.00 V is inclusive) |
| 5 | Repeat at 11.99 V | REST drops to **0/30** — boundary respected |

**Test Data:**

```
mean_rest_voltage_30d: 12.05 V
boundary_low:          12.00 V
boundary_high:         12.29 V
```

**Post-conditions:**
- REST=10 persisted for 12.05 V case; REST=0 persisted for 11.99 V case

**Automation Candidate:** Yes — three deterministic data points, easy to parameterise.  
**Status:** Not Run  
**Notes:** New in v4 — closes review §3.1 10-pt gap. Boundary inclusivity assumes Q10 confirms ≥ everywhere.

---

### Test Case: BATT-005

**Title:** Verify scoring REST signal as 0 pts when 30-day mean rest_voltage_avg is < 12.00 V  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.1.a + REQ-3.1.c — traced to: red-Battery Study_v1.md §3.1 Critical tier + Forecast modifier  
**Screen / Section:** Battery Health & Replacement Forecast — §3.1 REST Signal  
**Type:** Negative  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805151, forecast pipeline)  
**Requirement Summary:** Critical tier (<12.00 V) scores 0 pts. Additionally, mean rest <11.8 V arms the ×0.5 forecast modifier — both behaviours must be observed.

**Preconditions:**
- Vehicle has ≥ 30 days of telemetry
- 30-day mean rest_voltage_avg engineered to 11.85 V (below both thresholds)

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm 30-day mean = 11.85 V | Mean reads 11.85 V |
| 2 | Open the Health Score tooltip | Tooltip opens |
| 3 | Read the REST row | REST shows **0/30** with Critical (red) status |
| 4 | Inspect `forecast_audit.modifier_list` for this vehicle | Contains `rest<11.8_x0.5` |

**Test Data:**

```
mean_rest_voltage_30d: 11.85 V
```

**Post-conditions:**
- REST=0 persisted in `score_history`
- `rest<11.8_x0.5` modifier flagged in `forecast_audit`

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-006

**Title:** Verify scoring REST signal as 15 pts neutral fallback when no rest_voltage_avg samples are present  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.1.a — traced to: red-Battery Study_v1.md §3.1 "Missing data → 15 pts neutral"  
**Screen / Section:** Battery Health & Replacement Forecast — §3.1 REST Signal (Neutral fallback)  
**Type:** Edge Case  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805151)  
**Requirement Summary:** When calc 2805151 emits zero samples (newly onboarded vehicle, calc disabled, telemetry outage), REST must default to 15 pts (neutral). This prevents penalising vehicles for missing data.

**Preconditions:**
- Vehicle is newly onboarded with < 24 h of telemetry, OR calc 2805151 has been disabled for the vehicle
- No rest_voltage_avg samples exist in the 30-day window

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Query calc 2805151 for the vehicle over the 30-day window | Sample count = 0 |
| 2 | Open the Health Score tooltip | Tooltip opens |
| 3 | Read the REST row | REST shows **15/30** with Neutral (grey) status and explanatory text "Insufficient rest data" |

**Test Data:**

```
sample_count: 0
window:       last 30 days
```

**Post-conditions:**
- REST=15 persisted with `fallback_reason='no_rest_data'`

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-007

**Title:** Verify REST score boundary transitions cleanly at 12.70 V (30 pts) vs 12.69 V (25 pts)  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.1.a — traced to: red-Battery Study_v1.md §3.1 Excellent/Good boundary  
**Screen / Section:** Battery Health & Replacement Forecast — §3.1 REST Signal (boundary)  
**Type:** Edge Case  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805151)  
**Requirement Summary:** The 12.70 V tier boundary must score 30 pts at exactly 12.70 V (inclusive) and 25 pts at 12.69 V. Proves the comparison operator is ≥ and not >.

**Preconditions:**
- Two seeded vehicles or two seeded data states — Vehicle A: 30-day mean = 12.7000 V; Vehicle B: 12.6900 V

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Seed Vehicle A with 30-day mean = 12.7000 V and trigger recalc | Recalc completes |
| 2 | Open the tooltip for Vehicle A | REST = **30/30** |
| 3 | Seed Vehicle B with 30-day mean = 12.6900 V and trigger recalc | Recalc completes |
| 4 | Open the tooltip for Vehicle B | REST = **25/30** |

**Test Data:**

```
vehicle_A.mean: 12.7000 V
vehicle_B.mean: 12.6900 V
```

**Post-conditions:**
- A: REST=30 in `score_history`; B: REST=25 in `score_history`

**Automation Candidate:** Yes — parameterised boundary check.  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-008

**Title:** Verify forecast reference voltage falls back to mean rest voltage when live voltage is missing  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.1.b — traced to: red-Battery Study_v1.md §3.1 "ref_v = live_v if available else mean_rest"  
**Screen / Section:** Battery Health & Replacement Forecast — §3.1 REST Signal (Forecast reference fallback)  
**Type:** Edge Case  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805151, forecast pipeline)  
**Requirement Summary:** When the latest telemetry message lacks `external.powersource.voltage`, the forecast pipeline must fall back to the 30-day mean rest voltage as its reference. Without this fallback the forecast cannot compute and the vehicle row would show no forecast.

**Preconditions:**
- Vehicle has a valid 30-day mean rest_voltage_avg = 12.40 V
- Latest telemetry message has `external.powersource.voltage` absent (simulated by removing the last 6 h of messages from sandbox)

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Inspect the latest raw telemetry message | `external.powersource.voltage` field is absent |
| 2 | Trigger a forecast recalc | Pipeline runs without error |
| 3 | Inspect `forecast_audit.ref_voltage` and `forecast_audit.ref_voltage_source` | ref_voltage = 12.40 V; source = `rest_mean` |
| 4 | Open the Health Score tooltip | LATEST row shows neutral 5/10 with text "Live voltage unavailable — using rest mean" |

**Test Data:**

```
mean_rest_voltage_30d: 12.40 V
latest_voltage:        null
```

**Post-conditions:**
- `forecast_audit.ref_voltage_source = 'rest_mean'`
- Forecast completes successfully and lands on the dashboard

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

## CRANK Signal (§3.2)

### Test Case: BATT-009

**Title:** Verify scoring CRANK signal as 25 pts when minimum compensated crank_dip is ≥ 10.0 V  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.2.a — traced to: red-Battery Study_v1.md §3.2 (Strong tier ≥10.0 V)  
**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal  
**Type:** Functional  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805150)  
**Requirement Summary:** Strong-cranking tier: minimum 30-day crank_dip (compensated to 25 °C) ≥ 10.0 V scores the full 25 pts. Validates the primary CRANK happy path.

**Preconditions:**
- Vehicle has ≥ 30 days of telemetry with at least 5 crank events
- Min compensated crank_dip engineered to 10.10 V
- Calc 2805150 (Crank Events) is enabled with `min_active=0` + `merge_message_before/after=true`

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Inspect calc 2805150 outputs and compute min compensated crank_dip | Min compensated reads 10.10 V |
| 2 | Open the Health Score tooltip | Tooltip opens |
| 3 | Read the CRANK row | CRANK shows **25/25** with Strong (green) status |

**Test Data:**

```
min_crank_dip_compensated: 10.10 V
events_in_window:          7
```

**Post-conditions:**
- CRANK=25 persisted in `score_history`

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-010

**Title:** Verify CRANK score and forecast modifier transitions cleanly at 9.5 V (20 pts, no modifier) vs 9.4 V (13 pts + ×0.5 modifier)  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.2.a + REQ-3.2.e — traced to: red-Battery Study_v1.md §3.2 + §4 (CRANK modifier threshold)  
**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal (boundary + modifier)  
**Type:** Edge Case  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805150, forecast pipeline)  
**Requirement Summary:** Boundary check confirming dual effect: at 9.5 V the score is 20 and ×0.5 modifier is NOT armed; at 9.4 V the score drops to 13 AND the ×0.5 modifier IS armed.

**Preconditions:**
- Two seeded states — Vehicle A: min compensated crank_dip = 9.50 V; Vehicle B: 9.40 V

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Trigger recalc on Vehicle A | Recalc OK |
| 2 | Open tooltip for A; inspect `forecast_audit.modifier_list` | CRANK = 20/25; modifier list does NOT contain `crank<9.5_x0.5` |
| 3 | Trigger recalc on Vehicle B | Recalc OK |
| 4 | Open tooltip for B; inspect `forecast_audit.modifier_list` | CRANK = 13/25; modifier list contains `crank<9.5_x0.5` |

**Test Data:**

```
vehicle_A.min_crank: 9.50 V
vehicle_B.min_crank: 9.40 V
```

**Post-conditions:**
- A: modifier list does not contain `crank<9.5_x0.5`; B: it does

**Automation Candidate:** Yes — strong boundary regression.  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-011

**Title:** Verify scoring CRANK signal as 13 pts when minimum compensated crank_dip is in [9.0 V, 9.5 V)  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.2.a — traced to: red-Battery Study_v1.md §3.2 Marginal tier  
**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal  
**Type:** Functional  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805150)  
**Requirement Summary:** NEW v4 coverage. 13-pt "Marginal" tier (≥9.0 V and <9.5 V). Review §3.2 flagged this as a missing High-priority tier.

**Preconditions:**
- Min compensated crank_dip engineered to 9.20 V; ≥ 5 events

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm min compensated crank_dip = 9.20 V | Reads 9.20 V |
| 2 | Open tooltip | CRANK = **13/25** with Marginal (amber) status |
| 3 | Inspect `forecast_audit.modifier_list` | Contains `crank<9.5_x0.5` (modifier fires) |

**Test Data:**

```
min_crank_dip_compensated: 9.20 V
```

**Post-conditions:**
- CRANK=13 persisted; modifier `crank<9.5_x0.5` active

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** Closes review §3.2 13-pt gap. Verifies the modifier fires above the 0-pt threshold (see also BATT-051).

---

### Test Case: BATT-012

**Title:** Verify scoring CRANK signal as 6 pts when minimum compensated crank_dip is in [8.0 V, 9.0 V)  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.2.a — traced to: red-Battery Study_v1.md §3.2 Poor tier  
**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal  
**Type:** Functional  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805150)  
**Requirement Summary:** Poor tier (≥8.0 V and <9.0 V) scores 6 pts. Third-worst CRANK band.

**Preconditions:**
- Min compensated crank_dip engineered to 8.50 V

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm min compensated dip = 8.50 V | Reads 8.50 V |
| 2 | Open tooltip | CRANK = **6/25** with Poor (orange) status |
| 3 | Inspect `forecast_audit.modifier_list` | Contains `crank<9.5_x0.5` (still active below 9.5 V) |

**Test Data:**

```
min_crank_dip_compensated: 8.50 V
```

**Post-conditions:**
- CRANK=6 persisted; ×0.5 modifier active

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-013

**Title:** Verify scoring CRANK signal as 0 pts and arming ×0.5 forecast modifier when compensated crank_dip is < 8.0 V  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.2.a + REQ-3.2.e — traced to: red-Battery Study_v1.md §3.2 Critical tier  
**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal  
**Type:** Negative  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805150, forecast pipeline)  
**Requirement Summary:** Critical CRANK (<8.0 V compensated) scores 0 pts and triggers the ×0.5 high-internal-resistance forecast modifier. Highest-severity CRANK condition.

**Preconditions:**
- Min compensated crank_dip engineered to 7.5 V

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm min compensated dip = 7.5 V | Reads 7.5 V |
| 2 | Open tooltip | CRANK = **0/25** with Critical (red) status |
| 3 | Inspect `forecast_audit.modifier_list` | Contains `crank<9.5_x0.5` |
| 4 | Verify final forecast value | forecast_days ≤ 0.5 × base_days |

**Test Data:**

```
min_crank_dip_compensated: 7.5 V
```

**Post-conditions:**
- CRANK=0 persisted; modifier applied to forecast

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-014

**Title:** Verify CRANK temperature compensation formula adds 0.475 V when raw crank is 9.6 V at 6 °C ambient  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.2.b — traced to: red-Battery Study_v1.md §3.2 "Temperature compensation"  
**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal (Temperature compensation)  
**Type:** Functional  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805150 + WeatherAPI)  
**Requirement Summary:** Temperature compensation formula `crank_comp = crank_obs + 0.025 × (25 − ambient °C)` must be applied so cold-morning measurements don't false-fail healthy batteries. A 9.6 V raw at 6 °C should compensate to 10.075 V → 25 pts.

**Preconditions:**
- Vehicle's location at the crank event time has WeatherAPI ambient = 6 °C
- Raw crank_dip captured by calc 2805150 = 9.60 V

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Inspect raw crank_dip and ambient temp for the event | Raw = 9.60 V at 6.0 °C |
| 2 | Inspect `forecast_audit.compensated_crank_dip` | Equals 9.60 + 0.025 × (25 − 6) = **10.075 V** (±0.005) |
| 3 | Open tooltip | CRANK = **25/25** Strong (green) — would have been 13/25 without compensation |

**Test Data:**

```
raw_crank_dip:        9.60 V
ambient_temp:         6.0 °C
expected_compensated: 10.075 V
```

**Post-conditions:**
- `forecast_audit.compensated_crank_dip` ≈ 10.075 V

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** Hot-side compensation behaviour is covered by Q16 (currently assumed un-clamped at hot end).

---

### Test Case: BATT-015

**Title:** Verify CRANK temperature compensation adds zero adjustment at the 25 °C baseline  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.2.b — traced to: red-Battery Study_v1.md §3.2  
**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal (Temperature compensation)  
**Type:** Edge Case  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805150 + WeatherAPI)  
**Requirement Summary:** Sanity check on the compensation baseline: at 25 °C the adjustment term is zero, so raw == compensated.

**Preconditions:**
- Raw crank_dip = 9.60 V at ambient 25 °C

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm raw crank_dip and ambient | 9.60 V at 25 °C |
| 2 | Read `forecast_audit.compensated_crank_dip` | Equals 9.60 V (no adjustment) |

**Test Data:**

```
raw_crank_dip: 9.60 V
ambient_temp: 25 °C
```

**Post-conditions:**
- compensated_crank_dip == raw_crank_dip

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-016

**Title:** Verify CRANK signal falls back to round(25 × REST / 30) when no crank events exist in 30-day window  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.2.d — traced to: red-Battery Study_v1.md §3.2 "REST Fallback for CRANK"  
**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal (REST fallback)  
**Type:** Edge Case  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805150)  
**Requirement Summary:** When no crank events exist in 30 days, CRANK falls back proportionally to REST: `CRANK = round(25 × rest_pts / 30)`. Validates the formula at three reference REST values.

**Preconditions:**
- Vehicle has zero crank events in the 30-day window (parked, owner away, etc.)
- Three seeded REST scores: 30, 25, 0

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm calc 2805150 returns 0 events for the window | Event count = 0 |
| 2 | Seed REST=30/30 and recalc; read CRANK | CRANK = **25/25** (round(25×30/30)) |
| 3 | Seed REST=25/30 and recalc; read CRANK | CRANK = **21/25** (round(25×25/30) = 20.83 → 21) |
| 4 | Seed REST=0/30 and recalc; read CRANK | CRANK = **0/25** (round(25×0/30)) |

**Test Data:**

```
crank_events_count: 0
rest_pts_cases:     30, 25, 0
expected_crank:     25, 21, 0
```

**Post-conditions:**
- CRANK persisted with `fallback_reason='no_crank_events'` in each case

**Automation Candidate:** Yes — three reference points cover the formula well.  
**Status:** Not Run  
**Notes:** Rounding mode (half-up) assumed; pending Q11.

---

### Test Case: BATT-017

**Title:** Verify calc 2805150 captures cranks correctly with min_active=0 and merge_message_before/after=true  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.2.c — traced to: red-Battery Study_v1.md §3.2 "Critical config fix (28 Apr)"  
**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal (Calculator config)  
**Type:** Regression  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805150)  
**Requirement Summary:** Regression: calc 2805150 must use `min_active=0` with `merge_message_before/after=true`. Without these flags, 99% of crank events are missed (April 28 incident).

**Preconditions:**
- Vehicle drove ≥ 5 ignition cycles in a test session
- Permission to modify calc 2805150 config in a sandbox tenant

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open calc 2805150 config in Flespi | `min_active=0`, `merge_message_before=true`, `merge_message_after=true` |
| 2 | Count ignition OFF→ON transitions in raw telemetry for the session | ≥ 5 |
| 3 | Count crank events produced by calc 2805150 | Matches transition count within ±1 |
| 4 | Toggle `merge_message_before/after` to `false` in the sandbox and recount events | Event count drops by ≥ 90% — confirms regression |
| 5 | Restore configuration to `true` and validate count again | Event count returns to the level in Step 3 |

**Test Data:**

```
config.min_active:           0
config.merge_message_before: true
config.merge_message_after:  true
```

**Post-conditions:**
- Calc config restored to required values; production capture rate ≥ 95%

**Automation Candidate:** Partial — config inspection automatable; event-count comparison requires a fixed drive log.  
**Status:** Not Run  
**Notes:** Reverts the April 28 misconfiguration bug. Run in sandbox tenant only.

---

## TREND Signal (§3.3)

### Test Case: BATT-018

**Title:** Verify scoring TREND signal as 12 pts when 30-day rest voltage regression slope is ≥ −0.003 V/day  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.3.a — traced to: red-Battery Study_v1.md §3.3 Stable tier  
**Screen / Section:** Battery Health & Replacement Forecast — §3.3 TREND Signal  
**Type:** Functional  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (regression analyser)  
**Requirement Summary:** TREND scores the full 12 pts when the 30-day linear-regression slope of rest_voltage_avg is ≥ −0.003 V/day (stable or improving).

**Preconditions:**
- ≥ 20 rest_voltage_avg samples spanning ≥ 28 days
- Slope engineered to −0.001 V/day

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Inspect the trend analyser output | Slope = −0.001 V/day |
| 2 | Open tooltip | TREND = **12/12** with Stable (green) status |

**Test Data:**

```
slope_per_day: -0.001 V/day
sample_count:  24
```

**Post-conditions:**
- TREND=12 persisted

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-019

**Title:** Verify scoring TREND signal as 9 pts when 30-day slope is in [−0.008, −0.003) V/day  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.3.a — traced to: red-Battery Study_v1.md §3.3 Mild decline tier  
**Screen / Section:** Battery Health & Replacement Forecast — §3.3 TREND Signal  
**Type:** Functional  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (regression analyser)  
**Requirement Summary:** Mild-decline tier (≥ −0.008 and < −0.003 V/day) scores 9 pts — gentle downward trend, not yet alarming.

**Preconditions:**
- Slope engineered to −0.005 V/day

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm slope = −0.005 V/day | Reads −0.005 |
| 2 | Open tooltip | TREND = **9/12** with Mild Decline status |

**Test Data:**

```
slope_per_day: -0.005 V/day
```

**Post-conditions:**
- TREND=9 persisted

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-020

**Title:** Verify scoring TREND signal as 5 pts when 30-day slope is in [−0.015, −0.008) V/day  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.3.a — traced to: red-Battery Study_v1.md §3.3 Declining tier  
**Screen / Section:** Battery Health & Replacement Forecast — §3.3 TREND Signal  
**Type:** Functional  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (regression analyser, badge engine)  
**Requirement Summary:** NEW v4 coverage. 5-pt tier (≥ −0.015 and < −0.008 V/day) — review §3.3 flagged as a missing High-priority tier. Also triggers the TREND↓ badge in the Status column.

**Preconditions:**
- Slope engineered to −0.012 V/day

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm slope = −0.012 V/day | Reads −0.012 |
| 2 | Open tooltip | TREND = **5/12** with Declining (amber) status |
| 3 | Inspect the Status column on the vehicle row | TREND↓ badge visible |

**Test Data:**

```
slope_per_day: -0.012 V/day
```

**Post-conditions:**
- TREND=5 persisted; TREND↓ badge active for the row

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** Closes review §3.3 5-pt gap.

---

### Test Case: BATT-021

**Title:** Verify scoring TREND signal as 0 pts when 30-day slope is < −0.015 V/day  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.3.a — traced to: red-Battery Study_v1.md §3.3 Critical tier  
**Screen / Section:** Battery Health & Replacement Forecast — §3.3 TREND Signal  
**Type:** Negative  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (regression analyser, badge engine)  
**Requirement Summary:** Critical decline (< −0.015 V/day) scores 0 pts — battery is losing ≥ 0.45 V over 30 days, an accelerating-failure signature.

**Preconditions:**
- Slope engineered to −0.020 V/day

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm slope = −0.020 V/day | Reads −0.020 |
| 2 | Open tooltip | TREND = **0/12** with Critical (red) status |
| 3 | Inspect the Status column | TREND↓ badge visible in red tone |

**Test Data:**

```
slope_per_day: -0.020 V/day
```

**Post-conditions:**
- TREND=0 persisted; TREND↓ badge active

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-022

**Title:** Verify TREND regression x-axis uses interval midpoint, not the calc emission timestamp  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.3.b — traced to: red-Battery Study_v1.md §3.3 "Critical bug fix (v2.0 → v2.2)"  
**Screen / Section:** Battery Health & Replacement Forecast — §3.3 TREND Signal (Regression x-axis fix)  
**Type:** Regression  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (regression analyser)  
**Requirement Summary:** The regression x-axis MUST be `(interval_begin + interval_end) / 2`, NOT the calc emission timestamp. v2.0 had this wrong and masked BMW-class battery instability.

**Preconditions:**
- Test dataset with 25 rest intervals where the interval midpoint differs from the calc timestamp by ≥ 30 min
- Reference slope via midpoint method = −0.011 V/day; using timestamp incorrectly yields −0.004 V/day

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Run TREND regression on the dataset | Pipeline emits slope |
| 2 | Confirm slope = −0.011 V/day | Matches reference within ±0.0005 |
| 3 | Inspect the audit log for the x-axis source field | Reads `interval_midpoint` |
| 4 | Open tooltip | TREND = **5/12** (matches midpoint slope, not 9/12 which the timestamp method would produce) |

**Test Data:**

```
expected_slope: -0.011 V/day
x_axis_source: interval_midpoint
```

**Post-conditions:**
- TREND audit confirms midpoint method; no v2.0 regression

**Automation Candidate:** Yes — strong regression candidate with a frozen reference dataset.  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-023  🟧 PENDING

**Title:** Verify scoring TREND signal as 6 pts neutral fallback when sample count is below the regression threshold  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.3.c — traced to: red-Battery Study_v1.md §3.3 (neutral fallback — threshold not stated)  
**Screen / Section:** Battery Health & Replacement Forecast — §3.3 TREND Signal (Neutral fallback)  
**Type:** Edge Case  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (regression analyser)  
**Requirement Summary:** NEW v4 coverage. When sample count is insufficient for regression, TREND falls back to 6 pts neutral. Threshold not stated in spec — assumed <10 samples pending Q3.

**Preconditions:**
- Vehicle has only 7 rest_voltage_avg samples in the last 30 days (below assumed threshold of 10)

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm sample count = 7 | Count = 7 |
| 2 | Run regression | Pipeline skips regression and emits fallback |
| 3 | Open tooltip | TREND = **6/12** with Neutral (grey) status and text "Not enough data for trend" |

**Test Data:**

```
sample_count: 7
threshold:    10 (assumed pending Q3)
```

**Post-conditions:**
- TREND=6 persisted with `fallback_reason='insufficient_samples'`

**Automation Candidate:** Yes — once threshold is confirmed.  
**Status:** Not Run  
**Notes:** **Blocked by Q3 (CQ-Q3) — TREND minimum sample threshold not stated in spec.** Closes review §3.3 neutral-fallback gap.

---

## DECAY Signal (§3.4)

### Test Case: BATT-024

**Title:** Verify scoring DECAY signal as 13 pts when parked decay slope is ≤ 0.003 V/hr  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.4.a — traced to: red-Battery Study_v1.md §3.4 Excellent tier  
**Screen / Section:** Battery Health & Replacement Forecast — §3.4 DECAY Signal  
**Type:** Functional  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805232)  
**Requirement Summary:** DECAY scores the full 13 pts when parked decay slope ≤ 0.003 V/hr — battery holds charge well across long parks.

**Preconditions:**
- Vehicle has ≥ 3 qualifying parks (≥ 6 h, start ≤ 13.5 V) in the 30-day window
- Calc 2805232 enabled; mean decay slope engineered to 0.0020 V/hr

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Inspect calc 2805232 outputs | Mean slope = 0.0020 V/hr |
| 2 | Open tooltip | DECAY = **13/13** with Excellent (green) status |

**Test Data:**

```
mean_decay_slope: 0.0020 V/hr
qualifying_parks: 4
```

**Post-conditions:**
- DECAY=13 persisted

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-025

**Title:** Verify DECAY score boundary transitions at the 0.003, 0.006, and 0.015 V/hr thresholds  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.4.a — traced to: red-Battery Study_v1.md §3.4 tier boundaries  
**Screen / Section:** Battery Health & Replacement Forecast — §3.4 DECAY Signal (boundaries)  
**Type:** Edge Case  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805232)  
**Requirement Summary:** Boundary check across the four DECAY thresholds: 0.003 V/hr → 13 pts; 0.0031 → 10 pts; 0.0061 → 7 pts; 0.0151 → 0 pts (and ×0.7 modifier).

**Preconditions:**
- Four seeded states (0.0030, 0.0031, 0.0061, 0.0151 V/hr)

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Seed slope = 0.0030 V/hr and recalc | DECAY = **13/13** |
| 2 | Seed slope = 0.0031 V/hr and recalc | DECAY = **10/13** |
| 3 | Seed slope = 0.0061 V/hr and recalc | DECAY = **7/13** |
| 4 | Seed slope = 0.0151 V/hr and recalc; inspect `forecast_audit.modifier_list` | DECAY = **0/13**; modifier list contains `decay>0.015_x0.7` |

**Test Data:**

```
boundaries:        0.0030 / 0.0031 / 0.0061 / 0.0151 V/hr
expected_scores:   13 / 10 / 7 / 0 pts
```

**Post-conditions:**
- All four boundary scores persisted correctly

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-026

**Title:** Verify scoring DECAY signal as 7 pts when parked decay slope is in (0.006, 0.010] V/hr  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.4.a — traced to: red-Battery Study_v1.md §3.4 Watch tier  
**Screen / Section:** Battery Health & Replacement Forecast — §3.4 DECAY Signal  
**Type:** Functional  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805232)  
**Requirement Summary:** NEW v4 coverage. 7-pt tier (0.006 < slope ≤ 0.010 V/hr). Review §3.4 flagged as missing High-priority tier.

**Preconditions:**
- Mean decay slope engineered to 0.008 V/hr

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm slope = 0.008 V/hr | Reads 0.008 |
| 2 | Open tooltip | DECAY = **7/13** with Watch (amber) status |
| 3 | Inspect `forecast_audit.modifier_list` | Does NOT contain `decay>0.015_x0.7` (modifier only fires above 0.015) |

**Test Data:**

```
mean_decay_slope: 0.008 V/hr
```

**Post-conditions:**
- DECAY=7 persisted; no decay modifier in forecast

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** Closes review §3.4 7-pt gap.

---

### Test Case: BATT-027

**Title:** Verify scoring DECAY signal as 0 pts and arming ×0.7 forecast modifier when parked decay slope > 0.015 V/hr  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.4.a + REQ-3.4.e — traced to: red-Battery Study_v1.md §3.4 Critical tier + §4  
**Screen / Section:** Battery Health & Replacement Forecast — §3.4 DECAY Signal  
**Type:** Negative  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805232, forecast pipeline)  
**Requirement Summary:** Critical DECAY (>0.015 V/hr) scores 0 pts AND triggers the ×0.7 self-discharge forecast modifier. Worst DECAY band.

**Preconditions:**
- Mean decay slope engineered to 0.020 V/hr

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm slope = 0.020 V/hr | Reads 0.020 |
| 2 | Open tooltip | DECAY = **0/13** with Critical (red) status |
| 3 | Inspect `forecast_audit.modifier_list` | Contains `decay>0.015_x0.7` |

**Test Data:**

```
mean_decay_slope: 0.020 V/hr
```

**Post-conditions:**
- DECAY=0 persisted; ×0.7 modifier applied

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-028

**Title:** Verify DECAY pipeline drops parks shorter than 6 h and parks starting above 13.5 V before computing slope  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.4.b — traced to: red-Battery Study_v1.md §3.4 "Two required data cleanups"  
**Screen / Section:** Battery Health & Replacement Forecast — §3.4 DECAY Signal (Data cleanup)  
**Type:** Functional  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805232)  
**Requirement Summary:** Two mandatory data-cleanup rules in DECAY: drop parks shorter than 6 h (noise) AND parks where start voltage > 13.5 V (alternator tail not yet decayed).

**Preconditions:**
- Test dataset of 10 parks: 5 valid (≥6 h and start ≤13.5 V), 3 short (4–5 h), 2 with start voltage 13.6–13.9 V

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Run the DECAY pipeline on the dataset | Pipeline completes |
| 2 | Inspect the intermediate `qualifying_parks` list | Count = 5; the 3 short and 2 high-start parks are excluded |
| 3 | Inspect calc 2805232 config | `merge_message_before/after = false` (alternator voltage doesn't contaminate park edges) |
| 4 | Verify slope is computed only over the 5 valid parks | Audit shows 5 contributing intervals |

**Test Data:**

```
parks_total:           10
parks_qualifying:      5
parks_dropped_short:   3
parks_dropped_high_v:  2
config.merge_before:   false
config.merge_after:    false
```

**Post-conditions:**
- Only 5 parks contributed to the DECAY slope

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** Boundary inclusivity of "< 6 h" and "> 13.5 V" subject to Q12 / Q13 confirmations.

---

### Test Case: BATT-029

**Title:** Verify DECAY slope is clamped to zero when a park shows negative voltage change  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.4.c — traced to: red-Battery Study_v1.md §3.4 "clamped to ≥0"  
**Screen / Section:** Battery Health & Replacement Forecast — §3.4 DECAY Signal (Slope clamping)  
**Type:** Edge Case  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805232)  
**Requirement Summary:** Negative slope (start < end during a park) is a surface-charge artefact, not real recovery. Slope must be clamped to ≥0 so negative values don't bias the mean downward.

**Preconditions:**
- One park where start = 12.30 V, end = 12.35 V over 8 h (artefact)

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Run the DECAY pipeline on the artefact park | Pipeline completes |
| 2 | Inspect the park's contribution to slope | Raw = −0.00625 V/hr; clamped slope = 0.000 V/hr |
| 3 | Confirm no negative slopes propagate into the mean | Mean uses 0.000 from this park, not the negative value |

**Test Data:**

```
park.start_v:     12.30
park.end_v:       12.35
park.duration_h:  8
expected_clamped: 0.000 V/hr
```

**Post-conditions:**
- DECAY mean computed correctly with clamped values

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-030

**Title:** Verify scoring DECAY signal as 7 pts neutral fallback when no qualifying parks exist in the 30-day window  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.4.d — traced to: red-Battery Study_v1.md §3.4 (neutral fallback)  
**Screen / Section:** Battery Health & Replacement Forecast — §3.4 DECAY Signal (Neutral fallback)  
**Type:** Edge Case  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805232)  
**Requirement Summary:** NEW v4 coverage. When no qualifying parks (≥6 h, start ≤13.5 V) exist in 30 days, DECAY falls back to 7 pts neutral. Review §3.4 flagged as untested.

**Preconditions:**
- Vehicle has no parks ≥ 6 h with start voltage ≤ 13.5 V in 30 days

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm `qualifying_parks = 0` | Count = 0 |
| 2 | Open tooltip | DECAY = **7/13** Neutral (grey) with text "No qualifying park data" |

**Test Data:**

```
qualifying_parks: 0
```

**Post-conditions:**
- DECAY=7 persisted with `fallback_reason='no_qualifying_parks'`

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** Closes review §3.4 neutral-fallback gap.

---

## CHARGE Signal (§3.5)

### Test Case: BATT-031

**Title:** Verify scoring CHARGE signal as 10 pts when hit_absorption% ≥ 95 and short_trip% < 50  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.5.a — traced to: red-Battery Study_v1.md §3.5 10-pt tier  
**Screen / Section:** Battery Health & Replacement Forecast — §3.5 CHARGE Signal  
**Type:** Functional  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2809220)  
**Requirement Summary:** v2.2 NEW signal. CHARGE scores 10 pts when hit_absorption% ≥ 95% AND short-trip% < 50%. Top tier — vehicles whose duty cycle keeps the battery well-charged.

**Preconditions:**
- Calc 2809220 enabled; ≥ 20 trips in 30-day window
- hit_absorption% engineered to 96%, short_trip% to 35%

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm calc 2809220 metrics | abs%=96, short%=35 |
| 2 | Open tooltip | CHARGE = **10/10** Excellent (green) |
| 3 | Inspect the Status column on the row | No CHARGE↓ or SHORT↓ badge |

**Test Data:**

```
hit_absorption_pct: 96
short_trip_pct:     35
trips_in_window:    24
```

**Post-conditions:**
- CHARGE=10 persisted

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-032

**Title:** Verify scoring CHARGE signal as 7 pts when hit_absorption% is in [90, 95) and short_trip% < 70  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.5.a — traced to: red-Battery Study_v1.md §3.5 7-pt tier  
**Screen / Section:** Battery Health & Replacement Forecast — §3.5 CHARGE Signal  
**Type:** Functional  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2809220)  
**Requirement Summary:** 7-pt tier: hit_absorption% ≥ 90 AND short_trip% < 70 (and not in 10-pt tier). Middle band of CHARGE.

**Preconditions:**
- abs%=92, short%=60

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm metrics | abs%=92, short%=60 |
| 2 | Open tooltip | CHARGE = **7/10** Good |

**Test Data:**

```
hit_absorption_pct: 92
short_trip_pct:     60
```

**Post-conditions:**
- CHARGE=7 persisted

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-033  🟧 PENDING

**Title:** Verify scoring CHARGE signal as 4 pts when hit_absorption% is in [80, 90)  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.5.a — traced to: red-Battery Study_v1.md §3.5 4-pt tier  
**Screen / Section:** Battery Health & Replacement Forecast — §3.5 CHARGE Signal  
**Type:** Functional  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2809220)  
**Requirement Summary:** 4-pt tier requires only absorption ≥ 80%; short_trip% is not explicitly constrained at this tier. Ambiguity at high short-trip values needs CQ.

**Preconditions:**
- abs%=82, short%=85 (high short-trip to expose ambiguity)

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm metrics | abs%=82, short%=85 |
| 2 | Open tooltip | CHARGE shows score per current implementation (record actual) |
| 3 | After CQ-002 resolution, re-validate the expected score | Expected matches the confirmed rule |

**Test Data:**

```
hit_absorption_pct: 82
short_trip_pct:     85
```

**Post-conditions:**
- CHARGE persisted; CQ-002 cross-referenced in Notes

**Automation Candidate:** Yes — once threshold confirmed.  
**Status:** Not Run  
**Notes:** **Blocked by CQ-002** — short-trip behaviour at the 4-pt tier unclear.

---

### Test Case: BATT-034

**Title:** Verify scoring CHARGE signal as 0 pts and firing CHARGE↓ badge when hit_absorption% is < 80  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.5.a — traced to: red-Battery Study_v1.md §3.5 Critical tier + Status spec CHARGE↓ trigger  
**Screen / Section:** Battery Health & Replacement Forecast — §3.5 CHARGE Signal + Status Column Spec  
**Type:** Negative  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2809220, badge engine)  
**Requirement Summary:** 0-pt CHARGE tier (abs% < 80) catches duty cycles too short to reach absorption. CHARGE↓ badge fires alongside the score drop.

**Preconditions:**
- abs%=72, short%=80

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm metrics | abs%=72, short%=80 |
| 2 | Open tooltip | CHARGE = **0/10** Critical (red) |
| 3 | Inspect Status column | CHARGE↓ badge visible |

**Test Data:**

```
hit_absorption_pct: 72
short_trip_pct:     80
```

**Post-conditions:**
- CHARGE=0 persisted; CHARGE↓ badge active

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** CHARGE↓ numeric trigger confirmed only at the 0-pt boundary here; the 80%/90% disambiguation is BATT-037 (PENDING CQ-001).

---

### Test Case: BATT-035

**Title:** Verify CHARGE calculator filters out messages when speed is ≤ 5 km/h or engine is off  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.5.b — traced to: red-Battery Study_v1.md §3.5 "fires while engine running and speed >5 km/h"  
**Screen / Section:** Battery Health & Replacement Forecast — §3.5 CHARGE Signal (Speed filter)  
**Type:** Functional  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2809220)  
**Requirement Summary:** Calc 2809220 must only count messages when engine is running AND speed > 5 km/h. Filters out idling/cranking artefacts.

**Preconditions:**
- Seeded trip with 10 idle messages (speed 0 km/h) and 30 driving messages (speed 30 km/h)

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Inspect calc 2809220 selector | Selector requires `engine.on=true AND speed>5` |
| 2 | Inspect captured messages for the trip | Only the 30 driving messages contribute |

**Test Data:**

```
idle_msgs:             10 (speed=0 km/h)
driving_msgs:          30 (speed=30 km/h)
expected_contributing: 30
```

**Post-conditions:**
- Only driving messages contribute to CHARGE metrics

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-036  🟧 PENDING

**Title:** Verify scoring CHARGE signal as 5 pts neutral fallback when no trips exist in the 30-day window  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.5.c — traced to: red-Battery Study_v1.md §3.5 (neutral fallback)  
**Screen / Section:** Battery Health & Replacement Forecast — §3.5 CHARGE Signal (Neutral fallback)  
**Type:** Edge Case  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2809220)  
**Requirement Summary:** NEW v4 coverage. When no qualifying trips occur in 30 days (newly onboarded vehicles, parked 30+ days), CHARGE falls back to 5 pts neutral. Threshold not stated — assumed 0 trips pending Q5.

**Preconditions:**
- Vehicle parked for full 30-day window — zero qualifying trips

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm `trips_in_window = 0` | Count = 0 |
| 2 | Open tooltip | CHARGE = **5/10** Neutral (grey) with text "No trips in window" |

**Test Data:**

```
trips_in_window: 0
threshold:       0 (assumed pending Q5)
```

**Post-conditions:**
- CHARGE=5 persisted with `fallback_reason='no_trips'`

**Automation Candidate:** Yes — once threshold is confirmed.  
**Status:** Not Run  
**Notes:** **Blocked by Q5 (CQ-Q5).** Closes review §3.5 neutral-fallback gap.

---

### Test Case: BATT-037  🟧 PENDING

**Title:** Verify SHORT↓ badge fires when short_trip% exceeds 70 even when hit_absorption% is ≥ 95  
**Feature:** Battery Health & Replacement Forecast + Fleet Pulse: Status Column Spec  
**Requirement ID:** REQ-3.5.a + Status spec SHORT↓ trigger — traced to: review §4.6  
**Screen / Section:** Battery Health & Replacement Forecast — §3.5 + Fleet Pulse: Status Column Spec  
**Type:** Edge Case  
**Priority:** Medium  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)  
**Requirement Summary:** NEW v4 coverage. The SHORT↓ badge must fire when short-trip% > 70 even if absorption% ≥ 95 (vehicle reaches absorption only on too few long trips). Independent of CHARGE score.

**Preconditions:**
- abs%=96, short%=78

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm metrics | abs%=96, short%=78 |
| 2 | Inspect Status column on the row | SHORT↓ badge visible (amber) |
| 3 | Open tooltip | CHARGE score per implementation; SHORT↓ pill labelled in summary |

**Test Data:**

```
hit_absorption_pct: 96
short_trip_pct:     78
```

**Post-conditions:**
- SHORT↓ badge active; pill visible on the row

**Automation Candidate:** Yes — once CQ-001 confirms the disambiguation between CHARGE↓ and SHORT↓.  
**Status:** Not Run  
**Notes:** **Blocked by CQ-001** — CHARGE↓ vs SHORT↓ split needs sign-off.

---

## LATEST Signal (§3.6)

### Test Case: BATT-038

**Title:** Verify scoring LATEST signal as 10 pts when the latest powersource voltage is ≥ 12.50 V  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.6.a — traced to: red-Battery Study_v1.md §3.6 10-pt tier  
**Screen / Section:** Battery Health & Replacement Forecast — §3.6 LATEST Signal  
**Type:** Functional  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (telemetry pipeline)  
**Requirement Summary:** LATEST scores 10 pts when the most recent `external.powersource.voltage` is ≥ 12.50 V. Real-time freshness signal.

**Preconditions:**
- Latest telemetry message has `external.powersource.voltage = 12.65 V`, age < 2 h

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm latest message voltage | 12.65 V, fresh |
| 2 | Open tooltip | LATEST = **10/10** Excellent (green) |

**Test Data:**

```
latest_voltage: 12.65 V
message_age:    45 min
```

**Post-conditions:**
- LATEST=10 persisted

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-039

**Title:** Verify LATEST score boundaries at 12.20 V (7 pts), 11.90 V (4 pts), and below 11.90 V (0 pts)  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.6.a — traced to: red-Battery Study_v1.md §3.6 boundary table  
**Screen / Section:** Battery Health & Replacement Forecast — §3.6 LATEST Signal (boundaries)  
**Type:** Edge Case  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (telemetry pipeline)  
**Requirement Summary:** Boundary verification across the four LATEST tiers. Validates three transitions in one TC.

**Preconditions:**
- Four seeded states: 12.20 V, 12.19 V, 11.90 V, 11.89 V

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Seed latest = 12.20 V and recalc | LATEST = **7/10** |
| 2 | Seed latest = 12.19 V and recalc | LATEST = **4/10** |
| 3 | Seed latest = 11.90 V and recalc | LATEST = **4/10** |
| 4 | Seed latest = 11.89 V and recalc | LATEST = **0/10** |

**Test Data:**

```
boundaries: 12.20 / 12.19 / 11.90 / 11.89 V
expected:   7 / 4 / 4 / 0 pts
```

**Post-conditions:**
- All four boundary scores correct in `score_history`

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-040

**Title:** Verify scoring LATEST signal as 0 pts when the latest powersource voltage is < 11.90 V  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.6.a — traced to: red-Battery Study_v1.md §3.6 Critical tier  
**Screen / Section:** Battery Health & Replacement Forecast — §3.6 LATEST Signal  
**Type:** Negative  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (telemetry pipeline)  
**Requirement Summary:** Critical tier (<11.90 V) scores 0 pts — vehicle is in immediate trouble.

**Preconditions:**
- Latest voltage = 11.50 V

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm latest = 11.50 V | Reads 11.50 V |
| 2 | Open tooltip | LATEST = **0/10** Critical (red) |

**Test Data:**

```
latest_voltage: 11.50 V
```

**Post-conditions:**
- LATEST=0 persisted

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-041  🟧 PENDING

**Title:** Verify scoring LATEST signal as 5 pts neutral fallback when no telemetry message exists in the configured stale-data window  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.6.b — traced to: red-Battery Study_v1.md §3.6 (neutral fallback)  
**Screen / Section:** Battery Health & Replacement Forecast — §3.6 LATEST Signal (Neutral fallback)  
**Type:** Edge Case  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (telemetry pipeline)  
**Requirement Summary:** NEW v4 coverage. When the device has no telemetry within the stale-data window, LATEST falls back to 5 pts neutral. Window not stated — assumed 24 h pending Q4.

**Preconditions:**
- Device has no message in the last 24 h (offline)

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Confirm no recent message | Last message age > 24 h |
| 2 | Open tooltip | LATEST = **5/10** Neutral (grey) with text "No live data" |

**Test Data:**

```
last_message_age_h: 48
stale_window_h:     24 (assumed pending Q4)
```

**Post-conditions:**
- LATEST=5 persisted with `fallback_reason='no_telemetry'`

**Automation Candidate:** Yes — once window is confirmed.  
**Status:** Not Run  
**Notes:** **Blocked by Q4 (CQ-Q4).** Closes review §3.6 neutral-fallback gap.

---

## Forecast Logic (§4)

### Test Case: BATT-042

**Title:** Verify forecast base projection equals (live_voltage − 11.5) / abs(slope_per_day) clamped to 0–90 days  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-4.a — traced to: red-Battery Study_v1.md §4 Step 1  
**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast (Base projection)  
**Type:** Functional  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (forecast pipeline)  
**Requirement Summary:** Base forecast = (live_voltage − 11.5) / abs(slope_per_day), clamped to [0, 90] days. Validates the core projection formula before any modifiers are applied.

**Preconditions:**
- live_voltage = 12.50 V, slope = −0.010 V/day → expected raw = 100 → clamped to 90

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Seed inputs and trigger forecast | Forecast runs |
| 2 | Inspect `forecast_audit.base_days` | 100 (pre-clamp) |
| 3 | Inspect `forecast_audit.base_clamped` | 90 (after clamp to max) |

**Test Data:**

```
live_voltage:  12.50 V
slope_per_day: -0.010 V/day
expected_base: 100 -> clamped to 90
```

**Post-conditions:**
- `forecast_audit.base_clamped = 90`

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-043

**Title:** Verify forecast base is set to 90 days when slope is flat (≈0) or positive  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-4.b — traced to: red-Battery Study_v1.md §4 Step 1 "If slope is flat or positive (stable battery) → base = 90 days"  
**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast (Flat/positive slope)  
**Type:** Edge Case  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (forecast pipeline)  
**Requirement Summary:** Prevents division-by-zero and infinite forecasts. When slope ≈ 0 or positive, base is set to the 90-day ceiling regardless of voltage.

**Preconditions:**
- live_voltage = 12.40 V; three slope cases (+0.001, 0.0, −1e-6)

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Run forecast with slope = +0.001 V/day | base_days = 90 |
| 2 | Repeat with slope = 0.0 | base_days = 90 |
| 3 | Repeat with slope = −1e-6 (essentially flat) | base_days = 90 (clamped from a huge value) |

**Test Data:**

```
slope_positive: +0.001
slope_zero:      0.0
slope_flat:     -1e-6
```

**Post-conditions:**
- No division-by-zero errors; base capped at 90 d in all three cases

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-044  🟧 PENDING

**Title:** Verify forecast applies modifier compounding correctly after the redundancy guard de-duplicates correlated conditions  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-4.c + REQ-4.d — traced to: red-Battery Study_v1.md §4 Steps 2 & 3  
**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast (Modifiers + redundancy guard)  
**Type:** Functional  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (forecast pipeline)  
**Requirement Summary:** Modifiers are multiplied after the redundancy guard de-duplicates correlated conditions. Spec gives `rest<11.8 + deep_discharge` as one correlated pair (keep harsher). Full pair list pending Q9.

**Preconditions:**
- Vehicle has 3 active modifiers: `crank<9.5` (×0.5), `rest<11.8` (×0.5), `deep_discharge>=2` (×0.7)
- Redundancy guard knows `rest<11.8` and `deep_discharge` are correlated

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Run forecast | Pipeline completes |
| 2 | Inspect `forecast_audit.modifier_list_pre_guard` | Contains all 3 modifiers |
| 3 | Inspect `forecast_audit.modifier_list_post_guard` | Contains `crank<9.5` + `rest<11.8` (the harsher of the correlated pair); `deep_discharge` dropped |
| 4 | Verify the final multiplier | Equals 0.5 × 0.5 = **0.25** (rest kept over deep) |

**Test Data:**

```
modifiers_in:        crank<9.5 (×0.5), rest<11.8 (×0.5), deep>=2 (×0.7)
expected_post_guard: crank<9.5, rest<11.8 (deep dropped)
expected_multiplier: 0.25
```

**Post-conditions:**
- `forecast_audit.final_multiplier = 0.25 ± 0.001`

**Automation Candidate:** Yes — once full pair list is confirmed.  
**Status:** Not Run  
**Notes:** **Blocked by Q9 (CQ-Q9)** — complete list of redundancy-guard correlated pairs not stated in spec.

---

### Test Case: BATT-045  🟧 PENDING

**Title:** Verify forecast is clamped to 14 days AND band is forced to Critical when modifier stack would push below 14 days  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-4.e — traced to: red-Battery Study_v1.md §4 Step 4 "Floor & Override Rules"  
**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast (14-day floor + Critical override)  
**Type:** Edge Case  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (forecast pipeline)  
**Requirement Summary:** Minimum forecast = 14 days. Any modifier stack that would push below 14 is clamped to 14 AND the band is forced to Critical regardless of score.

**Preconditions:**
- Seeded vehicle: base=60 d, combined multiplier=0.10 → raw forecast = 6 d (pre-clamp)
- Score sums to 78 (Fair range) — would normally band Fair, not Critical

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Run forecast | Pipeline completes |
| 2 | Inspect `forecast_audit.forecast_days_raw` | 6 (pre-clamp) |
| 3 | Inspect `forecast_audit.forecast_days_final` | 14 (clamped) |
| 4 | Inspect `forecast_audit.final_band` | Critical (override applied despite score=78) |
| 5 | Open tooltip | Forecast shown as "14 days"; band label = Critical (red) |

**Test Data:**

```
base_days:           60
combined_multiplier: 0.10
raw_forecast:         6
expected_final:      14
expected_band:       Critical
score:               78
```

**Post-conditions:**
- forecast=14; band=Critical; `override_reason='floor_breach'`

**Automation Candidate:** Yes — once staging data is available.  
**Status:** Not Run  
**Notes:** **Blocked by CQ-003 (Q6)** — need a sandbox vehicle whose modifier stack produces sub-14-day base.

---

### Test Case: BATT-046

**Title:** Verify forecast resets to 90 days when calc 2805166 (Battery Replacement) fires within the last 24 hours  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-4.f — traced to: red-Battery Study_v1.md §4 Step 4 "Replacement override"  
**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast (Replacement override)  
**Type:** Edge Case  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805166, forecast pipeline)  
**Requirement Summary:** If calc 2805166 fires within 24 h, the forecast resets to 90 days regardless of all other inputs. Ensures fleet operators see a fresh forecast after a confirmed battery swap.

**Preconditions:**
- Vehicle had a 14 d forecast before the swap
- Calc 2805166 emitted a replacement event 2 h ago

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Inspect `forecast_audit.replacement_event_age` | 2 h |
| 2 | Inspect `forecast_audit.forecast_days_final` | 90 (override) |
| 3 | Inspect band | Excellent (override drives band as well) |
| 4 | Confirm override logged | `forecast_audit.override_reason = 'battery_replacement'` |

**Test Data:**

```
calc_2805166_age_h: 2
forecast_before:    14
forecast_after:     90
```

**Post-conditions:**
- forecast=90, band=Excellent for the 24 h window after the replacement event

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** Window semantics (rolling 24 h vs calendar day) per Q14.

---

### Test Case: BATT-047

**Title:** Verify a healthy vehicle scores 100 points end-to-end and lands in the Excellent band with a 90-day forecast  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-2.a + REQ-5.a — traced to: red-Battery Study_v1.md §2 + §5  
**Screen / Section:** Battery Health & Replacement Forecast — §2 + §5 (End-to-end happy path)  
**Type:** Functional  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (all signal calcs + forecast pipeline)  
**Requirement Summary:** Happy-path end-to-end: a healthy fleet vehicle scores all 6 signals at max → 100 → Excellent band → 90-day forecast. Primary smoke TC for the pipeline.

**Preconditions:**
- All 6 signals at max: REST=30, CRANK=25, TREND=12, DECAY=13, CHARGE=10, LATEST=10
- No modifiers armed

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Run the full pipeline | Pipeline completes without errors |
| 2 | Read total score on the dashboard chip | 100 |
| 3 | Read forecast on the row | 90 days |
| 4 | Read band | Excellent (green) |
| 5 | Open tooltip | All 6 rows green; summary line reads "Battery is healthy" |

**Test Data:**

```
rest:30 crank:25 trend:12 decay:13 charge:10 latest:10 -> 100
expected_forecast: 90 d
expected_band:     Excellent
```

**Post-conditions:**
- score=100, forecast=90, band=Excellent in `score_history`

**Automation Candidate:** Yes — primary smoke test.  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-048

**Title:** Verify forecast base is clamped to zero when live voltage is at or below the 11.5 V floor  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-4.g — traced to: red-Battery Study_v1.md §4 Step 1 clamp lower bound  
**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast (Clamp lower bound)  
**Type:** Edge Case  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (forecast pipeline)  
**Requirement Summary:** Base must clamp to 0 (not go negative) when live voltage is at/below the 11.5 V floor. Final forecast is then promoted to 14 by the floor rule, and band forced to Critical.

**Preconditions:**
- live_voltage = 11.30 V, slope = −0.005 V/day → raw = −40

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Run forecast | Runs without error |
| 2 | Inspect `forecast_audit.base_days_raw` | −40 |
| 3 | Inspect `forecast_audit.base_days_clamped` | 0 |
| 4 | Read the final forecast after floor | 14 (forced by floor rule) |
| 5 | Read the band | Critical |

**Test Data:**

```
live_voltage: 11.30 V
slope:        -0.005 V/day
```

**Post-conditions:**
- No negative forecast leaks downstream; final=14; band=Critical

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-049

**Title:** Verify forecast applies ×0.7 modifier when calc 2805152 records 2 or more deep-discharge events  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-4.c — traced to: red-Battery Study_v1.md §4 Step 2 "Deep discharges ≥ 2 events × 0.7"  
**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast (Deep Discharge modifier)  
**Type:** Functional  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805152, forecast pipeline)  
**Requirement Summary:** Deep-discharge events ≥ 2 in 30 d apply the ×0.7 forecast modifier — battery damaged by being run flat.

**Preconditions:**
- Calc 2805152 fired 3 times in last 30 d; no other modifiers

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Inspect `forecast_audit.modifier_list` | Contains `deep_discharge>=2_x0.7` |
| 2 | Compute expected forecast | base × 0.7 |
| 3 | Verify forecast value | Matches expectation within ±1 d rounding |

**Test Data:**

```
deep_discharge_events: 3
expected_modifier:     0.7
```

**Post-conditions:**
- `forecast_audit` shows ×0.7 applied

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-050

**Title:** Verify forecast applies ×0.6 modifier when calc 2805149 records 1 or more alternator-failure events  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-4.c — traced to: red-Battery Study_v1.md §4 Step 2 "Alternator failures ≥ 1 × 0.6"  
**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast (Alternator modifier)  
**Type:** Functional  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc 2805149, forecast pipeline)  
**Requirement Summary:** ≥ 1 alternator-failure event applies ×0.6 modifier — charging system unreliable.

**Preconditions:**
- Calc 2805149 fired once in last 30 d; no other modifiers

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Inspect `forecast_audit.modifier_list` | Contains `alternator>=1_x0.6` |
| 2 | Verify forecast value | = base × 0.6 |

**Test Data:**

```
alternator_events: 1
expected_modifier: 0.6
```

**Post-conditions:**
- `forecast_audit` shows ×0.6 applied

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-051

**Title:** Verify CRANK ×0.5 forecast modifier fires when compensated crank_dip is < 9.5 V even at the 13-pt scoring tier  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.2.e — traced to: red-Battery Study_v1.md §3.2 + §4 (review §4.3 gap)  
**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast (CRANK modifier threshold)  
**Type:** Regression  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (forecast pipeline)  
**Requirement Summary:** NEW v4 coverage. The ×0.5 CRANK modifier must fire at ANY compensated crank_dip < 9.5 V — not only at the 0-pt score boundary (<8.0 V). A vehicle scoring 13 CRANK points still arms the modifier.

**Preconditions:**
- Compensated min crank_dip = 9.20 V (→ CRANK score 13 pts, see BATT-011)

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Trigger pipeline | Runs |
| 2 | Inspect CRANK score | 13/25 |
| 3 | Inspect `forecast_audit.modifier_list` | Contains `crank<9.5_x0.5` |
| 4 | Verify the final forecast | Has ×0.5 applied |

**Test Data:**

```
min_crank_compensated: 9.20 V
expected_score:        13
expected_modifier:     0.5
```

**Post-conditions:**
- ×0.5 modifier active despite CRANK score being above 0

**Automation Candidate:** Yes — strong regression candidate.  
**Status:** Not Run  
**Notes:** Closes review §4.3 gap. Modifier threshold (9.5) confirmed independent of 0-pt score threshold (8.0).

---

## Health Bands (§5)

### Test Case: BATT-052

**Title:** Verify health band transitions cleanly from Excellent (95 pts) to Good (94 pts) at the 95-point boundary  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-5.a — traced to: red-Battery Study_v1.md §5 Excellent/Good boundary  
**Screen / Section:** Battery Health & Replacement Forecast — §5 Health Bands  
**Type:** Edge Case  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (banding logic)  
**Requirement Summary:** Excellent band requires 95–100. Vehicle at 95 = Excellent; vehicle at 94 = Good. Validates the most prestige boundary.

**Preconditions:**
- Two seeded scores: 95 and 94, both with forecast=90

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Seed score=95 and recalc | Band = Excellent (green dot) |
| 2 | Seed score=94 and recalc | Band = Good (green dot, different label) |

**Test Data:**

```
score_a:  95
score_b:  94
forecast: 90 d
```

**Post-conditions:**
- A: band=Excellent; B: band=Good

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-053

**Title:** Verify band lands at the most-restrictive value when score and forecast disagree  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-5.b — traced to: red-Battery Study_v1.md §5 "most restrictive"  
**Screen / Section:** Battery Health & Replacement Forecast — §5 Health Bands (Most-restrictive rule)  
**Type:** Functional  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (banding logic)  
**Requirement Summary:** Vehicle lands in the most-restrictive band triggered by either score OR forecast. Good score (85) with Poor-range forecast (25 d) must band Poor, not Good.

**Preconditions:**
- Score=85 (Good range); forecast=25 d (Poor range)

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Run pipeline | Runs |
| 2 | Inspect band | Poor (orange) — driven by forecast, not score |
| 3 | Inspect `band_audit.source` | `forecast` |

**Test Data:**

```
score:         85
forecast_days: 25
```

**Post-conditions:**
- band=Poor; `band_audit.source = 'forecast'`

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** Band downgrade direction (downgrade-only) per Q15.

---

### Test Case: BATT-054

**Title:** Verify Fair band when score is 72 and forecast is 38 days  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-5.a — traced to: red-Battery Study_v1.md §5 Fair tier  
**Screen / Section:** Battery Health & Replacement Forecast — §5 Health Bands  
**Type:** Functional  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (banding logic)  
**Requirement Summary:** Fair band: score 65–79 OR forecast 30–44 days.

**Preconditions:**
- score=72, forecast=38 d

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Run pipeline | Runs |
| 2 | Inspect band | Fair (amber) |

**Test Data:**

```
score:         72
forecast_days: 38
```

**Post-conditions:**
- band=Fair

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-055

**Title:** Verify Poor band when score is 57 and forecast is 32 days  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-5.a — traced to: red-Battery Study_v1.md §5 Poor tier  
**Screen / Section:** Battery Health & Replacement Forecast — §5 Health Bands  
**Type:** Functional  
**Priority:** Medium  
**Environment:** Mixed — Web (Chrome 120+) + Backend (banding logic)  
**Requirement Summary:** Poor band: score 50–64 OR forecast <30 days.

**Preconditions:**
- score=57, forecast=32 d (score drives Poor)

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Run pipeline | Runs |
| 2 | Inspect band | Poor (orange) |

**Test Data:**

```
score:         57
forecast_days: 32
```

**Post-conditions:**
- band=Poor

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-056

**Title:** Verify Critical band when total score is under 50 and REPLACE badge fires  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-5.a + Status spec REPLACE trigger — traced to: red-Battery Study_v1.md §5 + Status spec  
**Screen / Section:** Battery Health & Replacement Forecast — §5 Health Bands (Critical) + Status Column Spec  
**Type:** Negative  
**Priority:** High  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)  
**Requirement Summary:** Critical band fires when score <50 OR forecast <14 days. REPLACE badge appears alongside.

**Preconditions:**
- score=42, forecast >14 d (so band is score-driven)

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Run pipeline | Runs |
| 2 | Inspect band | Critical (red) |
| 3 | Inspect the Status column on the row | REPLACE badge visible |

**Test Data:**

```
score: 42
```

**Post-conditions:**
- band=Critical; REPLACE badge active

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-057

**Title:** Verify Good score is downgraded to Fair band when forecast lands in [30, 45) days  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-5.c — traced to: red-Battery Study_v1.md §5 (review §4.5)  
**Screen / Section:** Battery Health & Replacement Forecast — §5 Health Bands (Forecast override)  
**Type:** Edge Case  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (banding logic)  
**Requirement Summary:** NEW v4 coverage. A Good-band score (e.g. 85) combined with a Fair-band forecast (30–44 d) must downgrade to Fair via the most-restrictive rule. Review §4.5 flagged this gap.

**Preconditions:**
- score=85 (Good); forecast=40 d (Fair)

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Run pipeline | Runs |
| 2 | Inspect band | Fair — forecast wins |
| 3 | Inspect `band_audit` | source=`forecast`; original_score_band=`Good` |

**Test Data:**

```
score:         85
forecast_days: 40
expected_band: Fair
```

**Post-conditions:**
- band=Fair; `band_audit.source = 'forecast'`

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** Closes review §4.5 gap.

---

## Score Formula (§2 + Regression)

### Test Case: BATT-058

**Title:** Verify the score formula maxes sum to exactly 100 points across all 6 signals in v2.2  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-2.a — traced to: red-Battery Study_v1.md §2 + Score Rebalancing Summary  
**Screen / Section:** Battery Health & Replacement Forecast — §2 Score Formula  
**Type:** Regression  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (config inspection)  
**Requirement Summary:** Sum of all signal max weights must equal 100 in v2.2. Guards against rebalancing arithmetic errors.

**Preconditions:**
- Pipeline running v2.2 weightings

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Inspect the signal-weight table in pipeline config | REST 30 + CRANK 25 + TREND 12 + DECAY 13 + CHARGE 10 + LATEST 10 |
| 2 | Compute the sum | = 100 |

**Test Data:**

```
weights: 30 + 25 + 12 + 13 + 10 + 10 = 100
```

**Post-conditions:**
- Sum check passes; no drift from v2.2 specification

**Automation Candidate:** Yes — trivial sum-check unit test.  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-059

**Title:** Verify pipeline applies v2.2 weightings (REST=30, TREND=12, DECAY=13, CHARGE=10) and no longer uses v2.1 weightings  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-2.b — traced to: red-Battery Study_v1.md "Score Rebalancing Summary"  
**Screen / Section:** Battery Health & Replacement Forecast — §2 Score Formula (v2.1 → v2.2 regression)  
**Type:** Regression  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (config + score history)  
**Requirement Summary:** v2.2 introduces CHARGE (+10) and rebalances REST (35→30), TREND (15→12), DECAY (15→13). No production code may still use v2.1 weights.

**Preconditions:**
- Pipeline build = v2.2
- Reference vehicle with known scores under both schemes

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Inspect signal-weight config in code | Matches v2.2 exactly |
| 2 | Re-score the reference vehicle | Score matches v2.2 expectation, not v2.1 |
| 3 | Inspect score record version stamp | Reads `v2.2` |

**Test Data:**

```
v2_1_weights: rest=35, trend=15, decay=15, charge=0
v2_2_weights: rest=30, trend=12, decay=13, charge=10
```

**Post-conditions:**
- Score record stamped `v2.2`

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** Version stamp field name per Q17.

---

### Test Case: BATT-060

**Title:** Verify MURANO test vehicle drops from 100 to 90 between v2.1 and v2.2 due to CHARGE signal addition  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-2.c — traced to: red-Battery Study_v1.md §3.5 "Key insight (MURANO 100 → 90)"  
**Screen / Section:** Battery Health & Replacement Forecast — §2 + §3.5 (MURANO regression)  
**Type:** Regression  
**Priority:** High  
**Environment:** Mixed — Web (Chrome 120+) + Backend (pipeline replay)  
**Requirement Summary:** Real-world regression. MURANO scored 100/100 under v2.1 but drops to 90/100 under v2.2 because CHARGE (abs%=72) is now part of the formula. Locks in the bug fix.

**Preconditions:**
- MURANO reference dataset replayed against v2.1 and v2.2 pipelines

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Score MURANO with v2.1 pipeline | 100/100 (Excellent) |
| 2 | Score MURANO with v2.2 pipeline | 90/100 (Good); CHARGE = 0/10 (abs%=72) |
| 3 | Confirm band change | v2.1: Excellent; v2.2: Good |

**Test Data:**

```
vehicle:        MURANO
v2_1_score:     100 (Excellent)
v2_2_score:      90 (Good)
charge_in_v2_2:   0/10 (abs=72%)
```

**Post-conditions:**
- Both scores reproducible; v2.2 reflects the duty-cycle reality

**Automation Candidate:** Yes — frozen reference replay.  
**Status:** Not Run  
**Notes:** 

---

## Status Column / Badges

### Test Case: BATT-061  🟧 PENDING

**Title:** Verify all 8 Status column badges (DEEP DISCHARGE, ALTERNATOR, PARK DRAIN, TREND↓, CHARGE↓, SHORT↓, REPLACE, HEALTHY) fire under their documented trigger conditions  
**Feature:** Fleet Pulse: Status Column  
**Requirement ID:** REQ-Status.a — traced to: Fleet Pulse Status Column Spec (all 8 badge triggers)  
**Screen / Section:** Fleet Pulse: Status Column Spec (Badge triggers)  
**Type:** Functional  
**Priority:** High  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)  
**Requirement Summary:** The renamed Status column surfaces 8 badge types. Each must fire under its precise trigger condition.

**Preconditions:**
- 8 seeded test vehicles, each engineered to trigger exactly one badge

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Seed `deep_discharge_events=2` on vehicle 1 | DEEP DISCHARGE badge visible |
| 2 | Seed `alternator_events=1` on vehicle 2 | ALTERNATOR badge visible |
| 3 | Seed decay slope >0.015 V/hr on vehicle 3 | PARK DRAIN badge visible |
| 4 | Seed slope <−0.008 V/day on vehicle 4 | TREND↓ badge visible |
| 5 | Seed abs%<90 on vehicle 5 | CHARGE↓ badge visible (pending CQ-001 threshold) |
| 6 | Seed short%>70 on vehicle 6 | SHORT↓ badge visible |
| 7 | Seed score<50 or replacement event on vehicle 7 | REPLACE badge visible |
| 8 | Use clean healthy vehicle 8 (score=100, no events) | HEALTHY badge visible (no other badge active) |

**Test Data:**

```
vehicles:            8 seeded states
badge_count_per_row: 1
```

**Post-conditions:**
- Each vehicle row shows exactly the expected badge for its trigger

**Automation Candidate:** Yes — once CQ-001 and CQ-007 resolved.  
**Status:** Not Run  
**Notes:** **Blocked by CQ-007 (EV CHARGE↓ suppression) + CQ-001 (CHARGE↓ threshold).** Execute under current assumption and re-run after CQ closure.

---

### Test Case: BATT-062

**Title:** Verify multiple Status pills are ordered red, then amber, then green left-to-right on the row  
**Feature:** Fleet Pulse: Status Column  
**Requirement ID:** REQ-Status.b — traced to: Fleet Pulse Status Column Spec (Pill ordering)  
**Screen / Section:** Fleet Pulse: Status Column Spec (Pill ordering)  
**Type:** UI  
**Priority:** Medium  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)  
**Requirement Summary:** Multiple badges on a row must be ordered by severity: red first, then amber, then green. Drives operator attention to the worst signal first.

**Preconditions:**
- Vehicle seeded with REPLACE (red), TREND↓ (amber); HEALTHY is suppressed when others fire

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open the row | Pills render in order: REPLACE, TREND↓ |
| 2 | Confirm HEALTHY suppressed when any other badge fires | No green pill present |
| 3 | Repeat with ALTERNATOR (red) + CHARGE↓ (amber) + SHORT↓ (amber) | Order: ALTERNATOR, CHARGE↓, SHORT↓ |

**Test Data:**

```
case_a: REPLACE + TREND↓
case_b: ALTERNATOR + CHARGE↓ + SHORT↓
```

**Post-conditions:**
- Pills follow severity ordering rule

**Automation Candidate:** Yes — DOM-order assertion.  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-063  🟧 PENDING

**Title:** Verify Status column shows at most 3 pills and renders '+N more' overflow when more pills are active  
**Feature:** Fleet Pulse: Status Column  
**Requirement ID:** REQ-Status.c — traced to: Fleet Pulse Status Column Spec (Overflow)  
**Screen / Section:** Fleet Pulse: Status Column Spec (Overflow)  
**Type:** UI  
**Priority:** Medium  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)  
**Requirement Summary:** Maximum 3 visible pills per row; remaining pills collapse into a '+N more' chip. Prevents the column from growing arbitrarily wide.

**Preconditions:**
- Vehicle seeded with 5 simultaneous badges

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open the row | 3 pills visible in severity order |
| 2 | Confirm '+2 more' rendered after the 3rd pill | Overflow chip visible |
| 3 | Interact with the '+2 more' chip per PRD | Behaviour matches CQ-006 resolution (hover/click) |

**Test Data:**

```
active_badges:           REPLACE, ALTERNATOR, DEEP DISCHARGE, TREND↓, CHARGE↓ (5 total)
expected_visible:        3
expected_overflow_label: +2 more
```

**Post-conditions:**
- 3 pills + overflow chip rendered correctly

**Automation Candidate:** Partial — pill count assertable, interaction model depends on CQ-006.  
**Status:** Not Run  
**Notes:** **Blocked by CQ-006** — hover vs click interaction model TBD.

---

### Test Case: BATT-064

**Title:** Verify HEALTHY pill is shown on rows where no other badges fire so the Status column never renders empty  
**Feature:** Fleet Pulse: Status Column  
**Requirement ID:** REQ-Status.d — traced to: Fleet Pulse Status Column Spec (Always one pill)  
**Screen / Section:** Fleet Pulse: Status Column Spec (Always one pill)  
**Type:** Functional  
**Priority:** Medium  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)  
**Requirement Summary:** At least one pill must always render. HEALTHY appears when no other badges fire — ensures the column never looks empty.

**Preconditions:**
- Reference healthy vehicle: score=100, no events

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open the row | Single HEALTHY pill (green) renders |
| 2 | Trigger any other badge (e.g. seed `deep_discharge=2`) | HEALTHY disappears; new badge takes its place |
| 3 | Clear the trigger | HEALTHY re-appears |

**Test Data:**

```
reference_vehicle:    clean (no events)
badge_count_expected: 1 (HEALTHY)
```

**Post-conditions:**
- Status cell is never empty; HEALTHY appears only when alone

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-065  🟧 PENDING

**Title:** Verify Status column renders the correct plain-English summary line for each of the 9 canonical badge combinations  
**Feature:** Fleet Pulse: Status Column  
**Requirement ID:** REQ-Status.e — traced to: Fleet Pulse Status Column Spec (Summary line)  
**Screen / Section:** Fleet Pulse: Status Column Spec (Plain-English summary line)  
**Type:** Functional  
**Priority:** Medium  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)  
**Requirement Summary:** Each Status state shows a one-line plain-English summary below the pills. 9 combinations cover all canonical fleet scenarios.

**Preconditions:**
- 9 seeded vehicles, each in a canonical state per the Status spec

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | For each of the 9 vehicles, open the row | Summary line matches PRD text |
| 2 | Validate exact strings letter-for-letter against the spec | All 9 strings match exactly |

**Test Data:**

```
combinations:     9 (per Status spec)
expected_strings: see Status Column Spec page
```

**Post-conditions:**
- All 9 summary strings rendered correctly

**Automation Candidate:** Yes — once column header confirmed.  
**Status:** Not Run  
**Notes:** **Blocked by CQ-005** — final column header (Status / Active Alerts / Health Flags) still TBD.

---

### Test Case: BATT-066

**Title:** Verify Status column sorts rows by worst-severity badge first (red > amber > green)  
**Feature:** Fleet Pulse: Status Column  
**Requirement ID:** REQ-Status.f — traced to: Fleet Pulse Status Column Spec (Column sortability)  
**Screen / Section:** Fleet Pulse: Status Column Spec (Sortability)  
**Type:** UI  
**Priority:** Low  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)  
**Requirement Summary:** Status column sorts by worst severity per row, not alphabetically. Supports worst-first triage.

**Preconditions:**
- Fleet of 10 vehicles with a varied badge mix

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Click the Status column header | Sort indicator appears |
| 2 | Inspect row order | Red-badge rows at the top, amber next, green last |
| 3 | Click again to invert sort | Order reverses correctly |

**Test Data:**

```
vehicles:       10 mixed
expected_order: red-first then amber then green
```

**Post-conditions:**
- Sort order matches the severity rule

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-067

**Title:** Verify Status column hides the summary line and keeps pills visible on viewports narrower than 600 px  
**Feature:** Fleet Pulse: Status Column  
**Requirement ID:** REQ-Status.g — traced to: Fleet Pulse Status Column Spec (Mobile breakpoint)  
**Screen / Section:** Fleet Pulse: Status Column Spec (Mobile)  
**Type:** UI  
**Priority:** Low  
**Environment:** Web responsive — viewport 480–599 px (Chrome 120+ DevTools / iOS Safari)  
**Requirement Summary:** On viewports < 600 px the plain-English summary line must be hidden so badges remain readable; pills themselves remain.

**Preconditions:**
- Open Fleet Pulse on a viewport sized 599 px wide

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open Fleet Pulse at 599 px width | Status column renders |
| 2 | Inspect a row with 2 badges + summary line | Pills visible; summary line hidden |
| 3 | Resize to 600 px | Summary line becomes visible again |

**Test Data:**

```
viewport: 599 px (hide), 600 px (show)
```

**Post-conditions:**
- Summary line breakpoint behaves correctly across the boundary

**Automation Candidate:** Yes — responsive viewport snapshot.  
**Status:** Not Run  
**Notes:** 

---

## Health Score Tooltip

### Test Case: BATT-068

**Title:** Verify Health Score tooltip opens on hover/focus and closes on blur, mouseleave, and Escape  
**Feature:** Fleet Pulse: Health Score Tooltip  
**Requirement ID:** REQ-Tooltip.a — traced to: Fleet Pulse Health Score Tooltip Spec (Open/close)  
**Screen / Section:** Fleet Pulse: Health Score Tooltip Spec (Open/close interactions)  
**Type:** UI  
**Priority:** Medium  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)  
**Requirement Summary:** Tooltip opens on hover (desktop) and focus (keyboard). Closes on blur, mouseleave, or Escape. Critical for WCAG 2.1 keyboard accessibility.

**Preconditions:**
- Fleet Pulse dashboard open; any vehicle row visible

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Hover the Health Score chip | Tooltip opens within 150 ms |
| 2 | Move pointer off the chip | Tooltip closes |
| 3 | Tab focus to the chip via keyboard | Tooltip opens on focus |
| 4 | Press Escape | Tooltip closes; focus retained on the chip |
| 5 | Tab away from the chip | Tooltip closes on blur |

**Test Data:**

```
trigger: hover, focus
close:   blur, mouseleave, Escape
```

**Post-conditions:**
- All 5 interactions behave per spec

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-069

**Title:** Verify Health Score tooltip renders 6 sub-signal rows with friendly labels (not raw values or formula weights)  
**Feature:** Fleet Pulse: Health Score Tooltip  
**Requirement ID:** REQ-Tooltip.b — traced to: Fleet Pulse Health Score Tooltip Spec (Sub-signal rows)  
**Screen / Section:** Fleet Pulse: Health Score Tooltip Spec (Sub-signal rows)  
**Type:** UI  
**Priority:** Medium  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)  
**Requirement Summary:** Tooltip shows 6 rows (one per signal) with friendly labels (e.g. "Rest voltage", "Cranking strength"). Must NOT show raw values or weights.

**Preconditions:**
- Tooltip open on a vehicle row

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Read the 6 row labels | REST→"Rest voltage", CRANK→"Cranking strength", TREND→"Trend", DECAY→"Park drain", CHARGE→"Charging quality", LATEST→"Latest reading" |
| 2 | Confirm no row shows raw V or V/hr | No raw numeric readings displayed |
| 3 | Confirm no row shows weight (e.g. "/30") | No `/N` weight tokens displayed |

**Test Data:**

```
expected_labels: Rest voltage / Cranking strength / Trend / Park drain / Charging quality / Latest reading
```

**Post-conditions:**
- 6 rows present with the correct friendly labels

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-070  🟧 PENDING

**Title:** Verify Health Score tooltip dot colours follow the ≥80% green / 40–79% amber / <40% red rule across all 6 rows  
**Feature:** Fleet Pulse: Health Score Tooltip  
**Requirement ID:** REQ-Tooltip.c — traced to: Fleet Pulse Health Score Tooltip Spec (Dot colour thresholds)  
**Screen / Section:** Fleet Pulse: Health Score Tooltip Spec (Dot colours)  
**Type:** UI  
**Priority:** Medium  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)  
**Requirement Summary:** Dot colour rule: ≥80% green, 40–79% amber, <40% red (where % = score / max for that signal). Drives the at-a-glance row colours.

**Preconditions:**
- 3 seeded vehicles producing one row at each colour, plus boundary samples at 40% and 80%

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open tooltip on the green-row vehicle | All 6 dots green (each signal ≥80%) |
| 2 | Open tooltip on the amber-row vehicle | Each ≥40% and <80% renders amber |
| 3 | Open tooltip on the red-row vehicle | Each <40% renders red |
| 4 | Test exactly at the 40% boundary | Behaviour matches CQ-004 resolution |
| 5 | Test exactly at the 80% boundary | Green per spec |

**Test Data:**

```
thresholds:     green ≥80%, amber 40-79%, red <40%
boundary_cases: 40%, 80%
```

**Post-conditions:**
- Dot colours match thresholds at all percentages

**Automation Candidate:** Yes — once 40% inclusivity is fixed.  
**Status:** Not Run  
**Notes:** **Blocked by CQ-004** — 40% boundary inclusion still TBD.

---

### Test Case: BATT-071

**Title:** Verify Health Score tooltip displays neither formula weights (e.g. /30) nor raw voltage values  
**Feature:** Fleet Pulse: Health Score Tooltip  
**Requirement ID:** REQ-Tooltip.d — traced to: Fleet Pulse Health Score Tooltip Spec (No raw values / weights)  
**Screen / Section:** Fleet Pulse: Health Score Tooltip Spec (No raw values)  
**Type:** UI  
**Priority:** Medium  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)  
**Requirement Summary:** Tooltip is for non-technical operators. Formula weights (e.g. "/30") and raw V readings must not appear in the tooltip body.

**Preconditions:**
- Tooltip open on a healthy vehicle

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Inspect tooltip body text for weight tokens | No occurrences of `/30`, `/25`, `/12`, `/13`, `/10` |
| 2 | Inspect tooltip body text for raw units | No occurrences of `V`, `°C`, `V/day`, `V/hr` with numbers |
| 3 | Inspect tooltip body | Only friendly labels and dot colours present |

**Test Data:**

```
forbidden_tokens: /30 /25 /12 /13 /10 V V/hr V/day
```

**Post-conditions:**
- No forbidden tokens present in tooltip DOM

**Automation Candidate:** Yes — regex assertion on rendered DOM.  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-072

**Title:** Verify Health Score tooltip band label uses the documented hex colour for each of the 5 bands  
**Feature:** Fleet Pulse: Health Score Tooltip  
**Requirement ID:** REQ-Tooltip.e — traced to: Fleet Pulse Health Score Tooltip Spec (Band label colour)  
**Screen / Section:** Fleet Pulse: Health Score Tooltip Spec (Band label colour)  
**Type:** UI  
**Priority:** Medium  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)  
**Requirement Summary:** Band label inside the tooltip is colour-coded per band hex: Excellent #1B873F, Good #2E7D32, Fair #F4A300, Poor #E76F00, Critical #C0392B.

**Preconditions:**
- 5 seeded vehicles, one per band

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open tooltip on the Excellent vehicle | Band label colour = #1B873F |
| 2 | Open tooltip on the Good vehicle | = #2E7D32 |
| 3 | Open tooltip on the Fair vehicle | = #F4A300 |
| 4 | Open tooltip on the Poor vehicle | = #E76F00 |
| 5 | Open tooltip on the Critical vehicle | = #C0392B |

**Test Data:**

```
hexes: 1B873F, 2E7D32, F4A300, E76F00, C0392B
```

**Post-conditions:**
- All 5 band labels render the correct hex

**Automation Candidate:** Yes — computed-style colour comparison.  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-073

**Title:** Verify Health Score tooltip opens as a modal sheet on tap when viewport is narrower than 480 px  
**Feature:** Fleet Pulse: Health Score Tooltip  
**Requirement ID:** REQ-Tooltip.f — traced to: Fleet Pulse Health Score Tooltip Spec (Mobile modal)  
**Screen / Section:** Fleet Pulse: Health Score Tooltip Spec (Mobile)  
**Type:** UI  
**Priority:** Low  
**Environment:** Web responsive — viewport <480 px (Chrome 120+ DevTools / iOS Safari)  
**Requirement Summary:** On viewports < 480 px the tooltip opens as a tap-to-open modal sheet rather than an inline tooltip. Tap-anywhere-to-close dismisses.

**Preconditions:**
- Fleet Pulse open on a mobile viewport 479 px wide

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Tap the Health Score chip | Modal sheet opens (full-width, centered) |
| 2 | Tap outside the modal | Modal closes |
| 3 | Resize to 480 px and tap again | Inline tooltip behaviour returns |

**Test Data:**

```
viewport: 479 px (modal), 480 px (tooltip)
```

**Post-conditions:**
- Breakpoint switches presentation correctly across the boundary

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

## General UI Display

### Test Case: BATT-074

**Title:** Verify all 6 sub-signal rows are visible inside the Health Score tooltip without internal scrolling on default desktop viewport  
**Feature:** Fleet Pulse: Health Score Tooltip  
**Requirement ID:** REQ-UI.a — traced to: Fleet Pulse Health Score Tooltip Spec + general dashboard design  
**Screen / Section:** Fleet Pulse: Health Score Tooltip Spec (Layout)  
**Type:** UI  
**Priority:** Medium  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+) — viewport ≥ 1024 px  
**Requirement Summary:** All 6 sub-signal rows must fit inside the default tooltip viewport without internal scrolling on a 1024 px+ viewport at 100% zoom.

**Preconditions:**
- Browser viewport ≥ 1024 px wide, default zoom 100%

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open the tooltip on a vehicle row | Tooltip opens |
| 2 | Count visible sub-signal rows | All 6 rows fully visible |
| 3 | Confirm no scrollbar in the tooltip body | No scrollbar |

**Test Data:**

```
viewport_min_width: 1024 px
zoom:               100%
```

**Post-conditions:**
- No internal scroll on tooltip; all 6 rows rendered

**Automation Candidate:** Yes — geometry assertion.  
**Status:** Not Run  
**Notes:** 

---

### Test Case: BATT-075

**Title:** Verify forecast is displayed as relative days (e.g. "47 days") not as a calendar date  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-UI.b — traced to: red-Battery Study_v1.md §4 forecast display  
**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast display  
**Type:** UI  
**Priority:** Medium  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)  
**Requirement Summary:** Forecast must display as relative days (e.g. "47 days"), NOT a calendar date. Avoids timezone confusion across the fleet.

**Preconditions:**
- Vehicle with forecast = 47 d

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open the vehicle row | Forecast renders as "47 days" |
| 2 | Inspect the forecast cell DOM | No date format (YYYY-MM-DD or similar) present |

**Test Data:**

```
forecast_days:    47
expected_display: "47 days"
```

**Post-conditions:**
- Display matches expected format

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** 

---

## WeatherAPI Temperature Fallback

### Test Case: BATT-076

**Title:** Verify CRANK temperature compensation falls back to the most recent GPS fix within 7 days when current fix is missing  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.2.b (Weather fallback) — traced to: review §4.10  
**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal (WeatherAPI fallback)  
**Type:** Edge Case  
**Priority:** Low  
**Environment:** Mixed — Web (Chrome 120+) + Backend (WeatherAPI integration)  
**Requirement Summary:** NEW v4 coverage. When the vehicle has no GPS fix at the crank event time, WeatherAPI cannot resolve ambient temperature directly. The pipeline must fall back to the last-known fix within 7 days.

**Preconditions:**
- Vehicle has a crank event with no concurrent GPS fix
- Last known GPS fix was 3 days ago at a location whose WeatherAPI temp = 18 °C

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Run the CRANK pipeline on the event | Pipeline runs |
| 2 | Inspect `forecast_audit.temp_source` | `last_known_fix_within_7d` |
| 3 | Inspect `forecast_audit.ambient_temp_c` | 18 °C |
| 4 | Inspect `forecast_audit.compensated_crank_dip` | Computed using 18 °C, not the 25 °C default |

**Test Data:**

```
event_has_gps:     false
last_fix_age_days: 3
last_fix_temp_c:   18
```

**Post-conditions:**
- `forecast_audit.temp_source = 'last_known_fix_within_7d'`

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** Closes review §4.10 gap (no GPS scenario).

---

### Test Case: BATT-077

**Title:** Verify CRANK temperature compensation falls back to 25 °C baseline when no GPS fix exists within the last 7 days  
**Feature:** Battery Health & Replacement Forecast  
**Requirement ID:** REQ-3.2.b (Weather fallback) — traced to: review §4.10  
**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal (WeatherAPI fallback)  
**Type:** Edge Case  
**Priority:** Low  
**Environment:** Mixed — Web (Chrome 120+) + Backend (WeatherAPI integration)  
**Requirement Summary:** NEW v4 coverage. When no GPS fix exists in the last 7 days either, the pipeline falls back to the 25 °C baseline (zero adjustment) and logs a warning.

**Preconditions:**
- No GPS fix in the last 7 days for the vehicle

**Test Steps:**

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Run the CRANK pipeline on a crank event in this state | Pipeline runs |
| 2 | Inspect `forecast_audit.temp_source` | `baseline_default` |
| 3 | Inspect `forecast_audit.ambient_temp_c` | 25 °C |
| 4 | Inspect the compensation factor | 0.025 × (25 − 25) = 0 (no adjustment) |
| 5 | Inspect `forecast_audit.warnings` | Contains `temp_fallback_baseline` |

**Test Data:**

```
last_fix_age_days: 12
fallback_temp_c:   25
```

**Post-conditions:**
- `temp_source = 'baseline_default'`; warning logged

**Automation Candidate:** Yes  
**Status:** Not Run  
**Notes:** Closes review §4.10 gap (no fix within 7 d). Hot-side compensation clamp behaviour per Q16.

---

## Clarify Requirements (CQ Log)

> Orange (`#FFC000`) rows in the Excel export. Linked TCs are flagged PENDING until resolution.

| Ref # | Related TC ID | Source / Reference | Conflict Description | Question to Client | Priority | Raised By | Raised Date | Answer / Resolution | Status | Resolved Date |
|-------|---------------|--------------------|----------------------|--------------------|----------|-----------|-------------|---------------------|--------|---------------|
| CQ-001 | BATT-037, BATT-061 | Fleet Pulse: Status Column Spec — CHARGE↓ badge threshold | Spec lists CHARGE score thresholds at <80 % (4 pts) and <90 % (7 pts) but the Status Column Spec describes the CHARGE↓ badge as firing when "absorption is low" without a numeric cut-off. | Does the CHARGE↓ badge fire at absorption <90 % (matching the 7-pt tier) or only <80 % (matching the 0-pt tier)? | High | Hanna Lee | 2026-05-17 |  | Open |  |
| CQ-002 | BATT-033 | Battery Health & Replacement Forecast — §3.5 CHARGE Signal | The 4-pt CHARGE tier requires only absorption ≥80 % — the short-trip fraction is not constrained at this tier. Unclear whether a vehicle with abs=82 % and short=85 % should land in 4 pts or 0 pts. | At the 4-pt CHARGE tier, is the short-trip fraction ignored, or does an implicit short<70 % rule carry forward from the 7-pt tier? | Medium | Hanna Lee | 2026-05-17 |  | Open |  |
| CQ-003 | BATT-045 | Battery Health & Replacement Forecast — §4 Forecast Logic | Need a vehicle in staging whose modifier stack drives the forecast below 14 days so the floor + Critical override is testable. | Can the test team be provided with a sandbox vehicle/seeded data where (slope, modifiers) produce a base forecast <14 d before clamp? | High | Hanna Lee | 2026-05-17 |  | Open |  |
| CQ-004 | BATT-070 | Fleet Pulse: Health Score Tooltip Spec — Sub-signal dot colours | Spec states amber covers 40–79 % and red covers <40 %. The boundary value 40 % itself is undefined — does a row at exactly 40 % render amber or red? | Is the 40 % boundary inclusive of amber (≥40 % = amber) or red (≤40 % = red)? | Medium | Hanna Lee | 2026-05-17 |  | Open |  |
| CQ-005 | BATT-065 | Fleet Pulse: Status Column Spec — Column header | Three candidate names appear across the design files: "Status", "Active Alerts", "Health Flags". | Which header text is final for the renamed column? | Medium | Hanna Lee | 2026-05-17 |  | Open |  |
| CQ-006 | BATT-063 | Fleet Pulse: Status Column Spec — '+N more' overflow | Unclear whether '+N more' is a hover-only tooltip, a click-to-expand chip, or both. | Is the '+N more' overflow interaction hover-only, click-only, or both (hover + click)? | Medium | Hanna Lee | 2026-05-17 |  | Open |  |
| CQ-007 | BATT-061 | Fleet Pulse: Status Column Spec — EV vehicles | Charge behaviour for BEVs is fundamentally different (regen / DC fast charge). Spec doesn't say if CHARGE↓ should be suppressed for EV stock (e.g. SEAL 627KB5). | Should the CHARGE↓ badge be suppressed on EV vehicles until EV-specific charge logic ships? | Medium | Hanna Lee | 2026-05-17 |  | Open |  |
| CQ-Q2 | All TCs (assumed cadence) | red-Battery Study_v1.md — pipeline cadence not stated | How often does the pipeline recompute the Health Score, Forecast, and Band? | What is the recalc cadence (assumed 15 min)? | Critical | Hanna Lee | 2026-05-17 |  | Open |  |
| CQ-Q3 | BATT-023 | red-Battery Study_v1.md §3.3 — TREND threshold not stated | Minimum sample count for the TREND regression is not stated. | What is the minimum number of `rest_voltage_avg` samples below which TREND skips regression and returns 6 pts? (assumed <10) | Critical | Hanna Lee | 2026-05-17 |  | Open |  |
| CQ-Q4 | BATT-041 | red-Battery Study_v1.md §3.6 — LATEST stale-data threshold not stated | At what age does the latest telemetry trigger the 5-pt neutral fallback? | What is the LATEST stale-data threshold? (assumed 24 h) | Critical | Hanna Lee | 2026-05-17 |  | Open |  |
| CQ-Q5 | BATT-036 | red-Battery Study_v1.md §3.5 — CHARGE neutral fallback trip threshold | At what trip count does CHARGE fall back to 5-pt neutral? | What is the CHARGE neutral-fallback trip threshold? (assumed 0) | Critical | Hanna Lee | 2026-05-17 |  | Open |  |
| CQ-Q9 | BATT-044 | red-Battery Study_v1.md §4 step 3 — full redundancy-guard pair list missing | Spec only names `rest<11.8 + deep_discharge` as a correlated pair. Are there others? | Provide the complete list of correlated-modifier pairs and their precedence rules. | Critical | Hanna Lee | 2026-05-17 |  | Open |  |

---

## Summary

| TC ID | Screen / Section | Title | Type | Priority | Status |
|-------|------------------|-------|------|----------|--------|
| **REST SIGNAL (§3.1)** | | | | | |
| BATT-001 | §3.1 REST Signal | Verify scoring REST signal as 30 pts when 30-day mean rest_voltage_avg is ≥ 12.70 V | Functional | High | Not Run |
| BATT-002 | §3.1 REST Signal | Verify scoring REST signal as 25 pts when 30-day mean rest_voltage_avg is in [12.50, 12.70) V | Functional | High | Not Run |
| BATT-003 | §3.1 REST Signal | Verify scoring REST signal as 19 pts when 30-day mean rest_voltage_avg is in [12.30, 12.50) V | Functional | Medium | Not Run |
| BATT-004 | §3.1 REST Signal | Verify scoring REST signal as 10 pts when 30-day mean rest_voltage_avg is in [12.00, 12.30) V | Functional | High | Not Run |
| BATT-005 | §3.1 REST Signal | Verify scoring REST signal as 0 pts when 30-day mean rest_voltage_avg is < 12.00 V | Negative | High | Not Run |
| BATT-006 | §3.1 REST Signal (Neutral fallback) | Verify scoring REST signal as 15 pts neutral fallback when no rest_voltage_avg samples are present | Edge Case | Medium | Not Run |
| BATT-007 | §3.1 REST Signal (boundary) | Verify REST score boundary at 12.70 V vs 12.69 V | Edge Case | High | Not Run |
| BATT-008 | §3.1 REST Signal (Forecast ref fallback) | Verify forecast reference voltage falls back to mean rest voltage when live voltage is missing | Edge Case | Medium | Not Run |
| **CRANK SIGNAL (§3.2)** | | | | | |
| BATT-009 | §3.2 CRANK Signal | Verify scoring CRANK signal as 25 pts when min compensated crank_dip ≥ 10.0 V | Functional | High | Not Run |
| BATT-010 | §3.2 CRANK Signal (boundary + modifier) | Verify CRANK score + modifier boundary at 9.5 V vs 9.4 V | Edge Case | High | Not Run |
| BATT-011 | §3.2 CRANK Signal | Verify scoring CRANK signal as 13 pts when min compensated crank_dip in [9.0, 9.5) V | Functional | High | Not Run |
| BATT-012 | §3.2 CRANK Signal | Verify scoring CRANK signal as 6 pts when min compensated crank_dip in [8.0, 9.0) V | Functional | Medium | Not Run |
| BATT-013 | §3.2 CRANK Signal | Verify scoring CRANK signal as 0 pts and ×0.5 modifier when compensated crank_dip < 8.0 V | Negative | High | Not Run |
| BATT-014 | §3.2 CRANK Signal (Temp comp) | Verify CRANK temperature compensation adds 0.475 V at 9.6 V / 6 °C | Functional | High | Not Run |
| BATT-015 | §3.2 CRANK Signal (Temp comp) | Verify CRANK temperature compensation = 0 at the 25 °C baseline | Edge Case | Medium | Not Run |
| BATT-016 | §3.2 CRANK Signal (REST fallback) | Verify CRANK fallback to round(25 × REST/30) when no crank events | Edge Case | Medium | Not Run |
| BATT-017 | §3.2 CRANK Signal (Calc config) | Verify calc 2805150 config min_active=0 + merge_message_before/after=true | Regression | High | Not Run |
| **TREND SIGNAL (§3.3)** | | | | | |
| BATT-018 | §3.3 TREND Signal | Verify scoring TREND signal as 12 pts when slope ≥ −0.003 V/day | Functional | High | Not Run |
| BATT-019 | §3.3 TREND Signal | Verify scoring TREND signal as 9 pts when slope in [−0.008, −0.003) V/day | Functional | Medium | Not Run |
| BATT-020 | §3.3 TREND Signal | Verify scoring TREND signal as 5 pts when slope in [−0.015, −0.008) V/day | Functional | High | Not Run |
| BATT-021 | §3.3 TREND Signal | Verify scoring TREND signal as 0 pts when slope < −0.015 V/day | Negative | High | Not Run |
| BATT-022 | §3.3 TREND Signal (Regression x-axis fix) | Verify TREND regression uses interval midpoint, not calc timestamp | Regression | High | Not Run |
| BATT-023 | §3.3 TREND Signal (Neutral fallback) | Verify scoring TREND signal as 6 pts neutral fallback when sample count is below threshold | Edge Case | Medium | Not Run |
| **DECAY SIGNAL (§3.4)** | | | | | |
| BATT-024 | §3.4 DECAY Signal | Verify scoring DECAY signal as 13 pts when slope ≤ 0.003 V/hr | Functional | High | Not Run |
| BATT-025 | §3.4 DECAY Signal (boundaries) | Verify DECAY boundaries at 0.003 / 0.006 / 0.015 V/hr | Edge Case | Medium | Not Run |
| BATT-026 | §3.4 DECAY Signal | Verify scoring DECAY signal as 7 pts when slope in (0.006, 0.010] V/hr | Functional | High | Not Run |
| BATT-027 | §3.4 DECAY Signal | Verify scoring DECAY signal as 0 pts and ×0.7 modifier when slope > 0.015 V/hr | Negative | High | Not Run |
| BATT-028 | §3.4 DECAY Signal (Data cleanup) | Verify DECAY pipeline drops parks <6 h and parks with start > 13.5 V | Functional | High | Not Run |
| BATT-029 | §3.4 DECAY Signal (Slope clamping) | Verify DECAY slope is clamped to zero on negative-change parks | Edge Case | Medium | Not Run |
| BATT-030 | §3.4 DECAY Signal (Neutral fallback) | Verify scoring DECAY signal as 7 pts neutral fallback when no qualifying parks exist | Edge Case | Medium | Not Run |
| **CHARGE SIGNAL (§3.5)** | | | | | |
| BATT-031 | §3.5 CHARGE Signal | Verify scoring CHARGE signal as 10 pts when abs%≥95 and short%<50 | Functional | High | Not Run |
| BATT-032 | §3.5 CHARGE Signal | Verify scoring CHARGE signal as 7 pts when abs% in [90, 95) and short%<70 | Functional | Medium | Not Run |
| BATT-033 | §3.5 CHARGE Signal | Verify scoring CHARGE signal as 4 pts when abs% in [80, 90) | Functional | Medium | Not Run |
| BATT-034 | §3.5 CHARGE Signal | Verify scoring CHARGE signal as 0 pts and CHARGE↓ badge when abs% < 80 | Negative | High | Not Run |
| BATT-035 | §3.5 CHARGE Signal (Speed filter) | Verify CHARGE calculator filters messages with speed ≤ 5 km/h or engine off | Functional | Medium | Not Run |
| BATT-036 | §3.5 CHARGE Signal (Neutral fallback) | Verify scoring CHARGE signal as 5 pts neutral fallback when no trips in window | Edge Case | Medium | Not Run |
| BATT-037 | §3.5 CHARGE + Status spec | Verify SHORT↓ badge fires when short%>70 even when abs%≥95 | Edge Case | Medium | Not Run |
| **LATEST SIGNAL (§3.6)** | | | | | |
| BATT-038 | §3.6 LATEST Signal | Verify scoring LATEST signal as 10 pts when latest powersource voltage ≥ 12.50 V | Functional | High | Not Run |
| BATT-039 | §3.6 LATEST Signal (boundaries) | Verify LATEST boundaries at 12.20 / 11.90 V | Edge Case | Medium | Not Run |
| BATT-040 | §3.6 LATEST Signal | Verify scoring LATEST signal as 0 pts when latest powersource voltage < 11.90 V | Negative | High | Not Run |
| BATT-041 | §3.6 LATEST Signal (Neutral fallback) | Verify scoring LATEST signal as 5 pts neutral fallback when no recent telemetry | Edge Case | Medium | Not Run |
| **FORECAST LOGIC (§4)** | | | | | |
| BATT-042 | §4 Forecast (Base projection) | Verify forecast base projection formula + clamp to [0, 90] | Functional | High | Not Run |
| BATT-043 | §4 Forecast (Flat/positive slope) | Verify forecast base = 90 days when slope flat or positive | Edge Case | High | Not Run |
| BATT-044 | §4 Forecast (Modifiers + guard) | Verify modifier compounding after redundancy guard | Functional | High | Not Run |
| BATT-045 | §4 Forecast (14-day floor + Critical override) | Verify forecast clamps to 14 d and band forced to Critical when modifier stack pushes below 14 | Edge Case | High | Not Run |
| BATT-046 | §4 Forecast (Replacement override) | Verify forecast resets to 90 d when calc 2805166 fires within 24 h | Edge Case | High | Not Run |
| BATT-047 | §2 + §5 (End-to-end) | Verify a healthy vehicle scores 100 / forecast 90 d / band Excellent | Functional | High | Not Run |
| BATT-048 | §4 Forecast (Clamp lower bound) | Verify forecast base clamps to 0 when live voltage at/below 11.5 V floor | Edge Case | Medium | Not Run |
| BATT-049 | §4 Forecast (Deep Discharge modifier) | Verify ×0.7 modifier when calc 2805152 records ≥ 2 events | Functional | High | Not Run |
| BATT-050 | §4 Forecast (Alternator modifier) | Verify ×0.6 modifier when calc 2805149 records ≥ 1 event | Functional | High | Not Run |
| BATT-051 | §4 Forecast (CRANK modifier threshold) | Verify CRANK ×0.5 fires at < 9.5 V even at the 13-pt tier | Regression | High | Not Run |
| **HEALTH BANDS (§5)** | | | | | |
| BATT-052 | §5 Health Bands | Verify band transitions from Excellent (95) to Good (94) | Edge Case | High | Not Run |
| BATT-053 | §5 Health Bands (Most-restrictive rule) | Verify band lands at the most-restrictive when score and forecast disagree | Functional | High | Not Run |
| BATT-054 | §5 Health Bands (Fair) | Verify Fair band when score=72 and forecast=38 d | Functional | Medium | Not Run |
| BATT-055 | §5 Health Bands (Poor) | Verify Poor band when score=57 and forecast=32 d | Functional | Medium | Not Run |
| BATT-056 | §5 Health Bands (Critical) | Verify Critical band when score<50 and REPLACE badge fires | Negative | High | Not Run |
| BATT-057 | §5 Health Bands (Forecast override) | Verify Good score downgraded to Fair when forecast in [30, 45) d | Edge Case | High | Not Run |
| **SCORE FORMULA (§2 + Regression)** | | | | | |
| BATT-058 | §2 Score Formula | Verify weights sum to 100 in v2.2 | Regression | High | Not Run |
| BATT-059 | §2 Score Formula (v2.1 → v2.2 regression) | Verify v2.2 weightings applied; v2.1 weightings eliminated | Regression | High | Not Run |
| BATT-060 | §2 + §3.5 (MURANO regression) | Verify MURANO drops 100 → 90 between v2.1 and v2.2 | Regression | High | Not Run |
| **STATUS COLUMN / BADGES** | | | | | |
| BATT-061 | Status Spec (Badge triggers) | Verify all 8 Status column badges fire under their triggers | Functional | High | Not Run |
| BATT-062 | Status Spec (Pill ordering) | Verify pills ordered red > amber > green left-to-right | UI | Medium | Not Run |
| BATT-063 | Status Spec (Overflow) | Verify max 3 pills + '+N more' overflow when more badges active | UI | Medium | Not Run |
| BATT-064 | Status Spec (Always one pill) | Verify HEALTHY pill shown when no other badges fire | Functional | Medium | Not Run |
| BATT-065 | Status Spec (Summary line) | Verify plain-English summary line for each of 9 canonical badge combinations | Functional | Medium | Not Run |
| BATT-066 | Status Spec (Sortability) | Verify Status column sorts by worst-severity badge first | UI | Low | Not Run |
| BATT-067 | Status Spec (Mobile) | Verify summary line hidden and pills visible at viewport < 600 px | UI | Low | Not Run |
| **HEALTH SCORE TOOLTIP** | | | | | |
| BATT-068 | Tooltip Spec (Open/close) | Verify tooltip opens on hover/focus; closes on blur, mouseleave, Escape | UI | Medium | Not Run |
| BATT-069 | Tooltip Spec (Sub-signal rows) | Verify 6 sub-signal rows with friendly labels (no raw values / weights) | UI | Medium | Not Run |
| BATT-070 | Tooltip Spec (Dot colours) | Verify dot colour ≥80 % green / 40–79 % amber / <40 % red | UI | Medium | Not Run |
| BATT-071 | Tooltip Spec (No raw values) | Verify tooltip displays neither weights nor raw voltage values | UI | Medium | Not Run |
| BATT-072 | Tooltip Spec (Band label colour) | Verify band label hex matches spec for all 5 bands | UI | Medium | Not Run |
| BATT-073 | Tooltip Spec (Mobile modal) | Verify tooltip opens as modal sheet on viewport < 480 px | UI | Low | Not Run |
| **GENERAL UI DISPLAY** | | | | | |
| BATT-074 | Tooltip layout | Verify all 6 sub-signal rows visible without internal scrolling at ≥1024 px | UI | Medium | Not Run |
| BATT-075 | §4 Forecast display | Verify forecast displays as relative days, not calendar date | UI | Medium | Not Run |
| **WEATHERAPI TEMPERATURE FALLBACK** | | | | | |
| BATT-076 | §3.2 CRANK (WeatherAPI fallback) | Verify CRANK temp comp falls back to last known fix within 7 days | Edge Case | Low | Not Run |
| BATT-077 | §3.2 CRANK (WeatherAPI fallback) | Verify CRANK temp comp falls back to 25 °C baseline when no fix within 7 days | Edge Case | Low | Not Run |
