# W04 M21 late-source branch/topology interaction diagnostic v0.1

Status: prospectively frozen before intervention results.
Parent authority: cross-cosmology provider regression run `34918945022`, aggregate artifact `10377492480` (`sha256:9d3acb0b6c9de4e8a5287521677799efb3f880931664a2bef6f5fd92b1a04775`).

## Question
The parent regression established authority-clean ULP sign diversity on both adjacent CLASS pins but rejected the simple rule that crossing `l > transfer_neglect_late_source*angular_rescaling` is by itself sufficient for a structural source-count consequence. In the five below-unity cosmologies per pin, native l=400 predicate=true versus the identity counterfactual predicate=false was operationally inert in the recorded transfer diagnostics. Test prospectively whether the complementary intervention (force the l=400 late-source predicate TRUE) is causally active in the two above-unity cosmologies (`base`,`h105`) where native predicate=false, thereby distinguishing a branch/topology interaction from a universal threshold-only mechanism.

## Frozen providers and cases
Pins remain exactly P0=`e85808324f51fc694d12e3ed7439552a3c3f9540`, P1=`64bbab707faf4de4779a9e04edd180fef18d98fa`. Cases are exactly `{P0,P1} x {base,h105}`. Same frozen `P400_ON_TAIL_OFF` profile and cross-cosmology input builder as parent.

## Intervention
Instrumentation may modify only `source/transfer.c`. Native execution is required to be null against an unpatched clean execution at relative L2 <=1e-12. Counterfactual execution changes only the boolean late-source decision at exactly l=400 for scalar temperature transfer: force the branch TRUE; it must not alter `ptr->angular_rescaling`, threshold, q/k grids, sources, neighboring l=399/401 predicates, or any physics input. `OMP_NUM_THREADS=1` for diagnostic executions.

## Frozen authority checks
All four cells must: exact pin; all CLASS exits 0; only transfer.c modified; patched-native/clean Cl relative L2 <=1e-12; >=20 finite diagnostic q rows for each l=399,400,401; native/forced q,k keys identical; native angular_rescaling constant and >1; threshold exactly 400; native l400 predicate=false and forced l400 predicate=true; l399/l401 predicate and source-count diagnostics identical between native and intervention.

## Frozen causal classification
For each cell define `l400_count_changed` iff at least one matched l400 q row changes `index_tau_max_Bessel`; define `cl_changed` iff native-vs-force Cl relative L2 >1e-12.

- all four authority-clean, all four have `l400_count_changed=true` and `cl_changed=true`, while the immutable parent reports all five below-unity cosmologies on both pins with `structural_rule_pass=false` under the opposite TRUE->FALSE intervention: `M21_LATE_SOURCE_BRANCH_TOPOLOGY_INTERACTION_CAUSALLY_SUPPORTED_WITH_SCOPE`.
- all four authority-clean but no cell changes l400 source count and no cell changes Cl: `M21_LATE_SOURCE_BRANCH_INTERVENTION_INERT_WITH_SCOPE`.
- all four authority-clean with a reproducible mixed pattern identical across pins: `M21_LATE_SOURCE_BRANCH_SENSITIVITY_COSMOLOGY_DEPENDENT_WITH_SCOPE`.
- any authority/schema/null/neighbor/pin failure, or provider-pin disagreement in the active/inert pattern: `M21_LATE_SOURCE_BRANCH_TOPOLOGY_INTERACTION_BLOCKED`.

## Claim ceiling
No K1/K3/K4 promotion; no physical falsification; no claim of a production CLASS defect or preferred fix. This gate localizes a numerical mechanism only. No threshold retuning or physics retuning is permitted after result inspection.