# W03/M07 gauge residual diagnosis

Date: 2026-09-09
Status: ACTIVE — precision-convergence audit running

## Frozen context

Model: M07 canonical scalar-field/quintessence.
Physical point used for the gauge regression: `lambda=0.075`, with the already calibrated strict shooting branch.
Pinned CLASS: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

The first paired synchronous/Newtonian audit used:
- `matter_source_in_current_gauge=no`;
- `get_perturbations_in_current_gauge=no`;
- `tol_perturbations_integration=1e-8`;
- `perturbations_sampling_stepsize=0.01`.

The preregistered raw-output gauge gate was `1e-4`; the residual `ln P(model/ref)` L2-relative gate was `5e-3`.

## Result of enriched baseline rerun

Raw physical outputs remain cross-gauge stable within the frozen `1e-4` criterion:

- reference P(k,z): max symmetric relative difference `7.6728316e-5`;
- M07 P(k,z): `7.6770126e-5`;
- reference d_m: `3.8371364e-5`;
- M07 d_m: `3.8392267e-5`;
- reference phi/psi: about `4.1358e-5`;
- M07 phi/psi: about `4.1275e-5`.

The derived response

`r_Delta = ln[P_M07/P_ref]`

fails the frozen residual-level gate:

- synchronous response norm: `6.6066815e-4`;
- Newtonian response norm: `6.5249404e-4`;
- absolute cross-gauge residual mismatch norm: `2.0475143e-5`;
- L2-relative residual mismatch: `0.03099157` (~3.10%).

## Common-mode diagnostic

For raw log-P gauge errors:

- reference gauge-error norm: `1.9583049e-4`;
- M07 gauge-error norm: `1.9698662e-4`;
- norm of `(model gauge error - reference gauge error)`: `2.0475143e-5`;
- cosine between reference and model gauge-error vectors: `0.99458349`.

Thus the gauge error is strongly common-mode between reference and M07. The small reconstructed response is a subtraction of two large, nearly equal spectra, so the residual-level relative metric amplifies the remaining numerical difference.

This observation does NOT retroactively convert the failed hard response gate into PASS.

## Preregistered next test

Workflow:
`.github/workflows/w03-m07-gauge-residual-precision-audit.yml`

Actions run:
`34390302626`.

The test repeats both gauges at two precision tiers:

- baseline: `tol_perturbations_integration=1e-8`, sampling step `0.01`;
- tight: `tol_perturbations_integration=1e-10`, sampling step `0.002`.

Frozen before seeing tight-tier output:

1. all tight raw physical outputs must still satisfy max symmetric relative difference `<=1e-4`;
2. tight residual L2-relative gauge mismatch must be at most `0.50` times the baseline mismatch.

Interpretation:
- if the mismatch contracts by the preregistered factor, the previous residual failure is identified as a precision-limited subtraction floor and B2 may be closed only in a precision-qualified scope;
- if it does not, B2 remains PARTIAL and the response representation/gauge quotient must be redesigned rather than loosening the threshold post hoc.

## Methodological carry-forward

A response defined as a difference or log-ratio of large nearly equal quantities requires convergence testing of the response itself. Cross-gauge convergence of each raw observable separately is necessary but not sufficient.
