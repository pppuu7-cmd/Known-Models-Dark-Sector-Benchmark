# M21 l=400 flat-identity numerical-route audit — 2026-09-15

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

This is outcome-independent exact-source authority. It was recorded while the path-scope-recovered late-source predicate aggregate was still non-terminal. It does not use any predicate case value.

## Mathematical flat identity

For `sgnK==0`, the background table constructs the comoving radius at each stored node as

`conformal_distance = conformal_age - tau_table[index]`

and stores angular diameter distance

`D_A = conformal_distance/(1+z)`.

Thus at an exact table node, `D_A(1+z)` and `conformal_age-tau` are the same computed conformal distance.

## Distinct numerical routes at recombination

Thermodynamics first determines `z_rec`, then obtains:

- `tau_rec` from `background_tau_of_z()`, which spline-interpolates the separately stored `tau_table` as a function of `z_table`;
- `da_rec` from `background_at_z(..., long_info, ...)`, which evaluates the background table through its normal interpolation path in `loga=-log(1+z)` and returns the stored angular-distance column;
- `ra_rec = da_rec*(1+z_rec)`;
- `angular_rescaling = ra_rec/(conformal_age-tau_rec)`.

Therefore, even in exact flat geometry, numerator and denominator are obtained by different spline/interpolation routes at a generally non-grid value `z_rec`. Binary64 equality to exactly `1.0` is not guaranteed by the implementation.

## Why l=400 is a boundary-sensitive point

The exact precision default is `transfer_neglect_late_source=400.0` and the provider tests

`l > transfer_neglect_late_source * angular_rescaling`.

At direct `l=400`, this is mathematically equivalent to `angular_rescaling < 1.0`. Hence representable values immediately below and at/above binary64 `1.0` lie on opposite sides of a discrete source-support branch.

## Exact downstream consequence

Inside `transfer_integrate()` the provider first finds the Bessel-overlap endpoint and stores `index_tau_max_Bessel`. A true late-source-neglect flag can then decrement the endpoint until the late-source cutoff is reached. The Bessel edge correction is applied only when the final endpoint remains the Bessel endpoint.

Thus an ULP-scale sign change of `angular_rescaling-1` at this exact threshold can, in principle, change a full late-time support interval while leaving common-support source/radial values unchanged.

## Scope

This audit establishes source-level plausibility and a deterministic prediction for the frozen predicate test. It does not use the pending predicate result, does not establish that the pattern actually occurs, does not establish a CLASS defect, and does not alter K1/K3/K4 or physical-falsification status.