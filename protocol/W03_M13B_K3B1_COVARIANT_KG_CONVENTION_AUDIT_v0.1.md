# W03 M13b K3B1 covariant perturbed-KG convention audit v0.1

Date frozen: 2026-09-13  
Target: F13/M13b true two-field quintom  
Scope: equation-authority audit before independent dynamical embedding  
Physical falsification: **FORBIDDEN FROM THIS AUDIT**

## Trigger

K3A verified internal algebraic identities of the field stress-energy expressions and the literal perturbed field equations reported in Goh–Taylor 2026. K3B0 then established that the literal printed Einstein trace equation cannot be adopted as independent numerical authority under the stated Newtonian-gauge/physical-pressure interpretation.

A second authority check is required before numerical embedding because the printed perturbed Klein–Gordon equations must also be compared with the equation obtained by perturbing the covariant scalar equation in the same metric convention.

## Frozen metric and background equations

Metric:

`ds^2 = a^2[(1+2 Phi)d tau^2 - (1-2 Phi) dx^i dx_i]`

with zero anisotropic stress, so the two Newtonian potentials are equal.

Background equations:

- canonical: `phi'' + 2 Hc phi' + a^2 V_phi = 0`;
- phantom: `psi'' + 2 Hc psi' - a^2 V_psi = 0`.

## Frozen covariant perturbation comparator

For a minimally coupled scalar whose background equation is

`chi'' + 2 Hc chi' + sigma a^2 V_chi = 0`,

where `sigma=+1` for the canonical field and `sigma=-1` for the phantom field, the Newtonian-gauge perturbation equation obtained by linearizing the covariant field equation is frozen as

`delta_chi'' + 2 Hc delta_chi' + (k^2 + sigma a^2 V_chichi) delta_chi - 4 chi' Phi' + 2 sigma a^2 V_chi Phi = 0`.

Thus:

canonical comparator:

`delta_phi'' + 2 Hc delta_phi' + (k^2+a^2 V_phiphi)delta_phi -4 phi'Phi' +2a^2 V_phi Phi = 0`;

phantom comparator:

`delta_psi'' + 2 Hc delta_psi' + (k^2-a^2 V_psipsi)delta_psi -4 psi'Phi' -2a^2 V_psi Phi = 0`.

This comparator is the standard minimally coupled Newtonian-gauge scalar perturbation equation and is independent of the unavailable author implementation.

## Literal published forms under audit

The final article prints

- `delta_phi'' + 2 Hc delta_phi' + (k^2+a^2V_phiphi)delta_phi -3 Phi' phi' = 0`;
- `delta_psi'' + 2 Hc delta_psi' + (k^2-a^2V_psipsi)delta_psi -3 Phi' psi' = 0`.

## Frozen checks

The executable audit must verify symbolically:

1. canonical literal-minus-covariant difference is `phi' Phi' - 2 a^2 V_phi Phi`;
2. phantom literal-minus-covariant difference is `psi' Phi' + 2 a^2 V_psi Phi`;
3. neither difference vanishes identically for independent finite `Phi`, `Phi'`, field velocity and potential slope;
4. the two expressions coincide in the restricted special case `Phi=0` and `Phi'=0`, showing that background/no-metric limits do not diagnose the discrepancy;
5. the canonical covariant comparator reproduces the established Newtonian-gauge source structure `4 phi' Phi' - 2 a^2 V_phi Phi` when written with sources on the RHS;
6. the phantom comparator follows from the same covariant formula under `sigma=-1`, preserving the phantom sign in both `V_psipsi` and the metric-potential source term.

No numerical cosmological parameter or observational quantity enters this audit.

## Frozen classification

If all six checks pass, classify

`M13B_K3B1_PUBLISHED_PERTURBED_KG_NOT_LITERAL_COVARIANT_IMPLEMENTATION_AUTHORITY`.

Interpretation:

- the printed Eq. (21)/(24) cannot be silently used as the field equations of an independent standard Newtonian-gauge implementation;
- this does **not** show that the authors' nonpublic numerical implementation used the literal printed form;
- this does **not** falsify the quintom mechanism;
- the independent KMDSB dynamical implementation must use the covariantly derived standard-GR field equations and must be labelled independent verification;
- published figures may be comparison targets only, not proof of equation-level reproduction.

If any frozen symbolic relation is not reproduced, classify

`M13B_K3B1_COVARIANT_KG_AUDIT_NOT_ESTABLISHED`.

All outcomes retain canonical K3 at `PARTIAL` at most, K4/K5 unpromoted, and `physical_falsification=false`.

## Next gate

Only the expected PASS classification authorizes `K3B2_INDEPENDENT_STANDARD_GR_TWO_FIELD_DYNAMICAL_EMBEDDING`, using the standard Einstein closure from K3B0 and the covariant field perturbation equations defined here.
