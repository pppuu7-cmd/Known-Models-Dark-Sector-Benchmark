# W04 M21 l=400 accumulation-window localization v0.1

Status: prospectively frozen before execution.

## Authority
This analysis is authorized only after `M21_L400_EDGE_SPECIFICITY_ABSOLUTELY_INSUFFICIENT_WITH_SCOPE`. It uses the immutable clean convolution component artifacts from recovery run `34907528331` and the immutable edge-sufficiency result from run `34950152312`. No CLASS rerun and no physics retuning are allowed.

## Question
After excluding the specificity-localized edge term as absolutely insufficient, determine whether the f3-specific total-transfer excess is concentrated in a prospectively defined part of the signed tau accumulation.

## Frozen construction
For each common q, use the reference case's absolute pointwise convolution budget `|C_ref(tau)|` on the native consecutive tau index. Partition that budget into ten equal cumulative-absolute-budget bins with fixed boundaries 0,0.1,...,1.0. Boundaries are determined from reference only, never from f3. For every case and bin, sum the native signed pointwise contributions `C`; do not interpolate, zero-impute, or change grids. Require identical tau-index length and common q support across ref/f2/f3/f4.

For each q and bin b define `delta_b(case)=S_b(case)-S_b(ref)`. Define the f3-specific bin power `W_b(q)=max(delta_b(f3)^2-max(delta_b(f2)^2,delta_b(f4)^2),0)`. Define total f3-specific transfer power `W_T(q)` exactly as in the edge absolute-sufficiency audit from the reconstructed full transfer. Aggregate without post-hoc weights: `F_b=sum_q W_b(q)/sum_q W_T(q)`. Also report signed closure `sum_b delta_b(case)` against the no-edge transfer difference.

## Frozen classification
Integrity failure, non-positive total excess, or signed closure relative error >1e-10 -> `M21_L400_ACCUMULATION_WINDOW_LOCALIZATION_BLOCKED`.

Otherwise let `Fmax=max_b F_b` and `bmax` be its unique first maximum under fixed bin order. If `Fmax >= 0.5`, classify `M21_L400_ACCUMULATION_WINDOW_CONCENTRATED_WITH_SCOPE`; otherwise classify `M21_L400_ACCUMULATION_WINDOW_DISTRIBUTED_WITH_SCOPE`.

The 0.5 threshold is a prospective dominance criterion: one predeclared tenth of the reference absolute accumulation budget must account for at least half of the total f3-specific transfer-excess power. It is not a fit tolerance. Report all ten bins regardless of outcome.

## Interpretation guardrails
This is solver-layer localization only. It cannot promote K1/K3/K4, cannot establish physical falsification, and cannot by itself claim a CLASS defect. A concentrated result authorizes a narrower within-bin factor/phase diagnostic using prospectively fixed sub-bins; a distributed result authorizes a summation-arithmetic/phase-stability audit rather than visually selected tau windows.