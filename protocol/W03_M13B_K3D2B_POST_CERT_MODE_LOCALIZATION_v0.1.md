# W03 M13b K3D2-B post-certificate mode localization v0.1

Date: 2026-09-14

## Purpose

After the mapping-certified seam diagnostic passed, localize the exact CLASS perturbation mode that still drives the default NDF15 and reference RK minimum-step failures. This protocol is diagnostic only.

Frozen facts:

- exact provider `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`;
- native z=5 perturbation interval insertion/remap audit PASS;
- minimal right-owned point is 12 local tau ULP above `tau_handoff`;
- the prior A1 implementation begins beyond that point and its first default RHS has `a > a_handoff`;
- B1/B2/B3 remain unevaluated.

## Lanes

Run the unchanged A1 implementation in two independent lanes:

1. default NDF15;
2. `cl_ref.pre` reference RK.

For every k-mode, when entering the inserted post-handoff interval, print a `BEGIN` record containing `index_k`, physical `k`, exact interval boundary, actual evolver start, and interval end. If the evolver returns successfully, print the matching `END` record.

The failing mode is the final unmatched `BEGIN` record in each lane. No tolerance, equation, state, precision, or solver setting may be changed.

## Interpretation

- Matching failing k/index across default and reference is evidence of a mode-localized physics/numerics interface blocker, not a family falsification.
- Different failing modes indicate solver-dependent numerical sensitivity and require mode-specific diagnostics before any recovery.
- Successful completion of all modes would contradict the prior failure and requires provenance reconciliation before any promotion.

This protocol cannot promote K3/K4/K5. All outcomes preserve `physical_falsification=false`, `K3_state_ceiling=PARTIAL`, `K4_promoted=false`, `K5_promoted=false`.