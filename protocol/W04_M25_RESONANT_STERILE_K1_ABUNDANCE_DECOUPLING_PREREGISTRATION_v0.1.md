# W04 M25 resonant sterile-DM K1 abundance-decoupling preregistration v0.1

Date: 2026-09-11
Status: FROZEN BEFORE EXECUTION
Family: F25 / M25 resonantly produced sterile-neutrino-like WDM
Sterile-production provider: `ntveem/sterile-dm@e4486265e8207aa0dd28decc8c8d897266c0a52a`
Boltzmann provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`
Validated input bridge: run `34547836714`, classification `M25_CLASS_CONVENTION_CORRECTED_DENSITY_VALIDATED`

## Scope of K1
This protocol tests a physically admissible **abundance-decoupling embedding** of each frozen resonantly produced sterile-DM phase-space shape into a mixed CDM + sterile-DM cosmology. It does not claim that the original full-abundance production parameters possess a microphysical mass-to-infinity or mixing-angle-to-zero path that preserves the same relic-density branch.

Define one-sided abundance coordinate `eta >= 0`:
- `eta=0`: pure CDM reference, no ncdm species;
- finite `eta`: the source-corrected nonthermal sterile PSD is multiplied by `eta`, while CDM supplies the remaining dark-matter density.

Thus K1 asks whether the observable response of the validated nonthermal component continuously vanishes as its abundance vanishes.

## Frozen source convention
Use the already validated CLASS tabulated-PSD convention

`f0_CLASS(q) = (f_s(q)+f_sbar(q))/(2*pi)^3`

with
- `q=p_snapshot/T_snapshot`;
- `T_snapshot=10 MeV` verified against the immutable stock artifact;
- `T_ncdm/T_gamma=(4/11)^(1/3)`;
- `m_ncdm=7115 eV`;
- `deg_ncdm=1`;
- no `omega_ncdm` or `Omega_ncdm` input.

Use both stock PSD shapes from provider-control run `34544624039`.

## Frozen matched density bookkeeping
Reference total dark matter:
`omega_dm_ref = 0.1188`.

For each stock shape, use its independently measured CLASS full-amplitude density from corrected bridge run `34547836714` as a fixed bookkeeping coefficient:
- stock A: `omega_ncdm_base_CLASS = 0.1188179433088504`;
- stock B: `omega_ncdm_base_CLASS = 0.11893069791315644`.

At finite eta set
`omega_cdm(eta) = 0.1188 - eta * omega_ncdm_base_CLASS`.

This coefficient is frozen before K1 execution from an already validated bridge and is used only to hold the same-solver total dark-matter density fixed. The sterile PSD amplitude remains exactly `eta * f0_CLASS`; no fitted normalization is permitted.

## Frozen eta ladder
`eta = {0.10, 0.03, 0.01, 0.003, 0.001}`.

The physical geometry is one-sided. No negative eta test is meaningful.

## Frozen CLASS profile
Use the pinned CLASS source and the previously preregistered background-only capacity repair `_QUADRATURE_MAX_BG_: 800 -> 4000`, leaving `tol_ncdm_bg=1e-5` unchanged. Do not otherwise alter CLASS source or precision defaults.

Common cosmology:
- `h=0.675`
- `omega_b=0.0222`
- `omega_dm_ref=0.1188`
- `N_ur=3.046`
- flat Lambda closure inferred by CLASS
- `YHe=0.24`
- `T_cmb=2.7255 K`
- `A_s=2.1e-9`
- `n_s=0.965`
- `tau_reio=0.054`
- synchronous gauge
- linear theory only
- outputs `tCl,pCl,mPk` plus background
- `P_k_max_h/Mpc=20`, `z_pk=0`, `l_max_scalars=2500`.

No additional `.pre` precision file is authorized in v0.1.

## Frozen response measurements
Against the pure-CDM eta=0 reference, measure normalized residuals in:
- H(z) from CLASS background output;
- linear P(k,z=0);
- CMB TT;
- CMB EE;
- CMB TE.

Use the existing M21 support-aware symmetric residual metric and exact overlap-grid semantics.

For each block and each stock PSD:
1. `p95_abs(eta)` must be monotonic non-increasing as eta decreases, with 2% numerical slack between adjacent points;
2. the eta=0.001 residual must be smaller than eta=0.10;
3. a log-log fit to the smallest three eta values `{0.01,0.003,0.001}` must have exponent `p > 0.5`.

All five blocks must pass for both stock PSDs.

## Frozen classification
- provider/build/execution/output failure: `M25_K1_ABUNDANCE_DECOUPLING_PROVIDER_BLOCKED`;
- all blocks pass for both stock shapes: `M25_K1_ABUNDANCE_DECOUPLING_PASS_WITH_SCOPE`;
- otherwise: `M25_K1_ABUNDANCE_DECOUPLING_NOT_ESTABLISHED`.

On PASS set K1 only to:
`PASS_WITH_SCOPE_ABUNDANCE_TO_ZERO_MIXED_CDM_EMBEDDING`.

Always:
- `physical_falsification=false`;
- `K4_promoted=false`;
- PASS does not establish thermal-WDM discrimination, observational significance, or a microphysical zero-mixing production limit;
- FAIL/blocked does not falsify sterile-DM physics.

## Next-step rule
Only a K1 PASS authorizes K2/K3 bookkeeping and a later K4 perturbation/numerical robustness test for this representative. A K1 NOT_ESTABLISHED result must be diagnosed numerically before any K5/K6 claim.