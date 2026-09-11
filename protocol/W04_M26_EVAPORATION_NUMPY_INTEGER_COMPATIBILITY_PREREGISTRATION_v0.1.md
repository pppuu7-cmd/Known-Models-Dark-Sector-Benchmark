# W04 M26 evaporation NumPy integer-compatibility preregistration v0.1

## Trigger

After pinning a SciPy version compatible with historical DarkAges, the M26 spherical and disk PBH finite controls execute and pass their scoped provider-control gates. The evaporation branch alone fails before the physical response is produced because pinned `DarkAges/evaporator.py` calls `np.linspace(..., 1e5)`. Modern NumPy requires the `num` argument to be integer-valued and raises `TypeError: 'float' object cannot be interpreted as an integer`.

## Frozen intervention

Keep the pinned ExoCLASS commit `7c4b26e50d240f1f45f120b623aab2dba13094fd`, NumPy `2.2.6`, SciPy `1.13.1`, and the previously preregistered cacheless transfer-object intervention.

For the evaporation branch only, replace exactly the `np.linspace` sample-count literal `1e5` in `PBH_mass_at_z` by `100000`. This preserves the exact intended number of time-grid samples and changes no grid endpoint, PBH parameter, ODE equation, cosmology, transfer function, or scientific threshold.

Reuse successful baseline and exact-null controls from run `34550083757`; recompute only evaporation finite.

## Decision rule

Successful finite execution is analyzed with the unchanged M26 provider-control analyzer. Failure remains provider/infrastructure blocked. This compatibility repair cannot itself promote K1/K4 or constitute physical falsification.
