# W04 M21 late-source cross-cosmology and provider regression v0.1

Frozen: 2026-09-15 after terminal `M21_LATE_SOURCE_ULP_SENSITIVITY_THRESHOLD_LOCALIZED_WITH_SCOPE` and before any cross-cosmology/provider execution.

## Purpose

Test whether the benchmark-local l=400 late-source threshold mechanism generalizes across a prospectively frozen set of independent exactly-flat cosmologies and across two adjacent immutable public CLASS provider states, without tuning cosmologies to the observed ULP sign.

This is the first broad regression authorized to inform whether an issue-quality provider report is warranted. It still cannot by itself declare a production defect/fix.

## Immutable provider pins

Two pins are frozen:

- `P0 = e85808324f51fc694d12e3ed7439552a3c3f9540` — provider used by the complete M21 localization chain;
- `P1 = 64bbab707faf4de4779a9e04edd180fef18d98fa` — public `master` HEAD observed and frozen on 2026-09-15. P1 is an adjacent public successor of P0.

Source recon before execution established that both pins retain:

- `angular_rescaling = ra_rec/(conformal_age-tau_rec)`;
- late-source predicate `l > transfer_neglect_late_source*angular_rescaling`;
- default `transfer_neglect_late_source=400.0`.

## Frozen physical model

All cells use the same one-species M21 mixed cold+warm model:

- warm fraction `f_W = 0.003` of total physical dark-matter density;
- `m_ncdm = 3000 eV`;
- `T_ncdm = 0.71611`;
- `N_ncdm = 1`;
- `Omega_k = 0` exactly;
- synchronous gauge, scalar adiabatic initial conditions;
- `YHe=0.24`, `T_cmb=2.725`, `A_s=2.196e-9`, `n_s=0.9655`, `k_pivot=0.05`, `tau_reio=0.054`;
- lensing off, non-linear corrections off;
- direct CMB `tCl,pCl` only;
- `l_max_scalars=450` because this regression is restricted to the frozen local multipoles 399/400/401, not a high-l production-spectrum validation.

For each cell with total `omega_dm`, define exactly:

- `omega_ncdm = 0.003*omega_dm`;
- `omega_cdm = 0.997*omega_dm`.

## Prospectively frozen cosmology grid

Baseline values are inherited from M21: `h0=0.6731`, `omega_b0=0.02222`, `omega_dm0=0.1200`.

Seven cosmologies are fixed before execution:

- `base`: `(h,omega_b,omega_dm)=(0.6731,0.02222,0.1200)`;
- `h95`: `(0.639445,0.02222,0.1200)`;
- `h105`: `(0.706755,0.02222,0.1200)`;
- `ob95`: `(0.6731,0.021109,0.1200)`;
- `ob105`: `(0.6731,0.023331,0.1200)`;
- `odm95`: `(0.6731,0.02222,0.1140)`;
- `odm105`: `(0.6731,0.02222,0.1260)`.

No cosmology may be added, removed or changed after observing results.

## Precision and multipole support

Use the repository's frozen M21 precision construction `cl_permille.pre + m21_ncdm_tight.pre + P400_ON_TAIL_OFF`, except `l_max_scalars` is fixed by each INI at 450.

Diagnostic multipoles: `l={399,400,401}`.

Diagnostic physical-k band is prospectively broadened to `[0.02,0.06] Mpc^-1` to avoid inheriting a support band localized in only one parent cosmology.

`OMP_NUM_THREADS=1` is required for diagnostic serialization.

## Three executions per provider/cosmology cell

Each independent matrix job builds one provider pin and executes:

1. `clean_native`: unpatched provider;
2. `patched_native`: output/counterfactual patch installed but counterfactual disabled;
3. `flat_identity_predicate`: same patched binary, with the late-source predicate using exact binary64 `1.0` in place of `ptr->angular_rescaling` only when `sgnK==0`.

The patch must not mutate the stored `angular_rescaling`, q/k grids, Bessel functions, source arrays, precision structure or any physical input.

## Frozen integrity tests

For every provider/cosmology cell:

- exact provider HEAD equals the matrix pin;
- build and all three executions return zero;
- only `source/transfer.c` is modified by the patch;
- diagnostic schema is finite and complete for 399/400/401 in both patched lanes;
- normalized full-CMB L2 between `clean_native` and `patched_native` <= `1e-12`;
- same-q physical-k difference between patched native and counterfactual <= `1e-12` within a cell.

## Frozen source predictions

Let `a` be native `angular_rescaling` in a cell.

At threshold 400.0:

- l=399: native and counterfactual predicate must be false;
- l=401: native and counterfactual predicate must be true;
- l=400 native predicate must equal `(a < 1.0)`;
- l=400 flat-identity counterfactual predicate must be false.

For direct scalar-E:

- at l=399 and l=401, native/counterfactual endpoints must be identical and direct transfer relative difference <= `1e-10`;
- at l=400, native/counterfactual endpoint must change iff native `a<1.0`; if `a>=1.0`, endpoint must remain identical.

No expected ULP sign is assigned to any cosmology or provider version.

## Frozen aggregate classification

For each provider pin report:

- signed ULP of native `angular_rescaling` from 1 for all seven cosmologies;
- counts `a<1`, `a==1`, `a>1`;
- whether all source predictions and counterfactual consequences hold.

Aggregate classification:

- all 14 cells authority-clean and all frozen source/counterfactual predictions hold on both pins, and each pin samples at least one `a<1` and at least one `a>=1` -> `M21_LATE_SOURCE_THRESHOLD_MECHANISM_GENERALIZES_WITH_BOUNDARY_CROSSINGS_WITH_SCOPE`;
- all 14 cells authority-clean and all predictions hold, but at least one pin lacks sign diversity -> `M21_LATE_SOURCE_THRESHOLD_MECHANISM_GENERALIZES_STRUCTURALLY_WITH_SCOPE`;
- authority clean but the two provider pins differ in the structural source/counterfactual rule -> `M21_LATE_SOURCE_THRESHOLD_PROVIDER_VERSION_DIVERGENCE_WITH_SCOPE`;
- any patch/null/schema/provider failure -> `M21_LATE_SOURCE_CROSS_COSMOLOGY_PROVIDER_REGRESSION_BLOCKED`.

## Claim ceiling

A generalization result would establish that the threshold sensitivity is a reproducible property of the late-source approximation across a frozen local family of flat cosmologies and adjacent provider pins. It still does not automatically establish an upstream defect or prescribe a fix. A production-defect claim would require an issue-quality reproducer plus an explicit precision/accuracy comparison showing that the identity-normalized or otherwise corrected behavior is preferable to native provider behavior beyond merely being smoother.

No result from this gate promotes K1/K3/K4 or constitutes physical validation/falsification of M21.