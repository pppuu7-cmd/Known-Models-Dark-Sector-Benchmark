# W03 M13b K3D2-G vanilla CLASS RK restart-layer control v0.1

Date frozen: 2026-09-14

## Trigger

K3D2-F localized the exact M13b `cl_ref.pre` first-step RK collapse to the absolute error-scale floor of near-zero **standard** Boltzmann variables in 349/349 strict-clean modes, with zero direct qcf/qpf dominance.

## Question

Is the collapse a generic CLASS/RK hard perturbation-interval restart effect, or does it require the M13b two-field handoff state?

## Exact provider

`lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.

Use the provider's unchanged `cl_ref.pre`, including `evolver = 0` and `tol_perturbations_integration = 1.e-6`.

## Frozen two-lane control

Run two otherwise identical vanilla flat LCDM jobs with no qcf/qpf adapter and no dark-sector modifications:

- **U (unsplit):** exact upstream perturbation interval construction.
- **S (split):** insert one native perturbation interval boundary at the exact background `tau(z=5)` and restart the next interval at `nextafter(tau_z5, interval_end)`. Duplicate the pre-existing CLASS approximation row across the inserted boundary. Do not change state variables, initial conditions, hierarchy equations, Einstein sources, tolerances, precision file, or solver family.

Both lanes receive the same output-only RK collapse/component diagnostics. Instrumentation may change error text only and must not alter solver logic.

## Frozen cosmology

Use identical parameters in both lanes:

- h = 0.6715
- omega_b = 0.0224
- Omega_cdm = 0.26172292868512664
- Omega_Lambda = 0.6882
- Omega_k = 0
- N_ncdm = 0
- A_s = 2.1e-9
- n_s = 0.965
- tau_reio = 0.054
- gauge = synchronous
- output = tCl,pCl,lCl,mPk,dTk
- lensing = yes
- l_max_scalars = 1200
- P_k_max_1/Mpc = 1.0
- z_pk = 0

If the density closure is rejected by CLASS, classify implementation-blocked; do not retune cosmology after execution.

## Frozen classifications

1. If U returns rc=0 and S returns nonzero rc with an RK-collapse trace at the first post-z5 split step, and the dominant terminal components are standard photon/UR hierarchy variables with no qfield variables present:

`M13B_K3D2G_GENERIC_CLASS_RK_HARD_RESTART_LAYER_EFFECT_SUPPORTED`.

2. If U and S both return rc=0:

`M13B_K3D2G_GENERIC_CLASS_RK_HARD_RESTART_EFFECT_NOT_REPRODUCED`.

3. If U itself returns nonzero rc under the frozen vanilla control, or source/build/instrumentation checks fail:

`M13B_K3D2G_VANILLA_CONTROL_IMPLEMENTATION_BLOCKED`.

4. If S fails but not at the inserted restart boundary or without a parseable RK-collapse signature:

`M13B_K3D2G_SPLIT_CONTROL_NUMERICAL_GAP_NOT_LOCALIZED`.

## Claim ceiling

This is a numerical-layer control only. It cannot modify M13b equations, thresholds, tolerances, precision settings, seam location, solver family, or K3/K4/K5 status. It cannot establish physical falsification. A positive generic-control result only reclassifies the reference failure mechanism as shared CLASS/RK hard-restart infrastructure behavior.
