# W03 M14 K2-K5 local `cdm_c` response preregistration v0.1

Date frozen: 2026-09-10
Provider: `kabeleh/iDM@dc55e59dec8f5c647df6e9d764f5c6960796e1df`
Author anchor: `benchmark/gcc/tmp_ini/pgo_hyperbolic_cmb.ini`

## Scope

This gate tests only the field-dependent CDM-mass coupling axis `cdm_c` with the separate q-sector held at `q1=q2=q3=q4=0` and coupling exponents unchanged at zero. It does not yet attack M02 or any full comparator manifold and cannot authorize K6-K9.

## K2 geometry frozen before execution

Source defines

`m_CDM(phi) = m0/2 * [1 - tanh(cdm_c * phi)]`.

At the selected author hyperbolic scalar anchor, source documentation defines

`V(phi) = c1 * [1 - tanh(c2 * phi)]`,

with `c2=0.98` in the tracked workload. Consequently `phi -> -phi` alone is not a symmetry of the frozen scalar potential, so the sign of `cdm_c` cannot be quotiented away as `cdm_c^2` on this anchor. The provider's inference generator also samples signed `cdm_c` across zero. Therefore the local physical coordinate is frozen as the two-sided signed coordinate

`c := cdm_c in R`, reference `c=0`.

The q-sector is a distinct interaction-law axis and is not mixed into this coordinate.

## Frozen cases

Starting from the exact tracked author workload, modify only:
- output root (plumbing),
- `write_background = yes` (diagnostic output only),
- `cdm_c` to one of `0`, `+0.01`, `-0.01`, `+0.02`, `-0.02`.

No other cosmological, scalar, q-sector, numerical, gauge or nonlinear setting may change.

The step `0.01` is author-supported by the provider regression suite's `idm_weak` case; `0.02` is a prospectively frozen factor-two convergence step.

## Response vector

Use common solver-native outputs only:
1. background H channel: `ln H(z)` on matched background rows;
2. matter-power channel: `ln P(k,z)` on matched generated P(k) rows/files.

Undefined/non-positive entries are masked, never zero-imputed. Each channel is internally normalized by using logarithmic responses; concatenate available H and P components only after exact row/k matching.

For `h in {0.01,0.02}`, central tangent:

`v_h = [O(+h)-O(-h)]/(2h)`.

Also record one-sided finite responses against `c=0` to detect asymmetric/nonlinear behavior.

## Frozen K4 criteria

K4 local step convergence passes with scope only if all five solver cases execute and:
- tangent relative norm mismatch `||v_.01-v_.02|| / max(||v_.01||,||v_.02||) <= 0.10`;
- tangent direction angle `<= 3 deg`.

If a case fails numerically, classify implementation/numerical blocker, not physics failure. Thresholds are not to be relaxed after execution.

## Frozen K5 criteria

A non-null local `cdm_c` response is established with scope only if K4 passes and at least one channel has maximum absolute log response at `|c|=0.01` greater than `1e-5`, safely above the K1 reference-regression floors (`~1e-8` background and `~1e-6` P(k) relative).

Report channel norms and the combined tangent rank. With one physical coordinate, expected local rank is at most one; parameter count is not inferred from output dimensionality.

## Interpretation limits

PASS means only that this provider/anchor has a source-bound signed coupling coordinate with a numerically converged non-null multichannel local response. It is not observational discrimination, does not establish novelty versus M02/CPL/MG, and does not imply physical viability over the wider parameter space. K3 source/conservation closure and K6-K9 remain separate gates.
