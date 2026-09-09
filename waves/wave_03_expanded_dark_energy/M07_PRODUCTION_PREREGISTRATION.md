# M07 production preregistration — canonical quintessence

Frozen: 2026-09-09
Wave: W03 — Expanded dark-energy mechanisms
Model: M07 canonical scalar-field / quintessence
Status: **PREREGISTERED BEFORE PRODUCTION FINITE-LAMBDA RUN**

## Provenance

W03 DSIR authority:
`pppuu7-cmd/Dark-Sector-Influence-Reconstruction@328f2ca80b724870b851c7fe6366cce1ca5086cd`

Pinned solver:
`lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

Calibration run used only to measure the implementation/reference floor:
GitHub Actions run `34325977559`, head `e74f798a685f8b92f75ef3afe0b4be03eb51a576`.

The calibration finite-lambda values `{0.05,0.10,0.20}` remain descriptive infrastructure probes and are not B8 evidence.

## Frozen model branch

Pinned potential subset:

`V(phi)=(1+A) exp(-lambda phi)`

with:
- `alpha=0`;
- `B=0`;
- `attractor_ic_scf=no`;
- `phi_ini=1`;
- `phi_prime_ini=0`;
- physical theory parameter: `lambda`;
- closure/shooting nuisance: `A`;
- `scf_tuning_index=2`.

The nonzero field-coordinate origin `phi_ini=1` is a numerical coordinate choice required to avoid the literal `alpha*(phi-B)^(alpha-1)` alpha-zero singularity at `phi=B`; for alpha=0 its constant shift is absorbed into the normalization nuisance and does not change the frozen pure-exponential physical branch.

## Calibration result frozen before production science

The successful lambda-zero split reference in run `34325977559` achieved:

- target `Omega_scf=0.10`;
- achieved `Omega_scf(today)=0.10000000013560413`;
- `w_scf=-1` at all frozen z nodes;
- `phi=1` at all frozen z nodes;
- `phi_prime=0` at all frozen z nodes;
- `max_abs_lnH = 5.462919005900343e-11` versus pure LambdaCDM;
- `max_abs_lnP = 4.111520165089289e-7` on the frozen 7x5 low-k grid.

This establishes the implementation floor for the matched reference control. It does not itself constitute a prospective prediction.

## Hard production reference tolerance

The following thresholds are frozen now, after the calibration floor was measured and before any dark-energy-dominant finite-lambda production output is inspected:

1. `max_abs_lnH <= 1.0e-8` on frozen z nodes;
2. `max_abs_lnP <= 1.0e-5` on the frozen 7x5 low-k grid;
3. `abs(Omega_scf(today)-Omega_scf_target) <= 1.0e-6`;
4. lambda-zero `max_z abs(w_scf(z)+1) <= 1.0e-10`;
5. lambda-zero `max_z abs(phi_prime(z)) <= 1.0e-12`.

These are deliberately looser than the measured calibration floor while still remaining far below the response scale intended for scientific interpretation. They may not be relaxed after seeing production finite-lambda outputs without creating an explicit new protocol version and treating the old production attempt as a failed frozen gate.

## Dark-energy-dominant production branch

The pure LambdaCDM calibration background gives the present reference cosmological-constant fraction

`Omega_Lambda_ref = 0.682686955086854`.

Production therefore targets

`Omega_scf_target = 0.682686955086854`,

so the lambda-zero scalar branch replaces essentially the full reference Lambda component rather than the 10% subdominant calibration component.

The matched pure LambdaCDM case remains the response origin.

## Frozen production lambda grid

The first production grid is:

`lambda = {0.025, 0.075, 0.15, 0.30}`.

These values are distinct from the calibration finite-lambda diagnostic set `{0.05,0.10,0.20}`.

They are production response points for B3-B6 geometry/comparator work, **not** B8 holdouts. No universal or predictive relation has been defined yet.

## Frozen response grid

Redshift nodes:
`z={0.295,0.51,0.706,0.934,1.317,1.491,2.33}`.

Low-k nodes:
`k={0.001,0.003,0.01,0.03,0.1} h/Mpc`.

Primary response coordinates:

`r_H(z)=ln[H_M07(z)/H_LCDM(z)]`

`r_Delta(k,z)=ln[P_M07(k,z)/P_LCDM(k,z)]`.

This initial production pass does not imply complete B4 coverage: scalar/metric/slip and observation-space blocks remain separately auditable.

## Production decision rules

1. If pure LambdaCDM or lambda-zero scalar execution fails: `BLOCKED_NUMERICAL`/implementation diagnosis; no finite-lambda science.
2. If lambda-zero execution succeeds but violates any frozen hard reference tolerance: B1 production reference gate fails within this implementation scope; do not reinterpret finite-lambda outputs.
3. If lambda-zero passes, finite-lambda response may enter B3/B4 theory-response analysis.
4. B5 observational promotion remains forbidden without a pinned observational operator/covariance.
5. B6 must attack at least M01 smooth-w and M05 designer f(R) on valid common blocks.
6. No production point in this file is a B8 holdout.

## Natural-scale shooting seed

For every scalar production point use

`A_seed(lambda)=3 Omega_scf_target H0^2 exp(lambda phi_ini)-1`.

This seeds only the numerical normalization nuisance. `lambda` is never changed by shooting.
