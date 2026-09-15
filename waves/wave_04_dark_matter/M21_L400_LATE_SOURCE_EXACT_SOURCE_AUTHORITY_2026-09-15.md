# M21 l=400 late-source exact-source authority — 2026-09-15

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

This note is source authority only. It does not use any partial values from the active predicate recovery run and cannot classify the scientific gate.

## Exact angular rescaling

In `source/thermodynamics.c`, after recombination quantities are evaluated, the provider computes:

- `ra_rec = da_rec * (1 + z_rec)`;
- `angular_rescaling = ra_rec / (conformal_age - tau_rec)`.

For the mathematically flat FLRW geometry these numerator and denominator represent the same comoving radial distance, but the implementation obtains them through distinct numerical paths, so equality to the binary64 value `1.0` is not assumed here and must be measured.

## Exact late-source predicate

In `source/transfer.c`, `transfer_late_source_can_be_neglected()` initializes `neglect=false` and evaluates the strict outer predicate

`l > ppr->transfer_neglect_late_source * ptr->angular_rescaling`.

Inside the scalar branch, direct CMB E polarization (`index_tt_e`) sets `neglect=true` when that outer predicate is true.

The transfer module copies `pth->angular_rescaling` into `ptr->angular_rescaling` before constructing the transfer grid and uses the same value in the late-source decision.

## Scope

This establishes the exact code path that the frozen ULP audit is testing. It does not establish that the branch is responsible for the M21 excursion, that any floating-point deviation is erroneous, or that a provider defect exists. Those questions remain gated by the prospectively frozen predicate audit and, conditionally, a separate flat-identity counterfactual audit.