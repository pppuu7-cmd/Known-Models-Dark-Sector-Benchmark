# W04 M22 / F22 K4 tail precision transition preregistration v0.1

Status: FROZEN BEFORE P4 EXECUTION

## Motivation
The completed frozen M22 K4 ladder (run `34717830680`) found `permille -> reference` maximum symmetric discrepancy `Dmax=0.005705369407192887` at p3=`3.33e-25` and `Dmax=1.0579184021188854` at p5=`3.33e-26`, while exact zero-vs-omitted identities passed. This follow-up localizes the transition without repeating saturated p3/p5 calculations.

## Frozen new point and profiles
Compute only p4=`1.11e-25` under the exact same CLASS pin `e85808324f51fc694d12e3ed7439552a3c3f9540` and the exact provider precision profiles `cl_permille.pre` and `cl_ref.pre`. For each profile execute zero plus p4 so the response is self-contained. No default-profile rerun is authorized.

Mandatory blocks: TT, EE, TE, linear P(k). Reuse the same response definitions and symmetric cross-profile discrepancy `D=2|a-b|/(|a|+|b|+1e-30)` as the completed ladder. Missing/failed outputs are BLOCKED and never zero-imputed.

## Frozen interpretation
Let `D3`, `D4`, `D5` be the maximum over TT/EE/TE/P(k) for p3, p4, p5 respectively, with D3 and D5 read from the durable authoritative completed result.
- If not `D3 <= D4 <= D5`, classify `M22_K4_TAIL_PRECISION_STRUCTURE_NONMONOTONE_DIAGNOSTIC`.
- Otherwise if `D4 <= 0.10`, classify `M22_K4_TAIL_PRECISION_TRANSITION_LOCALIZED_P4_TO_P5_DIAGNOSTIC`.
- Otherwise classify `M22_K4_TAIL_PRECISION_TRANSITION_LOCALIZED_P3_TO_P4_DIAGNOSTIC`.
- Any execution/integrity failure -> `M22_K4_TAIL_PRECISION_TRANSITION_BLOCKED`.

This is localization only: `K4_promoted=false`, `diagnostic_only=true`, `scientific_fail=false`, `physical_falsification=false` for every non-blocked outcome. No threshold or point may be retuned after p4 is seen.
