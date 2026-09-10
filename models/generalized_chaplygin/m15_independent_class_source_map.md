# M15 independent GCG CLASS source map

Date: 2026-09-10
Status: `V1_EXACT_REFERENCE_PASS_V2_EQUATION_MAPPING_ACTIVE`
Scientific promotion: **NO**

## Purpose

Bind the preregistered independent reproduction in `protocol/W03_M15_INDEPENDENT_GCG_CLASS_REPRODUCTION_PREREGISTRATION_v0.1.md` to one immutable upstream CLASS revision and to explicit source entry points before any finite-alpha implementation or science run.

This is a KMDSB verification implementation plan, **not** recovery of the original 2017 author code.

## Frozen upstream

Repository: `lesgourg/class_public`
Commit: `e85808324f51fc694d12e3ed7439552a3c3f9540`

Rationale:
- this exact official CLASS pin is already exercised by KMDSB W03 and has working build/output infrastructure;
- using the same immutable upstream minimizes unrelated solver drift when comparing the future verification branch with its alpha=0 reference;
- no claim is made that this commit is the CLASS revision used by vom Marttens et al. (2017).

Changing this upstream pin requires a new preregistration delta.

## Frozen implementation boundary

Only the dark-sector background and linear scalar perturbation closure defined in the M15 preregistration may be modified. Standard photon, baryon, neutrino, recombination, primordial, transfer, harmonic, lensing and output machinery stays upstream.

The implementation exposes an explicit `m15_alpha` coordinate and must reject unsupported/non-frozen closure choices rather than silently falling back to fluid/PPF behavior.

### 1. Input/state ownership

Primary files:
- `include/background.h`: persistent M15 background parameters/state flags;
- `source/input.c`: parse/default/validation of `m15_alpha` and activation flag.

At the frozen upstream pin, `struct background` already owns H0, Omega0_b, Omega0_cdm, Omega0_lambda/fld/scf and fluid parameters. The M15 reproduction therefore belongs in this structure rather than in an external post-processing layer.

Reference rule: `m15_alpha = 0` must enter the same physical LambdaCDM equations as the unmodified reference. No output substitution, file copying or explicit zeroing of residuals is permitted.

### 2. Background evolution

Primary file: `source/background.c`.

Relevant upstream entry points:
- `background_initial_conditions(...)` for integrated-state initialization;
- `background_derivs(...)` for the ODE system;
- background vector filling/output functions for H and component densities.

Frozen M15 equations for the vacuum subcase:

`dot(rho_Lambda) = Q`

`dot(rho_c) + 3 H rho_c = -Q`

with the preregistered covariant background relation

`rho_Lambda/rho_Lambda0 = (H/H0)^(-2 alpha)`.

The implementation must keep radiation and baryons explicitly in the Friedmann budget; it must not replace this by the two-component analytic GCG background.

At `alpha=0`, `Q=0`, `rho_Lambda=const`, and CDM must recover the upstream `a^-3` branch continuously.

### 3. Scalar perturbations

Primary files:
- `include/perturbations.h` for any new perturbation-vector/source indices needed by the reproduction;
- `source/perturbations.c` for initialization, derivative evolution and source projection.

Primary evolution entry point: `perturbations_derivs(...)` and its scalar-mode branches.

Frozen gauge for the independent reproduction: **Newtonian gauge**.

The implementation must source-bind the 2017-paper closure rather than reuse CLASS `fld` sound-speed/PPF equations:
- vacuum energy balance corresponding to Eq. (45);
- momentum-transfer relation corresponding to Eq. (46);
- CDM density/velocity equations corresponding to Eqs. (47)-(48);
- `delta_Lambda = -(2 alpha/(3 H)) delta_Theta` corresponding to Eq. (49);
- Newtonian-gauge expansion perturbation `delta_Theta` corresponding to Eq. (50);
- `delta Q` derived from the vacuum energy-balance/covariant relation, not introduced as a free phenomenological parameter.

If an exact convention/sign mapping from the paper to CLASS variables cannot be demonstrated before coding a term, stop with `M15_INDEPENDENT_REPRO_BLOCKED_EQUATION_MAPPING`; do not choose a convenient sign or gauge conversion post hoc.

### 4. Observation products

No new observation operator is introduced at V0/V1. Standard CLASS output is used identically for reference and verification branches.

Products:
- background H(z) and component densities;
- TT/TE/EE;
- matter transfer and linear P(k,z=0);
- derived background quantities needed to verify matched cosmology.

Undefined entries remain masked; exact-zero denominators are excluded from relative metrics rather than zero-imputed.

## V0 upstream control — terminal PASS

Canonical machine record: `models/generalized_chaplygin/M15_INDEPENDENT_V0_RESULT.json`.

Recovery run `34499646016` executed the exact untouched upstream pin in Newtonian gauge and passed every frozen V0 stage. The CLASS exit code was 0 and fresh output contained finite numerical data in all required products:

- background: 40000 finite rows;
- CMB Cl table: 1799 finite rows;
- linear P(k): 470 finite rows;
- matter transfer: 470 finite rows.

Immutable artifact: `10161331129`.

V0 classification: `M15_INDEPENDENT_REPRO_V0_UPSTREAM_CONTROL_PASS`.

## V1 alpha=0 scaffold/reference — terminal PASS

Canonical machine record: `models/generalized_chaplygin/M15_INDEPENDENT_V1_RESULT.json`.
Workflow run: `34500064989`.

The V1 patch introduced only the explicit selector/state scaffold (`has_m15_gcg`, `m15_alpha`) in `include/background.h` and `source/input.c`. It added **no finite-alpha background or perturbation physics**.

Two independent clones of the exact upstream pin were built. One remained untouched; the other received only the V1 scaffold. Both were executed in Newtonian gauge at the same LambdaCDM point, with `m15_alpha=0` only in the scaffold branch.

Identity result:

- background: 40000 rows, maximum and RMS symmetric relative difference exactly `0`;
- TT: 1799 matched entries, RMS/max difference exactly `0`;
- EE: 1799 matched entries, RMS/max difference exactly `0`;
- TE: 1799 matched entries, RMS/max difference exactly `0`;
- linear P(k): 470 matched entries, RMS/max difference exactly `0`;
- matter transfer: 470 rows / 3760 compared entries, RMS/max difference exactly `0`;
- reference exit = `0`;
- scaffold alpha=0 exit = `0`;
- deliberate `m15_alpha=0.01` V1 negative control exit = `1`, with the expected rejection that finite-alpha physics is not yet authorized.

Classification: `M15_INDEPENDENT_REPRO_REFERENCE_PASS`.

This result establishes exact reference preservation by the M15 code path. It is still **not** a scientific M15 K0-K9 promotion because no nonzero-alpha equation has yet been implemented.

## Staged implementation rule

1. **V0 upstream control — PASS**.
2. **V1 alpha=0 scaffold/reference — PASS**.
3. **V2 finite alpha — EQUATION MAPPING ACTIVE**: finite-alpha coding is allowed only after every required published background/perturbation quantity is mapped to the frozen CLASS conventions and any under-specified closure parameter is either independently sourced or explicitly represented as a scoped extra closure coordinate.
4. **V3 local geometry — FORBIDDEN until V2 PASS**: requires a separate K4 numerical-floor preregistration.

## Current next gate

Complete `models/generalized_chaplygin/m15_v2_equation_to_class_map.md`. In particular, resolve the published perturbation closure around Eqs. (45)-(50), the paper-to-CLASS velocity-sign convention, conformal/cosmic-time factors, and the value/status of the DE comoving sound-speed parameter appearing explicitly in Eqs. (45)-(48).

Do **not** assume a solver default for an under-specified physical closure parameter merely because the original study used a modified Boltzmann code. If the published numerical value cannot be established, V2 must branch prospectively into explicitly labelled closure subcases or remain blocked; it cannot be called an exact reproduction of the unpublished author implementation.