# W04 M19 low-fraction floor decomposition preregistration v0.1

## Purpose
Diagnose the already observed non-zero residual floors in the M19 external-CDM convergence test without changing the frozen K1 convergence gate and without interpreting any provider mismatch as physical fuzzy/ultralight-axion falsification.

This diagnostic uses only the immutable raw outputs from Actions run `34536498517` / artifact `10175630339` produced under the frozen external-CDM protocol. It does not rerun or retune cosmology, axion mass, fractions, solver pins, transfer schema, thresholds, or normalization.

## Inputs
Finite ULA provider: `dgrin1/axionCAMB@891e779cc0bd422e49f97533e6c2fc761149737d`.
External pure-CDM reference: historical `cmbant/CAMB@dc437acd8c90aa7e5595fcb25c615b03de8357a7` with the preregistered compatibility-only `outtransf` identifier repair already used in run `34536498517`.

Frozen fractions are `f_ax={0.10,0.03,0.01,0.003,0.001}` at `m_ax=1e-27 eV`.

Analyze the same physically common blocks already defined by the blockwise analyzer: `CMB_TT`, `CMB_TE`, `CMB_EE`, `Pk`, `T_cdm`, `T_b`, `T_g`, `T_r`, `T_nu`, `T_tot`. Axion-only transfer columns remain excluded.

## Low-fraction asymptote fit
For every common physical sample/coordinate independently, use only the three smallest fractions `f={0.01,0.003,0.001}` and fit

`X(f) = b + a f`

by ordinary least squares in the native output variable after interpolation onto the same strict-overlap coordinate grid used by the frozen external-CDM analyzer. No extrapolation in k/ell is allowed.

`b` is a diagnostic estimate of the finite-provider `f_ax -> 0` asymptote. It is not declared to be an exact axionCAMB zero-density execution.

## Metrics
For each block report:

1. `external_floor_p95`: p95 symmetric relative residual between fitted asymptote `b` and the historical pure-CDM reference, using the same numerical floor convention as the frozen convergence analyzer.
2. `finite_effect_p95(f)`: p95 symmetric relative residual between each finite low-fraction output and the fitted asymptote `b` for `f={0.01,0.003,0.001}`.
3. `finite_effect_exponent`: log-log slope of `finite_effect_p95 ~ f^p` over those three points when all values are positive.
4. `fit_error_p95`: p95 symmetric relative residual of the fitted values `b+a f` against the three low-fraction outputs.
5. `two_point_asymptote_shift_p95`: p95 symmetric relative residual between the three-point OLS asymptote and the straight-line asymptote determined only by `f={0.003,0.001}`.

## Prospectively frozen diagnostic classification
A block is `BASELINE_FLOOR_DOMINANT_WITH_SCOPE` only if all are true:

- `finite_effect_p95` decreases from 0.01 -> 0.003 -> 0.001;
- `finite_effect_exponent > 0.5`;
- `external_floor_p95 >= 3 * finite_effect_p95(0.001)`;
- `fit_error_p95 <= finite_effect_p95(0.001)`;
- `two_point_asymptote_shift_p95 <= external_floor_p95`.

A block is `INTERNAL_LIMIT_CONVERGENT_BUT_BASELINE_NOT_DOMINANT` if the first two conditions hold but the baseline-dominance/stability conditions do not all hold.

Otherwise it is `LOW_FRACTION_LIMIT_NOT_DIAGNOSTICALLY_RESOLVED`.

## Interpretation guardrail
This diagnostic can establish that some failing frozen cross-provider blocks are dominated by a solver/reference baseline floor while the finite ULA perturbation itself approaches a stable provider-internal limit. It cannot promote K1, cannot erase the frozen `M19_EXTERNAL_CDM_REFERENCE_CONVERGENCE_NOT_ESTABLISHED` result, and cannot validate the crashing exact-zero axionCAMB path.

If the diagnostic isolates a baseline floor, the next scientifically allowed step is a separately preregistered matched-baseline calibration or independent modern implementation with an executable exact CDM limit. If it does not isolate the floor, M19 K1 remains blocked/open without physical-failure language.
