# M15 independent GCG CLASS source map

Date: 2026-09-10
Status: `UPSTREAM_PIN_AND_SOURCE_MAP_FROZEN`
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

Changing this upstream pin requires a new preregistration delta before V1.

## Frozen implementation boundary

Only the dark-sector background and linear scalar perturbation closure defined in the M15 preregistration may be modified. Standard photon, baryon, neutrino, recombination, primordial, transfer, harmonic, lensing and output machinery stays upstream.

The first implementation must expose an explicit `m15_alpha` coordinate and must reject unsupported/non-frozen closure choices rather than silently falling back to fluid/PPF behavior.

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

V1 products frozen by the parent preregistration:
- background H(z) and component densities;
- TT/TE/EE;
- matter transfer and linear P(k,z=0);
- derived background quantities needed to verify matched cosmology.

Undefined entries remain masked; exact-zero denominators are excluded from relative metrics rather than zero-imputed.

## Staged implementation rule

The code path is split prospectively:

1. **V0 upstream control**: exact pin builds and produces a fresh LambdaCDM background/CMB/matter bundle on the intended Newtonian-gauge output route.
2. **V1 alpha=0 scaffold/reference**: only after V0 passes, add the explicit M15 state/parser/equation scaffolding and prove `alpha=0` matches an independently built unmodified upstream reference within frozen thresholds.
3. **V2 finite alpha**: forbidden until V1 passes. Implement/activate finite-alpha background and perturbation terms and compare structural trends with the publication.
4. **V3 local geometry**: forbidden until V2 passes and a separate K4 numerical-floor preregistration is frozen.

A V0 success is infrastructure evidence only and does not change M15 K0-K9 matrix entries.

## Current next gate

Run the exact upstream V0 control on GitHub Actions. It must verify the checkout SHA, build without source edits, execute one fresh Newtonian-gauge LambdaCDM case with background + TT/TE/EE + mPk/mTk outputs, and upload immutable logs/config/products/provenance.

Only if that control passes may the alpha=0 M15 scaffold patch and V1 differential harness be written.