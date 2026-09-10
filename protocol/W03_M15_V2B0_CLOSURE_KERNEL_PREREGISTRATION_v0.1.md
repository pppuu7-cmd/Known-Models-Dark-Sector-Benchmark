# W03 / M15 V2b0 closure-kernel preregistration v0.1

Frozen: 2026-09-10
Status: PREREGISTERED
Family: F15/M15 generalized Chaplygin / decomposed unified dark fluid
Scientific promotion from this gate alone: **NO**

## 1. Purpose

V2a established the exact published four-component finite-alpha background and V1 established an exact alpha=0 LambdaCDM reference in pinned upstream CLASS. The remaining strict M15 blocker is the perturbation closure because arXiv:1702.00651 carries the DE comoving sound speed `c_s,Lambda^2` through Eqs. (45)-(48) but the accessible numerical description does not state the value used in the unpublished modified CLASS implementation.

V2b0 is a pre-solver algebra audit. It implements the literal published closure as a deterministic kernel on analytic smooth test histories and verifies its reference limit, derivative bookkeeping, and dependence on the hidden sound-speed coordinate before any full Einstein-Boltzmann patch is attempted.

V2b0 is **not** author-code reproduction, not an observational calculation, and cannot close K3 by itself.

## 2. Frozen source equations and conventions

Authority: `models/generalized_chaplygin/m15_v2_equation_to_class_map.md`.

Frozen Newtonian-gauge velocity map:

`theta_A_CLASS = -k^2 vhat_A_paper`

`theta_tot_CLASS = sum_A[(rho_A+p_A) theta_A] / sum_A(rho_A+p_A)`

`vhat_paper = -theta_tot_CLASS/k^2`.

Published Eq. (49):

`delta_Lambda = -(2 alpha/(3 H)) Thetahat`.

Published Eq. (50), preserved literally:

`Thetahat = (1/a) (psi' + phi' + theta_tot_CLASS)`.

Published Eq. (45), solved algebraically for `Qhat`:

`Qhat = (rho_Lambda/a) [delta_Lambda' + 3 mathcalH (c_s^2+1) delta_Lambda] - Q (psi-delta_Lambda)`.

Published Eq. (46):

`fhat = c_s^2 rho_Lambda delta_Lambda/a - Q vhat`.

The V2b0 implementation shall use cosmic `H = mathcalH/a`. No phi/psi interchange, sign repair, or replacement of Eq. (50) by a textbook expansion-scalar expression is allowed.

## 3. Prospective sound-speed bracket

The exact 2017 author numerical value remains unresolved. Therefore the only scientific question at V2b0 is sensitivity to an explicit hidden closure coordinate.

Freeze endpoints:

- `c_s,Lambda^2 = 0` — clustering endpoint;
- `c_s,Lambda^2 = 1` — luminal endpoint.

The endpoints are a **prospective sensitivity bracket**, not a claim about the unpublished author input. A later same-author dark-degeneracy line and a later gCg dark-energy analysis use the luminal choice as a standard assumption, which motivates inclusion of `1` but does not retroactively identify the 2017 value.

No fit of `c_s^2` to obtain a preferred response is authorized.

## 4. Frozen analytic test histories

Use dimensionless conformal time `x` on `[0.2, 1.0]` with 4097 equally spaced nodes.

Define smooth deterministic histories:

- `a(x) = x`;
- `H_cosmic(x) = H0 * sqrt(Omega_m/a^3 + Omega_L)` with `H0=1`, `Omega_m=0.3`, `Omega_L=0.7`;
- `mathcalH=a H_cosmic`;
- `rho_Lambda(x)=Omega_L * H_cosmic(x)^(-2 alpha)`;
- `psi(x)=2e-5 * (1 + 0.15 x + 0.03 x^2)`;
- `phi(x)=1.7e-5 * (1 - 0.08 x + 0.02 x^2)`;
- `theta_tot(x)=3e-5 * x^2 * exp(-0.4 x)`;
- `k=0.2`.

The test `Q` is not fitted. It is reconstructed from the frozen background ansatz using

`Q = d rho_Lambda/dt = H * d rho_Lambda/d ln a`

for the `w_Lambda=-1` branch.

Test alphas: `{0, -0.05, +0.05, +0.25}`. The large `+0.25` point is a stress point, not an observationally preferred value.

## 5. Derivative rule

Compute the primary analytic derivatives of the prescribed histories directly. Compute `delta_Lambda'` in two independent ways:

1. analytic product-rule derivative of Eq. (49);
2. fourth-order centered finite difference on the interior, excluding two boundary nodes.

Frozen derivative gate:

`max_symrel(deltaLambdaPrime_analytic, deltaLambdaPrime_FD4) <= 2e-7`.

A failure blocks the kernel; thresholds may not be relaxed after seeing results.

## 6. Reference/null gates

For `alpha=0`, regardless of `c_s^2`:

- `Q == 0` within `1e-14` absolute;
- `delta_Lambda == 0` within `1e-14`;
- `delta_Lambda' == 0` within `1e-14`;
- `Qhat == 0` within `1e-14`;
- the pressure part of `fhat` is zero and the full `fhat == 0` within `1e-14`;
- the M15 corrections induced by these terms therefore vanish at the kernel level.

This is a necessary regression of the V1 reference identity, not a substitute for a full CLASS alpha=0 regression in V2b1.

## 7. Sound-speed dependence gates

For every finite-alpha point, evaluate `c_s^2={0,0.5,1}` solely for an algebraic affinity test; `0.5` is diagnostic and is not promoted to a science branch.

Because Eqs. (45)-(46) are affine in `c_s^2` at fixed histories, require for both `Qhat` and `fhat`:

`max_symrel(X(cs2=0.5), 0.5*(X(0)+X(1))) <= 1e-12`.

Also require finite nonzero endpoint separation at each finite-alpha point:

`||X(1)-X(0)||_2 > 0` for at least one of `{Qhat,fhat}`.

If endpoint separation is exactly zero, the hidden sound-speed coordinate is locally irrelevant for this closure kernel and that result must be retained rather than forced to differ.

## 8. Finite/domain gates

For every case:

- every kernel array is finite on the frozen interior;
- `rho_Lambda>0`;
- no division by `k=0` or `H=0` is permitted;
- no NaN/Inf masking.

## 9. Output contract

Canonical machine result:

`models/generalized_chaplygin/M15_V2B0_CLOSURE_KERNEL_RESULT.json`

Wave mirror:

`waves/wave_03_expanded_dark_energy/M15_V2B0_CLOSURE_KERNEL_RESULT.json`

Required fields include source equations, frozen grid, alpha/sound-speed cases, derivative metrics, null metrics, affinity metrics, finite gates, and classification.

Allowed classifications:

- `M15_V2B0_CLOSURE_KERNEL_PASS`;
- `M15_V2B0_CLOSURE_KERNEL_FAIL_DERIVATIVE`;
- `M15_V2B0_CLOSURE_KERNEL_FAIL_REFERENCE`;
- `M15_V2B0_CLOSURE_KERNEL_FAIL_AFFINITY`;
- `M15_V2B0_CLOSURE_KERNEL_FAIL_DOMAIN`.

## 10. Promotion boundary and V2b1 entry condition

A V2b0 PASS authorizes implementation of V2b1, a self-consistent perturbation evolution, subject to a separate preregistration that freezes:

- the Einstein-equation feedback route;
- the exact early-time initial-condition prescription;
- an alpha=0 full-solver identity regression;
- finite-alpha convergence steps;
- the `c_s^2=0` and `1` science branches;
- multi-channel outputs and nearest-family attacks.

Ballesteros & Lesgourgues (arXiv:1004.5509) may inform the sound-speed initial-condition audit, but their non-interacting fluid attractor cannot be copied blindly into this interacting vacuum system. The interacting equations themselves must be checked in the early-time limit before V2b1 execution.

No K3/K4/K5 promotion occurs from V2b0 alone.
