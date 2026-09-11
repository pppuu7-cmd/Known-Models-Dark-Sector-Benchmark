# W04 M25 m0 P(k) compile-capacity isolation control — preregistration v0.1

## Motivation

The prospectively frozen evolver-isolation control classified `M25_M0_PK_CAPACITY_OR_EVOLVER_CONFOUNDED` (run `34619973784`, result commit `8b80ff824c9ebf9ecb6c479153180c803d6b8c2f`). With raised compile-time quadrature capacities, the provider-default perturbation evolver and explicit `evolver=0` agree closely: symmetric P(k)-tail differences are `[0.00033737134333093973, 0.00028064006403436003, 0.00038114151078310097]`, all far below the frozen 25% gate. However, the raised-cap default-evolver branch differs from the immutable pre-recovery automatic baseline by `[1.9969086343781357, 1.9976958815287216, 1.9978555964406235]`. Thus evolver choice alone does not reproduce the historical shift; compile-time quadrature capacity is the next prospectively admissible causal variable.

This control isolates compile-time capacity while holding provider physics, automatic quadrature, default evolver, tolerances, q support, and eta cases fixed.

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
- provider-default perturbation evolver: no explicit `evolver` override.
- **Diagnostic variable only:** use the pinned CLASS stock compile capacities (`_QUADRATURE_MAX_=250`, `_QUADRATURE_MAX_BG_=800`) instead of the raised 4000/4000 capacities used in run `34619973784`.
- Immutable raised-cap default-evolver comparator: `models/resonant_sterile_neutrino_wdm/M25_M0_PK_EVOLVER_ISOLATION_CONTROL_RESULT.json`, run `34619973784`, result commit `8b80ff824c9ebf9ecb6c479153180c803d6b8c2f`.
- Immutable old automatic baseline: the `old_auto_baseline_Pk_r95` values carried by that same canonical result, originating from run `34551925134`.

No sterile-neutrino physics, abundance, PSD, eta values, CLASS commit, fluid approximation, tolerance, q support, quadrature strategy, evolver choice, or decision threshold may be retuned after outputs are seen.

## Execution

The three eta cases (`e2`, `e3`, `e4`) SHALL execute as independent matrix jobs with `fail-fast: false`. A dependent aggregate stage SHALL wait for all three jobs. Only the stock-capacity branch is recomputed; the already validated raised-cap branch is consumed analysis-only from its canonical machine result. GitHub green status by itself is not a scientific PASS.

## Admissibility

The stock-capacity branch is admissible only if all three eta cases exit successfully and finite H/P(k) diagnostics can be computed against the immutable reference. A stock-capacity provider/configuration failure is classified as a numerical/provider capacity boundary and is not physical falsification.

## Frozen metric

For each eta-tail P(k) r95 value use

`D(a,b) = 2 |a-b| / (|a|+|b|)`.

Two comparisons are mandatory:

1. **Capacity isolation:** fresh stock-capacity/default-evolver versus immutable raised-capacity/default-evolver. Any `D > 0.25` is a materially capacity-sensitive response under otherwise matched settings.
2. **Baseline reproduction:** fresh stock-capacity/default-evolver versus immutable old automatic baseline. All three `D <= 0.25` are required before attributing the historical shift specifically to the compile-capacity change.

## Prospective classifications

1. `M25_M0_PK_COMPILE_CAPACITY_SENSITIVITY_CONFIRMED` if any stock-vs-raised difference is >25% and all three stock-vs-old-baseline differences are <=25%.
2. `M25_M0_PK_COMPILE_CAPACITY_SHIFT_NOT_CONFIRMED` if all three stock-vs-raised differences are <=25% and all executions are admissible.
3. `M25_M0_PK_OLD_BASELINE_NOT_REPRODUCED` if any stock-vs-old-baseline difference is >25%; no clean causal attribution to capacity is allowed.
4. `M25_M0_PK_STOCK_CAPACITY_PROVIDER_BLOCKED` if one or more stock-capacity cases fail execution or finite analysis.

## Interpretation boundary

This is a numerical causal-localization diagnostic. It cannot promote K1 or K4 by itself and cannot establish physical falsification of resonantly produced sterile-neutrino WDM. The matched-evolver quadrature agreement, manual N=2000->4000 convergence, and evolver-isolation result remain durable evidence and SHALL NOT be erased regardless of this control's outcome.