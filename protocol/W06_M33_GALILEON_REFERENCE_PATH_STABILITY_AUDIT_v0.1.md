# W06 M33 Galileon reference-path stability audit v0.1

## Purpose
Analysis-only diagnostic using immutable artifact from parser-compliant recovery run `34660258070` (artifact `10286747855`) plus exact pinned provider source `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`.

This audit cannot promote K1 and cannot erase or bypass the `Omega_smg=0.001` stability veto observed prospectively in the parent recovery.

## Frozen questions
1. On the executable positive-`Omega_smg` prefix `{0.5,0.1,0.01}`, do common TT/P(k) responses contract monotonically toward the immutable plain-GR control using normalized-L2 on common finite support?
2. Does the exact pinned provider expose/document an author-supported alternate cubic-Galileon GR/decoupling/reference route that avoids changing the theory or disabling stability checks?
3. Is the `Omega_smg=0.001` failure explicitly attributable to the provider scalar-stability gate rather than parser, missing output, or numerical infrastructure?

## Frozen metrics
For each executable positive arm versus `D_gr`:
- CMB metric: normalized L2 across all common finite numerical C_l columns on matched ell rows.
- P(k) metric: normalized L2 of common-support P(k), linearly interpolating only inside overlapping k support if grids differ.
- Prefix contraction requires strict decrease from 0.5 -> 0.1 -> 0.01 separately for CMB and P(k).

## Frozen source audit
Search exact pinned provider files for cubic Galileon parameterization, `Omega_smg`, debug/reference options, stability-test controls and documented GR/zero-coupling semantics. No provider code is modified.

## Classification
- `REFERENCE_PREFIX_CONTRACTS_STABILITY_BOUNDARY_CONFIRMED`: both metrics strictly contract on the executable prefix; 0.001 is confirmed provider stability veto; no documented alternate author-supported GR route found.
- `ALTERNATE_AUTHOR_REFERENCE_ROUTE_FOUND_REQUIRES_NEW_PREREGISTRATION`: an explicit provider-documented alternate physical reference route is found. No execution is authorized by this audit.
- `REFERENCE_PREFIX_NONCONTRACTING`: either metric fails strict contraction; still no physical falsification.
- `AUDIT_INTEGRITY_BLOCKED`: immutable artifact/source cannot be validated.

All classifications keep `K1_promoted=false` and `physical_falsification=false`. Any future alternate-route execution requires a new preregistration.
