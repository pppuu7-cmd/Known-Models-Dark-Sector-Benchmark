# W04 M27 normalized 27-way perturbation-source production recovery preregistration v0.1

## Authorization

The deep-tolerance recovery completed with `normalized_27way_recovery_authorized=true`: all three N=1 Gamma controls pass the two frozen deep tolerance pairs, with aggregate maximum residual `2.628696869174808e-7 < 1e-6`. The machine-selected production settings are therefore fixed to `rtol=1e-11` and the original D04 support fraction `1e-4`.

This production run preserves the failed raw-amplitude perturbation-source run as provenance. It does not weaken any old threshold; it uses the prospectively authorized normalized-state formulation.

## Frozen grid and equations

Use all 27 original DDM rays: delta={0.5,1,2}, y={1,2,3}, Gamma0/H*={0.03,0.3,3}, N=64, and k/H*={0.1,1,10}.

Use the exact same background ensemble, synchronous-comoving metric forcing and sigma=0 daughter fluid-source equations as the first perturbation-source probe, but integrate normalized O(1) variables `dhat=delta_dr/A_h`, `that=theta/A_h` directly.

For each ray start at its D04 daughter-comoving-energy support and compute each k at both:

- production: rtol=1e-11, atol=1e-14;
- verification: rtol=1e-12, atol=1e-15.

## Frozen gates

Each ray passes iff:

1. component source identity amplitude-normalized residual <=1e-12;
2. production-vs-verification normalized response residual <=1e-6 in both dhat and that for all three k;
3. all trajectories are finite;
4. the independent N=1 deep-tolerance authorization remains present in canonical repository state.

For response geometry, also compute the production normalized response of the moment-matched single-lifetime comparator with `Gamma_eff=sum w_i Gamma_i` and record normalized L2 distances in dhat/that for each k. Comparator distance is descriptive and not a pass/fail threshold.

## Classification

A ray passing all gates is `M27_DDM_PERTURBATION_SOURCE_CLOSURE_PASS_WITH_NORMALIZED_FLUID_SCOPE`. Aggregate 27/27 gives `M27_DDM_27_BRANCH_PERTURBATION_SOURCE_CLOSURE_PASS_WITH_NORMALIZED_FLUID_SCOPE`.

Even aggregate pass remains a sigma=0 source/continuity closure only. Dark-radiation shear/higher multipoles, full gauge robustness, Boltzmann observable mapping, K3/K4 promotion and likelihood remain open.

`K1_promoted=false`, `K3_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.
