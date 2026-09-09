# M07 gauge/bookkeeping audit

Date: 2026-09-09  
Primary Actions run: `34360101877`  
Artifact: `w03-m07-gauge-bookkeeping-audit`  
Artifact digest: `sha256:4bb66d2be2fcfc9c4570789d71c47a060b6537340fd5f45a1bca895ce6c159f3`  
Status: **PARTIAL / RESPONSE-LEVEL GAUGE GATE FAILED; RAW PHYSICAL OUTPUT REGRESSION PASSED**

## Frozen setup

Paired internal solver gauges:
- synchronous;
- Newtonian.

Same M07 point: `lambda=0.075`, strict shooting and tight perturbation settings.

Output conventions were deliberately frozen to gauge-independent / common representations:
- `matter_source_in_current_gauge=no`;
- `get_perturbations_in_current_gauge=no`.

Frozen gates before execution:
- raw output max symmetric relative difference <= `1e-4`;
- derived `lnP(model/reference)` response L2 relative difference <= `5e-3`.

## Raw-output results

All raw physical-output regressions pass the `1e-4` threshold.

| output | reference max relative | M07 max relative | gate |
|---|---:|---:|---|
| P(k,z) | `7.67283e-5` | `7.67701e-5` | PASS |
| d_m | `3.83714e-5` | `3.83923e-5` | PASS |
| phi | `4.13578e-5` | `4.12752e-5` | PASS |
| psi | `4.13578e-5` | `4.12752e-5` | PASS |

The internal gauge choice therefore does not produce an O(1) change in the physical outputs under the frozen output conventions.

## Derived residual response

For

`r_Delta = ln[P_M07/P_REF]`,

the synchronous/Newtonian comparison gives:
- max symmetric relative difference `0.0971296`;
- L2 relative difference `0.0309916`.

The preregistered `5e-3` response gate therefore **FAILS**.

## Interpretation

This failure is retained exactly as observed. It is not reclassified as a pass and its threshold is not loosened.

However, it is also not evidence that the underlying physics is gauge dependent. The raw `P`, `d_m`, `phi`, and `psi` outputs all pass the independent raw-output gauge threshold. The response is much smaller than the parent spectra, so subtracting/log-ratioing two nearly equal large outputs can amplify a common numerical gauge-regression floor into a percent-level relative error in the residual itself.

B2 therefore remains `PARTIAL`: raw physical-output bookkeeping is clean within the frozen threshold, while response-level gauge robustness is unresolved.

## Diagnostic continuation

The analyzer was upgraded to record:
- absolute response mismatch norm;
- response norms in both gauges;
- raw log-P gauge-error norms for reference and model;
- cosine/common-mode correlation between reference and model gauge errors.

A same-configuration diagnostic rerun was triggered by commit `a4885176054303ae0d17a908d40aed7660eac7ad`. This rerun does not replace or erase the primary failed gate; it only quantifies whether the residual failure is dominated by common-mode numerical subtraction.

If common-mode correlation is high, the next hard test must be a separately preregistered **gauge precision-convergence** run. It may tighten solver/perturbation precision, but it may not weaken the original `5e-3` threshold post hoc.

## Methodological consequence

A small reconstructed residual requires its own numerical invariance calibration. Gauge invariance of the large parent observables does not automatically guarantee a numerically stable gauge-invariant residual after subtraction.

Future model construction must therefore validate both:
1. parent observable invariance;
2. residual-response invariance at the scale on which the residual itself is interpreted.
