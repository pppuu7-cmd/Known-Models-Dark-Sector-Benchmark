# W04 M23 DM-dark-radiation / DAO K1 decoupling preregistration v0.1

Status: FROZEN BEFORE NUMERICAL RESULT
Date: 2026-09-11
Family: F23 / M23 DM-dark-radiation scattering / dark acoustic oscillations

## Provider and source scope
Primary solver: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Provider-scope audit: `models/dm_dark_radiation/m23_provider_scope_audit_2026-09-11.md`.

The solver contains native IDM-DR background, thermodynamic opacity, tight-coupling and perturbation machinery. This gate uses the NADM interaction coordinate `Gamma_0_nadm` only.

## Critical reference semantics
The decoupling reference preserves the species content. It is not ordinary LambdaCDM:
- `f_idm = 1` remains fixed;
- `N_idr = 0.4290` remains fixed;
- `nindex_idm_dr = 0` remains fixed;
- `idr_nature = fluid` remains fixed;
- only `Gamma_0_nadm -> 0`.

The last two settings are written explicitly into every input because merely supplying the `Gamma_0_nadm` key changes their CLASS defaults. This prevents an input-parser side effect from masquerading as interaction physics.

## Source-bound representative scale
An independent public DRDM Fisher configuration at `ctrendafilova/FisherLens@652eaecce4c6d167c13dd25fb8fcbaa9a4768246`, file `paperPlots/2307.01662/generateFisherBAO_DRDM.py`, uses `f_idm=1`, `N_idr=0.4290` and `Gamma_0_nadm=2.371e-8 Mpc^-1`.

We use that value only as the top of the K1 ladder. It is not adopted as a KMDSB observational best fit.

## Frozen common cosmology
- h = 0.675
- omega_b = 0.0222
- omega_cdm = 0.1197 before conversion by `f_idm=1`
- A_s = 2.196e-9
- n_s = 0.9655
- tau_reio = 0.06
- N_ur = 3.046
- f_idm = 1
- N_idr = 0.4290
- nindex_idm_dr = 0
- idr_nature = fluid
- b_idr = 0
- output = tCl,pCl,mPk
- lensing = no
- non linear = none
- P_k_max_h/Mpc = 20
- z_pk = 0
- l_max_scalars = 2500
- gauge = synchronous
- overwrite_root = yes

## Cases
`ref`: interaction key omitted, while NADM index and fluid-DR nature remain explicitly fixed.

`zero`: identical settings plus `Gamma_0_nadm = 0`.

Finite ladder in Mpc^-1:
- 2.371e-8
- 7.113e-9
- 2.371e-9
- 7.113e-10
- 2.371e-10

This is a one-sided physical coordinate `Gamma_0_nadm >= 0`; no sign quotient is asserted.

## Metrics
Use normalized L2 residuals against the explicit-zero case:
`R2 = ||y(gamma)-y(0)||_2 / max(||y(0)||_2, 1e-300)`.

CMB TT/EE/TE are compared on an exact common ell grid. P(k) is compared over common positive-k support after log-k interpolation if required.

## Exact omitted-vs-zero identity gate
Both `ref` and `zero` must execute. For TT, EE, TE and P(k), normalized L2 residual must be <= 1e-12. Failure blocks K1 and is first treated as provider/input-semantics evidence, not physical non-decoupling.

## Finite-tail continuity gate
P(k) is the primary required DAO-response block. TT is a second required block. EE and TE are recorded diagnostics.

For each required block:
- every finite case executes and metric is finite;
- top-ladder residual > 1e-8;
- residual sequence is non-increasing as gamma decreases, with 2% adjacent numerical slack;
- smallest residual <= 0.25 times top-ladder residual;
- log-log power-law slope from the three smallest points is positive with p > 0.20.

If a diagnostic CMB block fails while P(k) and TT pass, K1 may still pass with the diagnostic failure explicitly recorded; later K4/K5 cannot inherit such a diagnostic as validated.

## Classification
PASS: `M23_K1_DECOUPLING_PASS_WITH_SCOPE_FIXED_DM_DR_CONTENT`

NOT ESTABLISHED: `M23_K1_DECOUPLING_NOT_ESTABLISHED`

PROVIDER BLOCKED: `M23_K1_PROVIDER_EXECUTION_BLOCKED`

All outcomes retain `physical_falsification=false`. K3-K9 remain unpromoted by this gate.

## M23/M24 boundary
This gate tests only the NADM-like simple DM-DR scattering direction at fixed temperature law and fixed fluid DR. It does not represent the full ETHOS family F24, whose response space includes temperature-law, angular-kernel and DR-self-interaction directions.
