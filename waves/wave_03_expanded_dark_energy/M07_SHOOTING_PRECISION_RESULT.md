# M07 shooting-precision audit — result

Date: 2026-09-09  
Status: **PASS_WITH_SCOPE**  
Strict run: `34338140447`  
Strict artifact: `w03-m07-shooting-precision-audit`  
Artifact digest: `sha256:958708322566a2d36ce7522a3f705b543e0158c554a8de8e18e803c82a5c9cb8`  
Scientific branch: unchanged M07 production branch  
Only numerical intervention: `tol_shooting_deltax_rel: 1e-5 -> 1e-13`.

## Frozen target and acceptance

`Omega_scf_target = 0.682686955086854`.

Preregistered acceptance required, for every finite production lambda,

`abs(Omega_scf(today)-Omega_scf_target) <= 1e-6`.

All mandatory reference and finite-lambda cases executed successfully and the lambda-zero production reference thresholds remained satisfied.

## Achieved target control

| lambda | default-shooting error | strict-shooting error | strict status |
|---:|---:|---:|---|
| 0.025 | `+2.57319e-08` | `+2.57319e-08` | PASS |
| 0.075 | `+3.11478e-06` | `-3.43697e-11` | PASS |
| 0.15 | `+6.10320e-05` | `-1.58952e-10` | PASS |
| 0.30 | `+1.23798e-03` | `-3.01260e-10` | PASS |

The strict realization therefore passes the frozen `1e-6` target-error gate for every finite lambda.

## Lambda-zero reference control

Strict dark-energy-dominant scalar replacement at `lambda=0` gives

- `Omega_scf(today) = 0.682686955181768`;
- `w_scf(z) = -1` on all seven frozen redshift nodes;
- `phi(z) = 1`;
- `phi_prime(z) = 0`;
- `max_abs_lnP = 2.16648e-10`;
- `max_abs_lnH = 1.08876e-10`.

This remains far below the preregistered production tolerances (`1e-6` in lnP, `1e-8` in lnH).

## Why this audit matters scientifically

The default-tolerance run was not merely imprecise in a nuisance metadata field. Its response vector itself moved as target drift increased.

Comparing default and strict `r_Delta(k,z)` vectors on the frozen 35-node block:

| lambda | relative vector difference `||r_strict-r_default||/||r_strict||` | direction angle |
|---:|---:|---:|
| 0.025 | `~2.8e-12` | `~0 deg` |
| 0.075 | `0.01469` | `0.1354 deg` |
| 0.15 | `0.07496` | `0.3258 deg` |
| 0.30 | `0.38134` | `1.3276 deg` |

At `lambda=0.30`, default shooting also changes the H-response norm by about 49.6% relative to the strict result.

Therefore default-tolerance finite-lambda vectors are retained only as evidence of numerical conditioning failure. They are not the response authority for B4/B6.

## Gate consequence

- M07 B3 numerical/physical-domain control: `PASS_WITH_SCOPE` for the frozen branch and strict shooting realization.
- Strict run `34338140447` is the authoritative M07 production response source for subsequent B4/B6 work.
- B3 scope does not imply observational identifiability or predictive support.
- Finite-lambda points remain non-B8 production characterization; none are retroactively converted into prospective holdout evidence.

## Methodology consequence

When a physical normalization is represented by a cancellation such as `N=1+A` with `A~O(1)` but `N<<1`, root tolerance in the raw coordinate can be catastrophically ill-conditioned even when the run terminates successfully.

Future-model numerical audits must compare solver tolerances against the physically resolved combination, not merely against the magnitude of the raw nuisance coordinate.
