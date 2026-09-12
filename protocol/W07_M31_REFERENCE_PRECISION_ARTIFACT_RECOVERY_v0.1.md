# W07 M31 reference-precision immutable artifact recovery v0.1

Date: 2026-09-12

## Purpose
Correct an analysis-contract mismatch in run `34702705097` without rerunning any M31 simulation. The run compared only the fine central pair (`h=5e-4` versus `2.5e-4`), while its baseline-reproduction flag was compared against the earlier three-level band classification that also required the coarser (`1e-3` versus `5e-4`) pair. This made `BASELINE_REPRODUCTION_MISMATCH` non-diagnostic.

## Immutable inputs
- reference-precision run `34702705097`, artifact `10300871714`;
- prior CMB ell-localization run `34702495845`, artifact `10301225238`.

No spectra are recomputed. No threshold, physical parameter, precision parameter, finite-difference step, or band boundary is changed.

## Frozen integrity rule
For every frozen band, the `default.coarse_fine` angle and norm mismatch in artifact `10300871714` must equal the prior `h0005_vs_h00025` values in artifact `10301225238` to absolute tolerance `1e-12`. If not, classify `M31_REFERENCE_PRECISION_ARTIFACT_INTEGRITY_BLOCKED`.

## Frozen scientific interpretation
The provider `cl_ref.pre` profile is judged only on the same fine-pair convergence criterion already frozen: principal angle <=5 degrees and relative norm mismatch <=0.25.

If integrity passes and any of `acoustic_mid_201_1000`, `high_1001_2500`, or `full_2_2500` still fails under `cl_ref.pre`, classify `M31_REFERENCE_PRECISION_HIGH_ELL_NONCONVERGENCE_PERSISTS`.
If all three pass, classify `M31_REFERENCE_PRECISION_HIGH_ELL_FINE_PAIR_CONVERGENCE_RESTORED`.

This recovery cannot promote K2, cannot exclude the M31 family, and cannot reinterpret numerical derivative behavior as physical falsification. Always set `K2_promoted=false`, `canonical_K2=OPEN`, `physical_falsification=false`, `family_exclusion=false`.