# W04 M21 thermodynamics-state explicit-none parser recovery v0.1

Frozen: 2026-09-14 after terminal pre-execution recovery-v0.2 blocker `34886953863` and before any v0.3 state execution.

Parent scientific protocol remains `protocol/W04_M21_THERMODYNAMICS_STATE_BRANCH_SIGNATURE_v0.1.md` and all six solver/tolerance lanes, state columns, z-window, edge list, J definition, J>=3 threshold and classifier remain unchanged.

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Exact parser authority

The frozen M21 generator contains `non linear = none`, not `halofit`.

Exact `source/input.c` first reads `non_linear` (or compatibility key `non linear`). If the key is present at all, it tests `ppt->has_perturbations`; with the spectrum `output` line removed, this is false and CLASS stops with `You requested non-linear computation but no perturbations` **before** interpreting whether the supplied value is `halofit`, `hmcode`, or `none`.

Therefore a no-perturbation thermodynamics-only input must omit the `non linear` key entirely. Omitting it leaves the exact default non-linear method `none` and cannot change the already-earlier thermodynamics state.

## Only permitted state-case transformation

Relative to each original frozen K1 physical INI:

- remove exact line `output = tCl,pCl,mPk`;
- remove exact line `non linear = none`;
- add exact line `write_thermodynamics = yes`;
- preserve every other line byte-for-byte and order-for-order.

The case manifest must prove both removed lines occur exactly once and every retained line is unchanged.

## Recovery gates and ceiling

The v0.3 lane metadata must record exact provider pin, all four rc=0, one thermodynamics file per case, exact transformed-INI hashes, baseline precision hashes and physical-line preservation.

Any new parser/output-schema failure remains `M21_THERMO_STATE_BRANCH_SIGNATURE_BLOCKED` and cannot be interpreted scientifically.

This recovery changes only input serialization for state extraction. It cannot change the parent 2x3 experiment, thresholds, interpretation ceiling, K1/K3/K4 status, or physical conclusions.
