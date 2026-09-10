# W03 M14 IDECAMB provider-control preregistration v0.1

Date: 2026-09-10
Scope: infrastructure/provenance only; no K1-K9 scientific promotion.

## Immutable providers

- patch: `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`
- base: `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4` (`planck2018` compatibility anchor resolved prospectively)

## Author installation map

IDECAMB README says to copy all patch files into CosmoMC-planck2018 and overwrite same paths. The control therefore clones both exact commits and performs a literal recursive copy of the patch tree over the base tree. No source edits, file renames, physics edits or inferred patching are allowed.

## Frozen control

1. verify both HEADs equal the pins above;
2. overlay the patch literally;
3. verify expected overwritten files exist (`camb/equations_ppfi.f90`, `source/Calculator_CAMB.f90`, `source/CosmologyParameterizations.f90`, `source/CosmologyTypes.f90`, `source/Makefile`, `test_ide.ini`);
4. attempt `make cosmomc BUILD=` with GNU Fortran/BLAS/LAPACK available;
5. preserve build log, exit code, compiler version and post-overlay checksums.

`BUILD=` is an infrastructure choice to avoid requiring MPI for this compile control; it does not alter cosmological equations or parameters.

## Classification

- build exit 0 and executable `cosmomc` present: `M14_IDECAMB_PROVIDER_BUILD_PASS`;
- overlay succeeds but compilation fails: `M14_IDECAMB_BLOCKED_BUILD`, with exact diagnostics retained;
- missing/incompatible files before compile: `M14_IDECAMB_BLOCKED_OVERLAY_PROVENANCE`.

A green workflow is not itself a PASS: classification must consume the build exit/log.

## Explicit non-authorization

This gate does not authorize K1 decoupling, K2 geometry, K3 conservation/perturbation closure, K4 convergence, K5 response/rank, K6 comparator attack, K7 observation projection, K8 novelty or K9 holdout. If build PASSes, next gate is source-level CQ closure and beta->0 map audit, followed by a separately preregistered theory execution/control if feasible.
