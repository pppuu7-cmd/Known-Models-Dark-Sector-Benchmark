# W04 M21 l=400 transfer-convolution diagnostic serialization recovery v0.1

Frozen: 2026-09-15 after terminal run `34906741049` classified `M21_L400_TRANSFER_CONVOLUTION_DECOMPOSITION_BLOCKED` only because `same_q_index_set=false`, and before any recovery execution.

Provider remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Parent authority and observed harness failure

The parent scientific protocol is `protocol/W04_M21_L400_TRANSFER_CONVOLUTION_DECOMPOSITION_v0.1.md`; all its physical inputs, support, diagnostics, thresholds, profile metrics and classification rules remain frozen.

Parent run `34906741049` established:
- all four case executions `ref,f2,f3,f4` completed with `authority_clean=true`;
- all four full CMB null comparisons against the immutable parent passed at normalized L2 <= `1e-12`;
- exact provider identity passed;
- aggregate was blocked by `same_q_index_set=false` before scientific profile classification.

Post-terminal harness diagnosis found malformed/interleaved rows in the output-only diagnostic file under multithreaded execution. In `f2`, valid support rows contain the expected real q range `261..333`; reference also contains `261..333`. Same-q physical k values agree to max relative difference about `1.2e-10`, well inside the already-frozen `1e-6` geometry bound. Corrupted fragments created spurious parsed q values and therefore invalidated the raw q-set integrity check.

This is an instrumentation serialization failure, not a provider or physics result.

## Frozen recovery

The only allowed execution change is:

`OMP_NUM_THREADS=1`

for the four diagnostic CLASS case executions.

No source patch, provider pin, physical input, precision profile, l-grid, k support, timeout, numerical tolerance, observable, threshold, metric, parent artifact, analyzer, or classification rule may change.

The diagnostic patch remains output-only and the original frozen q-index integrity rule remains in force.

## Recovery integrity

The recovered run must still require for every case:
- CLASS return code zero;
- exact provider pin;
- only `source/transfer.c` modified by the output-only patch;
- diagnostic file present and non-empty;
- normalized L2 difference of full `cl.dat` from the immutable matching factorial parent <= `1e-12`.

The aggregate must then pass the original protocol unchanged, including:
- exact same support q-index set across all four cases;
- relative same-q k difference <= `1e-6`;
- block reconstruction relative error <= `1e-10`;
- at least 20 tau rows per block and consecutive tau indices.

Any failure remains `M21_L400_TRANSFER_CONVOLUTION_DECOMPOSITION_BLOCKED`.

## Claim ceiling

A successful recovery only repairs diagnostic serialization and permits the already-frozen source/radial/convolution classifier to execute. It does not establish a CLASS defect, a production precision recommendation, K1/K3/K4 promotion, or physical validation/falsification.
