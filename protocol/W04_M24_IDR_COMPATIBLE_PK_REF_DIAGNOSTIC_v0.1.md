# W04 M24 ETHOS-1 IDM-DR-compatible pk_ref diagnostic v0.1

Date: 2026-09-12
Status: FROZEN BEFORE ANY SUCCESSFUL pk_ref PHYSICS EXECUTION
Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

## Trigger and source-justified compatibility rule
The first exact `pk_ref.pre` diagnostic produced no physical outputs: all four cases stopped in pinned CLASS input validation because `pk_ref.pre` sets `ur_fluid_trigger_tau_over_tau_k=50`, while the pinned IDM-DR default is `idr_streaming_trigger_tau_over_tau_k=50`; pinned `source/input.c` explicitly forbids equality of those switching times.

The pinned provider defaults are source-defined before this diagnostic:
- `idr_streaming_trigger_tau_over_tau_k = 50.0`;
- `ur_fluid_trigger_tau_over_tau_k = 30.0`.

Therefore the only permitted compatibility change is to copy the exact provider `pk_ref.pre` and restore **only** `ur_fluid_trigger_tau_over_tau_k` from 50 to its pinned provider default 30. All other `pk_ref.pre` contents remain byte-identical. This choice is made from pinned source defaults and parser requirements, not from a physical output.

## Frozen physical cases
Use exactly the parent M24 ETHOS-1 source generator and physical configurations:
- `ref`: omitted `a_idm_dr`;
- `zero`: `a_idm_dr=0`;
- `top`: `a_idm_dr=60000` (parent `a0`);
- `tail`: `a_idm_dr=600` (parent `a4`).

No physical parameter is changed.

## Frozen metric
Use the same P(k) normalized-L2 metric and positive common-k log interpolation as `W04_M24_PK_REFERENCE_PRECISION_DIAGNOSTIC_v0.1`.
Requirements:
- all four provider runs exit 0 with finite P(k);
- ref-vs-zero P(k) R2 <=1e-12;
- top response R2 >1e-6;
- record `tail_over_top = tail_R2/top_R2`.

This single profile cannot promote K1 and cannot by itself classify precision sensitivity. It outputs either:
- `M24_IDR_COMPATIBLE_PK_REF_PROFILE_EXECUTED`; or
- `M24_IDR_COMPATIBLE_PK_REF_PROFILE_BLOCKED`.

A later immutable synthesis may compare this profile with the already-running matched default-profile artifact. Only if `tail_over_top<=0.25` may that synthesis authorize a separately preregistered full five-point compatible-pk_ref K1 confirmation. Always `K1_promoted=false`, `physical_falsification=false`.
