# M24 ETHOS source-level perturbation closure audit — 2026-09-11

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Scope
This audit records whether the native general ETHOS/IDM-DR implementation contains the perturbation structures needed by the M24 n=4/free-streaming representative. It does not numerically promote K3 or K4.

## Momentum-exchange closure
The same native IDM-DR system used for M23 contains paired interacting-DM / interacting-DR velocity exchange. The inertial ratio is `S_idm_dr=(4/3) rho_idr/rho_idm`, so the DM and relativistic-radiation Euler equations carry the corresponding weighted internal momentum transfer.

## Free-streaming DR hierarchy
For `idr_nature=free_streaming`, the solver does not truncate the ETHOS angular physics to a perfect fluid. It evolves:
- DR shear (l=2),
- l=3,
- all higher multipoles to `l_max_idr`,
with collision/damping terms of the form
`-(alpha_l * dmu_idm_dr + beta_l * dmu_idr) * F_l`.

Thus the `alpha_idm_dr` angular coefficients enter the DM-DR collision hierarchy explicitly, while `beta_idr` weights the optional DR self-interaction opacity. This is the response-distinct structure that M23's fluid-DR slice did not probe.

## Tight-coupling branch
When IDM-DR scattering becomes stiff, CLASS uses a dedicated IDM-DR tight-coupling approximation. The free-streaming branch reconstructs the DR shear using the same `alpha_idm_dr` coefficients and interaction opacity rather than silently dropping the angular structure.

## ETHOS-1 representative
M24 ETHOS model 1 uses:
- n=4,
- free-streaming DR,
- alpha_{l>=2}=3/2,
- b_idr=0.
For this slice, beta_l is dynamically inactive because the DR self-scattering opacity is zero, while alpha_l remains active in the DM-DR hierarchy.

## Current K3 status
Source-level classification:
`SOURCE_CLOSED_ETHOS_IDM_DR_FREE_STREAMING_HIERARCHY_NUMERICAL_K3_NOT_YET_PROMOTED`

This is stronger than a background-only provider and rules out the specific failure mode of missing perturbation interaction terms. However it is not yet a canonical K3 PASS because:
- the ETHOS-1 representative K1 run must first execute and establish its decoupling path;
- numerical robustness of the hierarchy/tight-coupling switching remains a K4 question;
- cross-gauge numerical response regression remains open.

## Future-model lesson
A future general interacting dark-sector model cannot be validated by background exchange plus a two-variable fluid closure when its microphysics predicts nontrivial angular scattering. The collision kernel/hierarchy coefficients are part of the physical model and must survive source, convergence and response-rank audits.
