# W04 M21 conditional late-source neighbor-multipole regression v0.1

Frozen: 2026-09-15 while the flat-identity predicate counterfactual is non-terminal, before any counterfactual result is inspected.

Provider remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Activation

Run only if the terminal parent classification is exactly:

`M21_L400_FLAT_IDENTITY_PREDICATE_BRANCH_CAUSAL_WITH_SCOPE`.

Otherwise skip without CLASS execution.

## Purpose

Test whether the identified flat-distance ULP branch sensitivity is confined to the exact integer multipole sitting on the default late-source threshold, using prospectively frozen neighboring multipoles as negative controls.

## Frozen grid

Cases: `ref,f2,f3,f4`.

Multipoles: `l={399,400,401}`.

Lanes: `native` and `flat_identity_predicate`, with the same counterfactual definition as the parent: in exactly flat geometry only, use binary64 `1.0` in place of `ptr->angular_rescaling` for the late-source predicate operand only. No other provider value is changed.

Runtime threshold remains the exact provider value `transfer_neglect_late_source=400.0`.

## Prospectively frozen predicate expectations

Given the already-terminal angular-rescaling values remain within a few ULP of 1:

- `l=399`: native and counterfactual predicate false for all four cases;
- `l=400`: native `{ref,f2,f4}=true, f3=false`; flat-identity counterfactual false for all four;
- `l=401`: native and counterfactual predicate true for all four cases.

No outcome-dependent threshold or multipole may be added.

## Execution and integrity

Use exact provider pin, exact physical inputs, exact `P400_ON_TAIL_OFF` profile and `OMP_NUM_THREADS=1`.

Instrument only endpoint/predicate/transfer diagnostics for direct scalar E at the three frozen multipoles and the existing frozen k-support `[0.03030247505892471,0.04401375054733766]` Mpc^-1.

Require native full-CMB normalized L2 <= `1e-12` against immutable clean parents from run `34907528331`.

Require same q/k geometry within the established `1e-6` bound and schema-clean finite diagnostics.

## Frozen classification

Define:

- `predicate_pattern_exact`: all three multipoles match the frozen expectations above;
- `neighbor_endpoints_invariant`: for `l=399` and `401`, native and counterfactual final endpoints match exactly for every case/q;
- `neighbor_transfer_null`: for `l=399` and `401`, native vs counterfactual direct scalar-E transfer relative difference <= `1e-10` for every case/q;
- `l400_expected_changes_only`: at `l=400`, endpoint changes occur only for `ref,f2,f4`, while f3 remains invariant.

If all hold -> `M21_LATE_SOURCE_ULP_SENSITIVITY_THRESHOLD_LOCALIZED_WITH_SCOPE`.

If parent causal class holds but any neighboring multipole changes under the identity counterfactual -> `M21_LATE_SOURCE_COUNTERFACTUAL_NEIGHBOR_NONLOCAL_BLOCKED`.

Any authority/null/geometry/schema failure -> `M21_LATE_SOURCE_NEIGHBOR_MULTIPOLE_REGRESSION_BLOCKED`.

## Claim ceiling

A pass establishes that the observed branch sensitivity is localized to the exact equality boundary of the default late-source threshold in this benchmark and is absent at the immediate integer-multipole controls. It still does not establish a general CLASS defect or production fix and does not promote K1/K3/K4 or physically validate/falsify M21.