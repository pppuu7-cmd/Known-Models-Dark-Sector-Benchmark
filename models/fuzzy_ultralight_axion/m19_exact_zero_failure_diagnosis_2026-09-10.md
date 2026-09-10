# M19 exact-zero axionCAMB-family failure diagnosis

Date: 2026-09-10
Status: `PROVIDER_ZERO_LIMIT_IMPLEMENTATION_DEFECT_LOCALIZED`
Scientific promotion: none
Physical falsification: false

## Reproduced behavior

Two independently pinned public implementations from the same axionCAMB lineage were exercised at an exact zero axion density/fraction and at a finite axion control.

- `Ra-yne/AxiECAMB@b7ca9ba80aca178da5003d864b8e20cb5905555b`: finite `axfrac=0.10` control executes with finite CMB, linear matter and transfer products; both exact-zero interfaces terminate with exit 139.
- `dgrin1/axionCAMB@891e779cc0bd422e49f97533e6c2fc761149737d`: after correcting the KMDSB output-root capture harness, finite `axfrac=0.10` executes with 4999 finite scalar-CMB rows, 554 finite matter-power rows and 192 finite transfer rows; both exact-zero interfaces terminate with exit 139.

Thus the failure is not evidence that finite ULA/FDM evolution is unavailable. It is localized to the exact zero-reference route.

## Debug localization

A diagnostic-only build of `dgrin1/axionCAMB@891e779...` with

`-O0 -g -fbacktrace -fcheck=all`

converts the raw segmentation fault into the line-resolved runtime error:

`modules.f90:1663` in `MassiveNu::Nu_rho`: array index `-2147483648` for spline table `r1`.

Backtrace:

`Nu_rho -> axion_background::lh (line 1107) -> derivs -> next_step -> w_evolve -> driver`.

## Root cause in the zero-density background initialization

Inside `w_evolve`, the starting scale factor includes

`as_scalar=(omegah2_ax/(maxion_twiddle**2))**(1/3)`

and then

`a_init=min(a_rel,a_lambda,a_m,as_matt,as_rad,as_scalar)*1e-7`.

At exact `omegah2_ax=0`, `as_scalar=0`, hence `a_init=0` and `log_a_init=log(0)=-Inf`. The subsequent logarithmic grid/RK construction therefore produces non-finite intermediate values. These reach `Nu_rho(a*nu_masses(i),...)`; comparisons with NaN fail, its spline index is formed from `int(log(am/am_min)/dlnam+1)`, and gfortran yields the observed minimum-integer index.

There is a second independent zero-density singularity in the same shooting path: the analytic scalar initial-condition guesses are proportional to `fax`; at `fax=0`, their min/max are zero and the code later takes logarithms of zero while constructing the shooting grid. Therefore clamping only `a_init` would not constitute a complete or scientifically acceptable repair.

## Interpretation

The exact `Omega_ax=0` point should not require scalar-field shooting at all. The technically appropriate recovery target is a true zero-axion bypass that omits `w_evolve` and supplies whatever inert/empty axion state downstream code requires, while leaving all finite-axion equations unchanged.

Before implementing such a patch, every downstream use of axion background tables/state must be audited for an `Omega_ax>0` guard or an explicit zero-state requirement. The recovery patch must then be verified against an independent CDM reference and against an unchanged finite-axion control.

An epsilon-axion substitution is not authorized as an exact K1 reference and the crash is not a physical failure of fuzzy/ultralight axion dark matter.
