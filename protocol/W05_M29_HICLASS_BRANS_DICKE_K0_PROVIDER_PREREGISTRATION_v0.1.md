# W05 M29 hi_class Brans-Dicke K0 provider preregistration v0.1

Date: 2026-09-11
Family: F29 / M29 Brans-Dicke scalar-tensor gravity
Gate: K0 provenance/provider executability only

## Frozen provider

Repository: `hiclass-code/hi_class_public`
Commit: `0009f51d89e6465c79e570b496c66fc90058fa77`
Native example: `gravity_models/brans_dicke.ini`

The shipped example identifies the covariant model as Brans-Dicke with `G_2=(omega_BD/phi)X-V0`, `G_4=phi M_p^2/2`, parameters `(V0, omega_BD, phi_ini, phi_prime_ini)`, `M2_tuning_smg=yes`, `M2_today_smg=1`, radiation-era attractor initialization for `phi_prime_ini=0`, and explicit early-time numerical-stability settings. These provider conventions are frozen for this K0 probe.

## Independent arms

1. `bd_author`: execute the unmodified shipped Brans-Dicke example except for output root/verbosity-only path changes.
2. `lcdm_control`: execute a minimal same-provider vanilla LCDM control requesting the same broad output classes (`tCl,mPk`) and background output.

The two arms are scientifically independent and must run in parallel with `fail-fast:false`.

## K0 acceptance

K0 provider/provenance is `PASS_WITH_SCOPE` iff all of the following hold:

- checkout HEAD equals the pinned commit exactly;
- provider compiles successfully;
- both arms return exit code 0;
- each arm produces non-empty finite CMB TT and linear matter-power outputs;
- the Brans-Dicke arm additionally produces a non-empty finite background table;
- the finite Brans-Dicke author point is numerically distinguishable from the same-provider LCDM control in at least one common CMB-TT or P(k) sample (`max relative difference > 1e-6`), guarding against a silently inactive model branch.

If build/configuration/output-format fails, classify `BLOCKED_IMPLEMENTATION` or `INFRASTRUCTURE_FAIL`, never physical failure.

## Scope guard

This gate does **not** test the GR limit, K1, numerical convergence K4, gauge/conservation closure K3, observational distinguishability, or physical validity of the Brans-Dicke family. It cannot promote any later gate and cannot produce physical falsification.

A separate prospective K1 preregistration is required before inspecting any omega_BD limit ladder.