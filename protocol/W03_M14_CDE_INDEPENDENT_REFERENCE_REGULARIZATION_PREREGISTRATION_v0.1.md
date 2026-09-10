# W03 M14 independent CDE exact-reference regularization preregistration v0.1

Date: 2026-09-10
Upstream source: `LisaGoh/CDE@b85a675af7544a5183e402964550811aa805b698`
Status: independent KMDSB verification layer; **not** the untouched author provider

## Motivation frozen before execution

The untouched author provider has now established:

- K0 execution PASS on the committed nonzero-coupling workload;
- published/source equation agreement for the coupled background and synchronous perturbation system;
- a complete exact beta=0 background table satisfying the preregistered rigid-vacuum/CDM invariants;
- exact beta=0 + exact-zero scalar IC full perturbation execution fails with a singular-matrix diagnostic;
- beta=0 + committed tiny scalar seed executes the full forward model;
- the tiny-seed raw perturbation diagnostic contains nonfinite `theta_scf`, while physical spectra still execute.

Source audit identifies two explicitly removable/degenerate numerical forms near the rigid-vacuum null:

1. scalar perturbation derivative-coupling term evaluates a factor proportional to `beta_z/phi_prime_scf`; for `beta_z==0` the physical term is exactly zero but literal evaluation can become `0/0`;
2. scalar velocity diagnostic divides momentum density by `rho_scf+p_scf`; for an exact rigid vacuum both numerator and denominator vanish, while the physically relevant momentum density itself is zero.

## Frozen source transformations

Create a separate patched verification copy of the exact upstream commit. No upstream commit is altered.

### R1 — derivative-coupling removable zero

In the scalar perturbation RHS only, replace literal evaluation of the `beta_prime ... / phi_prime_scf` term by an exact branch:

- if `beta_prime == 0.0`, contribution = exactly `0.0`;
- otherwise evaluate the original expression unchanged.

No epsilon or near-zero threshold is allowed.

### R2 — rigid-vacuum scalar velocity convention

At every source/output location that computes

`theta_scf = rho_plus_p_theta_scf / (rho_scf+p_scf)`,

use an exact branch:

- if `rho_scf+p_scf == 0.0`, set the derived `theta_scf` value to `0.0`;
- otherwise evaluate the original ratio unchanged.

This does not alter the Einstein-source momentum density, which continues to be computed directly as `rho_plus_p_theta_scf`.

No other source line, equation, precision setting, initial condition or physics parameter may be changed.

## Frozen executions

Build original and patched copies with the same standalone `make class -j2` target and create only the required empty output directories.

Run:

1. `AUTHOR_ORIG`: untouched source + untouched committed CDE physics/input;
2. `AUTHOR_PATCHED`: patched verification source + identical author physics/input;
3. `B0TINY_ORIG`: untouched source with `beta_1=beta_2=beta_3=0`, committed scalar seeds retained;
4. `B0TINY_PATCHED`: patched source with the identical B0TINY input;
5. `B0EXACT_PATCHED`: patched source with `beta_1=beta_2=beta_3=0`, `phi_ini_scf=phi_prime_ini_scf=0`.

Only output roots differ between paired cases.

## Frozen non-interference test

For both AUTHOR and B0TINY original/patched pairs, require exit zero and compare numeric contents of:

- background table;
- linear `pk.dat`;
- `pk_cb.dat`;
- unlensed `cl.dat`;
- lensed `cl_lensed.dat`;
- density transfer `tk.dat`.

Require identical table shapes and

`max symmetric relative difference <= 1e-12`

for every listed file, where

`srel(x,y)=|x-y|/max(|x|,|y|,1e-300)`.

Raw `*_perturbations*_s.dat` is excluded from non-interference equality because R2 intentionally regularizes the undefined scalar velocity diagnostic at the rigid-vacuum boundary. It is inspected separately.

## Frozen exact-reference tests

`B0EXACT_PATCHED` must exit zero and generate fresh nonempty background, perturbation, linear P(k), CMB Cl and transfer outputs.

Background must satisfy the already frozen K1 thresholds:

- max |beta| <= 1e-15;
- max |dbeta/dz| <= 1e-15;
- max |phi_prime_scf| <= 1e-14;
- max |w_scf+1| <= 1e-12;
- Rspan(rho_scf) <= 1e-12;
- Rspan(rho_cdm*a^3) <= 1e-8.

In the raw exact-reference scalar perturbation table require all numeric entries finite and:

- max |theta_cdm| <= 1e-12;
- max |delta_scf| <= 1e-12;
- max |theta_scf| <= 1e-12.

## Predeclared classifications

- `M14_CDE_INDEPENDENT_REFERENCE_REGULARIZATION_VALIDATED` if both non-interference pairs pass and B0EXACT_PATCHED passes every exact-reference condition.
- `M14_CDE_REGULARIZATION_NONINTERFERENCE_FAIL` if the patch changes any frozen physical output pair above threshold.
- `M14_CDE_EXACT_REFERENCE_STILL_BLOCKED` if non-interference passes but B0EXACT_PATCHED cannot complete or violates exact-reference conditions.
- `M14_CDE_REGULARIZATION_TEST_BLOCKED_INFRASTRUCTURE` only for a demonstrated harness/build/output issue before scientific evaluation.

## Gate semantics

A validation success does **not** retroactively turn the untouched LisaGoh/CDE provider K1 into PASS. It establishes a separate independent verification implementation with a regular exact null. That layer may be used for subsequent K1/K3-scoped geometry/convergence work only if clearly labelled as such.

No K4/K5 response result is part of this test. No physical M14 falsification is authorized.