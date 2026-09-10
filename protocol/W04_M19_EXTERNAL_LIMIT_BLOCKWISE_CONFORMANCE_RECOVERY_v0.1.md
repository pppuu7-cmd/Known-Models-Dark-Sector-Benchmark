# W04 M19 external-limit blockwise conformance recovery v0.1

## Status
Prospective analyzer-conformance repair. It implements the already frozen reporting contract in `W04_M19_EXTERNAL_CDM_REFERENCE_CONVERGENCE_PREREGISTRATION_v0.1.md`; no provider, cosmology, fraction, residual formula, interpolation rule, or convergence threshold changes.

## Trigger
Run `34536015822` completed all model/reference executions and evaluated the semantic transfer projection, but the v1 analyzer flattened the three CMB response columns and six transfer response columns into aggregate file-level residuals. The original preregistration requires robust norms separately for CMB TT/TE/EE and transfer columns.

## Frozen channel authority
At the pinned axionCAMB lineage, scalar output uses `Cl_scalar(C_Temp:C_Cross)` with `C_Temp=1`, `C_E=2`, `C_Cross=3`; therefore the four-column scalar file is `[ell, TT, EE, TE]`. The contemporaneous historical CAMB file uses the same classic convention.

The preregistered transfer-schema amendment already fixes the common transfer vector as `[kh, cdm, b, g, r, nu, tot]`.

## Frozen analyzer repair
Evaluate convergence gates independently for:
- CMB `TT`, `EE`, `TE`;
- matter power `Pk`;
- transfer `cdm`, `b`, `g`, `r`, `nu`, `tot`.

The coordinate columns `ell` and `kh` are never residual channels. TE retains the already frozen near-zero numerical-floor rule through the same symmetric residual implementation. Overall K1 promotion still requires every retained response block to pass the unchanged gates.

## Interpretation
This repair can only make the gate stricter/more diagnostic relative to accidental file-level flattening. It cannot rescue a failing channel through averaging with a passing channel and cannot by itself constitute physical falsification.
