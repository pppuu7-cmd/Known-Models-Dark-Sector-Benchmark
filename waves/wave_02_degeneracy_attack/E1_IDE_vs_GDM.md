# W02-E1 — IDE vs GDM common-block adversarial comparison

Date: 2026-09-08  
Status: **PASS_WITH_SCOPE — exact directional equivalence rejected in frozen G_lowk theory-response space; observational promotion OPEN**  
DSIR authority: `e3276e2193f6a5200b541a194e3175356ae5a1c1`

## Frozen input

DSIR artifact:
`data/derived/comparison_readiness/local_response_tangents_v0_1.json`

Input blob SHA:
`37179b18618c8376763c7fe0d69df6e07da4f904`

Common block:
- response: `r_Delta(k,z)`;
- z nodes: `{0.295,0.51,0.706,0.934,1.317,1.491,2.33}`;
- k nodes: `{0.001,0.003,0.01,0.03,0.1} h/Mpc`;
- vector dimension: 35;
- geometry: unwhitened theory-response tangent geometry.

Directions:
- `C2_IDE_alpha_negative`: physically allowed alpha cone ray from `0 -> -1e-4`; positive alpha is excluded by the frozen full-history positivity condition;
- `C2_IDE_beta`: two-sided central beta tangent;
- `C3_GDM_cs2`: positive local cs2 ray;
- `C3_GDM_cv2`: positive local cv2 ray.

Reproduction code:
`code/w02_e1_pair_angles.py`.

## Metric

For vectors `a,b`:

`cos(theta) = (a.b)/(||a|| ||b||)`.

We report:
- oriented angle `theta`;
- acute line angle `acos(|cos theta|)`, useful when sign orientation is not itself the comparison target;
- `sqrt(1-cos^2 theta)`, the unit-direction residual fraction after best scalar one-dimensional projection.

The alpha-negative ray has physical orientation. Beta is a two-sided tangent, so both oriented and acute-line readings are retained.

## Results

| IDE direction | GDM direction | cosine | oriented angle | acute line angle | best scalar projection residual |
|---|---|---:|---:|---:|---:|
| alpha-negative | cs2 | 0.90678998 | 24.93455 deg | 24.93455 deg | 0.42158 |
| alpha-negative | cv2 | 0.90787703 | 24.78640 deg | 24.78640 deg | 0.41924 |
| beta | cs2 | -0.55506099 | 123.71492 deg | 56.28508 deg | 0.83181 |
| beta | cv2 | -0.55494048 | 123.70662 deg | 56.29338 deg | 0.83189 |

## Interpretation

### 1. Exact low-k directional equivalence is rejected

None of the four IDE/GDM tangent pairs is collinear on the frozen 35-node common block. Even the closest pair, IDE alpha-negative vs GDM cv2, retains a unit-direction residual of about `0.419` after best scalar rescaling.

Therefore the E1 question has a scoped positive answer at the **unwhitened theory-response level**: IDE and GDM are not merely different parameterizations of one identical low-k tangent direction in this frozen setup.

### 2. Alpha is the more dangerous mimic

IDE alpha-negative lies only about `24.8–24.9 deg` from the two nearly collinear GDM directions, while the beta tangent is much farther away (`56.29 deg` as an unoriented line, about `123.71 deg` with positive-beta orientation).

Thus if later observational projection compresses directions, alpha-vs-GDM is the higher-priority adversarial edge.

### 3. Slip cannot currently be used for IDE/GDM attribution

The DSIR block-aware observability atlas marks `S_slip` as **unknown** for both IDE alpha and beta, while it is active for GDM. Therefore KMDSB does not import the GDM cs2/cv2 slip separator into the IDE/GDM edge.

The common validated blocks include `G_lowk` and `tau_lowk`; IDE `I_kz` is near-null whereas GDM `I_kz` is active, which suggests a promising later interaction/time-structure separator, but a new pair-specific hard test must be frozen before scoring that claim.

### 4. No observational-discrimination claim yet

This result is unwhitened. A covariance/response operator can rotate, compress or erase observable directions. Therefore E1 does **not** promote M02 or M03 to a new observation-space B6 status.

## E1 verdict

`PASS_WITH_SCOPE`

Precise meaning: **exact IDE/GDM tangent equivalence is rejected on the frozen common low-k theory-response block**.

Not claimed:
- survey-level distinguishability;
- unique attribution to IDE or GDM;
- generic separation of all interacting-DE and GDM models;
- validity of an IDE slip separator.

## Carry-forward hard task

`W02-E1b`: freeze a covariance-aware projection for the closest adversarial pair `IDE alpha-negative vs GDM cs2/cv2`. If no common observational operator can be pinned, classify the observation-space edge `BLOCKED_DATA` rather than promoting this theory-space result.
