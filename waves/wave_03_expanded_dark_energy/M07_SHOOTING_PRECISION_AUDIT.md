# M07 shooting-precision audit

Frozen: 2026-09-09
Status: **PREREGISTERED NUMERICAL AUDIT**
Scientific branch: unchanged M07 production branch

## Trigger

The preregistered dark-energy-dominant production run `34337676199` passed its lambda-zero reference gate and executed all production points, but the achieved present scalar fraction drifted from the fixed target as lambda increased.

Target:

`Omega_scf_target = 0.682686955086854`.

Default-shooting achieved errors:

| lambda | Omega_scf(today)-target | fractional error |
|---:|---:|---:|
| 0.025 | `+2.5731859532e-08` | `3.77e-08` |
| 0.075 | `+3.1147812486e-06` | `4.56e-06` |
| 0.15 | `+6.1031979429e-05` | `8.94e-05` |
| 0.30 | `+1.2379784585e-03` | `1.81e-03` |

This drift is treated as a B3 numerical-control question, not as physical scalar-field response.

## Source-level conditioning diagnosis

Pinned CLASS uses one-dimensional Ridders shooting with absolute root tolerance

`xtol = tol_shooting_deltax_rel * max(|x1|,|x2|)`.

The pinned default is

`tol_shooting_deltax_rel = 1e-5`.

For M07 the nuisance variable is `A ~ -1`, whereas the physical potential normalization is

`N = 1 + A ~ O(1e-7)`.

Therefore a tolerance scaled to `|A|~1` is poorly conditioned for the physically relevant normalization `1+A`: the default root-coordinate tolerance can be much larger than the normalization being resolved.

This is a numerical parametrization/conditioning issue. It does not permit changing physical `lambda`, the potential family, or the initial-condition branch.

## Frozen audit intervention

Rerun the exact same production branch and exact same lambda grid with only

`tol_shooting_deltax_rel = 1e-13`.

No physical or cosmological parameter changes are allowed.

The natural-scale `A_seed(lambda)` remains unchanged.

## Audit acceptance

The strict-shooting realization is accepted for subsequent B3/B4/B6 response work only if:

1. pure LambdaCDM and lambda-zero scalar reference execute successfully;
2. the existing frozen lambda-zero production thresholds remain satisfied;
3. for **every** finite production lambda, `abs(Omega_scf(today)-Omega_scf_target) <= 1e-6`;
4. all scalar backgrounds remain finite and the achieved `Omega_scf` is positive;
5. exact configs, exit codes, solver SHA and outputs are preserved.

If the target error does not fall below `1e-6`, M07 remains `PARTIAL` at B3 and the next step is an explicitly versioned numerical reparametrization or solver-level shooting audit—not relaxation of the target after inspecting the response.

## Authority rule for response vectors

The default-tolerance production vectors from run `34337676199` remain immutable evidence of the numerical-conditioning problem.

If this strict audit passes, strict-tolerance vectors become the authoritative M07 production response for B3/B4/B6. The default vectors are not deleted or silently overwritten.

Neither realization is B8 prospective evidence.
