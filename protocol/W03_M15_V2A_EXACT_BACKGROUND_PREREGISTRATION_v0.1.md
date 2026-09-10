# W03 M15 V2a exact four-component background preregistration v0.1

Date: 2026-09-10
Family: F15 / M15 generalized Chaplygin dark sector
Scope: w_Lambda=-1 finite-alpha background only
Scientific purpose: validate the exact four-component background branch independently of the unresolved perturbation sound-speed closure.

## Authority

Primary equations are Eqs. (8), (13)-(16), and (22)-(25) of vom Marttens et al., arXiv:1702.00651.

The authoritative numerical background is Eq. (16), not the analytic approximation Eq. (26). Eq. (26) is tested only as a comparator.

## Frozen equations

Use x=ln(a), E=H/H0 and E(0)=1 at a=1.

For w_Lambda=-1:

`dE/dx = [-3 E^2 + 3 Omega_Lambda0 E^(-2 alpha) - Omega_r0 exp(-4x)]/(2E)`.

Reconstruct

`OmegaLambda_scaled(a) = Omega_Lambda0 E^(-2 alpha)`

`OmegaC_scaled(a) = E^2 - Omega_b0 a^(-3) - Omega_r0 a^(-4) - OmegaLambda_scaled(a)`.

The dimensionless interaction diagnostic is

`Q/(H rho_crit0) = d[OmegaLambda_scaled]/dx`.

Thus positive alpha is expected to give positive Q over the expanding late-time branch, consistent with Eqs. (9)-(11): CDM loses energy and vacuum gains it.

## Frozen structural anchor

This gate is not a pointwise reproduction of the unpublished author CLASS run. To isolate equation consistency, use one explicit KMDSB structural anchor for baryons/radiation:

- `Omega_b0 = 0.049`
- `Omega_r0 = 9.0e-5`

These values are declared benchmark constants, not claimed as hidden author-code inputs.

For each paper alpha point, use the midpoint of the paper's Table III SNIa 2-sigma Omega_c0 interval:

- alpha=-0.50: Omega_c0=0.3075
- alpha=-0.25: Omega_c0=0.2745
- alpha=-0.05: Omega_c0=0.2505
- alpha=+0.05: Omega_c0=0.2385
- alpha=+0.25: Omega_c0=0.2165

Also run alpha=0 at Omega_c0=0.25 as an exact-reference control.

For every case set

`Omega_Lambda0 = 1 - Omega_b0 - Omega_r0 - Omega_c0`.

## Frozen domain and integration controls

Integrate backward from a=1 to a_min=1e-4 on a uniform x=ln(a) mesh using explicit RK4.

Run three nested resolutions:

- N=20000
- N=40000
- N=80000

At common diagnostic nodes

`a={1,0.8,0.5,0.2,0.1,0.03,0.01,0.003,0.001,0.0003,0.0001}`

compare E and reconstructed densities between N=40000 and N=80000.

Convergence PASS requires max symmetric relative difference <= 2e-7 for E and <= 2e-6 for each strictly positive reconstructed dark density on matched nodes. The N=20000 result is retained as a coarser trend control.

## Alpha=0 identity control

At alpha=0, compare the numerical Eq. (16) solution against

`E_LCDM^2 = Omega_r0 a^-4 + (Omega_b0+Omega_c0) a^-3 + Omega_Lambda0`.

PASS requires max symmetric relative difference in E <= 2e-7 over all diagnostic nodes.

## Positivity / physical-domain control

For each finite-alpha case, both reconstructed `rho_c/rho_crit0` and `rho_Lambda/rho_crit0` must remain finite and positive at every diagnostic node. A positivity failure is classified as a failure of that frozen background point/domain, not a family-wide physical falsification.

## Interaction-sign control

Evaluate `Q/(H rho_crit0)` from the exact ODE solution. Ignore alpha=0 where Q is identically zero.

At all diagnostic nodes with a>=0.01:

- alpha>0 must yield Q>0;
- alpha<0 must yield Q<0.

A sign failure stops promotion because it indicates an equation/convention implementation error or a branch pathology.

## Eq. (26) approximation audit

For each finite-alpha point compute

`E_approx^2 = [1-Omega_m0 + Omega_m0 a^(-3(1+alpha))]^(1/(1+alpha)) + Omega_r0 a^-4`,

with `Omega_m0=Omega_b0+Omega_c0`.

Record

`Deviation=(E_exact-E_approx)/E_exact`

at all diagnostic nodes and the maximum absolute deviation over:

- late domain a>=0.1;
- recombination-relevant broad domain a>=1e-3;
- full frozen domain a>=1e-4.

No post-hoc pass threshold is assigned to Eq. (26); this part is descriptive because the paper itself treats the formula as an approximation whose quality depends on alpha and matter density.

## Allowed classifications

- `M15_V2A_EXACT_BACKGROUND_PASS`
- `M15_V2A_REFERENCE_FAIL`
- `M15_V2A_CONVERGENCE_FAIL`
- `M15_V2A_PHYSICAL_DOMAIN_FAIL_WITH_SCOPE`
- `M15_V2A_INTERACTION_SIGN_FAIL`
- `M15_V2A_NUMERICAL_ERROR`

A V2a PASS validates the published finite-alpha background construction only. It does not resolve the perturbation sound-speed provenance gap and does not promote M15 K3-K7.

## Promotion rule

If V2a passes, the independent reproduction has a validated alpha=0 reference and a numerically stable finite-alpha background branch. The next perturbation step must either source the author numerical value of c_s,Lambda^2 or preregister a separate closure-sensitivity study. No hidden solver default is authorized.
