# KMDSB — Known Models Dark-Sector Benchmark

A controlled benchmark for passing known dark-sector and modified-gravity models through the DSIR methodology.

## Purpose

KMDSB is the test range for **DSIR in action**. It does not replace the main `Dark-Sector-Influence-Reconstruction` repository and it does not assume that a model is correct because it is established in the literature.

The benchmark asks, for each known model or model family:

1. Can it be embedded unambiguously in the frozen DSIR bookkeeping?
2. Does it satisfy conservation, gauge/frame, domain and numerical-control requirements?
3. Which DSIR response channels does it occupy, and which cells are genuinely undefined or unobserved?
4. Is its response identifiable against LambdaCDM and its nearest comparators after covariance-aware projection?
5. Which apparent signatures disappear after quotienting identities, calibrations and measurement degeneracies?
6. Does any surviving discriminator generalize to withheld parameter points, regimes or model families?
7. What design requirement for a future dark-sector model is learned from the pass/fail/blocked outcome?

## Scientific boundary

A DSIR benchmark `FAIL` is **not automatically a proof that a physical theory is false**. The benchmark distinguishes:

- physical/theoretical failure;
- DSIR bookkeeping incompatibility;
- numerical/implementation blockage;
- observational non-identifiability;
- comparator degeneracy;
- lack of predictive novelty;
- genuinely falsified frozen prediction.

Unknown or unavailable theory/channel cells are masked, never zero-imputed.

## Architecture

- `protocol/DSIR_BENCHMARK_PROTOCOL_v0.1.md` — frozen per-model B0-B9 funnel.
- `protocol/WAVE_TESTING_PROTOCOL_v0.1.md` — cross-model wave protocol.
- `protocol/STATUS_TAXONOMY.md` — allowed gate and overall verdicts.
- `protocol/FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.1.md` — living methodology for constructing a future original dark-sector model from benchmark evidence.
- `models/<model>/audit.md` — human-readable evidence ledger.
- `models/<model>/result.json` — machine-readable verdict.
- `waves/` — calibration, atlas and adversarial cross-model waves.
- `matrices/benchmark_matrix.csv` — cross-model comparison table.
- `matrices/wave_matrix.csv` — wave-level status.
- `matrices/design_prior_ledger.csv` — evidence-derived future-model requirements.
- `logs/research_log.md` — chronological research log.
- `recovery/STATE.md` — compact current frontier/handoff state.
- `recovery/RESTORE_FROM_NEW_CHAT.md` — full recovery manual sufficient to resume development from another chat.

## DSIR authority

The scientific authority remains the main DSIR repository. Existing KMDSB audits currently pin:

`pppuu7-cmd/Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`

KMDSB consumes frozen DSIR conventions and records the exact scope/version used by each audit. Changes discovered here may propose improvements to DSIR, but are not silently promoted into DSIR itself.

## Current benchmark state — 2026-09-08

### Wave 00 — Calibration and semantics: COMPLETE

- M00 LambdaCDM: `CONTROL_PASS_WITH_SCOPE`.
- M01 smooth non-phantom DE / local wCDM ray: DSIR-compatible but `NONIDENTIFIABLE` in the scoped corrected DESI DR1 ShapeFit control.
- Calibration result: `sigma(epsilon_w) ~= 0.1782`; frozen `epsilon_w=1e-4` corresponds to about `5.61e-4 sigma` in that limited nuisance-free test.

### Wave 01 — Baseline dark-sector control atlas: COMPLETE

M02 IDE, M03 GDM, M04 thermal WDM, M05 designer f(R), M06 DCDM were passed through the frozen protocol within pinned scopes.

The wave established durable methodology pressure around tangent-cone geometry, multi-channel discrimination, rank rather than parameter count, high-k/mask discipline, modified-gravity comparators and prospective temporal holdouts.

### Wave 02 — Same-observable degeneracy attack: ACTIVE

- E1 IDE vs GDM: `PASS_WITH_SCOPE` in frozen unwhitened common low-k response geometry; closest acute line angle about `24.7864 deg`. Observation-space promotion remains open.
- E2 IDE vs designer f(R): `PASS_WITH_SCOPE` in frozen unwhitened common low-k response geometry; acute angles about `42.4503 deg` and `59.4041 deg`. Observation-space promotion remains open.
- E3 WDM vs alternative small-scale suppression: valid second pinned comparator not yet present in frozen DSIR; use `BLOCKED_IMPLEMENTATION` rather than fabricate one.
- E4 DCDM vs alternative temporal-history mechanism: active same-coordinate provenance/implementation check.

## Future-model construction

The benchmark is intentionally building a methodology before building a new theory. The current construction stages are F0-F9:

1. provenance/authority freeze;
2. recoverable reference/decoupling limit;
3. physical parameter geometry before differentiation;
4. conservation/gauge/frame closure;
5. multi-channel response architecture;
6. covariance-aware observation-space identifiability;
7. nearest-comparator attack;
8. quotient-surviving novelty;
9. prospective holdout prediction;
10. candidate synthesis and promotion.

The current `design_prior_ledger.csv` contains DP-0001..DP-0604 (30 ACTIVE requirements). They are evidence-derived priors, not yet all axioms. The methodology treats promotion conceptually as `ACTIVE -> REINFORCED -> CORE -> RETIRED` as additional waves test them.

When the requirements are mature enough, the future original dark-sector candidate should be developed in a separate repository; KMDSB remains the benchmark/evidence layer and DSIR remains the formal reconstruction authority.

## Recovery

A fresh chat should begin with `recovery/STATE.md` and then `recovery/RESTORE_FROM_NEW_CHAT.md`. If chat memory conflicts with repository evidence, repository evidence wins.
