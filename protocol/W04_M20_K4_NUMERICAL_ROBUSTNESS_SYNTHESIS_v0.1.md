# W04 M20 / F20 SIDM K4 — numerical robustness synthesis v0.1

## Purpose
This is a deterministic synthesis of already prospectively frozen K4 diagnostics. It introduces **no new numerical threshold** and does not rerun or relabel any parent test.

## Immutable inputs
1. `waves/wave_04_dark_matter/M20_K4_WEIGHTED_NUMERICAL_RECOVERY_SUMMARY.json`
   - parent unweighted Hermite negative controls are preserved;
   - weighted high-order confirmation classification must be exactly `M20_K4_WEIGHTED_HIGH_ORDER_CONFIRMATION_PASS_DIAGNOSTIC`.
2. `waves/wave_04_dark_matter/M20_K4_WEIGHTED_GRID_AXES_SUMMARY.json`
   - mass-grid classification must be exactly `M20_K4_MASS_WEIGHTED_GRID_CONVERGENCE_CANDIDATE_DIAGNOSTIC`;
   - redshift-grid classification must be exactly `M20_K4_REDSHIFT_WEIGHTED_GRID_CONVERGENCE_CANDIDATE_DIAGNOSTIC`.

The parent classification rules already require exact-zero integrity, finite provider-weighted statistics, frozen response cells and the preregistered contraction/low-amplitude gates. Synthesis does not reinterpret their continuous metrics.

## Frozen synthesis rule
K4 may be promoted **with scope** iff all three required immutable input classifications above are present simultaneously and every input records `scientific_fail=false` and `physical_falsification=false`.

PASS classification:
`M20_K4_PASS_WITH_SCOPE_WEIGHTED_HERMITE_MASS_REDSHIFT_CONVERGENCE`

Otherwise:
`M20_K4_NOT_PROMOTED_SYNTHESIS_PREREQUISITE_MISSING`

## Scope of a PASS
A PASS applies only to the pinned nonlinear SASHIMI-SIDM structural-response setup used in the parent protocols: provider commit `e17d3664dac677b604fd4ff02fb2af105a6937fa`, host `M0=1e12`, redshift 0, the frozen sigma/m response cells and the tested numerical axes `N_herm`, `N_ma`, and `dz` using the provider-population-weighted p95 response statistic.

It is **not** a claim of numerical robustness for linear cosmology, every host mass/redshift, every SIDM velocity law, every provider algorithm, or every observable functional. The earlier unweighted-node sensitivity remains preserved as a methodological negative control showing that flattened quadrature nodes must not be treated as equal-weight population samples.

K4 synthesis has no bearing on K3/K5-K9 and cannot support a family-wide physical falsification or a terminal need-for-new-model verdict.
