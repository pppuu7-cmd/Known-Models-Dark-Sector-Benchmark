# W03 M14 LisaGoh/CDE provider-control recovery preregistration v0.3

Date: 2026-09-10
Parent recovery run: `34474433991`

## Observed result

With the v0.2 standalone `make class` recovery, the exact pinned source built successfully (`build_exit=0`) and the exact committed `CDE.ini` entered and completed the scientific computation stages:

- background;
- thermodynamics;
- perturbation sources;
- primordial spectra;
- Halofit;
- transfers;
- lensed spectra.

It then failed only in `output_init` because the auto-selected output root was `output/CDE00_...` and a fresh Git clone did not contain the empty `output/` directory:

`could not open *clfile with name output/CDE00_cl.dat and mode "w"`.

No physical equation/integration failure occurred before this filesystem error.

## Frozen recovery

Repeat the v0.2 control with exactly one additional infrastructure action before execution:

`mkdir -p provider/class_CDE/output`

Then execute unchanged:

`./class CDE.ini`

Do not edit source, INI, coupling amplitudes, scalar initial conditions, precision settings or output list.

## Decision rule

Retain the original provider-control PASS criteria: build/run exit zero plus fresh nonempty background, linear P(k), CMB Cl and transfer products.

Any new failure must be treated separately and cannot be repaired without another preregistration.

No K1/K3/K4/K5 promotion is authorized merely by creating the output directory.