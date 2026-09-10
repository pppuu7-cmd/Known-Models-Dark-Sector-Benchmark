# W03 / M15 V2b0 closure-kernel preregistration v0.2

Frozen: 2026-09-10, **before any V2b0 numerical execution**
Status: PREREGISTERED
Supersedes: `W03_M15_V2B0_CLOSURE_KERNEL_PREREGISTRATION_v0.1.md`
Reason for supersession: v0.1 simultaneously called its grid variable conformal time, set `a(x)=x`, and imposed an independent LambdaCDM `H(a)`. Those choices do not obey `a'=a^2 H`. The inconsistency was identified before a verifier or workflow was committed and before any result existed. v0.2 replaces the grid coordinate by `x=ln a` and maps derivatives to conformal time explicitly.
Scientific promotion from this gate alone: **NO**

## 1. Purpose

V2a established the exact published four-component finite-alpha background and V1 established an exact alpha=0 LambdaCDM reference in pinned upstream CLASS. The remaining strict M15 blocker is perturbation closure because arXiv:1702.00651 carries the DE comoving sound speed `c_s,Lambda^2` through Eqs. (45)-(48) but the accessible numerical description does not state the value used in the unpublished modified CLASS implementation.

V2b0 is a pre-solver algebra audit. It implements the literal published closure as a deterministic kernel on analytic smooth test histories and verifies reference behavior, derivative bookkeeping, and dependence on the hidden sound-speed coordinate before a full Einstein-Boltzmann patch is attempted.

V2b0 is **not** author-code reproduction, not an observational calculation, and cannot close K3 by itself.

## 2. Frozen source equations and conventions

Authority: `models/generalized_chaplygin/m15_v2_equation_to_class_map.md`.

Frozen Newtonian-gauge map:

`theta_A_CLASS = -k^2 vhat_A_paper`

`theta_tot_CLASS = sum_A[(rho_A+p_A) theta_A] / sum_A(rho_A+p_A)`

`vhat_paper = -theta_tot_CLASS/k^2`.

Published Eq. (49):

`delta_Lambda = -(2 alpha/(3 H)) Thetahat`.

Published Eq. (50), preserved literally:

`Thetahat = (1/a) (psi' + phi' + theta_tot_CLASS)`.

Published Eq. (45), solved for `Qhat`:

`Qhat = (rho_Lambda/a) [delta_Lambda' + 3 mathcalH (c_s^2+1) delta_Lambda] - Q (psi-delta_Lambda)`.

Published Eq. (46):

`fhat = c_s^2 rho_Lambda delta_Lambda/a - Q vhat`.

Cosmic `H` and conformal `mathcalH=aH` are distinct. No phi/psi interchange, sign repair, or replacement of Eq. (50) is allowed.

## 3. Prospective sound-speed bracket

The exact 2017 author numerical value remains unresolved. Freeze science endpoints only as an explicit sensitivity bracket:

- `c_s,Lambda^2=0`;
- `c_s,Lambda^2=1`.

A diagnostic midpoint `0.5` is used only to test the algebraic affine dependence and is not a promoted branch.

The luminal endpoint is scientifically motivated by later work in the same author line and by later gCg dark-energy work that explicitly fixes the DE rest-frame sound speed to unity. This does **not** identify the unpublished 2017 input.

No fit of `c_s^2` is authorized.

## 4. Frozen analytic coordinate and histories

Independent variable:

`x = ln a`, equally spaced on `[ln(0.2), 0]`, `N=4097`.

Then:

`a=exp(x)`

`H(x)=H0 sqrt(Omega_m exp(-3x)+Omega_L)`

with `H0=1`, `Omega_m=0.3`, `Omega_L=0.7`, and

`mathcalH=aH`.

For every scalar history `Y(x)`, conformal derivative is defined by

`Y' = mathcalH dY/dx`.

Synthetic deterministic perturbation histories:

- `psi(x)=2e-5 * (1 + 0.15 x + 0.03 x^2)`;
- `phi(x)=1.7e-5 * (1 - 0.08 x + 0.02 x^2)`;
- `theta_tot(x)=3e-5 * mathcalH * exp(0.4 x) * (1+0.1 x)`;
- `k=0.2`.

These are algebra-test histories only; they are not claimed to satisfy Einstein equations.

Dark-energy background test history follows the published ansatz:

`rho_Lambda(x)=Omega_L * H(x)^(-2 alpha)`.

For `w_Lambda=-1`, reconstruct

`Q = d rho_Lambda/dt = H d rho_Lambda/dx`.

Test alphas: `{0,-0.05,+0.05,+0.25}`. The `+0.25` point is a stress point, not an observational preference.

## 5. Derivative rule

Build `Thetahat` using analytic `dpsi/dx` and `dphi/dx`, converted to conformal derivatives with `mathcalH`.

Compute `delta_Lambda'` independently in two ways:

1. analytic differentiation with respect to `x` followed by multiplication by `mathcalH`;
2. fourth-order centered finite difference of `delta_Lambda(x)` with respect to `x`, followed by multiplication by `mathcalH`.

Compare only nodes `i=2...N-3`.

Frozen derivative gate:

`max_symrel(deltaLambdaPrime_analytic,deltaLambdaPrime_FD4) <= 2e-7`.

No post-result threshold relaxation.

## 6. Reference/null gates

At `alpha=0`, for every `c_s^2 in {0,0.5,1}` require:

- `maxabs(Q) <= 1e-14`;
- `maxabs(delta_Lambda) <= 1e-14`;
- `maxabs(delta_Lambda') <= 1e-14`;
- `maxabs(Qhat) <= 1e-14`;
- `maxabs(fhat) <= 1e-14`.

This is a necessary kernel-level reference regression. V2b1 must separately recover the full V1 solver identity.

## 7. Sound-speed dependence gates

At every finite-alpha point evaluate `c_s^2={0,0.5,1}`.

At fixed histories Eqs. (45)-(46) are affine in `c_s^2`. For both `Qhat` and `fhat` require

`max_symrel(X(0.5),0.5*(X(0)+X(1))) <= 1e-12`.

Also record endpoint L2 separation for both quantities and require at least one strictly positive endpoint separation at every finite-alpha point. A true zero separation must be reported rather than forced.

## 8. Finite/domain gates

For every case and comparison interior:

- all arrays finite;
- `rho_Lambda>0`;
- `H>0`, `mathcalH>0`, `k>0`;
- no NaN/Inf masking.

## 9. Output contract

Canonical result:
`models/generalized_chaplygin/M15_V2B0_CLOSURE_KERNEL_RESULT.json`

Wave mirror:
`waves/wave_03_expanded_dark_energy/M15_V2B0_CLOSURE_KERNEL_RESULT.json`

Allowed classifications:

- `M15_V2B0_CLOSURE_KERNEL_PASS`;
- `M15_V2B0_CLOSURE_KERNEL_FAIL_DERIVATIVE`;
- `M15_V2B0_CLOSURE_KERNEL_FAIL_REFERENCE`;
- `M15_V2B0_CLOSURE_KERNEL_FAIL_AFFINITY`;
- `M15_V2B0_CLOSURE_KERNEL_FAIL_DOMAIN`.

## 10. Promotion boundary and V2b1 entry condition

A PASS authorizes a separately preregistered self-consistent V2b1 perturbation evolution. V2b1 must freeze Einstein feedback, early-time ICs, a full alpha=0 solver identity regression, finite-alpha step convergence, both sound-speed endpoints, multichannel outputs, and nearest-family attacks.

Ballesteros & Lesgourgues (arXiv:1004.5509) provide general sound-speed attractor/initial-condition guidance for a non-interacting fluid. Their formulae cannot be copied blindly into this interacting vacuum system; V2b1 must re-check the interacting early-time limit.

No K3/K4/K5 promotion occurs from V2b0 alone.
