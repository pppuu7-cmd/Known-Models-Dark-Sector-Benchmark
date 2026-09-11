# W04 M27 DDM energy-transfer JSON serialization recovery preregistration v0.1

## Trigger

Run `34555410796` launched the complete frozen 27-branch cosmological energy-transfer matrix. Every branch failed at the same final output-writing statement after the solver/result object had been constructed:

`TypeError: Object of type bool is not JSON serializable`.

The traceback originates in `json.dumps(r, ...)` because one or more gate values are NumPy scalar booleans rather than native Python booleans. This is an evidence-serialization failure, not a solver or physical-model failure. The failed workflow also skipped artifact upload after the step error, so run `34555410796` is not admissible as scientific evidence for the energy-transfer gate.

## Frozen recovery

No physical or numerical quantity may change. Reuse exactly the parent preregistration:

`protocol/W04_M27_DDM_COSMOLOGICAL_ENERGY_TRANSFER_PREREGISTRATION_v0.1.md`.

Keep unchanged:

- all 27 `(delta,y,Gamma0/H*)` branches;
- N=64, mass/width/abundance construction;
- cosmological normalization and initial scale factor;
- DOP853 integrator;
- `rtol=1e-10`, `atol=1e-12`;
- 4001 log-scale-factor evaluation points;
- direct N=1 DCDM reference equations;
- all positivity, monotonicity, conservation and reference thresholds.

The sole allowed implementation repair is to convert NumPy scalar values (`np.bool_`, `np.integer`, `np.floating`) to native JSON-serializable Python scalar types at serialization time. No array values or gate logic may be changed.

The artifact-upload step must also use `if: always()` so that future execution failures retain diagnostics.

## Execution

Rerun all 27 independent branches concurrently through the same matrix. The recovery result for each branch must carry both the parent preregistration and this serialization-recovery preregistration in provenance.

## Scientific semantics

Only recovered, successfully serialized branch results may enter the aggregate gate. The parent failed run is recorded as `SERIALIZATION_BLOCKED_NO_EVIDENCE` and is not counted as a physical or numerical-model result.

`K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false` unless and until the unchanged parent gates are successfully evaluated.
