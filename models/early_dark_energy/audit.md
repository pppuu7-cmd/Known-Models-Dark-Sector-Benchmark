# M09 — solver-native Early Dark Energy audit

Wave: W03 — Expanded dark-energy mechanisms  
Status: **BLOCKED_IMPLEMENTATION**  
DSIR methodology overlay: `bc28acc47cc5facba046741fd09f710ae8da9689`  
Pinned solver: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

## Branch
`fluid_equation_of_state=EDE`, `w0_fld=-1`, `cs2_fld=1`, `use_ppf=yes`, physical local coordinate `e=Omega_EDE>=0`.

The exact preregistration was frozen before execution in `protocol/W03_M09_EDE_PREREGISTRATION_V0_1.md`.

## Execution
Actions run: `34409305291`  
Head: `4c94cf0da8d793cf04532d68b4a8e015dab17af8`  
Artifact: `10126634345`  
Digest: `sha256:be6b8e1685c9eca114bc7cda42031f1fd2ea3da8df1c17ed8115461c7d68b3a2`

Pure LambdaCDM completed with exit 0.

Every EDE case exited 1 before background evolution, including the nominal branch zero point `Omega_EDE=0` and all preregistered positive probes.

Frozen EDE cases:
- `0` -> exit 1
- `1e-4` -> exit 1
- `3e-4` -> exit 1
- `1e-3` -> exit 1
- `3e-3` -> exit 1

The upstream error is:

`EDE implementation not finished: to finish it, read the comments in background.c just before this line`

This is an implementation block, not a failed physical prediction.

## Upstream code audit
The pinned CLASS source contains substantial but incomplete EDE machinery:

1. `Omega_ede(a)` is coded from the referenced EDE parameterization.
2. `d Omega_ede / da` is coded analytically.
3. `w_ede(a)` is coded and includes the radiation-to-matter tracking term through `a_eq`.
4. In the EDE `dw/da` branch, `d2Omega_ede_over_da2` is explicitly set to `0.` before forming the derivative. This is an implementation placeholder/limitation for the perturbation derivative and is not treated as a validated analytic second derivative.
5. Most decisively, the EDE branch has no implemented solution for the continuity integral
   `int_a^1 da 3(1+w_fld)/a`.
   The source comments say this integral is required for the initial fluid density and suggest numerical integration if no simple analytic expression is supplied. The EDE case then calls `class_stop` unconditionally.
6. `background_checks()` calls `background_w_fld()` already at `a=0`, so the stop occurs before normal background initialization; it is not a late P(k) or perturbation failure.

Therefore no EDE response vector can be produced by this pinned upstream branch without modifying the third-party solver.

## Gate ledger after execution
| Gate | State | Note |
|---|---|---|
| B0 | `PASS_WITH_SCOPE` | exact unfinished upstream branch identified and pinned |
| B1 | `BLOCKED_IMPLEMENTATION` | EDE-zero reference cannot execute |
| B2 | `BLOCKED_IMPLEMENTATION` | perturbation derivative implementation is incomplete and branch never initializes |
| B3 | `BLOCKED_IMPLEMENTATION` | physical one-sided ray cannot be numerically evaluated upstream |
| B4 | `BLOCKED_IMPLEMENTATION` | L/S response blocks do not exist |
| B5 | `OPEN` | not reached |
| B6 | `OPEN` | not reached |
| B7 | `OPEN` | not reached |
| B8 | `OPEN` | no holdout |
| B9 | `PASS` | implementation-coverage lesson is definite |

Overall: `BLOCKED` / `BLOCKED_IMPLEMENTATION_UPSTREAM_SOLVER_BRANCH`.

## Scientific lesson
An advertised parameter/parser branch is not sufficient evidence that a model is executable. Solver capability itself must be part of benchmark coverage.

KMDSB will **not** silently remove the `class_stop`, insert a guessed integral, or treat the placeholder second derivative as validated physics. Any local completion patch would be a new implementation branch with separate equations, validation and provenance.

The next EDE benchmark should therefore use a published implementation whose background and perturbation dynamics are explicitly completed, while preserving M09 as the negative implementation-control result.

## Anti-overclaim
- M09 does **not** show that Early Dark Energy is false.
- It shows only that this pinned native `class_public` EDE fluid branch is unfinished and unusable for the preregistered response test.
- No null response, no observational non-identifiability and no comparator equivalence may be inferred from the failed execution.
