# KMDSB current state / recovery handoff

Updated: 2026-09-08

## Mission
Pass known dark-sector and modified-gravity models through a frozen DSIR benchmark funnel, record why each gate passes/fails/blocks, and accumulate design priors for a future candidate dark-sector model.

## Scientific authority
Main DSIR snapshot currently used:
`pppuu7-cmd/Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`

Do not silently replace this snapshot inside an existing audit. If authority advances, record a new audit revision or authority-delta note.

## Frozen KMDSB protocol
`protocol/DSIR_BENCHMARK_PROTOCOL_v0.1.md`

Gate sequence:
- B0 identity/provenance
- B1 DSIR embedding/reference limit
- B2 conservation/gauge/frame bookkeeping
- B3 physical-domain/numerical control
- B4 response coverage/masks
- B5 LambdaCDM/reference identifiability
- B6 nearest-comparator discrimination
- B7 quotient-surviving residual novelty
- B8 prospective withheld prediction
- B9 synthesis/design-prior extraction

## Completed audits

### M00 LambdaCDM
`CONTROL_PASS_WITH_SCOPE`

Purpose: null/reference calibration. No novelty expected.

### M01 smooth non-phantom DE / wCDM local ray
`DSIR_COMPATIBLE`

B0–B4 controlled within frozen C1 scope. B5 is PARTIAL. B6–B8 OPEN.

## Current highest-priority task

**M01/B5 — observation-space whitened identifiability.**

The task must not use raw theory-space angle alone. Freeze an observational response operator/covariance treatment, project the C1 local response and LambdaCDM origin into that space, whiten consistently, then state whether the deformation is identifiable at the chosen amplitude/domain.

If available observational covariance is insufficient, return `BLOCKED_DATA` or a calibrated sensitivity curve rather than forcing PASS/FAIL.

## Next model after M01 B5

M02 — interacting dark sector (IDE), using the frozen DSIR C2 geometry:
- physical local geometry is a tangent cone;
- positive alpha violates the frozen full-history positivity condition, so alpha is one-sided;
- beta tangent is two-sided;
- no symmetric finite-difference fiction is permitted across the forbidden domain.

## Non-negotiable rules

1. Never zero-impute missing channels.
2. Never equate theory-space separation with observational discrimination.
3. Never equate non-identifiability with theory falsification.
4. Never promote a retrospective relation to prospective B8 support.
5. Every completed audit adds explicit design-prior deltas.
6. Update matrix, log and this state whenever the frontier changes.
