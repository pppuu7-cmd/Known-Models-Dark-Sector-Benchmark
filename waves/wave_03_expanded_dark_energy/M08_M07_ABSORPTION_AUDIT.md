# W03 M08 -> M07 absorption audit

Date: 2026-09-09  
Status: **PASS_WITH_SCOPE / ADVERSARIAL ABSORPTION**

## Question frozen before M08 outputs

Can the two-dimensional CPL local manifold

`w(a)=w0+wa(1-a)`

absorb the M07 canonical-quintessence local `q=lambda^2` response across the same low-k matter and background-expansion blocks using **one shared parameter vector**?

Independent fits in P and H were forbidden.

## M08 local-basis authority

Corrected M08 Actions run: `34394929596`  
Head: `a3bb13aab2f181fed31882d31f819c9d0b0a7a36`  
Artifact digest: `sha256:561bf0abc6b9247fe9bd517c142eeac5f96c677eab430993bd6cb1473e3a6a97`  
Pinned CLASS: `e85808324f51fc694d12e3ed7439552a3c3f9540`.

The initial run `34391852165` remains preserved as an implementation/configuration failure caused by simultaneously specifying `Omega_Lambda` and `Omega_fld`; it is not scientific evidence against CPL.

## Local CPL geometry

Central step: `1e-3` in both `epsilon0=1+w0` and `wa`.

Reference self-floor:
- `max_abs_lnP=0`;
- `max_abs_lnH=0`.

Combined P+H local directions:
- angle `9.1790225 deg`;
- singular values `{1.8829717593, 0.0945281863}`;
- `sigma2/sigma1 = 0.0502016`.

Thus the nominally two-parameter CPL manifold is locally strongly anisotropic and almost one-dimensional in this response block. Parameter count is not response rank.

Central nonlinearity ratios are all small at the frozen step:
- epsilon0 P `1.3332e-3`;
- epsilon0 H `7.7704e-4`;
- wa P `7.1553e-4`;
- wa H `3.4394e-4`.

This is sufficient for the first local linear absorption test; it is not a global CPL statement.

## M07 target

Target is the controlled M07 local quotient direction

`dr/dq`, `q=lambda^2`,

from `M07_LOCAL_Q_DIRECTION.json`.

## Shared two-parameter fit

Solve

`J_CPL c ~= r_M07`

on one concatenated vector containing the 35 low-k `lnP` coordinates followed by the 7 `lnH` coordinates.

Best coefficients per unit M07 q:

- `epsilon0/q = 0.1406534871`;
- `wa/q = -0.2006790927`.

Residual fractions after this **single shared** fit:

- combined P+H: `0.01107468` = **1.107%**;
- P block: `0.00864187` = **0.864%**;
- H block: `0.01992933` = **1.993%**.

For comparison, the same-solver constant-w-like `epsilon0` direction alone gives:

- combined: `0.15819789` = **15.820%**;
- P: `0.12063934` = **12.064%**;
- H: `0.29148838` = **29.149%**.

Therefore adding the CPL time-dependent direction improves the residual by factors:

- combined: `14.28x`;
- P: `13.96x`;
- H: `14.63x`.

## Physical scale of the local mapping

For the M07 production endpoint `lambda=0.30`, `q=0.09`, the local CPL mapping is only

- `epsilon0 ~= 0.01266`, hence `w0 ~= -0.98734`;
- `wa ~= -0.01806`.

For the prospective M07 holdout `lambda=0.225`, `q=0.050625`:

- `w0 ~= -0.99288`;
- `wa ~= -0.01016`.

These examples show the absorption does not require an extreme local CPL excursion. They are linear-map illustrations, not global finite-parameter validation.

## Classification

`CPL_ABSORBS_M07_CROSSCHANNEL_SEPARATOR_WITH_SCOPE`.

This is a **negative result for M07 mechanism-level novelty**, not a failure of M07 as a mathematically controlled or within-family predictive model.

M07 still has:
- a clean LambdaCDM limit;
- controlled local `q=lambda^2` geometry;
- level-1 prospective within-family holdout support.

But its previously identified P/H separation from constant-w C1 is not robust against the stronger time-dependent smooth-DE comparator.

## B7 implication

The M07 P/H separator must not be promoted as quotient-surviving mechanism novelty. B7 remains at most `PARTIAL` until a response survives:

1. a flexible smooth-DE family span such as CPL;
2. modified-gravity alternatives;
3. numerical gauge/subtraction controls;
4. a valid common observation operator/covariance projection under AD-002.

## Methodology consequence for the future original model

Nearest-comparator attack must target not only one representative ray but the **implemented local span/manifold of the nearest family**. A new model that is separated from constant-w but lies almost entirely inside the two-dimensional CPL span has not generated a genuinely new observable direction.

The useful object is therefore the residual after profiling the comparator family manifold, not the angle to one hand-picked comparator vector.

## Anti-overclaim

- No observational discrimination is claimed; this audit is unwhitened theory-response geometry.
- CPL absorption does not prove CPL is the physical explanation of dark energy.
- The result is local around LambdaCDM and does not establish global M07/CPL equivalence.
- Observation-space cross-family promotion must obey DSIR authority overlay `864952e...`: one exact frozen operator, coordinate vector and covariance for both families.
