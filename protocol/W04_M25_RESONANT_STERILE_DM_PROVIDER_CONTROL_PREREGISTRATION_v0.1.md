# W04 M25 resonant sterile-DM provider-control preregistration v0.1

Date: 2026-09-11
Status: FROZEN BEFORE EXECUTION
Family: F25 / M25 resonantly produced sterile-neutrino-like warm dark matter
Provider: `ntveem/sterile-dm@e4486265e8207aa0dd28decc8c8d897266c0a52a`
Associated provider documentation cites arXiv:1507.06655.

## Purpose
Establish only that the pinned public provider can be built and can reproduce its own stock resonant-production workflow sufficiently to emit finite nonthermal sterile/antisterile phase-space distributions (PSDs) and a closure-density record on a current GitHub-hosted Linux runner.

This is infrastructure/provenance control. It does **not** establish a CLASS bridge, K1 reference limit, K3 closure, observational validity, or a physical preference for resonant sterile-neutrino dark matter.

## Frozen source and input
- Clone exactly `ntveem/sterile-dm` and checkout detached commit `e4486265e8207aa0dd28decc8c8d897266c0a52a`.
- Build using the provider's own current instructions: `./configure gfortran` then `make`.
- Run the provider's unmodified committed `params.ini` with `./sterile-nu params.ini`.
- No physical parameter, tolerance, grid, compiler flag, table or source file may be edited in this v0 control.
- Before execution, copy the committed `outfiles/` tree to a separate provenance-reference directory, then remove the run-side `outfiles/`; this prevents precommitted outputs from being mistaken for newly generated evidence.

The committed stock input contains two models with `m_s=7.115e-3 MeV` and `sin^2(2theta)={4e-11,8e-12}`, with the initial lepton asymmetry omitted so that the provider determines the value required to approach its target `omegadmh2=0.1188`.

## Frozen execution budget
The stock run may be computationally expensive because it can solve for the lepton asymmetry via repeated LSODE integrations. Give the executable a hard 30-minute wall-clock timeout on `ubuntu-latest`.

- Timeout/resource exhaustion is `M25_PROVIDER_CONTROL_BLOCKED_RUNTIME`, not physical failure.
- Build/configuration failure is `M25_PROVIDER_CONTROL_BLOCKED_BUILD`, not physical failure.

## Frozen output validation
If execution exits 0 inside the budget, inspect **newly generated** outputs only. Require at least two model directories containing:
- `params.dat` with at least six finite numeric entries: mass, mixing, lepton asymmetry, total `Omega_wdm h^2`, sterile contribution and antisterile contribution;
- `state.dat` with >= 2 finite numeric state rows and >= 5 columns;
- `Snapshot100.dat` with >= 100 finite rows and exactly/at least the first three numeric columns `(p[MeV], delta f_nu, delta f_nubar)`; momentum must be positive and strictly increasing, and both PSD columns must be nonnegative;
- total density consistency `|Omega_wdm - (Omega_s+Omega_sbar)| <= 5e-8` for each model;
- closure consistency `|Omega_wdm h^2 - 0.1188| <= 5e-4` for each model.

Record SHA256 hashes and structural summaries of generated `params.dat`, `state.dat` and `Snapshot100.dat`. Also record corresponding hashes of the committed stock reference when filenames/directories can be matched, but **do not require byte identity** across compiler/runtime generations.

## Frozen classification
- build/configure nonzero: `M25_PROVIDER_CONTROL_BLOCKED_BUILD`
- stock executable timeout/resource stop: `M25_PROVIDER_CONTROL_BLOCKED_RUNTIME`
- executable exits nonzero or required outputs are structurally/physically invalid under the frozen checks: `M25_PROVIDER_CONTROL_OUTPUT_INVALID`
- otherwise: `M25_PROVIDER_CONTROL_PASS_STOCK_RESONANT_PSD`

For every classification:
- `K1_promoted = false`
- `physical_falsification = false`

## Next-step rule
Only after PASS may a new prospective bridge preregistration map the final nonthermal PSD to CLASS `ncdm_psd_files`. That bridge must define the momentum variable, normalization, sterile+antisterile combination, density preservation, and a decoupling/reference construction before any K1 claim. Do not approximate F25 with a thermal-WDM distribution merely because it is easier to run.
