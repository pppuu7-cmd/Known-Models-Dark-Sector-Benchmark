# M19 axionCAMB2 exact-zero bypass downstream audit

Date: 2026-09-10
Provider authority: `dgrin1/axionCAMB@891e779cc0bd422e49f97533e6c2fc761149737d`
Status: `ZERO_BYPASS_PATCH_SCOPE_DEFINED`
Scientific promotion: none

## Purpose

Define the smallest exact-`Omega_ax=0` recovery patch that avoids the inherited scalar-shooting singularity without changing any finite-axion equations.

## Producer failure already localized

`inidriver_axion.F90` calls `w_evolve(P,badflag)` unconditionally. In `w_evolve`, exact `omegah2_ax=0` gives `as_scalar=0`, then `a_init=0`, `log(a_init)=-Inf`; a second independent singularity arises from logarithms of zero scalar shooting guesses at `fax=0`. The debug build resolves the eventual failure to `MassiveNu::Nu_rho` with an invalid minimum-integer spline index.

Therefore the exact zero point must bypass scalar-field shooting rather than be repaired by epsilon density or by clamping one logarithm.

## Downstream state/use audit

Exact-symbol searches at the pinned provider identify the following consumers of the axion lookup state.

### `equations_ppf.f90`

The background `dtauda(a)` reads `CP%loga_table/CP%grhoax_table` only under `if (a .lt. CP%a_osc)`. Otherwise it uses

`dorp = grhom * CP%drefp_hsq * ((CP%a_osc/a)**3)`.

Thus setting exact-zero state `CP%a_osc=0` and `CP%drefp_hsq=0` makes the axion background contribution identically zero for every physical `a>0` without reading a lookup table.

The perturbation-side EOS/sound-speed table reads found by exact-symbol search are likewise inside `a < a_osc` branches. With `a_osc=0`, these branches are not entered for physical scale factors. Axion isocurvature is frozen off in the recovery cases.

### `cmbmain.f90` / `cmbmainOMP.f90`

The axion-specific start-time/equality construction is explicitly guarded by `if(CP%Omegaax>0)`. Exact zero therefore bypasses that block.

### `modules.f90`

`Recombination_Init` is called with `CP%omegaax`, `CP%a_osc`, `CP%drefp_hsq`, and the fixed-size axion lookup arrays. Passing the arrays is harmless by itself; they must simply not be dereferenced at exact zero.

### `recfast_axion.f90`

The ordinary recombination Hubble rate is computed through `dtauda(1/(1+z))`, which is safe under the zero state above.

However, the matter-temperature derivative contains an additional axion-density finite-difference calculation. At the offset point it calls

`call spline_out(loga_table,grhoax_table,grhoax_table_buff,ntable,dlog10(sfac+deriv_eps),gr)`

*before* testing whether `(sfac+deriv_eps) < aosc`. This is an unguarded lookup-table read and makes `skip w_evolve` alone unsafe.

For exact `OmegaAx=0`, the mathematically correct axion contribution and its scale-factor derivative are both exactly zero. The minimal safe repair is therefore to bypass the axion finite-difference spline block and set its derivative contribution `dorpa=0` when `OmegaAx==0`, while preserving the existing finite-axion block byte-for-byte/semantically unchanged.

## Neutral zero state

The recovery patch may initialize only the scalar-specific state needed to prevent downstream accidental use:

- `P%a_osc = 0`
- `P%drefp_hsq = 0`
- `P%phiinit = 0`
- `P%ainit = 0`
- `P%aeq = 0` as an inert axion-specific placeholder; axion-specific equality uses are guarded by `Omegaax>0` or isocurvature, which is off in this recovery.
- `badflag = 0`

No logarithmic axion-density lookup table is synthesized because exact zero has no finite logarithm.

## Required recovery tests

1. patched exact-zero fraction interface executes;
2. patched exact-zero density interface executes;
3. both zero parameterizations agree numerically on CMB, linear matter power and transfer outputs;
4. a finite `axfrac=0.10` control from the patched provider agrees with the unpatched provider, demonstrating no finite-axion physics change;
5. production build and a runtime-check build do not access invalid axion state at exact zero.

This recovery is provider-infrastructure evidence only. It does not by itself promote K1. Independent pure-CDM comparison remains required before an exact reference-limit claim.
