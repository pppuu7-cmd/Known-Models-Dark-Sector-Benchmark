# W04 M20 SIDM K4 higher-order Hermite extension preregistration v0.1

Date: 2026-09-12
Status: FROZEN BEFORE EXECUTION
Provider: `shinichiroando/sashimi-si@e17d3664dac677b604fd4ff02fb2af105a6937fa`
Trigger: preregistered 5->7->9 ladder classified `M20_K4_HERMITE_IMPROVING_NOT_CONVERGED_DIAGNOSTIC`, with max symmetric discrepancy decreasing from `1.1726655606126613` to `0.8211898017857969`, still above the frozen 0.10 convergence-candidate level.

## Frozen physics
Retain exactly the prior Hermite-convergence physics and response contract: `M0=1e12`, redshift 0, `M0_at_redshift=True`, `dz=0.2`, `zmax=4`, `logmamin=9`, `N_ma=30`, `w=24.33 km/s`, `sigma0_m={0,1,0.1,0.01}`, and observables `Vmax_z0`, `rmax_z0`, `rs_z0`, `rhos_z0`, `core_ratio`. Exact provider and dependency environment unchanged.

Only `N_herm` changes.

## Frozen ladder
Evaluate `N_herm={9,11,13}`. Every profile recomputes its own exact-zero reference. Compute the same cellwise symmetric relative discrepancy for 9->11 and 11->13, recording maximum and median over all 15 nonzero-response cells.

## Frozen interpretation
Require finite outputs and exact-zero identity <=1e-10 in every profile.
- max(D_11to13) <=0.10 and max(D_11to13)<max(D_9to11): `M20_K4_HERMITE_HIGH_ORDER_CONVERGENCE_CANDIDATE_DIAGNOSTIC`.
- max(D_11to13)<max(D_9to11) but >0.10: `M20_K4_HERMITE_HIGH_ORDER_IMPROVING_NOT_CONVERGED_DIAGNOSTIC`.
- max(D_11to13)>=max(D_9to11): `M20_K4_HERMITE_HIGH_ORDER_NONCONVERGENCE_PERSISTS_DIAGNOSTIC`.
- execution/integrity failure: `M20_K4_HERMITE_HIGH_ORDER_BLOCKED`.

Always diagnostic-only: `K4_promoted=false`, `physical_falsification=false`, `scientific_fail=false`. No canonical K4 promotion is authorized by this diagnostic alone.
