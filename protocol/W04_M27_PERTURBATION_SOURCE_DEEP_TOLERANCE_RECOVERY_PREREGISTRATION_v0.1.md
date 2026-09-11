# W04 M27 perturbation-source deep-tolerance recovery preregistration v0.1

## Trigger

The normalized conditioning audit established the N=1 exact-vs-direct reference at the original D04 support for all `Gamma0/H*={0.03,0.3,3}` and all `k/H*={0.1,1,10}`. It failed only the prospectively frozen solver-convergence gate: the `rtol=1e-10` versus `1e-11` pair exceeded `1e-6` in exactly one reported block, `Gamma0/H*=0.3`, `k/H*=0.1`, daughter velocity, at `1.0136580721e-6`. No threshold is changed.

This recovery asks whether that marginal miss is a solver-tolerance floor by going one decade deeper. It changes no physical parameter, equation, support, k-grid, source prescription, or acceptance threshold.

## Frozen computation

For each independent `Gamma0/H*={0.03,0.3,3}` job, use the normalized N=1 exact formulation from the conditioning audit at the original D04 support and solve all `k/H*={0.1,1,10}` at:

- `rtol=1e-11`, `atol=1e-14`;
- `rtol=3e-12`, `atol=3e-15`;
- `rtol=1e-12`, `atol=1e-15`.

The same DOP853 solver, background solution, metric forcing and D04 start boundary are retained.

## Frozen gates

For every Gamma and k record amplitude-normalized maximum differences in normalized daughter density and velocity for:

- pair A: `1e-11` vs `3e-12`;
- pair B: `3e-12` vs `1e-12`.

A block passes iff both variables are <=`1e-6` for both pairs. All trajectories must be finite.

Aggregate classification is `M27_PERTURBATION_SOURCE_DEEP_TOLERANCE_RECOVERY_PASS_WITH_SCOPE` iff all 3 Gamma x 3 k blocks pass and all trajectories are finite.

A pass authorizes a new normalized-state 27-way production recovery using `rtol=1e-11` and the original D04 support. It does not rewrite or reclassify the failed original raw-amplitude run; provenance must preserve both.

`K1_promoted=false`, `K3_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.
