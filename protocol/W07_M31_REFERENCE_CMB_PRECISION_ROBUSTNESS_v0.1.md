# W07 M31 reference-CMB precision robustness preregistration v0.1

Date: 2026-09-12
Model: M31 effective beyond-Horndeski in pinned hi_class
Provider: `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`
Purpose: prospectively test whether the already-localized high-ell TT radial derivative nonconvergence is sensitive to the provider's own trusted CMB reference precision profile `cl_ref.pre`.

## Frozen physical stencil

Use exactly the existing M31 fine radial stencil at q0=0.1 with `parameters_smg=(q,0.5q,0.2q,0,0.3q,1)`:
- base q=0.10000;
- coarse central q=0.10050 / 0.09950, h=0.00050;
- fine central q=0.10025 / 0.09975, h=0.00025.

Keep the shipped `propto_omega_bh.ini` physics, including `kineticity_safe_smg=1e-2` and `background_Nloga=40000`.

## Frozen numerical profiles

Run every arm under exactly two profiles:
1. `default`: input `.ini` only, reproducing the prior run;
2. `cl_ref`: the same `.ini` followed by the exact pinned provider `cl_ref.pre` as a second CLASS input file.

No other numerical knobs, step sizes, k-cuts, physical parameters or thresholds may change.

## Frozen decision rule

For TT ell bands 2-30, 31-200, 201-1000, 1001-2500 and full 2-2500, compare coarse/fine central derivatives within each profile. Normalize by that profile's base TT L2 norm in the same band. Convergence criterion remains principal angle <=5 degrees AND relative norm mismatch <=0.25.

Also report the base-spectrum default-vs-cl_ref normalized L2 difference per band.

Allowed descriptive outcomes include:
- `M31_CMB_NONCONVERGENCE_PRECISION_SENSITIVE` if `cl_ref` restores convergence in every previously failing subband while default reproduces the failures;
- `M31_CMB_NONCONVERGENCE_PERSISTS_AT_REFERENCE_PRECISION` if one or more previously failing subbands still fail under `cl_ref`;
- integrity/provider blocked states.

Regardless of outcome: `K2_promoted=false`, `physical_falsification=false`, `family_exclusion=false`. A precision-sensitive result diagnoses numerics; a persistent result still does not falsify the family.