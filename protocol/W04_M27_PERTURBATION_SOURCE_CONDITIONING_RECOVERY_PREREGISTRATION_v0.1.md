# W04 M27 perturbation-source conditioning recovery preregistration v0.1

## Trigger

The first 27-way perturbation-source probe completed without execution failures. Component source identity is excellent (aggregate max residual ~4.9e-16) and all solutions are finite, but every ray fails the original aggregate gate because:

- the N=1 exact-vs-direct daughter velocity response can reach a few times 1e-5 while the frozen threshold is 1e-5;
- the two-amplitude linearity comparison is worst at low k, at roughly 1e-4 to 1e-3 amplitude-normalized residual in some rays.

The fluid perturbation system is mathematically linear in the prescribed metric forcing. Integrating raw states of order 1e-5 with a fixed absolute ODE tolerance can therefore create a conditioning floor. This audit changes only numerical state normalization/evaluation support; no DDM physics, background solution, source equation, k-grid or acceptance threshold is retuned.

## Frozen normalized formulation

Define normalized variables `dhat=delta_dr/A_h`, `that=theta/A_h`, and normalized metric forcing `hhat=h/A_h`. Integrate the same sigma=0 fluid-source equations directly in these O(1) variables. The forcing amplitude then cancels analytically.

Run the N=1 reference only for `Gamma0/H*={0.03,0.3,3}`; delta/y are irrelevant at N=1. Probe `k/H*={0.1,1,10}`.

Start each trajectory at the original D04 boundary (`(D_exact+D_direct)>1e-4 Dmax`) with the same initial conditions. Do not restart trajectories at later supports.

## Prospectively frozen evaluation-support ladder

On each already-integrated trajectory evaluate exact-vs-direct residuals on nested supports

`f_D = {1e-4,3e-4,1e-3,3e-3,1e-2}`

defined by `(D_exact+D_direct) > f_D * Dmax`.

For each support and k record amplitude-normalized max residual in dhat and that. A support passes for a Gamma only if both variables are <=1e-5 at all three k. `first_common_support` is the smallest tested f_D at which all three Gamma values pass. The ladder is frozen before results and the threshold remains 1e-5.

## Solver convergence gate

For the normalized exact-N1 formulation, run DOP853 at `rtol={1e-9,1e-10,1e-11}` with `atol=rtol*1e-3`. Evaluate on the selected first-common support. The fine pair 1e-10 vs 1e-11 must have amplitude-normalized max difference <=1e-6 in both dhat and that for every Gamma and k.

## Classification

`M27_PERTURBATION_SOURCE_CONDITIONING_RECOVERY_PASS_WITH_SCOPE` iff:

- a first_common_support exists in the frozen ladder;
- all N=1 exact-vs-direct dhat/that residuals on that support are <=1e-5;
- the normalized fine solver pair passes <=1e-6 everywhere;
- all trajectories are finite.

A pass authorizes a separate normalized-state 27-way production recovery using exactly the machine-selected first_common_support. It does not by itself reclassify the original 27 artifacts.

`K1_promoted=false`, `K3_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.
