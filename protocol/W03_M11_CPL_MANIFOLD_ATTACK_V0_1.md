# W03 M11 full-CPL manifold attack v0.1

Frozen: 2026-09-10
Status: PREREGISTERED BEFORE STAGE-B OUTPUT
Target: M11 effective noncanonical sound-speed direction
Comparator: local 2D CPL smooth-DE manifold

## Question

Does the sound-speed response detected in M11 Stage A survive the **full local smooth-DE CPL manifold** when candidate and comparator are evaluated in the same solver, same P+H response block and at the same physical anchor?

The existing M08 CPL basis at the LambdaCDM point is not reused because M11 sound speed is unidentifiable at `w=-1` and local tangent geometry may vary with the anchor.

## Frozen anchor and solver

Pinned CLASS: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Common anchor:
- `w0=-0.95`
- `wa=0`
- `cs2_fld=1`
- `Omega_Lambda=0`, fluid density inferred by closure
- `use_ppf=yes`
- same h, omega_b, omega_cdm, z grid, k grid and precision as M11 Stage A.

Target candidate direction:

`J_s = [r(w0=-0.95,wa=0,cs2=.95)-r(anchor)] / 0.05`

with Stage-A convergence against the `.90` case already passed.

## Comparator basis

CPL columns are evaluated at two symmetric finite-difference steps:

- large: `h=1e-3`
- small: `h=5e-4`

For each h:

`J_0 = [r(w0+h,wa=0)-r(w0-h,wa=0)]/(2h)`

`J_a = [r(w0,wa=+h)-r(w0,wa=-h)]/(2h)`.

All comparator cases use `cs2_fld=1`.

The small-step basis is used for the primary projection after both columns pass step-stability.

## Frozen numerical stability gates

For each CPL column, large-step vs small-step:
- relative vector difference <= 0.01
- acute angle <= 0.5 deg

If either fails, K6 remains `PARTIAL` and no manifold classification is promoted.

## Shared manifold projection

On concatenated `35 lnP + 7 lnH`, solve

`c* = argmin_c || J_s - [J_0 J_a] c ||_2`.

The same `c*` is then used to report residual fractions separately in P and H. No independent per-block refit is allowed for the classifying result.

Also report a diagnostic P-only optimum, clearly labeled non-classifying.

## Frozen interpretation bands

These bands are benchmark classifications, not observational significance thresholds:

- combined residual <= 0.10: `CPL_ABSORBS_M11_WITH_SCOPE`
- combined residual >= 0.30: `M11_SEPARATED_FROM_LOCAL_CPL_WITH_SCOPE`
- 0.10 < residual < 0.30: `INCONCLUSIVE_MANIFOLD_SEPARATION`

Even a separated result is **theory-response only**. K7 remains OPEN until a common exact observation operator and covariance are applied.

## Covariant k-essence escalation rule

A covariant `P(phi,X)` M11b implementation becomes mandatory before family-level novelty if:
1. M11 survives the full CPL manifold with combined residual >=0.30; or
2. a known covariant kinetic model is shown to occupy an orthogonal channel absent from the effective fluid representative.

If the effective sound-speed direction is absorbed, covariant subcases remain in the escape-search census but are lower priority unless their microphysics adds a distinct response/stability structure.
