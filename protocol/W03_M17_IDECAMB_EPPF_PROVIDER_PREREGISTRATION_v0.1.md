# W03 M17 IDECAMB ePPF provider preregistration v0.1

Date: 2026-09-10
Family: F17 / M17 original future-event-horizon holographic dark energy (OHDE/HDE)
Purpose: establish whether a pinned public Boltzmann implementation supplies an executable, explicit perturbation prescription for the original HDE background family.

## Frozen provider

- Base: `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`
- Overlay: `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`
- Build recovery already admitted elsewhere in KMDSB: compiler-compatibility flag `-fallow-argument-mismatch`; no physics-source edits.

This exact provider is independently cited by Li et al., *Revisiting holographic dark energy after DESI 2024*, Eur. Phys. J. C 85, 608 (2025), DOI `10.1140/epjc/s10052-025-14279-7`, as the modified CAMB implementation used while applying the ePPF prescription to HDE/IHDE perturbations.

## Frozen source binding

The provider source must satisfy all of the following before execution can promote the candidate:

1. `Class_IDE=1` selects the coupled-fluid machinery.
2. `WForm_CF=2` selects HDE, with native parameter `c_hde` mapped to the HDE `c` coordinate.
3. The HDE equation of state is the original event-horizon relation
   `w_de = -1/3 - 2 sqrt(Omega_de)/(3 c)` in equivalent solver variables.
4. `beta_cf=0` is frozen so M17 is noninteracting HDE rather than IHDE.
5. `Use_PPF=T` is explicit, not inherited silently from a default.
6. The perturbation system actually evolves the PPF/ePPF dark-energy state and feeds the resulting dark-energy density/momentum perturbations back into the Einstein-Boltzmann source equations.

## Scope restriction

Passing this gate establishes only an **effective ePPF perturbation completion of OHDE**. It does not prove that perturbing the nonlocal future-event-horizon definition uniquely yields this closure, and it does not make ePPF part of the original Li-2004 model definition. Therefore any K3 promotion must be labelled `PASS_WITH_SCOPE_EPPF_PRESCRIPTION`.

A background-only effective `w(a)` substitution remains inadmissible as perturbation evidence.

## Frozen execution cases

Likelihoods are disabled; the existing IDECAMB `action=4` theory-output route is used. All cases use `Class_IDE=1`, `WForm_CF=2`, `beta_cf=0`, `Use_PPF=T`.

Finite HDE points:

- `c=0.6`
- `c=0.8`
- `c=1.0`
- `c=1.2`

These are finite/global response points because M17 has no native LambdaCDM reference intersection in the `c` coordinate. No local derivative at LambdaCDM is authorized.

A second identical `c=0.8` execution is included as a same-input determinism control.

## Frozen provider-control gates

A provider-control PASS requires:

- exact pinned commits verified;
- build exit code 0;
- every frozen HDE case exit code 0;
- nonempty numeric `.quantity` and `.theory_cl` outputs for every case;
- all parsed numeric entries finite;
- repeated `c=0.8` outputs have max symmetric relative difference <= `2e-10` on matched numeric arrays.

The repeat threshold is a provider determinism/reproducibility control, not the full K4 precision/convergence gate.

## Allowed classifications

- `M17_IDECAMB_EPPF_PROVIDER_EXECUTABLE_WITH_SCOPE`
- `M17_IDECAMB_EPPF_BLOCKED_BUILD`
- `M17_IDECAMB_EPPF_BLOCKED_EXECUTION`
- `M17_IDECAMB_EPPF_BLOCKED_OUTPUT_SCHEMA`
- `M17_IDECAMB_EPPF_REPEAT_NONDETERMINISM`

No outcome in this provider gate is a physical falsification of HDE.

## Promotion rule

If the source-binding audit is satisfied and the provider-control passes, M17 K3 may move from untested to `PASS_WITH_SCOPE_EPPF_PRESCRIPTION`. K4 remains open except for the narrow repeatability control. K5/K7 and any observation-space novelty claim remain open. The already completed finite-background CPL attack remains a separate result and must not be overwritten.
