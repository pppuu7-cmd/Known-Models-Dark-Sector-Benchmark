# W04 / M19 — axionCAMB exact-zero value-trace diagnostic preregistration v0.1

Date: 2026-09-11

## Purpose

Diagnose the *second* exact-zero execution blocker exposed after the preregistered zero-bypass recovery v0.1. This is a diagnostic-only experiment. It does **not** authorize K1 or any later scientific gate.

## Frozen provider

- `dgrin1/axionCAMB`
- commit `891e779cc0bd422e49f97533e6c2fc761149737d`

## Prior evidence frozen before this diagnostic

1. Original exact-zero paths crash in `w_evolve` because `Omega_ax=0` drives `a_init=0` and logarithmic shooting variables to singular values.
2. Recovery v0.1 bypasses scalar shooting at `Omega_ax=0` and bypasses the unconditional RECFAST axion-density derivative spline.
3. Recovery v0.1 leaves the finite `f_ax=0.10` path executable, but both exact-zero parameterizations still terminate (`139` optimized, `2` with runtime checks).
4. The new checked trace reaches `Nu_rho` from `dtauda` during `InitThermo`; the invalid spline index implies a non-finite `a*nu_masses` at that point.
5. Source audit shows `CP%ainit` is not used by `GetTauStart`, and `CP%aeq` is only used in the axion-specific `GetTauStart` block guarded by `CP%Omegaax>0`. In modified RECFAST, `z_eq=aeq^-1-1` is computed but has no downstream use. Therefore this diagnostic does **not** change `ainit` or `aeq` further.

## Diagnostic intervention

Apply the already-frozen recovery-v0.1 patch, then add print-only trace markers at these points:

- after `taumin=GetTauStart(maxq)` in `cmbmain.f90`;
- immediately before and after `Recombination_Init(...)` in `modules.f90::inithermo`;
- immediately before the first `dtauda(a)` call in the `inithermo` integration loop;
- inside `equations_ppf.f90::dtauda`, immediately before each massive-neutrino `Nu_rho(a*nu_masses(nu_i),...)` call, but only for the exact-zero case and only for the first few calls / any non-finite argument.

No physical formula, branch condition, parameter, precision control, or solver tolerance may be changed beyond recovery v0.1.

## Frozen case

Use the same exact-zero `r0f` case produced by `verification/m19/axioncamb2_zero_probe.py`.

## Build

Use runtime checking:

`-O0 -g -fbacktrace -fcheck=all -ffree-line-length-none -fallow-argument-mismatch`

## Recorded values

At minimum persist:

- `CP%tau0`
- `qmax`, `maxq`, `taumin`
- `adotrad`
- `nu_masses(1)` before RECFAST, after RECFAST, and before failing `Nu_rho`
- `tauminn`, `a0`, `dtau`, `a`
- `a*nu_masses(1)`
- exit code and backtrace

## Decision rule

- If `taumin` is non-finite before RECFAST, classify `GETTAUSTART_NONFINITE` and localize upstream.
- If `nu_masses(1)` changes from finite to non-finite across `Recombination_Init`, classify `RECFAST_STATE_CORRUPTION` and audit RECFAST memory/state writes.
- If `a` is non-finite with finite `taumin`, `adotrad`, and `nu_masses`, classify `INITHERMO_SCALE_FACTOR_NONFINITE`.
- If all traced values are finite but `Nu_rho` still receives a non-finite argument, classify `TRACE_INCONSISTENT_REQUIRES_DEEPER_INSTRUMENTATION`.
- Otherwise report the first value that becomes non-finite and its source location.

## Scientific claim boundary

This diagnostic can only localize an implementation defect. It cannot falsify fuzzy/ultralight axion physics and cannot promote M19 beyond its current gates.
