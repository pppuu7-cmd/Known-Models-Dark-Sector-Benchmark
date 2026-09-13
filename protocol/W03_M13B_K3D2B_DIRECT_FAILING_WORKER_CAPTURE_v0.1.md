# W03 M13b K3D2-B direct failing-worker capture v0.1

Date: 2026-09-14

## Motivation

The post-certificate BEGIN/END tracer established that CLASS executes many k-mode perturbation solves concurrently. Therefore chronological BEGIN/END ordering cannot identify the worker that originated the first solver failure. In the default lane 116 BEGIN and 36 END records were observed before abort; in the reference lane 133 BEGIN and 0 END records were observed. These counts are concurrency diagnostics, not scientific failures.

## Frozen diagnostic recovery

Preserve the exact provider, qcf/qpf equations, z=5 IVP, background U1 seam, native perturbation interval insertion, A1 perturbation seam, solver choice, tolerances, outputs, and k grid.

Replace only the `class_call(generic_evolver(...))` wrapper inside `perturbations_solve()` by an explicit call with byte-identical `generic_evolver` arguments. If and only if that call returns `_FAILURE_`, print one `KMDSB_MODE_FAIL` record containing:

- `index_md`
- `index_ic`
- `index_k`
- physical `k`
- exact interval start
- actual evolver start
- interval end
- the raw solver error already stored in `ppt->error_message`

Then return `_FAILURE_` without changing the error, state, or solver.

## Parallel lanes

Run independently:

1. default NDF15;
2. `cl_ref.pre` reference RK;
3. a source-only guard that verifies the diagnostic wrapper preserves the exact generic-evolver argument list and changes no tolerance/equation/state-vector setting.

## Interpretation

- One or more `KMDSB_MODE_FAIL` records directly identify workers that actually returned solver failure; concurrency no longer requires reconstructing blame from log order.
- A common `(index_md,index_ic,index_k,k)` across default and reference is strong evidence for a solver-independent mode-localized numerical/physics-interface blocker.
- Disjoint failing sets imply solver-dependent numerical sensitivity and require separate lane diagnostics.
- No result in this protocol evaluates B1/B2/B3 or authorizes K3/K4/K5 promotion.

All outcomes preserve `physical_falsification=false`, `K3_state_ceiling=PARTIAL`, `K4_promoted=false`, and `K5_promoted=false`.