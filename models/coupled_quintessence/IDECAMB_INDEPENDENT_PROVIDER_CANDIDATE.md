# M14 independent perturbation-complete provider candidate: IDECAMB

Date: 2026-09-10
Status: `PROVIDER_BUILD_PASS_SOURCE_CLOSURE_WITH_SCOPE_K1_EXECUTION_NEXT`

## Immutable provider

Patch: `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`.

Base compatibility anchor: `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4` from the author-specified `planck2018` line.

The IDECAMB README explicitly states that it supplies coupled quintessence (CQ) and coupled-fluid models, and instructs users to copy all patch files into CosmoMC-planck2018 and overwrite same paths. `test_ide.ini` defines `Class_IDE=2` as coupled quintessence, with `alpha_quint` and `beta_cq` as the CQ parameters.

## Provider-control result

Prospective provider control: `protocol/W03_M14_IDECAMB_PROVIDER_CONTROL_PREREGISTRATION_v0.1.md`.

Run `34452683017`, job `102791799552`, artifact `10142180500` performed the exact literal overlay. GNU Fortran 13.3.0 reached `camb/equations_ppfi.f90` but rejected legacy `dverk` argument mismatches; no physics execution occurred. This was classified compiler compatibility only.

A separately frozen compiler recovery added only gfortran's legacy compatibility flag `-fallow-argument-mismatch`; no Fortran source or cosmological parameter changed. Run `34452783661`, job `102792130632`, artifact `10142233561` completed with build exit 0 and produced the `cosmomc` executable. Classification: `M14_IDECAMB_PROVIDER_BUILD_PASS_COMPAT_FLAG`.

Canonical machine record: `waves/wave_03_expanded_dark_energy/M14_IDECAMB_PROVIDER_CONTROL_RESULT.json`.

## Source-bound CQ physics / decoupling map

For the implemented exponential coupling branch (`QForm_CQ=1`):

- CDM background density is
  `grhoca2_CQ = grhoc/a * exp(-beta*(gphi-gphi0))`;
- energy transfer is
  `Coup_CQ = beta * grhoc_t * gphidot`;
- scalar background evolution calls this same `Coup_CQ` in `Eqs_CQ`;
- `PerturCoupC_CQ` obtains its perturbation-transfer coefficients from the same `gQ=Coup_CQ(...)`;
- `PerturCoupD_CQ` likewise returns a `gD` built from `gQ`;
- the active scalar perturbation routine `derivs` calls `IDEout(...,gQ,gC,gD,...)`, so the coupling perturbation objects are on the live perturbation path rather than commented placeholders;
- `Class_IDE=2` disables the fluid PPF shortcut and selects the coupled-quintessence evolution.

Thus the source-level total interaction-off map for this branch is exact at `beta_cq=0`: the exponential CDM factor becomes unity, `gQ=0`, and hence CQ `gC/gD` interaction terms vanish, while `alpha_quint` may remain nonzero. The correct K1 comparator is therefore the same scalar-potential model with uncoupled CDM, not LambdaCDM unless alpha is separately taken to its own null limit.

## K3 interpretation

This provider is materially stronger than the first `kabeleh/iDM` route: both background exchange and perturbation-transfer objects are active in the executable equations, and the perturbation integrator consumes them. This supports `K3_SOURCE_COMPLETE_WITH_SCOPE` for the implemented exponential-coupling branch.

It is not yet a numerical K3/K5 PASS: an executable CQ theory point and beta->0 regression must still be demonstrated, and conservation residuals have not yet been numerically audited.

The alternative power-law coupling branch is explicitly `Not supported currently` and is outside scope.

## Execution limitation to resolve prospectively

The author-documented invocation is `./cosmomc test_ide.ini`. The committed `test_ide.ini` loads Planck 2018, lensing, BAO and Pantheon likelihood defaults, so a clean theory execution may be blocked by external likelihood data not contained in the two pinned source repositories. Do not silently delete likelihoods and call that an author control.

The base CAMB tree has a standalone `camb` target, but IDECAMB's CQ parameter binding (`Class_IDE`, `alpha_quint`, `beta_cq`) is implemented through the CosmoMC-side parameterization/calculator overlay. Therefore a standalone CAMB run must not be assumed equivalent without a source-documented binding path.

## Next prospectively allowed gate

1. Attempt the unmodified author `test_ide.ini` only as a provider-execution probe and preserve whether any failure is solely missing external likelihood data.
2. If external data block it, search the pinned provider or cited release/materials for an author-supported theory-only CosmoMC/CAMB configuration; do not invent one.
3. Once a valid executable CQ route exists, separately preregister K1 at `beta_cq=0` versus the identical uncoupled scalar+CDM comparator.
4. Only after K1 numerical PASS, audit beta physical geometry and launch K2-K5 convergence/response tests.

No result here is a physical falsification or observational discrimination of coupled quintessence.
