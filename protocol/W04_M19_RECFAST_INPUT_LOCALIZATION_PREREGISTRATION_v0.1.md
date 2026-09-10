# W04 M19 axionCAMB2 RECFAST input-localization preregistration v0.1

Date: 2026-09-10
Status: FROZEN BEFORE EXECUTION

## Scope
Provider is pinned exactly to `dgrin1/axionCAMB@891e779cc0bd422e49f97533e6c2fc761149737d`.

This is a bounded provider diagnostic only. It MUST NOT promote K1-K9 and MUST NOT be interpreted as physical falsification of fuzzy/ultralight-axion dark matter.

## Motivation fixed before result
The preceding zero-bypass + massive-neutrino-off isolation run `34518146927` executed all solver cases before its analyzer failed for an infrastructure-only missing-numpy dependency. Both exact-zero cases still segfaulted (`zf=139`, `zd=139`), while patched and untouched finite `axfrac=0.10` controls both exited zero. Runtime checking moved the first hard failure from the massive-neutrino interpolation path to `Recombination_xe`, `recfast_axion.f90:451`, where an invalid spline index is generated from `zst=(zinitial-z)/delta_z` after `z=1/a-1`.

## Frozen intervention
Reuse exactly the previously audited exact-zero bypass from `verification/m19/axioncamb2_zero_bypass_recovery.py` and exactly the preceding neutrino-off exact-zero configuration (`omnuh2=0`, `massive_neutrinos=0`, `nu_mass_eigenstates=0`). Do not change cosmological parameters, axion equations, recombination equations, thresholds, or finite control physics.

For the debug-only source copy, instrument `Recombination_xe(a)` immediately before `z=1/a-1` and immediately before `ihi=int(zst)` to print finite diagnostic scalars (`a`, `z`, `zst`, `zinitial`, `delta_z`) and abort deliberately before the invalid array access if any of `a`, `z`, or `zst` is non-finite or outside the interpolation-consistent domain. Instrumentation may observe/control-flow abort but may not alter returned physical values.

Build a second uninstrumented patched copy as execution control and retain the untouched finite `axfrac=0.10` control.

## Frozen classification
- `M19_RECFAST_INPUT_NONFINITE_LOCALIZED_WITH_SCOPE`: a non-finite or interpolation-invalid `a/z/zst` is observed before the legacy spline index conversion.
- `M19_RECFAST_INDEX_FAILURE_NOT_PRECURSOR_LOCALIZED`: all printed inputs are finite/in-domain but runtime checking still fails at the spline access.
- `M19_RECFAST_DIAGNOSTIC_BLOCKED`: build/instrumentation/harness prevents observation.

None of these classifications is a K1 PASS/FAIL or family-level scientific verdict.

## Next-gate rule
If a non-finite/invalid `a` reaches RECFAST, trace only the immediate caller chain to the earliest non-finite background/thermodynamic input in a separately preregistered diagnostic. Do not introduce epsilon axion density, change recombination physics, or tune initial conditions post hoc. If RECFAST inputs are finite and valid, audit the legacy interpolation bounds/index convention before any further provider execution.
