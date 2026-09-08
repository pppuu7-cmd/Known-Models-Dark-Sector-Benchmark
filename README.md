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

- `protocol/DSIR_BENCHMARK_PROTOCOL_v0.1.md` — frozen per-model funnel.
- `protocol/STATUS_TAXONOMY.md` — allowed gate and overall verdicts.
- `models/<model>/audit.md` — human-readable evidence ledger.
- `models/<model>/result.json` — machine-readable verdict.
- `matrices/benchmark_matrix.csv` — cross-model comparison table.
- `logs/research_log.md` — chronological research log.
- `recovery/STATE.md` — current authority/handoff state.

## DSIR authority

The scientific authority remains the main DSIR repository. KMDSB consumes frozen DSIR conventions and records the exact scope/version used by each audit. Changes discovered here may propose improvements to DSIR, but are not silently promoted into DSIR itself.

## First calibration target

**M00 — LambdaCDM** is the null/reference control. Its job is not to show novelty; its job is to verify that the benchmark reproduces the DSIR reference origin without manufacturing residual structure.

Initial status (2026-09-08): `CONTROL_PASS_WITH_SCOPE` — DSIR already reports C0 as the reference origin with multiple solver-specific zero limits, while the global DSIR G0 remains PARTIAL because a broader solver-independent reference suite is still desirable.

## Planned first wave

1. M00 LambdaCDM — null/reference control.
2. M01 smooth non-phantom DE / wCDM local family.
3. M02 interacting dark sector (IDE).
4. M03 generalized dark matter (GDM).
5. M04 thermal warm dark matter (WDM).
6. M05 designer f(R) modified gravity.
7. M06 decaying CDM -> dark radiation (withheld-family control already present in DSIR).

After calibration, the catalogue expands to additional quintessence/k-essence, interacting-sector, unified-dark-sector, fuzzy/SIDM and modified-gravity families, subject to explicit implementation/provenance availability.
