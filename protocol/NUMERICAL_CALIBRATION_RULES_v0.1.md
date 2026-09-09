# KMDSB Numerical Calibration Rules v0.1

Updated: 2026-09-09
Status: LIVING methodology supplement

## Purpose

Prevent numerical implementation failures from being confused with physical-model failures when KMDSB benchmarks known models or later constructs an original dark-sector candidate.

This supplement is evidence-fed by W03/M07 and is subordinate to the frozen B0-B9 semantics.

## N1 — natural-scale initialization before shooting

If a solver tunes a nuisance/closure parameter to reproduce a physical target, initialize that nuisance at the natural scale implied by the target equations whenever such a scale can be derived.

Do not start a root finder many orders of magnitude away merely because a dimensionless-looking default such as zero is convenient.

For M07 canonical scalar field,

`rho_phi = [phi_prime^2/(2a^2)+V]/3`.

At the lambda-zero constant-field reference, `phi_prime=0`, hence for a target scalar fraction

`V_target = 3 Omega_scf H0^2`.

For `V=(1+A) exp(-lambda phi)` this yields the scale-aware seed

`A_seed(lambda) = 3 Omega_scf H0^2 exp(lambda phi_ini) - 1`.

This formula initializes only the numerical nuisance `A`; it does not fit or alter physical `lambda`.

## N2 — physical parameters must never be repaired by shooting

A failed closure solve may justify changing:
- nuisance initial guess;
- bracketing/root-finder strategy;
- integration precision;
- equivalent numerical parametrization.

It does not justify silently changing:
- physical coupling/slope/mass;
- kinetic sign;
- potential family;
- physical initial-condition branch;
- comparison target.

Any such change creates a new scientific branch and must receive new provenance.

## N3 — mandatory reference control before finite-deformation science

A finite-deformation grid is scientifically inert until the exact/controlled reference case succeeds.

For M07:
1. pure LambdaCDM must run;
2. lambda-zero constant-field split reference must run;
3. its matched response residual defines the numerical reference floor;
4. a hard production tolerance is preregistered before interpreting finite lambda.

Finite-lambda values generated during infrastructure debugging can never be retroactively promoted to B8 prospective evidence.

## N4 — failure taxonomy for numerical probes

Classify failures in this order:

1. workflow/parser failure;
2. build/dependency failure;
3. input/configuration failure;
4. shooting/root-finder failure;
5. integrator/precision failure;
6. physical-domain violation with a successfully evaluated model;
7. frozen-prediction failure against data.

Only levels 6-7 may directly support a physical-model failure label, and only within their frozen scope.

## N5 — preserve failed-run artifacts

A diagnostic workflow must preserve:
- exact input configuration;
- solver and repository SHAs;
- exit codes by case;
- stdout/stderr logs;
- available outputs;
- analysis products when possible.

The final mandatory gate should execute after diagnostic upload, so a failed control remains auditable.

## N6 — future-model construction implication

When the future original dark-sector model is constructed, every dimensionful or exponentially sensitive parameterization must carry an explicit natural-scale estimate before automated fitting/shooting. This is a numerical design requirement, not a physical axiom.

Evidence source: `recovery/M07_SHOOTING_DIAGNOSIS_2026-09-09.md`.
