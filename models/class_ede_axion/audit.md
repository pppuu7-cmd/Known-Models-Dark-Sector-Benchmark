# M10 — CLASS_EDE axion-like scalar-field Early Dark Energy

Wave: W03 — Expanded dark-energy mechanisms  
Status: **PREREGISTERED / STAGE A OPEN**  
DSIR overlay: `bc28acc47cc5facba046741fd09f710ae8da9689`  
Solver: `mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97`

## Role
M10 is the supported EDE continuation after M09 demonstrated that the native pinned `class_public` EDE fluid branch is unfinished. M10 is a distinct model/implementation authority, not a patch of M09.

Frozen branch:
- axion-like scalar potential implemented by CLASS_EDE;
- `n_scf=3`;
- `thetai_scf=2.6`;
- `log10z_c=3.5`;
- physical coordinate `f=fEDE>0`;
- first grid `{0.005,0.01,0.03,0.05}`.

Full preregistration: `protocol/W03_M10_CLASS_EDE_PREREGISTRATION_V0_1.md`.

## Stage A gates
| Gate | State | Requirement |
|---|---|---|
| B0 | PASS_WITH_SCOPE | exact external implementation commit/parameter semantics pinned |
| B1 | OPEN | pure Lambda reference in same CLASS_EDE solver |
| B2 | PARTIAL | scalar perturbation implementation exists; promoted gauge audit not yet done |
| B3 | OPEN | shooting accuracy + one-sided response convergence |
| B4 | OPEN | L and broad-k S response |
| B5 | OPEN | no observational operator yet |
| B6 | OPEN | full CPL local span preregistered for Stage B |
| B7 | OPEN | depends on CPL-manifold residual |
| B8 | OPEN | no holdout |
| B9 | PARTIAL | role and construction question frozen |

## Stop conditions
- If reference fails: `BLOCKED_IMPLEMENTATION`.
- If EDE cases fail to shoot reproducibly: `BLOCKED_NUMERICAL_SHOOTING` / `PARTIAL`.
- If L is near-null but S is stable, retain the masked distinction and continue to Stage B on valid blocks.
- No raw S separation is called observational novelty.
