# W04 M21 G1A single-key recombination precision decomposition v0.1

Date: 2026-09-14
Status: PREREGISTERED BEFORE EXECUTION
Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`
Parent stage-2 run: `34872522336`
Parent stage-2 artifact: `10360228613`

## Motivation
The prospectively frozen stage-2 decomposition classified G1A as `SUBGROUP_REMOVES_EXCURSION` with Emax=0.03431664516144772, while G1B/G1C were insufficient. G1A changes four recombination/thermodynamics precision keys simultaneously. This gate asks whether one key is sufficient or whether the removal requires a within-G1A interaction.

## Frozen arms
Exactly one of the following G1A overrides is applied per arm on top of the unchanged `cl_permille.pre` + `verification/m21/m21_ncdm_tight.pre` + `evolver=0` baseline:

- `A_NZ`: `recfast_Nz0 = 100000`
- `A_THERMO`: `tol_thermo_integration = 1.e-5`
- `A_HE`: `recfast_x_He0_trigger_delta = 0.01`
- `A_H`: `recfast_x_H0_trigger_delta = 0.01`

No other G1A key may be changed in a single-key arm. Physics inputs, warm fraction cases and provider source remain frozen.

## Cases and parallelism
For every arm run the same four immutable M21 cases `ref,f2,f3,f4`, independently with `fail-fast:false`. Aggregate only after all 16 lanes finish.

## Frozen classifier
Use the same TT/EE/TE excursion metric and parent RK reference Emax=534.8355868817356 used by stage 2.

For each arm:
- `SINGLE_KEY_REMOVES_EXCURSION` iff every TT/EE/TE excursion factor <= 3.0.
- `SINGLE_KEY_REDUCES_EXCURSION` iff Emax <= 534.8355868817356/3 and removal criterion is not met.
- `SINGLE_KEY_INSUFFICIENT` otherwise.
- Missing/nonfinite/provider-failed evidence => `SINGLE_KEY_BLOCKED`.

Aggregate classification:
- if any arm removes/reduces: `M21_G1A_SINGLE_KEY_SUFFICIENCY_IDENTIFIED`;
- if all four are finite/valid but insufficient: `M21_G1A_WITHIN_SUBGROUP_INTERACTION_REQUIRED`;
- otherwise: `M21_G1A_SINGLE_KEY_DECOMPOSITION_BLOCKED`.

## Interpretation ceiling
This is numerical failure-mode localization only. It does not prove a unique CLASS bug, does not authorize post-hoc retuning, does not promote K1/K3/K4, and is not physical falsification of mixed cold+warm DM. If one key is sufficient, a separate prospectively frozen local value/step diagnostic is required before any robustness claim. If interaction is required, only preregistered pairwise decomposition may follow.
