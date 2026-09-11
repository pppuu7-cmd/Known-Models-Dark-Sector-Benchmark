# W05 M35 Einstein-Aether/vector-tensor — CLASS_LVDM K0 provider preregistration v0.1

## Objective
Test only K0 provider provenance/executability for the M35 Einstein-Aether/vector-tensor census row using the public CLASS_LVDM implementation. This is not a K1-K9 test and is not a claim of complete Einstein-Aether scalar/vector/tensor coverage.

## Frozen provider
- Repository: `Michalychforever/CLASS_LVDM`
- Commit: `d9a20bd0c7b7a6c8957410fd245ed06b30b915c1`
- Upstream description: modified CLASS v1.7 for Lorentz violation in gravity and dark matter, with gravity parameters `alpha`, `beta`, `lambda` and DM parameter `Y_dm`.

## Frozen arms
1. `weak_gravity_control`: upstream `lcdm.ini`, retaining its small gravity-sector point (`alpha=1e-5`, `beta=0`, `lambda=0`, `Y_dm=0`). This is a numerical weak-coupling control, not an exact GR-limit K1 test.
2. `aether_gravity_active`: upstream `Misha.ini` gravity-only example (`alpha=0.05`, `beta=0.25`, `lambda=-0.1`, `Y_dm=0`).

Only output root names may be changed. No theory parameters may be tuned after seeing results.

## K0 acceptance
`PASS_WITH_SCOPE` iff:
- exact provider commit is checked out;
- provider builds without source modification;
- both frozen arms exit zero;
- requested CMB TT and matter P(k) outputs exist and all parsed numeric values are finite;
- at least one common-observable normalized L2 response (TT or P(k)) between active and weak-control arms is > 1e-6.

If the exact provider does not build or an arm cannot execute, classify as implementation/provider blocked, not physical FAIL. If outputs are finite but no active response is established, K0 is not promoted.

## Scope
A K0 pass establishes only a pinned executable preferred-frame/LV-gravity provider with an active gravity-only response. It does not establish exact GR recovery, gauge closure, numerical robustness, observational viability, novelty, or complete vector/tensor Einstein-Aether phenomenology. K1-K9 remain OPEN.
