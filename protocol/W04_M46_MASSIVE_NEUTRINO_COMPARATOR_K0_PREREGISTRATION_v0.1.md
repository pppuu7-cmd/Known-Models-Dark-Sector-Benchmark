# W04 M46 massive-neutrino / hot-DM comparator K0 preregistration v0.1

Date: 2026-09-11
Benchmark: M46 external known-sector comparator
Provider: `lesgourg/class_public` pinned at `e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Purpose

Establish a pinned, executable known-sector massive-neutrino comparator for later subtraction/nearest-family audits. This is K0 provenance/executability only; it is not a neutrino-mass constraint and does not promote K1-K9.

The pinned CLASS documentation explicitly supports `N_ncdm`, `m_ncdm`, and the standard active-neutrino temperature prescription; for one 0.06 eV massive neutrino with the default non-thermal temperature correction it recommends `N_ur=2.0308` to keep the standard effective radiation content.

## Frozen arms

Shared cosmology:

- `h=0.675`
- `omega_b=0.0222`
- `omega_cdm=0.1197`
- `A_s=2.196e-9`
- `n_s=0.9655`
- `tau_reio=0.06`
- `output=tCl,pCl,mPk`
- `lensing=no`
- `non linear=none`
- `P_k_max_h/Mpc=10`
- `z_pk=0`
- `l_max_scalars=2500`
- synchronous gauge.

1. `massless_control`: `N_ncdm=0`, `N_ur=3.044`.
2. `massive_nu_006`: `N_ncdm=1`, `m_ncdm=0.06 eV`, default provider `T_ncdm=0.71611`, `N_ur=2.0308`.

The comparator point is a provider-native standard calibration point, not an observational inference.

## Frozen K0 checks

Require both arms to execute at the exact provider pin with exit code 0 and finite non-empty TT and P(k) outputs. The massive-neutrino arm must also differ actively from the massless control with normalized-L2 difference > `1e-6` in at least one of TT or P(k), solely as a negative control against inert/misparsed ncdm inputs.

## Frozen classification

- all checks pass: `M46_K0_PASS_WITH_SCOPE_PINNED_CLASS_MASSIVE_NEUTRINO_COMPARATOR`;
- execution/finite-output/pin failure: `M46_K0_BLOCKED_IMPLEMENTATION_OR_PROVIDER_EXECUTION`;
- executable but inactive under the frozen negative control: `M46_K0_NOT_ESTABLISHED_ACTIVE_COMPARATOR_RESPONSE`.

`physical_falsification=false` in all cases. K1-K9 remain open.
