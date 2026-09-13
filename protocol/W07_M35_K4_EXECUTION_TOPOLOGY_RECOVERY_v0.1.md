# W07 M35 K4 execution-topology recovery v0.1

Status: FROZEN BEFORE RECOVERY RESULT

## Trigger

The prospectively frozen M35/F35 local-2D provider-precision workflow `w07-m35-k4-local-2d-precision.yml` was attempted twice in run `34741545139`. In both attempts the exact pinned CLASS_LVDM build and the frozen three-point / three-profile configuration stage completed, while the single job terminated during the step that executes all nine frozen solver cases. Attempt 2 is job `103707189468`; the downstream unchanged analyzer and artifact upload were skipped. No machine scientific classification exists from that run.

The execution step itself was written with `set +e` and an explicit final `exit 0`, so a job-level failure inside that step is not an admissible scientific/provider classification. It is an execution-topology/infrastructure blocker until individual frozen cases are isolated.

## Frozen science

This recovery MUST preserve without modification:

- provider `Michalychforever/CLASS_LVDM` branch `LVDM` at exact commit `d9a20bd0c7b7a6c8957410fd245ed06b30b915c1`;
- physical points exactly as preregistered: `base=(q=0.100,Y_dm=0)`, `gravity=(q=0.102,Y_dm=0)`, `Y=(q=0.100,Y_dm=0.002)` with `alpha=0.05q`, `beta=0.25q`, `lambda=-0.10q`;
- mandatory outputs `tCl,pCl,lCl,mPk`;
- exact provider precision profiles `default`, `cl_permille.pre`, `cl_ref.pre` and the existing parser-compatible merge rule;
- the original analyzer `verification/m35/k4_local_2d_precision.py`, its TT/EE/TE/P(k) metrics, gates and classifications;
- no physical retuning, no threshold change, no channel masking beyond the already frozen analyzer.

## Permitted execution-only change

The nine independent frozen solver cases are split across a matrix with `fail-fast:false` after one exact-pin build/configuration barrier. The build/configuration bundle may be transferred byte-for-byte by GitHub artifact to the matrix jobs. Each matrix job executes exactly one already-frozen INI from the provider working directory and records its return code plus stdout/stderr/output files. No case may condition the configuration of another case.

After all nine matrix jobs reach terminal state, an explicit aggregate barrier reconstructs `status.json` and invokes the unchanged preregistered analyzer exactly once. A solver nonzero return code is consumed as provider/profile execution evidence by the analyzer; a runner/infrastructure interruption is not silently converted to physics.

## Frozen classification

- all required executions finite and every original numerical gate passes -> `M35_K4_PASS_WITH_SCOPE_LOCAL_2D_PROVIDER_PRECISION_LADDER`;
- all required executions complete but any original numerical gate fails -> `M35_K4_NUMERICAL_ROBUSTNESS_NOT_ESTABLISHED_LOCAL_2D`;
- any required provider/profile execution/output is unavailable -> `M35_K4_PROVIDER_OR_PRECISION_EXECUTION_BLOCKED`.

All outcomes retain `physical_falsification=false`. A green workflow is not itself a scientific PASS.
