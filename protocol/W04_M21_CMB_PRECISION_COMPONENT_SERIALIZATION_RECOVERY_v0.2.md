# W04 M21 CMB precision-component profile serialization recovery v0.2

Frozen: 2026-09-14 after run `34869154283` demonstrated a parser-layer implementation blocker and before any recovered component execution.

Parent protocol: `protocol/W04_M21_CONDITIONAL_CMB_PRECISION_COMPONENT_DECOMPOSITION_v0.1.md`  
Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

## Historical result preserved

Run `34869154283` is an implementation-blocked execution attempt. Exact provider builds succeeded, but component executions terminated immediately in CLASS input parsing because the first implementation physically concatenated layered precision files and therefore serialized duplicate parameter names into one parser namespace.

Observed examples:

- G1: duplicated `perturbations_sampling_stepsize` / `tol_perturbations_integration` already present in the frozen ncdm-tight baseline;
- G2: `hyper_flat_approximation_nu` exists in `cl_permille.pre` and is intentionally replaced by the G2 `cl_ref.pre` value;
- G3: scalar `transfer_neglect_delta_k_S_*` values exist in `cl_permille.pre` and are intentionally replaced by the G3 `cl_ref.pre` values.

CLASS rejects duplicate names rather than applying override semantics. No physical lane reached cosmological integration, so run `34869154283` carries no G1/G2/G3 scientific verdict.

## Recovery scope

This recovery changes **serialization only**. It does not alter:

- physical ref/f2/f3/f4 cases;
- provider pin;
- RK `evolver=0` control;
- `m21_ncdm_tight.pre` values;
- G1/G2/G3 membership;
- any numerical value in a group;
- response metrics;
- the frozen `<=3` removal criterion;
- the frozen `Emax_parent_RK/3` reduction criterion.

## Deterministic effective-profile construction

For each group, construct an ordered parameter map by applying assignments in the exact conceptual order frozen in v0.1:

1. exact `class/cl_permille.pre`;
2. exact `verification/m21/m21_ncdm_tight.pre`;
3. `evolver=0`;
4. the exact frozen G1, G2 or G3 assignment list.

If a key is assigned more than once, keep exactly the **last frozen assignment** and record the previous and final values in a merge manifest. Serialize every final key exactly once.

This is the executable form of the parent protocol's `start from ... then append ...` construction under a provider parser that forbids duplicate keys.

Expected conflict classes are fixed before the recovery run:

- G1 identical-value deduplication: `tol_perturbations_integration`, `perturbations_sampling_stepsize`;
- G2 intended override: `hyper_flat_approximation_nu` (`7000.` -> `1.e6`);
- G3 intended overrides: `transfer_neglect_delta_k_S_t0`, `transfer_neglect_delta_k_S_t1`, `transfer_neglect_delta_k_S_t2`, `transfer_neglect_delta_k_S_e` (the `cl_permille.pre` values -> `100.`).

Any additional duplicate/conflict is an implementation blocker and must stop the recovery before provider execution.

## Activation and classification

Activation remains the already-terminal full-reference result:

`M21_FULL_CMB_REFERENCE_PRECISION_REMOVES_EXCURSION`

from run `34864827822`.

Recovered G1/G2/G3 scientific classifications are exactly those frozen in the parent v0.1 protocol. No threshold or interpretation changes are authorized.

All blocker states remain non-physical. `K1_promoted=false`; `physical_falsification=false`.
