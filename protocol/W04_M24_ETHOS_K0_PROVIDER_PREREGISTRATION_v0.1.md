# W04 M24 ETHOS-like K0 provider preregistration v0.1

Date: 2026-09-11
Benchmark: M24 / F24 ETHOS-like dark sector
Provider: `lesgourg/class_public` pinned at `e85808324f51fc694d12e3ed7439552a3c3f9540` (same provider lineage already used for M23).

## Question fixed before execution

Does the pinned native CLASS IDM-DR implementation execute a genuinely ETHOS-parameterized branch, distinct in scope from the already-tested M23 NADM-like `Gamma_0_nadm`, `nindex_idm_dr=0`, fluid branch, while producing finite linear cosmological observables and an active non-zero response relative to an uncoupled control?

This is K0 provenance/executability only. It is not a K1 reference-limit test, not a precision/gauge/novelty gate, and no failure is physical falsification.

## Provider authority and scope

The pinned provider explanatory input declares the IDM-DR/IDR sector to follow the ETHOS framework and documents the ETHOS-native controls `a_idm_dr`, `nindex_idm_dr`, `idr_nature`, `b_idr`, `alpha_idm_dr`, and `beta_idr`. It states `nindex_idm_dr=4` as the ETHOS default unless the alternative `Gamma_0_nadm` parameterization is used, and identifies `alpha_idm_dr=3/4` for a vector-boson mediator and `3/2` for a scalar-boson mediator.

M24 is therefore tested as an ETHOS response class with temperature-dependent scattering and free-streaming angular hierarchy. This does not claim to span all ETHOS microphysical mappings or nonlinear self-interaction phenomenology.

## Frozen cosmology/shared dark-sector content

Use the M23 baseline cosmology for direct lineage control:

- `h=0.675`
- `omega_b=0.0222`
- `omega_cdm=0.1197`
- `A_s=2.196e-9`
- `n_s=0.9655`
- `tau_reio=0.06`
- `N_ur=3.046`
- `f_idm=1`
- `N_idr=0.4290`
- `output=tCl,pCl,mPk`
- `lensing=no`
- `non linear=none`
- `P_k_max_h/Mpc=20`
- `z_pk=0`
- `l_max_scalars=2500`
- synchronous gauge.

## Frozen arms

All arms use the ETHOS-native input route, never `Gamma_0_nadm`.

1. `uncoupled_control`: `a_idm_dr=0`, `nindex_idm_dr=4`, `idr_nature=free_streaming`, `b_idr=0`, `alpha_idm_dr=1.5`, `beta_idr=1.5`.
2. `ethos_vector`: `a_idm_dr=1e6 Mpc^-1`, `nindex_idm_dr=4`, `idr_nature=free_streaming`, `b_idr=0`, `alpha_idm_dr=0.75`, `beta_idr=1.5`.
3. `ethos_scalar`: `a_idm_dr=1e6 Mpc^-1`, `nindex_idm_dr=4`, `idr_nature=free_streaming`, `b_idr=0`, `alpha_idm_dr=1.5`, `beta_idr=1.5`.

The non-zero coupling amplitude is a provider-execution stress point, not an observational best fit or canonical particle model. The scientific claim is limited to native ETHOS-parameterized executability and active response.

## Frozen K0 checks

For every arm require:

- exact provider pin;
- process exit code 0;
- non-empty finite `*_cl.dat` and `*_pk.dat` output tables;
- preserved input/config and stdout/stderr provenance.

For each non-zero ETHOS arm additionally require an active response relative to `uncoupled_control`: at least one of TT or P(k) has a normalized L2 difference greater than `1e-6` on common support. This is only a negative control against accidentally inert/misparsed inputs.

## Frozen classification

- all three arms execute, outputs are finite, exact pin holds, and both ETHOS arms are active: `M24_K0_PASS_WITH_SCOPE_PINNED_NATIVE_CLASS_ETHOS`;
- provider rejects or cannot execute one or more preregistered native ETHOS arms: `M24_K0_BLOCKED_IMPLEMENTATION_OR_PROVIDER_EXECUTION`;
- all arms execute but one or both non-zero ETHOS inputs are observationally inert under the frozen negative-control metric: `M24_K0_NOT_ESTABLISHED_ACTIVE_ETHOS_RESPONSE`.

`physical_falsification=false` in all K0 outcomes. K1-K9 remain untouched.
