# W04 / M19 axionCAMB2 exact-zero bypass recovery preregistration v0.1

Frozen: 2026-09-10
Provider: `dgrin1/axionCAMB@891e779cc0bd422e49f97533e6c2fc761149737d`
Status before execution: `PREREGISTERED_NOT_RUN`
Scientific gate promotion: **NONE**. This is provider recovery only; K1 remains blocked pending an independent pure-CDM reference comparison.

## Frozen patch scope

Only exact `Omega_ax=0` behavior may change.

1. In `inidriver_axion.F90`, replace the unconditional `w_evolve(P,badflag)` call with an exact-zero branch. For `P%omegaax == 0._dl`, do not call `w_evolve`; set only:
   - `P%a_osc=0._dl`
   - `P%drefp_hsq=0._dl`
   - `P%phiinit=0._dl`
   - `P%ainit=0._dl`
   - `P%aeq=0._dl`
   - `badflag=0`
   For `P%omegaax /= 0`, execute the original `w_evolve(P,badflag)` call unchanged.

2. In `recfast_axion.f90`, in the matter-temperature `dH/dz` axion-density finite-difference block, if `OmegaAx == 0._dl`, set the axion density-derivative contribution `dorpa=0._dl` and do not call the axion density spline. For finite `OmegaAx`, retain the original finite-difference/spline expressions unchanged.

No epsilon floor, no altered axion mass, no changes to finite-axion equations, accuracy settings, perturbation equations, recombination coefficients, neutrino physics or output normalization are permitted.

## Frozen cases

Use the same generator/cosmological settings as `verification/m19/axioncamb2_zero_probe.py`:

- `Z-F`: `use_axfrac=T`, `omdah2=0.1200`, `axfrac=0`, `m_ax=1e-27 eV`.
- `Z-D`: `use_axfrac=F`, `omch2=0.1200`, `omaxh2=0`, `m_ax=1e-27 eV`.
- `P-PATCH`: patched provider, `use_axfrac=T`, `omdah2=0.1200`, `axfrac=0.10`, `m_ax=1e-27 eV`.
- `P-ORIG`: unpatched provider, identical finite parameters to `P-PATCH`.

Required outputs for every successful case:
- scalar CMB file;
- linear matter-power file;
- transfer file;
- all parsed numeric entries finite.

## Frozen recovery metrics

For each common numeric output array A,B define

`D_inf = max(abs(A-B))/max(1e-30,max(abs(A)),max(abs(B)))`.

A comparison passes only if shapes match and `D_inf <= 1e-12`.

Required passes:

- `Z-F` exit 0 and output contract PASS;
- `Z-D` exit 0 and output contract PASS;
- `Z-F` vs `Z-D`: all three required outputs `D_inf<=1e-12`;
- `P-PATCH` vs `P-ORIG`: all three required outputs `D_inf<=1e-12`.

The finite non-interference condition is mandatory: a recovery that changes the finite axion control is rejected even if zero cases execute.

## Diagnostic runtime-check case

Also compile the patched provider serially with `-O0 -g -fbacktrace -fcheck=all -ffree-line-length-none -fallow-argument-mismatch` and execute `Z-F`. It must exit 0. Its numerical outputs are not compared against optimized outputs because compiler/optimization settings differ; the diagnostic requirement is execution without runtime bounds/uninitialized-state failure.

## Classification

- All required optimized execution/output/identity/non-interference checks + diagnostic exit 0: `M19_AXIONCAMB2_ZERO_BYPASS_RECOVERY_PASS_WITH_SCOPE`.
- Patch changes finite control: `M19_ZERO_BYPASS_REJECTED_FINITE_PATH_CHANGED`.
- Zero cases still fail: `M19_ZERO_BYPASS_RECOVERY_EXECUTION_BLOCKED`.
- Zero parameterizations disagree above tolerance: `M19_ZERO_BYPASS_RECOVERY_IDENTITY_BLOCKED`.
- Otherwise: `M19_ZERO_BYPASS_RECOVERY_OUTPUT_BLOCKED`.

No classification here is a physical falsification and no PASS here promotes K1. The next gate after a recovery PASS is a separately preregistered comparison to a pinned pure-CDM CAMB reference, preferably from the same historical solver generation.
