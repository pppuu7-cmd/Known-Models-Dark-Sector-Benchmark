# W03/M07 observation-space lessons

Updated: 2026-09-09
Status: evidence-backed supplement for future-model construction

## 1. Predictive regularity and detectability are independent axes

M07 canonical quintessence supports a prospective within-family holdout at lambda=0.225, but the same branch is strongly non-identifiable in the corrected DESI DR1 ShapeFit AP+growth control.

Local physical coordinate after quotient: `q=lambda^2`.

B5 scoped result:
- `F_q ~= 0.19428`;
- optimistic unmarginalized `sigma_q ~= 2.2687`;
- largest tested production point `lambda=0.30`, `q=0.09`, reaches only `0.0401 sigma` against the reference in this control.

Therefore a successful predictive relation is not evidence that the relation is currently observable.

## 2. Whitening angle is not enough

After profiling the nearest C1 smooth-w amplitude in the same ShapeFit covariance:
- whitened acute angle M07-q vs C1-epsilon: `33.724 deg`;
- orthogonal residual fraction: `0.5552`;
- `sigma_q` degrades from `2.2689` to `4.0866`;
- the largest tested `q=0.09` has only `0.0220 sigma` profiled significance.

Thus a visibly non-collinear whitened direction can still carry negligible absolute information. Future-model promotion must report both geometry and absolute covariance-weighted significance.

## 3. Orthogonal channels require representation-level robustness

Raw cross-gauge physical outputs (`P`, `d_m`, `phi`, `psi`) pass a `1e-4` paired synchronous/Newtonian regression in the tested setup, but small model/reference residuals do not.

Measured response-level cross-gauge mismatch:
- `ln P(model/ref)`: about `3.10%`;
- direct `ln|d_m_model/d_m_ref|`: about `3.10%`;
- fractional Weyl `(phi+psi)` response: about `12.9%`.

A dedicated precision-convergence run changed the `lnP` mismatch by only a factor `0.999884`, so ordinary tightening did not remove it.

Therefore an apparent orthogonal metric response cannot be counted as a clean mechanism separator until its residual representation passes gauge/frame and subtraction-floor audits.

## 4. Construction implication

The future original model should not be optimized merely for:
- formal microphysical novelty;
- a large theory-space angle;
- a successful within-family interpolation law.

It should be optimized for a response direction that simultaneously:
1. survives exact quotienting and numerical convergence;
2. survives nearest-comparator profiling;
3. survives gauge/frame representation tests;
4. carries non-negligible covariance-whitened signal;
5. predicts a prospective holdout not used in fitting.

These lessons feed DP-0812..DP-0814.

## 5. M07 stopping rule

Do not spend unlimited cycles tightening the same M07 gauge residual. M07 has already established the methodological point: the current residual representation is not sufficiently cross-gauge robust for metric-channel promotion.

Further M07 work is justified only if a genuinely different gauge-invariant observable construction is introduced. Otherwise Wave 03 should gain more information by moving to the next dark-energy family and testing whether its response geometry escapes the M07/C1 bottleneck.
