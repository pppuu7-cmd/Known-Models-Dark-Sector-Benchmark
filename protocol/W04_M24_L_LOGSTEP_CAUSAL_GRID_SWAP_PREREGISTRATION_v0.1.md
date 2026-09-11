# W04 M24 `l_logstep` causal grid-swap preregistration v0.1

## Trigger

The prospective M24 multipole-grid topology gate (run `34626787237`) reproduced the frozen endpoints exactly and classified the transition as `M24_L_LOGSTEP_CMB_JUMP_ALIGNED_WITH_GRID_TOPOLOGY_CHANGE`.

Frozen endpoint facts from that gate:

- `l_logstep=1.1195`: `Emax = 0.6244612907744809`, exact-zero identity PASS;
- `l_logstep=1.1200`: `Emax = 62.644974496926224`, exact-zero identity PASS;
- jump ratio = `100.3184271345811`;
- the profile-reference grid changes from 1.1195 to 1.1200 at first differing index 33 (`ell: 102 -> 103`), with 68 changed tail nodes and symmetric-difference size 134;
- both reference grids have 101 nodes;
- some case-specific grids differ in size (notably `profile_a6k` at 1.1200 has 100 nodes), so the intervention must use each physical case's own frozen grid rather than a single common grid.

Grid changes also occur at several non-catastrophic neighboring steps. Therefore correlation/alignment alone is not sufficient for causal attribution. This follow-up performs an intervention by swapping the already-frozen grids while keeping the `l_logstep` input fixed.

## Immutable parent inputs

- CLASS commit: `e85808324f51fc694d12e3ed7439552a3c3f9540`.
- Parent topology run: `34626787237`, head `9cc95c34c32302425d2ba60310270c31662913da`.
- Frozen source grid artifacts from that run:
  - `m24-l-grid-topology-1.1195`, artifact id `10275410692`, digest `sha256:7d21cf177b97a5c058894e28eed3b5ceff4d068fe269e841223a1b71333332cf`;
  - `m24-l-grid-topology-1.1200`, artifact id `10273829802`, digest `sha256:70f30d5a3c72e9a2c00d09c5ebd16814b6f63ebcb7f558a73a00360c993ca35e`.
- Same M24 ten-case definitions and frozen global numerical-precision analyzer as the topology parent.
- `idr_streaming_trigger_tau_over_tau_k = 49` remains unchanged.
- No ETHOS physical parameter is changed.

## Intervention

Patch the pinned CLASS only at the point immediately after the normal final `ptr->l[]` list is constructed and before per-mode/per-transfer `l_size` values are derived. If `KMDSB_FORCE_LGRID_PATH` is set, read the exact ordered grid from the corresponding frozen parent `grids/<profile_case>.tsv`, resize `ptr->l` with `class_realloc`, replace `ptr->l[]`, and set `ptr->l_size_max` to the frozen target size.

Only `profile_*` cases are eligible for forcing. `default_*` controls run natively and are never grid-forced.

The patch must be dormant when the environment variable is absent.

## Frozen four-arm design

Run four independent matrix arms (`fail-fast: false`):

1. `native_1195`: input `l_logstep=1.1195`, no forced grid;
2. `force_1200_on_1195`: input `l_logstep=1.1195`, but every `profile_*` case receives its own frozen 1.1200 grid;
3. `native_1200`: input `l_logstep=1.1200`, no forced grid;
4. `force_1195_on_1200`: input `l_logstep=1.1200`, but every `profile_*` case receives its own frozen 1.1195 grid.

Run the ten M24 cases in each arm with the same execution structure as the parent. Record exit codes, the frozen parent analyzer output, and an independent dump of the final grid actually used by each profile case.

## Frozen integrity checks

- `native_1195` must reproduce parent Emax with relative error <= `1e-8`.
- `native_1200` must reproduce parent Emax with relative error <= `1e-8`.
- Every forced profile grid digest and ordered sequence must exactly match its requested frozen target grid.
- All required cases must exit zero.
- Exact-zero identity must pass in every arm.

Failure of an integrity condition is `M24_CAUSAL_GRID_SWAP_PROVIDER_OR_INSTRUMENTATION_BLOCKED` and must not be physically interpreted.

## Frozen causal metrics

Let:

- `E1195` = Emax(native_1195)
- `E1200` = Emax(native_1200)
- `E1200grid_on_1195` = Emax(force_1200_on_1195)
- `E1195grid_on_1200` = Emax(force_1195_on_1200)

Define:

- `induction_ratio = E1200grid_on_1195 / E1195`;
- `rescue_ratio = E1200 / E1195grid_on_1200`.

Frozen thresholds:

- `induction_pass` iff `induction_ratio >= 10`;
- `rescue_pass` iff `rescue_ratio >= 10`.

Also record target similarity without using it as a gate:

- `forward_target_ratio = E1200grid_on_1195 / E1200`;
- `reverse_target_ratio = E1195grid_on_1200 / E1195`.

## Frozen classification

- both induction and rescue PASS: `M24_L_LOGSTEP_CMB_CATASTROPHE_CAUSALLY_TRANSFERS_WITH_MULTIPOLE_GRID`;
- rescue only: `M24_L_LOGSTEP_CMB_CATASTROPHE_GRID_NECESSARY_NOT_SUFFICIENT`;
- induction only: `M24_L_LOGSTEP_CMB_CATASTROPHE_GRID_SUFFICIENT_NOT_NECESSARY`;
- neither: `M24_L_LOGSTEP_CMB_CATASTROPHE_NOT_CAUSALLY_ASSIGNED_TO_GRID_BY_SWAP`;
- any integrity failure: `M24_CAUSAL_GRID_SWAP_PROVIDER_OR_INSTRUMENTATION_BLOCKED`.

## Interpretation boundary

Even a bidirectional causal-transfer result is a numerical-attribution result for this frozen provider/configuration. It does not establish a physical failure of ETHOS, does not promote K1/K4, and does not imply that all numerical pathways associated with transfer sampling are understood.
