# M01 — Smooth non-phantom dark energy / wCDM local-family audit

Date: 2026-09-08  
KMDSB protocol: `DSIR_BENCHMARK_PROTOCOL_v0.1`  
DSIR authority snapshot: `pppuu7-cmd/Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`

## Tested scope

This first non-null audit deliberately uses the **already frozen DSIR C1 local ray**, not the entire space of scalar-field dark-energy theories.

Frozen local coordinate:

`epsilon_w = 1 + w -> 0+`

The tested side is non-phantom and one-sided around the LambdaCDM intersection. The smallest frozen step reported by DSIR is `epsilon_w = 1e-4` at p8 precision.

## Why M01 is the first non-null target

It is the cleanest test of the KMDSB distinction between:

- a valid DSIR embedding;
- a numerically controlled nonzero deformation;
- observational identifiability;
- genuine residual novelty.

Those are not the same claim.

## Frozen DSIR evidence used

DSIR G3B reports C1 as comparison-ready in its block-aware v0.1 scope. At the frozen local ray:

- the reference intersection is `w=-1` / `epsilon_w=0`;
- the smallest production step is `epsilon_w=1e-4`;
- finite-difference change at `epsilon_w=1e-3` is about `0.12%` in L2 and `0.014 deg` in direction;
- the cross-solver smooth-w response bridge passes the hard threshold `1e-9`, with matched-p8 calibration mismatch `2.3747404043e-10`.

These establish a controlled local Theory→Response deformation. They do **not** by themselves establish observational detectability or a new law.

## Gate ledger

| Gate | State | Evidence / interpretation |
|---|---|---|
| B0 Identity & provenance | PASS | Tested object is explicitly restricted to the frozen DSIR C1 smooth non-phantom local ray. |
| B1 DSIR embedding/reference limit | PASS_WITH_SCOPE | Exact intersection at `w=-1`; response map is frozen in the C1 block-aware scope. This is not a claim about every quintessence or k-essence realization. |
| B2 Conservation/gauge bookkeeping | PASS_WITH_SCOPE | Uses the frozen DSIR v0.1.1 response bookkeeping and same-solver comoving total-matter response. |
| B3 Physical/numerical control | PASS_WITH_SCOPE | One-sided non-phantom domain and local finite-difference/convergence diagnostics are frozen; cross-solver smooth-w bridge passes. |
| B4 Response coverage/masks | PASS_WITH_SCOPE | Background/AP and frozen low-k structure response are available in the C1 comparison block. Unrepresented channels remain masked. |
| B5 Reference identifiability | PARTIAL | The local response is nonzero away from `w=-1`, but a hard observational identifiability verdict requires survey response kernels/covariance whitening. Raw theory separation is insufficient. |
| B6 Nearest-comparator discrimination | OPEN | No frozen KMDSB nearest-comparator test yet separates this local smooth-w ray from alternative smooth-DE/mimicking responses in observation space. |
| B7 Quotient-surviving novelty | OPEN | A controlled deformation is not automatically a residual law after quotienting. |
| B8 Prospective withheld prediction | OPEN | No KMDSB preregistered withheld test for this M01 claim has yet been executed. |
| B9 Synthesis/design prior | PASS | The audit already yields explicit design constraints even without a novelty claim. |

## Overall verdict

`DSIR_COMPATIBLE`

Meaning: within the frozen C1 local scope, the model family is reproducibly embedded, has a clean LambdaCDM limit, and survives the applicable numerical/bookkeeping controls. **It has not yet earned `DSIR_DISCRIMINATED` or `DSIR_PREDICTIVE_SUPPORT`.**

## First methodological lesson from M01

A known model can pass the DSIR compatibility funnel without passing the observational-discrimination funnel. This separation must remain explicit in every future KMDSB result.

## Design-prior delta

DP-0101 — **Controlled decoupling/intersection:** future models should expose a numerically smooth and physically admissible path to the reference limit.

DP-0102 — **Local geometry matters:** one-sided rays/tangent cones must be respected; a symmetric finite difference is not legitimate when the physical domain is one-sided.

DP-0103 — **Theory-space distance is insufficient:** candidate construction should target response directions that survive survey kernels and covariance whitening, not merely produce a nonzero raw response.

DP-0104 — **Cross-solver calibration:** any future claimed small residual should be larger than and robust to pinned cross-solver calibration mismatch.

## Next hard task for M01

Construct the first KMDSB observation-space B5 test: choose a frozen response block and covariance/operator treatment, then test whether the C1 local ray remains distinguishable from the LambdaCDM origin after whitening. Until that is done, B5 remains PARTIAL.
