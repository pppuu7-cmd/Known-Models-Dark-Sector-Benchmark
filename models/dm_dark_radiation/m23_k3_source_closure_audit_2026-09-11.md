# M23 K3 source-closure audit — 2026-09-11

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Scope
This audit asks whether the native DM-dark-radiation implementation contains paired perturbation-level interaction terms consistent with internal momentum exchange for the exact NADM branch used by M23 K1. It does not claim a completed cross-gauge numerical regression.

## Thermodynamic interaction rate
The provider computes the IDM-DR opacity `dmu_idm_dr` from the native coupling and fixed dark-sector densities. The perturbation module reads the same thermodynamic rate and defines
`S_idm_dr = (4/3) rho_idr / rho_idm`.

## Interacting-DM Euler equation
When the IDM-DR tight-coupling approximation is off, the source adds
`- S_idm_dr * dmu_idm_dr * (theta_idm - theta_idr)`
to the interacting-DM velocity equation.

The code also provides a dedicated IDM-DR tight-coupling branch rather than silently dropping the exchange in the stiff regime.

## Dark-radiation Euler equation
The DR velocity equation receives the counterpart
`+ dmu_idm_dr * (theta_idm - theta_idr)`.

With the inertial weighting carried by `S_idm_dr=(4/3)rho_idr/rho_idm`, these two terms are the paired internal momentum-transfer structure expected for DM <-> relativistic-radiation scattering.

For free-streaming DR branches the hierarchy also contains interaction damping terms in the shear and higher multipoles. The M23 K1 NADM branch explicitly fixes `idr_nature=fluid`, so those higher-multipole terms are not used to enlarge the K1 claim.

## Gauge/frame scope
M23 numerical K1 used synchronous gauge. The source equations are integrated inside CLASS's gauge-aware perturbation machinery, but this source audit alone does not establish numerical cross-gauge equality of small derived response residuals.

Therefore K3 classification is:
`PASS_WITH_SCOPE_NATIVE_IDM_DR_PERTURBATION_MOMENTUM_CLOSURE_SYNCHRONOUS_NUMERICAL_CROSS_GAUGE_OPEN`.

This is sufficient to reject the failure mode seen in providers where interaction terms exist only at background level or are commented out at perturbation level. It is not sufficient for K4/K5 promotion without numerical convergence.

## Scientific boundary
No physical model preference, observational significance, DAO uniqueness, or family falsification follows from this source audit. M24 ETHOS remains distinct and open.
