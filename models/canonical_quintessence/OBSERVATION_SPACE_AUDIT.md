# M07 observation-space and gauge terminal audit

Date: 2026-09-09
Status: **M07 current stopping rule reached / W03 continues with next family**

## Scope

This audit supplements `models/canonical_quintessence/audit.md`. The machine authority for the current gate state is `models/canonical_quintessence/result.json`.

## Current B0-B9 state

| Gate | State | Meaning |
|---|---|---|
| B0 | PASS_WITH_SCOPE | pinned canonical CLASS branch and provenance |
| B1 | PASS_WITH_SCOPE | lambda-zero scalar replacement reproduces LambdaCDM |
| B2 | PARTIAL | raw physical outputs regress across gauges; small derived residuals have persistent response-level cross-gauge floor |
| B3 | PASS_WITH_SCOPE | natural-scale seed and strict shooting remove fake target drift |
| B4 | PASS_WITH_SCOPE | controlled low-k matter/background response produced |
| B5 | NONIDENTIFIABLE | corrected ShapeFit AP+growth control carries negligible M07 q information |
| B6 | PASS_WITH_SCOPE | low-k theory-space nearest-comparator attack completed |
| B7 | PARTIAL | non-collinear whitened C1-orthogonal component exists but has negligible absolute profiled significance |
| B8 | SUPPORTED | prospective level-1 within-family lambda=.225 holdout passed |
| B9 | PARTIAL | durable model-construction lessons extracted; no fundamental-model promotion |

Overall: `DSIR_PREDICTIVE_SUPPORT`.

## B5 — reference identifiability

Result file: `b5_shapefit_q_fisher_result.json`.
Workflow run: `34390859777`.
Artifact digest: `sha256:91cd68778994d06a3d41c849a7dadf2ccb9ca23f8abd924666dc41d6d2f526c4`.

Using the corrected DESI DR1 ShapeFit covariance in the same AP+growth+shape control used for M01:

`F_q ~= 0.19428289`,

`sigma_q ~= 2.26873`, where `q=lambda^2`.

Largest tested production point:
`lambda=.30`, `q=.09`, significance `~0.04009 sigma`.

Classification:
`NONIDENTIFIABLE_IN_FROZEN_LOCAL_CONTROL_SCOPE`.

This is an optimistic unmarginalized sensitivity and is not a full DESI likelihood. It is not a physical falsification of quintessence.

## B7 — observation-space nearest-comparator profiling

Result file: `b7_shapefit_c1_profile_result.json`.
Comparator: M01 C1 smooth non-phantom constant-w local direction.

In the same ShapeFit covariance:
- whitened acute angle: `33.72395 deg`;
- whitened orthogonal residual fraction: `0.55519`;
- sigma_q before C1 profiling: `2.26885`;
- sigma_q after C1 profiling: `4.08661`;
- largest tested q=.09 profiled significance: `0.02202 sigma`.

Thus M07 and C1 are not covariance-whitened collinear, but the surviving direction is observationally tiny in this control. A large angle does not rescue a vanishing absolute signal.

B7 remains `PARTIAL`, not PASS.

## B2 — gauge/frame response limitation

Raw paired synchronous/Newtonian outputs `P`, `d_m`, `phi`, `psi` satisfy the frozen `1e-4` cross-gauge regression.

Derived model/reference residuals do not:
- `lnP` response mismatch ~`3.10%`;
- direct `ln|d_m_model/d_m_ref|` mismatch ~`3.10%`;
- fractional Weyl `(phi+psi)` response mismatch ~`12.9%`.

Independent perturbation precision tightening produced an improvement ratio `0.999884`, far from the preregistered <=0.50 convergence criterion.

Therefore the current residual representations carry a persistent gauge/subtraction systematic. This is not evidence that the physical model is gauge dependent. It means these derived channels cannot be promoted as clean discriminants under current bookkeeping.

## B8 — prospective predictive support

The lambda=.225 holdout was preregistered before execution. Prediction used the frozen q-scaled response relation from training lambda={.075,.15,.30}.

Measured holdout errors:
- lnH relative L2 `0.0013263`, angle `0.019998 deg`;
- lnP relative L2 `0.0098686`, angle `0.524953 deg`.

Classification: `SUPPORTED`, strength level 1 (within-family interpolation).

This supports local predictive regularity of the tested branch only. It is not a universal DSIR law and does not overcome B5 non-identifiability.

## M07 synthesis

M07 demonstrates all of the following simultaneously:
1. a microphysical model can have a very clean reference limit;
2. its physical local coordinate may emerge only after quotienting exact field redundancy;
3. it can possess reproducible prospective within-family predictive regularity;
4. it can remain almost invisible in a realistic covariance control;
5. a theoretically orthogonal channel may be unusable if its derived residual is not gauge/frame robust.

Therefore prediction, identifiability, comparator separation and numerical/gauge robustness must remain independent promotion axes.

## Stopping rule

Do not spend more W03 cycles tightening the same M07 residual representation. Further M07 work requires a genuinely new gauge-invariant observable construction or new observational operator.

The next W03 information-gaining target is M08: time-varying smooth dark energy / CPL w0-wa, testing whether a 2D phenomenological DE manifold can absorb the M07 P/H separator that constant-w C1 cannot.
