# W04 M21 default-precision excursion diagnostic preregistration v0.1

## Purpose
Localize the deterministic `f_w=0.003` CMB excursion seen in the frozen M21 K1-v1 run before designing any K1-v2 statistic. This is a numerical/provider diagnostic only. It cannot promote K1.

## Provider and physical cases
Use the same pinned provider and physical realization as M21 K1-v1:

`lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

Cases:
- exact CDM reference `f_w=0`, `N_ncdm=0`, `omega_cdm=0.1200`;
- `f_w=0.01`;
- `f_w=0.003`;
- `f_w=0.001`.

For finite cases retain exactly:
- total `omega_dm=0.1200`;
- `m_ncdm=3000 eV`;
- `T_ncdm=0.71611`;
- default analytic Fermi-Dirac PSD;
- all common cosmology from `W04_M21_MIXED_COLD_WARM_K1_REFERENCE_PREREGISTRATION_v0.1.md`.

No physical parameter or output may change.

## Precision profiles
Execute every case under two prospectively fixed profiles in addition to the already archived default-precision v1 result.

### Profile P1: provider-shipped `cl_permille.pre`
Invoke CLASS with the pinned provider's unchanged `cl_permille.pre`. At this pin it changes only the source/transfer settings contained in that provider file. Archive the exact file SHA/content provenance.

### Profile P2: P1 plus source-bound ncdm-tight subset
In addition to unchanged `cl_permille.pre`, apply a local precision file containing only the following parameters copied verbatim from the pinned provider's `cl_ref.pre`:

- `tol_ncdm_bg = 1.e-10`
- `l_max_ncdm = 50`
- `ncdm_fluid_approximation = 3`
- `ncdm_fluid_trigger_tau_over_tau_k = 51.`
- `tol_ncdm_synchronous = 1.e-10`
- `tol_ncdm_newtonian = 1.e-10`
- `tol_perturbations_integration = 1.e-6`
- `perturbations_sampling_stepsize = 0.01`

No other `cl_ref.pre` setting is imported in P2. The goal is to separate the ncdm/perturbation precision mechanism from the much heavier full reference-precision profile.

## Measurements
For TT, EE and TE, use exact common integer ell nodes. For each profile and finite point report:

- median absolute symmetric relative residual versus that profile's exact CDM reference;
- RMS residual;
- p95 absolute residual.

For each CMB channel define the deterministic excursion factor

`E = R95(f=0.003) / max(R95(f=0.01), R95(f=0.001), 1e-300)`.

Also report the same metrics for P(k), using log-k interpolation of the reference only inside the strict overlap domain, and direct H(z) using the identical CLASS redshift grid after canonicalizing coordinate orientation.

## Diagnostic classification
For each precision profile:

- `EXCURSION_SUPPRESSED` if all three CMB channels have `E <= 3`;
- `EXCURSION_REDUCED` if the maximum CMB E is lower than the frozen default maximum by at least a factor of 3 but one or more channels still have `E>3`;
- `EXCURSION_PERSISTS` otherwise.

The frozen default-v1 excursion factors are computed from the canonical v1 result and are used only as the comparison baseline, not as a mutable threshold source.

Overall classification:
- `M21_DEFAULT_PRECISION_EXCURSION_LOCALIZED_TO_NUMERICAL_PROFILE` if P1 or P2 is `EXCURSION_SUPPRESSED`;
- `M21_DEFAULT_PRECISION_EXCURSION_REDUCED_NOT_RESOLVED` if no profile suppresses it but at least one reduces it;
- `M21_DEFAULT_PRECISION_EXCURSION_PERSISTS` otherwise.

## Guardrails
- No K1 promotion.
- Do not overwrite the K1-v1 result.
- Do not tune precision parameters after observing this diagnostic.
- If P2 suppresses the excursion, K1-v2 may preregister P2 as its numerical profile before execution.
- If P2 does not suppress it, the next step must be separately preregistered; do not silently import the full `cl_ref.pre` post hoc.
