# W03 M13b K3D1 exact-pin CLASS adapter-base structural audit v0.1

Date frozen: 2026-09-13  
Target: F13/M13b true two-field quintom  
Selected adapter base: `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`  
Scope: infrastructure/source audit before any quintom patch  
Physics modification in this gate: **NONE**

## Trigger

K3D0 found no public DIRECT_PROVIDER_GRADE two-field quintom Einstein–Boltzmann solver. Standard CLASS is the strongest ADAPTER_GRADE base because it already supplies the full source-complete Boltzmann/recombination/output stack and one direct canonical scalar-field species.

K3D1 must establish the exact modification boundary mechanically before any source patch is written.

## Frozen provider

Repository: `https://github.com/lesgourg/class_public.git`  
Commit: `64bbab707faf4de4779a9e04edd180fef18d98fa`.

No later upstream commit may be substituted inside this gate.

## Frozen control build/run

Build exact pin on Ubuntu 22.04 with the provider Makefile:

`make -j2 class`

Run one minimal standard LambdaCDM control with:

- `h=0.67`;
- `omega_b=0.0224`;
- `omega_cdm=0.12`;
- `A_s=2.1e-9`;
- `n_s=0.965`;
- `tau_reio=0.054`;
- `output=mPk`;
- `P_k_max_1/Mpc=1`;
- `z_pk=0`.

The control must return provider rc=0 and emit a finite matter-power output. This is infrastructure evidence only.

## Frozen source-structure checks

The executable audit must verify at the pinned source:

### A. Existing scalar-field species is direct and singular

1. `include/background.h` exposes one scalar background pair `index_bi_phi_scf`, `index_bi_phi_prime_scf` and one `Omega0_scf` family coordinate.
2. `include/perturbations.h` exposes one perturbation pair `index_pt_phi_scf`, `index_pt_phi_prime_scf`.
3. No second `scf` field pair such as `phi2_scf`, `psi_scf`, `scf2` is already declared in the core background/perturbation headers.

### B. Existing scalar species has canonical signs

4. `source/background.c` contains canonical scalar density/pressure structure with positive kinetic density and pressure:
   - `rho_scf ~ +phi_prime^2/(2a^2)+V_scf`;
   - `p_scf ~ +phi_prime^2/(2a^2)-V_scf`.
5. The background scalar evolution/source uses the single `phi_scf`/potential family, not a two-field container.

### C. Full Boltzmann base is independently present

6. `include/perturbations.h` contains photon and polarization hierarchy indices plus ultra-relativistic hierarchy indices.
7. the repository contains the standard `thermodynamics` module and perturbation/output modules required for CMB/matter transfer generation.
8. the control run confirms the unmodified exact pin produces standard cosmological output.

### D. Frozen planned modification boundary

The audit must produce a manifest stating that the minimal independent quintom adapter is allowed to touch only the species/interface files needed to introduce a second direct scalar field and sum its stress-energy into Einstein sources. The planned file families are frozen as:

- `include/background.h`;
- `source/background.c`;
- `include/input.h` / `source/input.c` only as needed for parameters;
- `include/perturbations.h`;
- `source/perturbations.c`;
- `source/output.c` / Python exposure only if needed for regression outputs.

The following solver subsystems are **protected** and may not be modified in the first adapter implementation:

- photon hierarchy dynamics;
- polarization hierarchy dynamics;
- massless/massive neutrino hierarchy dynamics;
- thermodynamics/recombination equations;
- primordial module;
- nonlinear module.

A later patch that needs a protected-subsystem physics modification requires a new preregistration and cannot inherit K3D1 authorization.

## Frozen classification

If the exact pin builds/runs and all structural checks pass:

`M13B_K3D1_CLASS_ADAPTER_BASE_PASS_WITH_SCOPE`

This authorizes a separately preregistered K3D2 patch adding an independently defined phantom second scalar while preserving the protected Boltzmann/thermodynamics machinery.

If CLASS builds/runs but the source architecture contradicts the frozen single-scf/minimal-boundary assumptions:

`M13B_K3D1_CLASS_ADAPTER_BASE_NOT_ESTABLISHED`.

If exact-pin build/control execution fails:

`M13B_K3D1_CLASS_ADAPTER_BASE_IMPLEMENTATION_BLOCKED`.

All outcomes retain:

- `author_model_reproduced=false`;
- `author_normalization_map_claimed=false`;
- `K3_state_ceiling=PARTIAL`;
- `K4_promoted=false`;
- `K5_promoted=false`;
- `physical_falsification=false`.
