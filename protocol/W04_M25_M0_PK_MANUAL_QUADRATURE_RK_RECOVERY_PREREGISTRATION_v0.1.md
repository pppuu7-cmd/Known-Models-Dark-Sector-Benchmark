# W04 M25 m0 P(k) manual momentum quadrature — explicit-RK provider-capacity recovery preregistration v0.1

## Motivation

The preregistered manual momentum-quadrature diagnostic is provider-blocked under the default implicit `ndf15` perturbation evolver at large NCDM momentum-grid dimension. Raw logs show dense-Jacobian allocation failure (including integer-overflow-sized allocation at N=4000). This is a numerical/provider-capacity failure and is not a physical M25 failure.

Pinned CLASS itself exposes the non-ndf15 perturbation path as `evolver = 0`; CLASS reference precision profiles use this path. This recovery changes only the perturbation ODE evolver in order to test provider reachability of the already-preregistered momentum quadrature gate.

## Frozen inputs

- CLASS pin: `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- Sterile-neutrino source/provider artifacts and m0 eta cases are the same immutable inputs as the parent manual-quadrature gate.
- Cases: m0 eta tail `e2`, `e3`, `e4` exactly as in the parent gate.
- Output: `mPk` only.
- `tol_ncdm_bg = 1e-6`.
- `tol_ncdm = 1e-6`.
- `ncdm_fluid_approximation = 3`.
- `ncdm_quadrature_strategy = 3` (manual trapezoidal q-grid).
- `ncdm_maximum_q = 10.0`.
- Momentum-bin ladder: N = 500, 1000, 2000, 4000.
- **Only recovery change:** `evolver = 0`.
- `_QUADRATURE_MAX_` and `_QUADRATURE_MAX_BG_` are raised to 4000 only to admit the frozen manual grids, exactly as in the parent diagnostic.

## Execution and independence

The four N values are independent and SHALL run as a `fail-fast: false` matrix. Within each N branch the three eta cases may run concurrently. No branch result may alter another branch's inputs.

## Admissibility / provider-capacity gate

A branch is scientifically admissible only if all three CLASS eta runs exit successfully and the existing `verification/m25/m0_pk_manual_quadrature_diagnostic.py` analyzer can compute H/P(k) diagnostics from complete outputs. GitHub-job success without successful CLASS exits is not scientific success.

If any required fine branch N=2000 or N=4000 remains provider-blocked, the parent quadrature classification remains `NOT_ESTABLISHED/PROVIDER_BLOCKED`; there is no physical falsification.

## Frozen scientific decision rule

The parent frozen rule is preserved, not retuned:

1. Fine-grid stability: N=2000 versus N=4000 symmetric relative difference <= 25% for all three P(k) tail r95 values.
2. If fine-grid stable, compare manual N=4000 against the immutable automatic-quadrature baseline.
3. If manual-4000 and automatic baseline agree <=25% for all eta tails, classify the residual floor as quadrature-insensitive/stable.
4. If the fine pair is stable but differs from automatic baseline by >25% for any eta tail, classify as quadrature-sensitive.
5. A recovered tail-scaling result may be classified separately by the already-frozen analyzer semantics.

No threshold may be changed after outputs are seen.

## Interpretation boundary

This experiment is a **numerical provider-capacity recovery and quadrature-sensitivity diagnostic**. It cannot by itself promote K1/K4, cannot establish physical falsification, and cannot be interpreted as a physical retuning of the resonant sterile-neutrino model.
