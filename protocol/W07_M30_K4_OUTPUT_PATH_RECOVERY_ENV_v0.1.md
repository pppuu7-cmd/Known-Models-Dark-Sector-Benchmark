# W07 M30 K4 analysis-environment recovery v0.1

## Trigger
Analysis-only output-path recovery run `34741703242` successfully downloaded the immutable M30 parent artifacts and reached the unchanged frozen analyzer, but every point job stopped before scientific classification with `ModuleNotFoundError: No module named 'numpy'` in `verification/m30/k4_local_2d_precision.py`.

This is an analysis-runner dependency defect only. It is not solver, provider, numerical-convergence, or physical evidence.

## Frozen evidence and science
All frozen evidence, provider pin, local points, precision profiles, observables, thresholds, convergence rules, and classification logic remain exactly as preregistered in `protocol/W07_M30_K4_OUTPUT_PATH_RECOVERY_v0.1.md`. No cosmology/provider computation may be rerun.

## Allowed intervention
Install exactly `numpy==2.3.3`, matching the repository's established analysis-only recovery convention, immediately before invoking the unchanged analyzer. Then rerun only the three analysis-only point recoveries and their aggregate barrier over the same immutable parent artifacts from run `34719607382`.

No other package, source file, input, threshold, or scientific rule may be changed.

## Fail closed
A package-installation failure or any later harness/environment failure remains infrastructure blocked and cannot be interpreted as M30 K4 failure or physical falsification. Only the unchanged frozen aggregate gate may promote K4.