# M21 transfer-l sampling grid-geometry audit — 2026-09-14

Provider authority: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Purpose: outcome-independent source/geometry audit while `W04 M21 G2B l-sampling direction interaction audit v0.1` is non-terminal. No executed pair value, threshold, or classifier is changed.

## Exact grid construction

Exact `source/transfer.c::transfer_get_l_list()` starts at `l=2` and uses

`increment = max(int(l * (pow(l_logstep, angular_rescaling)-1)),1)`

while that logarithmic increment is below `l_linstep*angular_rescaling`. It then switches to the constant linear increment

`increment = l_linstep*angular_rescaling`

through `l_max`, with the final requested `l_max` included.

Exact thermodynamics/transfer structures document `angular_rescaling=1` for flat curvature `K=0`. The frozen M21 cosmology has `Omega_k=0`, hence the pair audit is an ordered flat-grid refinement.

## Frozen pair path

With `l_max_scalars=2500` and `angular_rescaling=1`, direct reproduction of the exact integer grid algorithm gives:

| profile | l_logstep | l_linstep | transfer-l nodes to 2500 | maximum linear step |
|---|---:|---:|---:|---:|
| exact default | 1.12 | 40 | 99 | 40 |
| LPAIR_I | 1.05 | 32 | 159 | 32 |
| LPAIR_R | 1.026 | 25 | 246 | 25 |
| LPAIR_T1 | 1.015 | 20 | 362 | 20 |
| LPAIR_T2 | 1.010 | 15 | 492 | 15 |

Thus `I -> R -> T1 -> T2` monotonically increases transfer-function multipole sampling density. `LPAIR_R` is already roughly 2.5 times the default node count and `LPAIR_T2` roughly 5 times the default node count for this scalar l-range.

The numerical pair workflow remains authoritative for whether the CMB excursion follows this refinement monotonically. This source/geometry audit only proves that the frozen direction corresponds to increasingly dense l sampling.

## Interpretation ceiling

This does not establish convergence, a CLASS defect, a production precision recommendation, or any physical property of mixed cold+warm dark matter. It does not promote K1/K3/K4 and cannot alter the frozen pair-audit classifications.
