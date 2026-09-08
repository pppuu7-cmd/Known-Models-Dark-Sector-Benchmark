# M00 — LambdaCDM calibration audit

Date: 2026-09-08  
KMDSB protocol: `DSIR_BENCHMARK_PROTOCOL_v0.1`  
DSIR authority snapshot: `pppuu7-cmd/Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`

## Role

LambdaCDM is the **null/reference control**, not a novelty candidate. The benchmark passes only if the DSIR bookkeeping reproduces the reference origin without manufacturing residual structure.

## Frozen DSIR evidence used

At the authority snapshot:

- DSIR G0 is `PARTIAL`: multiple solver-specific LambdaCDM/control limits pass, while a broader solver-independent reference suite remains desirable.
- DSIR G1 is PASS for v0.1.1 scope: conservation/Bianchi bookkeeping, comoving total-matter source and hard gauge regression are frozen.
- DSIR G2 is PASS v0.1.1 with response coordinates
  - `r_E(z;z*) = ln[(H/H*)/(H_ref/H_ref*)]`,
  - `r_Delta(k,z) = ln[P_Delta_model^S/P_Delta_ref^S]`.
- DSIR G3B defines C0 LambdaCDM as the reference origin with multiple solver-specific zero limits.

Therefore for model == reference under matched solver lineage and numerical settings:

- `r_E = 0` identically;
- `r_Delta = 0` identically up to numerical tolerance;
- any nonzero residual is a bookkeeping/solver/calibration diagnostic, not dark-sector novelty.

## Gate ledger

| Gate | State | Evidence / interpretation |
|---|---|---|
| B0 Identity & provenance | PASS | Standard C0 reference is explicitly defined in DSIR; authority snapshot pinned above. |
| B1 DSIR embedding/reference limit | PASS_WITH_SCOPE | LambdaCDM is the DSIR reference origin. Exact/zero control limits have passed in multiple solver-specific setups; solver-independent suite is not yet complete. |
| B2 Conservation/gauge bookkeeping | PASS_WITH_SCOPE | Inherited from DSIR G1 PASS v0.1.1 scope, including hard Newtonian/synchronous gauge regression and common total-matter response definition. |
| B3 Physical/numerical control | PASS_WITH_SCOPE | Multiple solver-specific zero limits pass. Scope qualifier retained because global G0 remains PARTIAL. |
| B4 Response coverage/masks | PASS | As a null control, defined common response coordinates are the zero origin; unavailable/non-applicable channels remain masked rather than inferred as zero. |
| B5 Reference identifiability | NOT_APPLICABLE_CONTROL | LambdaCDM defines the reference; self-discrimination is not meaningful. |
| B6 Comparator discrimination | NOT_APPLICABLE_CONTROL | M00 calibrates the null. Alternative models will be tested against M00, not vice versa. |
| B7 Quotient-surviving novelty | NO_NOVELTY_EXPECTED | Correct outcome for a null control. Any claimed residual novelty here would be a benchmark failure. |
| B8 Prospective withheld prediction | NOT_APPLICABLE_CONTROL | No novel law is being promoted from M00. Future independent LambdaCDM solver/data controls may strengthen scope but are not discovery tests. |
| B9 Synthesis/design prior | PASS | Benchmark null must remain exactly recoverable; future model construction must contain a controlled LambdaCDM/reference limit or explicitly justify its absence. |

## Overall verdict

`CONTROL_PASS_WITH_SCOPE`

This is a successful **calibration**, not evidence that LambdaCDM uniquely explains the dark sector. It establishes that KMDSB can represent the DSIR null without confusing “zero residual by construction” with a discovered law.

## Design-prior delta for a future dark-sector model

DP-0001 — **Recoverability:** a future candidate should expose a clean reference/decoupling limit, preferably LambdaCDM or a precisely defined alternative baseline.

DP-0002 — **No fake novelty:** exact reference-limit residuals must vanish under matched solver lineage and covariance-consistent bookkeeping.

DP-0003 — **Mask discipline:** absence of a computed/applicable channel may not be encoded as zero.

DP-0004 — **Scope honesty:** solver-specific control success must not be upgraded to solver-independent universality without an explicit cross-solver suite.

## Next benchmark action

Run M01 smooth non-phantom DE / wCDM as the first non-null local deformation because DSIR already has a frozen C1 one-sided `epsilon_w = 1+w -> 0+` ray and convergence diagnostics. This will be the first test of whether the KMDSB funnel distinguishes “valid embedding” from “observable discrimination”.
