# W04 M20 SIDM K4 Hermite-convergence preregistration v0.1

Date: 2026-09-12
Status: FROZEN BEFORE EXECUTION
Provider: `shinichiroando/sashimi-si@e17d3664dac677b604fd4ff02fb2af105a6937fa`
Trigger: the prospectively defined `N_herm=3 -> 5` diagnostic produced `M20_K4_AXIS_STRONG_SENSITIVITY_DIAGNOSTIC` with maximum symmetric response discrepancy `0.8842068464159993` while both zero-reference identities were exact.

## Purpose

Determine whether the strong Hermite-order dependence is converging at higher quadrature order or persists. This is numerical K4 localization only. It cannot promote K4 or alter the scoped K1 result.

## Frozen physics and observables

Keep exactly the parent M20 K4 profile:
- `M0=1e12`, `redshift=0`, `M0_at_redshift=True`, `dz=0.2`, `zmax=4`, `logmamin=9`, `N_ma=30`;
- `w=24.33 km/s`;
- `sigma0_m={0,1,0.1,0.01} cm^2/g`;
- structural observables `Vmax_z0`, `rmax_z0`, `rs_z0`, `rhos_z0`, `core_ratio`;
- exact provider commit above and the already validated dependency environment.

Only `N_herm` changes.

## Frozen ladder

Evaluate matched profiles at `N_herm={5,7,9}`. Each profile recomputes its own exact-zero reference and all three nonzero cross sections.

For every sigma/observable cell compute the same symmetric relative discrepancy used by the parent diagnostic for the pairs 5->7 and 7->9:

`D = 2 |R_b-R_a| / (|R_b|+|R_a|+1e-30)`.

Record pairwise maximum and median discrepancy.

## Frozen diagnostic interpretation

Require all profiles finite and exact-zero identity <= `1e-10`.

- `max(D_7to9) <= 0.10` and `max(D_7to9) < max(D_5to7)` -> `M20_K4_HERMITE_CONVERGENCE_CANDIDATE_DIAGNOSTIC`;
- `max(D_7to9) < max(D_5to7)` but `max(D_7to9) > 0.10` -> `M20_K4_HERMITE_IMPROVING_NOT_CONVERGED_DIAGNOSTIC`;
- `max(D_7to9) >= max(D_5to7)` -> `M20_K4_HERMITE_NONCONVERGENCE_PERSISTS_DIAGNOSTIC`;
- execution/finite/identity failure -> `M20_K4_HERMITE_CONVERGENCE_BLOCKED`.

Even a convergence-candidate label is not canonical K4 PASS. Always `K4_promoted=false`, `physical_falsification=false`, `scientific_fail=false`; canonical K4 requires later synthesis with the independent dz-axis result.
