# W05 M29 Brans-Dicke K4c TT localization preregistration v0.1

Date: 2026-09-11
Provider: `hiclass-code/hi_class_public` commit `0009f51d89e6465c79e570b496c66fc90058fa77`.
Parent evidence: frozen K4 numerical-robustness failure plus K4b evidence that the P(k) high-k discrepancy is k-sampling dominated.

## Purpose

K4c is a diagnostic attribution experiment for the remaining CMB TT precision discrepancy. It does not replace K4, does not relax the original K4 thresholds, and can never set `K4_promoted=true`.

The original frozen K4 TT gate fails only at `omega_BD=15`; the `omega_BD=1e4` TT arm already satisfies its frozen max/RMS thresholds. Therefore K4c localizes the failing `omega_BD=15` TT discrepancy only. A later K4d acceptance gate must retest both omega points.

## Frozen model and common settings

Use the shipped `gravity_models/brans_dicke.ini` with only output root and `omega_BD=15` changed. Keep all model/cosmological conventions fixed. Every K4c arm uses:

- `background_Nloga=40000`;
- provider `cl_permille.pre` as the baseline CMB precision file;
- the K4b-localized reference k-sampling block: `k_min_tau0=0.002`, `k_max_tau0_over_l_max=3`, `k_step_sub=0.015`, `k_step_super=0.0001`, `k_step_super_reduction=0.1`.

## Frozen diagnostic profiles

Run independent arms (`fail-fast:false`):

1. `base_grid`: common settings only.
2. `thermo_ref`: common settings plus the `cl_ref.pre` thermodynamics/background microphysics block: `tol_ncdm_bg=1e-10`, `recfast_Nz0=100000`, `tol_thermo_integration=1e-5`, `recfast_x_He0_trigger_delta=0.01`, `recfast_x_H0_trigger_delta=0.01`.
3. `projection_ref`: common settings plus the `cl_ref.pre` harmonic/projection/transfer/lensing block: `l_logstep`, `l_linstep`, hyper-sampling settings, q-sampling settings, scalar transfer-neglect settings, `neglect_CMB_sources_below_visibility`, `transfer_neglect_late_source`, `l_switch_limber`, `accurate_lensing`, `num_mu_minus_lmax`, and `delta_l_max`, copied verbatim from the pinned provider file.
4. `thermo_projection_ref`: union of profiles 2 and 3 on top of common settings.
5. `full_core_ref`: profile 4 plus the already-tested `cl_ref.pre` perturbation-evolution/hierarchy block used by K4b `evolution_ref`, plus `tol_ncdm_synchronous=1e-10` and `tol_ncdm_newtonian=1e-10`.
6. `full_ref`: pinned provider `cl_ref.pre` with the same `background_Nloga=40000`.

No physical/model parameter differs between profiles.

## Observable and frozen metric

Primary diagnostic observable is TT from `*_cl.dat` (ell column 0, TT column 1). Use the K4 symmetric relative error `2|x-y|/(|x|+|y|+1e-300)` against `full_ref`, recording max, RMS, median, p95, p99 and ell of max.

Let `E0` be the max TT discrepancy of `base_grid` vs `full_ref`. For every diagnostic profile define max-error reduction `R = 1 - E_profile/E0`.

## Frozen attribution rule

A block is sufficient to localize the parent TT max discrepancy if `R >= 0.80`.

Classification order:

1. `THERMO_DOMINATED` if `thermo_ref` is sufficient and `projection_ref` is not;
2. `PROJECTION_DOMINATED` if `projection_ref` is sufficient and `thermo_ref` is not;
3. `BOTH_INDIVIDUALLY_SUFFICIENT` if both individual blocks are sufficient;
4. `COMBINED_THERMO_PROJECTION` if neither individual block is sufficient but `thermo_projection_ref` is;
5. `FULL_CORE_REQUIRED` if the preceding profiles are insufficient but `full_core_ref` is;
6. otherwise `UNRESOLVED_REF_PROFILE_DEPENDENCE`.

Execution/non-finite failure is classified separately.

## Interpretation boundary

K4c is attribution only. K3 remains separately provider-blocked. No K4c result is physical falsification. After K4c, a separate preregistered K4d acceptance test must use the localized settings and re-run both `omega_BD=15` and `1e4` against an independently refined numerical reference while preserving the original K4 acceptance thresholds.
