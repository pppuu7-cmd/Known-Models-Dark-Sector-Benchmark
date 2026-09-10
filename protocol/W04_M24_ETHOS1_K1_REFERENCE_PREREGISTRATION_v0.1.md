# W04 M24 ETHOS-1 K1 decoupling preregistration v0.1

Status: FROZEN BEFORE NUMERICAL RESULT
Date: 2026-09-11
Family: F24 / M24 ETHOS-like interacting dark sector
Representative: published ETHOS model 1, n=4 free-streaming DR

## Provider and representative authority
Solver: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.
Provider/scope audit: `models/ethos_like_dark_sector/m24_ethos1_provider_scope_audit_2026-09-11.md`.

Literature representative: arXiv:1712.03976, ETHOS model 1. The published model fixes xi=0.5, n=4 and alpha_{l>=2}=3/2 and evaluates a4={0.6e5,4.2e5,1.2e6} Mpc^-1. The smallest published point a4=0.6e5 Mpc^-1 is used as the top of the K1 continuity ladder.

## Frozen species / cosmology
- h = 0.675
- omega_b = 0.0222
- omega_cdm = 0.1197 before conversion by f_idm
- N_ur = 3.046
- A_s = 2.196e-9
- n_s = 0.9655
- tau_reio = 0.06
- f_idm = 1
- xi_idr = 0.5
- stat_f_idr = 0.875
- nindex_idm_dr = 4
- idr_nature = free_streaming
- alpha_idm_dr = 1.5
- b_idr = 0
- output = tCl,pCl,mPk
- lensing = no
- non linear = none
- P_k_max_h/Mpc = 50
- z_pk = 0
- l_max_scalars = 2500
- gauge = synchronous
- overwrite_root = yes

The decoupled reference preserves the same nonzero free-streaming DR population and the same ETHOS branch selectors. It is not pure LambdaCDM.

## Cases
`ref`: `a_idm_dr` omitted; all branch selectors explicitly frozen.

`zero`: identical configuration plus `a_idm_dr = 0`.

Finite one-sided ladder in Mpc^-1:
- 6.0e4
- 1.8e4
- 6.0e3
- 1.8e3
- 6.0e2

No negative-opacity branch is tested.

## Metrics
Use normalized L2 residuals relative to explicit zero.

CMB TT/EE/TE: exact common ell grid.
P(k): positive common k support, log-k interpolation if required.

## Exact zero/omitted identity
Both reference cases must execute. TT/EE/TE/P(k) normalized L2 must each be <=1e-12.

## Finite-tail K1 gate
P(k) is the primary required response block because the published representative is defined by small-scale suppression/DAO structure.

For P(k):
- all finite points execute and are finite;
- R2 at 6.0e4 > 1e-6;
- R2 sequence is non-increasing as a4 decreases, with 2% adjacent numerical slack;
- final R2 <=0.25 of top-ladder R2;
- log-log slope over the three smallest points is positive with p>0.20.

TT/EE/TE are diagnostic continuity blocks. Each is judged with the same monotonic/contraction/slope logic only if its top-ladder R2 >1e-8. If a CMB channel stays below that response floor it is classified `SUBTHRESHOLD_RESPONSE` rather than failed. A diagnostic CMB failure does not veto K1, but it remains open for K4/K5.

## Classification
PASS: `M24_ETHOS1_K1_DECOUPLING_PASS_WITH_SCOPE_N4_FREE_STREAMING`

NOT ESTABLISHED: `M24_ETHOS1_K1_DECOUPLING_NOT_ESTABLISHED`

PROVIDER BLOCKED: `M24_ETHOS1_K1_PROVIDER_EXECUTION_BLOCKED`

All classifications retain `physical_falsification=false`; K3-K9 are not promoted by this gate.

## Family-coverage boundary
Even a PASS represents only the published ETHOS-1 n=4/free-streaming/alpha=1.5 direction. F24 remains nonterminal until response-distinct n, angular-kernel and DR-self-interaction directions are tested or shown redundant in the common response space.
