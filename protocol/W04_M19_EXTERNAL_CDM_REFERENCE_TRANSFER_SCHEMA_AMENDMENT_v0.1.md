# W04 M19 external CDM reference transfer-schema amendment v0.1

## Status
Prospective infrastructure/output-schema amendment. It changes no cosmological input, provider pin, finite axion fraction, convergence threshold, residual definition, or scientific acceptance rule in `W04_M19_EXTERNAL_CDM_REFERENCE_CONVERGENCE_PREREGISTRATION_v0.1.md`.

## Trigger
Run `34535087322` reached successful build and execution for all five finite axionCAMB cases and the independent historical CAMB reference, then stopped before any convergence classification because the transfer files have different provider-specific column counts (axionCAMB: 9; historical CAMB: 7).

## Exact semantic authority
At the frozen axionCAMB pin `dgrin1/axionCAMB@891e779cc0bd422e49f97533e6c2fc761149737d`, `modules.f90` defines:

1. `Transfer_kh`
2. `Transfer_cdm`
3. `Transfer_b`
4. `Transfer_g`
5. `Transfer_r`
6. `Transfer_nu`
7. `Transfer_axion`
8. `Transfer_f`
9. `Transfer_tot`

At the frozen historical CAMB pin `cmbant/CAMB@dc437acd8c90aa7e5595fcb25c615b03de8357a7`, `modules.f90` defines:

1. `Transfer_kh`
2. `Transfer_cdm`
3. `Transfer_b`
4. `Transfer_g`
5. `Transfer_r`
6. `Transfer_nu`
7. `Transfer_tot`

Therefore raw column equality is not a valid comparison contract.

## Frozen common transfer projection
Before interpolation/residual calculation, project both transfer products onto the response-common semantic vector

`[kh, cdm, b, g, r, nu, tot]`.

Historical CAMB uses raw columns `[1,2,3,4,5,6,7]`.
AxionCAMB uses raw columns `[1,2,3,4,5,6,9]`.

Axion-only `Transfer_axion` and `Transfer_f` are provider-specific observables with no pure-CDM counterpart. They are excluded/masked, never set to zero and never substituted for `Transfer_tot`.

## Guardrails
- Require exactly 9 columns for finite axionCAMB transfer files and exactly 7 columns for the historical CAMB transfer file in this frozen test. Any other schema is `OUTPUT_SCHEMA_BLOCKED`.
- Keep `kh` as the interpolation coordinate and compare the six common response columns only.
- CMB and matter-power analysis are unchanged.
- No extrapolation; use only the strict overlap domain.
- All original convergence gates remain unchanged.

## Interpretation
This amendment repairs only a semantic output-schema mismatch discovered before any M19 external-limit convergence statistic was evaluated. It cannot turn a scientific non-convergence into a pass and does not by itself promote K1.
