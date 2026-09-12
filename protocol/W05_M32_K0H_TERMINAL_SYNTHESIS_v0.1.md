# W05 M32 K0h terminal synthesis v0.1

Date: 2026-09-12
Model: M32 DGP / EFT-Ramses infrastructure frontier.

## Immutable evidence
- exact provider: `nat-woodcock/EFT-Ramses@849ddb716041316d0e223ba22badc0d630b72435`
- immutable K0f stage-1 checkpoint artifact: `10283774354`
- K0h matrix run: `34710463111`
- K0h recovery run: `34710583217`
- recovered-nine artifact: `10303116881`
- missing target recovery job: `103598523485`

The recovered-nine artifact is authoritative for nine target objects and must contain exactly nine rows, all with `build_exit_code=0`, `target_object_exists=true`, `classification=TARGET_COMPILED_EXACT_PIN`.

The `umuscl.o` recovery job is authoritative only for infrastructure status. Its decoded job log must contain both an external runner shutdown message and exit code 143 while the frozen `make umuscl.o` command is active. Absence of an uploaded `umuscl.o` artifact is therefore not converted to a compiler/source failure.

## Frozen terminal classification
- if all nine immutable rows pass and the umuscl job shows external shutdown/143 without an explicit compiler/source diagnostic: `M32_K0H_NINE_HYDRO_TARGETS_COMPILED_UMUSCL_HOSTED_INFRASTRUCTURE_BLOCKED`.
- if any recovered immutable row fails integrity: `M32_K0H_RECOVERED_TARGET_INTEGRITY_BLOCKED`.
- if the umuscl log contains a genuine compiler/source error before termination: `M32_K0H_UMUSCL_COMPILER_OR_SOURCE_BLOCKED`.
- otherwise: `M32_K0H_TERMINAL_SYNTHESIS_INTEGRITY_BLOCKED`.

No K0 promotion and no physical falsification are allowed. If the first classification is obtained, the next allowed M32 step is an infrastructure strategy specifically for `umuscl.o`; Poisson/PM/link continuation is not yet authorized because `umuscl.o` is an exact Makefile prerequisite of the full provider target.
