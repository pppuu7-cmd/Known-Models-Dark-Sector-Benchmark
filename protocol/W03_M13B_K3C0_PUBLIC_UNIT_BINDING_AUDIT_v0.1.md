# W03 M13b K3C0 public unit-binding audit v0.1

Date frozen: 2026-09-13  
Target: F13/M13b true two-field quintom  
Scope: public numerical-label to physical-cosmology unit binding before any cosmology-scale independent embedding  
Physical falsification: **FORBIDDEN FROM THIS AUDIT**

## Trigger

M13b K3B2 established a local dimensionless independent standard-GR two-field perturbation realization through an exact transverse `w=-1` crossing. The next authorized scientific step is a cosmology-scale independent Einstein/Boltzmann realization.

That step cannot lawfully import the published `V0`, field values and velocities until their physical normalization is unambiguous. The public 2025 Goh–Taylor benchmark labels `m_P` as the reduced Planck mass and quotes both ordinary cosmological parameters and scalar-potential parameters in powers of `m_P`. A literal binding must therefore be checked before any numerical reuse or rescaling.

This audit is a normalization/provenance gate. It does not test whether the quintom mechanism is physically viable and does not infer what the unavailable author code actually used internally.

## Frozen public authority

Authority: L. W. K. Goh & A. N. Taylor, `Phantom crossing with quintom models`, MNRAS 544 (2025) 3142.

The exact public tanh benchmark is frozen as:

- `z_ini = 1e20`;
- `Omega_m0 = 0.3114`;
- `Omega_r0 = 9.23e-5`;
- `H0 = 67.15 km s^-1 Mpc^-1`;
- `m_P` explicitly defined as the reduced Planck mass `1/sqrt(8 pi G)`;
- `V(x)=V0[tanh(s(1-x))+1]`;
- `phi_ini = 0.92 m_P`;
- `psi_ini = 1.02 m_P`;
- `dot_phi_ini = dot_psi_ini = 1e-5 m_P^2`;
- `V0 = 0.91e-8 m_P^4`;
- `s = 29 m_P^-1`.

The same public discussion states that the fields are frozen until approximately `z>5`, when dark energy begins to dominate. Therefore a literal Planck-unit reading predicts that around `z=5` the field positions and potential energy should still be close to the quoted initial plateau values, while the standard matter/radiation densities are fixed by `H0`, `Omega_m0`, and `Omega_r0`.

## Frozen constants

Use exactly:

- `c = 299792458 m/s`;
- `G = 6.67430e-11 m^3 kg^-1 s^-2`;
- `hbar = 1.054571817e-34 J s`;
- `Mpc = 3.0856775814913673e22 m`.

No fitted or inferred constant is permitted.

## Frozen literal-Planck calculation

Define reduced Planck mass/energy in SI:

`M_P_mass = sqrt(hbar*c/(8*pi*G))`

`M_P_energy = M_P_mass*c^2`.

Convert the measured Hubble constant to the reduced-Planck dimensionless ratio

`h_P = hbar*H0 / M_P_energy`.

Then, under a literal physical Planck-unit reading,

`rho_crit,0 / M_P^4 = 3 h_P^2`.

Flat-reference dark-energy scale:

`Omega_DE,ref = 1 - Omega_m0 - Omega_r0`

`rho_DE,ref / M_P^4 = 3 Omega_DE,ref h_P^2`.

Matter+radiation density at the frozen comparison redshift `z*=5`:

`rho_mr(z*) / M_P^4 = 3 h_P^2 [Omega_m0(1+z*)^3 + Omega_r0(1+z*)^4]`.

Because the public statement says the fields are still frozen until approximately this epoch, evaluate the quoted tanh potential at the published initial field positions:

`V_literal(z*)/M_P^4 = V0 * {tanh[s(1-phi_ini)]+1 + tanh[s(1-psi_ini)]+1}`.

Here `phi_ini` and `psi_ini` are inserted in units of `M_P`, while `s` is in `M_P^-1`, so each tanh argument is dimensionless.

The quoted initial kinetic contributions cancel exactly in `rho_phi+rho_psi` because `dot_phi_ini=dot_psi_ini`, and the public frozen-field statement makes a huge kinetic cancellation at `z*=5` unavailable as an unregistered rescue.

## Frozen checks

The executable audit must report all intermediate quantities and verify:

1. every conversion/result is finite and positive where expected;
2. the quoted initial kinetic contribution to the combined dark-energy density cancels exactly under the canonical/phantom signs;
3. the literal tanh potential sum at the quoted frozen positions is positive;
4. `R5 = V_literal(z=5)/rho_mr(z=5)`;
5. `R0 = V_literal/rho_DE,ref`;
6. if both `R5 > 1e50` and `R0 > 1e50`, the literal Planck-unit reading is incompatible with using the quoted labels directly in an ordinary late-time cosmology with the simultaneously quoted `H0/Omega` values and the stated frozen-through-z~5 behavior;
7. report the multiplicative scales `S5=rho_mr(z=5)/V_literal` and `S0=rho_DE,ref/V_literal` only as the magnitudes of missing normalization that would be required for comparability. These factors MUST NOT be adopted as a model definition or tuned correction.

The `1e50` threshold is prospectively frozen and deliberately many orders of magnitude weaker than the expected discrepancy. It is a normalization diagnostic, not a precision threshold.

## Frozen classifications

If checks 1–7 pass and the literal ratios exceed the frozen threshold, classify:

`M13B_K3C0_PUBLIC_UNIT_BINDING_NOT_ESTABLISHED_LITERAL_PLANCK_READING_INCONSISTENT`

Interpretation:

- the public numerical labels cannot be inserted literally into an independent physical cosmology using the stated reduced-Planck definition and the quoted Hubble/density parameters;
- at least one undisclosed code normalization, rescaling convention, table/unit convention, or correction is required before published parameter values can be reproduced independently;
- the audit does **not** determine which explanation is correct;
- the audit does **not** establish an error in the unavailable author implementation;
- the audit does **not** falsify the quintom mechanism;
- no guessed rescale may be promoted to scientific authority.

If the literal ratios do not exceed the threshold or an algebraic conversion fails, classify:

`M13B_K3C0_PUBLIC_UNIT_BINDING_AUDIT_NOT_ESTABLISHED`.

All outcomes retain:

- `K3` at `PARTIAL` at most;
- `K4_promoted=false`;
- `K5_promoted=false`;
- `physical_falsification=false`;
- `original_provider_reproduced=false`.

## Next authorized action after the expected blocker

If the expected unit-binding blocker is confirmed, two paths are allowed:

1. obtain an author/source-code normalization map or another public immutable source that explicitly binds `V0`, fields, time/Hubble units and CLASS variables; or
2. construct a separately preregistered **fully independent dimensionless cosmology-scale benchmark** with an explicit internal normalization chosen from first principles/closure conditions. Such a benchmark may test mechanism consistency, but it MUST NOT claim numerical reproduction of Goh–Taylor Table/Figure parameters until a public unit map is established.
