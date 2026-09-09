# Wave 03 — Expanded dark-energy mechanisms

Status: **ACTIVE**  
Opened: 2026-09-09  
Protocol: `protocol/WAVE_TESTING_PROTOCOL_v0.1.md`  
Starting DSIR authority: `328f2ca80b724870b851c7fe6366cce1ca5086cd`  
Authority transition: `recovery/AUTHORITY_DELTAS.md` (`AD-001`)

## Scientific purpose

Wave 03 expands beyond phenomenological smooth-w dark energy into explicit microphysical dark-energy dynamics. The first target is a minimally coupled canonical scalar field (quintessence-like `scf`) implemented in the same pinned official CLASS lineage already used by DSIR WDM/DCDM controls.

The wave asks whether background-level similarity survives when the model is forced to expose its perturbation, time-evolution and nearest-comparator response structure.

## First target — M07 canonical scalar-field / quintessence

Pinned upstream solver for the initial implementation probe:

`lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

This is intentionally the same official CLASS commit already used in frozen DSIR high-k WDM/DCDM work.

The CLASS scalar-field sector uses

`V(phi) = ((phi-B)^alpha + A) exp(-lambda phi)`.

For the first controlled branch freeze:

- `alpha = 0`;
- `B = 0`;
- therefore `V(phi) = (1+A) exp(-lambda phi)`;
- `attractor_ic_scf = no` so the initial field state is explicit rather than inherited from a tracking-attractor convention;
- `phi_ini = 0`, `phi_prime_ini = 0` in the initial implementation probe;
- `lambda` is a physical shape/slope parameter and must **not** be used as the shooting nuisance;
- `scf_tuning_index = 2`, so `A` is the normalization adjusted by the CLASS `Omega_scf` shooting machinery.

The canonical background stress is solver-native:

`rho_phi = [phi_prime^2/(2 a^2) + V(phi)]/3`

`p_phi   = [phi_prime^2/(2 a^2) - V(phi)]/3`.

The pinned perturbation implementation exposes scalar-field density/velocity perturbation sources (`delta_scf`, `theta_scf`) as well as the standard metric/matter outputs.

## M07 calibration branch

Before using a dark-energy-dominant scalar branch, W03 first validates a clean intersection with LambdaCDM.

Infrastructure/calibration branch:

- pure LambdaCDM reference: `Omega_scf = 0`;
- split-reference control: positive fixed `Omega_scf` with the remaining closure filled by Lambda;
- `lambda = 0`, `phi_prime_ini = 0` should make the scalar stress constant (`p_phi = -rho_phi`) and therefore reproduce the LambdaCDM total response under matched bookkeeping;
- finite `lambda > 0` samples are descriptive implementation probes only until the reference control and physical-domain behavior are verified.

The initial probe uses a subdominant scalar fraction deliberately. It is **not** yet the final all-dark-energy quintessence benchmark. A dark-energy-dominant production branch is frozen only after solver/reference calibration succeeds.

## Frozen Wave-03 hypotheses

### W03-H1 — background equivalence is not perturbation equivalence

A microphysical scalar model must be compared beyond `H(z)`; a background-level match cannot establish equivalence to smooth-w or LambdaCDM.

### W03-H2 — reference intersection must be solver-clean before local geometry

No quintessence tangent or discriminator is trusted until the `lambda=0` constant-field control reproduces the LambdaCDM reference to a predeclared numerical tolerance in matched outputs.

### W03-H3 — physical shape and shooting nuisance must remain distinct

The slope `lambda` is a theory parameter. It may not be silently redefined by the `Omega_scf` shooting step. A separate potential-normalization parameter is used for closure calibration.

### W03-H4 — microphysical and phenomenological DE remain different benchmark categories

A scalar-field model is not declared equivalent to wCDM/CPL merely because one effective `w(z)` can be fitted to its background. Comparison must occur in common DSIR response coordinates.

### W03-H5 — observational promotion remains separate

Even a hard theory-response separation may remain `NONIDENTIFIABLE` after a realistic observational operator/covariance, as already calibrated by W00.

## Exit criteria

Wave 03 is complete only when:

1. M07 B0-B3 provenance/reference/physical-domain controls are hard-scored;
2. at least one scalar-field production branch is mapped into the standard DSIR response coordinates, or honestly marked `BLOCKED_*`;
3. M07 is attacked against at least M01 smooth-w and one non-DE comparator relevant to its response (e.g. M05 modified gravity) on valid common blocks;
4. any additional DE family added to W03 has pinned implementation/provenance before scoring;
5. theory-space and observation-space claims remain separate;
6. new methodology/design priors and recovery state are synchronized.

## Immediate hard task

**M07 implementation/reference probe, then preregister the production calibration threshold before using finite-lambda outputs for any scientific claim.**
