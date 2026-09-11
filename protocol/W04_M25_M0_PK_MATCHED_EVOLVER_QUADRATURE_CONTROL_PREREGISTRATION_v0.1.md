# W04 M25 m0 P(k) matched-evolver quadrature control — preregistration v0.1

## Motivation

The terminal explicit-RK manual-quadrature recovery classified the m0 P(k) residual floor as `M25_M0_PK_QUADRATURE_RK_SENSITIVE`: N=2000 and N=4000 manual grids agree extremely well, while manual N=4000 differs strongly from the earlier immutable automatic-quadrature baseline. However, the provider-capacity recovery necessarily changed the perturbation ODE branch to `evolver = 0`, whereas the earlier automatic baseline was generated before that recovery. Therefore the manual-vs-automatic comparison is not yet an isolated quadrature test: quadrature strategy and perturbation evolver differ simultaneously.

This diagnostic prospectively removes that confound. It recomputes only the automatic-quadrature side with the same pinned CLASS source and the same explicit-RK `evolver = 0` used by the successful manual N=4000 branch. The manual N=4000 artifact is immutable and is not rerun.

## Frozen provider and physical inputs

- CLASS pin: `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- Sterile-neutrino distribution/provider inputs: exactly the immutable m0 `e2`, `e3`, `e4` cases from M25 K1 run `34548988620`.
- Reference CDM outputs: exactly the immutable reference outputs carried by the same K1 artifact.
- Output: `mPk` only for the three eta-tail cases.
- `tol_ncdm_bg = 1e-6`.
- `tol_ncdm = 1e-6`.
- `ncdm_fluid_approximation = 3`.
- `ncdm_maximum_q = 10.0`.
- `evolver = 0`.
- `_QUADRATURE_MAX_` and `_QUADRATURE_MAX_BG_` are raised to 4000 exactly as in the successful manual-grid recovery so that compile-time provider capacity is held fixed.
- **Diagnostic variable only:** `ncdm_quadrature_strategy = 0` (automatic) instead of manual strategy 3 with N=4000.
- Immutable manual comparator: artifact `m25-m0-pk-qgrid-rk-4000` from run `34601708310`.
- Immutable pre-recovery automatic baseline: `m25-ncdm-nofluid-m0` from run `34551925134`, retained only to localize any evolver effect; it is not the primary quadrature comparator.

No sterile-neutrino physics, abundance, PSD, eta values, CLASS commit, fluid approximation, tolerance, q support, or decision threshold may be retuned after outputs are seen.

## Execution

The three eta cases (`e2`, `e3`, `e4`) SHALL run concurrently where runner resources permit. A dependent aggregate stage SHALL wait for all provider executions and SHALL consume the immutable manual-N4000 result. GitHub green status by itself is not a scientific PASS.

## Admissibility

The matched automatic-RK branch is admissible only if all three eta cases exit successfully and finite H/P(k) diagnostics can be computed against the immutable reference. Provider/configuration failure is `BLOCKED_IMPLEMENTATION/PROVIDER` and is not physical falsification.

## Frozen metrics

For each eta-tail P(k) r95 value use the symmetric relative difference

`D(a,b) = 2 |a-b| / (|a|+|b|)`.

Primary matched-evolver quadrature comparison:

- `D(auto_RK, manual_RK_N4000) <= 0.25` for all three eta-tail r95 values = quadrature agreement under a matched evolver.
- Any eta-tail value `> 0.25` = quadrature sensitivity persists after matching the evolver.

Secondary localization only:

- compare `auto_RK` to the immutable earlier automatic baseline with the same 25% metric.
- This secondary comparison can identify an evolver-associated shift but cannot override the primary matched-evolver quadrature result.

## Prospective classifications

1. `M25_M0_PK_MATCHED_EVOLVER_QUADRATURE_AGREEMENT` if all three primary differences are <=25%.
2. `M25_M0_PK_MATCHED_EVOLVER_QUADRATURE_SENSITIVITY` if any primary difference is >25%.
3. `M25_M0_PK_MATCHED_EVOLVER_QUADRATURE_PROVIDER_BLOCKED` if required execution/analysis is unavailable.

The result SHALL separately record whether the automatic-RK branch differs from the old automatic baseline by >25%.

## Interpretation boundary

This is a numerical causal-localization diagnostic. It cannot promote K1 or K4 by itself and cannot establish physical falsification of resonantly produced sterile-neutrino WDM. The already recorded N=2000↔4000 manual-grid convergence remains valid evidence about the manual discretization and SHALL NOT be erased regardless of this result.