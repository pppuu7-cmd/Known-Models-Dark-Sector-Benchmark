# M05 — Designer f(R) modified-gravity comparator audit

Date: 2026-09-08  
Wave: `wave_01_baseline_atlas`  
DSIR authority: `pppuu7-cmd/Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`

## Tested scope

Frozen DSIR C5 designer-f(R) production manifold using the official H-EFTCAMB lineage reported by DSIR (`EFTCAMB/EFTCAMB@16d9c4e9...`).

Frozen controls:
- MG-S0 exact-GR hard gate PASS;
- MG-S1 common-baseline multi-z hard gate PASS;
- production points `B0={1e-6,1e-5,1e-4,1e-3}`;
- `1e-7` retained as transition control near the solver GR threshold.

Key comparator evidence from DSIR:
- GDM cs2 vs f(R) leading scale-mode angle: `0.07813 deg`;
- time-mode unoriented angle: `25.18 deg`;
- full oriented ray angle: `154.82 deg`;
- GDM cv2 vs f(R): scale-mode `0.10169 deg`, time-mode `25.49 deg`, full oriented ray `154.51 deg`.

Therefore a scale-only view can make GDM and f(R) look nearly identical while time evolution and physical response orientation break the degeneracy. Separate slip information further strengthens multi-channel separation in the frozen theory setup.

Later DSIR work also reports a preregistered within-family designer-f(R) interpolation test in which the relevant transition scale moves toward smaller k with increasing microscopic parameter and `k_I^geo` changes in the preregistered non-increasing direction.

## Gate ledger

| Gate | State | Evidence / interpretation |
|---|---|---|
| B0 Identity & provenance | PASS | C5 implementation lineage and production manifold are pinned in DSIR. |
| B1 DSIR embedding/reference limit | PASS_WITH_SCOPE | Exact-GR/near-GR controls are explicitly tested in the frozen H-EFTCAMB scope. |
| B2 Conservation/gauge bookkeeping | PASS_WITH_SCOPE | Uses frozen DSIR response conventions and same-baseline comparison rules. |
| B3 Physical/numerical control | PASS_WITH_SCOPE | MG-S0 and MG-S1 hard gates pass; transition control is separated from production points rather than treated as a generic reliable ray point. |
| B4 Response coverage/masks | PASS_WITH_SCOPE | Multi-z low-k structure plus metric-response comparison is available in the frozen C5 block; unavailable blocks remain masked. |
| B5 Reference identifiability | PARTIAL | Non-GR response is hard in theory space, but observational covariance/operator projection is still required for survey-level identifiability. |
| B6 Nearest-comparator discrimination | PASS_WITH_SCOPE | Scale-only GDM/f(R) near-degeneracy is broken by time evolution/orientation (and metric channels) in the frozen theory-response setup. |
| B7 Quotient-surviving novelty | OPEN | A cross-family separator is not yet a model-independent residual law. |
| B8 Prospective withheld prediction | SUPPORTED | Preregistered within-family interpolation support exists, but it is not a true withheld-family universal-law test. |
| B9 Synthesis/design prior | PASS | Attribution degeneracy between dark-sector microphysics and modified gravity yields direct requirements for future model tests. |

## Overall verdict

`DSIR_DISCRIMINATED`

Scope: designer f(R) is reproducibly separated from important dark-sector comparators in the frozen multi-response theory space. This is not yet observational proof of modified gravity and not evidence that GDM is physically false.

## Wave-1 hypothesis contribution

### W01-H3 — HARD PASS in theory-response space

M05 supplies a cross-family version of the same lesson as M03: one scale-profile snapshot is insufficient. Time evolution and response orientation can turn an almost zero scale-mode angle into a large full-ray separation.

### W01-H4 — respected

The designer-f(R) interpolation test is retained as within-family prospective support only.

## Design-prior delta

DP-0501 — **Attribution must be cross-sector.** A future dark-sector model must be compared against modified-gravity explanations, not only against other matter/energy models.

DP-0502 — **Time and sign/orientation are first-class observables.** Similar scale shapes do not imply equivalent dynamics.

DP-0503 — **Near-reference solver thresholds must be explicit.** Transition-control points cannot silently define the production tangent.

DP-0504 — **A distinctive mechanism needs a distinctive observable direction**, not merely a different microscopic interpretation of the same response.
