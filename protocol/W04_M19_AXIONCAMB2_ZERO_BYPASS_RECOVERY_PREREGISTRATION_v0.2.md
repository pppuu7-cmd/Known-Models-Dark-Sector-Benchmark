# W04 / M19 — axionCAMB exact-zero bypass recovery preregistration v0.2

Date: 2026-09-11

## Purpose

Recover the mathematically exact `Omega_ax=0` implementation path in pinned axionCAMB without changing finite-axion physics. This supersedes recovery v0.1 only for the exact-zero implementation patch; v0.1 remains immutable evidence.

This test is implementation recovery only. A PASS does **not** promote K1/B1; a separate historical pure-CAMB reference comparator remains mandatory.

## Frozen provider

- `dgrin1/axionCAMB`
- commit `891e779cc0bd422e49f97533e6c2fc761149737d`

## Evidence motivating v0.2

Recovery-v0.1 value tracing established:

- `nu_masses(1)=332.50423927255861` is finite;
- `adotrad=2.1558083228285127e-6` is finite;
- `GetTauStart` returns finite `taumin=2.9713266973702092e-4`;
- `CP%tau0` is already `NaN` before RECFAST;
- `InitThermo` therefore receives `taumax=NaN`, after which its logarithmic time grid makes `dtau` and `a` non-finite.

Pinned source shows why `CP%tau0=TimeOfz(0)` becomes non-finite: in `equations_ppf.f90::dtauda`, the zero-axion case reaches

`dorp = grhom * CP%drefp_hsq * (CP%a_osc/a)^3`

with `drefp_hsq=0`, `a_osc=0`, and the integration endpoint `a=0`, generating `0*(0/0)` instead of the exact physical zero.

Source audit also shows that `Params%omegar` is assigned inside `w_evolve` as

`Params%omegar = Params%omegah2_rad / hsq`, `hsq=(H0/100)^2`.

Because the exact-zero bypass legitimately skips `w_evolve`, v0.2 must reproduce this non-axion bookkeeping assignment from the already-computed `P%omegah2_rad`; otherwise RECFAST and any downstream code may receive an uninitialized `omegar` even after the `tau0` singularity is removed.

`aeq=0` is not treated as the cause of the v0.1 failure: `GetTauStart` reads `aeq` only under `Omegaax>0`, and RECFAST computes `z_eq=aeq^-1-1` but does not subsequently use `z_eq` in the pinned file.

## Frozen patch scope

Only the following exact-zero changes are authorized:

1. `inidriver_axion.F90`:
   - if `P%omegaax == 0`, skip `w_evolve`;
   - set `P%a_osc=0`, `P%drefp_hsq=0`, `P%phiinit=0`, `P%ainit=0`, `P%aeq=0`;
   - set `P%omegar = P%omegah2_rad / (P%H0/100)^2`;
   - set `badflag=0`.
2. `recfast_axion.f90`:
   - in the previously unconditional finite-difference axion-density derivative block, if `OmegaAx==0`, set the axion derivative contribution `dorpa=0` and do not read axion spline tables.
3. `equations_ppf.f90`:
   - for **both** source occurrences of the late-time axion-density expression `grhom*CP%drefp_hsq*(CP%a_osc/a)^3`, if `CP%omegaax==0`, set `dorp=0` before any division by `a`;
   - otherwise execute the original expression unchanged.

No finite-axion formula, tolerance, precision setting, initial condition, or output normalization may change.

## Frozen cases

Use the same cases as prior independent zero probe:

- `r0f`: exact zero via axion fraction interface;
- `r0d`: exact zero via direct axion-density interface;
- `p1`: finite control `f_ax=0.10`.

Run `p1` in both original and patched trees.

## Builds

- optimized original and patched: existing provider build flags used by prior probe;
- checked patched zero: `-O0 -g -fbacktrace -fcheck=all -ffree-line-length-none -fallow-argument-mismatch`.

## Frozen gates

A recovery PASS requires all of:

1. original and patched builds exit 0;
2. patched `r0f` and `r0d` exit 0;
3. patched debug `r0f` exits 0 under runtime checks;
4. patched `p1` and original `p1` exit 0;
5. CMB, matter-power and transfer outputs exist and are fully finite for all executable cases;
6. exact-zero parameterization identity: patched `r0f` vs `r0d` has normalized `D_inf <= 1e-12` for each output product;
7. finite non-interference: patched `p1` vs original `p1` has normalized `D_inf <= 1e-12` for each output product.

## Classifications

- all gates pass -> `M19_AXIONCAMB2_ZERO_BYPASS_RECOVERY_V2_PASS_WITH_SCOPE`
- finite control changes -> `M19_ZERO_BYPASS_V2_REJECTED_FINITE_PATH_CHANGED`
- zero still fails -> `M19_ZERO_BYPASS_V2_EXECUTION_BLOCKED`
- zero parameterizations disagree -> `M19_ZERO_BYPASS_V2_IDENTITY_BLOCKED`
- debug-only failure -> `M19_ZERO_BYPASS_V2_RUNTIME_CHECK_BLOCKED`

## Claim boundary

Even `PASS_WITH_SCOPE` means only that the pinned implementation now has a source-audited exact-zero branch while preserving the finite branch under the frozen regression. K1/B1 remains unpromoted until the recovered zero outputs are compared to an independently pinned historical pure-CAMB CDM reference.
