# M07 B6 — nearest-comparator attack

Date: 2026-09-09  
Status: **PARTIAL**  
Wave: W03 — Expanded dark-energy mechanisms

## Scientific question

Does the controlled dark-energy-dominant canonical scalar-field response occupy a low-k matter-response direction distinct from the nearest phenomenological dark-energy comparator M01 smooth non-phantom DE and from the modified-gravity comparator M05 designer f(R)?

This audit answers only the common **unwhitened theory-response geometry** question. It does not claim survey distinguishability.

## M07 input

Authoritative strict-shooting production response:

- Actions run `34338140447`;
- KMDSB head `404d4bef9a2d6bbb23e4a5c3e6db723ec2dc5709`;
- artifact digest `sha256:958708322566a2d36ce7522a3f705b543e0158c554a8de8e18e803c82a5c9cb8`;
- solver `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`;
- W03 DSIR authority `328f2ca80b724870b851c7fe6366cce1ca5086cd`;
- strict scalar target `Omega_scf=0.682686955086854`;
- `tol_shooting_deltax_rel=1e-13`;
- lambda `{0.025,0.075,0.15,0.30}`.

Stored as `models/canonical_quintessence/strict_production_response.json`.

## Comparator input

Frozen DSIR W00-W02 artifact:

`Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`

`data/derived/comparison_readiness/local_response_tangents_v0_1.json`

blob SHA `37179b18618c8376763c7fe0d69df6e07da4f904`.

Directions:

- `C1_smooth_w_nonphantom`: one-sided local `epsilon_w=1+w -> 0+` tangent;
- `C5_designer_fR_B0`: minimum resolved designer-f(R) production ray at `B0=1e-6`, not labeled an exact `B0->0` tangent because of the frozen solver threshold.

The authority bridge is explicit under AD-001: the older C1/C5 vectors are not silently reinterpreted under the newer W03 DSIR authority. The common response convention/grid is unchanged for this comparison.

## Common block

`r_Delta(k,z)=ln[P_model(k,z)/P_LCDM(k,z)]`

with the frozen 7x5 grid:

- `z={0.295,0.51,0.706,0.934,1.317,1.491,2.33}`;
- `k={0.001,0.003,0.01,0.03,0.1} h/Mpc`.

No covariance whitening is applied.

For response vectors `u,v`:

`cos(theta)=(u.v)/(|u||v|)`.

Both oriented and acute line angles are reported. The best scalar-projection residual fraction is

`sqrt(1-cos(theta)^2)`.

## Results — M07 versus M01 smooth-w

| M07 lambda | cosine | acute angle | best scalar-projection residual |
|---:|---:|---:|---:|
| 0.025 | 0.961405 | 15.9702 deg | 0.27514 |
| 0.075 | 0.992714 | 6.9206 deg | 0.12049 |
| 0.15 | 0.993186 | 6.6924 deg | 0.11654 |
| 0.30 | 0.993350 | 6.6114 deg | 0.11513 |

### Interpretation

For `lambda>=0.075`, the M07 low-k matter-response direction is strongly aligned with the frozen M01 smooth-w tangent. Exact collinearity is not present, but an approximately 6.6–6.9 degree unwhitened angle is too small to treat the low-k matter block as a robust microphysical discriminator.

This is a direct realization of W03-H1/W03-H4 pressure: a canonical scalar field may carry different microphysics while remaining close to a phenomenological smooth-w response in a restricted observable block.

Therefore **M01 remains the nearest unresolved comparator**.

## Results — M07 versus M05 designer f(R)

| M07 lambda | oriented angle | acute angle | best scalar-projection residual |
|---:|---:|---:|---:|
| 0.025 | 106.9195 deg | 73.0805 deg | 0.95671 |
| 0.075 | 117.8819 deg | 62.1181 deg | 0.88391 |
| 0.15 | 118.9568 deg | 61.0432 deg | 0.87499 |
| 0.30 | 119.2032 deg | 60.7968 deg | 0.87289 |

Exact low-k response-direction equivalence to the frozen minimum-resolved designer-f(R) ray is strongly rejected within this theory-response scope.

This is not a unique-attribution claim and is not observational discrimination.

## Internal M07 shape stability

The strict production family is not exactly a single ray. Relative to `lambda=0.025`, the angles are approximately:

- to `0.075`: `12.506 deg`;
- to `0.15`: `13.680 deg`;
- to `0.30`: `13.956 deg`.

But the larger-lambda directions are extremely stable among themselves:

- `0.075` vs `0.15`: `1.212 deg`;
- `0.075` vs `0.30`: `1.503 deg`;
- `0.15` vs `0.30`: `0.300 deg`.

Meanwhile the response norm grows rapidly with lambda. Thus amplitude growth and response-direction evolution must be treated separately.

## B6 verdict

`PARTIAL`.

Closed within scope:

- M07 is not low-k directionally equivalent to the frozen M05 designer-f(R) production ray.

Still open:

- M07 versus M01 smooth-w remains near-degenerate in the low-k matter block;
- an orthogonal perturbation/time/metric/scalar-source response is required before a stronger B6 verdict;
- observational promotion remains forbidden without a pinned operator/covariance.

## Methodological consequence

For microphysical dark-energy candidates, `P(k,z)` can remain nearly tangent to a phenomenological smooth-w family even after solver-clean microphysical implementation. The future-model funnel must therefore attack a phenomenological DE nearest comparator using at least one additional physically motivated response axis instead of treating microphysical ontology itself as novelty.

Machine-readable result:
`M07_B6_COMPARATOR_RESULT.json`.

Reproduction code:
`code/w03_m07_comparator_geometry.py`.
