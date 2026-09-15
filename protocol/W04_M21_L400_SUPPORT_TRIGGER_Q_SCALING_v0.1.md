# W04 M21 l=400 support-trigger q-scaling diagnostic v0.1

Status: prospectively frozen after terminal support-domain run `34978980507` classified `M21_L400_F3_EXTENDED_SUPPORT_AMPLITUDE_SUFFICIENT_WITH_SCOPE`, before this diagnostic is evaluated.

## Authority
Use only immutable topology artifact from run `34972611076` and immutable support-domain artifact from run `34978980507`. No CLASS rerun, interpolation, retuning, or physical parameter changes.

## Purpose
Determine whether the amplitude-sufficient f3-only support extension is a systematic q-dependent grid/support phenomenon or an irregular collection of isolated q nodes. This is a solver-layer trigger-map diagnostic, not physical falsification and not a CLASS-defect claim.

## Frozen observables
For q=261..333 require all 73 q integrity-clean in both parents, f3 extended support nonempty, and f2/f4 outside-reference support absent. Read f3 native row count N3(q), reference row count Nref(q), and support endpoints from the topology artifact. Define dN(q)=N3-Nref and du_lo(q)=u_min_ref-u_min_f3. Require finite values and dN>0, du_lo>0 for every q.

Compute ordinary least-squares fits dN=a_N+b_N(q-261) and du_lo=a_u+b_u(q-261), and normalized RMS residuals NRMS_N and NRMS_u relative to each observable's full range. Also compute strict monotonic-step fractions: fraction of adjacent q pairs with dN(q+1)>=dN(q) and du_lo(q+1)>=du_lo(q).

## Frozen classification
Any authority/schema/q/integrity/nonfinite failure -> `M21_L400_SUPPORT_TRIGGER_Q_SCALING_BLOCKED`.

If both monotonic-step fractions >=0.95 and both NRMS <=0.10 -> `M21_L400_F3_SUPPORT_EXTENSION_SMOOTH_Q_DEPENDENT_WITH_SCOPE`.

If both monotonic-step fractions >=0.90 but either NRMS >0.10 -> `M21_L400_F3_SUPPORT_EXTENSION_MONOTONE_NONLINEAR_WITH_SCOPE`.

Otherwise -> `M21_L400_F3_SUPPORT_EXTENSION_IRREGULAR_Q_DEPENDENCE_WITH_SCOPE`.

## Guardrails / successor
No K1/K3/K4 promotion and no physical falsification. A smooth or monotone outcome authorizes a separately preregistered source-zero / approximation-state transition audit on the exact provider trajectory; an irregular outcome requires first localizing discrete q-grid/approximation transitions. Survival or failure here is not evidence for or against mixed cold+warm DM physics.