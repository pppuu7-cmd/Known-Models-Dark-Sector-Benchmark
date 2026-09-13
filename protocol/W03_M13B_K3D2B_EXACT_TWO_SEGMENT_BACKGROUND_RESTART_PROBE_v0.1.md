# W03 M13b K3D2-B exact two-segment background restart probe v0.1

Frozen: 2026-09-14 after source-audit recovery run 34787372736 passed and before any two-segment numerical result is inspected.

Provider: `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.
Parent adapter: `M13B_K3D2_CLASS_TWO_FIELD_SPECIES_ADAPTER_BUILD_AND_REDUCTION_PASS_WITH_SCOPE`.
Parent numerical blocker: `M13B_K3D2B_RK_RECOVERY_NUMERICAL_BLOCKED_NO_B1_B2_B3_EVALUATION`.

## Motivation

The enabled hard-handoff background failed because a single NDF15 integration attempted to step across the exact derivative discontinuity at `loga=log(1/6)`. Replacing NDF15 by RK was prospectively tested and rejected by the frozen disabled-adapter P(k) equivalence gate.

Exact-pin source inspection establishes that `background_solve` uses one local `generic_evolver` call with mutable `loga_ini`/`loga_final` and the same `pvecback_integration` state vector. `evolver_ndf15` constructs all method/Jacobian/history storage locally per call and initializes the output cursor by advancing through the global `t_vec` until `t_vec[next] >= x_ini`. Therefore a second NDF15 call can restart from the first call's final state while retaining global background-table indexing.

## Frozen implementation

Define exactly

`loga_handoff = log(1/6)`.

Replace the single background NDF15 call by two otherwise byte-equivalent calls:

1. `[loga_ini, loga_handoff]`;
2. `[loga_handoff, loga_final]`;

using the same `pvecback_integration`, `used_in_output`, background workspace, tolerances, global `pba->loga_table`, `pba->bt_size`, and `background_sources` callback.

No solver family, tolerance, cosmological parameter, field equation, sampling table, output callback, or acceptance threshold is changed.

For the enabled hard-handoff realization only, change the four background handoff guards from `a < 1./6.` to `a <= 1./6.`. This assigns the single boundary point to the frozen pre-handoff branch so the first segment terminates on the frozen IVP. The post-handoff equations for every open interval `a>1/6` are unchanged. Perturbation equations are not modified in this probe.

## Lane N: null segmentation control

Run exact-pin upstream CLASS twice with identical frozen LambdaCDM inputs and NDF15:

- unsegmented upstream;
- segmented upstream.

Required:

- both provider return codes zero;
- finite positive matter-power tables on the common k-range;
- normalized L2 difference in P(k) <= `1e-8`;
- relative H0 difference <= `1e-10`.

PASS means the restart itself is numerically acceptable for this control. Failure blocks the implementation route and cannot be relaxed retrospectively.

## Lane E: enabled background implementation probe

Apply, in order:

1. frozen K3D2 qcf+qpf adapter entrypoint;
2. exact two-segment background restart;
3. boundary-point ownership recovery (`<=` only in the four background handoff guards).

Use the already frozen enabled K3C1-normalized input and default NDF15 background evolver.

This lane is deliberately implementation-only. Required:

- build succeeds;
- provider return code zero;
- a background file is produced;
- all background rows are finite and H>0;
- stderr contains no `stepsize underflow`;
- output contains at least one sample below and above `a=1/6`;
- the z=5 interpolated direct fields satisfy `|phi_qcf-0.92| <= 2e-4`, `|psi_qpf-1.02| <= 2e-4`, `|dphi/dN| <= 2e-3`, `|dpsi/dN| <= 2e-3`.

The crossing, z<5 trajectory, B1 acceptance, B2 full-Boltzmann spectra and B3 direct perturbation comparison are **not evaluated** in this probe.

## Classification

If both lanes pass:

`M13B_K3D2B_EXACT_TWO_SEGMENT_BACKGROUND_RESTART_IMPLEMENTATION_PASS_WITH_SCOPE`.

This authorizes a separately frozen full K3D2-B regression using the same restart implementation. K3 remains PARTIAL until that regression passes. K4/K5 remain closed.

If Lane N fails:

`M13B_K3D2B_TWO_SEGMENT_NULL_CONTROL_FAIL`.

If Lane N passes but Lane E fails:

`M13B_K3D2B_TWO_SEGMENT_ENABLED_BACKGROUND_BLOCKED`.

No outcome in this protocol is a physical falsification of the quintom family or a reproduction of the unavailable author code.
