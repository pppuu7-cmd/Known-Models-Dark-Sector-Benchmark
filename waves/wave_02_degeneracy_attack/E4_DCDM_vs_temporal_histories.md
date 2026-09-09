# W02-E4 — DCDM vs alternative temporal / interaction histories

Status: **INCONCLUSIVE**  
Wave: W02 — Same-observable degeneracy attack  
Frozen DSIR authority: `e3276e2193f6a5200b541a194e3175356ae5a1c1`

## Question

Can the DCDM->dark-radiation response be distinguished from alternative temporal/interaction histories using a temporal-localization coordinate that is defined identically for every model?

## Common coordinate

DSIR Exp053A already froze the response-power temporal centroid on the standard low-k 7x5 block:

`q_z(z) = sum_k r(k,z)^2 / sum_{z,k} r(k,z)^2`

`z_R = exp[sum_z q_z ln(1+z)] - 1`

Frozen grid:

- `z = {0.295, 0.51, 0.706, 0.934, 1.317, 1.491, 2.33}`;
- `k = {0.001, 0.003, 0.01, 0.03, 0.1} h/Mpc`.

Because `z_R` is invariant under an overall rescaling of `r`, the same coordinate can be evaluated on frozen local response directions from the C1/C2/C3/C5 comparison-readiness product without redefining the observable per model.

Reproducible calculator:
`code/wave02_temporal_centroid_comparator.py`.

## DCDM result

Exp053A gives the preregistered sequence

`z_R = {0.6304573, 0.6343830, 0.6419613, 0.6562403}`

for `Gamma/H0 = {0.25,0.5,1,2}`. Every consecutive step is positive by more than the preregistered `1e-3` threshold; that is a valid within-DCDM withheld-family temporal-motion result.

## Same-coordinate alternative centroids

Applying the identical `z_R` definition to frozen local response directions gives:

| Frozen direction | z_R |
|---|---:|
| C1 smooth non-phantom DE | 0.6214183 |
| C2 IDE alpha-negative | 0.9516949 |
| C2 IDE beta | 1.0839530 |
| C3 GDM cs2 | 0.7315737 |
| C3 GDM cv2 | 0.7362246 |
| C5 designer f(R) minimum-resolved ray | 0.4547904 |

The nearest listed scalar comparator to every sampled DCDM point is C1. Absolute DCDM-C1 centroid separations are approximately

`{0.0090390, 0.0129647, 0.0205430, 0.0348220}`.

## Why this is not a PASS

Wave 02 did not preregister a hard model-separation threshold in scalar `z_R`, and no observational covariance/operator has been attached to this coordinate. In addition, one scalar temporal centroid compresses away the full temporal response profile and can therefore hide mechanism differences or tunable near-coincidences.

The correct hard state is therefore:

`INCONCLUSIVE`

Specifically:

- E4 is **not blocked**: a common coordinate exists and is reproducibly computable;
- scalar `z_R` alone does **not** establish robust mechanism discrimination;
- the close C1 value demonstrates why a one-number characteristic-epoch summary cannot be assumed unique;
- full `q_z` / multi-channel temporal-response geometry and later covariance-aware projection are required for promotion.

## Methodological lesson

Characteristic epoch motion is valuable as a response axis, but a future model must not rely on a single characteristic epoch as its uniqueness claim. Preserve the full temporal profile and cross-channel correlations, then attack the nearest comparator before interpreting the mechanism.
