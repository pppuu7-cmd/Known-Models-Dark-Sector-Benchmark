# Wave 02 — observation-space comparator graph

Closed synthesis: 2026-09-09  
Frozen audit authority: `pppuu7-cmd/Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`

This graph is deliberately separate from `THEORY_SPACE_GRAPH.md`.

## Rule

An edge is promoted here only after both models are projected through a pinned observational response operator and a consistent covariance/noise treatment, with masks preserved and nuisance treatment stated.

## Wave-02 edges

| Edge | Observation-space status | Reason |
|---|---|---|
| PC1 GDM vs designer f(R) | `OPEN` | theory-space multichannel separator exists, but no pinned common survey operator/covariance is attached to this edge |
| E1 IDE vs GDM | `OPEN` | low-k tangent non-collinearity is unwhitened; no pair-specific observation operator/covariance frozen |
| E2 IDE vs designer f(R) | `OPEN` | low-k tangent separation is unwhitened; no pair-specific observation operator/covariance frozen |
| E3 WDM vs alternative suppression | `BLOCKED_IMPLEMENTATION` | no second pinned same-convention high-k mechanism exists, so observational projection cannot yet be constructed |
| E4 DCDM vs temporal alternatives | `INCONCLUSIVE` | common scalar `z_R` has no frozen observational covariance/threshold and is too lossy for a hard mechanism separator |

## Calibration inherited from Wave 00

KMDSB already has one observation-space semantic calibration: M01 local wCDM is physically/DSIR compatible but `NONIDENTIFIABLE` in the scoped corrected DESI DR1 ShapeFit control. Therefore a clean theory-space response must never be promoted merely because it is nonzero.

## Wave-02 observation conclusion

Wave 02 closes **without promoting any new comparator edge to observational discrimination**. This is intentional. The theory graph is now better constrained, while the observation graph records exactly what kernels/covariances or implementations remain missing.
