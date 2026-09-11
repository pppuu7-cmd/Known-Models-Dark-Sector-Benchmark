# W04 M26 PBH provider runtime recovery preregistration v0.1

Status: **FROZEN BEFORE RUNTIME-RECOVERY EXECUTION**

## Trigger

The executable-only build recovery removed the shared ExoCLASS build blocker, but the three PBH energy-injection children remained provider-blocked for two runtime reasons:

1. ExoCLASS explicitly rejects `PBH_fraction = 0` together with a positive PBH mass. Therefore the original fixed-mass explicit-zero case is outside the provider input contract.
2. A finite PBH case invoking DarkAges failed while loading generated transfer-function dump objects. DarkAges stores mutable serialized transfer caches under the provider tree, so separate CLASS processes using one checkout cannot be treated as independent with respect to this cache.

Neither observation is a physical falsification.

## Frozen provider-null repair

The omitted-key baseline is unchanged.

Replace only the invalid explicit-zero representation by the provider-valid full null tuple:

- evaporation: `PBH_fraction = 0`, `PBH_evaporating_mass = 0`;
- spherical/disk accretion: `PBH_fraction = 0`, `PBH_accreting_mass = 0`, with no accretion recipe key in the null case.

The finite controls remain exactly as in the original preregistration:

- evaporation: fraction `1e-5`, mass `1e15 g`;
- spherical: fraction `1e-5`, mass `1e3 Msun`, spherical recipe;
- disk: fraction `1e-5`, mass `1e3 Msun`, disk recipe.

The full-null identity test is a provider semantics control only. It does not establish a fixed-positive-mass limit at fraction exactly zero. A later K1 test must approach zero from positive fractions and extrapolate/scale; it must not request an input point forbidden by the provider.

## Frozen DarkAges cache repair

Use the same pinned provider commit and the executable-only `class` build target from the build recovery.

Before each CLASS case, remove only generated DarkAges dump files matching:

- `DarkAgesModule/transfer_functions/transfer_Ch*.obj`
- `DarkAgesModule/transfer_functions/transfer_Corr.obj`

Do not delete or modify the immutable `transfer_functions/original/` tables.

Run baseline, null, and finite sequentially inside each child checkout because the DarkAges dump directory is shared mutable state. The three PBH children remain independent and should run in parallel as separate matrix jobs.

No on-the-spot approximation is introduced; retain `on the spot = no`, `energy_deposition_function = DarkAges`, `DarkAges_mode = built_in`, and all original cosmological/output settings.

## Frozen analysis and classification

Use the same sorted-support residual analysis and thresholds from `W04_M26_PBH_ENERGY_INJECTION_PROVIDER_CONTROL_PREREGISTRATION_v0.1.md`:

- baseline vs provider-valid full null: p95 <= 1e-8 in all measured blocks;
- finite response must exceed the frozen numerical floor in at least one thermodynamics/CMB block.

Allowed per-child classifications remain the original provider-control classes, with runtime-recovery provenance added. All outcomes retain:

- `K1_promoted = false`;
- `K4_promoted = false`;
- `physical_falsification = false`.

A scoped pass only establishes provider operability/null semantics for that PBH child and authorizes a later positive-fraction K1 ladder.
