# M04 — Thermal warm dark matter (WDM) block-mask audit

Date: 2026-09-08  
Wave: `wave_01_baseline_atlas`  
DSIR authority: `pppuu7-cmd/Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`

## Tested scope

Frozen DSIR C4 thermal-WDM control. This model is used to stress-test response-block masking because the low-k DSIR block is intentionally almost blind while the high-k transfer/growth block carries the physical cutoff.

Frozen DSIR facts include:
- for 3 keV WDM, `r_T(k=0.1 h/Mpc) = -3.46e-6`;
- for the same model, `r_T(k=10 h/Mpc) = -0.10375`;
- later pinned CLASS runs for 2, 3 and 5 keV provide six high-k nodes across seven redshifts;
- on that frozen linear high-k domain the response is nearly time-separable (`chi_I ~ 2e-10`);
- a preregistered interpolation test at 2.5, 3.5, 4.0 and 4.5 keV passed: the solver-defined first `ln(P_WDM/P_CDM)=-0.1` crossing increases monotonically with mass at all seven redshifts.

## Gate ledger

| Gate | State | Evidence / interpretation |
|---|---|---|
| B0 Identity & provenance | PASS | Thermal-WDM control and pinned CLASS production scope are explicit in DSIR. |
| B1 DSIR embedding/reference limit | PASS_WITH_SCOPE | WDM is embedded as a separate high-k response block with a CDM/reference limit. |
| B2 Conservation/gauge bookkeeping | PASS_WITH_SCOPE | Uses the frozen DSIR response conventions within the valid solver block. |
| B3 Physical/numerical control | PASS_WITH_SCOPE | High-k time-dependent production and interpolation controls pass in the pinned thermal-WDM scope. |
| B4 Response coverage/masks | PASS | C4 is the canonical block-mask positive control: low-k near-null response is not zero-imputed into a common low-k matrix; high-k is a distinct valid block. |
| B5 Reference identifiability | PASS_WITH_SCOPE | In the frozen theory-response high-k block, the 3 keV deformation is large (`-0.10375` at k=10) while low-k is nearly blind. This is block-level identifiability, not a survey-significance claim. |
| B6 Nearest-comparator discrimination | PARTIAL | The high-k cutoff provides a characteristic separator from LambdaCDM/CDM, but a hard nearest-alternative comparator test against other small-scale suppression mechanisms is not yet frozen in KMDSB. |
| B7 Quotient-surviving novelty | OPEN | A cutoff scale is a model response coordinate, not yet a universal residual law. |
| B8 Prospective withheld prediction | SUPPORTED | Frozen within-family mass interpolation passed prospectively; it does not constitute a withheld-family universal-law test. |
| B9 Synthesis/design prior | PASS | The low-k/high-k blindness contrast gives direct methodology constraints. |

## Overall verdict

`DSIR_DISCRIMINATED`

Scope: WDM is strongly separated from its CDM reference in the valid high-k theory-response block while being nearly invisible in low-k. The verdict must not be read as a unique attribution of small-scale suppression to WDM.

## Wave-1 hypothesis contribution

### W01-H2 — HARD PASS

C4 proves that valid response masks are scientifically operative. Filling the high-k-only information into low-k cells as zeros would falsely imply a globally measured null response.

### W01-H4 — respected

The mass-interpolation holdout is retained as within-family `SUPPORTED`, not universal B8 support.

## Design-prior delta

DP-0401 — **A future model cannot be judged in one k-window.** Its characteristic scale may lie outside the chosen response window.

DP-0402 — **Blind blocks must remain blind.** Near-null/solver-limited/undefined are distinct states.

DP-0403 — **Characteristic-scale motion is a high-value coordinate**, but model attribution requires comparison against alternative suppression mechanisms.

DP-0404 — **Time separability itself is diagnostic.** A nearly static cutoff evolution can help distinguish mechanisms when combined with other families.
