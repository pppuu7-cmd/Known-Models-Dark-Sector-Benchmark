# W04 M25 m0 P(k) evolver-isolation control — preregistration v0.1

## Motivation

The prospectively frozen matched-evolver quadrature control classified `M25_M0_PK_MATCHED_EVOLVER_QUADRATURE_AGREEMENT`: with the same explicit-RK `evolver = 0`, automatic quadrature and the immutable manual N=4000 branch agree by symmetric relative differences `[2.2619695830008982e-4, 6.843414083315417e-5, 2.284619684214263e-5]`, all far below the frozen 25% threshold. The same automatic-RK branch differs from the immutable pre-recovery automatic baseline by approximately `[1.99691, 1.99770, 1.99786]`. Thus the earlier manual-vs-automatic discrepancy cannot be assigned to quadrature alone; an evolver-associated shift is present, but the prior recovery also raised compile-time quadrature-capacity constants.

This diagnostic prospectively isolates the perturbation evolver while holding the raised compile-time quadrature capacity and all physical/provider inputs fixed.

## Frozen provider and physical inputs

- CLASS pin: `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- Sterile-neutrino distribution/provider inputs: exactly the immutable m0 `e2`, `e3`, `e4` cases from M25 K1 run `34548988620`.
- Reference CDM outputs: exactly the immutable reference outputs carried by that K1 artifact.
- Output: `mPk` only for the three eta-tail cases.
- `tol_ncdm_bg = 1e-6`.
- `tol_ncdm = 1e-6`.
- `ncdm_fluid_approximation = 3`.
- `ncdm_quadrature_strategy = 0` (automatic).
- `ncdm_maximum_q = 10.0`.
- `_QUADRATURE_MAX_ = 4000` and `_QUADRATURE_MAX_BG_ = 4000`, exactly matching the successful explicit-RK matched-evolver control.
- **Diagnostic variable only:** omit the explicit `evolver = 0` override and use the pinned provider's unmodified default evolver choice.
- Immutable explicit-RK comparator: `models/resonant_sterile_neutrino_wdm/M25_M0_PK_MATCHED_EVOLVER_QUADRATURE_CONTROL_RESULT.json`, result commit `97e56cc6e90b4337ac915198362903582d05ca32`, run `34614012430`.
- Immutable old automatic baseline: artifact `m25-ncdm-nofluid-m0` from run `34551925134`, retained as a compile-capacity control.

No sterile-neutrino physics, abundance, PSD, eta values, CLASS commit, fluid approximation, tolerance, q support, quadrature strategy, compile-time capacity, or decision threshold may be retuned after outputs are seen.

## Execution

The three eta cases (`e2`, `e3`, `e4`) SHALL execute as independent matrix jobs with `fail-fast: false`. A dependent aggregate stage SHALL wait for all three jobs. GitHub green status by itself is not a scientific PASS.

## Admissibility

The default-evolver branch is admissible only if all three eta cases exit successfully and finite H/P(k) diagnostics can be computed against the immutable reference. Provider/configuration failure is `BLOCKED_IMPLEMENTATION/PROVIDER` and is not physical falsification.

## Frozen metric

For each eta-tail P(k) r95 value use the same symmetric relative difference as the parent control:

`D(a,b) = 2 |a-b| / (|a|+|b|)`.

Primary evolver comparison:

- compare `auto_default_evolver` to immutable `auto_RK` from run `34614012430`;
- all three `D <= 0.25` means the large historical shift is not reproduced by the evolver change alone;
- any `D > 0.25` means a numerically material evolver dependence is present under otherwise matched settings.

Capacity-control comparison:

- compare `auto_default_evolver` with raised compile caps to the immutable old automatic baseline generated with the provider's original compile caps;
- all three `D <= 0.25` is required to attribute a primary >25% difference specifically to the evolver rather than the capacity change;
- any capacity-control `D > 0.25` keeps the cause confounded between compile-capacity and evolver/provider numerical layers.

## Prospective classifications

1. `M25_M0_PK_EVOLVER_SENSITIVITY_CONFIRMED` if any primary default-vs-RK difference is >25% and all three capacity-control differences are <=25%.
2. `M25_M0_PK_EVOLVER_SHIFT_NOT_CONFIRMED` if all three primary differences are <=25% and the provider execution is admissible.
3. `M25_M0_PK_CAPACITY_OR_EVOLVER_CONFOUNDED` if any capacity-control difference is >25%; this classification takes precedence over causal attribution to the evolver alone.
4. `M25_M0_PK_EVOLVER_CONTROL_PROVIDER_BLOCKED` if required execution/analysis is unavailable.

## Interpretation boundary

This is a numerical causal-localization diagnostic. It cannot promote K1 or K4 by itself and cannot establish physical falsification of resonantly produced sterile-neutrino WDM. The prior matched-evolver quadrature agreement and the manual N=2000->4000 convergence remain durable evidence and SHALL NOT be erased regardless of this result.