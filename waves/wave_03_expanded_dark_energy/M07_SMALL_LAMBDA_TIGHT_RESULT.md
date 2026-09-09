# M07 small-lambda order audit — tight perturbation result

Date: 2026-09-09  
Status: **INCONCLUSIVE FOR ASYMPTOTIC q-DIRECTION / QUADRATIC ORDER SUPPORTED**  
Run: `34359941026`  
Artifact: `w03-m07-small-lambda-order-tight`  
Artifact ID: `10107423019`  
Artifact digest: `sha256:9386730c7b08f7f72a573c34d86913869abf5911cab7e89a60b80aa29349ff90`.

## Why this run is authoritative for the small-lambda test

The original small-lambda test used default perturbation precision and failed strongly. A separate, independently preregistered q-precision audit (`34359536106`) then demonstrated that tightening only

- `tol_perturbations_integration=1e-8`;
- `perturbations_sampling_stepsize=0.01`

reduces the q-scaled `.025` vs `.075` low-k mismatch from `0.21849` to `5.52e-4` and the angle from `12.51 deg` to `0.0273 deg`.

The present rerun therefore changed only that independently validated numerical tier. All original scientific gates were kept unchanged.

## Frozen grid

`lambda={0.005,0.010,0.020,0.040}`.

All cases ran successfully and the scalar-density target remained controlled.

Lambda-zero low-k reference norm:
`||r_Delta(0)||=4.04705e-9`.

Response norms:
- `.005`: `2.95144e-6`;
- `.010`: `1.17552e-5`;
- `.020`: `4.69771e-5`;
- `.040`: `1.87806e-4`.

All exceed the preregistered `100 x` reference-floor requirement.

## Leading response order

The frozen fit

`ln ||r_Delta|| = a + p ln lambda`

gives

`p = 1.99736912995`.

The preregistered quadratic-order interval was `[1.8,2.2]`, so the **quadratic-order gate passes**.

The q-scaled norms are also highly stable:
- `.005`: `0.11805765`;
- `.010`: `0.11755216`;
- `.020`: `0.11744271`;
- `.040`: `0.11737864`.

This strongly supports a leading response proportional to `q=lambda^2` over the resolved window.

## Why the overall preregistered audit is still INCONCLUSIVE

The original protocol required adjacent q-vector differences to improve monotonically toward smaller lambda.

Measured large->small pairs:

| pair | q angle | relative q difference |
|---|---:|---:|
| `.040 -> .020` | `0.01203 deg` | `5.845e-4` |
| `.020 -> .010` | `0.09653 deg` | `1.924e-3` |
| `.010 -> .005` | `0.25021 deg` | `6.109e-3` |

The mismatch grows as the physical signal shrinks, so the preregistered monotone-convergence gate fails. Under the frozen protocol the overall verdict is therefore `INCONCLUSIVE`, not PASS.

## Reconciliation with the existing q=lambda^2 PASS_WITH_SCOPE

W03 already has a separate resolved-window q-convergence PASS from run `34359536106` at lambda `.025/.075`, where the nonzero response is well resolved and q vectors agree to `5.5e-4` and `0.027 deg`.

The two statements are compatible:

1. **resolved-window local invariant coordinate:** `q=lambda^2` is `PASS_WITH_SCOPE` and is useful for M07 response geometry;
2. **strict asymptotic q-vector convergence as lambda->0:** remains `INCONCLUSIVE` because numerical relative error increases on the smallest tested responses.

Therefore `dr/dq` may be used as the controlled resolved local direction in the stated numerical window, but W03 must not claim that the exact asymptotic tangent has been numerically converged arbitrarily close to q=0.

## No further tuning rule

The precision-conditioned rerun protocol explicitly forbade a third round of precision escalation or threshold relaxation after seeing this result. W03 therefore stops numerical tuning here and carries the asymptotic limitation forward explicitly.

## Methodology consequence

Support for a leading response exponent and hard convergence of the full local direction are different claims. A fitted `p approximately 2` can be robust while the smallest-vector orientation remains solver-floor limited.

Future model construction must report separately:
- leading response order;
- resolved local direction;
- asymptotic tangent convergence.
