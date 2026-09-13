# W03 M13b independent two-field perturbation K3A equation-closure preregistration v0.1

Date frozen: 2026-09-13  
Target: F13/M13b true two-field quintom  
Implementation provenance: **independent KMDSB verification implementation**  
Original Goh–Taylor provider claim: **FORBIDDEN**

## Trigger

The renewed public-provider reconnaissance found no immutable public source for the 2026 Goh–Taylor modified Boltzmann implementation and no alternative public source-complete two-field perturbation provider. Existing public `Quintom.py` hits are background-only. Repository recovery rules explicitly authorize an independently labelled verification implementation from published covariant equations when this provenance condition persists.

## Scientific authority

Equation authority is Goh & Taylor 2026, arXiv:2606.27049 / MNRAS 551 stag1403, final title `Quintom model perturbations and constraints with observational data`.

The verifier freezes the following published structure.

### Background

For canonical `phi`:

- `rho_phi = phi_dot^2/2 + V(phi)`
- `p_phi   = phi_dot^2/2 - V(phi)`
- `phi_ddot + 3 H phi_dot + V_phi = 0`

For phantom `psi`:

- `rho_psi = -psi_dot^2/2 + V(psi)`
- `p_psi   = -psi_dot^2/2 - V(psi)`
- `psi_ddot + 3 H psi_dot - V_psi = 0`

The common potential is

`V(x) = V0 [tanh(s(1-x)) + 1]`.

Therefore the independently derived analytic derivatives frozen before execution are

- `V_x  = -V0 s sech^2(s(1-x))`
- `V_xx = -2 V0 s^2 sech^2(s(1-x)) tanh(s(1-x))`.

### Linear scalar-field perturbations in conformal Newtonian gauge

Metric convention:

`ds^2 = a^2[(1+2 Psi)d tau^2 - (1-2 Phi) dx^i dx_i]`, with the published no-anisotropic-stress scope `Psi=Phi`.

Define

`A_phi = (phi' delta_phi' - phi'^2 Psi)/a^2`

`A_psi = (psi' delta_psi' - psi'^2 Psi)/a^2`.

Published field stress-energy perturbations:

- `delta_rho_phi =  A_phi + V_phi delta_phi`
- `delta_p_phi   =  A_phi - V_phi delta_phi`
- `delta_rho_psi = -A_psi + V_psi delta_psi`
- `delta_p_psi   = -A_psi - V_psi delta_psi`

Published perturbed Klein–Gordon equations:

- `delta_phi'' + 2 Hc delta_phi' + (k^2 + a^2 V_phiphi) delta_phi - 3 Phi' phi' = 0`
- `delta_psi'' + 2 Hc delta_psi' + (k^2 - a^2 V_psipsi) delta_psi - 3 Phi' psi' = 0`

where `Hc=a'/a`.

## Frozen K3A checks

The executable verifier must perform all of the following without fitting or tuning.

1. **Potential derivative identity**: symbolic derivatives of the frozen potential must equal the frozen `V_x` and `V_xx` exactly.
2. **Canonical background continuity**: after substituting the conformal-time canonical KG equation `phi'' + 2 Hc phi' + a^2 V_phi = 0`, verify exactly `rho_phi' + 3 Hc (rho_phi+p_phi)=0`.
3. **Phantom background continuity**: after substituting `psi'' + 2 Hc psi' - a^2 V_psi = 0`, verify exactly `rho_psi' + 3 Hc (rho_psi+p_psi)=0`.
4. **Perturbed stress-energy sign identities**:
   - `delta_rho_phi + delta_p_phi = 2 A_phi`;
   - `delta_rho_phi - delta_p_phi = 2 V_phi delta_phi`;
   - `delta_rho_psi + delta_p_psi = -2 A_psi`;
   - `delta_rho_psi - delta_p_psi = 2 V_psi delta_psi`.
5. **Crossing identity**: verify `rho_DE+p_DE = (phi'^2-psi'^2)/a^2`, so a nontrivial effective `w_DE=-1` crossing occurs at equal kinetic magnitudes, not by forcing either field equation singular.
6. **Direct-variable regularity at crossing**: substitute a finite nonzero crossing test state `phi'=psi' != 0` and finite `a,Hc,k,V_xx,Phi'`; every coefficient/source of both direct perturbed KG equations must remain finite and contain no division by `phi'^2-psi'^2`.
7. **Effective-fluid warning**: verify that the published effective velocity combination `theta_DE = sum_i[(rho_i+p_i)theta_i] / sum_i(rho_i+p_i)` has a vanishing denominator at the crossing state. This is a required diagnostic, not a test failure. It establishes why the independent implementation must integrate field perturbations directly through crossing instead of using `theta_DE` as a fundamental state variable.
8. **No hidden coupling**: the K3A equation manifest must contain no direct `delta_psi` term in the `delta_phi` KG equation and no direct `delta_phi` term in the `delta_psi` KG equation under the published minimal-coupling scope. Metric coupling is allowed and required later.

## Frozen classifications

If all required identities and the expected effective-fluid warning are reproduced:

`M13B_INDEPENDENT_K3A_EQUATION_CLOSURE_PASS_WITH_SCOPE`

This may move the independent-verification contribution to K3 from `BLOCKED` to `PARTIAL` **only for equation/sign/continuity closure**. It does not establish a self-consistent Einstein–Boltzmann realization and cannot make K3 `PASS`.

If an equation/sign/continuity identity fails:

`M13B_INDEPENDENT_K3A_EQUATION_CLOSURE_NOT_ESTABLISHED`

If the checker cannot execute or the frozen authority manifest is internally inconsistent:

`M13B_INDEPENDENT_K3A_VERIFIER_BLOCKED`

All outcomes require:

- `K4_promoted=false`
- `K5_promoted=false`
- `physical_falsification=false`
- `original_provider_reproduced=false`.

## Post-K3A authorization

Only a K3A pass authorizes preregistration of K3B: an independently implemented metric/Einstein plus two-field perturbation evolution with a pinned numerical base and explicit comparison to the published scale/redshift behaviour. No K4/K5 grid is authorized before K3B establishes a finite same-realization background+perturbation solution through the crossing.
