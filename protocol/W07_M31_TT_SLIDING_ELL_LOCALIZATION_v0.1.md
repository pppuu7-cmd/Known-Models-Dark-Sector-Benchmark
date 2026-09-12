# W07 M31 TT sliding-ell localization v0.1

Date: 2026-09-12
Immutable parent: run `34702705097`, artifact `10300871714`; recovered integrity authority: run `34708033251`, artifact `10302631267`.

## Purpose
Analysis-only localization of the already-established M31 high-ell derivative nonconvergence. The immutable C_l files contain a single numerical spectrum column labeled `TT`, so this audit asks where in ell the radial fine-pair TT derivative loses convergence under default precision and provider `cl_ref.pre`.

No spectra are rerun and no threshold changes are allowed.

## Frozen inputs and derivative pair
For both `default` and `cl_ref`, use only the immutable `rp2/rm2` pair at h=0.0005 and `rp1/rm1` pair at h=0.00025 from artifact `10300871714`, with the same base q=0.1 radial M31 path. Compute central TT derivative in each frozen ell window using exact common ell support.

## Frozen windows
Non-overlapping windows: 2-30, 31-100, 101-200, then successive 200-wide windows 201-400, 401-600, 601-800, 801-1000, 1001-1200, 1201-1400, 1401-1600, 1601-1800, 1801-2000, 2001-2200, 2201-2400, and 2401-2500.

For each window and profile compute coarse/fine signed cosine, principal angle, and relative norm mismatch. Retain the existing diagnostic convergence criterion angle <=5 degrees and mismatch <=0.25; this audit does not create or change a K2 gate.

## Interpretation
Report the first failing window for each profile and all pass/fail windows. Classification is `M31_TT_HIGH_ELL_NONCONVERGENCE_LOCALIZED` if at least one window fails under `cl_ref`, otherwise `M31_TT_FINE_PAIR_WINDOWS_CONVERGED_UNDER_CL_REF`.

Always `K2_promoted=false`, `canonical_K2=OPEN`, `physical_falsification=false`, `family_exclusion=false`.