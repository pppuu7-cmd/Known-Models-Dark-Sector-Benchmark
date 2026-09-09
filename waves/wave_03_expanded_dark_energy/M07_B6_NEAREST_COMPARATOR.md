# M07 B6 — nearest-comparator geometry

Date: 2026-09-09  
Status: **PASS_WITH_SCOPE**  
Comparator run: `34358089618`  
Artifact: `w03-m07-b6-comparator`  
Artifact digest: `sha256:aadf7fac0ae6ba3d10ddd8c1345c42bf5678ce4d7356b2b72880f8b0517d3fd6`.

## Scope

Common response block:
- `r_Delta(k,z)`;
- frozen 7 redshift x 5 low-k nodes = 35 components;
- unwhitened theory-response geometry only.

M07 input authority:
- strict production run `34338140447`;
- strict artifact digest `sha256:958708322566a2d36ce7522a3f705b543e0158c554a8de8e18e803c82a5c9cb8`.

Comparator authority:
`Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`, frozen `local_response_tangents_v0_1.json`.

Comparators:
1. `C1_smooth_w_nonphantom`;
2. `C5_designer_fR_B0` minimum resolved production ray.

No result below is an observational discrimination claim.

## Results

| M07 lambda | vs C1 smooth-w acute angle | residual after best scalar projection | vs C5 designer f(R) acute angle | residual after best scalar projection |
|---:|---:|---:|---:|---:|
| 0.025 | `15.9702 deg` | `0.2751` | `73.0805 deg` | `0.9567` |
| 0.075 | `6.9206 deg` | `0.1205` | `62.1181 deg` | `0.8839` |
| 0.15 | `6.6924 deg` | `0.1165` | `61.0432 deg` | `0.8750` |
| 0.30 | `6.6114 deg` | `0.1151` | `60.7968 deg` | `0.8729` |

## Interpretation

### M07 is close to the smooth-w direction in low-k matter response

For the controlled production branch at `lambda >= 0.075`, M07 lies within about `6.6-6.9 deg` of the frozen C1 smooth-w response direction. Best scalar rescaling still leaves about `11.5-12.0%` orthogonal residual.

Therefore exact directional equivalence is rejected, but **near-degeneracy is real** in this restricted theory-response block. A background/growth-only analysis can plausibly compress canonical quintessence toward a phenomenological smooth-w description.

This is exactly the kind of case where B6 must not be promoted to observation-space discrimination without a pinned covariance/operator.

### M07 is not close to the frozen designer-f(R) ray

The acute M07/f(R) angle remains about `60.8-73.1 deg`, with `87-96%` residual after best scalar projection. In the same common low-k structure block, the canonical scalar branch is therefore far more aligned with the smooth-DE comparator than with the frozen modified-gravity comparator.

This is a scoped response-geometry statement, not a theorem that quintessence can always be separated from modified gravity observationally.

## Internal M07 geometry

Relative to the smallest-lambda production vector (`lambda=0.025`):
- lambda 0.075: `12.5058 deg`;
- lambda 0.15: `13.6804 deg`;
- lambda 0.30: `13.9562 deg`.

However, the higher-lambda vectors are much more mutually stable:
- 0.075 vs 0.15: about `1.2124 deg`;
- 0.075 vs 0.30: about `1.5026 deg`;
- 0.15 vs 0.30: about `0.3004 deg`.

The response norm scales approximately as lambda squared:
`||r_Delta||/lambda^2 = {0.1105, 0.1167, 0.1175, 0.1189}` for lambda `{0.025,0.075,0.15,0.30}`.

This motivates a new local-coordinate audit: the physically relevant near-reference coordinate may be `q=lambda^2`, so the naive Jacobian `dr/dlambda` at lambda=0 could vanish while the model has a nonzero second-order identifiable direction.

## B6 verdict

`PASS_WITH_SCOPE` means:
- exact M07/C1 collinearity is rejected, but a strong low-k near-degeneracy is present;
- exact M07/f(R) collinearity is strongly rejected in the same block;
- observational discrimination remains OPEN;
- a parity/local-coordinate audit is required before defining the canonical M07 tangent at the LambdaCDM reference.
