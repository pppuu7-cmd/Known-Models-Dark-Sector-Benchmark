# M07 small-lambda order audit at default perturbation precision — result

Date: 2026-09-09  
Status: **QUADRATIC_ORDER_REJECTED AT THIS NUMERICAL TIER**  
Run: `34359576368`  
Artifact: `w03-m07-small-lambda-order-audit`  
Artifact ID: `10107275635`  
Artifact digest: `sha256:1807d825dc6172a0e6a589dea557f4d36054b20c9380edcd6e84b430d08aef7e`.

## Frozen science test

New local-geometry points:
`lambda={0.005,0.010,0.020,0.040}`.

Preregistered before output:
- every response norm >= `100 x` lambda-zero reference norm;
- fitted `ln ||r_Delta|| = a + p ln lambda` must have `1.8<=p<=2.2` for quadratic-order support;
- q-scaled vectors `r/lambda^2` must show monotone adjacent convergence toward smaller lambda.

Physical branch and scalar-density shooting were strict and unchanged. Perturbation integration/sampling used CLASS defaults.

## Results

Reference `||r_Delta(lambda=0)|| = 6.01186e-10`.

Response norms:
- lambda .005: `1.69355e-5`;
- .010: `1.88308e-5`;
- .020: `4.49744e-5`;
- .040: `1.84922e-4`.

All formal signal/reference-floor ratios exceed 28,000, so the preregistered simple floor gate passes.

But the fitted power is

`p = 1.1602404921`,

outside the frozen `[1.8,2.2]` interval.

q-scaled norms:
- .005: `0.677419`;
- .010: `0.188308`;
- .020: `0.112436`;
- .040: `0.115577`.

Adjacent q convergence from large to small:
- .040 -> .020: angle `15.117 deg`, relative difference `0.26818`;
- .020 -> .010: angle `51.474 deg`, relative difference `0.78275`;
- .010 -> .005: angle `22.229 deg`, relative difference `0.75009`.

Monotone convergence gate fails.

## Crucial channel split

The background H response behaves very differently from P(k): its norms scale nearly exactly by a factor four whenever lambda doubles across `.005,.010,.020,.040`, i.e. approximately quadratic scaling.

The pathological order estimate is therefore driven by the low-k matter perturbation channel, including non-monotone small-lambda behavior.

## Interpretation after independent precision audit

This result remains an immutable FAIL of the stated numerical realization. It is **not** deleted after the later perturbation-precision audit.

Independent run `34359536106` subsequently showed that q-scaled low-k P mismatch at lambda .025/.075 falls from relative `0.21849` and `12.51 deg` at baseline precision to `0.0005519` and `0.0273 deg` at the preregistered tight perturbation tier.

Thus the present FAIL is now classified as evidence that the formal lambda-zero reference floor is not a sufficient estimate of numerical uncertainty in a small nonzero perturbation response.

A precision-conditioned rerun is allowed only because the tighter tier was selected and validated independently, and it must retain all original science thresholds unchanged.

## Methodology consequence

For local derivatives/order tests, distinguish:
1. exact-origin residual floor;
2. physical-target/shooting error;
3. nonzero perturbation response convergence across precision tiers.

A huge response/reference-floor ratio cannot substitute for item 3.
