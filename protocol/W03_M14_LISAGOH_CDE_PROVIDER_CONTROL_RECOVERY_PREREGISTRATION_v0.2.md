# W03 M14 LisaGoh/CDE provider-control recovery preregistration v0.2

Date: 2026-09-10
Parent control: `W03_M14_LISAGOH_CDE_PROVIDER_CONTROL_PREREGISTRATION_v0.1.md`
Parent run: `34474257067`

## Observed blocker

The exact pinned source compiled every C object and successfully linked the standalone executable `class`. The default Makefile then continued into the optional Python `classy` installation target and failed because the GitHub runner lacked the Python `Cython` package:

`ModuleNotFoundError: No module named 'Cython'`.

The committed author workload is executed through `./class CDE.ini`; it does not require the Python `classy` extension.

Therefore the parent result is an environment/package-target blocker, not a source/physics build failure.

## Frozen recovery

Repeat the exact same provider control with one infrastructure-only change:

- after `make clean`, invoke the committed Makefile's standalone executable target `make class -j2` instead of the default `make -j2` target that additionally attempts `classy` installation.

No compiler flags, source files, INI parameters, physics equations, beta values, scalar initial conditions, precision settings or output requests may change.

The execution remains exactly:

`./class CDE.ini`

## Decision rule

Use the unchanged v0.1 provider-control PASS criteria: build/run exit zero plus fresh nonempty background, linear P(k), CMB Cl and transfer outputs.

If `make class` or `./class CDE.ini` fails, classify the provider as runtime/implementation blocked and inspect that new failure separately. Do not apply further environment/source changes without a new preregistration.

No K1/K3/K4/K5 scientific promotion is authorized by the recovery itself.