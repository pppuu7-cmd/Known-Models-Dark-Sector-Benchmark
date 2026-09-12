# W04 M20 / F20 SIDM K4 — weighted Hermite-support recovery preregistration v0.1

## Motivation
The already frozen unweighted K4 diagnostics vary `N_herm` and summarize the flattened provider catalog with ordinary percentiles. At the pinned SASHIMI-SIDM provider, `N_herm` is the Gauss-Hermite node count (`hermgauss(N_herm)`), while the provider exposes `weightCDM`/`weightSIDM` as effective subhalo-number weights and uses weights in its population examples. The retained flattened support therefore grows exactly with `N_herm`; an unweighted percentile can mix quadrature-node sampling with the physical/numerical response.

This recovery is prospective and diagnostic-only. It does not relabel any previous result and cannot promote K4 by itself.

## Frozen provider and physics
- provider: `shinichiroando/sashimi-si`
- commit: `e17d3664dac677b604fd4ff02fb2af105a6937fa`
- `M0=1e12`, `redshift=0`, `M0_at_redshift=True`, `dz=0.2`, `zmax=4`, `logmamin=9`, `N_ma=30`
- `w=24.33 km/s`
- sigma/m cells: `{1.0, 0.1, 0.01}` plus exact zero reference
- equal-step high-order Hermite sequence: `N_herm={13,17,21}`

## Frozen weighted statistic
For every order, define the reference support from finite positive `weightCDM` at sigma/m=0. Normalize those weights to unit sum. For each sigma/m and each structural observable (`Vmax_z0`, `rmax_z0`, `rs_z0`, `rhos_z0`), compute the absolute symmetric SIDM-vs-CDM node response and its reference-CDM-weighted 95th percentile. For `core_ratio`, compute the weighted 95th percentile of `abs(rcSIDM_z0/rsCDM_z0)` on the same reference support.

The numerical-axis comparison uses symmetric relative discrepancy between these weighted-p95 response summaries for 13->17 and 17->21. The same script also records the unweighted p95 as an integrity/control channel; the scientific recovery classification is based only on the prospectively frozen weighted channel.

Using reference-CDM weights is deliberate: this isolates convergence of the Hermite quadrature representation while holding the reference population measure fixed conceptually. Sigma-dependent changes in `weightSIDM` remain a separate physical population-response diagnostic and are not zero-imputed or silently absorbed into this K4 recovery.

## Frozen diagnostic thresholds
Let `Dmax_13_17` and `Dmax_17_21` be the maximum weighted-summary symmetric discrepancy over the 15 sigma/observable cells.

- `M20_K4_WEIGHTED_HERMITE_CONVERGENCE_RECOVERED_DIAGNOSTIC` iff exact-zero identity passes, all weights/statistics are finite, `Dmax_17_21 <= 0.10`, and `Dmax_17_21 <= 1.05*Dmax_13_17`.
- `M20_K4_WEIGHTING_REDUCES_SENSITIVITY_NOT_CONVERGED_DIAGNOSTIC` iff integrity passes, the above convergence gate fails, but weighted `Dmax_17_21` is <= half of the simultaneously measured unweighted `Dmax_17_21`.
- otherwise `M20_K4_WEIGHTED_HERMITE_NONCONVERGENCE_PERSISTS_DIAGNOSTIC`.
- execution/shape/nonfinite/weight failures -> `M20_K4_WEIGHTED_HERMITE_EXECUTION_OR_INTEGRITY_BLOCKED`.

In every outcome: `K4_promoted=false`, `scientific_fail=false`, `physical_falsification=false`. A recovered weighted diagnostic would require a separate confirmation protocol before any K4 promotion.
