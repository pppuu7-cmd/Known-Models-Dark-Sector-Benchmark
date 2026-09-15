# W04 M21 conditional late-source approximation-off accuracy reference v0.1

Frozen: 2026-09-15 while cross-cosmology/provider regression run `34918945022` is non-terminal, before any of its cell values are inspected.

## Activation

This gate is authorized only if the terminal parent classification is one of:

- `M21_LATE_SOURCE_THRESHOLD_MECHANISM_GENERALIZES_WITH_BOUNDARY_CROSSINGS_WITH_SCOPE`;
- `M21_LATE_SOURCE_THRESHOLD_MECHANISM_GENERALIZES_STRUCTURALLY_WITH_SCOPE`.

Otherwise it must skip without CLASS execution.

## Purpose

Test whether the flat-identity l=400 counterfactual agrees with a more complete transfer-integral reference obtained by disabling the late-source truncation approximation, and quantify native approximation error across the same prospectively frozen 7 cosmologies × 2 provider pins.

This gate addresses accuracy, not only branch causality.

## Frozen cells and provider pins

Exactly reuse all 14 parent cells from `protocol/W04_M21_LATE_SOURCE_CROSS_COSMOLOGY_PROVIDER_REGRESSION_v0.1.md`. No cell may be selected based on parent ULP sign.

## Approximation-off reference

For each cell, preserve the exact same physical INI and M21 precision profile except set:

`transfer_neglect_late_source = 1000000000`

for the reference execution.

At l=399,400,401 this prospectively guarantees the late-source truncation predicate is false without modifying physical parameters, source equations, radial functions, q/k grids or the flat-distance quantity itself.

This is treated as a higher-completeness internal integration reference, not as an assumed production fix.

## Execution

One independent approximation-off CLASS execution per provider/cosmology cell (14 jobs, max parallel 14), exact provider pin, `OMP_NUM_THREADS=1`, same `l_max_scalars=450` and same physical inputs as parent.

Instrument direct scalar-E endpoints/transfers at l=399,400,401 and k in `[0.02,0.06] Mpc^-1` using output-only diagnostics.

Download immutable `clean_native`, `patched_native`, and `flat_identity_predicate` outputs from the authorized parent cross-regression run for comparison; do not recompute or replace them.

## Frozen integrity

Require:

- exact provider pin;
- CLASS rc=0;
- only output-only diagnostic source modification;
- runtime threshold exactly `1e9` in approximation-off reference;
- no late-source neglect at 399/400/401;
- same-q physical-k agreement with parent <= `1e-12`;
- schema-clean finite diagnostics.

## Frozen accuracy comparisons

For every cell and q at l=400 compute direct scalar-E relative differences:

- `D_native = |Delta_native - Delta_off| / max(|Delta_native|,|Delta_off|,floor)`;
- `D_identity = |Delta_identity - Delta_off| / max(|Delta_identity|,|Delta_off|,floor)`;

with `floor = 1e-300` only to avoid division by zero.

Also compare the l=400 CMB EE coefficient from parent native/identity and approximation-off output using the same symmetric denominator floor.

At l=399, parent native/identity are already non-truncated and must agree with approximation-off within direct-transfer relative `1e-10`; otherwise the reference is nonlocal/blocked.

No hard accuracy expectation is frozen for l=401 because parent native/identity intentionally retain the late-source approximation there while approximation-off disables it; report it descriptively only.

For cells whose parent native `angular_rescaling < 1.0` (definition fixed by source rule, not chosen post-hoc), test:

- `identity_matches_off`: max l400 direct-transfer `D_identity <= 1e-10`;
- `native_is_not_better`: max l400 `D_identity <= D_native + 1e-14` and l400 EE absolute symmetric error of identity <= native + `1e-14`.

For cells whose parent native `angular_rescaling >= 1.0`, native and identity were the same no-cut branch at l400; both must match approximation-off within `1e-10` direct transfer.

## Classification

- all 14 cells authority clean, l399 locality clean, all affected cells satisfy `identity_matches_off` and `native_is_not_better`, and all unaffected cells match off -> `M21_LATE_SOURCE_FLAT_IDENTITY_MATCHES_APPROXIMATION_OFF_REFERENCE_WITH_SCOPE`;
- reference is valid but identity does not consistently match/beat native at l400 -> `M21_LATE_SOURCE_FLAT_IDENTITY_ACCURACY_ADVANTAGE_NOT_ESTABLISHED_WITH_SCOPE`;
- any provider/schema/geometry/nonlocal-reference failure -> `M21_LATE_SOURCE_APPROXIMATION_OFF_ACCURACY_REFERENCE_BLOCKED`.

## Claim ceiling

A match result would establish that, on this frozen grid, replacing the flat late-source predicate operand by exact identity at l=400 reproduces the more complete no-late-cut transfer integral and is not less accurate than the native threshold branch. That would justify preparing an issue-quality upstream reproducer and candidate-fix regression. It still would not by itself authorize modifying upstream CLASS, assert all cosmologies are affected, or promote K1/K3/K4/physical claims.