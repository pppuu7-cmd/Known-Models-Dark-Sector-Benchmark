# W04 M26 PBH energy-injection provider control preregistration v0.1

Status: **FROZEN BEFORE EXECUTION**

## Scope

This control opens only the energy-injection children of F26 primordial-black-hole dark matter. It does **not** promote or reject F26 as a family and does not cover the discrete/Poisson gravitational-structure channel.

Following the W04 methodology addendum, response-distinct PBH mechanisms are kept separate. Three children are tested independently:

1. `evaporation` — Hawking-evaporation energy injection;
2. `spherical` — baryonic accretion using the provider's `spherical_accretion` prescription;
3. `disk` — baryonic accretion using the provider's `disk_accretion` prescription.

A pass in one child cannot represent another child.

## Immutable provider

Provider: `GFAbellan/ExoCLASS`

Pinned commit: `7c4b26e50d240f1f45f120b623aab2dba13094fd`

The pinned provider documents `PBH_fraction`, `PBH_evaporating_mass`, `PBH_accreting_mass`, and distinct spherical/disk accretion recipes. This is a historical/current executable provider control for these implemented prescriptions, not a claim that every later PBH-feedback correction is represented.

## Frozen common cosmology / execution profile

Use the provider's example energy-injection cosmology as the common anchor:

- `omega_b = 0.02218`
- `omega_cdm = 0.1205`
- `100*theta_s = 1.04069`
- `z_reio = 8.24`
- `ln10^{10}A_s = 3.056`
- `n_s = 0.9619`
- `on the spot = no`
- `energy_deposition_function = DarkAges`
- `DarkAges_mode = built_in`
- `energy_repartition_coefficient = no_factorization`
- `recombination = recfast`
- `reio_stars_and_dark_matter = yes`

For this provider/reference control only, compute unlensed `tCl,pCl,mPk`, background and thermodynamics with `l_max_scalars = 1200`, `P_k_max_h/Mpc = 5`, and `z_pk = 0`.

## Frozen child coordinates

For each child run three cases with all non-coordinate settings held fixed:

### evaporation
- baseline: omit all PBH keys;
- explicit zero: `PBH_fraction = 0`, `PBH_evaporating_mass = 1e15` g;
- finite control: `PBH_fraction = 1e-5`, `PBH_evaporating_mass = 1e15` g.

### spherical
- baseline: omit all PBH keys;
- explicit zero: `PBH_fraction = 0`, `PBH_accreting_mass = 1e3` Msun, `PBH_accretion_recipe = spherical_accretion`;
- finite control: same mass/recipe with `PBH_fraction = 1e-5`.

### disk
- baseline: omit all PBH keys;
- explicit zero: `PBH_fraction = 0`, `PBH_accreting_mass = 1e3` Msun, `PBH_accretion_recipe = disk_accretion`;
- finite control: same mass/recipe with `PBH_fraction = 1e-5`.

The explicit-zero case exists specifically to test the W04 parameter-presence rule; omitted-key and explicit-zero equivalence is measured, not assumed.

## Frozen diagnostics

For each child require executable provider/build status and valid numeric outputs for baseline, explicit-zero and finite cases.

Compare baseline vs explicit zero in:

- background table;
- thermodynamics table;
- CMB TT/EE/TE blocks from `cl.dat`;
- matter power spectrum from `pk.dat`.

Use support-aware symmetric normalized residuals. The reference-semantics identity control passes when every measured block has `p95_abs <= 1e-8`.

The finite case is only a sensitivity control. It must differ from baseline in at least one thermodynamics or CMB block above numerical floor (`max_abs > 1e-10`). No minimum physical effect size is imposed at this provider-control stage.

## Classification

Allowed per-child classifications:

- `M26_<CHILD>_PROVIDER_REFERENCE_CONTROL_PASS_WITH_SCOPE`
- `M26_<CHILD>_EXPLICIT_ZERO_IDENTITY_NOT_ESTABLISHED`
- `M26_<CHILD>_FINITE_RESPONSE_NOT_RESOLVED`
- `M26_<CHILD>_PROVIDER_EXECUTION_BLOCKED`

All classifications keep:

- `K1_promoted = false`
- `K4_promoted = false`
- `physical_falsification = false`

A scoped provider-control pass only authorizes a separately preregistered multi-point K1 continuity/scaling ladder for that child. It does not authorize family-level PBH claims.
