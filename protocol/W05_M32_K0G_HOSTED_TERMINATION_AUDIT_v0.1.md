# W05 M32 K0g hosted-termination immutable audit v0.1

Date: 2026-09-12

## Purpose
Preserve and classify the terminal evidence from K0g run `34708140820` without rerunning the Intel compilation. This is analysis-only infrastructure adjudication.

## Immutable requirements
The run must be the workflow `.github/workflows/w05-m32-k0g-umuscl-microcheckpoint.yml` at head SHA `70c7f89bbc2ed27b7f7f71ab5e7770d3422e4815`. Its job evidence must show the immutable-checkpoint fetch and Intel toolchain installation completed successfully, the explicit `umuscl.o` compile step started, then the hosted runner reported a shutdown signal / exit 143 and terminated an `ifx` orphan process. No Fortran compiler diagnostic may be reinterpreted from absence of a completed log.

## Frozen interpretation
If all signatures are present, classify `M32_K0G_HOSTED_RUNNER_TERMINATED_DURING_IFX`. This is an infrastructure blocker only. It is not a source/compiler/physics failure and cannot promote or falsify K0. Repeating the same hosted route is not authorized by this audit; any further execution must materially change the execution environment while preserving provider pin, source and flags.