# W07 M35 K4 serialized precision diagnostic v0.1

Status: FROZEN BEFORE RESULT

## Trigger
Two independent attempts of run 34773348806 reproduced the same execution pattern: all three default precision cases complete, while every permille/reference case is externally terminated by the GitHub-hosted runner before the wrapper can write the provider return code. Example: attempt-2 base_permille job 103774859056 received a runner shutdown signal and exit 143 about 28 s after solver launch. This is an infrastructure/execution interruption, not a provider rc and not a K4 scientific classification.

A subsequent single-job rerun request maps to the whole matrix job in GitHub Actions, so it is not a safe way to isolate one matrix child. Therefore the next diagnostic uses a dedicated six-case precision-only matrix with max-parallel: 1.

## Frozen science
Provider remains Michalychforever/CLASS_LVDM exact commit d9a20bd0c7b7a6c8957410fd245ed06b30b915c1. Physical points remain base=(q=.100,Y=0), gravity=(q=.102,Y=0), Y=(q=.100,Y=.002) with alpha=.05q, beta=.25q, lambda=-.10q. Observables remain tCl,pCl,lCl,mPk. Precision profiles remain the exact provider cl_permille.pre and cl_ref.pre files. No thresholds, equations, parameters, output channels, or scientific analyzer rules may change.

## Allowed change
Execution topology only: run the six previously interrupted permille/reference cases one at a time with matrix max-parallel: 1 and fail-fast:false. Each wrapper must use set +e, record the actual provider rc if control returns, upload stdout/stderr/rc with if:always(), and never reinterpret external runner shutdown as provider failure.

## Classification
This diagnostic does not promote K4 by itself. If serialized cases still receive runner shutdown before an rc is written, classify persistent hosted-runner execution-capacity/infrastructure blocker. If cases return provider rc and artifacts, those immutable outputs may be consumed by a separately preregistered analysis-only reconstruction together with already validated default-case artifacts; no heavy default recomputation is authorized merely for convenience.
