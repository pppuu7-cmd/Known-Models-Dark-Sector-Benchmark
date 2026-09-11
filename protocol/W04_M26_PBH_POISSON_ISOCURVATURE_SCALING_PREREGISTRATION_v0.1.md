# W04 M26 PBH Poisson/isocurvature scaling preregistration v0.1

## Scope

This is a theory-level K1/K2 precursor for the distinctive PBH discreteness channel. It does not replace a later Boltzmann/observation-space implementation.

Reference: Afshordi, McDonald & Spergel, astro-ph/0302035. For monochromatic PBHs the PBH-number Poisson mode has `P_p = 1/n_PBH` and behaves as a conserved isocurvature/entropy perturbation. For a PBH fraction `f` of the total dark matter, `n_PBH = f rho_dm / M_PBH`; the contribution of PBH number fluctuations to the total-DM density contrast is weighted by `f`, giving the initial total-DM shot-noise power

`P_shot,total = f^2 / n_PBH = f M_PBH / rho_dm`.

Thus the exact `f -> 0` limit is CDM and the shot-noise amplitude is linear in both `f` and monochromatic PBH mass.

## Frozen cosmological normalization

Use physical dark-matter density `omega_dm = Omega_dm h^2 = 0.12` and

`rho_dm = 2.77536627e11 * omega_dm Msun/Mpc^3`.

The classification depends only on scaling ratios, not on this normalization choice.

## Frozen grid

Independent mass branches:

- 1 Msun
- 10 Msun
- 100 Msun
- 1000 Msun
- 10000 Msun

Fraction ladder in every branch:

`f = [1, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001, 0]`.

The mass branches SHOULD run concurrently.

## Gates

For each mass:

1. exact-null: `P_shot,total(f=0) == 0`;
2. positivity for every `f>0`;
3. log-log slope in `f` over positive points equals 1 within `1e-12`;
4. `P/f` is constant across the ladder to relative `1e-12`.

Across mass branches the aggregate additionally checks a log-log mass slope of 1 at every positive fraction.

## Classification

Per mass: `M26_PBH_POISSON_K1_ANALYTIC_PASS_WITH_SCOPE` iff all fraction gates pass.

Aggregate: `M26_PBH_POISSON_MASS_FRACTION_SCALING_PASS_WITH_SCOPE` iff every mass branch passes and all mass slopes pass.

This establishes only the analytic discreteness geometry. `K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false` until the transfer/observable implementation is independently validated.
