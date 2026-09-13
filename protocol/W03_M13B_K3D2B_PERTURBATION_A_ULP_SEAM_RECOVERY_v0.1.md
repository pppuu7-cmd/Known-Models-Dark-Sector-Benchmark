# W03 M13b K3D2-B perturbation a-ULP seam recovery v0.1

Frozen: 2026-09-14 after run 34788270310 and before any a-ULP seam result is inspected.

Provider: `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.
Parent: `protocol/W03_M13B_K3D2B_PERTURBATION_NATIVE_INTERVAL_SPLIT_PROBE_v0.1.md`.

## Established observation

The native perturbation interval split compiles and the disabled exact-null lane passes. In enabled default and reference lanes, the original long interval is successfully split at the z=5 conformal-time boundary, but the second numerical interval still fails immediately. For default NDF15 the reported failing interval changes from `[558.061,13984.9]` to `[6257,13984.9]`.

The previous seam recovery moved the second numerical start by one representable value in conformal time. That shift is smaller than the resolution at which the interpolated background scale factor changes branch, so the first RHS evaluation can still reconstruct the isolated left-owned handoff scale factor. B1/B2/B3 remain unevaluated.

## Frozen recovery

Keep the native inserted interval boundary exactly at physical `z=5`, obtained from `background_tau_of_z(pba,5.,...)`. Keep `perturbations_vector_init` at that exact boundary and keep the state vector unchanged.

Define the right-side numerical start through the physical scale-factor coordinate rather than by `nextafter` on tau:

- A1: `a_post = nextafter(exp(log(1./6.)),1.0)`;
- A2: apply `nextafter(...,1.0)` twice.

For each lane compute

`z_post = 1/a_post - 1`

and obtain `tau_post` only through existing `background_tau_of_z(pba,z_post,&tau_post)`.

The second qfield interval numerical evolver starts at `tau_post`. The state is not evolved, interpolated, reset or fitted between `tau_handoff` and `tau_post`.

No open-interval equation, tolerance, solver family, approximation criterion, hierarchy equation, Einstein source, initial condition or acceptance threshold changes. qfield-disabled CLASS remains on the untouched native interval path.

## Frozen per-lane implementation gates

For A1 and A2 independently, on the unchanged K3C1-normalized enabled cosmology:

- build succeeds;
- provider rc=0 for default NDF15 and `cl_ref.pre` RK;
- no minimum-step/underflow diagnostic;
- finite positive P(k);
- two requested scalar perturbation trajectories are present and finite;
- photon and ultra-relativistic hierarchy columns are present;
- qcf and qpf direct perturbations are dynamically nonzero.

The `0.1` direct-field amplitude gate from the parent remains unchanged and is evaluated on the same raw direct qfield columns.

## A1/A2 sensitivity

If both A1 and A2 execute successfully, compare their default-lane observables/trajectories. Require:

- normalized P(k) L2 <= `1e-7`;
- at today, absolute differences in each direct qcf/qpf perturbation variable <= `1e-7` after applying the same B3 primordial normalization to both lanes;
- relative H0 difference <= `1e-10`;
- background today qfield differences each <= `1e-8`.

These are implementation sensitivity gates only; B1/B2/B3 are not promoted here.

## Classification

All A1/A2 default/reference execution gates plus sensitivity pass:

`M13B_K3D2B_PERTURBATION_A_ULP_SEAM_IMPLEMENTATION_PASS_WITH_SCOPE`, authorizing A1 for the already frozen full B1/B2/B3 regression.

Otherwise:

`M13B_K3D2B_PERTURBATION_A_ULP_SEAM_BLOCKED`.

K3 remains PARTIAL; K4/K5 remain closed. No author-code reproduction or physical falsification is claimed.
