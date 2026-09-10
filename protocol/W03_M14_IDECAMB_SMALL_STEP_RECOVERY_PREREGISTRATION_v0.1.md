# W03 M14 IDECAMB smaller-step local-convergence recovery — preregistration v0.1

Frozen: 2026-09-10

## Motivation and non-erasure rule

The prior prospectively frozen IDECAMB gate at `beta={0,0.005,0.010}` is terminal `FAIL_LOCAL_CONVERGENCE` (norm mismatch 42.56%, angle 4.385 deg). That failure is immutable and is not weakened or reclassified.

The same result showed that the fine point `beta=0.005` produces a very large early-DE response (`max |dln rho_de| ~ 13.34`). A separate smaller-step experiment is therefore scientifically justified to determine whether a genuine local tangent exists closer to the exact K1 boundary. This is a new preregistered scale-localization gate, not retrospective threshold tuning.

## Frozen provider/anchor/vector

Provider, `alpha_quint=0.02` anchor, theory-only execution route and eight-channel dimensionless response vector are exactly those in `W03_M14_IDECAMB_K4K5_LOCAL_RESPONSE_PREREGISTRATION_v0.1.md`.

No channel, sign convention or threshold is changed.

## Frozen grid

Run exact beta values:

`{0, 0.00005, 0.00010, 0.00050, 0.00100}`.

Define two predeclared right-tangent pairs:

- intermediate: h=0.00050 vs 2h=0.00100;
- finest: h=0.00005 vs 2h=0.00010.

The **scientific K4 recovery decision is based only on the finest pair**. The intermediate pair is a preregistered scale-trend diagnostic and cannot substitute for a failing finest pair.

## Frozen thresholds

Same as the failed parent gate:

- relative tangent norm mismatch <= 0.10;
- tangent direction angle <= 3 degrees.

Additionally report whether both mismatch and angle improve from the original `.005/.010` gate through the intermediate pair to the finest pair. Improvement is diagnostic only, not a PASS requirement beyond the finest-pair thresholds.

## K5

Only if the finest K4 pair passes, apply the unchanged fine-response non-null floor `max |r_h| >= 5e-5`. With one varied physical coordinate, maximum identified local rank is 1.

## Classification

- finest pair passes: `M14_IDECAMB_K4_RECOVERED_AT_SMALLER_SCALE_WITH_PRIOR_FAIL_RETAINED`; K5 then `PASS_WITH_SCOPE_RANK1` or `NONIDENTIFIABLE_AT_OUTPUT_FLOOR`.
- finest pair fails: `M14_IDECAMB_K4_SMALL_STEP_RECOVERY_FAIL`; K5 remains blocked.
- implementation/config failure: scoped blocker only.

Neither outcome is physical falsification of coupled quintessence. The original coarse-grid K4 FAIL remains part of the permanent evidence ledger in all cases.
