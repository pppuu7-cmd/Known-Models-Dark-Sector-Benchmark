# W03 M13b K3D2-B exact piecewise background-restart source audit v0.1

Frozen: 2026-09-14 after run `34785222496` showed that the previously frozen global RK substitution is not validated and that the enabled hard handoff still underflows exactly at `loga=log(1/6)`.

Provider: `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.

## Motivation

The hard z=5 realization uses an exact RHS switch at `a=1/6`. NDF15 and RK both fail while attempting to integrate across that discontinuity. Smoothing or moving the switch, changing field starts, changing equations, relaxing thresholds, or retuning physics is forbidden.

The only new route authorized here is a source-structural audit asking whether the exact pinned CLASS background integration can be split into two consecutive integrations with an explicit restart exactly at `loga_h = log(1/6)`, carrying the complete integration state continuously across the boundary. This would change numerical execution topology only; the pre-handoff zero RHS and post-handoff frozen KG RHS must remain byte-identical.

## Frozen structural checks

The audit shall inspect exact-pin `source/background.c` and fail closed unless all of the following are true:

1. `background_solve` contains exactly one direct `generic_evolver(background_derivs, ...)` production call.
2. That call is parameterized by mutable local `loga_ini` and `loga_final` bounds.
3. The integration state is represented by the same `pvecback_integration` buffer before and after the call, allowing a second call to continue from the state produced at the first endpoint without resetting field variables.
4. The output callback is `background_sources`, so both segments can populate the same background table semantics.
5. No hidden solver-specific state object is passed between calls beyond the integration vector and the ordinary CLASS background workspace.
6. The exact handoff value `loga_h=log(1/6)` lies strictly inside the normal integration interval.

## Interpretation

PASS_WITH_SCOPE authorizes only a separately preregistered implementation probe of a two-segment exact restart at `loga_h`, followed by unchanged B1/B2/B3 gates and an independent null-control proving segmentation itself does not alter standard LambdaCDM beyond frozen tolerances.

NOT_ESTABLISHED means this numerical route is not structurally justified from the pinned source and K3D2-B remains numerically blocked. Neither outcome is physical falsification.
