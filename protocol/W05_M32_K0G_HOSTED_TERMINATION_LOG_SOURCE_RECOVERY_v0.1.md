# W05 M32 K0g hosted-termination log-source recovery v0.1

Date: 2026-09-12

Parent immutable audit run `34708420204` was integrity-blocked only because `gh run view --log` omitted a runner-level shutdown line that is present in the job-specific immutable log. This recovery changes only the log retrieval source to the exact K0g job `103591842815` from source run `34708140820`.

All evidence requirements remain unchanged: exact source run/head/workflow; checkpoint fetch success; Intel install success; explicit umuscl compile step failed; job-specific log must contain the runner shutdown signal, exit code 143, `make umuscl.o`, and termination of an orphan `ifx` process. No compiler/source/physics conclusion is inferred from an externally terminated process.

If all unchanged signatures pass, classify `M32_K0G_HOSTED_RUNNER_TERMINATED_DURING_IFX`. K0 remains unpromoted and physical_falsification=false.