# W04 M21 CLASS output-root naming recovery v0.1

## Trigger
Hosted run `34537696887` built the pinned CLASS provider and executed the exact reference plus all five finite mixed cold+warm cases with exit code 0. The scientific analyzer then failed before reading any observable because it expected `output/ref_cl.dat`, while the pinned CLASS executable serializes these command-line runs with a `_00_` insertion in the output root (for example `f0_00_cl.dat`, `f0_00_pk.dat`, `f0_00_background.dat`).

This is an output-discovery defect in the KMDSB harness. It is not a model failure and no K gate was evaluated.

## Frozen repair
Change only output-file discovery in `verification/m21/mixed_cold_warm_k1_reference.py` and evidence upload patterns:

- for a case prefix `ref` or `f{i}`, require exactly one file matching `<prefix>_*_cl.dat`;
- require exactly one matching `<prefix>_*_pk.dat`;
- require exactly one matching `<prefix>_*_background.dat`.

The implementation may retain a fallback to the originally expected `<prefix>_cl.dat`, `<prefix>_pk.dat`, `<prefix>_background.dat` only if exactly one path is resolved.

## Noninterference
Do not change:
- CLASS pin;
- cosmological parameters;
- warm mass or temperature;
- fraction ladder;
- common outputs;
- interpolation;
- residual definition;
- K1 thresholds or K2 interpretation.

The repaired run must execute the same frozen physical cases from scratch. Only then may the K1 result be consumed.
