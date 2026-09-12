# W04 M20 / F20 SIDM K4 — weighted independent grid axes preregistration v0.1

## Motivation
Prospective weighted-Hermite recovery and high-order confirmation showed that the earlier O(1) `N_herm` sensitivity was largely an unweighted-node-sampling artifact. The pinned provider documentation defines `N_ma` as the number of logarithmic subhalo-mass-at-accretion grid points; changing `dz` likewise changes the sampled redshift grid. Therefore numerical robustness must test these two independent grids with the same provider-population-weighted statistic rather than raw flattened-node percentiles.

This protocol is frozen before either grid-axis run and cannot promote K4 by itself.

## Frozen provider and physics
- provider `shinichiroando/sashimi-si`
- commit `e17d3664dac677b604fd4ff02fb2af105a6937fa`
- `M0=1e12`, `redshift=0`, `M0_at_redshift=True`, `zmax=4`, `logmamin=9`
- `w=24.33 km/s`
- sigma/m `{1.0,0.1,0.01}` plus exact-zero reference
- `N_herm=25`, selected from the prospectively confirmed weighted high-order regime; it is held fixed for both axes.

## Axis A — accretion-mass grid
Hold `dz=0.2`; evaluate `N_ma={30,60,120}`.

## Axis B — redshift grid
Hold `N_ma=30`; evaluate `dz={0.2,0.1,0.05}`.

## Frozen response statistic
At each grid setting, define the reference support from finite positive sigma=0 `weightCDM`. Normalize these effective-number weights. For each sigma and structural observable (`Vmax_z0`, `rmax_z0`, `rs_z0`, `rhos_z0`) compute the reference-CDM-weighted p95 of absolute symmetric SIDM-vs-CDM node response. For `core_ratio`, compute the weighted p95 of `abs(rcSIDM_z0/rsCDM_z0)`. Exact-zero identity must pass at every setting.

For each consecutive refinement, compute symmetric relative discrepancy of the 15 weighted summaries. Let D1 be the max discrepancy for the coarse->middle step and D2 for middle->fine.

## Frozen labels per axis
- `..._WEIGHTED_GRID_CONVERGENCE_CANDIDATE_DIAGNOSTIC` iff integrity passes, D1<=0.10, D2<=0.10, and D2<=1.05*D1.
- `..._WEIGHTED_GRID_LOW_AMPLITUDE_NONMONOTONE_DIAGNOSTIC` iff integrity passes and both D1,D2<=0.10 but the contraction clause fails.
- `..._WEIGHTED_GRID_IMPROVING_NOT_CONVERGED_DIAGNOSTIC` iff integrity passes, D2<D1, but at least one max exceeds 0.10.
- otherwise `..._WEIGHTED_GRID_NONCONVERGENCE_PERSISTS_DIAGNOSTIC`.
- execution/shape/nonfinite/weight failure -> `..._WEIGHTED_GRID_EXECUTION_OR_INTEGRITY_BLOCKED`.

All outcomes remain diagnostic-only with `K4_promoted=false`, `scientific_fail=false`, `physical_falsification=false`. A later K4 synthesis must combine Hermite, mass-grid and redshift-grid evidence without erasing earlier frozen negative controls.
