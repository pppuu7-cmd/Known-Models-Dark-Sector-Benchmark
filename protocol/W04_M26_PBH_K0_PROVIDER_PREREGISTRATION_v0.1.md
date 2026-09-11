# W04 M26 primordial-black-hole DM K0 provider preregistration v0.1

Date: 2026-09-11
Benchmark: M26 / F26 primordial-black-hole dark matter
Provider: `lesgourg/class_public` pinned at `e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Purpose fixed before execution

Establish whether the pinned native CLASS energy-injection implementation executes two PBH-specific cosmological response channels documented by the provider: Hawking evaporation and baryonic matter accretion. This is a scoped K0 provenance/executability gate only.

M26's broader census definition also includes compact-object discreteness/Poisson/isocurvature response. Those effects are explicitly **not** established by this K0 gate. A PASS therefore means `PASS_WITH_SCOPE_PBH_ENERGY_INJECTION_PROVIDER`, not complete PBH-family coverage.

No K0 outcome is physical falsification. K1-K9 remain untouched.

## Provider-native semantics

The pinned provider documentation exposes:

- `PBH_evaporation_fraction` and `PBH_evaporation_mass` (mass in g), with the evaporated-particle spectrum entering the time-dependent injection efficiency;
- `PBH_accretion_fraction` and `PBH_accretion_mass` (mass in solar masses), with native `spherical_accretion` and `disk_accretion` prescriptions.

Only these provider-native inputs are used. No PBH source equations are added or patched.

## Frozen shared cosmology

Use a simple linear CMB/P(k) configuration:

- `h=0.675`
- `omega_b=0.0222`
- `omega_cdm=0.1197`
- `A_s=2.196e-9`
- `n_s=0.9655`
- `tau_reio=0.06`
- `N_ur=3.046`
- `output=tCl,pCl,mPk`
- `lensing=no`
- `non linear=none`
- `P_k_max_h/Mpc=10`
- `z_pk=0`
- `l_max_scalars=2500`
- synchronous gauge.

## Frozen arms

1. `zero_control`: `PBH_evaporation_fraction=0`, `PBH_evaporation_mass=0`, `PBH_accretion_fraction=0`, `PBH_accretion_mass=0`.
2. `evaporation`: `PBH_evaporation_fraction=1e-7`, `PBH_evaporation_mass=1e15 g`; accretion inputs remain zero.
3. `accretion_disk`: `PBH_accretion_fraction=1e-2`, `PBH_accretion_mass=30 Msun`, `PBH_accretion_recipe=disk_accretion`, `PBH_accretion_ADAF_delta=1e-3`, `PBH_accretion_eigenvalue=0.1`; evaporation inputs remain zero.

The two non-zero points are provider-execution stress points only. They are not claimed as observationally allowed, representative posterior points, or preferred PBH masses/fractions.

## Frozen K0 checks

For every arm require:

- exact provider pin;
- exit code 0;
- finite, non-empty `*_cl.dat` and `*_pk.dat`;
- preserved input and stdout/stderr provenance.

For each non-zero PBH arm additionally require an active response versus `zero_control`: normalized L2 difference in TT greater than `1e-6`. This is only a negative control against silently ignored/misparsed PBH inputs.

## Frozen classification

- all three arms execute at the exact pin, outputs are finite, and both non-zero PBH channels pass the active-response negative control: `M26_K0_PASS_WITH_SCOPE_NATIVE_CLASS_PBH_ENERGY_INJECTION`;
- provider rejects/fails one or more frozen PBH arms or finite outputs are missing: `M26_K0_BLOCKED_IMPLEMENTATION_OR_PROVIDER_EXECUTION`;
- all arms execute but at least one non-zero arm is inactive under the frozen TT metric: `M26_K0_NOT_ESTABLISHED_ACTIVE_PBH_RESPONSE`.

`physical_falsification=false` in all cases. Even a PASS does not establish PBH discreteness/Poisson/isocurvature, exact zero-limit continuity, numerical robustness, or K1-K9.
