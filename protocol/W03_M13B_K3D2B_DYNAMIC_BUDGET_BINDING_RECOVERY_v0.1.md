# W03 M13b K3D2-B dynamic-budget binding recovery v0.1

Frozen: 2026-09-14, after enabled run 34784490777 failed inside `input_read_parameters_species` and before any qcf/qpf background or perturbation integration occurred.

Parent: `protocol/W03_M13B_K3D2B_ENABLED_TWO_FIELD_COSMOLOGY_REGRESSION_v0.1.md`.
Provider: `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.

## Observed infrastructure failure

The first enabled qcf+qpf run stopped before background integration with the upstream CLASS rule that one of `Omega_Lambda` or `Omega_fld` must be left unspecified when `Omega_scf>=0`.

That upstream rule assumes all closure-carrying dark-energy species are represented by `{Lambda,fld,scf}`. K3D2 adds independent direct fields `qcf+qpf`; their density is dynamical and is not represented by an input `Omega0_*` budget scalar. Omitting `Omega_Lambda` would therefore make upstream CLASS fill the missing budget with a spurious cosmological constant and is explicitly forbidden as a recovery.

The K3D2-A patch also read the qcf/qpf input parameters only after `input_read_parameters_species`, so the budget parser could not know that the independent dynamic closure was active.

No enabled qcf/qpf ODE state was integrated in run 34784490777. No K3D2-B numerical/science gate was evaluated.

## Frozen recovery

1. Move the existing qcf/qpf input reads to `input_read_parameters` immediately after the general-parameter read and before `input_read_parameters_species`.
2. Do not change defaults, potential, U0, field starts, velocity starts, cosmology, or any K3D2-B threshold.
3. In the single upstream budget-consistency guard, allow all three `Omega_Lambda`, `Omega_fld`, and nonnegative `Omega_scf` values to be explicitly specified only when `qcf_U0 != 0` or `qpf_U0 != 0`.
4. With the frozen K3D2-B input, keep `Omega_Lambda=Omega_fld=Omega_scf=0`. Do not invoke upstream Lambda/fluid/scf budget filling.
5. Do not add an inferred/fitted Omega for qcf or qpf. Their energy densities remain determined solely by the already frozen direct-field state and `V_class=3 H0^2 U` map.
6. When qcf=qpf are absent (`U0=0`), the upstream budget condition must remain logically identical to the exact-pin CLASS condition.
7. No background, perturbation, Einstein, photon, neutrino, thermodynamics, primordial, transfer, harmonic, lensing, or nonlinear evolution equation may change in this recovery.

## Required recovery audit

Before interpreting an enabled result, source audit must establish:

- qcf/qpf reads occur before `input_read_parameters_species`;
- the old late duplicate qcf/qpf read block is absent;
- the budget exemption is conditioned only on nonzero qcf/qpf U0;
- exact standard CLASS behavior is retained when qcf_U0=qpf_U0=0;
- frozen K3D2-B cosmological inputs still contain explicit zeros for Lambda/fld/scf.

Classification of run 34784490777 remains `INPUT_BUDGET_BINDING_INFRASTRUCTURE_ONLY_NO_ENABLED_DYNAMICS` and is not a physical/model result.
