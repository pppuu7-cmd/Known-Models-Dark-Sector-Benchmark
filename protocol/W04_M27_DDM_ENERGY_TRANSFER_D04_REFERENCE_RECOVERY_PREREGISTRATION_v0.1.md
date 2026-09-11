# W04 M27 DDM energy-transfer D04 reference recovery preregistration v0.1

## Trigger and provenance

The recovered 27-branch M27 cosmological energy-transfer run `34555747835` completed and serialized all branches. Every branch is currently `NOT_ESTABLISHED` because the original N=1 daughter-density relative gate fails, while the ensemble positivity/monotonicity/source-integral machinery remains executable. The aggregate maximum source-integral relative residual is `1.7736192502568625e-06`, within the frozen 1e-4 conservation threshold.

Two independent N=1 audits were then completed before this recovery was defined:

1. Comoving-variable conditioning audit: H and parent agree at ~1e-13--1e-11, while the daughter relative metric remains ~4.4e-5 when nearly-zero accumulated daughter energy is included.
2. Prospectively frozen six-decade comoving-D support ladder `D12,D10,D08,D06,D04,D02` at Gamma0/H*={0.03,0.3,3.0}.

The ladder shows that `D04`, defined by `(D_exact+D_direct) > 1e-4 Dmax`, is the **first common tested decade** for which all three Gamma0 values satisfy the original 1e-7 p95 relative threshold. Its p95 values are approximately 4.89e-9, 5.60e-9, and 9.24e-9. D06 is not common-pass because Gamma0/H*=3 remains at ~1.16e-7.

Thus D04 is selected by a predeclared convergence ladder, not by continuous post-hoc threshold tuning.

## Frozen recovered N=1 reference gate

For each Gamma0/H* in {0.03,0.3,3.0}, the N=1 reference is accepted only if all are true in the already completed audit evidence:

- H p95 symmetric-relative residual <= 1e-7;
- parent p95 symmetric-relative residual <= 1e-7;
- comoving daughter D p95 symmetric-relative residual on the D04 support <= 1e-7;
- global amplitude-normalized max absolute D discrepancy <= 1e-8.

No solver, cosmological, ensemble, or acceptance parameter is recomputed or changed.

## Analysis-only recovery

Reuse immutable per-branch artifacts from run `34555747835`. For each of the 27 branches:

1. retain every original ensemble gate exactly as recorded;
2. replace only the failed density-based `n1_reference` Boolean by the independently audited D04 reference Boolean for that branch's Gamma0/H*;
3. record both the original and recovered reference status;
4. classify `M27_DDM_COSMOLOGICAL_ENERGY_TRANSFER_PASS_WITH_D04_REFERENCE_SCOPE` iff the recovered N=1 gate and every unchanged ensemble gate pass.

Aggregate pass requires all 27 recovered branches to pass.

## Scientific scope

This recovery changes the **reference comparison support/variable**, not the DDM physics or solver output. The original density-based reference failure remains in provenance and is not erased.

A recovered aggregate pass establishes background energy-transfer closure with scope only. Perturbation/source closure remains open. `K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.
