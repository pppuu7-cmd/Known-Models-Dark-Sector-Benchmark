# M10 — CLASS_EDE axion-like scalar-field Early Dark Energy

Wave: W03 — Expanded dark-energy mechanisms  
Status: **STAGE A ACTIVE / IMPLEMENTATION PLUMBING AUDIT**  
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

## Diagnostic execution 1
Actions run `34410251259`, head `b91c3c10cec928f96c349def633f8e21eb194abd`.
Artifact `10126950436`, digest `sha256:8978d6450da1081ed15cc52eb338aa6ef827bdf0c230acc41e0fd55af90de3e4`.

- pinned CLASS_EDE build: PASS;
- pure Lambda reference: exit 0;
- all four EDE configurations: exit 139 / segmentation fault before science output;
- no M10 response was interpreted.

Source audit identified an implementation-plumbing cause: the CLASS_EDE shooting guess path reads entries from `ba.scf_parameters` before replacing the effective `fEDE/log10z_c` targets. The first workflow supplied `n_scf`, `thetai_scf` and `CC_scf` by their named inputs but omitted the six-entry `scf_parameters` seed array used by this older implementation. The official explanatory EDE configuration supplies this array.

This is not a change to the preregistered physical branch. Run 2 adds only the structural seed
`scf_parameters = 3,1,1,1,2.6,0.0` corresponding to `[n, f-placeholder, m-placeholder, CC, theta_i, phi'_i]`; the effective targets still determine `f` and `m` through the native shooting code.

## Stage A gates
| Gate | State | Requirement |
|---|---|---|
| B0 | PASS_WITH_SCOPE | exact external implementation commit/parameter semantics pinned |
| B1 | OPEN | pure Lambda reference passes run 1; EDE reference path still under plumbing audit |
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
- If EDE cases fail to shoot reproducibly after using the implementation's documented seed semantics: `BLOCKED_NUMERICAL_SHOOTING` / implementation-limited.
- If L is near-null but S is stable, retain the masked distinction and continue to Stage B on valid blocks.
- No raw S separation is called observational novelty.
