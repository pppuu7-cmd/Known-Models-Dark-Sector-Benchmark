# W07 M33 cubic-tracker local tangent preregistration v0.1

Date: 2026-09-12
Provider: `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`
Parent source audit: run `34708671061`, artifact `10302796592`, classification `M33_DOCUMENTED_CUBIC_TRACKER_SOURCE_MANIFOLD_1D_WITH_DEBUG_ROGUE_ROUTE_EXCLUDED_FROM_PRODUCTION_SCOPE`.

## Purpose
Prospectively test whether the unique documented production coordinate `Omega_smg` has a numerically converged local observable tangent on the provider-documented numerical-noise-safe cubic-tracker route. This calculation cannot promote K2 by itself.

## Frozen profile and base
- exact pinned cubic Galileon tracker example;
- `D_safe_smg = 1e-100`, already validated at K1 to leave the strict `Omega_smg=0.01` spectra exactly unchanged;
- `a_min_stability_test_smg = 0`;
- base `Omega_smg = 0.005`.

## Frozen symmetric stencils
- coarse: `Omega_smg = 0.004` and `0.006` (`h=0.001`);
- fine: `Omega_smg = 0.0045` and `0.0055` (`h=0.0005`).
All other cosmological/provider settings remain those of the pinned `galileon_3.ini`. `Omega_Lambda` and `Omega_fld` are removed exactly as in the validated parser-compliant/K1 routes so closure tuning determines the intended scalar fraction.

## Observable derivative
For every arm require solver exit 0 and finite CMB plus P(k). Build a single global common CMB support across all five arms by exact integer ell and common numerical columns. Build P(k) support on the base grid restricted to the intersection of all arm k-ranges, with linear interpolation only inside that common range. Normalize CMB and P(k) blocks by the base block L2 norms. Central derivative is `(response_plus-response_minus)/(2h)` and the two normalized blocks are concatenated.

## Frozen convergence criteria
Coarse versus fine central tangent must satisfy all:
- signed cosine >= 0.995;
- principal angle <= 5 degrees;
- relative norm mismatch <= 0.25.
Additionally, both plus/minus displacements at coarse and fine scale must have finite nonzero observable distance from base, and the fine symmetric displacement scale must be smaller than the coarse symmetric displacement scale separately for CMB and P(k).

## Frozen interpretation
If exact source-audit provenance is validated and all tangent criteria pass, classify `M33_CUBIC_TRACKER_1D_LOCAL_TANGENT_CONVERGED_K2_SYNTHESIS_ELIGIBLE`.
Otherwise classify either provider/control blocked or `M33_CUBIC_TRACKER_LOCAL_TANGENT_NOT_CONVERGED`.

Always set `K2_promoted=false`, `canonical_K2=OPEN`, `physical_falsification=false`, `all_Galileon_variants_claim=false`. A later immutable synthesis must decide whether source-unique 1D geometry plus a converged local tangent is sufficient for a scoped K2 promotion.