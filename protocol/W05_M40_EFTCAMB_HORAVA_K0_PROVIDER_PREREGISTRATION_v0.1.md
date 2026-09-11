# W05 M40 EFTCAMB Hořava K0 provider preregistration v0.1

Date: 2026-09-11
Family: F40 / M40 Hořava-Lifshitz gravity
Gate: K0 provenance/provider executability only

## Frozen provider

Repository: `EFTCAMB/EFTCAMB`
Commit: `16d9c4e9f85751e30efd0a53b177941713078904`
Native full-mapping implementation: `EFTflag=4`, `FullMappingEFTmodel=1`.
Native source: `fortran/eftcamb/08f_full_models/008p1_Horava.f90`.

The pinned provider documentation identifies the required parameters as `Horava_eta`, `Horava_xi`, and `Horava_lambda`. The provider's own test point `fortran/eftcamb_test/parameters/5_Horava_eta_3.ini` is frozen as the finite model point:

- `Horava_eta = 0.021`
- `Horava_xi = -0.001`
- `Horava_lambda = 0.001`

The same repository's native `1_EFT_GR.ini` test is the same-provider GR control.

## Independent arms

1. `horava_native`: execute the unmodified pinned `5_Horava_eta_3.ini` except output destination if required.
2. `eft_gr_control`: execute the unmodified pinned `1_EFT_GR.ini` except output destination if required.

Run in parallel with `fail-fast:false`.

## Frozen K0 acceptance

K0 is `PASS_WITH_SCOPE_PINNED_EFTCAMB_HORAVA_PROVIDER` iff:

- both checkouts equal the pinned commit exactly;
- EFTCAMB compiles with its documented `make camb` target;
- both arms exit 0;
- each arm produces non-empty finite scalar-CMB and matter-power outputs from the provider's native test pipeline;
- the finite Hořava arm is distinguishable from the same-provider GR control in at least one common CMB or matter-power sample by max symmetric relative difference > `1e-6`.

Build/runtime/output failure is provider or infrastructure blocking, never physical failure.

## Scope guard

This is K0 only. It does not establish the Hořava->GR limit, K2-K9, stability across parameter space, observational viability, or physical falsification. A separate prospective K1 gate is required before inspecting a parameter-to-zero ladder.