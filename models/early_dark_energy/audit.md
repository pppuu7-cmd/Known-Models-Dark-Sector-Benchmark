# M09 — solver-native Early Dark Energy audit

Wave: W03 — Expanded dark-energy mechanisms  
Status: **PREREGISTERED / LOCAL CONTROL OPEN**  
DSIR methodology overlay: `bc28acc47cc5facba046741fd09f710ae8da9689`  
Pinned solver: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

## Branch
`fluid_equation_of_state=EDE`, `w0_fld=-1`, `cs2_fld=1`, `use_ppf=yes`, local physical coordinate `e=Omega_EDE>=0`.

The exact preregistration and frozen response blocks are in `protocol/W03_M09_EDE_PREREGISTRATION_V0_1.md`.

## Scientific purpose
M07 canonical quintessence became nearly indistinguishable from the local M08 CPL manifold after a common ShapeFit observation mapping. M09 therefore attacks a different axis: early-time, scale-dependent transfer/shape response.

The first calculation is intentionally prior to any claim of observational discrimination. It must establish:
1. whether the EDE-zero branch numerically intersects pure LambdaCDM in the frozen response scope;
2. whether a stable one-sided local `Omega_EDE` tangent exists;
3. whether the broad-k amplitude-quotiented shape response is non-negligible and converged.

## Frozen initial gate ledger
| Gate | State | Note |
|---|---|---|
| B0 | PASS_WITH_SCOPE | exact solver branch pinned |
| B1 | PARTIAL | EDE-zero/Lambda regression pending |
| B2 | PARTIAL | PPF branch pinned; no promoted residual gauge audit yet |
| B3 | OPEN | one-sided tangent convergence pending |
| B4 | OPEN | L and S blocks pending |
| B5 | OPEN | no observational operator for S yet |
| B6 | OPEN | primary next comparator is M08 CPL |
| B7 | OPEN | depends on CPL-manifold residual |
| B8 | OPEN | no prospective holdout yet |
| B9 | PARTIAL | role/design question preregistered |

## Non-negotiable interpretation
Negative `Omega_EDE` is not introduced merely to obtain a central derivative. A near-null shape result is kept distinct from missing or solver-limited shape. A nonzero raw S response is not an observational claim.
