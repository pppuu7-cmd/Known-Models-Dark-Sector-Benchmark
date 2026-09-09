# W03 M07/M08 common ShapeFit observation-space audit

Date: 2026-09-09  
Status: **PASS_WITH_SCOPE / M07 NONIDENTIFIABLE AFTER CPL PROFILING**

## Why this test was needed

Earlier M07 observation-space work profiled a constant-w C1 direction, but M08 subsequently showed that the broader two-dimensional CPL local family absorbs the M07 P+H theory-response direction to about 1.1% residual.

Meanwhile DSIR advanced to `864952e1520d82473a9e976edfeb69f9899d174d` and froze a stricter Article-2 G5 rule: a covariance cannot support a cross-family claim unless every compared family is mapped through one exact common observation operator into the same covariance coordinates.

Therefore this audit does **not** combine old family-specific proxies. It reruns M07 and M08 together with:
- one pinned CLASS build;
- one pure-LambdaCDM reference;
- one prospectively frozen ShapeFit mapping;
- one fixed 15-coordinate order;
- one fixed covariance;
- one whitening and profiling calculation.

Preregistered contract:
`protocol/W03_M07_M08_COMMON_SHAPEFIT_OPERATOR_V0_1.md`.

Contract commit before execution:
`46424a91cf625d52d4bcb5da18e09ec69eb33772`.

## Execution authority

Actions run: `34396432509`  
Head: `457db40ce1defaf9d9cf1ce326db93cc584c0cf0`  
Artifact digest: `sha256:57e35eea1a1a72f5ecf13f949abfdf3c67ac451b7ab133f4f0578e6097111b28`  
Pinned CLASS: `e85808324f51fc694d12e3ed7439552a3c3f9540`.

All seven CLASS cases passed, the analyzer passed, and the fail-closed common-bridge gate passed.

Machine result:
`M07_M08_COMMON_SHAPEFIT_RESULT.json`.

## Common coordinate/covariance controls

Exact vector length: 15.

Order:
five bins `LRG1, LRG2, LRG3, ELG2, QSO`, each with
`[DH/DM, f_sigma_s8_control, m_plus_n_control]`.

Covariance diagnostics:
- shape `15x15`;
- max asymmetry `0`;
- 2-norm condition number `38.4089`;
- Cholesky roundtrip relative L2 `8.46e-17`.

No regularization, truncation, pseudoinverse or output-dependent coordinate deletion was used.

## M07 local q direction inside the common operator

M07 uses the already-controlled quotient coordinate

`q=lambda^2`.

The common workflow independently builds q-scaled mapped directions at lambda .025 and .075.

Their consistency in the common ShapeFit operator is:
- cosine `0.9999967336`;
- angle `0.146445 deg`;
- relative L2 difference `0.00274250`.

This supports use of their componentwise mean as the local M07 q direction for this scoped operator.

Before profiling CPL:

`F_q = 0.19428249`

`sigma_q = 2.26873185`.

This independently reproduces the scale of the earlier model-specific M07 B5 result while now using the same joint workflow that also generates the M08 comparator directions.

## M08 local span after covariance whitening

Whitened M08 CPL singular values:

`{5.48700104, 0.99049586}`.

Whitened ratio:

`sigma2/sigma1 = 0.1805168`.

This is notable because the corresponding unwhitened P+H theory-space ratio was about `0.0502`.

Therefore the observational metric changes the relative importance of the weak CPL direction. It remains weaker than the leading direction, but the covariance weights it substantially more strongly than the raw theory norm does.

This is another direct example of why unwhitened rank geometry is not observational rank geometry.

## M07 after profiling the full local CPL span

One shared M08 parameter vector is fitted in the 15-dimensional whitened space.

Best coefficients per unit M07 q:

- `epsilon0/q = 0.14430605`;
- `wa/q = -0.22336290`.

Whitened residual:
- norm `0.00470210`;
- residual fraction `0.01066780` = **1.067%**;
- subspace angle `0.611232 deg`.

Thus the covariance-whitened M07 direction lies almost entirely inside the local CPL subspace in this common operator.

### Profiled information

After Schur-complement profiling of `(epsilon0,wa)`:

`F_q,prof = 2.21097e-5`

`sigma_q,prof = 212.6709`.

Compared with unprofiled `sigma_q=2.26873`, this is a degradation factor of

`93.74x`.

At the already-frozen largest M07 production scale

`lambda=.30`, `q=.09`,

the local profiled significance is only

`0.00042319 sigma`.

The prospectively frozen classification threshold was 1 sigma for this benchmark identifiability screen.

Result:

`NONIDENTIFIABLE_AFTER_CPL_PROFILING_IN_COMMON_SHAPEFIT_CONTROL`.

## Scientific interpretation

This is stronger than the earlier C1 result in two ways:

1. M08 represents the flexible local smooth-DE family span rather than one constant-w ray.
2. M07 and M08 are mapped through the same observation operator and covariance in one workflow.

The result is therefore strong evidence that the tested late-time ShapeFit signature of canonical M07 quintessence does **not** carry mechanism-level observational novelty beyond flexible CPL smooth dark energy in this scope.

It does **not** mean M07 is physically false. M07 still has:
- a clean LambdaCDM intersection;
- controlled q geometry;
- stable numerical production;
- prospective within-family holdout support.

The correct separation is:

**predictive regularity: yes**  
**mechanism-specific ShapeFit novelty beyond local CPL: no evidence / nonidentifiable in this control**.

## Consequence for B7

M07 global B7 remains `PARTIAL`, because KMDSB has not exhausted every valid channel or survey operator. But the specific P/H / ShapeFit novelty path is now strongly closed against local CPL:

- constant-w separator: insufficiently adversarial;
- 2D CPL theory-space profiling: ~1.1% residual;
- common ShapeFit whitening + CPL profiling: ~1.07% residual and `0.000423 sigma` at q=.09.

Therefore this channel cannot be used to promote M07 mechanism novelty.

## Consequence for the future original model

A future dark-sector model must not rely on a signature that can be generated by a mild flexible `w(a)` history after covariance weighting.

The design target must move toward at least one **robust extra-family direction**, for example:
- scale-dependent structure not captured by smooth DE;
- gauge-robust slip/lensing combinations;
- nonlinear or high-k characteristic-scale behavior;
- temporal-scale relations constrained by one shared parameter mapping;
- tensor/GW or coupling channels where physically defined;
- prospective withheld relations that flexible smooth-DE and MG manifolds fail.

## Boundary relative to DSIR Article-2 G5

This audit follows the new coordinate-compatibility discipline but is **not** full G5 closure:
- only M07 and M08 are compared;
- no multi-family weighting schemes;
- no family-stratified bootstrap;
- no leave-one-family-out stress;
- ShapeFit shape response is frozen to zero as part of the scoped late-time control.

Full Article-2 G5 still requires the broader bound multi-family observation-provider matrix or another prospectively frozen equivalent.
