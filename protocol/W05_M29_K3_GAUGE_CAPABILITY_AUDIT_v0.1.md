# W05 M29 Brans-Dicke K3 gauge-capability audit v0.1

Date: 2026-09-11
Provider: `hiclass-code/hi_class_public` at `0009f51d89e6465c79e570b496c66fc90058fa77`.
Scope: determine whether the pinned provider can support the prescribed same-model synchronous-vs-Newtonian observable cross-gauge closure gate.

## Frozen decision rule

- `CAPABLE` only if scalar modified-gravity perturbations can execute in both synchronous and Newtonian gauges in the pinned provider without model-changing patches.
- `BLOCKED_PROVIDER_GAUGE_IMPLEMENTATION` if the source explicitly rejects either required gauge for scalar modified gravity.
- Provider blocking is not physical falsification and cannot be converted into K3 PASS/FAIL for Brans-Dicke physics.

No new physics calculation is authorized under this audit. Source capability is the object being tested.