# M03 — Generalized dark matter (GDM) cs2/cv2 audit

Date: 2026-09-08  
Wave: `wave_01_baseline_atlas`  
DSIR authority: `pppuu7-cmd/Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`

## Tested scope

Frozen DSIR C3 GDM local rays in sound speed `cs2` and viscosity `cv2`, using the pinned GDM_CLASS lineage reported by DSIR.

Key frozen facts:
- zero/reference limit passes;
- low-k matter-power responses are nearly collinear: angle `0.322616 deg`;
- two-axis singular ratio `sigma2/sigma1 = 2.572e-3`;
- later DSIR metric-sector audit finds Weyl-amplitude angle `0.3007 deg` but metric-slip angle `137.9432 deg` and equalized Weyl+slip angle `56.9632 deg`.

Thus M03 is a deliberately strong degeneracy test: a pair that is almost indistinguishable in one response block can separate sharply in another.

## Gate ledger

| Gate | State | Evidence / interpretation |
|---|---|---|
| B0 Identity & provenance | PASS | C3 local cs2/cv2 rays and pinned implementation are frozen in DSIR. |
| B1 DSIR embedding/reference limit | PASS_WITH_SCOPE | Zero/reference limit passes. |
| B2 Conservation/gauge bookkeeping | PASS_WITH_SCOPE | Uses the DSIR total-matter comoving response and pinned source audit. |
| B3 Physical/numerical control | PASS_WITH_SCOPE | Local rays and hard regression are frozen in the stated solver/domain. |
| B4 Response coverage/masks | PASS_WITH_SCOPE | Low-k matter response plus Weyl/slip comparison blocks exist; uncomputed blocks stay masked. |
| B5 Reference identifiability | PARTIAL | Nonzero local rays exist, but survey-level whitening remains required. |
| B6 Nearest-comparator discrimination | PASS_WITH_SCOPE | Within the frozen theory setup, cs2/cv2 matter/Weyl near-degeneracy is broken by metric slip; equalized Weyl+slip angle is `56.9632 deg`. This is a hard theory-response discriminator, not yet a survey detectability claim. |
| B7 Quotient-surviving novelty | OPEN | The separator is a discriminator, not yet a model-independent residual law. |
| B8 Prospective withheld prediction | SUPPORTED | DSIR later froze and passed within-family withheld interpolation for the C3 characteristic-scale direction, but this is below a true withheld-family universal-law test. |
| B9 Synthesis/design prior | PASS | Multi-channel discrimination yields direct model-design requirements. |

## Overall verdict

`DSIR_DISCRIMINATED`

Scope: the cs2/cv2 local GDM directions are demonstrably separable in the frozen multi-response theory space despite near-degeneracy in low-k matter power. This does **not** yet mean a survey can measure that separator at useful significance.

## Wave-1 hypothesis contribution

### W01-H3 — HARD PASS in theory-response space

The GDM pair provides the cleanest current example that one observable block is insufficient: matter-power/Weyl amplitude is almost degenerate while slip sharply separates the directions.

### W01-H4 — respected

The later within-family withheld interpolation support is retained as `SUPPORTED`, not promoted to universal B8 predictive support.

## Design-prior delta

DP-0301 — **Multi-channel necessity:** a future model should make predictions in at least one response channel orthogonal to common growth/amplitude degeneracies.

DP-0302 — **Metric slip is high-value:** slip-like observables can carry information hidden in matter-power amplitude/shape.

DP-0303 — **Near-collinearity must be quantified:** parameter count is not identifiable rank.

DP-0304 — **Within-family withheld support is useful but limited:** it calibrates mechanism stability without establishing universality.
