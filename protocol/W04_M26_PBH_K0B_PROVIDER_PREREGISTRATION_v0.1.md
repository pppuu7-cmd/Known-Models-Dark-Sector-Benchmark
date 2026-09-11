# W04 M26 PBH K0b provider preregistration v0.1

Date: 2026-09-11
Provider: `lesgourg/class_public` pin `e85808324f51fc694d12e3ed7439552a3c3f9540`.
Parent attempt: `M26_K0_ATTEMPT1_ACCRETION_STRESS_POINT_REIONIZATION_INCOMPATIBLE`.

## Fixed rationale

Attempt 1 established that the zero control and evaporation arm execute, while the frozen disk-accretion stress point `PBH_accretion_fraction=1e-2`, `PBH_accretion_mass=30 Msun` forces a provider-computed minimum optical depth `tau_reio_min=0.079154013316`, incompatible with the shared fixed `tau_reio=0.06`. This is a parameter/cosmology incompatibility, not missing accretion implementation.

K0b changes exactly one scientific input: the disk-accretion fraction is reduced by one decade from `1e-2` to `1e-3`. This one-decade step was fixed before K0b execution. All other provider/model/cosmology settings and K0 checks remain identical to attempt 1.

## Frozen arms

1. `zero_control`: identical to attempt 1.
2. `evaporation`: `PBH_evaporation_fraction=1e-7`, `PBH_evaporation_mass=1e15 g`, identical to attempt 1.
3. `accretion_disk`: `PBH_accretion_fraction=1e-3`, `PBH_accretion_mass=30 Msun`, `disk_accretion`, `PBH_accretion_ADAF_delta=1e-3`, `PBH_accretion_eigenvalue=0.1`.

Shared cosmology and output configuration are exactly those in `W04_M26_PBH_K0_PROVIDER_PREREGISTRATION_v0.1.md`.

## Frozen checks and classification

Exactly the attempt-1 K0 checks are retained: exact pin, exit 0, finite TT/P(k) for all arms, and TT normalized-L2 > `1e-6` versus zero control for both non-zero PBH channels.

If all pass: `M26_K0_PASS_WITH_SCOPE_NATIVE_CLASS_PBH_ENERGY_INJECTION`.
Execution/finite-output failure: `M26_K0_BLOCKED_IMPLEMENTATION_OR_PROVIDER_EXECUTION`.
Executable but inactive response: `M26_K0_NOT_ESTABLISHED_ACTIVE_PBH_RESPONSE`.

A PASS remains scoped only to native PBH evaporation/accretion energy-injection channels. PBH Poisson/discreteness/isocurvature and K1-K9 remain open. `physical_falsification=false` in all outcomes.
