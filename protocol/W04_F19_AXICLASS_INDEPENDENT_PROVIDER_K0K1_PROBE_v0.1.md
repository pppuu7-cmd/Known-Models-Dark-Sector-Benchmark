# W04 F19 AxiCLASS independent-provider K0/K1 probe v0.1

Frozen: 2026-09-14
Status: PREREGISTERED
Family: F19/M19 fuzzy / ultralight axion dark matter
Candidate provider: `PoulinV/AxiCLASS@ae9609e1f96ddebbb6cc8a46de94512514c68781`

## Motivation
The preceding F19 independent-provider discovery found `PoulinV/AxiCLASS` as an implementation-bearing candidate outside the already-blocked axionCAMB/AxiECAMB lineage. Repository metadata describes AxiCLASS as a CLASS-based solver for axion-like particles, and the pinned tree contains an author-supplied `example_axionDM.ini` with scalar-field background, perturbation/fluid controls and matter-power output. This probe is frozen before executing the candidate.

## Frozen scope
This probe may establish only:
1. source-complete independent-provider eligibility (K0 scope);
2. provider executability via the unchanged author axion-DM example;
3. an exact zero-field reference identity test in the same pinned AxiCLASS binary.

It cannot promote K2-K9, cannot erase prior axionCAMB/AxiECAMB exact-zero blockers, and cannot constitute physical falsification if the candidate fails numerically.

## Frozen source requirements
The exact pinned source must show all of:
- CLASS-derived background and linear perturbation implementation for the scalar/axion degree of freedom;
- source/input parameters for axion/scalar potential and perturbation inclusion;
- an author axion-DM example producing linear matter response;
- no dependency on `dgrin1/axionCAMB` or `Ra-yne/AxiECAMB` source for its Boltzmann evolution.

Failure of any requirement => `F19_AXICLASS_K0_SOURCE_INCOMPLETE_OR_LINEAGE_REJECTED`; no K1 interpretation.

## Frozen provider control
Clone exactly `PoulinV/AxiCLASS@ae9609e1f96ddebbb6cc8a46de94512514c68781`, build without physics edits, and execute the committed `example_axionDM.ini`. Root/output-directory plumbing may be changed only if necessary to make the committed workload write into the CI workspace; scalar/cosmological/precision physics must remain unchanged.

Provider control PASS requires exit code 0 plus fresh finite background and matter-power products. Otherwise classify `F19_AXICLASS_PROVIDER_CONTROL_BLOCKED`.

## Frozen exact zero-field K1 map
Use the same pinned AxiCLASS binary and the same vanilla cosmological inputs as the candidate test. Compare:

- **C0 vanilla control:** no scalar-field component enabled; standard CDM carries the matter density.
- **Z0 exact scalar-zero branch:** retain the axion potential/mass/decay-scale and perturbation-capable code path, disable scalar shooting, and set the author-defined scalar initial field and velocity exactly to `scf_parameters = 0,0`. For the axion potential this is the exact field minimum, so scalar background density and perturbations should vanish. Do not use a small nonzero field as a surrogate zero.

Both branches must request the same background and linear `mPk` products, same H0/baryon/CDM/primordial/reionization settings, same k range and precision defaults. No post-hoc change of tolerances, mass, `f_axion`, gauge, fluid switch, or CDM density is permitted after seeing results.

## Frozen K1 metrics
The zero-field branch must execute with exit code 0. On common finite support compare:
- background `H [1/Mpc]`: max symmetric relative difference <= `1e-10`;
- background CDM density (or closest same-source CDM density column): max symmetric relative difference <= `1e-10`;
- linear P(k): max symmetric relative difference <= `1e-8`.

If all pass: `F19_AXICLASS_EXACT_ZERO_FIELD_K1_PASS_WITH_SCOPE`.
If execution is finite but any metric exceeds threshold: `F19_AXICLASS_EXACT_ZERO_FIELD_K1_FAIL_NUMERICAL_IDENTITY`.
If Z0 cannot execute or output is nonfinite: `F19_AXICLASS_EXACT_ZERO_FIELD_REFERENCE_BLOCKED_IMPLEMENTATION`.

Any FAIL/BLOCKED classification is provider-specific and is not F19 physical falsification.

## Parallel execution / barrier
Run source audit, unchanged author provider control, and C0/Z0 identity calculation as independent jobs with `fail-fast:false` where applicable. Aggregate classification waits for all prerequisites. A green workflow alone is not a K1 PASS; the aggregate must consume raw products and apply the frozen thresholds above.

## Next gate
If K0 source eligibility + provider control + exact-zero K1 PASS, synchronize F19 K0/K1 matrices and preregister K2 physical geometry around the nonzero ULA abundance/fraction coordinate. If K1 is provider-blocked, preserve the independent-provider evidence but do not infer physical failure; continue to another independent implementation or author-supported regular zero-abundance prescription.