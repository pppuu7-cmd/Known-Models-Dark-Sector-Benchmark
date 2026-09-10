# M14 IDECAMB global-amin sensitivity run 1

Date: 2026-09-10
Workflow run: `34466686434`
Status: `DIAGNOSTIC_BLOCKED_REFERENCE_DOMAIN`
Physical interpretation: **none**

## What was attempted

The preregistered diagnostic changed only the coupled-quintessence global background start/grid parameter from the upstream `amin=1e-12` to later surfaces while retaining the same beta grid, alpha anchor, output vector, and K4 thresholds.

The sequence was `{1e-12,1e-8,1e-6,1e-5}`.

## Observed execution boundary

The upstream `amin=1e-12` control completed for all three beta points and produced both `.quantity` and `.theory_cl` outputs.

At the first altered surface `amin=1e-8`:

- `beta=0` terminated with process exit `139` (segmentation fault);
- `beta=5e-8` emitted a CAMB/DVERK error stating that the integrator could not satisfy the error requirement at the minimum step size; the process returned zero but produced only the background `.quantity` file and no `.theory_cl` file;
- the workflow then stopped on the missing theory file before the remaining grid points/surfaces were executed.

Thus the full response vector cannot be evaluated after changing the global interpolation/integration floor.

## Interpretation

This is an infrastructure/domain failure of the proposed diagnostic, not evidence against the initial-asymptotic hypothesis and not evidence against coupled quintessence.

Changing the same `amin` symbol simultaneously changes:

1. the background initial surface;
2. the stored interpolation grid lower boundary used later by the full CAMB evolution.

The full Boltzmann calculation evidently requires the coupled-quintessence background to be available earlier than `1e-8` for at least part of its execution. Therefore a global-`amin` ladder does not isolate the initial-condition question cleanly.

The preregistered rule for any execution/shape failure applies: the diagnostic is classified as blocked and no K4 inference is drawn from it.

## Revised diagnostic principle

Keep the provider's global interpolation/background coverage at `amin=1e-12` and change only the **initial asymptotic state supplied at that fixed surface**. This preserves the full time domain needed by CAMB.

The source equations admit a coupling-dominated radiation-era inner asymptotic. At early radiation domination, with the exponential CDM coupling and inverse-power potential, the regular leading particular solution is

`phi(a) ~= beta * grhoc * a / (2 adotrad^2)`,

`a^2 phi' ~= beta * grhoc * a^2 / (2 adotrad)`,

when the coupling term dominates the potential-gradient term. This is different from the upstream beta-independent uncoupled tracker `phi proportional to a^[4/(2+alpha)]`.

A separate preregistered diagnostic should compare the upstream tracker against this coupling-aware inner state at the same fixed `amin=1e-12`, without changing the background interpolation domain. Any such patched result remains diagnostic-only until validated by matched-asymptotic/independent-provider checks.