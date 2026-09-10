# W03 M11 Effective k-essence / sound-speed response preregistration v0.1

Frozen: 2026-09-10
Status: PREREGISTERED BEFORE RUN
Coverage family: F11 / benchmark M11

## Scientific scope

M11 is **not** claimed to be the full space of covariant k-essence Lagrangians `P(phi,X)`. It is a controlled effective response representative for the defining cosmological feature that distinguishes many noncanonical scalar-DE models from canonical smooth quintessence: a rest-frame sound speed `cs2_fld != 1` at the perturbation level.

Implementation: pinned upstream CLASS fluid dark energy with CLP equation of state and PPF enabled. A later covariant kinetic subcase is required only if it produces a response outside this effective family or exposes a new physical/stability constraint.

## Why the test is stratified

At exact `w=-1`, dark-energy perturbations vanish and `cs2_fld` is physically unidentifiable. Therefore the derivative with respect to sound speed at the LambdaCDM point is not a valid independent tangent direction.

We freeze a two-stage geometry:

1. **K1 reference branch:** `w -> -1` with `cs2=1`, including a separate pure-LambdaCDM vs fluid-`w=-1` reference regression.
2. **K5 sound-speed branch:** evaluate the noncanonical coordinate on the fixed anchor `w=-0.95`, where DE perturbations are nonzero.

Define the one-sided subluminal coordinate

`q_s = 1 - cs2_fld >= 0`.

The local sound-speed direction is estimated at the anchor from two prospectively fixed steps:

- `q_s=0.05` (`cs2=0.95`)
- `q_s=0.10` (`cs2=0.90`)

with

`J_s(h) = [r(w=-0.95, cs2=1-h) - r(w=-0.95, cs2=1)] / h`.

A smooth-DE direction at the same anchor is estimated by a central derivative in

`epsilon_w = 1+w`

using `w=-0.949` and `w=-0.951` (`h_w=0.001`) at `cs2=1`.

## Frozen solver configuration

- CLASS repository: `lesgourg/class_public`
- commit: `e85808324f51fc694d12e3ed7439552a3c3f9540`
- `h=0.67`
- `omega_b=0.0224`
- `omega_cdm=0.1200`
- flat geometry
- fluid branch: `Omega_Lambda=0`, `Omega_fld` inferred by closure
- `fluid_equation_of_state=CLP`
- `wa_fld=0`
- `use_ppf=yes`
- synchronous solver gauge
- linear `mPk`; no nonlinear correction
- z nodes: `{0.295,0.51,0.706,0.934,1.317,1.491,2.33}`
- k nodes: `{0.001,0.003,0.01,0.03,0.1} h/Mpc`
- `tol_perturbations_integration=1e-8`
- `perturbations_sampling_stepsize=0.01`

## Frozen cases

- `lcdm`: pure LambdaCDM reference
- `fld0`: fluid `w=-1`, `cs2=1`
- `anchor`: fluid `w=-0.95`, `cs2=1`
- `wp`: `w=-0.949`, `cs2=1`
- `wm`: `w=-0.951`, `cs2=1`
- `cs005`: `w=-0.95`, `cs2=0.95`
- `cs010`: `w=-0.95`, `cs2=0.90`

## Hard gates frozen before output

### Reference gate
Pure LambdaCDM vs fluid `w=-1`:
- `max |ln P_fld0/P_LCDM| <= 1e-6`
- `max |ln H_fld0/H_LCDM| <= 1e-8`

If this fails, M11 K1 remains PARTIAL and all finite sound-speed geometry is relative only to the internal fluid anchor.

### Sound-speed convergence gate
Between `J_s(0.05)` and `J_s(0.10)`:
- relative norm difference <= 0.10
- acute angle <= 3 deg

### Non-null gate
The sound-speed direction must satisfy `||J_s(0.05)_P|| > 1e-8`; otherwise classify the tested block as `NEAR_NULL/NONIDENTIFIABLE`, not as evidence that k-essence is false.

### Rank/novelty diagnostic
Report angle, projection residual and singular spectrum between the smooth-w direction and sound-speed direction at the same `w=-0.95` anchor.

No theory-space angle is an observational claim. K7 remains OPEN until an exact common observation operator/covariance bridge is constructed.

## Interpretation rules

- `cs2` response being null at `w=-1` is a stratified-identifiability property, not a failure.
- A distinct sound-speed direction supports a new perturbation response axis but not full covariant k-essence uniqueness.
- If the effective fluid sound-speed direction is absorbed by the existing smooth-DE/CPL manifold, a covariant k-essence implementation is still required only if its additional background/metric/stability structure can escape that manifold.
- No post-hoc change of the anchor, steps or thresholds after the first successful solver output.
