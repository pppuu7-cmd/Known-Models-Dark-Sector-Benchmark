# W07 M31 immutable block-localization audit v0.1

## Purpose

Diagnose the already-observed M31 radial central-difference nonconvergence without changing the provider, physical point, numerical settings, thresholds, or step sizes. This is analysis-only over two immutable Actions artifacts and cannot promote K2.

The pinned provider's `propto_omega_bh.ini` explicitly warns that alpha_H terms can make perturbation equations numerically stiff at early times because alpha_H contributions are amplified by `(k/aH)^4`. The present audit asks whether the recorded nonconvergence is localized primarily to the CMB block, the matter-P(k) block, both, or neither under the exact existing outputs.

## Frozen inputs

- Parent central-Jacobian run `34694420359`, M31 artifact `10298453048`: h=(0.002,0.001).
- Finer localization run `34695461864`, artifact `10298900445`: h=(0.0005,0.00025).
- Exact provider pin in both: `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`.

No provider rerun is allowed in this audit.

## Frozen calculations

For each immutable artifact independently, reconstruct the same central radial and c_T derivative blocks from its raw `*_cl.dat` and `*_pk.dat` outputs using a single common support across all arms of that artifact and the same base-block L2 normalization used by the production workflows.

For each block separately (CMB and P(k)) compute coarse-vs-fine:

- principal angle;
- relative derivative-norm mismatch.

Retain the existing diagnostic convergence criterion: angle <= 5 deg AND relative norm mismatch <= 0.25.

Additionally compare the radial derivatives across adjacent frozen resolutions:

- parent fine h=0.001 versus finer-run coarse h=0.0005;
- finer-run coarse h=0.0005 versus finer-run fine h=0.00025;

again separately in CMB and P(k), with the same 5 deg / 0.25 diagnostic criterion.

## Classification

This audit is explanatory only:

- `M31_RADIAL_NONCONVERGENCE_CMB_LOCALIZED` if P(k) satisfies the adjacent-scale criterion at both comparisons while CMB fails at least one;
- `M31_RADIAL_NONCONVERGENCE_PK_LOCALIZED` if CMB satisfies both while P(k) fails at least one;
- `M31_RADIAL_NONCONVERGENCE_BOTH_BLOCKS` if both blocks fail at least one adjacent-scale comparison;
- `M31_RADIAL_NONCONVERGENCE_NOT_REPRODUCED_BY_BLOCK_AUDIT` if both blocks satisfy both comparisons despite the combined-vector record;
- `M31_BLOCK_LOCALIZATION_INTEGRITY_BLOCKED` if immutable provenance/support cannot be verified.

## Scope guard

Always set `K2_promoted=false`, `physical_falsification=false`, `family_exclusion=false`. A channel-localized numerical instability is not a physical failure of beyond-Horndeski/DHOST. No additional step shrinking, k-cut, kineticity-floor change, background sampling change, threshold change, or post-hoc retuning is authorized by this protocol.
