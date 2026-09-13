# W03 M13b K3D2-B piecewise restart source-audit recovery v0.1

Frozen: 2026-09-14 after run 34785693083 and before the recovery audit is executed.

Parent: `protocol/W03_M13B_K3D2B_PIECEWISE_BACKGROUND_RESTART_SOURCE_AUDIT_v0.1.md`.
Provider: `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.

## Observed harness-only failure

Run 34785693083 passed every frozen structural check except `loga_ini_assigned`. The failed predicate searched only for an explicit textual assignment `loga_ini = ...`.

Exact-pin CLASS instead initializes `loga_ini` through the output argument of the existing call

`background_initial_conditions(..., &(loga_ini))`.

This recovery changes no solver equation, handoff value, physical parameter, threshold, or authorization boundary. It only broadens the source-audit predicate so that `loga_ini` is considered established if either:

1. an explicit assignment to `loga_ini` exists; or
2. `loga_ini` is passed by address to `background_initial_conditions`.

All other frozen checks are unchanged.

## PASS

PASS requires all original structural checks plus the recovered initialization predicate. Classification remains

`M13B_K3D2B_EXACT_PIECEWISE_RESTART_STRUCTURALLY_AUTHORIZED_WITH_SCOPE`.

A PASS authorizes a separately frozen two-segment implementation probe with a null segmentation control. It does not authorize a K3 promotion and does not establish physical agreement with K3C1/K3C2.
