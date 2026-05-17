---
status: Draft
version: v1
date: 2026-05-17
author: Hanna Lee (hanna.lee@telemax.com.au)
---

# Requirement Analysis — Battery Prediction (Fleet Pulse by Telemax)

> Step 1 of the SDET workflow. Sources: `req-battery prediction_v1.md` (links) and `red-Battery Study_v1.md` (Engineering Briefing v2.2, 28 Apr 2026). TC type in scope: **Functional**; Environment: **Web**.

---

## 1. Source & Reference

| Field | Value |
|---|---|
| Feature / Story ID | Battery Health & Replacement Forecast — Engineering Briefing v2.2 |
| Source document(s) | 1) `red-Battery Study_v1.md` (full spec) · 2) Netlify: https://flepsi-batteryhealth-replacement.netlify.app/ · 3) Status Column Spec: https://cosmic-brioche-eccf27.netlify.app/ · 4) Health Score Tooltip Spec: https://eclectic-cassata-b60697.netlify.app/ |
| Provided by | Engineering (briefing v2.2, 28 Apr 2026) |
| Date received | 2026-05-08 (via Chrome Extension session) |
| Target release / sprint | v2.2 GA (rolling out replacing v2.0/v2.1) |

---

## 2. Feature Summary (plain English)

**What is being built**
A scoring + forecast system for vehicle batteries on the **Fleet Pulse** dashboard. It combines **6 Flespi-derived signals** (REST, CRANK, TREND, DECAY, CHARGE, LATEST) into a single **0–100 Health Score**, then computes a **0–90 day replacement forecast** with up to 5 degradation modifiers, a redundancy guard, a 14-day floor, and a battery-replacement override. The score and forecast feed a **5-tier Health Band**, a **Status pill column** (8 badge types), and a **Health Score Tooltip** (6 sub-signal rows, friendly labels only).

**Why it is being built (business goal)**
Predict battery failure **before** unplanned roadside breakdowns. Move fleet maintenance from reactive to proactive, reduce vehicle downtime, and surface duty-cycle problems (e.g. short-trip vehicles) that look healthy by voltage alone. v2.2 specifically adds the CHARGE signal to catch "battery is fine but duty cycle is hostile" failures (MURANO real-world example: 100→90).

**Primary users**
Fleet operators, maintenance supervisors, and dispatchers using the Fleet Pulse web dashboard. Secondary: vehicle owners on mobile responsive view.

**Does this change affect existing features or workflows?**
**Yes.** The legacy **"AI Diagnosis"** dashboard column is renamed to **"Status"** (or one of two alternatives — see CQ-005). The Health Score chip is new, and its tooltip replaces older raw-voltage popups. v2.1 weightings (REST 35 / TREND 15 / DECAY 15 / CHARGE 0) are replaced by v2.2 (30 / 12 / 13 / 10). Historic scores for the same vehicle will shift — see BATT-060 MURANO regression.

---

## 3. Requirement Type Classification

Check all that apply:

- [x] **Functional** — signal scoring, forecast calc, band assignment, override rules
- [x] **Integration** — 8 Flespi calculator IDs, WeatherAPI ambient temperature, score_history persistence
- [x] **UI/UX** — Status pills (ordering, overflow, mobile breakpoints), Health Score Tooltip, dashboard column
- [x] **Non-functional** — refresh cadence, accessibility (keyboard focus on tooltip, WCAG), mobile responsive (<480 px modal, <600 px summary hide)
- [ ] API/Contract — no public API contract in this requirement (internal Flespi calcs only)

> **TC type requested by user:** Functional only. Note this leaves out UI-only and integration-only TCs (BATT-062…BATT-067, BATT-068…BATT-073, BATT-074, BATT-076, BATT-077) unless the user expands scope. Confirmation needed — flagged as CQ in Step 2.

---

## 4. In Scope vs Out of Scope

| In Scope (this cycle) | Out of Scope |
|---|---|
| 6 signal scoring tiers + neutral fallbacks (REST/CRANK/TREND/DECAY/CHARGE/LATEST) | DECAY temperature compensation (Arrhenius) — backlog |
| Forecast base formula, modifier stack, redundancy guard, 14-day floor, replacement override | Crank Recovery ratio — counter exists but not yet scored |
| Health Bands (5 tiers) + most-restrictive rule + Good→Fair downgrade | EV-specific re-weighting (SEAL 627KB5) — backlog |
| CRANK temperature compensation at 25 °C baseline + WeatherAPI fallback chain | Forecast uncertainty intervals — backlog |
| Status Column badge logic (functional triggers) | Pre-v2.2 historical score migration policy |
| Health Score Tooltip data (friendly labels, dot colours) | Postman / API contract testing (no public API) |
| Score formula sum = 100 + v2.1→v2.2 regression (MURANO) | Mobile native app (only mobile-responsive web in scope) |
| Calc 2805150 config regression (min_active=0, merge_message) | Push-notification or email alerts for Critical band |

---

## 5. Key Screens / Flows / Sections Referenced

| Reference | Type | Location / Link |
|---|---|---|
| §2 Score Formula | BRD section | red-Battery Study_v1.md L7–9 |
| §3.1 REST Signal | BRD section | red-Battery Study_v1.md L15–45 |
| §3.2 CRANK Signal | BRD section | red-Battery Study_v1.md L48–91 |
| §3.3 TREND Signal | BRD section | red-Battery Study_v1.md L94–109 |
| §3.4 DECAY Signal | BRD section | red-Battery Study_v1.md L112–135 |
| §3.5 CHARGE Signal | BRD section | red-Battery Study_v1.md L138–154 |
| §3.6 LATEST Signal | BRD section | red-Battery Study_v1.md L157–170 |
| §4 Forecast Logic (4 steps) | BRD section | red-Battery Study_v1.md L188–215 |
| §5 Health Bands | BRD section | red-Battery Study_v1.md L218–228 |
| Calculator IDs table | BRD section | red-Battery Study_v1.md L173–185 |
| Status Column Spec | UI spec | https://cosmic-brioche-eccf27.netlify.app/ |
| Health Score Tooltip Spec | UI spec | https://eclectic-cassata-b60697.netlify.app/ |
| Battery Briefing landing | UI/BRD | https://flepsi-batteryhealth-replacement.netlify.app/ |

---

## 6. Acceptance Criteria — Extracted from Source

| # | Acceptance Criterion (paraphrased) | Source location |
|---|---|---|
| AC-01 | Health Score = REST + CRANK + TREND + DECAY + CHARGE + LATEST, max 100, weights 30/25/12/13/10/10 | §2 |
| AC-02 | REST scores 30/25/19/10/0 across 5 voltage tiers; missing → 15 pts neutral | §3.1 |
| AC-03 | REST acts as forecast reference voltage when live voltage missing | §3.1 |
| AC-04 | REST <11.8 V triggers ×0.5 forecast modifier | §3.1 |
| AC-05 | CRANK scores 25/20/13/6/0 across 5 tiers using **compensated** crank_dip | §3.2 |
| AC-06 | Temp compensation: crank_comp = crank_obs + 0.025 × (25 − ambient °C) | §3.2 |
| AC-07 | Calc 2805150 selector requires `min_active=0` + `merge_message_before/after=true` | §3.2 |
| AC-08 | When no crank events, CRANK = round(25 × REST/30) | §3.2 |
| AC-09 | CRANK <9.5 V (compensated) triggers ×0.5 forecast modifier | §3.2 + §4 |
| AC-10 | TREND scores 12/9/5/0 by 30-day rest-voltage regression slope | §3.3 |
| AC-11 | TREND regression x-axis = (interval_begin + interval_end)/2, NOT calc timestamp | §3.3 |
| AC-12 | DECAY scores 13/10/7/3/0 by parked decay slope V/hr | §3.4 |
| AC-13 | DECAY drops parks <6 h and parks with start voltage >13.5 V | §3.4 |
| AC-14 | DECAY slope clamped to ≥0 (surface-charge artefacts not allowed) | §3.4 |
| AC-15 | DECAY >0.015 V/hr triggers ×0.7 forecast modifier | §3.4 + §4 |
| AC-16 | CHARGE (v2.2 NEW) scores 10/7/4/0 by hit_absorption% + short_trip% | §3.5 |
| AC-17 | CHARGE calc only counts engine.on=true AND speed>5 km/h | §3.5 |
| AC-18 | LATEST scores 10/7/4/0 by latest powersource voltage | §3.6 |
| AC-19 | Forecast base = (live_v − 11.5) / abs(slope_per_day), clamped 0–90 d | §4 step 1 |
| AC-20 | Flat or positive slope → base = 90 days | §4 step 1 |
| AC-21 | 5 modifiers (×0.5, ×0.7, ×0.6, ×0.5, ×0.7) — see §4 step 2 | §4 step 2 |
| AC-22 | Redundancy guard: correlated modifiers de-duplicated (keep harsher) | §4 step 3 |
| AC-23 | Worst combined multiplier = 0.5×0.5×0.7 = 0.175 | §4 step 3 |
| AC-24 | Forecast minimum = 14 days; below → clamp to 14 AND force band=Critical | §4 step 4 |
| AC-25 | Calc 2805166 firing within 24 h → forecast resets to 90 days | §4 step 4 |
| AC-26 | 5 bands (Excellent/Good/Fair/Poor/Critical) at score 95+/80+/65+/50+/<50 | §5 |
| AC-27 | Band lands at most-restrictive triggered by score OR forecast | §5 |

---

## 7. Requirement → Testable Condition Mapping (Traceability)

| Req ID | Testable Condition | Priority | Type | Traceability anchor |
|---|---|---|---|---|
| REQ-3.1.a | REST scores correctly across 5 tiers + neutral fallback (incl. 10-pt tier 12.00–12.29 V) | High | Functional | red-Battery Study §3.1 — voltage tier table |
| REQ-3.1.b | REST forecast reference voltage fallback when live voltage absent | Medium | Functional | red-Battery Study §3.1 "ref_v = live_v if available else mean_rest" |
| REQ-3.1.c | REST <11.8 V triggers forecast ×0.5 modifier | High | Functional | red-Battery Study §3.1 "Forecast modifier" |
| REQ-3.2.a | CRANK scores correctly across 5 tiers using compensated values (incl. 13-pt tier 9.0–9.49 V) | High | Functional | red-Battery Study §3.2 — compensated thresholds table |
| REQ-3.2.b | CRANK temp compensation formula correct at cold-morning and 25 °C baseline | High | Functional | red-Battery Study §3.2 "crank_compensated = …" |
| REQ-3.2.c | Calc 2805150 config: min_active=0 + merge_message_before/after=true | High | Functional / Regression | red-Battery Study §3.2 "Critical config fix (28 Apr)" |
| REQ-3.2.d | CRANK falls back to round(25 × REST/30) when no events | Medium | Functional | red-Battery Study §3.2 "REST Fallback for CRANK" |
| REQ-3.2.e | CRANK <9.5 V triggers ×0.5 forecast modifier (independent of 0-pt threshold) | High | Functional | red-Battery Study §3.2 + §4 |
| REQ-3.3.a | TREND scores correctly across 4 tiers (incl. 5-pt tier −0.015…−0.008 V/day) | High | Functional | red-Battery Study §3.3 — slope table |
| REQ-3.3.b | TREND regression uses interval midpoint, NOT calc timestamp | High | Functional / Regression | red-Battery Study §3.3 "Critical bug fix (v2.0→v2.2)" |
| REQ-3.3.c | TREND neutral fallback when insufficient samples | Medium | Functional | red-Battery Study §3.3 (implied; threshold value is a CQ) |
| REQ-3.4.a | DECAY scores correctly across 5 tiers (incl. 7-pt tier 0.006–0.010 V/hr) | High | Functional | red-Battery Study §3.4 — slope table |
| REQ-3.4.b | DECAY drops parks <6 h and start voltage >13.5 V | High | Functional | red-Battery Study §3.4 "Two required data cleanups" |
| REQ-3.4.c | DECAY slope clamped to ≥0 | Medium | Functional | red-Battery Study §3.4 "clamped to ≥0" |
| REQ-3.4.d | DECAY neutral fallback when no qualifying parks | Medium | Functional | red-Battery Study §3.4 (implied) |
| REQ-3.4.e | DECAY >0.015 V/hr triggers ×0.7 forecast modifier | High | Functional | red-Battery Study §3.4 + §4 |
| REQ-3.5.a | CHARGE scores correctly across 4 tiers (10/7/4/0) | High | Functional | red-Battery Study §3.5 |
| REQ-3.5.b | CHARGE speed/engine filter applied (speed >5 km/h + engine on) | Medium | Functional | red-Battery Study §3.5 — calc 2809220 |
| REQ-3.5.c | CHARGE neutral fallback when no trips in window | Medium | Functional | red-Battery Study §3.5 (implied) |
| REQ-3.6.a | LATEST scores correctly across 4 tiers | High | Functional | red-Battery Study §3.6 |
| REQ-3.6.b | LATEST neutral fallback when no telemetry in last 24 h (threshold is a CQ) | Medium | Functional | red-Battery Study §3.6 (implied) |
| REQ-4.a | Forecast base formula + clamp to [0, 90] | High | Functional | red-Battery Study §4 step 1 |
| REQ-4.b | Flat or positive slope → base = 90 | High | Functional | red-Battery Study §4 step 1 |
| REQ-4.c | All 5 modifiers fire correctly under their triggers | High | Functional | red-Battery Study §4 step 2 |
| REQ-4.d | Redundancy guard de-duplicates correlated modifiers | High | Functional | red-Battery Study §4 step 3 |
| REQ-4.e | 14-day floor + band override to Critical | High | Functional | red-Battery Study §4 step 4 |
| REQ-4.f | Battery replacement override (calc 2805166 within 24 h → 90 d) | High | Functional | red-Battery Study §4 step 4 |
| REQ-4.g | Negative base clamps to 0 (live voltage at/below 11.5 V floor) | Medium | Functional | red-Battery Study §4 step 1 (clamp) |
| REQ-5.a | All 5 band boundaries respected (95/94, 80/79, 65/64, 50/49) | High | Functional | red-Battery Study §5 |
| REQ-5.b | Most-restrictive rule (band driven by worse of score or forecast) | High | Functional | red-Battery Study §5 |
| REQ-5.c | Good score downgraded to Fair when forecast 30–44 d | High | Functional | red-Battery Study §5 (review §4.5) |
| REQ-2.a | Score weights sum to exactly 100 in v2.2 | High | Functional / Regression | red-Battery Study §2 + §rebalancing summary |
| REQ-2.b | v2.2 weights enforced; v2.1 weights eliminated | High | Functional / Regression | red-Battery Study §rebalancing summary |
| REQ-2.c | MURANO real-world regression (100 → 90) | High | Functional / Regression | red-Battery Study §3.5 "Key insight" |

> **Out-of-this-cycle** mappings (UI/Tooltip/Status/WeatherAPI) are tracked in the spec but excluded because the user requested **Functional + Web** only this cycle.

---

## 8. Testability Issues (flag for Q&A)

| # | Issue | Severity | Q to raise |
|---|---|---|---|
| T-01 | Refresh / recalc cadence not stated — assumed 15 min in v3 TCs | High | How often does the pipeline recalculate scores? |
| T-02 | TREND minimum sample threshold for regression not stated | High | What is the minimum sample count below which TREND falls back to 6 pts neutral? |
| T-03 | LATEST stale-data threshold not stated | High | At what message age does LATEST fall back to 5 pts neutral? |
| T-04 | CHARGE neutral fallback threshold (trips in window) not stated | High | At what trip count does CHARGE fall back to 5 pts neutral? 0? <5? |
| T-05 | DECAY neutral fallback threshold (qualifying parks) not stated | Medium | At what qualifying-park count does DECAY fall back to 7 pts? |
| T-06 | Rounding rule for CRANK fallback formula (round vs floor vs banker's) | Medium | Standard half-up rounding? |
| T-07 | Inclusivity at REST 12.00 V boundary (≥ vs >) explicit table reads ≥ everywhere | Medium | Confirm "≥12.00 V → 10 pts" is the actual code rule |
| T-08 | Forecast modifier order before/after redundancy guard | Medium | Which correlated pairs are dedupe pairs? Only rest+deep? Or others? |
| T-09 | Band downgrade direction — never upgrade band even if score better than forecast band | Medium | Confirm: most-restrictive only ever downgrades, never upgrades |
| T-10 | Replacement event window timezone — 24 h from event timestamp or calendar day? | Medium | Define 24 h precisely |
| T-11 | Cold-weather edge: very hot ambient (e.g. 45 °C) — formula goes negative comp; clamped? | Low | Is compensation clamped at hot end too? |
| T-12 | WeatherAPI dependency missing-fix fallback policy not in spec (assumed 25 °C) | Medium | Confirm fallback to 25 °C baseline when no fix within 7 days |
| T-13 | Pending v2.2 backlog items — confirm out of scope for this test cycle | Medium | Confirm |
| T-14 | TC type scope — user requested Functional only; Status & Tooltip UI cases excluded | High | Confirm Functional-only scope this cycle |
| T-15 | Environment restricted to Web — mobile responsive cases excluded | Medium | Confirm Web-only this cycle |

---

## 9. Risk Assessment

### High risk
- **Forecast modifier compounding + redundancy guard** — multiplication of up to 5 modifiers with de-duplication has many paths; misfires cause silent forecast inflation/deflation that goes undetected until field failures.
- **REST/CRANK fallback semantics** — proportional rounding, the dual ×0.5 trigger thresholds (REST <11.8 vs CRANK <9.5) are easy to swap or off-by-one.
- **TREND regression x-axis** — v2.0 had this wrong; without explicit regression coverage it can silently revert and mask BMW-class instabilities (cited in spec).
- **Calc 2805150 config** — `min_active=0` + `merge_message_before/after=true` causing 99% miss when wrong. Operationally fragile.
- **14-day floor + Critical override** — score band must be overridden even when score says Fair; ordering of band assignment vs forecast clamp is critical.
- **WeatherAPI dependency** — compensation factor of 0.475 V at cold ambient is the difference between Strong CRANK and Marginal; if temperature is missing or wrong, healthy batteries fail and weak batteries pass.

### Medium risk
- **Score boundary inclusivity** — `≥` vs `>` at every tier (REST, CRANK, TREND, DECAY, CHARGE, LATEST) — 12 separate boundaries.
- **DECAY data cleanup ordering** — drop-short and drop-high-voltage must both apply before slope; ordering can change qualifying set.
- **Replacement override race** — calc 2805166 firing while modifier stack is being computed.
- **Band downgrade** — Good + 40 d forecast → Fair (review §4.5 gap).

### Low risk
- **Forecast display format** ("47 days" vs date) — cosmetic.
- **Score history version stamp** — `v2.2` label.
- **Calc 2805166 audit log copy** — wording only.

---

## 10. Initial Observations & Open Risks

| # | Observation | Risk level | Action needed |
|---|---|---|---|
| 1 | v3 TC set has tier gaps the review (`Review Battery Prediction Test case.md`) already identified — v4 must close them | High | Confirmed; covered in mapping above |
| 2 | 7 open clarification items already on record (CQ-001…CQ-007) | High | Carry forward into Step 2 Q&A |
| 3 | TC type scope is Functional only this cycle — risk of UI regression slipping through | High | Raise as CQ-Scope-01 |
| 4 | Engineering acceptance is across 8 calculator IDs — coordination risk | Medium | Confirm calc owners + access in Q&A |
| 5 | v2.1→v2.2 historic data regression — fleet vehicles will see score drops | Medium | Confirm migration / communication plan |

---

## Next Step

→ Proceed to **Step 2** (`qa-battery-prediction_v1.md`) — generate CRITICAL / IMPORTANT / NICE TO HAVE questions. **PAUSE** for user answers before writing test cases.
