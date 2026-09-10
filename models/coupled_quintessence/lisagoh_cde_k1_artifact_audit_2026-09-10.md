# M14 LisaGoh/CDE K1 exact-reference artifact audit

Updated: 2026-09-10
Provider: `LisaGoh/CDE@b85a675af7544a5183e402964550811aa805b698`
Parent K1 run: `34488423569`
Background recovery run: `34488921064`
Recovery artifact: `10156865237`
Artifact digest: `sha256:92cf82d36c18d413e376f5330eb2a48c5785371f5a678abb590ab45f813874d8`

## Immutable parent outcomes

The prospectively frozen three-arm K1 test established:

- exact-zero full perturbation arm: exit 1 in perturbation integration with `Failure in sp_ludcmp. Possibly singular matrix!`;
- beta=0 committed-tiny-seed full arm: exit 0 with fresh background, perturbation, linear P(k), CMB Cl and transfer products;
- the first exact-zero background-only arm was blocked by output-request plumbing and was recovered separately without changing physics or thresholds.

## Recovered exact-zero background artifact

The final background-only recovery used

- `beta_1=beta_2=beta_3=0`;
- `phi_ini_scf=0`;
- `phi_prime_ini_scf=0`;
- `output=`;
- `lensing=no`;
- `non linear=`;
- `write background=yes`.

The process eventually exited 139, but before that it wrote a complete nonempty background table `k1_exact_bg_recovery_background.dat` covering 5281 rows from `z=1e16` through the final `z=0` row.

The immutable output was consumed after the run using exactly the prospectively frozen K1 functionals and thresholds. Results:

- all inspected values finite: **YES**;
- `max |beta| = 0`;
- `max |dbeta/dz| = 0`;
- `max |phi_prime_scf| = 0`;
- `max |w_scf+1| = 0`;
- `Rspan(rho_scf) = 0`;
- `Rspan(rho_cdm*a^3) = 2.946835858494685e-9`, below the frozen `1e-8` threshold.

Thus the **physical/background reference solution itself satisfies every preregistered invariant** and reaches the present epoch. The nonzero process exit must not be misreported as a failure of the background decoupling equations.

## Relation to the tiny-seed beta=0 diagnostic

The exact-zero and tiny-seed beta=0 background tables have the same redshift grid. Their H and CDM-density columns agree at the serialized precision across that grid, while the tiny seed carries an early-time scalar kinetic transient (`w_scf -> +1` at the earliest row) that becomes dynamically negligible. This explains why the tiny-seed route can regularize denominators without being literally the same scalar state as the exact rigid-vacuum reference.

The tiny seed therefore remains a numerical diagnostic only; it does not replace the exact reference demanded by K1.

## Scientific interpretation

The combined evidence is now:

1. exact beta=0 background equations have the correct rigid-vacuum/CDM reference and satisfy all frozen invariants;
2. exact beta=0 full perturbation execution fails in the untouched provider near the exact-zero scalar state;
3. beta=0 with the committed tiny scalar seed executes the full forward model;
4. source audit identifies removable/degenerate zero-state numerical structures such as a `beta_z/phi'` expression in the scalar perturbation equation and a scalar velocity definition involving `rho_phi+p_phi`, while the published nonsingular equations themselves are well defined in the uncoupled limit.

Therefore the scientifically appropriate provider classification is

`M14_LISAGOH_CDE_EXACT_BACKGROUND_REFERENCE_VALID_FULL_REFERENCE_IMPLEMENTATION_BLOCKED`.

Strict K1 remains **not passed**, because the exact full forward-model reference does not execute. This is a provider/reference-implementation blocker, not a physical falsification of M14 and not a failure of the exact background limit.

The machine JSON from the recovery retains its process-level `BLOCKED_INFRASTRUCTURE` classification because its preregistered evaluator required exit code zero before parsing the background table. This audit does not rewrite that historical machine result; it consumes the immutable artifact and refines the scientific interpretation while preserving the raw outcome.

## Next allowed route

Do not tune the author seed or denominator after the fact and call the original provider K1-passing. The clean route is a separately preregistered **independent reference-regularization verification** that changes only algebraically removable beta=0 singular handling, demonstrates zero effect away from the singular null, and is labelled as an independent KMDSB verification layer rather than the untouched author provider.