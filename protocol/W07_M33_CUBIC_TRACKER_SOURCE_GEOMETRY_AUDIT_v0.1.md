# W07 M33 cubic-tracker source geometry audit v0.1

Date: 2026-09-12
Provider: `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`

## Purpose
Prospectively determine the dimensionality and branch scope of the **documented production cubic-Galileon tracker route** before any M33 K2 response calculation or promotion decision.

This is source-only. It cannot promote K2 and cannot erase alternate debug/rogue modes.

## Frozen evidence questions
The exact pinned provider must be checked for all of the following:
1. `gravity_models/galileon_3.ini` identifies `gravity_model=galileon`, `gravity_submodel=cubic`.
2. The same documented example states that all model parameters are fixed by `Omega_smg` and the tracker condition.
3. The same example exposes no active `parameters_smg` value for the cubic model and explicitly documents no extra cubic parameters.
4. Exact source documents a distinct rogue/user-set mode associated with `Omega_smg_debug` or disabling attractor initial conditions, separately from the cubic attractor route.
5. Exact source contains a cubic-attractor branch in which the Galileon coefficients are internally fixed/set rather than read as an independent active `parameters_smg` vector from the production example.
6. The pinned input defaults `attractor_ic_smg` to true.

## Frozen classification
If all six checks pass, classify `M33_DOCUMENTED_CUBIC_TRACKER_SOURCE_MANIFOLD_1D_WITH_DEBUG_ROGUE_ROUTE_EXCLUDED_FROM_PRODUCTION_SCOPE`.

This means only: within the provider-documented production cubic-tracker representation used by KMDSB, the exposed physical continuation coordinate is `Omega_smg`; the source also contains an explicitly separate debug/rogue route that is outside this scoped production manifold.

If any required check fails, classify `M33_CUBIC_TRACKER_SOURCE_GEOMETRY_NOT_CLOSED`.

## Nonclaims
Always `K2_promoted=false`, `canonical_K2=OPEN`, `physical_falsification=false`, `all_Galileon_variants_claim=false`. Source dimensionality alone is not K2 PASS. A later prospectively frozen local-tangent calculation and an explicit sufficiency rule are required before any K2 status change.