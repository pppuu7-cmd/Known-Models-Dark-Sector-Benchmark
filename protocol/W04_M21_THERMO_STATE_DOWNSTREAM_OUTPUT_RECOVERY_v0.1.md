# W04 M21 thermodynamics-state downstream-output recovery v0.1

Frozen: 2026-09-14 after observing the first state-extraction parser failures in run `34886286903` and before any recovery state execution.

Parent scientific protocol remains:
`protocol/W04_M21_THERMODYNAMICS_STATE_BRANCH_SIGNATURE_v0.1.md`.

Provider remains exactly:
`lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Observed blocker

Representative NDF15 lane artifacts show all `ref/f2/f3/f4` cases stop in `input_read_parameters_nonlinear()` before thermodynamics execution with:

`You requested non-linear computation but no perturbations. You must set the 'output' field.`

The state-case derivation removed `output = tCl,pCl,mPk` but preserved `non linear = halofit`. Exact CLASS therefore rejects the input because a downstream non-linear request remains active while no perturbation output is requested.

This is a state-extraction harness blocker, not a thermodynamics solver or physical result.

## Exact source authority

Exact `main/class.c` executes modules in the order:

1. background;
2. thermodynamics;
3. perturbations;
4. later Fourier/non-linear/output stages.

Therefore the `non linear = halofit` request is downstream of the thermodynamics state being audited and cannot alter the already computed `x_e`, opacity, visibility or baryon-temperature state.

## Recovery scope

The only permitted state-case transformation relative to the original K1 physical INI is now:

- remove exact line `output = tCl,pCl,mPk`;
- remove exact line `non linear = halofit`;
- add exact line `write_thermodynamics = yes`.

Every other line must be byte-for-byte preserved and order-preserved.

The recovery manifest must record both removed lines, the one added line, source/state hashes and `physical_lines_preserved=true` after reconstructing the original by restoring exactly those downstream lines.

No solver/tolerance dimension changes. The six lanes remain exactly:

- NDF15: `1e-5`, `1e-6`, `1e-7`;
- RK: `1e-5`, `1e-6`, `1e-7`.

All primary columns, redshift window, interpolation rules, J definition, `Jmax>=3` threshold, branch-change/control edge lists and frozen classification remain unchanged from the parent protocol.

## Recovery ceiling

If recovery reaches thermodynamics execution, only the parent state-signature classifier may be used. Any further parsing/output-schema failure remains BLOCKED. No code-defect, solver-quality, production-setting, K1/K3/K4, or physical M21 claim is allowed from this recovery itself.
