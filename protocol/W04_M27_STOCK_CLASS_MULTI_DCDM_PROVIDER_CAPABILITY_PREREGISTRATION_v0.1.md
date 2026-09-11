# W04 M27 stock-CLASS multi-DCDM provider capability preregistration v0.1

## Purpose
The M27 high-L daughter-radiation hierarchy refinement passed on all 27 frozen ensemble branches at L32->L64, but that verification still uses a prescribed metric forcing. Before implementing a new self-consistent Einstein-Boltzmann closure, test whether the already pinned official CLASS provider can represent an ensemble of independently decaying cold parent species with distinct decay rates without source modification.

This is a provider-capability/provenance gate only. It cannot promote K1, K3, K4 or falsify dynamical dark matter.

## Immutable provider
- repository: `lesgourg/class_public`
- commit: `e85808324f51fc694d12e3ed7439552a3c3f9540`

## Parallel controls
Two independent jobs are required with `fail-fast:false` semantics at the workflow level.

### A. Source capability audit
Inspect the pinned parser/background/perturbation source for the native DCDM->DR implementation. Record:
- whether the decay rate is represented as a scalar or an indexed/list quantity;
- whether background DCDM densities are scalar or indexed over independently decaying parents;
- whether perturbation variables/source terms loop over independently decaying DCDM parents;
- whether the input parser exposes a documented way to supply at least two independent decay rates and abundances.

`NATIVE_MULTI_DCDM_CAPABLE` requires all of the following source-level conditions simultaneously:
1. at least two independently parameterizable DCDM parent abundances;
2. at least two independently parameterizable decay rates;
3. background evolution loops/indexes those parents separately;
4. perturbation/source evolution loops/indexes those parents separately;
5. no source-code modification is needed to instantiate N>=2.

Otherwise classify source capability as `NATIVE_MULTI_DCDM_NOT_EXPOSED`.

### B. Provider execution control
Build the exact pinned source using the repository's ordinary build path and execute a standard one-species DCDM->DR case. This control only establishes that the pinned provider/build is functional. It does not test the ensemble model.

The control passes if the executable exits 0 and creates finite background plus linear perturbation/spectrum output for a nonzero DCDM abundance and finite decay rate.

## Aggregate classification
- `M27_STOCK_CLASS_NATIVE_MULTI_DCDM_PROVIDER_AVAILABLE_WITH_SCOPE` only if the source capability audit is `NATIVE_MULTI_DCDM_CAPABLE` and the one-species provider control passes.
- `M27_STOCK_CLASS_MULTI_DCDM_PROVIDER_UNAVAILABLE` if the provider control passes but source capability is `NATIVE_MULTI_DCDM_NOT_EXPOSED`.
- `M27_STOCK_CLASS_PROVIDER_CAPABILITY_AUDIT_BLOCKED` for build/configuration/audit infrastructure failure.

No result is a physical DDM FAIL. No post-hoc patch adding extra species is authorized by this gate.

## Continuation rule
If native multi-DCDM support is unavailable, the next self-consistent metric route must be either (a) a different pinned public provider with documented multi-parent decay support or (b) a separately preregistered independent verification implementation from the covariant component equations. Do not silently convert stock single-DCDM CLASS into an M27 ensemble provider.
