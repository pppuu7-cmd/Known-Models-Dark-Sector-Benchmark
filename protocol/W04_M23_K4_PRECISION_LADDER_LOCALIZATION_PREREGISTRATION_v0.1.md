# W04 M23 K4 precision-ladder localization preregistration v0.1

## Motivation

The prospectively frozen M23 K4/cross-gauge run `34596841563` is terminal. All 14 case×gauge branches execute, and its canonical result commit `605d97039eedee0d779b8a2d518667a92a32250e` classifies K3 cross-gauge common-observable closure as PASS_WITH_SCOPE but K4 as `M23_K4_NUMERICAL_ROBUSTNESS_NOT_ESTABLISHED`.

This localization is analysis-only. It does not rerun CLASS, alter the M23 cosmology, alter the Gamma0 ladder, alter gauges/channels, alter any precision profile, or relax the frozen K4 threshold/contraction rule.

## Frozen input

Canonical machine result only:
`waves/wave_04_dark_matter/M23_K4_CROSS_GAUGE_PRECISION_RESULT.json`
from run `34596841563`, aggregate artifact `10262840156`, digest `sha256:d36dc8134fe4d4066a0de635093610263915262c072d67152f335ffc86f7a1b4`.

## Deterministic analysis

For every required block TT/TE/EE/Pk across all 14 branches:

1. count frozen PASS/FAIL entries;
2. compute max R_coarse and max R_fine over finite entries;
3. count entries with R_fine > R_coarse (non-monotone precision refinement);
4. count entries satisfying the absolute `R_fine <= 1e-4` bound but failing the frozen contraction rule;
5. summarize the same quantities separately for synchronous and Newtonian gauges.

For the already-frozen cross-gauge table, report max R_gauge by block and globally. No new threshold is introduced.

## Classification boundary

This diagnostic may classify only the numerical failure pattern, for example `PRECISION_LADDER_NONMONOTONE_IN_CMB_BLOCKS` or `ABSOLUTE_BOUND_ONLY_CONTRACTION_FAILURE`. It cannot promote K4, cannot demote the already-passed scoped K3 cross-gauge result, and cannot be interpreted as physical NADM/DM-DR falsification.

A later rerun with a different solver profile is forbidden unless separately preregistered from an independently justified provider/source criterion. The failed original K4 gate remains permanent evidence.