# W03 M13b K3D1 CLASS control-output recovery v0.1

Date frozen: 2026-09-13
Parent: `protocol/W03_M13B_K3D1_CLASS_ADAPTER_BASE_STRUCTURAL_AUDIT_v0.1.md`
Provider: `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`

## Trigger

K3D1 run `34782356655` proved that the exact provider pin builds successfully. The next step failed after invoking the frozen LambdaCDM control. The uploaded artifact contains the unchanged INI and empty solver stdout/stderr, but no expected `control/k3d1_pk.dat`. Because the shell block used `set -e`, the run did not record the CLASS return code and cannot distinguish a provider nonzero exit from a successful solver followed by a harness output-path assertion failure.

This recovery is infrastructure-only.

## Frozen science and input

The exact provider commit and all LambdaCDM control parameters remain byte-for-byte identical to K3D1:

- h=0.67
- omega_b=0.0224
- omega_cdm=0.12
- A_s=2.1e-9
- n_s=0.965
- tau_reio=0.054
- output=mPk
- P_k_max_1/Mpc=1.0
- z_pk=0
- identical absolute root string ending `control/k3d1_`.

No CLASS source, precision, cosmological parameter, output request or structural criterion may change.

## Allowed recovery actions

1. run CLASS under `set +e` and persist its exact numeric return code;
2. persist stdout/stderr without interpreting empty streams;
3. recursively list files created under `control/` and provider `output/` after execution;
4. if provider rc=0, identify any nonempty file whose name/path is a deterministic CLASS matter-power output for the frozen root/request;
5. parse the located P(k) file only for finite numeric rows;
6. if provider rc=0 and a finite P(k) exists at a path different from the original harness assertion, classify the first run as `HARNESS_OUTPUT_PATH_ONLY` and continue the unchanged source-structure audit using the discovered deterministic path rule;
7. if provider rc is nonzero, classify K3D1 control as `PROVIDER_CONTROL_EXECUTION_BLOCKED` and do not continue to K3D2;
8. if provider rc=0 but no finite requested P(k) exists anywhere in the allowed output roots, classify `CONTROL_OUTPUT_NOT_ESTABLISHED`.

No scientific pass is inferred from a green workflow alone.
