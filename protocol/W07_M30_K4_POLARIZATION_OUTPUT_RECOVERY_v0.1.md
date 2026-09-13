# W07 M30 K4 polarization-output recovery v0.1

## Trigger
The authoritative M30 local-2D K4 production run `34719607382` completed the frozen `base`, `radial`, and `cT` point ladders under exact pinned hi_class commit `0009f51d89e6465c79e570b496c66fc90058fa77`. Subsequent analysis-only recovery run `34741839442` established that the immutable C_ell products contain only `ell+TT`, while the prospectively frozen K4 observable basis in `W07_M30_K4_LOCAL_2D_PRECISION_PREREGISTRATION_v0.1.md` requires TT, EE, TE, and P(k). Therefore K4 remains NOT_ESTABLISHED due to a harness output-request omission; the missing EE/TE channels cannot be reconstructed from the immutable TT-only artifacts.

This is a harness/output-request blocker, not a numerical-robustness failure and not physical falsification.

## Frozen science
The following are unchanged from the original prospective K4 protocol and production workflow:

- model/family: M30/F30 Horndeski effective-alpha subspace;
- provider: `hiclass-code/hi_class_public`;
- exact provider commit: `0009f51d89e6465c79e570b496c66fc90058fa77`;
- physical points: `base`, `radial`, `cT` with the exact original `parameters_smg` construction;
- precision profiles: provider default, `cl_permille.pre`, `cl_ref.pre`;
- cosmological/provider configuration apart from the output request described below;
- observables required by the original K4 gate: TT, EE, TE, P(k);
- numerical statistic, common-grid handling, thresholds, point gate, aggregate gate, and all classification strings in `verification/m30/k4_local_2d_precision.py`;
- `fail-fast:false` three-point parallelization and aggregate barrier.

No physical parameter, precision value, grid, threshold, provider source, stability rule, or classification criterion may be changed after results are seen.

## Sole permitted recovery change
For every generated INI in each physical point/profile, replace the output request with the provider-native request

`output = tCl,pCl,mPk`

so that the already-preregistered EE and TE channels are actually computed in addition to TT and P(k). No other scientific setting may change.

Because this output request changes what the solver computes, this recovery must rerun the nine required solver cases (3 physical points x 3 precision profiles). The three physical points are independent and must run in parallel with `fail-fast:false`; the aggregate must wait for all point jobs.

The recovery harness may expose hi_class's native `*_00_cl.dat` / `*_00_pk.dat` products under the unchanged analyzer filenames `*_cl.dat` / `*_pk.dat` only by byte-identical copy after each successful solver call. This is path normalization only.

## Prospective classification
After the explicit three-point barrier, apply the unchanged original analyzer:

- if all required solver/profile executions succeed and all three point gates pass: `M30_K4_PASS_WITH_SCOPE_LOCAL_2D_PROVIDER_PRECISION_LADDER`;
- if all mandatory channels execute but any frozen numerical gate fails: `M30_K4_NUMERICAL_ROBUSTNESS_NOT_ESTABLISHED_LOCAL_2D`;
- if any provider/profile execution fails, a mandatory TT/EE/TE/P(k) channel is absent/non-finite, or path normalization cannot be byte-verified: `M30_K4_PROVIDER_OR_PRECISION_EXECUTION_BLOCKED`.

A green GitHub workflow is not by itself a scientific PASS. K4 promotion is allowed only from the machine result produced by the unchanged frozen analyzer.

## Prohibited interpretations
- Missing/failed channels are never zero-imputed.
- Provider/configuration/infrastructure failure is not physical failure.
- This local-2D K4 test does not establish full Horndeski-family validity, observational discrimination, K5-K9, or any global KMDSB sufficiency/new-model conclusion.
