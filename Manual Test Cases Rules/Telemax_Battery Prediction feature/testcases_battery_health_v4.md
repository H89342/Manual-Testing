# Test Cases: Battery Prediction (Battery Health & Replacement Forecast)

## Overview

| Field       | Value                                                   |
|-------------|---------------------------------------------------------|
| Author      | Hanna Lee (hanna.lee@telemax.com.au)                    |
| Date        | 2026-05-17                                              |
| Version     | 4.0                                                     |
| Module      | Battery Prediction — Fleet Pulse by Telemax            |
| Environment | Mixed — Web + Backend (Flespi calc) + Mobile responsive |
| Status      | In Progress                                             |

**Source documents:**
- Battery Health & Replacement Forecast (Engineering Briefing v2.2) — https://flepsi-batteryhealth-replacement.netlify.app/
- Fleet Pulse: Status Column Spec — https://cosmic-brioche-eccf27.netlify.app/
- Fleet Pulse: Health Score Tooltip Spec — https://eclectic-cassata-b60697.netlify.app/
- Test case rules — TESTCASE_RULES_SHARED.md / TESTCASE_RULES_UI.md

**v4 changes vs v3:**
- Full re-issue under v4 IDs (BATT-001 … BATT-077). v3 IDs are not preserved (rebuild from scratch per request).
- Closes all gaps from `Review Battery Prediction Test case.md` §3–§4: tier gaps, neutral fallbacks, Status/Tooltip coverage, WeatherAPI fallback.
- Requirement summaries updated per review §2 corrections (full REST tier table; v2.2 DECAY weights; CHARGE neutral fallback).
- 7 PENDING TCs flagged with Open CQ items — see Clarify Requirements section.

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
| Pending       |   7   | 9.1%       |
| Not Run       |  70   | 90.9%      |

#### Derived Metrics

| Metric                | Formula          | Value   |
|-----------------------|------------------|---------|
| Executed              | Pass + Fail      | 0 / 77  |
| Execution Progress %  | Executed / Total | 0%      |
| Pass Rate %           | Pass / Executed  | n/a     |

#### Priority Breakdown

| Priority   | Total | Pass | Fail | Blocked | Not Run | Pass Rate % |
|------------|-------|------|------|---------|---------|-------------|
| High       |  40   |  0   |  0   |   0     |   40    |     0%      |
| Medium     |  32   |  0   |  0   |   0     |   32    |     0%      |
| Low        |   5   |  0   |  0   |   0     |    5    |     0%      |
| **Total**  |  77   |  0   |  0   |   0     |   77    |     0%      |

> High-priority share = **51.9%** (rule: ≥ 30%). ✅

## Table of Contents

- **REST Signal (§3.1)** — BATT-001 … BATT-008 (8 TCs)
- **CRANK Signal (§3.2)** — BATT-009 … BATT-017 (9 TCs)
- **TREND Signal (§3.3)** — BATT-018 … BATT-023 (6 TCs)
- **DECAY Signal (§3.4)** — BATT-024 … BATT-030 (7 TCs)
- **CHARGE Signal (§3.5)** — BATT-031 … BATT-037 (7 TCs)
- **LATEST Signal (§3.6)** — BATT-038 … BATT-041 (4 TCs)
- **Forecast Logic (§4)** — BATT-042 … BATT-051 (10 TCs)
- **Health Bands (§5)** — BATT-052 … BATT-057 (6 TCs)
- **Score Formula (§2)** — BATT-058 … BATT-060 (3 TCs)
- **Status Column / Badges** — BATT-061 … BATT-067 (7 TCs)
- **Health Score Tooltip** — BATT-068 … BATT-073 (6 TCs)
- **UI Display** — BATT-074 … BATT-075 (2 TCs)
- **WeatherAPI fallback** — BATT-076 … BATT-077 (2 TCs)
- **Clarify Requirements (CQ Log)** — 7 open items

---

## REST Signal (§3.1)

### BATT-001: Verify scoring REST signal as 30 pts when 30-day mean rest_voltage_avg is ≥ 12.70 V

**Screen / Section:** Battery Health & Replacement Forecast — §3.1 REST Signal  
**Priority:** High  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** REST contributes up to 30 pts of the 100-point Health Score. The top tier (≥12.70 V mean rest voltage) maps to 30 pts (Excellent). If wrong, a healthy battery scores low and triggers false replacement forecasts.

**Preconditions:**
- Vehicle has ≥ 30 days of telemetry in the Flespi tenant
- Calc 2805151 (Rest Voltage) is enabled and producing rest_voltage_avg samples
- 30-day mean rest_voltage_avg is engineered to be 12.72 V
- Test user is logged in to Fleet Pulse and the vehicle row is visible on the dashboard

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Open the Flespi calc 2805151 device messages and confirm at least 20 rest_voltage_avg samples in the last 30 days | Sample count ≥ 20 and the visible average reads 12.72 V (±0.01) |
| 2 | In Fleet Pulse, open the Health Score tooltip for the vehicle | Tooltip opens and the REST row is visible |
| 3 | Read the REST score in the tooltip | REST shows 30/30 with the Excellent status indicator (green) |
| 4 | Trigger a manual score recalculation (or wait for the next 15-min cycle) and re-open the tooltip | REST remains 30/30 — score is stable across recalc |

#### Test Data

```
vehicle_id:            TLX-DEMO-001
mean_rest_voltage_30d: 12.72 V
sample_count:          24
calc_id:               2805151
```

**Postconditions:**
- REST score persisted as 30 in the score_history table
- Overall battery_health_score reflects REST=30 in its breakdown payload

**Status:** Not Run  
**Notes:** 

---

### BATT-002: Verify scoring REST signal as 25 pts when 30-day mean rest_voltage_avg is in [12.50 V, 12.70 V)

**Screen / Section:** Battery Health & Replacement Forecast — §3.1 REST Signal  
**Priority:** High  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** The Good tier (≥12.50 V and <12.70 V) must score 25 pts. Validates that the tier just below Excellent is correctly identified.

**Preconditions:**
- Vehicle has ≥ 30 days of telemetry
- Mean rest_voltage_avg engineered to 12.55 V
- User is logged in to Fleet Pulse

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm calc 2805151 reports 30-day mean = 12.55 V | Mean reads 12.55 V (±0.01) |
| 2 | Open Health Score tooltip on the dashboard | Tooltip opens |
| 3 | Read REST row | REST shows 25/30 with Good status (green) |

#### Test Data

```
mean_rest_voltage_30d: 12.55 V
```

**Postconditions:**
- REST score persisted as 25 in score_history

**Status:** Not Run  
**Notes:** 

---

### BATT-003: Verify scoring REST signal as 19 pts when 30-day mean rest_voltage_avg is in [12.30 V, 12.50 V)

**Screen / Section:** Battery Health & Replacement Forecast — §3.1 REST Signal  
**Priority:** Medium  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Fair tier (≥12.30 V and <12.50 V) scores 19 pts — first amber tier in the REST band.

**Preconditions:**
- Vehicle has ≥ 30 days of telemetry
- Mean rest_voltage_avg engineered to 12.35 V

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm 30-day mean = 12.35 V in calc 2805151 | Mean reads 12.35 V |
| 2 | Open Health Score tooltip | Tooltip opens |
| 3 | Read REST row | REST shows 19/30 with Fair status (amber) |

#### Test Data

```
mean_rest_voltage_30d: 12.35 V
```

**Postconditions:**
- REST=19 persisted; tooltip dot colour is amber

**Status:** Not Run  
**Notes:** 

---

### BATT-004: Verify scoring REST signal as 10 pts when 30-day mean rest_voltage_avg is in [12.00 V, 12.30 V)

**Screen / Section:** Battery Health & Replacement Forecast — §3.1 REST Signal  
**Priority:** High  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** NEW v4 coverage: Poor tier (≥12.00 V and <12.30 V) must score 10 pts. This 10-pt tier is operationally significant and was untested in v3 — the review flagged it as a High-priority gap.

**Preconditions:**
- Vehicle has ≥ 30 days of telemetry
- Mean rest_voltage_avg engineered to 12.05 V

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm 30-day mean = 12.05 V in calc 2805151 | Mean reads 12.05 V |
| 2 | Open Health Score tooltip on Fleet Pulse | Tooltip opens |
| 3 | Read REST row | REST shows 10/30 with Poor status (orange) |
| 4 | Repeat at boundary value 12.00 V exactly | REST still shows 10/30 (≥12.00 V is inclusive) |
| 5 | Repeat at 11.99 V | REST drops to 0/30 — boundary respected |

#### Test Data

```
mean_rest_voltage_30d: 12.05 V
boundary_low:          12.00 V
boundary_high:         12.29 V
```

**Postconditions:**
- REST=10 persisted for 12.05 V case; REST=0 for 11.99 V case

**Status:** Not Run  
**Notes:** New in v4 — closes review §3.1 gap (10-pt tier).

---

### BATT-005: Verify scoring REST signal as 0 pts when 30-day mean rest_voltage_avg is < 12.00 V

**Screen / Section:** Battery Health & Replacement Forecast — §3.1 REST Signal  
**Priority:** High  
**Type:** Negative  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Critical tier (<12.00 V) scores 0 pts. Catches batteries that are functionally flat at rest — a leading indicator of imminent failure.

**Preconditions:**
- Vehicle has ≥ 30 days of telemetry
- Mean rest_voltage_avg engineered to 11.85 V

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm 30-day mean = 11.85 V | Mean reads 11.85 V |
| 2 | Open Health Score tooltip | Tooltip opens |
| 3 | Read REST row | REST shows 0/30 with Critical status (red) |
| 4 | Check forecast pipeline outputs | Forecast modifier ×0.5 (rest <11.8 V) has fired in the modifier list |

#### Test Data

```
mean_rest_voltage_30d: 11.85 V
```

**Postconditions:**
- REST=0 persisted; rest<11.8 V forecast modifier flagged in forecast_audit

**Status:** Not Run  
**Notes:** 

---

### BATT-006: Verify scoring REST signal as 15 pts neutral fallback when no rest_voltage_avg samples are present

**Screen / Section:** Battery Health & Replacement Forecast — §3.1 REST Signal  
**Priority:** Medium  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Neutral fallback: when no rest_voltage_avg samples exist (new vehicle, calc disabled), REST scores 15 pts to avoid penalising a vehicle for missing data.

**Preconditions:**
- Vehicle is newly onboarded with < 24 h of telemetry, OR calc 2805151 has been disabled
- No rest_voltage_avg samples exist in the 30-day window

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm calc 2805151 returns zero samples for the vehicle | Sample count = 0 |
| 2 | Open Health Score tooltip | Tooltip opens |
| 3 | Read REST row | REST shows 15/30 with Neutral (grey) status and tooltip text 'Insufficient rest data' |

#### Test Data

```
sample_count: 0
window:       last 30 days
```

**Postconditions:**
- REST=15 persisted with fallback_reason='no_rest_data'

**Status:** Not Run  
**Notes:** 

---

### BATT-007: Verify REST score boundary transitions cleanly at 12.70 V (30 pts) vs 12.69 V (25 pts)

**Screen / Section:** Battery Health & Replacement Forecast — §3.1 REST Signal  
**Priority:** High  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** The 12.70 V tier boundary must score 30 pts at exactly 12.70 V and 25 pts at 12.69 V (inclusive lower bound). Edge case proves the comparison is ≥ and not >.

**Preconditions:**
- Two test vehicles or two seeded data states — one at exactly 12.70 V mean, one at 12.69 V

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Seed vehicle A with 30-day mean = 12.7000 V and trigger recalc | Recalc completes |
| 2 | Open tooltip for vehicle A | REST = 30/30 |
| 3 | Seed vehicle B with 30-day mean = 12.6900 V and trigger recalc | Recalc completes |
| 4 | Open tooltip for vehicle B | REST = 25/30 |

#### Test Data

```
vehicle_A.mean: 12.7000 V
vehicle_B.mean: 12.6900 V
```

**Postconditions:**
- A: REST=30; B: REST=25 in score_history

**Status:** Not Run  
**Notes:** 

---

### BATT-008: Verify forecast reference voltage falls back to mean rest voltage when live voltage is missing

**Screen / Section:** Battery Health & Replacement Forecast — §3.1 REST Signal  
**Priority:** Medium  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** When live voltage is missing, the forecast must fall back to mean_rest as its reference voltage (ref_v = live_v if available else mean_rest). Without this, forecast cannot compute.

**Preconditions:**
- Vehicle has a valid 30-day mean rest_voltage_avg = 12.40 V
- Latest telemetry message has external.powersource.voltage = null (simulated by removing the last 6 h of msgs)

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm latest message lacks powersource.voltage | Field is absent in raw payload |
| 2 | Trigger forecast recalc | Forecast pipeline runs without error |
| 3 | Inspect forecast_audit.ref_voltage | ref_voltage == 12.40 V (mean rest) not 0 or null |
| 4 | Open Health Score tooltip | LATEST row shows neutral 5/10 and tooltip text 'Live voltage unavailable — using rest mean' |

#### Test Data

```
mean_rest_voltage_30d: 12.40 V
latest_voltage:        null
```

**Postconditions:**
- forecast_audit.ref_voltage_source='rest_mean'; forecast completes successfully

**Status:** Not Run  
**Notes:** 

---

## CRANK Signal (§3.2)

### BATT-009: Verify scoring CRANK signal as 25 pts when minimum compensated crank_dip is ≥ 10.0 V

**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal  
**Priority:** High  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Strong-cranking tier: minimum 30-day crank_dip (compensated to 25 °C) ≥ 10.0 V scores the full 25 pts. Validates the primary CRANK happy path.

**Preconditions:**
- Vehicle has ≥ 30 days of telemetry with at least 5 crank events
- Min compensated crank_dip engineered to 10.10 V
- Calc 2805150 (Crank Events) is enabled

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Open calc 2805150 messages and confirm min crank_dip across the window | Min raw crank_dip + temp comp = 10.10 V |
| 2 | Open Health Score tooltip | Tooltip opens |
| 3 | Read CRANK row | CRANK shows 25/25 with Strong status (green) |

#### Test Data

```
min_crank_dip_compensated: 10.10 V
events_in_window:          7
```

**Postconditions:**
- CRANK=25 persisted

**Status:** Not Run  
**Notes:** 

---

### BATT-010: Verify CRANK score and forecast modifier transitions cleanly at 9.5 V (20 pts) vs 9.4 V (13 pts + ×0.5)

**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal  
**Priority:** High  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** 20-pt tier boundary: ≥9.5 V scores 20, 9.4 V drops to 13 and additionally arms the ×0.5 forecast modifier. Validates dual-effect boundary.

**Preconditions:**
- Two vehicles or seeded states — A: min crank_dip = 9.50 V, B: 9.40 V

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Trigger recalc on vehicle A (9.50 V) | Recalc OK |
| 2 | Open tooltip for A | CRANK = 20/25; forecast modifier ×0.5 NOT armed |
| 3 | Trigger recalc on vehicle B (9.40 V) | Recalc OK |
| 4 | Open tooltip for B | CRANK = 13/25; forecast modifier ×0.5 armed in forecast_audit |

#### Test Data

```
vehicle_A.min_crank: 9.50 V
vehicle_B.min_crank: 9.40 V
```

**Postconditions:**
- A: modifier list empty for CRANK; B: modifier list contains 'crank<9.5_x0.5'

**Status:** Not Run  
**Notes:** 

---

### BATT-011: Verify scoring CRANK signal as 13 pts when minimum compensated crank_dip is in [9.0 V, 9.5 V)

**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal  
**Priority:** High  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** NEW v4 coverage: 13-pt 'Marginal' tier (≥9.0 V and <9.5 V). Review §3.2 flagged this as a missing High-priority tier.

**Preconditions:**
- Vehicle has ≥ 5 crank events; min compensated dip engineered to 9.20 V

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm min compensated crank_dip = 9.20 V | Reads 9.20 V |
| 2 | Open Health Score tooltip | Tooltip opens |
| 3 | Read CRANK row | CRANK = 13/25 with Marginal status (amber) |
| 4 | Inspect forecast_audit | ×0.5 modifier armed (crank<9.5) |

#### Test Data

```
min_crank_dip_compensated: 9.20 V
```

**Postconditions:**
- CRANK=13 persisted; forecast modifier list contains 'crank<9.5_x0.5'

**Status:** Not Run  
**Notes:** New in v4 — closes review §3.2 gap (13-pt tier).

---

### BATT-012: Verify scoring CRANK signal as 6 pts when minimum compensated crank_dip is in [8.0 V, 9.0 V)

**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal  
**Priority:** Medium  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Poor tier (≥8.0 V and <9.0 V) scores 6 pts. Validates the third-worst CRANK band.

**Preconditions:**
- Min compensated crank_dip engineered to 8.50 V

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm min compensated dip = 8.50 V | Reads 8.50 V |
| 2 | Open tooltip | CRANK = 6/25 with Poor status (orange) |
| 3 | Inspect forecast_audit | ×0.5 modifier still armed (any value <9.5 V) |

#### Test Data

```
min_crank_dip_compensated: 8.50 V
```

**Postconditions:**
- CRANK=6 persisted

**Status:** Not Run  
**Notes:** 

---

### BATT-013: Verify scoring CRANK signal as 0 pts and arming ×0.5 forecast modifier when compensated crank_dip is < 8.0 V

**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal  
**Priority:** High  
**Type:** Negative  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Critical CRANK (<8.0 V) scores 0 pts AND triggers the ×0.5 high-internal-resistance forecast modifier. Highest-severity CRANK condition.

**Preconditions:**
- Min compensated crank_dip engineered to 7.5 V

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm min compensated dip = 7.5 V | Reads 7.5 V |
| 2 | Open tooltip | CRANK = 0/25 with Critical status (red) |
| 3 | Inspect forecast_audit | Modifier list contains 'crank<9.5_x0.5' |
| 4 | Verify forecast value reflects ×0.5 multiplier | forecast_days <= 0.5 × base_days |

#### Test Data

```
min_crank_dip_compensated: 7.5 V
```

**Postconditions:**
- CRANK=0 persisted; modifier applied in forecast pipeline

**Status:** Not Run  
**Notes:** 

---

### BATT-014: Verify CRANK temperature compensation formula adds 0.475 V when raw crank is 9.6 V at 6 °C ambient

**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal — temperature compensation  
**Priority:** High  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Temperature compensation: crank_compensated = crank_observed + 0.025 × (25 − ambient_temp_c). Required so cold-morning measurements don't false-fail healthy batteries.

**Preconditions:**
- Ambient temperature for the vehicle's location at the time of the crank event is 6 °C (from WeatherAPI)
- Raw crank_dip captured by calc 2805150 = 9.60 V

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm raw crank_dip = 9.60 V at ambient 6 °C | Both values read correctly |
| 2 | Open forecast_audit.compensated_crank_dip | Equals 9.60 + 0.025×(25-6) = 10.075 V |
| 3 | Open tooltip | CRANK = 25/25 (Strong) — would have been 13/25 without compensation |

#### Test Data

```
raw_crank_dip:        9.60 V
ambient_temp:         6.0 °C
expected_compensated: 10.075 V
```

**Postconditions:**
- forecast_audit.compensated_crank_dip ≈ 10.075 V (±0.005)

**Status:** Not Run  
**Notes:** 

---

### BATT-015: Verify CRANK temperature compensation adds zero adjustment at the 25 °C baseline

**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal — temperature compensation  
**Priority:** Medium  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** At ambient 25 °C the compensation factor is zero — raw == compensated. Sanity check the formula's baseline.

**Preconditions:**
- Raw crank_dip = 9.60 V at ambient 25 °C

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm raw crank_dip and temp | 9.60 V at 25 °C |
| 2 | Read compensated value | Equals 9.60 V (no adjustment) |

#### Test Data

```
raw_crank_dip: 9.60 V
ambient_temp:  25 °C
```

**Postconditions:**
- compensated_crank_dip == raw_crank_dip

**Status:** Not Run  
**Notes:** 

---

### BATT-016: Verify CRANK signal falls back to round(25 × REST/30) when no crank events exist in 30-day window

**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal — REST fallback  
**Priority:** Medium  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** When no crank events in 30 days, CRANK falls back proportionally to REST: CRANK = round(25 × rest_pts / 30). Validates fallback existence and accuracy.

**Preconditions:**
- Vehicle has zero crank events in the 30-day window (e.g. parked in yard)
- REST scored 25/30

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm calc 2805150 returns 0 events | Event count = 0 |
| 2 | Open tooltip and read REST and CRANK rows | REST = 25/30; CRANK = 21/25 (round(25×25/30)=20.83→21) |
| 3 | Repeat with REST=30/30 | CRANK = 25/25 |
| 4 | Repeat with REST=0/30 | CRANK = 0/25 |

#### Test Data

```
crank_events_count: 0
rest_pts:           25 (then 30, then 0)
expected_crank:     21, 25, 0
```

**Postconditions:**
- CRANK persisted with fallback_reason='no_crank_events'

**Status:** Not Run  
**Notes:** 

---

### BATT-017: Verify calc 2805150 captures cranks correctly with min_active=0 and merge_message_before/after=true

**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal — calculator config  
**Priority:** High  
**Type:** Regression  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Regression: calc 2805150 selector MUST use min_active=0 with merge_message_before/after=true. Without this, 99% of crank events are missed (April 28 fix).

**Preconditions:**
- Vehicle drove ≥ 5 ignition cycles in a test session

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Open calc 2805150 config in Flespi | min_active=0; merge_message_before=true; merge_message_after=true |
| 2 | Count ignition OFF→ON transitions in raw telemetry for the test session | ≥ 5 |
| 3 | Count crank events produced by calc 2805150 | Matches transition count within ±1 |
| 4 | Toggle merge_message_before/after to false and recount | Event count drops by ≥ 90% — confirms regression |
| 5 | Restore configuration to true | Config is restored |

#### Test Data

```
config.min_active:           0
config.merge_message_before: true
config.merge_message_after:  true
```

**Postconditions:**
- Calc config matches required values; production capture rate ≥ 95%

**Status:** Not Run  
**Notes:** Reverts the April 28 misconfiguration bug.

---

## TREND Signal (§3.3)

### BATT-018: Verify scoring TREND signal as 12 pts when 30-day rest voltage regression slope is ≥ −0.003 V/day

**Screen / Section:** Battery Health & Replacement Forecast — §3.3 TREND Signal  
**Priority:** High  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** TREND scores 12 pts when the linear-regression slope of rest_voltage_avg over 30 days is ≥ −0.003 V/day (stable or improving). Top tier of the TREND signal.

**Preconditions:**
- ≥ 20 rest_voltage_avg samples spanning ≥ 28 days
- Slope engineered to −0.001 V/day (stable)

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Open the trend analysis output and confirm slope | Slope = −0.001 V/day |
| 2 | Open tooltip | TREND row shows 12/12 with Stable status (green) |

#### Test Data

```
slope_per_day: -0.001 V/day
sample_count:  24
```

**Postconditions:**
- TREND=12 persisted

**Status:** Not Run  
**Notes:** 

---

### BATT-019: Verify scoring TREND signal as 9 pts when 30-day slope is in [−0.008, −0.003) V/day

**Screen / Section:** Battery Health & Replacement Forecast — §3.3 TREND Signal  
**Priority:** Medium  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Mild-decline tier (≥ −0.008 and < −0.003 V/day) scores 9 pts. Indicates a gentle downward trend that does not yet warrant alarm.

**Preconditions:**
- Slope engineered to −0.005 V/day

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm slope = −0.005 V/day | Reads −0.005 |
| 2 | Open tooltip | TREND = 9/12 (Mild decline, green-amber) |

#### Test Data

```
slope_per_day: -0.005 V/day
```

**Postconditions:**
- TREND=9 persisted

**Status:** Not Run  
**Notes:** 

---

### BATT-020: Verify scoring TREND signal as 5 pts when 30-day slope is in [−0.015, −0.008) V/day

**Screen / Section:** Battery Health & Replacement Forecast — §3.3 TREND Signal  
**Priority:** High  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** NEW v4 coverage: 5-pt tier (≥ −0.015 V/day and < −0.008 V/day). Review §3.3 flagged this as a missing High-priority tier.

**Preconditions:**
- Slope engineered to −0.012 V/day

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm slope = −0.012 V/day | Reads −0.012 |
| 2 | Open tooltip | TREND = 5/12 with Declining status (amber) |
| 3 | Confirm TREND↓ badge fires in Status column | TREND↓ badge visible on the row |

#### Test Data

```
slope_per_day: -0.012 V/day
```

**Postconditions:**
- TREND=5 persisted; TREND↓ badge active

**Status:** Not Run  
**Notes:** New in v4 — closes review §3.3 gap (5-pt tier).

---

### BATT-021: Verify scoring TREND signal as 0 pts when 30-day slope is < −0.015 V/day

**Screen / Section:** Battery Health & Replacement Forecast — §3.3 TREND Signal  
**Priority:** High  
**Type:** Negative  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Critical decline (< −0.015 V/day) scores 0 pts — battery is losing ≥ 0.45 V over 30 days, an accelerating-failure signature.

**Preconditions:**
- Slope engineered to −0.020 V/day

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm slope = −0.020 V/day | Reads −0.020 |
| 2 | Open tooltip | TREND = 0/12 with Critical (red) status |
| 3 | Confirm TREND↓ badge fires | TREND↓ visible and uses red tone |

#### Test Data

```
slope_per_day: -0.020 V/day
```

**Postconditions:**
- TREND=0 persisted

**Status:** Not Run  
**Notes:** 

---

### BATT-022: Verify TREND regression x-axis uses interval midpoint, not the calc emission timestamp

**Screen / Section:** Battery Health & Replacement Forecast — §3.3 TREND Signal — regression x-axis fix  
**Priority:** High  
**Type:** Regression  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Regression: x-axis for slope regression MUST be (interval_begin + interval_end) / 2, NOT the calc timestamp. v2.0 had this wrong and masked BMW battery instability.

**Preconditions:**
- Test dataset with 25 rest intervals where interval midpoint differs from calc timestamp by ≥ 30 min
- Reference slope computed via midpoint = −0.011 V/day; using timestamp incorrectly yields −0.004 V/day

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Run TREND regression on the dataset | Pipeline emits slope value |
| 2 | Confirm slope = −0.011 V/day (midpoint method) | Matches reference within ±0.0005 |
| 3 | Inspect the implementation/audit log | x_axis source field reads 'interval_midpoint' |
| 4 | Open tooltip | TREND scores 5/12 (matches midpoint slope, not 9/12 which timestamp method would produce) |

#### Test Data

```
expected_slope: -0.011 V/day
x_axis_source:  interval_midpoint
```

**Postconditions:**
- TREND audit confirms midpoint method; no v2.0 regression

**Status:** Not Run  
**Notes:** 

---

### BATT-023: Verify scoring TREND signal as 6 pts neutral fallback when fewer than 10 rest samples exist in the 30-day window

**Screen / Section:** Battery Health & Replacement Forecast — §3.3 TREND Signal — neutral fallback  
**Priority:** Medium  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** NEW v4 coverage: when sample count is insufficient for regression (e.g. <10 rest samples), TREND falls back to 6 pts neutral. Review §3.3 flagged this as untested.

**Preconditions:**
- Vehicle has only 7 rest_voltage_avg samples in the last 30 days

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm sample count = 7 | Count = 7 |
| 2 | Run regression | Pipeline skips regression and emits fallback |
| 3 | Open tooltip | TREND = 6/12 with Neutral (grey) status and tooltip text 'Not enough data for trend' |

#### Test Data

```
sample_count: 7
threshold:    10
```

**Postconditions:**
- TREND=6 persisted with fallback_reason='insufficient_samples'

**Status:** Not Run  
**Notes:** New in v4 — closes review §3.3 neutral-fallback gap.

---

## DECAY Signal (§3.4)

### BATT-024: Verify scoring DECAY signal as 13 pts when parked decay slope is ≤ 0.003 V/hr

**Screen / Section:** Battery Health & Replacement Forecast — §3.4 DECAY Signal  
**Priority:** High  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** DECAY scores 13 pts (max) when the parked decay slope is ≤ 0.003 V/hr — battery holds charge well across long parks. Top tier.

**Preconditions:**
- Vehicle has ≥ 3 qualifying parks (≥ 6 h, start voltage ≤ 13.5 V) in 30-day window
- Calc 2805232 (Parked Voltage Decay) is enabled
- Mean decay slope engineered to 0.0020 V/hr

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Inspect calc 2805232 outputs | Mean slope = 0.0020 V/hr |
| 2 | Open tooltip | DECAY = 13/13 with Excellent status (green) |

#### Test Data

```
mean_decay_slope: 0.0020 V/hr
qualifying_parks: 4
```

**Postconditions:**
- DECAY=13 persisted

**Status:** Not Run  
**Notes:** 

---

### BATT-025: Verify DECAY score boundary transitions at 0.003, 0.006, and 0.015 V/hr thresholds

**Screen / Section:** Battery Health & Replacement Forecast — §3.4 DECAY Signal  
**Priority:** Medium  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Boundary check: 0.003 V/hr → 13 pts; 0.0031 V/hr → 10 pts; 0.0061 V/hr → 7 pts; 0.0151 V/hr → 0 pts. Three boundary transitions in one TC.

**Preconditions:**
- Four seeded states: 0.0030, 0.0031, 0.0061, 0.0151 V/hr

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Seed slope = 0.0030 V/hr and recalc | DECAY = 13/13 |
| 2 | Seed slope = 0.0031 V/hr and recalc | DECAY = 10/13 |
| 3 | Seed slope = 0.0061 V/hr and recalc | DECAY = 7/13 |
| 4 | Seed slope = 0.0151 V/hr and recalc | DECAY = 0/13 + ×0.7 forecast modifier armed |

#### Test Data

```
boundaries: 0.0030 / 0.0031 / 0.0061 / 0.0151 V/hr
expected:   13 / 10 / 7 / 0 pts
```

**Postconditions:**
- All four boundary scores persisted correctly

**Status:** Not Run  
**Notes:** 

---

### BATT-026: Verify scoring DECAY signal as 7 pts when parked decay slope is in (0.006, 0.010] V/hr

**Screen / Section:** Battery Health & Replacement Forecast — §3.4 DECAY Signal  
**Priority:** High  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** NEW v4 coverage: 7-pt tier (0.006 V/hr < slope ≤ 0.010 V/hr). Review §3.4 flagged this as a missing High-priority tier.

**Preconditions:**
- Mean decay slope engineered to 0.008 V/hr

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm slope = 0.008 V/hr | Reads 0.008 |
| 2 | Open tooltip | DECAY = 7/13 with Watch status (amber) |
| 3 | Inspect forecast_audit | DECAY ×0.7 modifier NOT armed (only fires when slope > 0.015) |

#### Test Data

```
mean_decay_slope: 0.008 V/hr
```

**Postconditions:**
- DECAY=7 persisted; no decay modifier in forecast

**Status:** Not Run  
**Notes:** New in v4 — closes review §3.4 gap (7-pt tier).

---

### BATT-027: Verify scoring DECAY signal as 0 pts and arming ×0.7 forecast modifier when parked decay slope > 0.015 V/hr

**Screen / Section:** Battery Health & Replacement Forecast — §3.4 DECAY Signal  
**Priority:** High  
**Type:** Negative  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Critical DECAY (>0.015 V/hr) scores 0 pts AND triggers the ×0.7 self-discharge forecast modifier. Worst DECAY band.

**Preconditions:**
- Mean decay slope engineered to 0.020 V/hr

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm slope = 0.020 V/hr | Reads 0.020 |
| 2 | Open tooltip | DECAY = 0/13 with Critical (red) status |
| 3 | Inspect forecast_audit | Modifier list contains 'decay>0.015_x0.7' |

#### Test Data

```
mean_decay_slope: 0.020 V/hr
```

**Postconditions:**
- DECAY=0 persisted; forecast ×0.7 applied

**Status:** Not Run  
**Notes:** 

---

### BATT-028: Verify DECAY pipeline drops parks shorter than 6 h and parks starting above 13.5 V before computing slope

**Screen / Section:** Battery Health & Replacement Forecast — §3.4 DECAY Signal — data cleanup rules  
**Priority:** High  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Two mandatory data-cleanup rules in DECAY: drop parks shorter than 6 h (noise) AND parks where start voltage > 13.5 V (alternator tail not yet decayed).

**Preconditions:**
- Test dataset of 10 parks: 5 valid (≥6 h and start ≤13.5 V), 3 short (4-5 h), 2 with start voltage 13.6-13.9 V

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Run DECAY pipeline on the dataset | Pipeline completes |
| 2 | Inspect intermediate 'qualifying_parks' list | Count = 5; the 3 short and 2 high-start parks are excluded |
| 3 | Inspect calc 2805232 config | merge_message_before/after = false (so alternator voltage doesn't contaminate park edges) |
| 4 | Verify slope is computed only over the 5 valid parks | Audit shows 5 contributing intervals |

#### Test Data

```
parks_total:           10
parks_qualifying:      5
parks_dropped_short:   3
parks_dropped_high_v:  2
config.merge_before:   false
config.merge_after:    false
```

**Postconditions:**
- Only 5 parks contributed to DECAY slope

**Status:** Not Run  
**Notes:** 

---

### BATT-029: Verify DECAY slope is clamped to zero when a park shows negative voltage change

**Screen / Section:** Battery Health & Replacement Forecast — §3.4 DECAY Signal — slope clamping  
**Priority:** Medium  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Negative slope (start < end during a park) is a surface-charge artefact, not real recovery. Slope must be clamped to ≥0.

**Preconditions:**
- One park where start = 12.30 V, end = 12.35 V over 8 h (artefact)

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Run DECAY pipeline on the artefact park | Pipeline completes |
| 2 | Inspect that park's contribution to slope | Raw slope = −0.00625 V/hr; clamped slope = 0.000 V/hr |
| 3 | Confirm no negative slopes propagate into mean | Mean slope uses 0.000 from this park, not the negative value |

#### Test Data

```
park.start_v:     12.30
park.end_v:       12.35
park.duration_h:  8
expected_clamped: 0.000 V/hr
```

**Postconditions:**
- DECAY mean computed correctly with clamped values

**Status:** Not Run  
**Notes:** 

---

### BATT-030: Verify scoring DECAY signal as 7 pts neutral fallback when no qualifying parks exist in the 30-day window

**Screen / Section:** Battery Health & Replacement Forecast — §3.4 DECAY Signal — neutral fallback  
**Priority:** Medium  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** NEW v4 coverage: when no qualifying parks exist in 30-day window, DECAY falls back to 7 pts neutral. Review §3.4 flagged this as untested.

**Preconditions:**
- Vehicle has no parks ≥ 6 h with start voltage ≤ 13.5 V in 30 days

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm qualifying_parks = 0 | Count = 0 |
| 2 | Open tooltip | DECAY = 7/13 with Neutral (grey) status and text 'No qualifying park data' |

#### Test Data

```
qualifying_parks: 0
```

**Postconditions:**
- DECAY=7 persisted with fallback_reason='no_qualifying_parks'

**Status:** Not Run  
**Notes:** New in v4 — closes review §3.4 neutral-fallback gap.

---

## CHARGE Signal (§3.5)

### BATT-031: Verify scoring CHARGE signal as 10 pts when hit_absorption% is ≥ 95 and short_trip% is < 50

**Screen / Section:** Battery Health & Replacement Forecast — §3.5 CHARGE Signal  
**Priority:** High  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** CHARGE (v2.2 NEW) scores 10 pts when hit_absorption% ≥ 95% AND short-trip% < 50%. Top tier; vehicles whose duty cycle keeps the battery well-charged.

**Preconditions:**
- Calc 2809220 enabled; ≥ 20 trips in 30-day window
- hit_absorption% engineered to 96%, short_trip% to 35%

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm calc 2809220 metrics | abs%=96, short%=35 |
| 2 | Open tooltip | CHARGE = 10/10 Excellent (green) |
| 3 | Confirm Status column | No CHARGE↓ or SHORT↓ badge |

#### Test Data

```
hit_absorption_pct: 96
short_trip_pct:     35
trips_in_window:    24
```

**Postconditions:**
- CHARGE=10 persisted

**Status:** Not Run  
**Notes:** 

---

### BATT-032: Verify scoring CHARGE signal as 7 pts when hit_absorption% is in [90, 95) and short_trip% < 70

**Screen / Section:** Battery Health & Replacement Forecast — §3.5 CHARGE Signal  
**Priority:** Medium  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** 7-pt tier: hit_absorption% ≥ 90 AND short_trip% < 70 (and not in 10-pt tier). Validates the middle band.

**Preconditions:**
- abs%=92, short%=60

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm metrics | abs%=92, short%=60 |
| 2 | Open tooltip | CHARGE = 7/10 Good |

#### Test Data

```
hit_absorption_pct: 92
short_trip_pct:     60
```

**Postconditions:**
- CHARGE=7 persisted

**Status:** Not Run  
**Notes:** 

---

### BATT-033: Verify scoring CHARGE signal as 4 pts when hit_absorption% is in [80, 90)  🟧 PENDING

**Screen / Section:** Battery Health & Replacement Forecast — §3.5 CHARGE Signal  
**Priority:** Medium  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** 4-pt tier: hit_absorption% ≥ 80 (short trip not constrained in spec). PENDING CQ-002 — needs clarification on short% interaction.

**Preconditions:**
- abs%=82, short%=85 (high short trips to expose CQ-002 ambiguity)

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm metrics | abs%=82, short%=85 |
| 2 | Open tooltip | CHARGE shows score per current implementation (record actual) |
| 3 | Capture actual vs CQ resolution and update post-CQ | Notes record actual score; verify against CQ-002 answer when received |

#### Test Data

```
hit_absorption_pct: 82
short_trip_pct:     85
```

**Postconditions:**
- CHARGE score persisted; CQ-002 referenced in Notes

**Status:** Not Run  
**Notes:** Blocked by CQ-002 — see Clarify Requirements. Short-trip behaviour at 4-pt tier unclear.

---

### BATT-034: Verify scoring CHARGE signal as 0 pts when hit_absorption% is < 80

**Screen / Section:** Battery Health & Replacement Forecast — §3.5 CHARGE Signal  
**Priority:** High  
**Type:** Negative  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** 0-pt tier: hit_absorption% < 80. Catches duty cycles too short to reach absorption — root cause of battery undercharging.

**Preconditions:**
- abs%=72, short%=80

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm metrics | abs%=72 |
| 2 | Open tooltip | CHARGE = 0/10 Critical (red) |
| 3 | Confirm CHARGE↓ badge fires in Status column | Badge visible |

#### Test Data

```
hit_absorption_pct: 72
short_trip_pct:     80
```

**Postconditions:**
- CHARGE=0 persisted; CHARGE↓ badge active

**Status:** Not Run  
**Notes:** 

---

### BATT-035: Verify CHARGE calculator filters out messages when speed is ≤ 5 km/h or engine is off

**Screen / Section:** Battery Health & Replacement Forecast — §3.5 CHARGE Signal — speed filter  
**Priority:** Medium  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Calc 2809220 must only count messages when engine is running AND speed > 5 km/h. Filters out idling/cranking artefacts.

**Preconditions:**
- Seeded trip with 10 idle messages (speed 0 km/h) and 30 driving messages (speed 30 km/h)

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Inspect calc 2809220 selector | Selector requires engine.on=true AND speed>5 |
| 2 | Inspect captured messages for the trip | Only the 30 driving messages contribute |

#### Test Data

```
idle_msgs:             10 (speed=0 km/h)
driving_msgs:          30 (speed=30 km/h)
expected_contributing: 30
```

**Postconditions:**
- Only driving messages contribute to CHARGE metrics

**Status:** Not Run  
**Notes:** 

---

### BATT-036: Verify scoring CHARGE signal as 5 pts neutral fallback when no trips exist in the 30-day window

**Screen / Section:** Battery Health & Replacement Forecast — §3.5 CHARGE Signal — neutral fallback  
**Priority:** Medium  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** NEW v4 coverage: when no trips occur in 30-day window, CHARGE falls back to 5 pts neutral (applies to newly onboarded vehicles and vehicles parked 30+ days). Review §3.5 flagged this as untested.

**Preconditions:**
- Vehicle parked for full 30-day window — zero trips

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm trips_in_window = 0 | Count = 0 |
| 2 | Open tooltip | CHARGE = 5/10 Neutral (grey) with text 'No trips in window' |

#### Test Data

```
trips_in_window: 0
```

**Postconditions:**
- CHARGE=5 persisted with fallback_reason='no_trips'

**Status:** Not Run  
**Notes:** New in v4 — closes review §3.5 neutral-fallback gap.

---

### BATT-037: Verify SHORT↓ badge fires when short_trip% exceeds 70% even when hit_absorption% is ≥ 95  🟧 PENDING

**Screen / Section:** Battery Health & Replacement Forecast — §3.5 CHARGE Signal + Fleet Pulse: Status Column Spec  
**Priority:** Medium  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** NEW v4 coverage: SHORT↓ badge must fire when short-trip% > 70% even if hit_absorption% ≥ 95% (vehicle reaches absorption but on too few long trips).

**Preconditions:**
- abs%=96, short%=78

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm metrics | abs%=96, short%=78 |
| 2 | Open Status column | SHORT↓ badge visible (amber) |
| 3 | Open tooltip | CHARGE score per implementation; SHORT↓ pill labelled in summary |

#### Test Data

```
hit_absorption_pct: 96
short_trip_pct:     78
```

**Postconditions:**
- SHORT↓ badge fired; pill present in row

**Status:** Not Run  
**Notes:** Blocked by CQ-001 — see Clarify Requirements. CHARGE↓ vs SHORT↓ split needs sign-off.

---

## LATEST Signal (§3.6)

### BATT-038: Verify scoring LATEST signal as 10 pts when latest powersource voltage is ≥ 12.50 V

**Screen / Section:** Battery Health & Replacement Forecast — §3.6 LATEST Signal  
**Priority:** High  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** LATEST scores 10 pts when the most recent external.powersource.voltage is ≥ 12.50 V. Real-time freshness signal.

**Preconditions:**
- Latest message has external.powersource.voltage = 12.65 V, age < 2 h

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm latest message voltage | 12.65 V, fresh |
| 2 | Open tooltip | LATEST = 10/10 Excellent (green) |

#### Test Data

```
latest_voltage: 12.65 V
message_age:    45 min
```

**Postconditions:**
- LATEST=10 persisted

**Status:** Not Run  
**Notes:** 

---

### BATT-039: Verify LATEST score boundaries at 12.20 V (7 pts) and 11.90 V (4 pts)

**Screen / Section:** Battery Health & Replacement Forecast — §3.6 LATEST Signal  
**Priority:** Medium  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Boundary verification at 12.20 V (7 pts) and 11.90 V (4 pts). Validates two tier transitions in one TC.

**Preconditions:**
- Two seeded states: 12.20 V and 11.90 V

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Seed latest = 12.20 V and recalc | LATEST = 7/10 |
| 2 | Seed latest = 12.19 V and recalc | LATEST = 4/10 |
| 3 | Seed latest = 11.90 V and recalc | LATEST = 4/10 |
| 4 | Seed latest = 11.89 V and recalc | LATEST = 0/10 |

#### Test Data

```
boundaries: 12.20 / 12.19 / 11.90 / 11.89 V
expected:   7 / 4 / 4 / 0 pts
```

**Postconditions:**
- All four boundary scores correct

**Status:** Not Run  
**Notes:** 

---

### BATT-040: Verify scoring LATEST signal as 0 pts when latest powersource voltage is < 11.90 V

**Screen / Section:** Battery Health & Replacement Forecast — §3.6 LATEST Signal  
**Priority:** High  
**Type:** Negative  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Critical tier (<11.90 V) scores 0 pts. Vehicle is in immediate trouble at this voltage.

**Preconditions:**
- Latest voltage = 11.50 V

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm latest = 11.50 V | Reads 11.50 V |
| 2 | Open tooltip | LATEST = 0/10 Critical (red) |

#### Test Data

```
latest_voltage: 11.50 V
```

**Postconditions:**
- LATEST=0 persisted

**Status:** Not Run  
**Notes:** 

---

### BATT-041: Verify scoring LATEST signal as 5 pts neutral fallback when no telemetry message exists in last 24 h

**Screen / Section:** Battery Health & Replacement Forecast — §3.6 LATEST Signal — neutral fallback  
**Priority:** Medium  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** NEW v4 coverage: when no telemetry message exists (device offline >24 h or never reported), LATEST falls back to 5 pts neutral. Review §3.6 flagged this as untested.

**Preconditions:**
- Device has no message in the last 24 h (offline)

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Confirm no recent message | Last message age > 24 h |
| 2 | Open tooltip | LATEST = 5/10 Neutral (grey) with text 'No live data' |

#### Test Data

```
last_message_age_h: 48
```

**Postconditions:**
- LATEST=5 persisted with fallback_reason='no_telemetry'

**Status:** Not Run  
**Notes:** New in v4 — closes review §3.6 neutral-fallback gap.

---

## Forecast Logic (§4)

### BATT-042: Verify forecast base projection equals (live_voltage − 11.5) / abs(slope_per_day) clamped to 0–90 days

**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast — Step 1 Base Projection  
**Priority:** High  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Base forecast = (live_voltage − 11.5) / abs(slope_per_day), clamped to 0–90 days. Validates the core projection formula before modifiers.

**Preconditions:**
- live_voltage=12.50 V, slope=−0.010 V/day → expected base = (12.5−11.5)/0.010 = 100 → clamp to 90 d

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Seed inputs and trigger forecast | Forecast runs |
| 2 | Inspect forecast_audit.base_days | 100 (before clamp) |
| 3 | Inspect forecast_audit.base_clamped | 90 (after clamp to max 90) |

#### Test Data

```
live_voltage:  12.50 V
slope_per_day: -0.010 V/day
expected_base: 100 -> clamped 90
```

**Postconditions:**
- forecast_audit.base_clamped = 90

**Status:** Not Run  
**Notes:** 

---

### BATT-043: Verify forecast base is set to 90 days when slope is flat (≈0) or positive

**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast — Step 1 (flat/positive slope)  
**Priority:** High  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** When slope is flat (~0) or positive (stable battery), base is set to the 90-day ceiling regardless of voltage. Prevents division-by-zero and infinite forecasts.

**Preconditions:**
- live_voltage=12.40 V, slope=+0.001 V/day (positive)

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Run forecast with positive slope | Forecast runs without error |
| 2 | Inspect base_days | 90 |
| 3 | Repeat with slope = 0.0 | base_days = 90 |
| 4 | Repeat with slope = −1e-6 (essentially flat) | base_days = 90 (clamped from huge value) |

#### Test Data

```
slope_positive: +0.001
slope_zero:      0.0
slope_flat:     -1e-6
```

**Postconditions:**
- No division-by-zero errors; base capped at 90 d

**Status:** Not Run  
**Notes:** 

---

### BATT-044: Verify forecast applies modifier compounding correctly after redundancy guard de-duplicates correlated conditions

**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast — Steps 2 & 3 (modifiers + redundancy guard)  
**Priority:** High  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Modifiers are multiplied after the redundancy guard de-duplicates correlated conditions (low REST + deep discharges = one penalty). Worst-case combined multiplier is 0.5 × 0.5 × 0.7 = 0.175.

**Preconditions:**
- Vehicle has: crank<9.5 V (×0.5), mean_rest<11.8 V (×0.5), 2 deep discharges (×0.7)
- Redundancy guard knows rest<11.8 V and deep_discharge are correlated → keep only harsher

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Run forecast | Forecast runs |
| 2 | Inspect modifier_list_pre_guard | Contains all 3 modifiers |
| 3 | Inspect modifier_list_post_guard | Contains crank×0.5 and either rest×0.5 OR deep×0.7 (the harsher), not both |
| 4 | Verify final multiplier | Equals 0.5 × 0.5 = 0.25 (rest kept over deep) — base × 0.25 |

#### Test Data

```
modifiers_in:        crank<9.5 (×0.5), rest<11.8 (×0.5), deep>=2 (×0.7)
expected_post_guard: crank<9.5, rest<11.8 (deep dropped)
expected_multiplier: 0.25
```

**Postconditions:**
- forecast_audit.final_multiplier = 0.25 ± 0.001

**Status:** Not Run  
**Notes:** 

---

### BATT-045: Verify forecast is clamped to 14 days and band is forced to Critical when modifier stack would push below 14  🟧 PENDING

**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast — Step 4 (14-day floor + Critical override)  
**Priority:** High  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Minimum forecast = 14 days. Any modifier stack that would push below 14 is clamped to 14, AND the band is forced to Critical regardless of score.

**Preconditions:**
- Seeded vehicle with base=60 d and combined multiplier=0.10 → would be 6 d before clamp
- Score sums to 78 (Fair) — would normally band Fair, not Critical

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Run forecast | Pipeline runs |
| 2 | Inspect forecast_days_raw | 6 (pre-clamp) |
| 3 | Inspect forecast_days_final | 14 (clamped) |
| 4 | Inspect final_band | Critical (forced override, despite score=78) |

#### Test Data

```
base_days:           60
combined_multiplier: 0.10
raw_forecast:         6
expected_final:      14
expected_band:       Critical
```

**Postconditions:**
- forecast=14; band=Critical; override_reason='floor_breach'

**Status:** Not Run  
**Notes:** Blocked by CQ-003 — see Clarify Requirements. Need a sandbox vehicle whose modifier stack produces sub-14-day base; awaiting data.

---

### BATT-046: Verify forecast resets to 90 days when calc 2805166 (Battery Replacement) fires within the last 24 hours

**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast — Replacement override  
**Priority:** High  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** If calc 2805166 (Battery Replacement) fires within 24 h, the forecast must reset to 90 days regardless of all other inputs.

**Preconditions:**
- Vehicle had 14 d forecast before swap
- Calc 2805166 emitted a replacement event 2 h ago

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Inspect forecast_audit.replacement_event_age | 2 h |
| 2 | Inspect forecast_days_final | 90 (override) |
| 3 | Inspect band | Excellent (override drives band as well) |
| 4 | Confirm override is logged | forecast_audit.override_reason='battery_replacement' |

#### Test Data

```
calc_2805166_age_h: 2
forecast_before:    14
forecast_after:     90
```

**Postconditions:**
- forecast=90, band=Excellent for 24 h after replacement event

**Status:** Not Run  
**Notes:** 

---

### BATT-047: Verify a healthy vehicle scores 100 points end-to-end and lands in the Excellent band with 90-day forecast

**Screen / Section:** Battery Health & Replacement Forecast — §2 + §5 End-to-end  
**Priority:** High  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Perfect 100 happy path: a healthy fleet vehicle scores all 6 signals at max and lands in the Excellent band with a 90-day forecast.

**Preconditions:**
- All 6 signals at max: REST=30, CRANK=25, TREND=12, DECAY=13, CHARGE=10, LATEST=10
- No modifiers should be armed

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Run full pipeline | Pipeline completes |
| 2 | Read total score | 100 |
| 3 | Read forecast | 90 days |
| 4 | Read band | Excellent (green) |
| 5 | Open tooltip | All 6 rows green; summary 'Battery is healthy' |

#### Test Data

```
rest:30 crank:25 trend:12 decay:13 charge:10 latest:10 -> 100
expected_forecast: 90 d
expected_band:     Excellent
```

**Postconditions:**
- score=100, forecast=90, band=Excellent

**Status:** Not Run  
**Notes:** 

---

### BATT-048: Verify forecast base is clamped to zero when live voltage is at or below the 11.5 V floor

**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast — clamp lower bound  
**Priority:** Medium  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** If base computation yields negative (live voltage already below 11.5 V floor), base must clamp to 0 — not become negative.

**Preconditions:**
- live_voltage=11.30 V, slope=−0.005 V/day → raw = −40

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Run forecast | Runs without error |
| 2 | Inspect base_days_raw | −40 |
| 3 | Inspect base_days_clamped | 0 |
| 4 | Final forecast after floor | 14 (forced by 14-day floor rule) |
| 5 | Band | Critical |

#### Test Data

```
live_voltage: 11.30 V
slope:        -0.005 V/day
```

**Postconditions:**
- No negative forecast; final=14; band=Critical

**Status:** Not Run  
**Notes:** 

---

### BATT-049: Verify forecast applies ×0.7 modifier when calc 2805152 records 2 or more deep-discharge events

**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast — Deep Discharge modifier  
**Priority:** High  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Deep-discharge events ≥ 2 in 30 d apply ×0.7 forecast modifier — battery damaged by being run flat.

**Preconditions:**
- Calc 2805152 (Deep Discharge) fired 3 times in last 30 d; no other modifiers

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Inspect modifier list | Contains 'deep_discharge>=2_x0.7' |
| 2 | Compute expected | forecast_final = base × 0.7 |
| 3 | Verify forecast value | Matches expectation within ±1 d rounding |

#### Test Data

```
deep_discharge_events: 3
expected_modifier:     0.7
```

**Postconditions:**
- forecast_audit shows ×0.7 applied

**Status:** Not Run  
**Notes:** 

---

### BATT-050: Verify forecast applies ×0.6 modifier when calc 2805149 records 1 or more alternator-failure events

**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast — Alternator Failure modifier  
**Priority:** High  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** ≥ 1 alternator failure event (calc 2805149) applies ×0.6 modifier — charging system unreliable.

**Preconditions:**
- Calc 2805149 fired once in last 30 d; no other modifiers

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Inspect modifier list | Contains 'alternator>=1_x0.6' |
| 2 | Verify forecast value | = base × 0.6 |

#### Test Data

```
alternator_events: 1
expected_modifier: 0.6
```

**Postconditions:**
- forecast_audit shows ×0.6 applied

**Status:** Not Run  
**Notes:** 

---

### BATT-051: Verify CRANK ×0.5 forecast modifier fires when compensated crank_dip is < 9.5 V even at the 13-pt scoring tier

**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast — CRANK modifier threshold  
**Priority:** High  
**Type:** Regression  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** NEW v4 coverage: ×0.5 CRANK forecast modifier must fire at any compensated crank <9.5 V (not only <8.0 V). A vehicle scoring 13 CRANK points still arms the modifier. Review §4.3 flagged this as untested.

**Preconditions:**
- Compensated min crank_dip = 9.20 V (→ CRANK score 13 pts, see BATT-011)

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Trigger pipeline | Runs |
| 2 | Inspect CRANK score | 13/25 |
| 3 | Inspect forecast_audit modifier_list | Contains 'crank<9.5_x0.5' |
| 4 | Verify final forecast value | Has ×0.5 applied |

#### Test Data

```
min_crank_compensated: 9.20 V
expected_score:        13
expected_modifier:     0.5
```

**Postconditions:**
- ×0.5 modifier active despite CRANK score being above 0

**Status:** Not Run  
**Notes:** New in v4 — closes review §4.3 gap. The modifier threshold (9.5) is independent of the 0-pt threshold (8.0).

---

## Health Bands (§5)

### BATT-052: Verify health band transitions cleanly from Excellent (95 pts) to Good (94 pts) at the 95-point boundary

**Screen / Section:** Battery Health & Replacement Forecast — §5 Health Bands  
**Priority:** High  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Excellent band requires 95–100. Vehicle at 95 = Excellent; vehicle at 94 = Good. Validates the most prestige boundary.

**Preconditions:**
- Two seeded scores: 95 and 94, both with forecast=90

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Seed score=95 and recalc | Band = Excellent (green dot) |
| 2 | Seed score=94 and recalc | Band = Good (green dot, different label) |

#### Test Data

```
score_a:  95
score_b:  94
forecast: 90 d
```

**Postconditions:**
- A: band=Excellent; B: band=Good

**Status:** Not Run  
**Notes:** 

---

### BATT-053: Verify band lands at the most-restrictive value when score and forecast disagree

**Screen / Section:** Battery Health & Replacement Forecast — §5 Health Bands — most-restrictive rule  
**Priority:** High  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Vehicle lands in most-restrictive band triggered by either score OR forecast. Good score (85) with Poor forecast (25 d) must band Poor, not Good.

**Preconditions:**
- Score=85 (Good range), forecast=25 d (Poor range)

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Run pipeline | Runs |
| 2 | Inspect band | Poor (orange) — driven by forecast, not score |
| 3 | Inspect band_audit | band_source='forecast' |

#### Test Data

```
score:         85
forecast_days: 25
```

**Postconditions:**
- band=Poor; band_audit.source='forecast'

**Status:** Not Run  
**Notes:** 

---

### BATT-054: Verify Fair band when score is 72 and forecast is 38 days

**Screen / Section:** Battery Health & Replacement Forecast — §5 Health Bands — Fair  
**Priority:** Medium  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Fair band: score 65–79 OR forecast 30–44 days.

**Preconditions:**
- score=72, forecast=38 d

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Run pipeline | Runs |
| 2 | Inspect band | Fair (amber) |

#### Test Data

```
score:         72
forecast_days: 38
```

**Postconditions:**
- band=Fair

**Status:** Not Run  
**Notes:** 

---

### BATT-055: Verify Poor band when score is 57 and forecast is 32 days

**Screen / Section:** Battery Health & Replacement Forecast — §5 Health Bands — Poor  
**Priority:** Medium  
**Type:** Functional  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Poor band: score 50–64 OR forecast <30 days.

**Preconditions:**
- score=57, forecast=32 d (score drives Poor)

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Run pipeline | Runs |
| 2 | Inspect band | Poor (orange) |

#### Test Data

```
score:         57
forecast_days: 32
```

**Postconditions:**
- band=Poor

**Status:** Not Run  
**Notes:** 

---

### BATT-056: Verify Critical band when total score is under 50

**Screen / Section:** Battery Health & Replacement Forecast — §5 Health Bands — Critical  
**Priority:** High  
**Type:** Negative  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Critical band when score <50 OR forecast <14 days. The hardest fail condition — REPLACE badge should fire.

**Preconditions:**
- score=42

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Run pipeline | Runs |
| 2 | Inspect band | Critical (red) |
| 3 | Confirm REPLACE badge in Status column | Visible |

#### Test Data

```
score: 42
```

**Postconditions:**
- band=Critical; REPLACE badge active

**Status:** Not Run  
**Notes:** 

---

### BATT-057: Verify Good score is downgraded to Fair band when forecast lands in [30, 45) days

**Screen / Section:** Battery Health & Replacement Forecast — §5 Health Bands — forecast override  
**Priority:** High  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** NEW v4 coverage: a Good-band score (e.g. 85) combined with a Fair-band forecast (30–44 d) must downgrade the row to Fair via the most-restrictive rule. Review §4.5 flagged this gap.

**Preconditions:**
- score=85 (Good), forecast=40 d (Fair)

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Run pipeline | Runs |
| 2 | Inspect band | Fair — forecast wins |
| 3 | Inspect band_audit | band_source='forecast', original_score_band='Good' |

#### Test Data

```
score:         85
forecast_days: 40
expected_band: Fair
```

**Postconditions:**
- band=Fair; band_audit.source='forecast'

**Status:** Not Run  
**Notes:** New in v4 — closes review §4.5 gap.

---

## Score Formula (§2)

### BATT-058: Verify the score formula maxes sum to exactly 100 points across all 6 signals in v2.2

**Screen / Section:** Battery Health & Replacement Forecast — §2 Score Formula  
**Priority:** High  
**Type:** Regression  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Sum of all signal maxes must equal 100. Guard against rebalancing arithmetic errors.

**Preconditions:**
- Pipeline running v2.2 weightings

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Inspect signal weight table | REST 30 + CRANK 25 + TREND 12 + DECAY 13 + CHARGE 10 + LATEST 10 |
| 2 | Compute sum | = 100 |

#### Test Data

```
weights: 30 + 25 + 12 + 13 + 10 + 10 = 100
```

**Postconditions:**
- Sum-check passes

**Status:** Not Run  
**Notes:** 

---

### BATT-059: Verify pipeline applies v2.2 weightings (REST=30, TREND=12, DECAY=13, CHARGE=10) and no longer uses v2.1 weightings

**Screen / Section:** Battery Health & Replacement Forecast — §2 Score Formula — v2.1→v2.2 regression  
**Priority:** High  
**Type:** Regression  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** v2.2 introduced CHARGE (+10) and rebalanced REST (35→30), TREND (15→12), DECAY (15→13). Make sure no production code still uses v2.1 weights.

**Preconditions:**
- Pipeline build = v2.2; reference vehicle scores known under both schemes

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Inspect signal weight configuration in code/config | Matches v2.2 exactly |
| 2 | Re-score the reference vehicle | Score matches v2.2 expectation, not v2.1 |

#### Test Data

```
v2_1: rest=35, trend=15, decay=15, charge=0
v2_2: rest=30, trend=12, decay=13, charge=10
```

**Postconditions:**
- Score history shows the version stamp 'v2.2'

**Status:** Not Run  
**Notes:** 

---

### BATT-060: Verify MURANO test vehicle drops from 100 to 90 between v2.1 and v2.2 due to CHARGE signal addition

**Screen / Section:** Battery Health & Replacement Forecast — §2 Score Formula — MURANO regression  
**Priority:** High  
**Type:** Regression  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** Real-world regression: MURANO vehicle scored 100/100 under v2.1 but dropped to 90/100 under v2.2 because CHARGE (72% absorption) was added. Use to lock the bug fix in place.

**Preconditions:**
- MURANO reference dataset replayed against v2.1 and v2.2 pipelines

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Score MURANO with v2.1 pipeline | 100/100 |
| 2 | Score MURANO with v2.2 pipeline | 90/100 — CHARGE = 0/10 (abs%=72), band = Good |
| 3 | Confirm band change | v2.1: Excellent; v2.2: Good |

#### Test Data

```
vehicle:        MURANO
v2_1_score:     100 (Excellent)
v2_2_score:      90 (Good)
charge_in_v2_2:   0/10 (abs=72%)
```

**Postconditions:**
- Both scores reproducible; v2.2 reflects the duty-cycle reality

**Status:** Not Run  
**Notes:** 

---

## Status Column / Badges

### BATT-061: Verify all 8 Status column badges (DEEP DISCHARGE, ALTERNATOR, PARK DRAIN, TREND↓, CHARGE↓, SHORT↓, REPLACE, HEALTHY) fire under their documented trigger conditions  🟧 PENDING

**Screen / Section:** Fleet Pulse: Status Column Spec — All badge triggers  
**Priority:** High  
**Type:** Functional  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)

**Requirement Summary:** The renamed Status column must surface 8 badge types: DEEP DISCHARGE, ALTERNATOR, PARK DRAIN, TREND↓, CHARGE↓, SHORT↓, REPLACE, HEALTHY. Validate each fires under its precise trigger.

**Preconditions:**
- 8 seeded test vehicles, each engineered to trigger exactly one badge

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Seed deep_discharge_events=2 on vehicle 1 | DEEP DISCHARGE badge visible |
| 2 | Seed alternator_events=1 on vehicle 2 | ALTERNATOR badge visible |
| 3 | Seed decay slope >0.015 V/hr on vehicle 3 | PARK DRAIN badge visible |
| 4 | Seed slope < −0.008 V/day on vehicle 4 | TREND↓ badge visible |
| 5 | Seed abs%<90 on vehicle 5 | CHARGE↓ badge visible (pending CQ-001 threshold confirmation) |
| 6 | Seed short%>70 on vehicle 6 | SHORT↓ badge visible |
| 7 | Seed score<50 or replacement event on vehicle 7 | REPLACE badge visible |
| 8 | Use clean healthy vehicle 8 | HEALTHY badge visible (no other badge active) |

#### Test Data

```
vehicles:            8 seeded states
badge_count_per_row: 1
```

**Postconditions:**
- Each vehicle row shows exactly its expected badge

**Status:** Not Run  
**Notes:** Blocked by CQ-007 — see Clarify Requirements. Also impacted by CQ-001 (CHARGE↓ threshold). Execute under current assumption and re-run after CQ closure.

---

### BATT-062: Verify multiple Status pills are ordered red, then amber, then green left-to-right on the row

**Screen / Section:** Fleet Pulse: Status Column Spec — Pill ordering  
**Priority:** Medium  
**Type:** UI  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)

**Requirement Summary:** When multiple badges fire on one row, pills must order by severity: red before amber before green. Drives operator attention to the worst signal first.

**Preconditions:**
- Vehicle seeded with REPLACE (red), TREND↓ (amber), HEALTHY (green) — but HEALTHY should suppress when others fire

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Open the row | Pills render in this order: REPLACE, TREND↓ |
| 2 | Confirm HEALTHY is suppressed when any other badge fires | No green pill present |
| 3 | Repeat with: ALTERNATOR (red), CHARGE↓ (amber), SHORT↓ (amber) | Order: ALTERNATOR, CHARGE↓, SHORT↓ |

#### Test Data

```
case_a: REPLACE + TREND↓
case_b: ALTERNATOR + CHARGE↓ + SHORT↓
```

**Postconditions:**
- Pills follow severity ordering rule

**Status:** Not Run  
**Notes:** 

---

### BATT-063: Verify Status column shows at most 3 pills and renders '+N more' overflow when more pills are active  🟧 PENDING

**Screen / Section:** Fleet Pulse: Status Column Spec — Overflow  
**Priority:** Medium  
**Type:** UI  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)

**Requirement Summary:** Maximum 3 visible pills per row; additional pills collapse into '+N more'. Prevents the column from growing arbitrarily wide.

**Preconditions:**
- Vehicle seeded with 5 simultaneous badges

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Open the row | 3 pills visible (in severity order) |
| 2 | Confirm '+2 more' rendered after the 3rd pill | Overflow chip visible |
| 3 | Interact with '+2 more' chip per PRD | Behaviour matches CQ-006 resolution (hover/click) |

#### Test Data

```
active_badges:           REPLACE, ALTERNATOR, DEEP DISCHARGE, TREND↓, CHARGE↓ (5 total)
expected_visible:        3
expected_overflow_label: +2 more
```

**Postconditions:**
- 3 pills + overflow chip rendered

**Status:** Not Run  
**Notes:** Blocked by CQ-006 — see Clarify Requirements. Hover vs click interaction TBD.

---

### BATT-064: Verify HEALTHY pill is shown on rows where no other badges fire so the Status column never renders empty

**Screen / Section:** Fleet Pulse: Status Column Spec — Always one pill  
**Priority:** Medium  
**Type:** Functional  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)

**Requirement Summary:** At least one pill must always render. HEALTHY is shown when no other badges fire — ensures column never looks empty.

**Preconditions:**
- Reference healthy vehicle: score=100, no events

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Open the row | Single HEALTHY pill (green) renders |
| 2 | Trigger any other badge (e.g. deep_discharge=2) | HEALTHY disappears; new badge takes its place |
| 3 | Clear the trigger | HEALTHY re-appears |

#### Test Data

```
reference_vehicle:    clean (no events)
badge_count_expected: 1 (HEALTHY)
```

**Postconditions:**
- Status cell always non-empty; HEALTHY appears only when alone

**Status:** Not Run  
**Notes:** 

---

### BATT-065: Verify Status column renders the correct plain-English summary line for each of the 9 canonical badge combinations  🟧 PENDING

**Screen / Section:** Fleet Pulse: Status Column Spec — Plain-English summary line  
**Priority:** Medium  
**Type:** Functional  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)

**Requirement Summary:** Each Status state should show a one-line plain-English summary below the pills. 9 combinations cover all canonical fleet scenarios.

**Preconditions:**
- 9 seeded vehicles each in a canonical state per spec

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | For each of 9 vehicles, open the row | Summary line matches PRD text |
| 2 | Validate exact strings letter-for-letter against the spec | All 9 strings match |

#### Test Data

```
combinations:     9 (per Status spec)
expected_strings: see Health Score Tooltip Spec page
```

**Postconditions:**
- All 9 summary strings rendered correctly

**Status:** Not Run  
**Notes:** Blocked by CQ-005 — see Clarify Requirements. Column header (Status/Active Alerts/Health Flags) still TBD.

---

### BATT-066: Verify Status column sorts rows by worst-severity badge first (red > amber > green)

**Screen / Section:** Fleet Pulse: Status Column Spec — Column sortability  
**Priority:** Low  
**Type:** UI  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)

**Requirement Summary:** Status column must sort by worst severity per row (red > amber > green), not alphabetically. Drives the worst-first triage workflow.

**Preconditions:**
- Fleet of 10 vehicles, varied badge mix

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Click the Status column header | Sort indicator appears |
| 2 | Inspect row order | Rows with a red badge are at the top, amber next, green last |
| 3 | Click again to invert sort | Order reverses correctly |

#### Test Data

```
vehicles:       10 mixed
expected_order: red-first then amber then green
```

**Postconditions:**
- Sort order matches severity rule

**Status:** Not Run  
**Notes:** 

---

### BATT-067: Verify Status column hides the summary line and keeps pills visible on viewports narrower than 600 px

**Screen / Section:** Fleet Pulse: Status Column Spec — Mobile narrow column behaviour  
**Priority:** Low  
**Type:** UI  
**Environment:** Mobile (iOS 17+ / Android 13+)

**Requirement Summary:** On viewports < 600 px, the plain-English summary line must be hidden so badges remain readable. Pills themselves stay.

**Preconditions:**
- Open Fleet Pulse on a viewport sized 599 px wide

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Open Fleet Pulse at 599 px width | Status column renders |
| 2 | Inspect a row with 2 badges + summary line | Pills visible; summary line hidden |
| 3 | Resize to 600 px | Summary line becomes visible again |

#### Test Data

```
viewport: 599 px (hide), 600 px (show)
```

**Postconditions:**
- Summary line breakpoint behaves correctly

**Status:** Not Run  
**Notes:** 

---

## Health Score Tooltip

### BATT-068: Verify Health Score tooltip opens on hover/focus and closes on blur, mouseleave, and Escape

**Screen / Section:** Fleet Pulse: Health Score Tooltip Spec — Open/close interactions  
**Priority:** Medium  
**Type:** UI  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)

**Requirement Summary:** Tooltip opens on hover (desktop) and on focus (keyboard). Closes on blur, mouseleave, or Escape. Critical for keyboard accessibility (WCAG 2.1).

**Preconditions:**
- Fleet Pulse dashboard open; any vehicle row visible

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Hover the Health Score chip | Tooltip opens within 150 ms |
| 2 | Move pointer off the chip | Tooltip closes |
| 3 | Tab focus to the chip via keyboard | Tooltip opens on focus |
| 4 | Press Escape | Tooltip closes; focus retained on chip |
| 5 | Tab away from chip | Tooltip closes on blur |

#### Test Data

```
trigger: hover, focus
close:   blur, mouseleave, Escape
```

**Postconditions:**
- All 5 open/close interactions match spec

**Status:** Not Run  
**Notes:** 

---

### BATT-069: Verify Health Score tooltip renders 6 sub-signal rows with friendly labels (not raw values or weights)

**Screen / Section:** Fleet Pulse: Health Score Tooltip Spec — Sub-signal rows  
**Priority:** Medium  
**Type:** UI  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)

**Requirement Summary:** Tooltip shows 6 rows (one per signal) with friendly labels (e.g. 'Rest voltage', 'Cranking strength'). Should NOT show raw values or formula weights.

**Preconditions:**
- Tooltip open on a vehicle row

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Read the 6 row labels | REST→'Rest voltage', CRANK→'Cranking strength', TREND→'Trend', DECAY→'Park drain', CHARGE→'Charging quality', LATEST→'Latest reading' |
| 2 | Confirm no row shows raw V or V/hr | No raw numbers displayed |
| 3 | Confirm no row shows weight (e.g. '/30') | No '/N' weight tokens displayed |

#### Test Data

```
expected_labels: Rest voltage / Cranking strength / Trend / Park drain / Charging quality / Latest reading
```

**Postconditions:**
- 6 rows present with the correct labels

**Status:** Not Run  
**Notes:** 

---

### BATT-070: Verify Health Score tooltip dot colours follow the ≥80% green / 40–79% amber / <40% red rule across all 6 rows  🟧 PENDING

**Screen / Section:** Fleet Pulse: Health Score Tooltip Spec — Dot colour thresholds  
**Priority:** Medium  
**Type:** UI  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)

**Requirement Summary:** Dot colour rule: ≥80% green, 40–79% amber, <40% red, where % = score / max for that signal. Drives the at-a-glance row colours.

**Preconditions:**
- 3 seeded vehicles producing one row at each colour

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Open tooltip on green-row vehicle | All 6 dots green (each signal ≥80%) |
| 2 | Open tooltip on amber-row vehicle | Each ≥40% and <80% renders amber |
| 3 | Open tooltip on red-row vehicle | Each <40% renders red |
| 4 | Test exactly at 40% boundary | Behaviour matches CQ-004 resolution |
| 5 | Test exactly at 80% boundary | Green per spec |

#### Test Data

```
thresholds:     green ≥80%, amber 40-79%, red <40%
boundary_cases: 40%, 80%
```

**Postconditions:**
- Dot colours match thresholds at all percentages

**Status:** Not Run  
**Notes:** Blocked by CQ-004 — see Clarify Requirements. 40% boundary inclusion still TBD.

---

### BATT-071: Verify Health Score tooltip displays neither formula weights (e.g. /30) nor raw voltage values

**Screen / Section:** Fleet Pulse: Health Score Tooltip Spec — No raw values / weights  
**Priority:** Medium  
**Type:** UI  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)

**Requirement Summary:** Tooltip is for non-technical operators. Formula weights (e.g. '/30') and raw V readings MUST NOT appear in the tooltip body.

**Preconditions:**
- Tooltip open on a healthy vehicle

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Inspect tooltip body text | No occurrences of '/30', '/25', etc. |
| 2 | Inspect tooltip body text | No occurrences of 'V' or '°C' or 'V/day' values |
| 3 | Inspect tooltip body text | Only friendly labels and dot colours present |

#### Test Data

```
forbidden_tokens: /30 /25 /12 /13 /10 V V/hr V/day
```

**Postconditions:**
- No forbidden tokens present in tooltip

**Status:** Not Run  
**Notes:** 

---

### BATT-072: Verify Health Score tooltip band label uses the documented hex colour for each of the 5 bands

**Screen / Section:** Fleet Pulse: Health Score Tooltip Spec — Band label colour  
**Priority:** Medium  
**Type:** UI  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)

**Requirement Summary:** Band label inside the tooltip is colour-coded per band hex (Excellent #1B873F, Good #2E7D32, Fair #F4A300, Poor #E76F00, Critical #C0392B).

**Preconditions:**
- 5 seeded vehicles, one per band

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Open tooltip on Excellent vehicle | Band label colour = #1B873F |
| 2 | Open tooltip on Good vehicle | = #2E7D32 |
| 3 | Open tooltip on Fair vehicle | = #F4A300 |
| 4 | Open tooltip on Poor vehicle | = #E76F00 |
| 5 | Open tooltip on Critical vehicle | = #C0392B |

#### Test Data

```
hexes: 1B873F 2E7D32 F4A300 E76F00 C0392B
```

**Postconditions:**
- All 5 band labels render the correct hex

**Status:** Not Run  
**Notes:** 

---

### BATT-073: Verify Health Score tooltip opens as a modal sheet on tap when viewport is narrower than 480 px

**Screen / Section:** Fleet Pulse: Health Score Tooltip Spec — Mobile modal  
**Priority:** Low  
**Type:** UI  
**Environment:** Mobile (iOS 17+ / Android 13+)

**Requirement Summary:** On viewports < 480 px the tooltip must open as a tap-to-open modal sheet rather than an inline tooltip. Tap-anywhere-to-close dismisses.

**Preconditions:**
- Fleet Pulse open on mobile viewport 479 px wide

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Tap the Health Score chip | Modal sheet opens (full-width, centered) |
| 2 | Tap outside the modal | Modal closes |
| 3 | Resize to 480 px and tap again | Inline tooltip behaviour returns |

#### Test Data

```
viewport: 479 px (modal), 480 px (tooltip)
```

**Postconditions:**
- Breakpoint switches presentation correctly

**Status:** Not Run  
**Notes:** 

---

## UI Display

### BATT-074: Verify all 6 sub-signal rows are visible inside the Health Score tooltip without internal scrolling

**Screen / Section:** Fleet Pulse: Status Column Spec + Fleet Pulse: Health Score Tooltip Spec  
**Priority:** Medium  
**Type:** UI  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)

**Requirement Summary:** All 6 sub-signal rows must fit inside the default tooltip viewport without internal scrolling. Visual sanity check.

**Preconditions:**
- Browser viewport ≥ 1024 px wide, default zoom 100%

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Open tooltip on a vehicle row | Tooltip opens |
| 2 | Count visible rows | 6 sub-signal rows fully visible |
| 3 | Confirm no scrollbar in tooltip body | No scrollbar |

#### Test Data

```
viewport_min_width: 1024 px
zoom:               100%
```

**Postconditions:**
- No internal scroll on tooltip

**Status:** Not Run  
**Notes:** 

---

### BATT-075: Verify forecast is displayed as relative days (e.g. '47 days') not as a calendar date

**Screen / Section:** Battery Health & Replacement Forecast — §4 Forecast display  
**Priority:** Medium  
**Type:** UI  
**Environment:** Web (Chrome 120+, Firefox 121+, Safari 17+)

**Requirement Summary:** Forecast must display as relative days (e.g. '47 days') NOT a calendar date. Avoids timezone confusion across the fleet.

**Preconditions:**
- Vehicle with forecast=47 d

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Open the row | Forecast renders as '47 days' |
| 2 | Inspect DOM text | No date format (YYYY-MM-DD or similar) anywhere in the forecast cell |

#### Test Data

```
forecast_days:    47
expected_display: '47 days'
```

**Postconditions:**
- Display matches expected format

**Status:** Not Run  
**Notes:** 

---

## WeatherAPI fallback

### BATT-076: Verify CRANK temperature compensation falls back to the most recent GPS fix within 7 days when current fix is missing

**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal (WeatherAPI)  
**Priority:** Low  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** NEW v4 coverage: when the vehicle has no GPS fix at the time of a crank event, WeatherAPI cannot resolve ambient temperature. The pipeline must fall back to the last-known fix within 7 days. Review §4.10 flagged this gap.

**Preconditions:**
- Vehicle has a crank event with no concurrent GPS fix
- Last known GPS fix was 3 days ago at a location whose WeatherAPI temp = 18 °C

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Run CRANK pipeline on the event | Pipeline runs |
| 2 | Inspect ambient_temp_source | 'last_known_fix_within_7d' |
| 3 | Inspect ambient_temp_c | 18 °C |
| 4 | Inspect compensated_crank_dip | Computed using 18 °C, not 25 °C default |

#### Test Data

```
event_has_gps:     false
last_fix_age_days: 3
last_fix_temp_c:   18
```

**Postconditions:**
- forecast_audit.temp_source = 'last_known_fix_within_7d'

**Status:** Not Run  
**Notes:** New in v4 — closes review §4.10 gap (no GPS scenario).

---

### BATT-077: Verify CRANK temperature compensation falls back to 25 °C baseline when no GPS fix exists within the last 7 days

**Screen / Section:** Battery Health & Replacement Forecast — §3.2 CRANK Signal (WeatherAPI)  
**Priority:** Low  
**Type:** Edge Case  
**Environment:** Mixed — Web (Chrome 120+) + Backend (Flespi calc)

**Requirement Summary:** NEW v4 coverage: when no GPS fix exists in the last 7 days either, the pipeline must fall back to the 25 °C baseline (zero adjustment) and flag the event. Review §4.10 flagged this gap.

**Preconditions:**
- No GPS fix in the last 7 days for the vehicle

#### Steps

| # | Action | Expected Result |
|---|--------|-----------------|
| 1 | Run CRANK pipeline on a crank event in this state | Pipeline runs |
| 2 | Inspect ambient_temp_source | 'baseline_default' |
| 3 | Inspect ambient_temp_c | 25 °C |
| 4 | Inspect compensation factor | 0.025 × (25 − 25) = 0 (no adjustment) |
| 5 | Inspect forecast_audit.warnings | Contains 'temp_fallback_baseline' |

#### Test Data

```
last_fix_age_days: 12
fallback_temp_c:   25
```

**Postconditions:**
- temp_source='baseline_default'; warning logged

**Status:** Not Run  
**Notes:** New in v4 — closes review §4.10 gap (no fix within 7 d).

---

## Clarify Requirements (CQ Log)

> Orange (#FFC000) rows in the Excel export. All linked TCs are flagged PENDING until resolution.

| Ref # | Related TC ID | Source / Reference | Conflict Description | Question to Client | Priority | Raised By | Raised Date | Answer / Resolution | Status | Resolved Date |
|-------|---------------|--------------------|----------------------|--------------------|----------|-----------|-------------|---------------------|--------|---------------|
| CQ-001 | BATT-037 | Fleet Pulse: Status Column Spec — CHARGE↓ badge threshold | Spec lists CHARGE score thresholds at <80% (4 pts) / <90% (7 pts) but the Status Column Spec describes the CHARGE↓ badge as firing when 'absorption is low' without a numeric cut-off. | Does the CHARGE↓ badge fire at absorption <90% (matching the 7-pt tier) or only <80% (matching the 0-pt tier)? | High | Hanna Lee | 2026-05-17 |  | Open |  |
| CQ-002 | BATT-033 | Battery Health & Replacement Forecast — §3.5 CHARGE Signal | The 4-pt CHARGE tier requires only absorption ≥80% — the short-trip fraction is not constrained at this tier. Unclear whether a vehicle with abs=82% and short=85% should land in 4 pts or 0 pts. | At the 4-pt CHARGE tier, is the short-trip fraction ignored (any value allowed) or does an implicit short<70% rule carry forward from the 7-pt tier? | Medium | Hanna Lee | 2026-05-17 |  | Open |  |
| CQ-003 | BATT-045 | Battery Health & Replacement Forecast — §4 Forecast Logic | Need a vehicle in staging whose modifier stack drives the forecast below 14 days so the floor + Critical override is testable. | Can the test team be provided with a sandbox vehicle/seeded data where (slope, modifiers) produce a base forecast <14 d before clamp? | High | Hanna Lee | 2026-05-17 |  | Open |  |
| CQ-004 | BATT-070 | Fleet Pulse: Health Score Tooltip Spec — Sub-signal dot colours | Spec states amber covers 40–79% and red covers <40%. The boundary value 40% itself is undefined — does a row at exactly 40% render amber or red? | Is the 40% boundary inclusive of amber (≥40% = amber) or red (<=40% = red)? | Medium | Hanna Lee | 2026-05-17 |  | Open |  |
| CQ-005 | BATT-065 | Fleet Pulse: Status Column Spec — Column header | Three candidate names appear across the design files: 'Status', 'Active Alerts', 'Health Flags'. | Which header text is final for the renamed column? | Medium | Hanna Lee | 2026-05-17 |  | Open |  |
| CQ-006 | BATT-063 | Fleet Pulse: Status Column Spec — '+N more' overflow | Unclear whether '+N more' is a hover-only tooltip, a click-to-expand chip, or both. | Is the '+N more' overflow interaction hover-only, click-only, or both (hover + click)? | Medium | Hanna Lee | 2026-05-17 |  | Open |  |
| CQ-007 | BATT-061 | Fleet Pulse: Status Column Spec — EV vehicles | Charge behaviour for BEVs is fundamentally different (regen / DC fast charge). Spec doesn't say if CHARGE↓ should be suppressed for EV stock (e.g. SEAL 627KB5). | Should the CHARGE↓ badge be suppressed on EV vehicles until EV-specific charge logic ships? | Medium | Hanna Lee | 2026-05-17 |  | Open |  |

---

## Summary

| TC ID | Screen / Section | Requirement Summary | Title | Type | Priority | Status |
|-------|------------------|---------------------|-------|------|----------|--------|
| **REST SIGNAL (§3.1)** | | | | | | |
| BATT-001 | Battery Health & Replacement Forecast — §3.1 REST Signal | REST contributes up to 30 pts of the 100-point Health Score. The top tier (≥12.7... | Verify scoring REST signal as 30 pts when 30-day mean rest_voltage_avg is ≥ 12.70 V | Functional | High | Not Run |
| BATT-002 | Battery Health & Replacement Forecast — §3.1 REST Signal | The Good tier (≥12.50 V and <12.70 V) must score 25 pts. Validates that the t... | Verify scoring REST signal as 25 pts when 30-day mean rest_voltage_avg is in [12.50 V, 12.70 V) | Functional | High | Not Run |
| BATT-003 | Battery Health & Replacement Forecast — §3.1 REST Signal | Fair tier (≥12.30 V and <12.50 V) scores 19 pts — first amber tier in the REST band. | Verify scoring REST signal as 19 pts when 30-day mean rest_voltage_avg is in [12.30 V, 12.50 V) | Functional | Medium | Not Run |
| BATT-004 | Battery Health & Replacement Forecast — §3.1 REST Signal | NEW v4 coverage: Poor tier (≥12.00 V and <12.30 V) must score 10 pts. This 10... | Verify scoring REST signal as 10 pts when 30-day mean rest_voltage_avg is in [12.00 V, 12.30 V) | Functional | High | Not Run |
| BATT-005 | Battery Health & Replacement Forecast — §3.1 REST Signal | Critical tier (<12.00 V) scores 0 pts. Catches batteries that are functionall... | Verify scoring REST signal as 0 pts when 30-day mean rest_voltage_avg is < 12.00 V | Negative | High | Not Run |
| BATT-006 | Battery Health & Replacement Forecast — §3.1 REST Signal | Neutral fallback: when no rest_voltage_avg samples exist (new vehicle, calc d... | Verify scoring REST signal as 15 pts neutral fallback when no rest_voltage_avg samples are present | Edge Case | Medium | Not Run |
| BATT-007 | Battery Health & Replacement Forecast — §3.1 REST Signal | The 12.70 V tier boundary must score 30 pts at exactly 12.70 V and 25 pts at ... | Verify REST score boundary transitions cleanly at 12.70 V (30 pts) vs 12.69 V (25 pts) | Edge Case | High | Not Run |
| BATT-008 | Battery Health & Replacement Forecast — §3.1 REST Signal | When live voltage is missing, the forecast must fall back to mean_rest as its... | Verify forecast reference voltage falls back to mean rest voltage when live voltage is missing | Edge Case | Medium | Not Run |
| **CRANK SIGNAL (§3.2)** | | | | | | |
| BATT-009 | Battery Health & Replacement Forecast — §3.2 CRANK Signal | Strong-cranking tier: minimum 30-day crank_dip (compensated to 25 °C) ≥ 10.0 V... | Verify scoring CRANK signal as 25 pts when minimum compensated crank_dip is ≥ 10.0 V | Functional | High | Not Run |
| BATT-010 | Battery Health & Replacement Forecast — §3.2 CRANK Signal | 20-pt tier boundary: ≥9.5 V scores 20, 9.4 V drops to 13 and additionally arm... | Verify CRANK score and forecast modifier transitions cleanly at 9.5 V (20 pts) vs 9.4 V (13 pts + ×0.5) | Edge Case | High | Not Run |
| BATT-011 | Battery Health & Replacement Forecast — §3.2 CRANK Signal | NEW v4 coverage: 13-pt 'Marginal' tier (≥9.0 V and <9.5 V). Review §3.2 flagged... | Verify scoring CRANK signal as 13 pts when minimum compensated crank_dip is in [9.0 V, 9.5 V) | Functional | High | Not Run |
| BATT-012 | Battery Health & Replacement Forecast — §3.2 CRANK Signal | Poor tier (≥8.0 V and <9.0 V) scores 6 pts. Validates the third-worst CRANK band. | Verify scoring CRANK signal as 6 pts when minimum compensated crank_dip is in [8.0 V, 9.0 V) | Functional | Medium | Not Run |
| BATT-013 | Battery Health & Replacement Forecast — §3.2 CRANK Signal | Critical CRANK (<8.0 V) scores 0 pts AND triggers the ×0.5 high-internal-resi... | Verify scoring CRANK signal as 0 pts and arming ×0.5 forecast modifier when compensated crank_dip is < 8.0 V | Negative | High | Not Run |
| BATT-014 | Battery Health & Replacement Forecast — §3.2 CRANK Signal — temperature... | Temperature compensation: crank_compensated = crank_observed + 0.025 × (25 − a... | Verify CRANK temperature compensation formula adds 0.475 V when raw crank is 9.6 V at 6 °C ambient | Functional | High | Not Run |
| BATT-015 | Battery Health & Replacement Forecast — §3.2 CRANK Signal — temperature... | At ambient 25 °C the compensation factor is zero — raw == compensated. Sanity... | Verify CRANK temperature compensation adds zero adjustment at the 25 °C baseline | Edge Case | Medium | Not Run |
| BATT-016 | Battery Health & Replacement Forecast — §3.2 CRANK Signal — REST fallback | When no crank events in 30 days, CRANK falls back proportionally to REST: CRA... | Verify CRANK signal falls back to round(25 × REST/30) when no crank events exist in 30-day window | Edge Case | Medium | Not Run |
| BATT-017 | Battery Health & Replacement Forecast — §3.2 CRANK Signal — calculator... | Regression: calc 2805150 selector MUST use min_active=0 with merge_message_be... | Verify calc 2805150 captures cranks correctly with min_active=0 and merge_message_before/after=true | Regression | High | Not Run |
| **TREND SIGNAL (§3.3)** | | | | | | |
| BATT-018 | Battery Health & Replacement Forecast — §3.3 TREND Signal | TREND scores 12 pts when the linear-regression slope of rest_voltage_avg over... | Verify scoring TREND signal as 12 pts when 30-day rest voltage regression slope is ≥ −0.003 V/day | Functional | High | Not Run |
| BATT-019 | Battery Health & Replacement Forecast — §3.3 TREND Signal | Mild-decline tier (≥ −0.008 and < −0.003 V/day) scores 9 pts. Indicates a gen... | Verify scoring TREND signal as 9 pts when 30-day slope is in [−0.008, −0.003) V/day | Functional | Medium | Not Run |
| BATT-020 | Battery Health & Replacement Forecast — §3.3 TREND Signal | NEW v4 coverage: 5-pt tier (≥ −0.015 V/day and < −0.008 V/day). Review §3.3 fl... | Verify scoring TREND signal as 5 pts when 30-day slope is in [−0.015, −0.008) V/day | Functional | High | Not Run |
| BATT-021 | Battery Health & Replacement Forecast — §3.3 TREND Signal | Critical decline (< −0.015 V/day) scores 0 pts — battery is losing ≥ 0.45 V o... | Verify scoring TREND signal as 0 pts when 30-day slope is < −0.015 V/day | Negative | High | Not Run |
| BATT-022 | Battery Health & Replacement Forecast — §3.3 TREND Signal — regression... | Regression: x-axis for slope regression MUST be (interval_begin + interval_en... | Verify TREND regression x-axis uses interval midpoint, not the calc emission timestamp | Regression | High | Not Run |
| BATT-023 | Battery Health & Replacement Forecast — §3.3 TREND Signal — neutral fal... | NEW v4 coverage: when sample count is insufficient for regression (e.g. <10 r... | Verify scoring TREND signal as 6 pts neutral fallback when fewer than 10 rest samples exist in the 30-day window | Edge Case | Medium | Not Run |
| **DECAY SIGNAL (§3.4)** | | | | | | |
| BATT-024 | Battery Health & Replacement Forecast — §3.4 DECAY Signal | DECAY scores 13 pts (max) when the parked decay slope is ≤ 0.003 V/hr — batter... | Verify scoring DECAY signal as 13 pts when parked decay slope is ≤ 0.003 V/hr | Functional | High | Not Run |
| BATT-025 | Battery Health & Replacement Forecast — §3.4 DECAY Signal | Boundary check: 0.003 V/hr → 13 pts; 0.0031 V/hr → 10 pts; 0.0061 V/hr → 7 pts... | Verify DECAY score boundary transitions at 0.003, 0.006, and 0.015 V/hr thresholds | Edge Case | Medium | Not Run |
| BATT-026 | Battery Health & Replacement Forecast — §3.4 DECAY Signal | NEW v4 coverage: 7-pt tier (0.006 V/hr < slope ≤ 0.010 V/hr). Review §3.4 flagg... | Verify scoring DECAY signal as 7 pts when parked decay slope is in (0.006, 0.010] V/hr | Functional | High | Not Run |
| BATT-027 | Battery Health & Replacement Forecast — §3.4 DECAY Signal | Critical DECAY (>0.015 V/hr) scores 0 pts AND triggers the ×0.7 self-discharg... | Verify scoring DECAY signal as 0 pts and arming ×0.7 forecast modifier when parked decay slope > 0.015 V/hr | Negative | High | Not Run |
| BATT-028 | Battery Health & Replacement Forecast — §3.4 DECAY Signal — data cleanup... | Two mandatory data-cleanup rules in DECAY: drop parks shorter than 6 h (noise... | Verify DECAY pipeline drops parks shorter than 6 h and parks starting above 13.5 V before computing slope | Functional | High | Not Run |
| BATT-029 | Battery Health & Replacement Forecast — §3.4 DECAY Signal — slope clamping | Negative slope (start < end during a park) is a surface-charge artefact, not... | Verify DECAY slope is clamped to zero when a park shows negative voltage change | Edge Case | Medium | Not Run |
| BATT-030 | Battery Health & Replacement Forecast — §3.4 DECAY Signal — neutral fal... | NEW v4 coverage: when no qualifying parks exist in 30-day window, DECAY falls... | Verify scoring DECAY signal as 7 pts neutral fallback when no qualifying parks exist in the 30-day window | Edge Case | Medium | Not Run |
| **CHARGE SIGNAL (§3.5)** | | | | | | |
| BATT-031 | Battery Health & Replacement Forecast — §3.5 CHARGE Signal | CHARGE (v2.2 NEW) scores 10 pts when hit_absorption% ≥ 95% AND short-trip% < ... | Verify scoring CHARGE signal as 10 pts when hit_absorption% is ≥ 95 and short_trip% is < 50 | Functional | High | Not Run |
| BATT-032 | Battery Health & Replacement Forecast — §3.5 CHARGE Signal | 7-pt tier: hit_absorption% ≥ 90 AND short_trip% < 70 (and not in 10-pt tier).... | Verify scoring CHARGE signal as 7 pts when hit_absorption% is in [90, 95) and short_trip% < 70 | Functional | Medium | Not Run |
| BATT-033 | Battery Health & Replacement Forecast — §3.5 CHARGE Signal | 4-pt tier: hit_absorption% ≥ 80 (short trip not constrained in spec). PENDING... | Verify scoring CHARGE signal as 4 pts when hit_absorption% is in [80, 90) | Functional | Medium | Not Run |
| BATT-034 | Battery Health & Replacement Forecast — §3.5 CHARGE Signal | 0-pt tier: hit_absorption% < 80. Catches duty cycles too short to reach absor... | Verify scoring CHARGE signal as 0 pts when hit_absorption% is < 80 | Negative | High | Not Run |
| BATT-035 | Battery Health & Replacement Forecast — §3.5 CHARGE Signal — speed filter | Calc 2809220 must only count messages when engine is running AND speed > 5 km... | Verify CHARGE calculator filters out messages when speed is ≤ 5 km/h or engine is off | Functional | Medium | Not Run |
| BATT-036 | Battery Health & Replacement Forecast — §3.5 CHARGE Signal — neutral fa... | NEW v4 coverage: when no trips occur in 30-day window, CHARGE falls back to 5... | Verify scoring CHARGE signal as 5 pts neutral fallback when no trips exist in the 30-day window | Edge Case | Medium | Not Run |
| BATT-037 | Battery Health & Replacement Forecast — §3.5 CHARGE Signal + Fleet Pulse... | NEW v4 coverage: SHORT↓ badge must fire when short-trip% > 70% even if hit_ab... | Verify SHORT↓ badge fires when short_trip% exceeds 70% even when hit_absorption% is ≥ 95 | Edge Case | Medium | Not Run |
| **LATEST SIGNAL (§3.6)** | | | | | | |
| BATT-038 | Battery Health & Replacement Forecast — §3.6 LATEST Signal | LATEST scores 10 pts when the most recent external.powersource.voltage is ≥ 1... | Verify scoring LATEST signal as 10 pts when latest powersource voltage is ≥ 12.50 V | Functional | High | Not Run |
| BATT-039 | Battery Health & Replacement Forecast — §3.6 LATEST Signal | Boundary verification at 12.20 V (7 pts) and 11.90 V (4 pts). Validates two t... | Verify LATEST score boundaries at 12.20 V (7 pts) and 11.90 V (4 pts) | Edge Case | Medium | Not Run |
| BATT-040 | Battery Health & Replacement Forecast — §3.6 LATEST Signal | Critical tier (<11.90 V) scores 0 pts. Vehicle is in immediate trouble at thi... | Verify scoring LATEST signal as 0 pts when latest powersource voltage is < 11.90 V | Negative | High | Not Run |
| BATT-041 | Battery Health & Replacement Forecast — §3.6 LATEST Signal — neutral fa... | NEW v4 coverage: when no telemetry message exists (device offline >24 h or ne... | Verify scoring LATEST signal as 5 pts neutral fallback when no telemetry message exists in last 24 h | Edge Case | Medium | Not Run |
| **FORECAST LOGIC (§4)** | | | | | | |
| BATT-042 | Battery Health & Replacement Forecast — §4 Forecast — Step 1 Base Proj... | Base forecast = (live_voltage − 11.5) / abs(slope_per_day), clamped to 0–90 d... | Verify forecast base projection equals (live_voltage − 11.5) / abs(slope_per_day) clamped to 0–90 days | Functional | High | Not Run |
| BATT-043 | Battery Health & Replacement Forecast — §4 Forecast — Step 1 (flat/posi... | When slope is flat (~0) or positive (stable battery), base is set to the 90-d... | Verify forecast base is set to 90 days when slope is flat (≈0) or positive | Edge Case | High | Not Run |
| BATT-044 | Battery Health & Replacement Forecast — §4 Forecast — Steps 2 & 3 (modi... | Modifiers are multiplied after the redundancy guard de-duplicates correlated... | Verify forecast applies modifier compounding correctly after redundancy guard de-duplicates correlated conditions | Functional | High | Not Run |
| BATT-045 | Battery Health & Replacement Forecast — §4 Forecast — Step 4 (14-day fl... | Minimum forecast = 14 days. Any modifier stack that would push below 14 is cl... | Verify forecast is clamped to 14 days and band is forced to Critical when modifier stack would push below 14 | Edge Case | High | Not Run |
| BATT-046 | Battery Health & Replacement Forecast — §4 Forecast — Replacement override | If calc 2805166 (Battery Replacement) fires within 24 h, the forecast must re... | Verify forecast resets to 90 days when calc 2805166 (Battery Replacement) fires within the last 24 hours | Edge Case | High | Not Run |
| BATT-047 | Battery Health & Replacement Forecast — §2 + §5 End-to-end | Perfect 100 happy path: a healthy fleet vehicle scores all 6 signals at max a... | Verify a healthy vehicle scores 100 points end-to-end and lands in the Excellent band with 90-day forecast | Functional | High | Not Run |
| BATT-048 | Battery Health & Replacement Forecast — §4 Forecast — clamp lower bound | If base computation yields negative (live voltage already below 11.5 V floor)... | Verify forecast base is clamped to zero when live voltage is at or below the 11.5 V floor | Edge Case | Medium | Not Run |
| BATT-049 | Battery Health & Replacement Forecast — §4 Forecast — Deep Discharge mo... | Deep-discharge events ≥ 2 in 30 d apply ×0.7 forecast modifier — battery dama... | Verify forecast applies ×0.7 modifier when calc 2805152 records 2 or more deep-discharge events | Functional | High | Not Run |
| BATT-050 | Battery Health & Replacement Forecast — §4 Forecast — Alternator Failur... | ≥ 1 alternator failure event (calc 2805149) applies ×0.6 modifier — charging... | Verify forecast applies ×0.6 modifier when calc 2805149 records 1 or more alternator-failure events | Functional | High | Not Run |
| BATT-051 | Battery Health & Replacement Forecast — §4 Forecast — CRANK modifier th... | NEW v4 coverage: ×0.5 CRANK forecast modifier must fire at any compensated cr... | Verify CRANK ×0.5 forecast modifier fires when compensated crank_dip is < 9.5 V even at the 13-pt scoring tier | Regression | High | Not Run |
| **HEALTH BANDS (§5)** | | | | | | |
| BATT-052 | Battery Health & Replacement Forecast — §5 Health Bands | Excellent band requires 95–100. Vehicle at 95 = Excellent; vehicle at 94 = Goo... | Verify health band transitions cleanly from Excellent (95 pts) to Good (94 pts) at the 95-point boundary | Edge Case | High | Not Run |
| BATT-053 | Battery Health & Replacement Forecast — §5 Health Bands — most-restrict... | Vehicle lands in most-restrictive band triggered by either score OR forecast.... | Verify band lands at the most-restrictive value when score and forecast disagree | Functional | High | Not Run |
| BATT-054 | Battery Health & Replacement Forecast — §5 Health Bands — Fair | Fair band: score 65–79 OR forecast 30–44 days. | Verify Fair band when score is 72 and forecast is 38 days | Functional | Medium | Not Run |
| BATT-055 | Battery Health & Replacement Forecast — §5 Health Bands — Poor | Poor band: score 50–64 OR forecast <30 days. | Verify Poor band when score is 57 and forecast is 32 days | Functional | Medium | Not Run |
| BATT-056 | Battery Health & Replacement Forecast — §5 Health Bands — Critical | Critical band when score <50 OR forecast <14 days. The hardest fail condition... | Verify Critical band when total score is under 50 | Negative | High | Not Run |
| BATT-057 | Battery Health & Replacement Forecast — §5 Health Bands — forecast over... | NEW v4 coverage: a Good-band score (e.g. 85) combined with a Fair-band foreca... | Verify Good score is downgraded to Fair band when forecast lands in [30, 45) days | Edge Case | High | Not Run |
| **SCORE FORMULA (§2)** | | | | | | |
| BATT-058 | Battery Health & Replacement Forecast — §2 Score Formula | Sum of all signal maxes must equal 100. Guard against rebalancing arithmetic... | Verify the score formula maxes sum to exactly 100 points across all 6 signals in v2.2 | Regression | High | Not Run |
| BATT-059 | Battery Health & Replacement Forecast — §2 Score Formula — v2.1→v2.2 r... | v2.2 introduced CHARGE (+10) and rebalanced REST (35→30), TREND (15→12), DECA... | Verify pipeline applies v2.2 weightings (REST=30, TREND=12, DECAY=13, CHARGE=10) and no longer uses v2.1 weightings | Regression | High | Not Run |
| BATT-060 | Battery Health & Replacement Forecast — §2 Score Formula — MURANO regr... | Real-world regression: MURANO vehicle scored 100/100 under v2.1 but dropped t... | Verify MURANO test vehicle drops from 100 to 90 between v2.1 and v2.2 due to CHARGE signal addition | Regression | High | Not Run |
| **STATUS COLUMN / BADGES** | | | | | | |
| BATT-061 | Fleet Pulse: Status Column Spec — All badge triggers | The renamed Status column must surface 8 badge types: DEEP DISCHARGE, ALTERNA... | Verify all 8 Status column badges (DEEP DISCHARGE, ALTERNATOR, PARK DRAIN, TREND↓, CHARGE↓, SHORT↓, REPLACE, HEALTHY) fire under their documented trigger conditions | Functional | High | Not Run |
| BATT-062 | Fleet Pulse: Status Column Spec — Pill ordering | When multiple badges fire on one row, pills must order by severity: red befor... | Verify multiple Status pills are ordered red, then amber, then green left-to-right on the row | UI | Medium | Not Run |
| BATT-063 | Fleet Pulse: Status Column Spec — Overflow | Maximum 3 visible pills per row; additional pills collapse into '+N more'. Pr... | Verify Status column shows at most 3 pills and renders '+N more' overflow when more pills are active | UI | Medium | Not Run |
| BATT-064 | Fleet Pulse: Status Column Spec — Always one pill | At least one pill must always render. HEALTHY is shown when no other badges f... | Verify HEALTHY pill is shown on rows where no other badges fire so the Status column never renders empty | Functional | Medium | Not Run |
| BATT-065 | Fleet Pulse: Status Column Spec — Plain-English summary line | Each Status state should show a one-line plain-English summary below the pil... | Verify Status column renders the correct plain-English summary line for each of the 9 canonical badge combinations | Functional | Medium | Not Run |
| BATT-066 | Fleet Pulse: Status Column Spec — Column sortability | Status column must sort by worst severity per row (red > amber > green), not... | Verify Status column sorts rows by worst-severity badge first (red > amber > green) | UI | Low | Not Run |
| BATT-067 | Fleet Pulse: Status Column Spec — Mobile narrow column behaviour | On viewports < 600 px, the plain-English summary line must be hidden so badge... | Verify Status column hides the summary line and keeps pills visible on viewports narrower than 600 px | UI | Low | Not Run |
| **HEALTH SCORE TOOLTIP** | | | | | | |
| BATT-068 | Fleet Pulse: Health Score Tooltip Spec — Open/close interactions | Tooltip opens on hover (desktop) and on focus (keyboard). Closes on blur, mou... | Verify Health Score tooltip opens on hover/focus and closes on blur, mouseleave, and Escape | UI | Medium | Not Run |
| BATT-069 | Fleet Pulse: Health Score Tooltip Spec — Sub-signal rows | Tooltip shows 6 rows (one per signal) with friendly labels (e.g. 'Rest voltag... | Verify Health Score tooltip renders 6 sub-signal rows with friendly labels (not raw values or weights) | UI | Medium | Not Run |
| BATT-070 | Fleet Pulse: Health Score Tooltip Spec — Dot colour thresholds | Dot colour rule: ≥80% green, 40–79% amber, <40% red, where % = score / max for... | Verify Health Score tooltip dot colours follow the ≥80% green / 40–79% amber / <40% red rule across all 6 rows | UI | Medium | Not Run |
| BATT-071 | Fleet Pulse: Health Score Tooltip Spec — No raw values / weights | Tooltip is for non-technical operators. Formula weights (e.g. '/30') and raw... | Verify Health Score tooltip displays neither formula weights (e.g. /30) nor raw voltage values | UI | Medium | Not Run |
| BATT-072 | Fleet Pulse: Health Score Tooltip Spec — Band label colour | Band label inside the tooltip is colour-coded per band hex (Excellent #1B873F... | Verify Health Score tooltip band label uses the documented hex colour for each of the 5 bands | UI | Medium | Not Run |
| BATT-073 | Fleet Pulse: Health Score Tooltip Spec — Mobile modal | On viewports < 480 px the tooltip must open as a tap-to-open modal sheet rath... | Verify Health Score tooltip opens as a modal sheet on tap when viewport is narrower than 480 px | UI | Low | Not Run |
| **UI DISPLAY** | | | | | | |
| BATT-074 | Fleet Pulse: Status Column Spec + Fleet Pulse: Health Score Tooltip Spec | All 6 sub-signal rows must fit inside the default tooltip viewport without in... | Verify all 6 sub-signal rows are visible inside the Health Score tooltip without internal scrolling | UI | Medium | Not Run |
| BATT-075 | Battery Health & Replacement Forecast — §4 Forecast display | Forecast must display as relative days (e.g. '47 days') NOT a calendar date.... | Verify forecast is displayed as relative days (e.g. '47 days') not as a calendar date | UI | Medium | Not Run |
| **WEATHERAPI FALLBACK** | | | | | | |
| BATT-076 | Battery Health & Replacement Forecast — §3.2 CRANK Signal (WeatherAPI) | NEW v4 coverage: when the vehicle has no GPS fix at the time of a crank event... | Verify CRANK temperature compensation falls back to the most recent GPS fix within 7 days when current fix is missing | Edge Case | Low | Not Run |
| BATT-077 | Battery Health & Replacement Forecast — §3.2 CRANK Signal (WeatherAPI) | NEW v4 coverage: when no GPS fix exists in the last 7 days either, the pipeli... | Verify CRANK temperature compensation falls back to 25 °C baseline when no GPS fix exists within the last 7 days | Edge Case | Low | Not Run |
