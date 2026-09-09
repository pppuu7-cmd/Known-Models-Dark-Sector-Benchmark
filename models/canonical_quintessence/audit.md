# M07 — canonical scalar-field / quintessence audit

Wave: W03 — Expanded dark-energy mechanisms  
Status: **ACTIVE / REFERENCE CALIBRATED / PRODUCTION RUNNING**  
W03 DSIR authority: `328f2ca80b724870b851c7fe6366cce1ca5086cd`  
Pinned scalar solver: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

## Model identity

M07 is a minimally coupled canonical scalar field with standard kinetic term and a controlled pure-exponential potential branch of the pinned CLASS `scf` implementation.

CLASS potential family:

`V(phi) = ((phi-B)^alpha + A) exp(-lambda phi)`.

Frozen M07 subset:

`alpha = 0`, `B = 0`, hence

`V(phi) = (1+A) exp(-lambda phi)`.

Canonical solver stress:

`rho_phi = [phi_prime^2/(2a^2) + V]/3`

`p_phi = [phi_prime^2/(2a^2) - V]/3`.

The perturbation solver exposes scalar-field density and velocity response sources (`delta_scf`, `theta_scf`) in addition to the standard matter and metric outputs.

## Parameter/provenance decision

The default CLASS scalar-field shooting convention can tune parameter index 0 (`lambda`) when `Omega_scf` is targeted. That convention is unsuitable for a benchmark in which `lambda` is itself the physical slope parameter.

M07 therefore freezes:

- `attractor_ic_scf = no`;
- `phi_ini = 1`;
- `phi_prime_ini = 0`;
- `scf_tuning_index = 2`;
- potential normalization `A` is the shooting nuisance used to hit the requested `Omega_scf`;
- `lambda` remains fixed by the benchmark point.

`phi_ini=1` replaces the initial implementation idea `phi_ini=0` because pinned CLASS evaluates the alpha-zero polynomial derivative literally as `alpha*(phi-B)^(alpha-1)`; choosing `phi=B=0` creates the numerical coordinate singularity `0*0^-1`. For `alpha=0`, a constant field-coordinate shift is absorbed into the normalization nuisance and does not alter the pure-exponential branch being benchmarked.

This physical-parameter / solver-nuisance separation is required before any local derivative or comparator geometry is defined.

## Reference-intersection logic

At `lambda = 0` and `phi_prime = 0`, the pure-exponential branch becomes a constant potential. Then

`p_phi = -rho_phi`.

A matched split-reference control can therefore replace a fixed fraction of Lambda by the constant scalar while leaving the total dark-energy response at the LambdaCDM origin, if solver and bookkeeping are clean.

This statement has now been tested numerically in the calibration scope.

## Successful calibration — Actions run 34325977559

Pinned KMDSB head:
`e74f798a685f8b92f75ef3afe0b4be03eb51a576`.

Pinned CLASS head:
`e85808324f51fc694d12e3ed7439552a3c3f9540`.

Mandatory cases and all diagnostic finite-lambda cases exited with code 0.

For the `Omega_scf=0.10`, `lambda=0` split reference:

- achieved `Omega_scf(today)=0.10000000013560413`;
- `w_scf(z)=-1` at all seven frozen redshift nodes;
- `phi(z)=1` at all seven nodes;
- `phi_prime(z)=0` at all seven nodes;
- `max_abs_lnH = 5.462919005900343e-11` against pure LambdaCDM;
- `max_abs_lnP = 4.111520165089289e-7` on the frozen 7x5 low-k grid.

Thus the analytic constant-field reference intersection is solver-clean in the calibrated subdominant split scope.

The calibration finite-lambda points `{0.05,0.10,0.20}` remain implementation diagnostics only and can never be relabeled as B8 prospective evidence.

## Numerical shooting diagnosis

The earlier failed SCF runs were traced to an inappropriate nuisance initial scale, not a physical-domain failure.

At lambda zero,

`V_target = 3 Omega_scf H0^2`.

For `V=(1+A)exp(-lambda phi)`, the scale-aware shooting seed is

`A_seed(lambda)=3 Omega_scf H0^2 exp(lambda phi_ini)-1`.

The successful run used this natural-scale initialization. The methodology is recorded in:

- `recovery/M07_SHOOTING_DIAGNOSIS_2026-09-09.md`;
- `protocol/NUMERICAL_CALIBRATION_RULES_v0.1.md`.

## Production preregistration

Frozen before inspecting any dark-energy-dominant finite-lambda production output:

`waves/wave_03_expanded_dark_energy/M07_PRODUCTION_PREREGISTRATION.md`.

Dark-energy-dominant target:

`Omega_scf_target = 0.682686955086854`,

the measured present Lambda fraction of the matched pure-LambdaCDM reference.

Hard lambda-zero production thresholds:

- `max_abs_lnH <= 1e-8`;
- `max_abs_lnP <= 1e-5`;
- `abs(Omega_scf(today)-Omega_scf_target) <= 1e-6`;
- `max_z abs(w_scf+1) <= 1e-10`;
- `max_z abs(phi_prime) <= 1e-12`.

Frozen production response grid:

`lambda={0.025,0.075,0.15,0.30}`.

These are B3-B6 production points, not B8 holdouts.

Active production workflow:
`.github/workflows/w03-m07-quintessence-production.yml`.

## B0-B9 gate ledger

| Gate | State | Evidence / requirement |
|---|---|---|
| B0 identity/provenance | `PASS_WITH_SCOPE` | canonical CLASS `scf` branch, exact upstream commit, potential subset, explicit IC and shooting semantics pinned |
| B1 DSIR embedding/reference limit | `PASS_WITH_SCOPE` | analytic constant-field intersection numerically reproduced in calibrated `Omega_scf=0.10` split; full-DE production lambda-zero gate preregistered and running |
| B2 conservation/gauge/frame bookkeeping | `PARTIAL` | minimally coupled canonical solver implementation and matched total response are clean; explicit cross-gauge / additional response bookkeeping audit still pending |
| B3 physical-domain/numerical control | `PARTIAL` | natural-scale shooting converges for lambda `{0,0.05,0.10,0.20}` in calibration; positive finite scalar background obtained; dark-energy-dominant production and precision robustness pending |
| B4 response coverage/masks | `PARTIAL` | frozen 7x5 low-k matter response is executable; production response and scalar/metric/slip coverage still pending |
| B5 reference identifiability | `OPEN` | no observational promotion without a pinned operator/covariance |
| B6 nearest comparator | `OPEN` | attack M01 smooth-w and M05 designer f(R) after production response passes its frozen reference gate |
| B7 quotient-surviving novelty | `OPEN` | premature |
| B8 prospective withheld prediction | `OPEN` | no relation/holdout frozen yet; calibration and production response points are not holdouts |
| B9 synthesis/design priors | `PARTIAL` | parameter/nuisance separation, natural-scale initialization and reference-first calibration feed methodology; final model verdict pending |

## Current overall verdict

`INCONCLUSIVE` while the preregistered dark-energy-dominant production gate and comparator attacks remain open.

This is no longer an implementation-blocked model: the calibrated reference branch is reproducibly executable.

## Design-prior pressure from M07

- physical theory parameters and solver shooting/nuisance parameters must be explicitly separated;
- exponentially or dimensionfully sensitive nuisance parameters require natural-scale initialization before automated fitting/shooting;
- exact analytic reference intersections require numerical regression and a frozen production tolerance before finite-deformation science;
- microphysical dark energy must expose perturbation/time response rather than being reduced to a fitted background `w(z)`.
