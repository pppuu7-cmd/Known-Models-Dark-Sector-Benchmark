# W07 M40 pinned-source geometry audit v0.1

## Purpose

Establish exactly what the pinned EFTCAMB Hořava implementation exposes at the source/configuration level before interpreting local response-rank calculations. This source audit is independent of the numerical xi/lambda coordinate-response batch and cannot by itself promote K2.

## Frozen provider and files

Provider: `EFTCAMB/EFTCAMB@16d9c4e9f85751e30efd0a53b177941713078904`.

Inspect and hash exactly:

- `fortran/eftcamb/08f_full_models/008p1_Horava.f90`
- `find_your_model/Setting and Specfying.md`
- `inifiles/params_EFT.ini`
- `fortran/eftcamb_test/parameters/5_Horava_eta_2.ini`
- `fortran/eftcamb_test/parameters/5_Horava_eta_3.ini`

## Frozen questions

1. Does the normal `FullMappingEFTmodel=1` route expose `Horava_xi`, `Horava_lambda`, and `Horava_eta` separately?
2. Is `HoravaSolarSystem` false by default in the pinned provider?
3. Does the optional `HoravaSolarSystem=true` branch explicitly ignore/reduce the xi input?
4. Does the source contain nontrivial formulas involving combinations of xi/lambda/eta, rather than treating them as mere aliases of one scalar input?
5. Is the current local-response base point `(-1e-4,+1e-4,0.0021)` an author-shipped test configuration in `5_Horava_eta_2.ini`?

## Classification

- `M40_SOURCE_THREE_INPUT_COORDINATES_OPTIONAL_SOLAR_REDUCTION` if questions 1-5 are all verified.
- `M40_SOURCE_INPUT_GEOMETRY_PARTIAL` if some but not all are verified.
- `M40_SOURCE_GEOMETRY_INTEGRITY_BLOCKED` if the exact pin/files cannot be verified.

## Scope guard

This audit establishes implementation-level input geometry only. It does not prove three independent physical degrees of freedom, an injective covariant parameterization, absence of degeneracies, local observable rank, global K2 closure, observational distinguishability, or physical validity. Always set `K2_promoted=false` and `physical_falsification=false`.
