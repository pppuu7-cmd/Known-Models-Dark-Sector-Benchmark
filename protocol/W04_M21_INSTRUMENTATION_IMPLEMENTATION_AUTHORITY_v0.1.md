# W04 M21 instrumentation implementation authority v0.1

Status: prospectively frozen after context-authority run `35244141537` PASS and before any instrumented scientific trajectory is executed.

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.
Scientific authority remains `protocol/W04_M21_L400_APPROX_STATE_SOURCE_ZERO_TRANSITION_AUDIT_v0.1.md`; this document does not alter any threshold or classification rule.

## Purpose
Before patching the pinned provider, machine-check exact insertion semantics for output-only instrumentation. The implementation must observe values only after scalar `index_tp_p` and approximation-state values are computed. It must not modify arrays, state, precision, integration order, source values, branching, or trajectory.

## Required implementation authority
A valid implementation-authority batch must independently validate:
1. `source_assignment`: an insertion point immediately after the native scalar-E source assignment, with native k/tau indices available.
2. `approximation_states`: RSA/TCA state variables are in lexical/runtime scope at the selected observation point, or an explicitly documented read-only propagation path is required before scientific execution.
3. `visibility`: provider-native `g` is available read-only at the observation point, without recomputation that changes state.
4. `polarization_primitives`: native `P` and primitive terms entering P are available read-only, or the batch must fail closed and identify the missing scope.

Each lane must emit exact provider file, line/context, provider commit and SHA256. Ambiguous/multiple candidate insertion points are not scientific authorization: classify implementation authority BLOCKED until a unique provider-native path is machine-resolved.

## Barrier
All four independent lanes must PASS before an instrumented ref/f2/f3/f4 scientific workflow may run. Any missing scope, ambiguous insertion point, source mismatch, provider mismatch, or inability to observe without trajectory mutation => `M21_L400_INSTRUMENTATION_IMPLEMENTATION_AUTHORITY_BLOCKED`.

PASS classification: `M21_L400_INSTRUMENTATION_IMPLEMENTATION_AUTHORITY_PASS`.

No K1/K3/K4 promotion and no physical falsification can result from this implementation-authority gate.
