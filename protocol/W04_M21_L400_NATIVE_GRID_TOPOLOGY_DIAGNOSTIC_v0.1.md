# W04 M21 l=400 native-grid topology diagnostic v0.1

Status: prospectively frozen before execution.

## Authority
Authorized only after immutable run `34961138696` classifies `M21_L400_ACCUMULATION_WINDOW_LOCALIZATION_BLOCKED` because native accumulation grids differ across ref/f2/f3/f4. Use only the immutable convolution component artifacts from recovery run `34907528331` plus immutable blocked-result artifact `10393755721`. No CLASS rerun, interpolation, zero-imputation, physics retuning, or grid alignment is allowed.

## Question
Determine whether the representation boundary is specifically an f3 native-grid topology expansion and characterize it without comparing pointwise physics on mismatched grids.

## Frozen observables
For every common q and case report native row count N; coordinate-u endpoints min/max; median absolute adjacent du; min/max absolute adjacent du; and count ratios relative to ref. Require authority-clean metadata, identical q sets, consecutive native index 0..N-1, N>=20, finite strictly monotone u, and exact stored index_tau_max=N-1.

Define dN_c(q)=N_c(q)-N_ref(q). Define f3-exclusive expansion at q iff dN_f3(q)>0 and dN_f3(q)>max(dN_f2(q),dN_f4(q)). Define expansion_fraction as fraction of q satisfying that predicate. Define endpoint-clean iff for every q/case both u-min and u-max relative differences versus ref are <=1e-8; this distinguishes denser sampling of the same support from support-domain extension. No interpolation is permitted.

## Frozen classification
Any authority/integrity/q-set/monotonicity failure -> `M21_L400_NATIVE_GRID_TOPOLOGY_BLOCKED`.
If expansion_fraction>=0.9 and endpoint-clean -> `M21_L400_F3_NATIVE_GRID_DENSIFICATION_WITH_SCOPE`.
If expansion_fraction>=0.9 and endpoint-clean is false -> `M21_L400_F3_NATIVE_GRID_SUPPORT_AND_DENSITY_CHANGE_WITH_SCOPE`.
Otherwise -> `M21_L400_NATIVE_GRID_CHANGE_NOT_F3_EXCLUSIVE_WITH_SCOPE`.

## Guardrails
Solver-layer representation diagnostic only. It cannot promote K1/K3/K4, establish physical falsification, or by itself claim a CLASS defect. A densification outcome authorizes a prospectively frozen common-coordinate observation operator diagnostic; a support-and-density outcome requires support-domain decomposition first; a non-exclusive outcome requires cross-case grid-generation analysis.