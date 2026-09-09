# M07 paired-gauge bookkeeping audit — baseline tight-tier result

Date: 2026-09-09  
Status: **PARTIAL PASS / RESPONSE GATE FAIL**  
Run: `34360101877`  
Artifact: `w03-m07-gauge-bookkeeping-audit`  
Artifact ID: `10107486807`  
Artifact digest: `sha256:4bb66d2be2fcfc9c4570789d71c47a060b6537340fd5f45a1bca895ce6c159f3`.

## Frozen setup

M07 point: `lambda=0.075` on the strict shooting branch.

Paired internal gauges:
- synchronous;
- Newtonian.

Both used:
- `tol_shooting_deltax_rel=1e-13`;
- `tol_perturbations_integration=1e-8`;
- `perturbations_sampling_stepsize=0.01`;
- `matter_source_in_current_gauge=no`;
- `get_perturbations_in_current_gauge=no`.

Thus exported matter and perturbation quantities are requested in CLASS's gauge-invariant/common output conventions rather than deliberately exposing raw current-gauge matter sources.

Preregistered gates:
- maximum symmetric relative difference for each raw exported quantity <= `1e-4`;
- L2 relative difference of the derived response `ln(P_M07/P_ref)` <= `5e-3`.

The thresholds are immutable after this result.

## Raw exported quantities — PASS

All raw cross-gauge regressions satisfy the `1e-4` gate:

| quantity | max symmetric relative difference |
|---|---:|
| reference P | `7.67283e-5` |
| M07 P | `7.67701e-5` |
| reference d_m | `3.83714e-5` |
| M07 d_m | `3.83923e-5` |
| reference phi | `4.13578e-5` |
| M07 phi | `4.12752e-5` |
| reference psi | `4.13578e-5` |
| M07 psi | `4.12752e-5` |

This is evidence that the two internal-gauge realizations reproduce the exported physical/GI quantities at the preregistered raw level.

## Derived small response — FAIL

For

`r_P = ln(P_M07/P_ref)`

computed separately in each internal gauge, the cross-gauge result is:

- maximum symmetric relative difference: `0.09713`;
- L2 relative difference: `0.0309916`.

The frozen response gate was `0.005`, so it fails by about a factor 6.2.

## Interpretation

This failure is not a physical inconsistency of canonical quintessence and is not evidence that physical P(k) is gauge dependent. The raw reference and M07 spectra independently pass the gauge regression.

The failure occurs after subtracting/dividing two nearly identical large quantities to obtain a small response. A small residual can amplify tiny gauge/integration realization differences that are negligible in each raw observable.

The correct status is therefore:
- raw exported gauge bookkeeping: `PASS_WITH_SCOPE`;
- response-level gauge regression: `FAIL` at the frozen numerical tier;
- M07 B2 overall remains `PARTIAL` pending one predeclared numerical diagnostic.

## One-diagnostic rule

W03 permits exactly one additional paired-gauge numerical-convergence diagnostic with:
- unchanged physical model and grids;
- unchanged raw `1e-4` gate;
- unchanged response `5e-3` gate;
- tighter numerical integration/sampling only;
- no further threshold relaxation or iterative tuning after that diagnostic.

If the unchanged response gate still fails, B2 remains `PARTIAL/INCONCLUSIVE` and W03 carries the limitation forward rather than tuning it away.

## Methodology consequence

Gauge invariance of raw observables does not automatically imply numerical gauge stability of a small *difference response*. Gauge bookkeeping audits for near-reference models must test both raw exported quantities and the residual/quotient actually used by DSIR.
