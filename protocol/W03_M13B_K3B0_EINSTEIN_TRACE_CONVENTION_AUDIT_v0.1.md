# W03 M13b K3B0 Einstein-trace convention audit v0.1

Date frozen: 2026-09-13  
Target: F13/M13b independent perturbation verification  
Scope: published metric/Einstein-equation convention integrity before dynamical K3B embedding  
Physical falsification: **FORBIDDEN FROM THIS AUDIT**

## Trigger

K3A independently verified the canonical/phantom field stress-energy signs, background continuity, potential derivatives, direct perturbed Klein–Gordon structure and regularity of the direct field variables at the effective `w=-1` crossing.

Before coupling those field equations to an independently implemented metric evolution, the final Goh–Taylor 2026 article must be checked for a convention ambiguity in its printed Einstein trace equation. The source code used by the authors is not publicly pinned, so KMDSB cannot infer whether a printed expression, a convention transformation, or the actual hidden implementation is authoritative.

## Frozen published forms

The final article states the conformal Newtonian metric

`ds^2 = a^2[(1+2 Psi)d tau^2 - (1-2 Phi) dx^i dx_i]`

with no anisotropic stress `Psi=Phi`.

Its printed equations are frozen for this audit as:

- published (00): `k^2 Phi - 3 Hc(Phi' + Hc Psi) = 4 pi G a^2 delta_rho`;
- published (ij): `Phi'' + 3 Hc Phi' + (2 Hc' - Hc^2) Phi = (4/3) pi G a^2 delta_p`.

The same paper subsequently defines the scalar-field `delta_p_phi` and `delta_p_psi` as ordinary physical pressure perturbations.

## Independent GR comparator

For the same `(+---)` Newtonian-gauge metric and zero anisotropic stress, standard linearized-GR references give

- coordinate-space (00): `nabla^2 Phi - 3 Hc(Phi' + Hc Phi) = 4 pi G a^2 delta_rho`;
- trace (ij): `Phi'' + 3 Hc Phi' + (2 Hc' + Hc^2) Phi = 4 pi G a^2 delta_p`.

Using the Fourier convention `nabla^2 -> -k^2`, sign placement in a displayed Fourier-space (00) equation can depend on the definition of the Fourier-space density source. Therefore this audit MUST NOT classify Eq. (13) as inconsistent merely from the displayed `k^2` sign. The trace equation is instead tested by a convention-insensitive matter-era limit.

## Frozen matter-era test

Take a flat pressureless matter-dominated GR background:

- `a(tau) proportional to tau^2`;
- `Hc = 2/tau`;
- `Hc' = -2/tau^2`;
- `delta_p = 0`;
- the regular growing adiabatic mode has constant nonzero `Phi`, so `Phi'=Phi''=0`.

Then:

- standard trace coefficient: `2 Hc' + Hc^2 = 0`, hence the trace equation admits constant `Phi` exactly;
- literal published trace coefficient: `2 Hc' - Hc^2 = -8/tau^2`, hence the literal printed equation leaves residual `-8 Phi/tau^2` for any finite nonzero constant `Phi`.

This test is frozen before execution.

## Additional normalization audit

The verifier must also record that the literal published RHS coefficient is one third of the standard physical-pressure trace coefficient. It must not guess whether this arises from a trace-index normalization, typography, or implementation convention. Because the later field equations label `delta_p_phi` and `delta_p_psi` as physical pressure perturbations, the factor cannot be silently absorbed in the independent implementation without explicit authority.

## Frozen classifications

If the standard trace passes the matter-era constant-potential check while the literal published trace fails it, and the coefficient/RHS differences are reproduced exactly, classify:

`M13B_K3B0_PUBLISHED_EINSTEIN_TRACE_FORM_NOT_LITERAL_IMPLEMENTATION_AUTHORITY`

Interpretation:

- a printed/convention ambiguity is established for strict reproduction;
- this is **not** a physical failure of the two-field quintom family;
- this is **not** evidence that the authors' numerical code used the literal printed Eq. (15);
- the nonpublic original code remains provenance blocked;
- independent K3B dynamics may proceed only with an explicitly independent standard-GR Einstein closure plus the separately verified field equations, never as an author-code reproduction.

If the frozen matter-era calculation does not reproduce the stated distinction, classify:

`M13B_K3B0_TRACE_AUDIT_NOT_ESTABLISHED`

All outcomes retain `K3=PARTIAL` at most, `K4_promoted=false`, `K5_promoted=false`, and `physical_falsification=false`.

## Next authorized gate

Only after the expected audit outcome may `K3B1_INDEPENDENT_STANDARD_GR_TWO_FIELD_DYNAMICAL_EMBEDDING` be preregistered. K3B1 must explicitly cite this convention boundary and must not use the literal printed trace Eq. (15) as numerical authority without a newly released source-code or author clarification.
