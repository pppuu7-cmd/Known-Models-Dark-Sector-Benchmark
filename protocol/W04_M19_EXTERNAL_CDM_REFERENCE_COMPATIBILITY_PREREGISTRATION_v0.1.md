# W04 M19 historical-CAMB compatibility repair preregistration v0.1

Date: 2026-09-11
Status: FROZEN BEFORE EXECUTION

## Trigger evidence
The prospectively frozen external-CDM convergence run `34534753238` used
`dgrin1/axionCAMB@891e779cc0bd422e49f97533e6c2fc761149737d` for the finite ULA sequence and
`cmbant/CAMB@dc437acd8c90aa7e5595fcb25c615b03de8357a7` for the external pure-CDM comparator.
All five finite ULA cases `f_ax={0.10,0.03,0.01,0.003,0.001}` built and executed (`a0..a4=0`).
The historical CAMB comparator failed at compile time (`build_cdm=2`; `c0` not executed).
The first hard compiler diagnostic is in `equations.f90`, subroutine `outtransf(EV,y,Arr)`: modern GNU Fortran reports `EV` as an ambiguous reference. This is a source-language/compiler compatibility blocker, not a scientific result.

## Frozen intervention
Keep both provider commits, cosmology, finite fractions, outputs, comparison metrics and all scientific gates exactly unchanged from
`protocol/W04_M19_EXTERNAL_CDM_REFERENCE_CONVERGENCE_PREREGISTRATION_v0.1.md`.

For the historical CAMB working tree only, apply one mechanical source-compatibility transformation to the single subroutine `outtransf` in `equations.f90`:

- rename the dummy argument/local identifier `EV` to `EVout` throughout that subroutine only;
- do not change any expression, literal, branch, array index, equation, parameter, numerical threshold, module import, output definition or neighboring subroutine;
- assert that the transformation is restricted between `subroutine outtransf` and `end subroutine outtransf` and archive the exact `git diff`.

Compiler/linker selection may remain the already-audited GNU compatibility override (`gfortran`, legacy dialect / argument-mismatch compatibility). No other provider-source patch is authorized.

## Frozen classification
1. If the comparator still does not build or execute, classify `M19_EXTERNAL_CDM_REFERENCE_COMPATIBILITY_BLOCKED`; no K1 promotion and no physical falsification.
2. If comparator build/execution succeeds, consume the unchanged external-CDM convergence analyzer. Only the pre-existing convergence protocol may classify `M19_EXTERNAL_CDM_REFERENCE_CONVERGENCE_PASS_WITH_SCOPE`.
3. A green workflow alone is not a scientific PASS; the machine result and archived products must be consumed against the frozen gate.

## Next-gate rule
If the compatibility-only comparator executes, evaluate the already frozen per-block convergence metrics. If any block fails, first distinguish a cross-solver baseline/output-convention mismatch from true non-convergence; do not retune fractions or thresholds post hoc. If compatibility remains blocked, stop patching this historical CAMB route and seek another independently pinned pure-CDM comparator from the same lineage or a documented build environment.
