# W02-E2 — IDE vs designer f(R) common-block adversarial comparison

Date: 2026-09-08  
Status: **PASS_WITH_SCOPE — exact directional equivalence rejected in frozen G_lowk theory-response space; observational promotion OPEN**  
DSIR authority: `e3276e2193f6a5200b541a194e3175356ae5a1c1`

## Frozen input and common block

Input: `data/derived/comparison_readiness/local_response_tangents_v0_1.json`  
Blob SHA: `37179b18618c8376763c7fe0d69df6e07da4f904`

Common response block:
- `r_Delta(k,z)`;
- 7 frozen z nodes x 5 frozen low-k nodes = 35 components;
- unwhitened theory-response geometry.

Directions:
- physically allowed `C2_IDE_alpha_negative` ray;
- two-sided `C2_IDE_beta` tangent;
- minimum resolved production ray `C5_designer_fR_B0` at `B0=1e-6`.

Important scope note: the f(R) vector is explicitly **not** labeled an exact `B0->0` tangent because the pinned solver has a GR-transition threshold. It is the minimum resolved production ray used by DSIR.

Reproduction code: `code/w02_e1_pair_angles.py`.

## Results

| IDE direction | f(R) direction | cosine | oriented angle | acute line angle | best scalar projection residual |
|---|---:|---:|---:|---:|---:|
| alpha-negative | B0=1e-6 | -0.73786341 | 137.54973 deg | 42.45027 deg | 0.67495 |
| beta | B0=1e-6 | 0.50897981 | 59.40410 deg | 59.40410 deg | 0.86078 |

## Interpretation

### Exact low-k tangent equivalence is rejected

Neither admissible IDE direction is collinear with the frozen minimum-resolved designer-f(R) production ray. After the best scalar rescaling, the unit-direction residual remains about `0.675` for IDE alpha-negative and `0.861` for IDE beta.

Therefore IDE and designer f(R) are not merely alternative microscopic labels for one identical low-k `r_Delta(k,z)` direction in the frozen production setup.

### Orientation contains physical information but is not overused

The alpha-negative/f(R) oriented angle is `137.55 deg` while its acute line angle is `42.45 deg`. Because alpha is a physically oriented one-sided cone ray, the response sign is meaningful; however the acute line angle is also reported so the result does not depend on sign convention alone.

### No f(R) slip claim

The DSIR block-aware atlas marks `S_slip` as unknown for both C2 IDE and C5 designer f(R). Therefore this E2 audit uses only the common validated low-k structure block and does not manufacture a metric-slip separator.

### Observation-space promotion remains open

The geometry is unwhitened. A survey operator/covariance can compress or erase some of this separation. E2 therefore closes only the exact-theory-direction equivalence question, not survey distinguishability.

## E2 verdict

`PASS_WITH_SCOPE`

Precise meaning: **exact IDE/f(R) directional equivalence is rejected in the frozen common G_lowk theory-response block.**

Not claimed:
- observational discrimination;
- unique attribution to interacting dark energy or modified gravity;
- a generic theorem for all IDE/f(R) theories;
- an exact f(R) `B0->0` tangent.

## Carry-forward

`W02-E2b`: observational projection of the physically allowed IDE alpha-negative direction against the minimum-resolved f(R) production ray, preserving solver-threshold and tangent-cone masks.
