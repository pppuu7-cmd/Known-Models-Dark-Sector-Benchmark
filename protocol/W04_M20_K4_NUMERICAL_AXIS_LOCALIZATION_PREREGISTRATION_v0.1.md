# W04 M20 SIDM K4 numerical-axis localization preregistration v0.1

Date: 2026-09-12
Status: FROZEN BEFORE EXECUTION
Provider: `shinichiroando/sashimi-si@e17d3664dac677b604fd4ff02fb2af105a6937fa`
Parent scientific result: `M20_K1_V2_NONLINEAR_REFERENCE_LIMIT_PASS_WITH_SCOPE`.

## Purpose

Localize whether the scoped nonlinear SIDM response used by M20 is materially sensitive to two independent numerical controls of the pinned provider. This is a K4 diagnostic only. It does not promote K4, does not alter the frozen K1 result, and cannot establish physical family failure.

## Frozen physics

Keep fixed:
- `M0=1e12`, `redshift=0`, `M0_at_redshift=True`, `zmax=4`, `logmamin=9`, `N_ma=30`;
- velocity scale `w=24.33 km/s`;
- cross sections `sigma0_m={0,1,0.1,0.01} cm^2/g`;
- the exact provider commit above;
- the same structural observables used by K1-v2: `Vmax_z0`, `rmax_z0`, `rs_z0`, `rhos_z0`, and `core_ratio`.

No physics parameter may be retuned after seeing output.

## Numerical lanes

Baseline numerical profile:
- `dz=0.2`
- `N_herm=3`

Independent diagnostic lanes:
1. `hermite5`: change only `N_herm: 3 -> 5`, retain `dz=0.2`.
2. `dz01`: change only `dz: 0.2 -> 0.1`, retain `N_herm=3`.

`N_ma=30` is unchanged so output support shape is expected to remain comparable.

## Metrics

For each numerical profile, recompute its own exact-zero CDM reference. Require finite outputs and exact-zero structural identity under the same `1e-10` bound used by K1-v2.

For each nonzero cross section and each structural observable, compute the K1-v2-style p95 response relative to that profile's own zero reference. Compare the resulting scalar response amplitudes between baseline and the diagnostic lane with symmetric relative discrepancy

`D = 2 |R_diag - R_base| / (|R_diag| + |R_base| + 1e-30)`.

Record every `D`, the maximum over all 15 response cells, and the median.

## Frozen diagnostic interpretation

- all executions finite, both zero identities pass, and `max(D) <= 0.10` -> `M20_K4_AXIS_LOW_SENSITIVITY_DIAGNOSTIC`;
- all executions finite and `0.10 < max(D) <= 0.30` -> `M20_K4_AXIS_MODERATE_SENSITIVITY_DIAGNOSTIC`;
- all executions finite and `max(D) > 0.30` -> `M20_K4_AXIS_STRONG_SENSITIVITY_DIAGNOSTIC`;
- provider/execution/shape/finite failure -> `M20_K4_AXIS_EXECUTION_OR_INTEGRITY_BLOCKED`.

These bands are localization labels, not a canonical K4 acceptance gate. In every outcome:
- `K4_promoted=false`;
- `physical_falsification=false`;
- `scientific_fail=false`.

A later preregistered synthesis/confirmation is required before any canonical K4 status change.
