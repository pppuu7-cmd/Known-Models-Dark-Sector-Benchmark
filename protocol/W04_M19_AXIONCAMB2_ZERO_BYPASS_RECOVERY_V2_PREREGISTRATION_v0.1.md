# W04 M19 axionCAMB2 exact-zero recovery v2 preregistration v0.1

## Purpose
Recover the exact `Omega_ax=0` reference limit of pinned `dgrin1/axionCAMB@891e779cc0bd422e49f97533e6c2fc761149737d` without changing any finite-axion physics.

The first recovery attempt is canonically classified `M19_ZERO_BYPASS_RECOVERY_EXECUTION_BLOCKED`. Its debug trace showed that bypassing `w_evolve` at the driver level also bypassed `Nu_init` and the construction of global `Nu_masses`, causing a later `dtauda -> Nu_rho` failure during thermodynamics. Recovery v2 therefore MUST preserve the generic initialization prefix of `w_evolve` and may only return after that prefix is complete.

## Frozen source diagnosis
At the provider pin, `w_evolve` performs, before the axion scalar-field integration:

1. cosmological-density conversions;
2. `call Nu_init`;
3. photon/massless-neutrino background construction;
4. construction of `Nu_masses` and massive-neutrino Hubble contributions.

Those operations are shared background initialization and are required even when `Omega_ax=0`.

## Allowed patch scope
Recovery v2 may change only:

1. `axion_background.f90`: add an exact-zero early return **after** the `Nu_masses` loop and before the scalar-field/integrator setup. For `Params%omegaax == 0`, the branch may assign only neutral axion state plus already-defined shared background scalars:
   - `Params%a_osc = 0`
   - `Params%drefp_hsq = 0`
   - `Params%phiinit = 0`
   - `Params%axfrac = 0`
   - `Params%omegar = Params%omegah2_rad/hsq`
   - `Params%aeq = (Params%omegah2_rad + sum(lhsqcont_massive))/(omegah2_b+omegah2_dm)`
   - `badflag = 0`
   - `return`

   No finite-axion statement may be altered.

2. `recfast_axion.f90`: for `OmegaAx == 0`, the auxiliary finite-difference derivative of axion density used only in the matter-temperature correction must be exactly zero and MUST NOT read axion spline tables. The primary Hubble rate remains the provider's own `dtauda`, whose `a_osc=0,drefp_hsq=0` branch contributes zero axion density.

No other provider source file may be patched.

## Frozen cases
Use the same generated cases as the earlier independent probe/recovery:

- `r0f`: exact zero through the axion-fraction interface;
- `r0d`: exact zero through the direct axion-density interface;
- `p1`: finite control, `f_ax=0.10`.

## Frozen gates
All are mandatory for a scoped recovery PASS:

- optimized original build exit 0;
- optimized v2-patched build exit 0;
- debug v2-patched build with `-O0 -g -fbacktrace -fcheck=all` exit 0;
- patched `r0f` and `r0d` exit 0 and produce finite CMB, matter-power and transfer products;
- exact-zero parameterization identity: normalized `D_inf <= 1e-12` for every retained product;
- finite non-interference: patched `p1` versus original `p1` normalized `D_inf <= 1e-12` for every retained product;
- debug exact-zero case exits 0.

## Interpretation
PASS may be called only `M19_AXIONCAMB2_ZERO_BYPASS_RECOVERY_V2_PASS_WITH_SCOPE`.

A recovery PASS is provider-engineering evidence only. It does **not** by itself promote K1. K1 still requires the separately preregistered historical pure-CAMB CDM comparator.

Any failure remains a provider/reference-limit blocker and is not physical falsification of fuzzy/ultralight-axion dark matter.
