# M24 ETHOS-like dark sector — ETHOS model 1 provider/scope audit (2026-09-11)

## Family boundary
M24/F24 is broader than M23/F23. M23 tested the NADM-like `Gamma_0_nadm` slice with interaction-temperature index n=0 and fluid dark radiation. The native CLASS ETHOS interface independently exposes:
- the interaction amplitude `a_idm_dr` / `a_dark`;
- temperature-law index `nindex_idm_dr`;
- DR nature (`free_streaming` or `fluid`);
- DR self-interaction strength `b_idr`;
- DM-DR angular hierarchy coefficients `alpha_idm_dr`;
- DR self-interaction hierarchy coefficients `beta_idr`.

Therefore the full ETHOS response family cannot be represented by M23.

## Primary provider
`lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Its explanatory/source interface states that `a_idm_dr` is the ETHOS `a_dark` coefficient in Mpc^-1 and that the DR-DM opacity scales with `((1+z)/10^7)^nindex_idm_dr`. The default ETHOS index is n=4; default DR nature is free streaming unless the distinct `Gamma_0_nadm` input is used.

## Literature-bound representative
Use the published ETHOS model 1 discussed in arXiv:1712.03976 (Das, Mondal, Rentala, Suresh), itself mapped from the ETHOS framework. The model is Dirac DM scattering with a sterile-neutrino DR bath through a heavy vector mediator. The paper fixes:
- temperature ratio xi = T_DR/T_CMB = 0.5;
- only a4 as the relevant nonzero interaction coefficient, corresponding to n=4;
- alpha_{l>=2} = 3/2;
- benchmark a4 values 0.6e5, 4.2e5 and 1.2e6 Mpc^-1.

The paper's linear spectra explicitly show small-scale suppression and DAO structure for these benchmarks, establishing that n=4/free-streaming ETHOS is response-distinct from a simple n=0 fluid-DR interaction slice.

## First representative chosen for K1
The K1 continuity ladder is anchored at the smallest published benchmark a4=0.6e5 Mpc^-1 rather than at the observational bound or strongest point. This limits unnecessary stiffness while retaining a literature-bound finite response.

Fixed physical assumptions:
- f_idm = 1 (all CDM assigned to the interacting DM species);
- xi_idr = 0.5;
- stat_f_idr = 0.875 (fermionic sterile-neutrino-like DR);
- nindex_idm_dr = 4;
- idr_nature = free_streaming;
- alpha_idm_dr = 1.5;
- b_idr = 0;
- beta_idr left at its provider default because b_idr=0 makes the DR self-scattering kernel inactive.

## Reference map
K1 removes only `a_idm_dr` while preserving the full species content and all ETHOS branch selectors above. The reference is therefore uncoupled IDM-labelled matter + free-streaming DR with xi=0.5, not ordinary LambdaCDM.

This follows the W04 durable rule that an interaction-decoupling reference preserves species content. Pure-LambdaCDM comparison belongs to later manifold/observation-space gates where the extra-radiation direction is profiled explicitly.

## K2 geometry
The physical interaction amplitude is treated as one-sided `a_idm_dr >= 0`. No negative-opacity branch is promoted to a physical model.

## Scope limitation
Passing the first n=4/xi=0.5/alpha=1.5 K1 representative would establish an executable decoupling direction for one published ETHOS model, not terminal coverage of F24. Later M24 work must test response-distinct ETHOS directions, especially changes in n, angular coefficients and DR self-interaction, before F24 can be treated as represented.
