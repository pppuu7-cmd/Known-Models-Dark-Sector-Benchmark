# W03 M14 iDM tracked-author-input provider-control recovery preregistration v0.1

Status: FROZEN BEFORE EXECUTION
Date: 2026-09-10
Scope: K0/provider reproducibility only. No K1-K9 scientific promotion from this control.

## Provider

- repository: `kabeleh/iDM`
- pinned commit: `dc55e59dec8f5c647df6e9d764f5c6960796e1df`
- source family: scalar-field dark energy + interacting dynamical dark matter
- build command documented by provider: `make clean; make class -j`

## Why this recovery is allowed

The root README references `./class iDM.ini`, but that filename is absent from the pinned public tree. A later exhaustive pinned-tree inspection found tracked author-generated CLASS inputs under `benchmark/*/tmp_ini/`. Therefore the previous statement "no exact author input exists in the pinned tree" was too broad.

This gate uses the exact tracked file:

`benchmark/gcc/tmp_ini/pgo_hyperbolic_cmb.ini`

The file explicitly states it is a PGO training workload based on the author's Cobaya configuration. Its physical/cosmological settings include the hyperbolic scalar potential and the uncoupled iDM limit (`model_cdm=i`, `q1-q4=0` in the scalar parameter vector). This is sufficient for a provider executable control and a future coupling-off reference anchor, but not by itself a nonzero-coupling M14 production point.

## Frozen execution rule

1. clone and checkout the exact pinned commit;
2. build `class` with the provider-documented command;
3. copy `benchmark/gcc/tmp_ini/pgo_hyperbolic_cmb.ini` without changing any physical, numerical-accuracy, observable, IC, potential, matter, neutrino, or scalar settings;
4. the **only permitted edit** is replacing the author-machine absolute `root` output path with a GitHub-workspace-local output root. This is plumbing only;
5. execute `./class <copied-input>`;
6. preserve exit code, logs, copied input, parameters output and available spectra.

## Frozen classifications

- build nonzero -> `M14_PROVIDER_CONTROL_BLOCKED_BUILD`;
- build zero but CLASS exit nonzero -> `M14_PROVIDER_CONTROL_BLOCKED_EXECUTION`;
- build zero, CLASS exit zero, and fresh parameter/output product(s) present -> `M14_PROVIDER_CONTROL_PASS_TRACKED_AUTHOR_WORKLOAD`.

A green workflow is not sufficient; classification is based on the machine result JSON and preserved products.

## Scientific scope

Even on PASS:

- K0 may be upgraded from blocked provenance to `PASS_WITH_SCOPE` for this provider/workload;
- K1 remains NOT_TESTED until a separately preregistered coupling-off/reference regression is source-bound;
- K2-K9 remain NOT_TESTED;
- no claim about coupled-quintessence novelty, fit quality, stability or observational discrimination is authorized.

## Next gate after PASS

Audit the exact source coupling map and identify the physical zero-coupling coordinate(s). Then preregister a K1 regression in which the coupling is turned off while all shared scalar/cosmological settings are held fixed, before defining any nonzero-coupling response grid.
