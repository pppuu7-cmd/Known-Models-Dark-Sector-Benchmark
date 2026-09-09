# KMDSB authority deltas

Updated: 2026-09-10

## Rule

Existing benchmark evidence is immutable with respect to its pinned scientific authority. A newer DSIR `main` may be adopted only by a new wave, a new audit revision, or an explicit authority-delta validation. Never silently reinterpret an old result under a newer DSIR commit.

## AD-001 — W00-W02 to W03

### Frozen authority used by W00-W02

`pppuu7-cmd/Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`

### DSIR main checked on 2026-09-09

`pppuu7-cmd/Dark-Sector-Influence-Reconstruction@328f2ca80b724870b851c7fe6366cce1ca5086cd`

The newer commit is 11 commits ahead of the W00-W02 authority.

### Delta inspection

The inspected delta contains DSIR4 ordered-join / radial-support / process-recovery work, including:
- `EXP073IL` C2 ordered-join structural-admission workflow/authority;
- DSIR4 ordered-join definition;
- DSIR4 radial-support input requirements;
- current-process and recovery updates.

No change in this inspected delta was used to recompute or silently alter the frozen C1-C6 response products underlying W00-W02.

### Decision

- W00, W01 and W02 remain pinned to `e3276e...`.
- W03 may use `328f2ca...` as its starting DSIR authority.
- Any W03 comparison against a W00-W02 numerical artifact must cite the artifact's own older authority/provenance explicitly.
- If a DSIR4 change later proves to alter a shared convention relevant to C1-C6, create a dedicated migration/regression audit rather than rewriting history.

## AD-002 — W03 methodology overlay after DSIR Article-2 G5 hardening

### Previous W03 starting authority

`pppuu7-cmd/Dark-Sector-Influence-Reconstruction@328f2ca80b724870b851c7fe6366cce1ca5086cd`

### New DSIR main inspected

`pppuu7-cmd/Dark-Sector-Influence-Reconstruction@864952e1520d82473a9e976edfeb69f9899d174d`

The new snapshot is 23 commits ahead of `328f2ca...`.

### Scientifically relevant delta for KMDSB

The important change for KMDSB is not a rewrite of the C1-C6 or M07 physical response definitions. It is a hardening of observation-space / cross-family methodology:

1. `docs/article2/DSIR2_G5_DATA_WHITENED_CROSS_FAMILY_STRESS_CONTRACT_V0_1.md` freezes a fail-closed cross-family whitening contract.
2. Synthetic implementation QA passes, but is explicitly non-scientific and does not close real G5.
3. A real covariance may be used only when a frozen observation/operator bridge maps every compared theory/model response into exactly the same covariance coordinate vector, with matched units/order and immutable provenance.
4. No zero imputation, covariance-coordinate relabeling, output-dependent regularization or post-hoc rank cutoff is allowed.
5. Cross-family robustness must stress catalog-multiplicity, equal-family and alternative within-family weighting, stratified bootstrap and leave-one-family-out diagnostics when a classifying G5 execution is attempted.
6. The existing ACT x unWISE 26-coordinate covariance/operator machinery is reusable, but DSIR records that a multi-family theory->exact-26-coordinate provider bridge is not yet bound. Therefore it cannot yet be used as a classifying real cross-family G5 matrix.
7. New DSIR4 authority-succession rules reinforce the general KMDSB rule that numerical equality/replay alone never transfers scientific authority; explicit provenance succession is required.

### Decision for existing M07 evidence

- M07 numerical production, local-q geometry, B6, B8 and its scoped ShapeFit B5 remain pinned to their original W03 authority/provenance. They are not silently recomputed under `864952e...`.
- The M07 ShapeFit B5 result remains a model-specific scoped observational control because it directly constructs the admitted AP/growth coordinate vector. It must **not** be relabelled as DSIR Article-2 cross-family G5 closure.
- M07/C1 or M07/M08 cross-family observational promotion under the new methodology requires the competing models to be propagated through one exact common observation operator into the same bound covariance vector.

### Decision for M08 and later W03 work

- M08 was preregistered under the W03 starting authority `328f2ca...` before this delta.
- Starting with the corrected M08 execution after the initial configuration-only failure, observation-space/B5-B7 methodology adopts `864952e...` as an explicit overlay authority while preserving the original preregistration record.
- M08 B0-B4 solver/model results remain tied to the pinned CLASS implementation and their own run provenance; the new DSIR snapshot chiefly governs any observation-space promotion and cross-family robustness claim.
- Any future classifying cross-family G5-style test must bind a machine-readable operator/covariance manifest before output inspection.

## AD-003 — M09 launch after DSIR4 angular authority closure

### Previous observation-methodology overlay

`pppuu7-cmd/Dark-Sector-Influence-Reconstruction@864952e1520d82473a9e976edfeb69f9899d174d`

### New DSIR main inspected on 2026-09-10

`pppuu7-cmd/Dark-Sector-Influence-Reconstruction@bc28acc47cc5facba046741fd09f710ae8da9689`

This snapshot is exactly 2 commits ahead of the AD-002 overlay.

### Delta inspection

The two-commit delta contains only DSIR4 authority work:
- completion of the `EXP073IM` angular-byte materialization audit at 14/14;
- addition of `EXP073IN_C2_WM_S0_AUTHORITY_SUCCESSION_V0_1.json`.

No file in the delta modifies the Article-2 G5 common-operator/covariance contract, C1-C6 response definitions, M07/M08 solver semantics, or the KMDSB ShapeFit coordinate construction.

### Decision

- M07 and M08 remain historically pinned to their own scientific and methodology authorities; no rebase is performed.
- The successful M07/M08 common-ShapeFit observation control remains valid under its frozen manifest and `864952e...` overlay; the two newer DSIR4 commits do not alter that operator contract.
- M09 may cite `bc28acc...` as the current methodology overlay because the inspected delta is authority/provenance-only with respect to the M09 response questions.
- If later DSIR commits modify G5, response definitions, masks or operator binding, create a new authority delta before observation-space promotion.

## Recovery instruction

A fresh chat must read this file before assuming that the newest DSIR `main` is the authority for every KMDSB result. Authority continuity is historical/provenance state, not a function of numerical closeness or reproducibility alone.
