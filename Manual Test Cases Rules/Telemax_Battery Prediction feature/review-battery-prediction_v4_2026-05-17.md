---
status: Reviewed (self-review)
version: v4
date: 2026-05-17
reviewer: Hanna Lee (hanna.lee@telemax.com.au, acting SDET reviewer)
target: tc-battery-prediction_v4.md / tc-battery-prediction_v4.csv (77 TCs)
---

# Test Case Review Report — Battery Prediction v4

> **Skill applied:** `review-test-cases` (`.claude/skills/review-test-cases/SKILL.md`)
> **Rules applied:** `TESTCASE_RULES_SHARED.md` §10 Pre-Submit Checklist (per-TC + per-file), §11 Anti-Patterns, plus `TESTCASE_RULES_UI.md` §3 UI additions.
> **Scope:** 77 functional, UI, tooltip and edge-case TCs covering REST/CRANK/TREND/DECAY/CHARGE/LATEST + Forecast Logic + Health Bands + Status Column + Tooltip + WeatherAPI fallback.

---

## 1. Headline

| Field | Value |
|---|---|
| Total TCs reviewed | 77 |
| Verdict | **APPROVED WITH CHANGES** |
| Critical issues | 2 |
| Minor issues | 6 |
| Coverage gaps | 4 (all blocked on Q&A; cannot be closed pre-answers) |
| PENDING TCs (open CQ-blocked) | 11 |
| High-priority share | 51.9 % (≥30 % rule ✅) |
| Automation candidates | 76 / 77 = 98.7 % (1 marked Partial: BATT-017 calc config) |

**Decision rationale:** the suite is structurally sound (13/14 mandatory columns + 3 command-required extras present on every row, IDs unique and sequential, titles in `Verify <-ing form>` shape, steps tabularised, test data fenced, post-conditions back-end-truth). It does **not** ship clean: 2 critical changes are required before Step 5 sign-off, and 4 coverage gaps remain open until Q&A answers land.

---

## 2. Summary Score

| Category | Pass | Warn | Fail | Notes |
|---|---|---|---|---|
| 2.1 Structure & Format | 77 | 0 | 0 | All TCs carry the 14 SHARED columns + Feature / Requirement ID / Automation Candidate from `/04-create-tc`. |
| 2.2 Clarity & Readability | 72 | 5 | 0 | Five TCs (BATT-025, BATT-039, BATT-016, BATT-043, BATT-061) bundle multiple boundary checks in a single TC — see §4 Minor Issues. |
| 2.3 Coverage | 73 | 4 | 0 | Four functional-coverage gaps remain, all blocked by Q&A (Q2/Q3/Q4/Q5/Q9). |
| 2.4 Traceability | 77 | 0 | 0 | Every TC links to a REQ-ID and a source-document section line. |
| 2.5 Expected Results | 75 | 2 | 0 | Two TCs (BATT-033, BATT-061) have a "record actual" placeholder pending CQ — acceptable while CQ is open but must be hardened post-answer. |
| 2.6 Test Data | 77 | 0 | 0 | All test data in fenced code blocks; every TC has data even when minimal. |
| 2.7 Reusability & Maintenance | 75 | 2 | 0 | No shared-setup extraction across the heavily-repeated Flespi-calc seeded preconditions — see §4 Minor Issue 6. |
| **TOTAL** | **74.9 avg** | **1.9 avg** | **0** | |

> SHARED §10 per-file checklist: file header ✅ · Execution Summary ✅ · TOC ✅ · Summary table ✅ · file naming `tc-battery-prediction_v4.md` ✅ (matches workflow `tc-[feature]_v[N].md`) · no duplicate IDs ✅ · `---` between TCs ✅ · ≥30 % High priority ✅ (51.9 %).

---

## 3. Critical Issues — must fix before Step 5 sign-off

### C-01. BATT-023 / BATT-036 / BATT-041 assume thresholds that aren't in the spec
- **Affected TCs:** BATT-023 (TREND <10 samples), BATT-036 (CHARGE 0 trips), BATT-041 (LATEST 24 h stale)
- **Issue:** Each neutral-fallback TC encodes a numeric threshold that I had to assume because the engineering briefing doesn't state one. Today these TCs would still execute, but the *expected* output is technically guess-work — if the real threshold is different, the TC will fail for the wrong reason and the bug report will be wasted effort.
- **Fix:** Either (a) wait for answers to CQ-Q3 / CQ-Q4 / CQ-Q5 before executing these three TCs (they are currently marked PENDING — good), or (b) when executing, capture the *implementation-reported* threshold from `forecast_audit` and amend the expected value before logging a defect. Both paths are fine; just don't run-and-fail.
- **Owner:** Tester executing the cycle.

### C-02. BATT-044 modifier compounding TC encodes only one correlated-pair (rest + deep)
- **Affected TC:** BATT-044
- **Issue:** Spec §4 step 3 explicitly names only one correlated pair (rest<11.8 + deep_discharge). Real-world fleets will hit *combinations* the spec never enumerated — e.g. alternator + crank, decay + rest. CQ-Q9 is open for the full pair list. The current TC validates the named example only and therefore won't catch a misconfigured guard that ignores other valid pairs.
- **Fix:** Once Q9 is answered, expand BATT-044 into one TC per documented pair (BATT-044a, -044b, …) or convert to a data-driven matrix. Today the TC is correctly marked PENDING — but flag in handoff to the team that this is **the single highest functional risk** in the v4 suite (multiplicative behaviour on a fleet-wide score).
- **Owner:** Tester + Backend/algorithm owner.

---

## 4. Minor Issues — should fix before next revision

1. **Multi-boundary bundling.** BATT-025 (three DECAY boundaries), BATT-039 (three LATEST boundaries), BATT-016 (three REST→CRANK fallback cases), BATT-043 (three flat-slope cases), BATT-061 (eight badge triggers in one TC). All explicitly violate SHARED §3 Rule 01 *"One behaviour per TC"*. They were kept compact to mirror the v3 structure, but each should be split for next revision so a partial failure isn't ambiguous (which boundary failed? which badge?). Action: split each into N TCs in v5.
2. **"Record actual" expected result.** BATT-033 step 2 and BATT-061 step 5 use *"score per current implementation (record actual)"* in the Expected Result column. This is acceptable while the linked CQ (CQ-002, CQ-001) is open, but violates SHARED §3 Rule 04 *"Expected results must be specific"*. Action: harden to specific expected values once CQs close.
3. **Boundary inclusivity assumption.** Every `≥` boundary TC silently assumes `≥` is the implementation rule (the spec uses `≥` throughout but says nothing about edge cases like 12.00000…01). Action: add a single explicit pre-execution sanity TC (or fold into BATT-007 / BATT-010 / BATT-025) that asserts the comparison operator.
4. **Calc 2805150 config TC executes destructively in a shared tenant.** BATT-017 step 4 toggles a calc config to `false` and measures the drop. If the sandbox is shared with other tests, this will perturb their preconditions. Action: route to a dedicated sandbox tenant or wrap in a try/finally so config restore is guaranteed even on failure. Currently called out in Notes; should be hard-coded into Preconditions.
5. **Cadence dependency not surfaced.** Many TCs end with *"trigger recalc or wait for next cycle, then re-read"*. Cadence is unanswered (CQ-Q2). If the real cadence is 5 min or 60 min, the wait step will mislead testers. Action: parameterise the wait into a single shared variable referenced from each TC.
6. **No shared-setup extraction.** Roughly 60 of the 77 TCs share the precondition *"Vehicle has ≥ 30 days of telemetry in Flespi tenant; calc XXXX is enabled"*. SHARED §11 calls this out (*"no copy-paste duplication — shared steps reference a common procedure"*). Action: factor out into a `Common Preconditions` block at the top of the file and reference by name (e.g. `[CP-1: standard vehicle setup]`) — saves ~150 lines of file size and one-touch updates if Flespi tenant changes.

---

## 5. Coverage Gap Analysis

Mapped every Acceptance Criterion (AC-01 … AC-27 from `analysis-battery-prediction_v1.md` §6) against the 77 TCs:

| AC ID | Coverage | TC(s) |
|---|---|---|
| AC-01 (formula sum=100, weights 30/25/12/13/10/10) | ✅ | BATT-058 |
| AC-02 (REST 5 tiers + missing→15) | ✅ | BATT-001 – BATT-007 |
| AC-03 (REST as forecast ref when live missing) | ✅ | BATT-008 |
| AC-04 (REST <11.8 V → ×0.5) | ✅ | BATT-005 |
| AC-05 (CRANK 5 tiers compensated) | ✅ | BATT-009 – BATT-013 |
| AC-06 (CRANK temp comp formula) | ✅ | BATT-014, BATT-015 |
| AC-07 (calc 2805150 config flags) | ✅ | BATT-017 |
| AC-08 (CRANK fallback formula) | ✅ | BATT-016 |
| AC-09 (CRANK <9.5 → ×0.5 modifier) | ✅ | BATT-010, BATT-011, BATT-013, BATT-051 |
| AC-10 (TREND 4 tiers) | ✅ | BATT-018 – BATT-021 |
| AC-11 (TREND x-axis midpoint) | ✅ | BATT-022 |
| AC-12 (DECAY 5 tiers) | ✅ | BATT-024 – BATT-027 |
| AC-13 (DECAY drop <6 h + >13.5 V starts) | ✅ | BATT-028 |
| AC-14 (DECAY slope clamp ≥0) | ✅ | BATT-029 |
| AC-15 (DECAY >0.015 → ×0.7) | ✅ | BATT-027 |
| AC-16 (CHARGE 4 tiers) | ✅ | BATT-031 – BATT-034 |
| AC-17 (CHARGE speed/engine filter) | ✅ | BATT-035 |
| AC-18 (LATEST 4 tiers) | ✅ | BATT-038 – BATT-040 |
| AC-19 (forecast base formula) | ✅ | BATT-042 |
| AC-20 (flat/positive → base 90) | ✅ | BATT-043 |
| AC-21 (5 modifiers) | ✅ | BATT-005, BATT-013, BATT-027, BATT-049, BATT-050, BATT-051 |
| AC-22 (redundancy guard) | ⚠️ | BATT-044 (PENDING — partial — Q9) |
| AC-23 (worst combined multiplier 0.175) | ⚠️ | not directly tested — covered indirectly by BATT-044; **add explicit TC** |
| AC-24 (14-day floor + Critical override) | ⚠️ | BATT-045 (PENDING — CQ-003) |
| AC-25 (replacement override 90 d) | ✅ | BATT-046 |
| AC-26 (5 bands + score thresholds) | ✅ | BATT-052, BATT-054, BATT-055, BATT-056 |
| AC-27 (most-restrictive rule) | ✅ | BATT-053, BATT-057 |

**Open coverage gaps (4):**

1. **AC-23 — explicit worst-case multiplier (0.5 × 0.5 × 0.7 = 0.175).** No standalone TC asserts the final 0.175 outcome. BATT-044 will catch one piece of this once Q9 lands, but the spec singles out 0.175 as the documented worst case and it deserves its own regression anchor.
   *Recommended new TC:* BATT-078 *"Verify worst-case combined forecast multiplier collapses to 0.175 ± 0.001 when all three independent modifier groups fire"*. Mark PENDING until Q9.
2. **Hot-side compensation clamp** (Q16). No TC verifies the behaviour of `crank_compensated = crank_obs + 0.025 × (25 − 45)` (i.e. ambient 45 °C → −0.5 V adjustment). A 9.6 V raw crank in a Pilbara summer would compensate to 9.1 V → 13 pts — potentially false-failing a healthy battery.
   *Recommended new TC:* BATT-079 *"Verify CRANK temperature compensation at high ambient (45 °C) — adjustment must be clamped to ≥0 OR allowed per spec"*. Mark PENDING until Q16.
3. **Replacement override window semantics** (Q14). BATT-046 covers `event_age = 2 h`. There is no TC at the rolling boundary (event_age = 23h59m vs 24h01m).
   *Recommended new TC:* BATT-080 *"Verify replacement override window boundary at 23h59m (active) vs 24h01m (expired)"*. Mark PENDING until Q14.
4. **Band downgrade direction not over-tested upward** (Q15). BATT-053 confirms downgrade Good → Poor, but no TC asserts that a *low* score with a *high* forecast does NOT upgrade band.
   *Recommended new TC:* BATT-081 *"Verify low score (42 = Critical) with high forecast (90 d) remains Critical — band must not upgrade"*. Mark PENDING until Q15.

These four would lift the suite from 77 TCs to 81. None can be authored confidently before the linked CQ closes.

---

## 6. Anti-Patterns Spot Check (SHARED §11)

| Anti-pattern | Found? | Where |
|---|---|---|
| Vague expected results | Once | BATT-033 step 2 ("score per current implementation (record actual)") — acceptable while PENDING |
| Prose steps instead of table | 0 | All 77 TCs use `\| Step \| Action \| Expected Result \|` |
| Test data embedded in prose | 0 | All test data in fenced code blocks |
| Pre-filling Status as PASS | 0 | All 77 TCs are `Not Run` |
| Multiple behaviours in one TC | 5 | BATT-025, BATT-039, BATT-016, BATT-043, BATT-061 — see Minor Issue 1 |
| Missing post-conditions | 0 | All 77 carry back-end-truth post-conditions |
| "N/A" preconditions | 0 | Every TC has explicit preconditions |
| Reusing deleted TC IDs | 0 | IDs sequential from BATT-001 to BATT-077 with no gaps |
| Skipping test data block | 0 | Even one-line data is fenced |
| "See above" expected results | 0 | Each TC is self-contained |

---

## 7. SHARED §10 Pre-Submit Checklist — File-Level

### Per file
- [x] File is named `tc-battery-prediction_v4.md` (matches workflow `tc-[feature]_v[N].md` convention)
- [x] File header (Overview table) filled in completely
- [x] Execution Summary block present (status counts + priority breakdown)
- [x] Table of Contents lists all TCs
- [x] Summary table at the bottom is consistent with the per-TC headers
- [x] No two modules mixed in the same file (Battery Prediction only)
- [x] No duplicate TC IDs

### Per TC (sampled 10 random TCs: BATT-001, -011, -017, -022, -028, -035, -044, -057, -065, -077)
- [x] TC ID unique, sequential, `BATT-NNN` format
- [x] Title in `Verify <-ing form> when <condition>` pattern
- [x] Screen / Section filled, traceable to source doc section
- [x] Requirement Summary present (1–4 sentences)
- [x] Preconditions list all assumptions
- [x] Test Steps in table with ≥2 rows
- [x] Expected Results specific (with the one acceptable exception called out above)
- [x] Test Data in fenced code block
- [x] Post-conditions describe DB/system truth
- [x] Priority + Type + Environment + Status filled
- [x] TC ends with `---`

### UI extension (`TESTCASE_RULES_UI.md` §3) — sampled UI TCs: BATT-062, -063, -067, -068, -070, -073
- [x] Steps start from the entry point (e.g. "Open Fleet Pulse dashboard")
- [x] Every error/observed string is quoted verbatim (e.g. "Not enough data for trend", "No live data")
- [x] Mobile TCs (BATT-067, BATT-073) use Tap / Resize — no "click" terminology
- [x] Screen references named explicitly ("Fleet Pulse: Status Column Spec", "Fleet Pulse: Health Score Tooltip Spec")

---

## 8. PENDING TCs — Final List & Cross-Reference

| TC | Blocked by CQ | Question summary |
|---|---|---|
| BATT-023 | CQ-Q3 | TREND minimum sample threshold |
| BATT-033 | CQ-002 | CHARGE 4-pt tier short_trip% interaction |
| BATT-036 | CQ-Q5 | CHARGE neutral fallback trip threshold |
| BATT-037 | CQ-001 | SHORT↓ vs CHARGE↓ threshold split |
| BATT-041 | CQ-Q4 | LATEST stale-data window |
| BATT-044 | CQ-Q9 | Full redundancy-guard pair list |
| BATT-045 | CQ-003 | Sandbox vehicle for sub-14 d forecast |
| BATT-061 | CQ-007 + CQ-001 | EV CHARGE↓ suppression + CHARGE↓ threshold |
| BATT-063 | CQ-006 | "+N more" interaction model |
| BATT-065 | CQ-005 | Status column header final name |
| BATT-070 | CQ-004 | Tooltip 40 % boundary inclusion |

11 PENDING (14.3 %). Acceptable for a v4 baseline since each is gated on an external answer rather than authoring effort.

---

## 9. Suggestions (non-blocking)

- **BATT-058 (formula sum = 100)** is a strong unit-test candidate — push down the pyramid; saves a manual cycle and gates every pipeline build.
- **BATT-060 (MURANO regression)** should be wired into CI as a frozen-dataset replay; it's the most expressive end-to-end functional regression in the suite.
- **BATT-017 (calc 2805150 config)** is essential but operationally risky to automate (mutates tenant config). Run manually in a dedicated sandbox each release.
- **BATT-022 (TREND x-axis midpoint)** and **BATT-051 (CRANK ×0.5 modifier)** are both regressions of prior bugs — tag with `regression:bmw-instability` and `regression:cq-3.2-april-28` respectively so they can be filtered in execution reports.
- For v5, consider splitting **Status Column** and **Tooltip** TC groups into a separate file (`tc-fleet-pulse-status_v1.md` / `tc-fleet-pulse-tooltip_v1.md`) per SHARED §1 *"one file per module"*. They drift from the core scoring algorithm and may have their own release cadence.

---

## 10. Reviewer Sign-Off

| Field | Value |
|---|---|
| Verdict | **APPROVED WITH CHANGES** |
| Ready for execution? | No — resolve CRITICAL items first (2 items, both Q&A-dependent) |
| Ready for stakeholder hand-off? | Yes — TC suite is review-ready and the gaps are clearly traceable to open CQs |
| Re-review needed after fixes? | Yes for: (a) any newly-added BATT-078 … BATT-081 from §5 gaps, (b) BATT-044 expansion after Q9, (c) split TCs from Minor Issue 1 |
| Sign-off | Hanna Lee — 2026-05-17 |

---

## Next Step

→ Step 5 — final delivery and dashboard update. After CRITICAL fixes land, run `/06-execute` per workflow.
