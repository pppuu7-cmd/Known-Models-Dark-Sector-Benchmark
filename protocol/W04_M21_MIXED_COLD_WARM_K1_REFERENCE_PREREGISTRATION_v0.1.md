# W04 M21 mixed cold+warm dark matter K1 reference preregistration v0.1

## Scientific question
Does a source-complete mixed cold+warm dark-matter realization approach the pure-CDM boundary continuously as the warm fraction tends to zero, in a single pinned Boltzmann solver and at fixed total dark-matter physical density?

This is the first M21 gate. It is a K0/K1/K2 scaffold only. It does not claim K4 numerical derivative convergence, K6 nearest-family uniqueness, observational significance, or model preference.

## Provider and pin
Use the public CLASS repository

`lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

This is the same pinned upstream CLASS line already used by the KMDSB independent M15 reproduction. No source patch is authorized.

CLASS documents its `ncdm` sector as the generic non-cold relic sector, including warm dark matter, and permits simultaneous `m_ncdm` and `omega_ncdm`, in which case the phase-space distribution normalization is adjusted to satisfy the requested abundance.

## Frozen physical realization
Use one Fermi-Dirac `ncdm` species as an effective thermal-like warm component:

- `N_ncdm = 1` for every finite warm-fraction case;
- `m_ncdm = 3000 eV`;
- `T_ncdm = 0.71611` in units of photon temperature;
- default analytic Fermi-Dirac phase-space distribution (`use_ncdm_psd_files = 0`);
- fixed total dark-matter physical density `omega_dm = omega_cdm + omega_ncdm = 0.1200`.

Warm-fraction coordinate:

`f_w = omega_ncdm / 0.1200`.

For each finite point set

`omega_ncdm = 0.1200 f_w`,
`omega_cdm  = 0.1200 (1-f_w)`.

The exact reference uses `N_ncdm=0`, `omega_cdm=0.1200`, with all other common cosmological settings identical. We do not pass `omega_ncdm=0` with `N_ncdm=1`, because CLASS documents a zero value as an instruction to infer the coefficient from the other ncdm input rather than as a zero-abundance species.

## Frozen common cosmology
- `h = 0.6731`;
- `omega_b = 0.02222`;
- `omega_dm = 0.1200` as above;
- `N_ur = 3.046`;
- flat geometry;
- cosmological constant dark energy (`Omega_fld=0`, no dynamical DE sector);
- `YHe = 0.24`;
- `T_cmb = 2.725`;
- adiabatic scalar initial conditions;
- `A_s = 2.196e-9`;
- `n_s = 0.9655`;
- `k_pivot = 0.05 Mpc^-1`;
- `tau_reio = 0.054`;
- linear perturbations only (`non linear = none`).

## Frozen finite ladder
Run

`f_w = {0.10, 0.03, 0.01, 0.003, 0.001}`

plus the exact `f_w=0` pure-CDM reference branch.

## Frozen outputs
Require fresh finite outputs for every case:

1. background expansion history, using the common `H [1/Mpc]` column on the strict common scale-factor/redshift domain;
2. linear total matter power `P(k,z=0)` on the strict common k-domain;
3. unlensed scalar CMB `TT`, `EE`, `TE` on common integer multipoles.

No undefined column is zero-imputed. Provider-specific species columns are not part of K1.

## Residual and interpolation
For each finite warm fraction and each common block, compare against the exact pure-CDM reference with the symmetric relative residual

`r = 2 (X_f - X_0) / (|X_f| + |X_0| + floor)`.

Use `floor = 1e-12 * max|X|` separately per block/case. Interpolate only the reference onto finite-case coordinates inside the strict overlap domain. No extrapolation.

Report median absolute residual, RMS, and p95 absolute residual.

## Frozen K1 convergence gate
A block supports the pure-CDM boundary only if all are true:

1. p95 residual is non-increasing for every consecutive reduction in `f_w`, allowing 2% relative numerical slack;
2. p95 at `f_w=0.001` is smaller than p95 at `f_w=0.10`;
3. a log-log fit of p95 versus `f_w` over the three smallest fractions has positive exponent `p > 0.5`;
4. all provider cases and retained samples are finite.

M21 K1 is `PASS_WITH_SCOPE_SAME_SOLVER_ZERO_FRACTION_LIMIT` only if every retained block passes.

If any block fails, classification is `M21_K1_REFERENCE_LIMIT_NOT_ESTABLISHED` and K1 remains open. A failure is not automatically physical falsification; first diagnose solver/output/numerical causes.

## K2 geometry interpretation
If K1 passes, record K2 only as a scoped geometry statement: `f_w >= 0` is a one-sided physical abundance coordinate with the pure-CDM boundary at `f_w=0`. Negative abundance is unphysical and there is no sign quotient.

## Guardrails
- No K4 promotion from this ladder alone.
- No claim that M21 is distinguishable from pure WDM, massive neutrinos, fuzzy DM, or other small-scale-suppression families until K6.
- No observational significance without K7 covariance/nuisance profiling.
- Do not use this result to alter M04 or M19 classifications.
