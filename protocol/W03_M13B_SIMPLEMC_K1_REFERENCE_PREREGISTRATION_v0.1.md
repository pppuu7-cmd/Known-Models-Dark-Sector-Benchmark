# W03 M13b SimpleMC K1 reference-limit preregistration v0.1

Date: 2026-09-10
Target: M13b covariant multi-DOF quintom, background provider scope
Provider: `ja-vazquez/SimpleMC@a268fe5e2545428ddcf76b37b166a55dbf692fb0`

## Purpose

Test the internal reference limit of the pinned two-field SimpleMC quintom implementation without claiming perturbation-level validation.

The source model has a canonical field `phi`, a phantom field `psi`, and

`V = 0.5 (mquin phi)^2 + 0.5 (mphan psi)^2 + beta (phi psi)^2`.

At `beta=0` and `mphan=0`, the phantom field starts with zero velocity and has zero potential derivative. Its kinetic contribution therefore remains zero and the two-field equations should reduce to the provider's canonical one-field quintessence branch at the same `mquin`.

## Frozen anchor

- `mquin = 1.7` (provider default)
- `beta = 0`
- flat/default inherited LCDM parameters
- provider's own initial-condition search unchanged
- historical compatible runtime already validated in the M13b provider control

Reference object:

`QuintomCosmology(vary_mquin=True, vary_mphan=False)` with provider `mphan=0`.

Two-field test object:

`QuintomCosmology(vary_mquin=True, vary_mphan=True)` with explicit `mphan` values.

## Frozen phantom-mass ladder

`mphan = {0, 1e-3, 5e-4, 2.5e-4}`.

The exact zero case is the K1 identity control. The positive ladder is a continuity diagnostic only; no post-hoc mass values may be inserted.

## Frozen outputs

On the provider-native `lna in [-10,0]` grid record:

- `H(a)`;
- `w_de(a)`;
- scalar-field density `sf_rho`;
- provider initial-condition status `phi_ini`;
- solution finiteness.

Relative H and rho differences use a denominator floor `1e-300`; w uses absolute differences.

## Predeclared K1 rule

`PASS_WITH_SCOPE` requires the explicit two-field `mphan=0` case to be nonfallback/finite and agree with the one-field reference to

- `max |Delta H/H| <= 1e-10`,
- `max |Delta rho/rho| <= 1e-10`,
- `max |Delta w| <= 1e-10`.

If the exact zero case fails these identity thresholds, classify `M13B_SIMPLEMC_K1_REFERENCE_FAIL_OR_BRANCH_DISCONTINUITY`.

The positive-mass ladder is reported separately. Since the provider's IC search uses a finite bisection tolerance and is explicitly marked unfinished for two fields, failure of smooth positive-mass convergence does not convert an exact-zero K1 identity pass into a physical family falsification; it instead creates a K4/IC robustness warning.

## Scope

Even a K1 pass is background-only. It does not close K3 conservation/gauge/perturbation closure, K4 numerical robustness of a crossing anchor, K5 multichannel rank, or observational discrimination. No M13b family falsification is authorized.