---
status: OPEN
version: v1
date: 2026-05-17
author: Hanna Lee (hanna.lee@telemax.com.au)
---

# Q&A Checklist — Battery Prediction (Fleet Pulse by Telemax)

> Step 2 of the SDET workflow. Sourced from `analysis-battery-prediction_v1.md` §8 (testability issues) and the 7 carry-over CQs from v3 review.
>
> **Rule:** all **CRITICAL** items must be resolved before Step 3 (writing test cases). IMPORTANT items affect test design; NICE TO HAVE items refine edges.

---

## Status Snapshot

| Bucket | Count | Must resolve before TC writing? |
|---|---|---|
| CRITICAL | 9 | **Yes** — Step 3 is blocked until each is answered |
| IMPORTANT | 8 | Influences test data + edge coverage |
| NICE TO HAVE | 5 | Will be assumed if unanswered |

---

## CRITICAL Questions

### Q1. Functional-vs-UI scope confirmation for this cycle
- **Question:** The request specifies **TC Type = Functional** and **Environment = Web**. Should I exclude Status Column pill UI cases, Health Score Tooltip UI cases, mobile-responsive cases, and WeatherAPI-fallback edge cases from v4? Or should "Functional" be read broadly to include the functional triggers behind the pills (e.g. "DEEP DISCHARGE badge fires when ≥2 deep-discharge events" — even though the pill is UI)?
- **Ask:** PO + QA Lead
- **Ref:** User request header + spec §3.1–§5 (Status & Tooltip)
- **Why it matters:** Determines whether v4 has ~35 functional-only TCs or the full ~77. Major scope swing.

### Q2. Score pipeline recalculation cadence
- **Question:** How often does the pipeline recompute the Health Score, Forecast, and Band for a given vehicle? Once per minute? Every 15 minutes? On every new message?
- **Ask:** Backend / Pipeline owner
- **Ref:** Not stated in `red-Battery Study_v1.md`
- **Why it matters:** Every functional TC needs to know when to expect the score update to land. Without this we can't define a deterministic step "wait N minutes, then read tooltip".

### Q3. TREND minimum sample threshold for neutral fallback
- **Question:** What is the minimum number of `rest_voltage_avg` samples below which TREND skips regression and returns the 6-pt neutral fallback? v3 review implied <10; spec doesn't state.
- **Ask:** Backend
- **Ref:** §3.3 (implied)
- **Why it matters:** Without the threshold I can't seed precise test data for the boundary or the neutral case.

### Q4. LATEST stale-data threshold
- **Question:** At what age of the most recent telemetry message does LATEST fall back to 5-pt neutral? 24 h? 48 h? Configurable?
- **Ask:** Backend
- **Ref:** §3.6 (implied)
- **Why it matters:** Without this I can't write the LATEST neutral-fallback TC or the boundary just before fallback.

### Q5. CHARGE neutral fallback trip threshold
- **Question:** At what number of trips in the 30-day window does CHARGE fall back to 5-pt neutral? 0? <3? <5?
- **Ask:** Backend
- **Ref:** §3.5 (implied)
- **Why it matters:** Same as Q3/Q4 — boundary data needed.

### Q6. Forecast — 14-day floor staging data availability
- **Question:** Can the test team be provided with a sandbox vehicle / seeded data where `(slope, modifiers)` produce a base forecast below 14 days **before** clamp? Or do I need to construct one via direct DB writes?
- **Ask:** QA Lead + Backend
- **Ref:** §4 step 4 (this is also carry-over **CQ-003** from v3)
- **Why it matters:** Without this data the floor + Critical-override TC cannot be deterministically executed.

### Q7. CHARGE↓ badge numeric threshold
- **Question:** The CHARGE↓ badge in the Status Column Spec triggers when "absorption is low" with no numeric cut-off. Does it fire at absorption <90 % (matching the 7-pt scoring tier), or only at <80 % (matching the 0-pt tier)?
- **Ask:** PO + Designer
- **Ref:** Status Column Spec (carry-over **CQ-001**)
- **Why it matters:** Even if pill rendering is out of scope (see Q1), this also affects functional decision boundaries downstream.

### Q8. CRANK ×0.5 forecast modifier threshold (verify independent of scoring)
- **Question:** Confirm: the CRANK ×0.5 forecast modifier fires at **any** compensated crank_dip <9.5 V, even when the scoring tier is 13 pts (9.0–9.49 V). i.e. modifier threshold (9.5) is independent of the 0-pt threshold (8.0). The spec implies this but a sanity check is required because v3 only tested it at the 0-pt threshold.
- **Ask:** Backend / Pipeline owner
- **Ref:** §3.2 + §4 step 2 (review §4.3 gap)
- **Why it matters:** Determines whether the modifier ever fires above the 0-pt CRANK score. Risk of silent forecast inflation if wrong.

### Q9. Redundancy-guard correlated pairs
- **Question:** §4 step 3 says "correlated conditions are de-duplicated" and gives `rest<11.8 + deep_discharge` as the example. Are there **other** dedupe pairs (e.g. alternator + crank, decay + rest)? If yes, list them in priority order.
- **Ask:** Backend / Algorithm owner
- **Ref:** §4 step 3
- **Why it matters:** Modifier-stack TCs need the complete pair list to assert "this combination must collapse to one penalty".

---

## IMPORTANT Questions

### Q10. Score boundary inclusivity — confirm `≥` everywhere
- **Question:** All scoring tables use `≥`. Confirm: at every boundary the higher score is inclusive (e.g. 12.70 V → 30 pts, 12.69 V → 25 pts; 9.5 V → 20 pts, 9.4 V → 13 pts). No `>` exceptions.
- **Ask:** Backend
- **Ref:** §3.1–§3.6
- **Why:** 12 boundary TCs depend on this being uniform.

### Q11. CRANK fallback rounding rule
- **Question:** `CRANK = round(25 × rest_pts / 30)`. Is `round` standard half-up (so 20.83 → 21) or banker's rounding (20.5 → 20)?
- **Ask:** Backend
- **Ref:** §3.2 "REST Fallback for CRANK"
- **Why:** Determines whether expected output at REST=25/30 is 21 (half-up) or 21 (banker's, same here) — matters at REST=24 → 25×24/30 = 20.0 (no ambiguity) but REST=27 → 22.5 changes by rounding mode.

### Q12. DECAY drop-short threshold — strict or inclusive
- **Question:** "Drop parks shorter than 6 h" — is `<6 h` dropped and `=6 h` kept? Or is `≤6 h` dropped?
- **Ask:** Backend
- **Ref:** §3.4 "Two required data cleanups"
- **Why:** Boundary TC for the 6 h cleanup.

### Q13. DECAY high-voltage drop threshold — strict or inclusive
- **Question:** "Drop parks where start voltage exceeds 13.5 V" — is `>13.5 V` dropped and `=13.5 V` kept? Or is `≥13.5 V` dropped?
- **Ask:** Backend
- **Ref:** §3.4
- **Why:** Boundary TC.

### Q14. Replacement override — calendar day or rolling 24 h
- **Question:** "If calc 2805166 fires within 24 hours → forecast resets to 90 days" — is this 24 h rolling from event timestamp, or until end of calendar day in vehicle TZ?
- **Ask:** Backend
- **Ref:** §4 step 4
- **Why:** Edge TC at event-age = 23h59m vs 24h00m.

### Q15. Band downgrade direction
- **Question:** Confirm: the most-restrictive rule only ever **downgrades** band — it cannot upgrade. e.g. score=42 (Critical) + forecast=90 d (Excellent forecast) → band remains Critical.
- **Ask:** Backend
- **Ref:** §5
- **Why:** A common implementation slip is to use min() over band indexes which works one way but not the other.

### Q16. Temp compensation hot-side clamp
- **Question:** `crank_comp = crank_obs + 0.025 × (25 − ambient)`. At ambient = 45 °C the term is −0.5 V (downward adjustment). Is this allowed, or is compensation clamped at the hot side?
- **Ask:** Backend
- **Ref:** §3.2 "Temperature compensation"
- **Why:** A hot-climate TC could legitimately drop a healthy battery to 0 pts if not clamped.

### Q17. Score history version stamping
- **Question:** Does the persisted score record include a `pipeline_version` field (e.g. `v2.2`)? If yes, what is its exact value?
- **Ask:** Backend
- **Ref:** §rebalancing summary
- **Why:** Postcondition assertion target for the v2.1→v2.2 regression TCs.

---

## NICE TO HAVE Questions

### Q18. Tooltip dot 40 % boundary inclusivity
- **Question:** Tooltip thresholds say `≥80 % green / 40–79 % amber / <40 % red`. At exactly 40 %, is it amber or red? (Carry-over **CQ-004**.)
- **Ask:** Designer
- **Ref:** Health Score Tooltip Spec
- **Note:** Only relevant if Q1 expands scope to include tooltip TCs.

### Q19. Status column final header name
- **Question:** "Status" vs "Active Alerts" vs "Health Flags" — final choice? (Carry-over **CQ-005**.)
- **Ask:** PO
- **Ref:** Status Column Spec
- **Note:** Only relevant if Q1 expands scope.

### Q20. "+N more" interaction model
- **Question:** Hover-only, click-only, or both? (Carry-over **CQ-006**.)
- **Ask:** Designer
- **Ref:** Status Column Spec
- **Note:** Only relevant if Q1 expands scope.

### Q21. EV vehicles — CHARGE↓ suppression
- **Question:** Should CHARGE↓ be suppressed for EV stock until EV-specific charge logic ships? (Carry-over **CQ-007**.)
- **Ask:** PO + Engineering
- **Ref:** Status Column Spec
- **Note:** Affects fleet-mix triage TCs.

### Q22. v2.1 → v2.2 historic score migration policy
- **Question:** When the v2.2 pipeline goes live, will existing score history entries be re-scored under v2.2 (mass recompute) or kept under v2.1 with a watermark line, only writing v2.2 going forward?
- **Ask:** PO + Backend
- **Ref:** §rebalancing summary
- **Note:** Affects regression-test coverage if migration ships in same release.

---

## Confirmed Answers
*(fill in as answers arrive)*

| Q# | Answer | Confirmed by | Date |
|----|--------|--------------|------|
|  | | | |

---

## Readiness Decision

- [ ] **READY** — all CRITICAL questions answered → proceed to `/04-create-tc`
- [x] **BLOCKED** — waiting on CRITICAL answers Q1–Q9

---

## Next Step

→ **PAUSED.** Awaiting answers to **Q1 through Q9** (CRITICAL) before Step 3 (write test cases). IMPORTANT items (Q10–Q17) can be answered alongside; NICE TO HAVE items will be assumed unless overridden.
