# M21 l=400 diagnostic threading forensics

Date: 2026-09-15

## Scope

This note explains the instrumentation-only corruption observed in terminal run `34906741049` and validates the preregistered serialization recovery. It does not change any scientific protocol, physical input, precision profile, threshold, metric, classifier, or provider pin.

Exact provider remains `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Observed failure

The multithreaded l=400 transfer-convolution diagnostic produced malformed rows in `conv_f2.dat`. The complete file had the same total newline count as the clean reference diagnostic, but 1330 rows did not contain the frozen 12-field schema. Examples showed fragments from distinct rows concatenated into one line and complementary truncated lines. This created spurious parsable q-index values and caused the frozen `same_q_index_set` integrity check to fail.

The underlying CLASS run itself remained clean: case execution returned zero, exact provider identity passed, and the full `cl.dat` null comparison against the immutable parent passed at normalized L2 <= `1e-12`.

## Why the original named OpenMP critical did not serialize I/O

The exact build log from run `34906741049` shows CLASS compiled with `-pthread` and without `-fopenmp`. Therefore `#pragma omp critical(kmdsb_m21_l400_conv_diag)` in the output-only diagnostic patch was not an active synchronization primitive in that build.

On this CLASS pin, parallelism is implemented by `include/parallel.h`, not by OpenMP. `class_setup_parallel()` constructs `Tools::TaskSystem`, which uses `std::thread`; `class_run_parallel()` submits asynchronous tasks to that task system.

`Tools::TaskSystem::GetNumThreads()` checks environment variables in this order:

1. `OMP_NUM_THREADS`
2. `SLURM_CPUS_PER_TASK`

and uses the first valid positive value as the task-system thread count.

The transfer module calls `class_setup_parallel()` and then runs the q/wavenumber loop through `class_run_parallel(...)`. Thus multiple q jobs can enter the diagnostic writer concurrently when the task system has more than one worker.

## Recovery authority

The preregistered recovery in `protocol/W04_M21_L400_TRANSFER_CONVOLUTION_DIAGNOSTIC_SERIALIZATION_RECOVERY_v0.1.md` changes only the diagnostic CLASS execution environment to:

`OMP_NUM_THREADS=1`

Although the provider is not compiled with OpenMP, this variable is explicitly consumed by the provider's own `Tools::TaskSystem`. Therefore it reduces the transfer q-loop to one worker and removes the actual concurrency responsible for the malformed diagnostic rows.

No provider source, output-only patch, physical input, precision profile, l-grid, k-support, timeout, metric, threshold, parent artifact, analyzer, or classification rule is changed.

## Current authoritative recovery

- runner commit: `2338fb5a4ee92c8b94a1583089465e42d164f439`
- recovery run: `34907528331`
- required parent scientific protocol: `protocol/W04_M21_L400_TRANSFER_CONVOLUTION_DECOMPOSITION_v0.1.md`
- required recovery protocol: `protocol/W04_M21_L400_TRANSFER_CONVOLUTION_DIAGNOSTIC_SERIALIZATION_RECOVERY_v0.1.md`

Until the recovery run is terminal, no source/radial/convolution scientific classifier may be promoted from this diagnostic.

## Claim ceiling

This establishes the mechanism of the diagnostic serialization blocker and validates the single-thread recovery mechanism. It does not establish a CLASS defect, a production threading recommendation, a physical warm-dark-matter effect, K1/K3/K4 promotion, or physical validation/falsification.
