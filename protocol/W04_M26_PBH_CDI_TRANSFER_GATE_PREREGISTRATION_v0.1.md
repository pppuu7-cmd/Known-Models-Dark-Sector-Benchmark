# W04 M26 PBH CDI transfer gate preregistration v0.1

## Purpose

Promote the already validated analytic PBH Poisson/isocurvature scaling into a solver-level linear matter-power test using the pinned CLASS CDM-isocurvature (`cdi`) mode.

This is still a scoped transfer-level gate, not an observation-space constraint.

## Frozen physics mapping

For monochromatic PBHs with fraction `f` and mass `M`:

`P_S = f M / rho_dm`,

where `P_S` is the white-noise entropy/isocurvature power of the total dark-matter density perturbation.

CLASS defines `f_cdi = S_cdi/R` and the CDI primordial auto-amplitude at the pivot as `A_s f_cdi^2`. For white dimensional entropy power, choose `n_cdi = 4`, so the dimensionless entropy spectrum scales as `k^3`. Match amplitudes at `k_pivot` with

`f_cdi = sqrt(P_S k_pivot^3 / (2 pi^2 A_s))`.

Set `c_ad_cdi = 0` (uncorrelated Poisson entropy mode).

## Frozen provider and cosmology

CLASS commit: `e85808324f51fc694d12e3ed7439552a3c3f9540`.

- `h = 0.675`
- `omega_b = 0.0222`
- `omega_cdm = 0.12`
- `N_ur = 3.046`
- `A_s = 2.1e-9`
- `n_s = 0.965`
- `k_pivot = 0.05 1/Mpc`
- `tau_reio = 0.054`
- `P_k_max_h/Mpc = 100`
- `z_pk = 0`
- linear matter power only; no nonlinear correction.

Use `rho_dm = 2.77536627e11 * omega_cdm Msun/Mpc^3`.

## Frozen mass and fraction grid

Independent mass jobs:

- 100 Msun
- 1000 Msun
- 10000 Msun

Within each mass job:

- adiabatic reference (CDI omitted);
- explicit `f=0` mixed `ad,cdi` case with `f_cdi=0`;
- `f = 1, 0.1, 0.01, 0.001`.

The three mass jobs SHOULD run concurrently. Cases within a mass job have unique output roots and MAY run three-at-a-time.

## Frozen measurements

For each finite fraction:

1. compute `Delta P(k) = P_ad+cdi(k) - P_ad(k)`;
2. require positive median `Delta P` in the high-k window `5 <= k/(h/Mpc) <= 50`;
3. fit the high-k log slope of `Delta P(k)` and test white-plateau behavior;
4. record the median high-k `Delta P`.

For each mass, fit median plateau amplitude versus `f`. Aggregate across masses fits plateau amplitude versus `M` at each positive fraction.

## Gates

- explicit zero versus omitted CDI: p95 symmetric relative difference <= `1e-10`;
- all finite high-k plateaus positive;
- each high-k plateau slope has absolute value <= `0.15`;
- fraction scaling exponent is within `0.05` of 1;
- aggregate mass scaling exponent is within `0.05` of 1 for every fraction.

Per mass classification: `M26_PBH_CDI_TRANSFER_PASS_WITH_SCOPE` iff all per-mass gates pass.

Aggregate classification: `M26_PBH_CDI_TRANSFER_MASS_FRACTION_PASS_WITH_SCOPE` iff all mass jobs and all mass-scaling gates pass.

No K4/observation-space claim is made. A provider execution failure is not physical falsification. No thresholds may be changed after seeing the result.
