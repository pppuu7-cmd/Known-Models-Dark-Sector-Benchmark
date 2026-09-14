# W04 M21 perturbation-state seam-preserving recovery v0.1

Frozen: 2026-09-14 after parent run `34895647832` completed with all six numerical lanes `success` and aggregate classification `M21_PERTURBATION_STATE_BRANCH_SIGNATURE_BLOCKED` due only to `invalid a coordinate` in native perturbation tables. No recovered branch-specific J values have been computed at freeze time.

Parent scientific contract remains `protocol/W04_M21_PERTURBATION_STATE_BRANCH_SIGNATURE_v0.1.md`. This recovery changes **only coordinate handling at native approximation-switch seams**. It does not change provider, cases, lanes, k anchors, state variables, physical window, D/J definitions, `J_FLOOR=1e-12`, `J>=3`, branch map, or classification thresholds.

## Immutable parent evidence

Parent run: `34895647832`.
Parent aggregate artifact: `10369361506`, digest `sha256:a7c26408e4c33a2fcda5de2ba5b7ebfed02bee041bbadcaa9b06ce3d2abe805c`.

All six parent lane artifacts are immutable and must be reused; no CLASS rerun is authorized by this recovery.

Observed blocker diagnosis on immutable parent artifacts, before recovered analysis:

- native scalar perturbation coordinates are nondecreasing but include adjacent duplicate `(tau,a)` pairs;
- representative parent tables have exactly three such duplicate seams and no negative coordinate step;
- duplicate rows are not mere formatting duplicates: state can differ across the two rows at the same coordinate (e.g. around tau~226.64 Mpc the two-sided `psi` value differs; later seams can change shear/polarization values);
- exact pinned CLASS source states that perturbations are integrated over intervals with uniform approximation scheme and that at approximation switching points `perturbations_vector_init()` redistributes the old perturbation vector into the new one before integrating the next interval. Therefore a two-sided same-coordinate state is an approximation-boundary seam, not a row to average or silently delete.

## Frozen seam integrity rules

For every reused perturbation table:

1. `tau` and `a` must be finite and nondecreasing in file order;
2. every zero increment in `tau` must coincide with a zero increment in `a` at the same adjacent row pair;
3. each duplicate coordinate may occur with multiplicity exactly two, never three or more;
4. exactly three adjacent duplicate seams must exist in the full table;
5. no negative `tau` or `a` increment is allowed;
6. the two state rows at a seam are preserved verbatim and may differ.

Any violation -> recovery BLOCKED.

## Frozen segment construction

A table with three seams is split into exactly four ordered monotone segments.

For each adjacent duplicate seam at row pair `(i,i+1)`:

- row `i` is the final row of the left segment;
- row `i+1` is the first row of the right segment.

Thus both two-sided states are retained, while no interpolation crosses an approximation seam.

Segments are paired between two numerical lanes by ordinal index 0..3 for the same physical case and k anchor. If either table does not have the required four-segment topology, the cell is BLOCKED.

## Frozen primary-window distance recovery

The parent physical window remains exactly `500 <= z <= 2500`, i.e. `1/2501 <= a <= 1/501`.

For each paired segment separately:

- select finite rows in the primary window;
- take strict `a` overlap between the corresponding segments;
- if at least two first-lane samples lie in the overlap, interpolate the second lane onto the first in `log(a)` **within that segment only**;
- accumulate squared difference and squared norms for that variable.

A segment with fewer than two overlap samples contributes nothing and is report-only as skipped. Across all contributing segments, at least 16 first-lane overlap samples are required, preserving the parent minimum-overlap rule.

Recovered distance is

`D = sqrt(sum_segments ||A-B_interp||^2) / max(sqrt(sum_segments ||A||^2), sqrt(sum_segments ||B_interp||^2), 1e-300)`.

This is the exact parent normalized-L2 statistic applied piecewise without interpolation across a native discontinuity. No seam row is averaged, modified, or selected post hoc.

## Frozen J and classification

Use the parent definitions unchanged:

Common-state:
`J = D_f3 / max(D_ref,D_f2,D_f4,1e-12)`.

ncdm-only:
`J = D_f3 / max(D_f2,D_f4,1e-12)`.

Localized cell: `J>=3`.

Branch/control edges and terminal classifications are exactly those in the parent protocol:

- four branch edges + zero controls localized -> `M21_PERTURBATION_STATE_BRANCH_SIGNATURE_MATCHES_CMB_MAP_WITH_SCOPE`;
- at least two branch edges localized otherwise -> `M21_PERTURBATION_STATE_BRANCH_SIGNATURE_PARTIAL`;
- fewer than two branch edges localized -> `M21_CMB_BRANCH_NOT_LOCALIZED_IN_NATIVE_PERTURBATION_STATES`;
- artifact/topology/schema/integrity failure -> `M21_PERTURBATION_STATE_SEAM_RECOVERY_BLOCKED`.

## Execution authority

Recovery workflow must download the six lane artifacts from parent run `34895647832` and perform only the recovered aggregate. It must not rerun CLASS or regenerate lane data.

## Interpretation ceiling

This recovery can only recover the already-preregistered perturbation-state localization verdict. It cannot establish a CLASS bug, global convergence, production precision, K1/K3/K4, or a physical mixed-dark-matter conclusion.