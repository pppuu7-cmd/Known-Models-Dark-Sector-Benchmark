# W07 M30 K2 immutable evidence synthesis preregistration v0.1

## Purpose

Synthesize already-immutable M30 evidence without rerunning the external provider and decide whether the canonical K2 bookkeeping may advance from OPEN to PARTIAL. This analysis cannot assign K2 PASS, physical falsification, or a family-wide covariant claim.

## Frozen inputs

1. K2 path-geometry audit: run `34667418003`, artifact `10289448682`, file `M30_M31_K2_GEOMETRY_SUFFICIENCY_AUDIT.json`.
2. Central local Jacobian: run `34694420359`, artifact `10297689056`, file `M30_CENTRAL_LOCAL_JACOBIAN.json`.
3. Provider pin required in both records: `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`.

## Frozen decision rule

Assign `M30_K2_PARTIAL_LOCAL_RESPONSE_RANK2_SOURCE_QUOTIENT_OPEN` and recommend canonical `K2=PARTIAL` iff all of the following hold:

- provider pin matches exactly;
- geometry record has `integrity_ok=true` for M30;
- geometry classification is `M30_K2_NOT_CLOSED_BY_ONE_DIMENSIONAL_K1_PATH`;
- frozen K1 path rank in the five alpha coefficients is 1 and `c_T` is among the frozen-zero coordinates;
- Jacobian classification is `M30_CENTRAL_LOCAL_2D_RESPONSE_RANK_EVIDENCE`;
- radial and c_T central derivatives both satisfy the preregistered convergence criteria;
- fine radial-vs-c_T response separation satisfies the preregistered angle criterion;
- Jacobian retains `K2_promoted=false` and `physical_falsification=false`.

If immutable inputs are absent, ambiguous, or inconsistent, classify `M30_K2_SYNTHESIS_INTEGRITY_BLOCKED`. If integrity holds but the rank condition is not met, classify `M30_K2_OPEN_LOCAL_RANK_NOT_ESTABLISHED`.

## Scope guard

`PARTIAL` means only that the pinned scalar hi_class representation has reproducible local response-rank evidence in at least two independently perturbed directions around the tested base point. It does **not** establish the complete Horndeski/EFT-of-DE physical parameter manifold, degeneracy quotient, stability domain, global rank, covariant equivalence classes, K3 closure, or observational distinguishability.

No thresholds may be changed after execution of this synthesis.
