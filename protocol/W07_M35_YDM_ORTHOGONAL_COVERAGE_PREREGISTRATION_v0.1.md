# W07 M35 orthogonal Y_dm coverage probe — preregistration v0.1

## Purpose

Extend the already successful M35 CLASS_LVDM K1 gravity-only weak-coupling ladder with one independent dark-matter Lorentz-violation direction. This is a K2 *coverage* probe only. It cannot by itself promote K2, establish the exact physical quotient, validate the full Einstein–Aether scalar/vector/tensor theory space, or exclude the family.

## Immutable provider

- repository: `Michalychforever/CLASS_LVDM`
- branch lineage: `LVDM`
- commit: `d9a20bd0c7b7a6c8957410fd245ed06b30b915c1`
- provider README states that the code implements the Lorentz-violating gravity/dark-matter model of arXiv:1209.0464 and was used in arXiv:1410.6514.

## Frozen coordinates

Hold the gravity coordinates fixed at the already-executed M35 `s01` point:

- `alpha = 0.005`
- `beta = 0.025`
- `lambda = -0.010`

Vary only the independent dark-matter coordinate:

- reference: `Y_dm = 0`
- arms: `Y_dm = 0.020, 0.010, 0.005, 0.001`

The selected positive values are below the order-of-magnitude cosmological upper limit on `Y` reported for Einstein–aether in the source-paper analysis and remain far from the provider pole at `Y_dm = 1`. They are not asserted to exhaust all theoretical/observational constraints.

## Frozen observables

For each arm and the `Y_dm=0` reference, run the exact pinned provider and collect finite CMB `*_cl.dat` and matter `*_pk.dat` outputs. Compute normalized L2 residuals against the `Y_dm=0` reference on matched/common support.

## Decision rule

Classify only the tested orthogonal coordinate coverage:

- `M35_YDM_DIRECTION_EXECUTABLE_CONTRACTING` if every arm exits 0 with finite observables and both CMB and P(k) residuals decrease strictly as `Y_dm -> 0` over the frozen positive ladder.
- `M35_YDM_DIRECTION_EXECUTABLE_NONCONTRACTING` if every arm is finite but either observable does not contract strictly.
- `M35_YDM_DIRECTION_PROVIDER_DOMAIN_BLOCKED` if the reference passes but one or more Y arms fail execution/provider-domain checks.
- `M35_YDM_DIRECTION_CONTROL_BLOCKED` if the `Y_dm=0` reference fails.

Regardless of outcome:

- `K2_promoted = false`
- `physical_falsification = false`
- `full_Einstein_Aether_SVT_claim = false`

No parameter tuning or stability-check disabling is allowed after observing outcomes.
