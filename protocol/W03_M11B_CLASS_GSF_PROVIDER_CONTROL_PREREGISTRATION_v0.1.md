# W03 / M11b — CLASS_GSF provider control preregistration v0.1

Status: **FROZEN BEFORE PROVIDER-CONTROL RUN**

## Purpose

M11b model-6 has now failed both the original probe and the prospectively frozen non-zero kinetic-seed recovery ladder. Before spending further degrees of freedom on model-6 initialization, test whether the pinned external provider itself reproduces its own committed working example in the same GitHub-hosted environment.

Pinned provider: `KunhaoZhong/CLASS_GSF@07e015246c4b40f4e22bb50c9a0a63a621bb61f7`.

This is an implementation/provenance control only. It cannot score k-essence B4–B8/K5–K9.

## Frozen controls

1. Clone the exact pinned commit.
2. Build the `class` binary using the provider Makefile.
3. Run the provider's committed `dgf.ini` **without changing its physical or numerical parameters**.
4. Require process exit code 0.
5. Require the declared DGF output files to be newly produced by the run, at minimum a background table and matter-power output (pre-existing committed `output/dgf_*` files must be removed before execution so they cannot satisfy the gate).
6. Preserve build/run logs and hashes/provenance in an immutable Actions artifact.

The committed provider example uses `model_gsf=1` (dilatonic ghost field through the first element of `gsf_parameters`), `Omega_gsf=-1`, `gsf_tuning_index=6`, `gsf_dxdy_guess=1`, `attractor_ic_gsf=no`, and a non-zero initial derivative encoded as `10 * 10^-18 = 10^-17`.

## Frozen interpretation

- `PROVIDER_CONTROL_PASS`: pinned source builds and the unmodified committed DGF example executes and produces fresh outputs.
- `PROVIDER_CONTROL_FAIL_BUILD`: exact source does not build.
- `PROVIDER_CONTROL_FAIL_EXAMPLE`: build succeeds but the exact committed DGF example does not execute/produce fresh required outputs.

If provider control PASSes while no author-supplied model-6 working example can be found, the current M11b model-6 branch remains `BLOCKED_IMPLEMENTATION/PROVENANCE`; provider-wide failure is rejected, but there is still no validated model-6 operating point.

If provider control FAILs, do not use this provider for scientific k-essence promotion until the provider/environment incompatibility is resolved.

No physical threshold or M11 effective-fluid conclusion changes under any provider-control outcome.
