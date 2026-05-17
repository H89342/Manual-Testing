# Battery Health & Replacement Forecast — Full Q&A Session
**Project:** Fleet Pulse by Telemax  
**Source:** Chrome Extension session (saved via pasted context, May 8 2026)  
**Version:** Engineering Briefing v2.2 (28 Apr 2026)

---

## SCORE FORMULA (v2.2)
REST(30) + CRANK(25) + TREND(12) + DECAY(13) + CHARGE(10) + LATEST(10) = 100

---

## THE 6 SIGNALS — COMPLETE SPECIFICATION

### 1. REST Signal — Max 30 pts
**What to test:** Parked battery voltage (ignition off, engine off, no movement).

- **Source:** Calc 2805151 — captures `rest_voltage_avg`
- **How it works:** Records `rest_voltage_avg` for each parked interval. 30-day mean of all values is scored 0–30 pts.
- **Scoring thresholds:**

| 30-day mean rest_voltage_avg | REST Score | Status |
|---|---|---|
| ≥ 12.70 V | 30 pts | ✅ Excellent |
| ≥ 12.50 V | 25 pts | ✅ Good |
| ≥ 12.30 V | 19 pts | 🟡 Fair |
| ≥ 12.00 V | 10 pts | 🟠 Poor |
| < 12.00 V | 0 pts | 🔴 Critical |
| Missing data | 15 pts | ⚪ Neutral fallback |

**Additional roles of REST signal:**
1. **Score** — Converts mean rest voltage into 0–30 pts (primary role)
2. **CRANK fallback** — Fills in CRANK score when no crank data exists: `round(25 × rest_pts / 30)`
3. **Forecast base** — Acts as reference voltage when live voltage is missing: `ref_v = live_v if available else mean_rest`
4. **Forecast modifier** — Triggers ×0.5 penalty on forecast if mean rest < 11.8 V

**What "30-day mean of rest_voltage_avg" means:**  
Each time the vehicle parks (ignition off, engine off, quiet), calc 2805151 opens an interval and measures the average battery voltage during that park. When the engine restarts, it records one `rest_voltage_avg` value for that session. The 30-day mean averages all those values over 30 days. Higher voltage = more charge stored = healthier battery.

**Note on calc 2805151:**  
`2805151` is a Flespi Calculator ID — just a unique number identifying this specific calculator, like an employee ID. It is not a voltage value.

**Score Rebalancing (v2.1 → v2.2):**  
REST was reduced from 35 pts → 30 pts to make room for the new CHARGE signal. This was a deliberate engineering decision, not triggered by any voltage reading.

---

### 2. CRANK Signal — Max 25 pts
**What to test:** Voltage dip during engine cranking (ignition start).

**What "cranking" physically means:**  
Every time you start a car engine, the battery delivers a huge burst of electricity to the starter motor. During this moment, the battery voltage drops sharply. This lowest point is called `crank_dip`. Think of it like squeezing a water bottle — a healthy battery barely collapses under pressure, a weak one collapses a lot.

- **Source:** Calc 2805150 — captures minimum voltage during ignition OFF→ON transitions
- **Key rule:** Uses the MINIMUM `crank_dip` across 30 days (worst start = most honest test)
- **Critical config fix (28 Apr):** Selector must use `min_active=0` with `merge_message_before/after=true` — otherwise 99% of crank events are missed

**Temperature compensation:**

crank_compensated = crank_observed + 0.025 × (25 − ambient_temp_c)

Cold weather makes batteries perform worse — a healthy battery at 6°C may only show 9.6V crank dip vs 10.1V at 25°C. The formula corrects for this so all readings are compared at a standard 25°C baseline.

**Example:** 9.6V crank on a 6°C morning:
- Raw: 9.6V → 13 pts (marginal — would wrongly penalise a healthy battery)  
- Compensated: 9.6 + 0.025 × (25−6) = 9.6 + 0.475 = **10.075V → 25 pts ✅**

**Scoring thresholds (compensated):**

| Min crank_dip (compensated) | CRANK Score | Status |
|---|---|---|
| ≥ 10.0 V | 25 pts | ✅ Strong |
| ≥ 9.5 V | 20 pts | ✅ Good |
| ≥ 9.0 V | 13 pts | 🟡 Marginal |
| ≥ 8.0 V | 6 pts | 🟠 Poor |
| < 8.0 V | 0 pts | 🔴 Critical |
| No crank data | Fallback (see below) | ⚪ |

**REST Fallback for CRANK:**  
When a vehicle has no crank events in 30 days (e.g. parked in warehouse, owner on holiday), the CRANK signal has no data. The system uses REST score proportionally:

CRANK fallback = round(25 × rest_pts / 30)
| Situation | REST score | CRANK fallback |
|---|---|---|
| Very healthy (12.70V+) | 30/30 | round(25×30/30) = **25/25** |
| Good (12.55V) | 25/30 | round(25×25/30) = **21/25** |
| Weak (12.10V) | 10/30 | round(25×10/30) = **8/25** |
| Critical (<12.0V) | 0/30 | round(25×0/30) = **0/25** |

**Why this makes sense:** REST and CRANK both measure the same underlying battery from different angles. A battery that rests at 12.70V almost always cranks strongly too. A battery resting at 11.8V will almost certainly show a weak crank.

---

### 3. TREND Signal — Max 12 pts
**What to test:** Linear regression slope of rest voltage over 30 days.

- **Source:** Same `rest_voltage_avg` data as REST, but regression analysis
- **Critical bug fix (v2.0 → v2.2):** The x-axis for regression must use `(interval_begin + interval_end) / 2`, NOT the calc timestamp (v2.0 had this wrong, was masking BMW's instability)
- **Scoring thresholds:**

| Slope (V/day) | TREND Score |
|---|---|
| ≥ −0.003 V/day | 12 pts ✅ |
| ≥ −0.008 V/day | 9 pts |
| ≥ −0.015 V/day | 5 pts |
| worse than −0.015 | 0 pts 🔴 |

*(Was 15 pts in v2.1; reduced to 12 pts in v2.2 to make room for CHARGE)*

---

### 4. DECAY Signal — Max 13 pts
**What to test:** How fast the battery loses voltage while parked over multi-hour periods.

- **Source:** Calc 2805232 — parks ≥4 hours, ignition & movement both off
- **Two required data cleanups:**
  - (a) Drop parks shorter than **6 hours**
  - (b) Drop parks where start voltage exceeds **13.5V** (alternator tail not yet decayed)
- **Slope formula:** `(start − end) / duration`, clamped to ≥0 (negative = surface charge artefact, not real recovery)
- **Config note:** `merge_message_before/after = false` so alternator voltage doesn't contaminate park start/end values

**Scoring thresholds:**

| DECAY slope (V/hr) | Score |
|---|---|
| ≤ 0.003 V/hr | 13 pts ✅ |
| ≤ 0.006 V/hr | 10 pts |
| ≤ 0.010 V/hr | 7 pts |
| ≤ 0.015 V/hr | 3 pts |
| > 0.015 V/hr | 0 pts 🔴 |

**Why it matters:** DECAY catches accelerating self-discharge weeks before TREND can.

*(Was 15 pts in v2.1; reduced to 13 pts in v2.2 to make room for CHARGE)*

---

### 5. CHARGE Signal (v2.2 NEW) — Max 10 pts
**What to test:** Charge-cycle quality — whether trips are long enough to reach absorption voltage.

- **Source:** Calc 2809220 (Charge Behaviour Tracker) — fires while engine running and speed >5 km/h
- **Measures:** `hit_absorption` flag (1 if peak voltage ≥13.8V), short-trip fraction (<15 min trips)

**Scoring thresholds:**

| Condition | Score |
|---|---|
| abs ≥95% AND short <50% | 10 pts ✅ |
| abs ≥90% AND short <70% | 7 pts |
| abs ≥80% | 4 pts |
| abs <80% | 0 pts 🔴 |

**Key insight:** Catches the "battery is fine but duty cycle is hostile" failure mode (e.g. MURANO only hits absorption on 72% of trips — score dropped from 100 → 90 when CHARGE was added in v2.2).

---

### 6. LATEST Signal — Max 10 pts
**What to test:** Most recent live voltage reading.

- **Source:** `external.powersource.voltage` from the latest telemetry message

**Scoring thresholds:**

| Latest voltage | Score |
|---|---|
| ≥ 12.50 V | 10 pts ✅ |
| ≥ 12.20 V | 7 pts |
| ≥ 11.90 V | 4 pts |
| < 11.90 V | 0 pts 🔴 |

---

## ALL 8 CALCULATOR IDs

| Calc ID | Name | What it measures |
|---|---|---|
| 2805151 | Rest Voltage | Battery voltage while parked (REST signal) |
| 2805150 | Crank Events | Voltage dip during engine start (CRANK signal) |
| 2805119 | Daily Voltage Monitor | Daily average of all voltage readings |
| 2805152 | Deep Discharge | Fires when voltage drops below 11.5V |
| 2805149 | Alternator Failure | Engine running but voltage stuck below 13.0V |
| 2805166 | Battery Replacement | Detects battery swap |
| 2805232 | Parked Voltage Decay | Measures voltage drop during long parks (DECAY signal) |
| 2809220 | Charge Behaviour Tracker | Detects charging quality per trip (CHARGE signal — v2.2 NEW) |

---

## FORECAST LOGIC — 4 STEPS

### Step 1 — Base Projection

base = (live_voltage − 11.5V) / abs(slope_per_day)
base = clamped to 0–90 days

If slope is flat or positive (stable battery) → base = 90 days.

### Step 2 — Apply Degradation Modifiers

| Trigger | Multiplier | Meaning |
|---|---|---|
| Min crank < 9.5V | ×0.5 | High internal resistance under load |
| Deep discharges ≥ 2 events | ×0.7 | Battery damaged by being run flat |
| Alternator failures ≥ 1 | ×0.6 | Charging system unreliable |
| Mean rest voltage < 11.8V | ×0.5 | Consistently low state of charge |
| DECAY band = bad (>0.015 V/hr) | ×0.7 | High self-discharge between drives |

### Step 3 — Redundancy Guard + Compounding
Correlated conditions are de-duplicated before multiplying (e.g. low rest voltage + deep discharges usually describe the same battery — only the harsher ×0.5 counts).  
Worst-case combined multiplier after guard: 0.5 × 0.5 × 0.7 = **0.175** (17.5% of base).

### Step 4 — Floor & Override Rules
- **Minimum forecast = 14 days** — anything lower is clamped to 14 and band forces to Critical
- **Replacement override:** If calc 2805166 fires within 24 hours → forecast immediately resets to 90 days

---

## HEALTH BANDS

| Band | Score Range | Forecast Requirement |
|---|---|---|
| 🟢 Excellent | 95–100 | Any |
| 🟢 Good | 80–94 | ≥45 days |
| 🟡 Fair | 65–79 | OR 30–44 days |
| 🟠 Poor | 50–64 | OR <30 days |
| 🔴 Critical | <50 | OR <14 days |

A vehicle always lands in the **most restrictive** band triggered by either score or forecast.

---

## SCORE REBALANCING SUMMARY (v2.1 → v2.2)

| Signal | v2.1 | v2.2 | Change |
|---|---|---|---|
| REST | 35 pts | 30 pts | −5 |
| CRANK | 25 pts | 25 pts | no change |
| TREND | 15 pts | 12 pts | −3 |
| DECAY | 15 pts | 13 pts | −2 |
| CHARGE | — | 10 pts | **NEW** |
| LATEST | 10 pts | 10 pts | no change |
| **Total** | **100** | **100** | balanced ✅ |

*Rebalancing was a deliberate engineering decision — NOT triggered by any voltage reading.*

---

## TEST CASES PROGRESS

- **Version:** v3 (54 TCs, 5 sheets)
- **File:** testcases_battery_health_v3.xlsx
- **Google Sheets:** https://docs.google.com/spreadsheets/d/1XCixbzWl2XL8sH0F8HKjTG70mkzUHa02/edit

### Test Case Groups (54 TCs total):

| Group | TCs | Signal/Topic |
|---|---|---|
| BATT-001 to 003 | 3 | REST Signal |
| BATT-004 to 007 | 4 | CRANK Signal |
| BATT-008 to 009 | 2 | TREND Signal |
| BATT-010 to 012 | 3 | DECAY Signal |
| BATT-013 to 016 | 4 | CHARGE Signal |
| BATT-017 to 018 | 2 | LATEST Signal |
| BATT-019 to 024 | 6 | Forecast Logic |
| BATT-025 to 030 | 6 | Band Display & Badges |
| BATT-031 to 042 | 12 | Fleet Pulse Status Column Spec |
| BATT-043 to 054 | 12 | Health Score Tooltip Spec |

### Open CQ Items (7 total):

| CQ # | Issue |
|---|---|
| CQ-001 | CHARGE score vs badge threshold (< 90% vs < 80%) |
| CQ-002 | SHORT interaction with 4-pt CHARGE scoring tier |
| CQ-003 | 14-day floor test data availability |
| CQ-004 | 40% boundary value (amber vs red dot in tooltip) |
| CQ-005 | Column header confirmation (Status vs Active Alerts vs Health Flags) |
| CQ-006 | +N more overflow interaction type |
| CQ-007 | EV CHARGE badge suppression question |

---

## SOURCE DOCUMENTS

1. **Battery Health & Replacement Forecast** (Engineering Briefing v2.2):  
   https://flepsi-batteryhealth-replacement.netlify.app/
2. **Fleet Pulse: Renaming "AI Diagnosis" → "Status"** (Status Column Spec):  
   https://cosmic-brioche-eccf27.netlify.app/
3. **Fleet Pulse: Health Score Tooltip Spec:**  
   https://eclectic-cassata-b60697.netlify.app/
4. **Test Case Rules (GitHub):**  
   https://github.com/H89342/Manual-Testing/tree/main/Manual%20Test%20Cases%20Rules/TestCases%20_Battery%20Prediction

---

## TEST CASE RULES (KEY POINTS)

- **13 mandatory columns:** TC ID | Title | Screen/Section | Preconditions | Steps | Expected Result | Test Data | Postconditions | Status | Priority | Type | Environment | Notes
- **TC ID format:** BATT-NNN (3 digits zero-padded)
- **Title:** Must start with "Verify" followed by action verb in -ing form
- **Screen/Section:** Must use EXACT document name + section reference (e.g. "Battery Health & Replacement Forecast — §3.1 The Score (REST Signal)")
- **Orange (#FFC000)** highlighting for PENDING rows with Open CQ items
- **Status:** "Not Run" by default
- **Priority:** At least 30% of TCs must be High
- **CQ sheet:** Always included in Excel export

---

## GOOGLE DRIVE

- **Folder:** https://drive.google.com/drive/folders/12hExo-h2Jm8nqOKCoC-C4-B_sYbTok6E
- **Account:** hanna.lee@telemax.com.au

---

## AI ACCURACY ANALYSIS (Honest Breakdown)

| Your Understanding Level | Effective AI Accuracy | What You Can Do |
|---|---|---|
| 0% — just copy-paste AI output | ~8–15% end-to-end | Cannot catch AI errors |
| 30% — read summary, understand 6 signals | ~40–55% | Can spot obvious wrong expected values |
| 60% — understand score formula + forecast | ~70–80% | Can guide AI, validate edge cases |
| 80%+ — understand spec deeply | ~85–90% | AI is a productivity tool, not a risk |

**Core risk:** AI being "confidently almost-right" — correct formula but wrong threshold boundary.

**Combined end-to-end reliability (AI alone, no human judgment):**  
~85% × 70% × 30% × 45% ≈ **~8%**

**Recommended minimum investment before relying on AI:** ~half a day reading §3.1 (score formula), §3.2 (DECAY signal), and §3.4 (forecast modifiers) — enough for ~60% understanding.

---

## TESTING TIME ESTIMATES

| | Without AI | With AI |
|---|---|---|
| Total hours | ~61.5 hrs | ~25 hrs |
| Working days | ~8 days | ~3 days |
| Time saving | — | ~60% (~36.5 hrs saved) |

*The 3-day AI estimate assumes ~60% understanding of the spec.*

---

## PENDING ITEMS (v2.2 Backlog — Not Yet Implemented)

- DECAY temperature compensation (Arrhenius formula: `decay_normalized = decay_observed / 1.08^(temp_c − 25)`)
- Crank Recovery ratio (counter exists in calc but not yet scored)
- EV-specific re-weighting for vehicles like SEAL 627KB5
- Forecast uncertainty intervals (e.g. "63d ± range")