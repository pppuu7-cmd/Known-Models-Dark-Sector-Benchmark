# W04 M20 SIDM K4 Hermite asymptotic extension preregistration v0.1

Date: 2026-09-12
Status: FROZEN BEFORE EXECUTION
Provider: `shinichiroando/sashimi-si@e17d3664dac677b604fd4ff02fb2af105a6937fa`
Trigger: successive preregistered ladders remain improving but nonconverged: max D 5->7=1.1726655606, 7->9=0.8211898018, 9->11=0.6803476320, 11->13=0.6135806019.

Purpose: determine whether the slow improvement continues into a wider high-order regime or stalls. Keep all physics, observables, provider, dependencies, dz=0.2 and N_ma=30 frozen. Only N_herm changes.

Evaluate N_herm={13,17,21}; recompute each profile's exact-zero reference and all nonzero response points. Compute the same symmetric cellwise discrepancy for 13->17 and 17->21.

Frozen interpretation:
- terminal max <=0.10 and decreases: `M20_K4_HERMITE_ASYMPTOTIC_CONVERGENCE_CANDIDATE_DIAGNOSTIC`;
- terminal max decreases but remains >0.10: `M20_K4_HERMITE_ASYMPTOTIC_IMPROVING_NOT_CONVERGED_DIAGNOSTIC`;
- terminal max does not decrease: `M20_K4_HERMITE_ASYMPTOTIC_STALL_OR_NONCONVERGENCE_DIAGNOSTIC`;
- execution/integrity failure: `M20_K4_HERMITE_ASYMPTOTIC_BLOCKED`.

Always diagnostic-only: K4_promoted=false, physical_falsification=false, scientific_fail=false.
