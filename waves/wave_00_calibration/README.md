# Wave 00 — Calibration and semantics

Status: **ACTIVE**  
Opened: 2026-09-08  
Protocol: `protocol/WAVE_TESTING_PROTOCOL_v0.1.md`  
DSIR authority for existing audits: `e3276e2193f6a5200b541a194e3175356ae5a1c1`

## Scientific question

Can KMDSB reproduce the DSIR null/reference origin and then correctly distinguish a controlled non-null theory response from genuine observation-space identifiability?

## Model set

| Model | Role | Current overall verdict | Wave-0 role |
|---|---|---|---|
| M00 LambdaCDM | null/reference control | `CONTROL_PASS_WITH_SCOPE` | verifies no fake residual novelty |
| M01 smooth non-phantom DE / local wCDM | first non-null control | `DSIR_COMPATIBLE` | tests compatibility vs identifiability semantics |

## Completed

- [x] M00 B0–B9 calibration audit.
- [x] M01 B0–B4 compatibility/numerical audit.
- [x] Explicit distinction between raw theory response and observational discrimination.
- [x] Wave protocol and exit criteria frozen before closing M01/B5.

## Open hard criterion

### W00-H1 / M01-B5

A hard observational-space classification requires a reproducible response operator and covariance/noise treatment that can be mapped to the frozen C1 response.

The main DSIR documentation states that DESI DR1 ShapeFit geometry/growth/shape covariance was used in Experiment 009, but the currently inspected repository code-search/tree surface does not expose a directly reusable, pinned ShapeFit covariance artifact under an obvious indexed path. KMDSB therefore does not invent a surrogate covariance.

Current state remains `PARTIAL` pending provenance recovery or a newly pinned observation-space package.

## Exit rule

Wave 00 is COMPLETE only when W00-H1 is classified as one of:

- `PASS` / `PASS_WITH_SCOPE`;
- `NONIDENTIFIABLE`;
- `BLOCKED_DATA` with a documented, reproducible provenance gap;
- `INCONCLUSIVE` after an executed hard test.

`PARTIAL` is not an exit state.

## Current wave verdict

`ACTIVE — calibration semantics validated; observation-space B5 unresolved.`

## Design-prior output so far

Wave 00 already establishes that a future model must:

1. possess a controlled reference/decoupling limit;
2. not manufacture residual novelty at that limit;
3. respect physical local-domain geometry;
4. demonstrate observable separation after covariance-aware projection, not only raw theory-space deformation;
5. retain explicit masks and solver/data scope.
