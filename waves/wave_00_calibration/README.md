# Wave 00 — Calibration and semantics

Status: **COMPLETE**  
Opened: 2026-09-08  
Completed: 2026-09-08  
Protocol: `protocol/WAVE_TESTING_PROTOCOL_v0.1.md`  
DSIR authority: `e3276e2193f6a5200b541a194e3175356ae5a1c1`

## Scientific question

Can KMDSB reproduce the DSIR null/reference origin and correctly distinguish a controlled non-null theory response from genuine observation-space identifiability?

## Final model set

| Model | Role | Final overall verdict | Wave-0 result |
|---|---|---|---|
| M00 LambdaCDM | null/reference control | `CONTROL_PASS_WITH_SCOPE` | null origin reproduced without fake novelty |
| M01 smooth non-phantom DE / local wCDM | first non-null control | `DSIR_COMPATIBLE_NONIDENTIFIABLE` | clean C1 response exists but is nonidentifiable in the scoped corrected ShapeFit control |

## W00-H1 / M01-B5 — CLOSED

The previously missing provenance was recovered directly from the frozen DSIR repository:

- `experiments/009_desi_dr1_multichannel_identifiability.py`;
- `data/observations/desi_dr1_shapefit_erratum_2026.json`;
- `src/dsir/shapefit_response.py`;
- `src/dsir/linear_controls.py`.

KMDSB then froze a reproducible one-sided local Fisher projection for the C1 phenomenological constant-w control into the corrected DESI DR1 ShapeFit `[DH/DM, f sigma_s8, m+n]` covariance.

Result at finite-difference step `epsilon_w=1e-4`:

- `F_epsilon_epsilon = 31.4928446382`;
- optimistic unmarginalized `sigma(epsilon_w)=0.1781944012`;
- frozen minimum C1 step `epsilon_w=1e-4` gives `sqrt(Delta chi2)=5.61185e-4`;
- even `epsilon_w=0.1` (`w=-0.9`) gives only `sqrt(Delta chi2)=0.615964` in this deliberately limited control.

Therefore M01/B5 is classified `NONIDENTIFIABLE` **in this explicit scoped projection**.

The no-nuisance Fisher information is an optimistic ceiling; nuisance marginalization can only weaken local information in the same mapping. This strengthens the nonidentifiability conclusion for the tiny frozen local step, while the result remains explicitly weaker than a full DESI likelihood analysis.

## Exit criteria

- [x] M00 null/reference origin reproduced.
- [x] M01 B0–B4 compatibility controls passed in frozen scope.
- [x] Observation-space covariance recovered from pinned DSIR provenance.
- [x] M01/B5 received a hard scoped classification: `NONIDENTIFIABLE`.
- [x] Raw response, observational identifiability and physical truth remain separate concepts.

Wave 00 is therefore **COMPLETE**.

## Central Wave-0 lesson

**A model direction can be physically/bookkeeping compatible, numerically clean, and still be observationally invisible.**

This validates one of the most important KMDSB semantics: `NONIDENTIFIABLE` is neither `FAIL` nor evidence that the theory is false.

## Design-prior output

A future dark-sector candidate should:

1. possess a controlled reference/decoupling limit;
2. not manufacture residual novelty at that limit;
3. respect physical local-domain geometry;
4. produce at least one response direction large enough relative to real covariance, not merely numerically nonzero;
5. target orthogonal channels when the optimistic nuisance-free sensitivity is already weak;
6. retain explicit masks, solver scope and observation-space provenance.

## Carry-forward

M01/B6 moves to Wave 02: nearest-comparator discrimination in the same covariance-aware spirit.
