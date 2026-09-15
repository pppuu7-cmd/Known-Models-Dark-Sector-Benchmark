# W04 M21 l=400 approximation-state / source-zero transition audit v0.1

Status: prospectively frozen after terminal q-scaling run `34985846954` classified `M21_L400_F3_SUPPORT_EXTENSION_MONOTONE_NONLINEAR_WITH_SCOPE`, before this audit is executed.

## Authority
Provider remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`. Parent authority: topology run `34972611076`, support-domain run `34978980507`, q-scaling run `34985846954`, and the exact source identity already frozen in `W04_M21_L400_CONDITIONAL_SOURCE_FACTORIZATION_v0.1.md`: scalar E source `S_E=sqrt(6)*g*P`; RSA => P=0; outside RSA, P follows the provider TCA/full-polarization branch.

## Purpose
Determine which exact provider state transition permits f3 scalar-E source support to remain non-zero beyond the common ref/f2/f4 source-zero endpoint. This is a solver-layer diagnostic only.

## Frozen execution
Run ref/f2/f3/f4 as four independent jobs at the same exact physical inputs and precision profile as the authoritative recovered M21 parent. Pin the provider commit above and use `OMP_NUM_THREADS=1`. The only source modification permitted is output-only instrumentation after scalar `index_tp_p` values and approximation states are computed. It may record native k/tau indices and values, RSA state, TCA state, visibility g, P, reconstructed `sqrt(6)*g*P`, and the primitive terms entering P. It must not modify arrays, state, precision, integration order, source values, or trajectory.

Each instrumented case must reproduce its corresponding immutable parent `cl.dat` with normalized L2 <=1e-12 or BLOCK.

## Frozen endpoint and observables
Use the already-authoritative common ref/f2/f4 terminal native transfer index J_shared=2905 and the q=261..333 parent support. For each accepted target q, map instrumented native perturbation-k data to the exact parent transfer k using the provider-authoritative spline rule; nearest-neighbor matching is forbidden. Require reconstructed scalar-E source relative error <=1e-10 on retained finite parent rows.

For each case/q report: last non-zero-P tau/u; last non-zero-S_E tau/u; nearest RSA transition; nearest TCA transition; g and P immediately before/at/after the shared endpoint; primitive-P components; and signed distance in u from each state transition to the shared endpoint and to the f3 terminal support. No interpolation between tau samples and no zero-imputation.

## Frozen classification
Any authority, reproduction, reconstruction, finite-value, q-support or instrumentation failure -> `M21_L400_APPROX_STATE_SOURCE_ZERO_TRANSITION_AUDIT_BLOCKED`.

If >=90% of q show an f3-exclusive RSA-state difference whose nearest transition lies within one native f3 tau step of the onset/termination of the extended non-zero source, while ref/f2/f4 share the alternate RSA state -> `M21_L400_F3_EXTENDED_SUPPORT_RSA_TRANSITION_LOCALIZED_WITH_SCOPE`.

Else if >=90% show the analogous f3-exclusive TCA-state difference -> `M21_L400_F3_EXTENDED_SUPPORT_TCA_TRANSITION_LOCALIZED_WITH_SCOPE`.

Else if approximation states are shared but >=90% show f3-exclusive persistence of |P|>0 beyond the common source-zero endpoint while g remains finite/nonzero -> `M21_L400_F3_EXTENDED_SUPPORT_POLARIZATION_FACTOR_PERSISTENCE_WITH_SCOPE`.

Else if P behavior is shared but >=90% show f3-exclusive visibility persistence driving S_E -> `M21_L400_F3_EXTENDED_SUPPORT_VISIBILITY_PERSISTENCE_WITH_SCOPE`.

Otherwise -> `M21_L400_F3_EXTENDED_SUPPORT_TRANSITION_NOT_SINGLE_FACTOR_LOCALIZED_WITH_SCOPE`.

The 90% boundary and one-native-step transition tolerance are frozen here before execution and must not be relaxed afterward.

## Guardrails / successor
No K1/K3/K4 promotion and no physical falsification. A localized approximation-state result authorizes a separately preregistered trigger-condition audit of that exact state transition. A P- or g-localized result authorizes a separately preregistered primitive-factor audit. A mixed result requires factor decomposition without retuning physics. This gate does not establish a CLASS defect or production recommendation.