# W04 M20 / F20 SIDM K2 — finite-base sigma0/m × w local response geometry preregistration v0.1

## Question
The pinned SASHIMI-SIDM interaction uses both an amplitude `sigma0_m` and a velocity scale `w`; provider source implements a velocity-dependent cross section proportional to `sigma0_m*w^4/(w^2+...)^2`. At the exact CDM boundary `sigma0_m=0`, `w` is unidentifiable, so the established K1 tangent cone remains one-sided in sigma. This diagnostic asks a different prospective question: **away from the null boundary, does `w` generate a numerically stable response direction independent of the sigma-amplitude direction?**

No K2 or K5 promotion is authorized by this diagnostic alone.

## Frozen provider / numerical profile
- provider `shinichiroando/sashimi-si`
- commit `e17d3664dac677b604fd4ff02fb2af105a6937fa`
- host `M0=1e12`, redshift 0, `M0_at_redshift=True`, `zmax=4`, `logmamin=9`
- numerics fixed in the previously weighted-converged regime: `N_herm=25`, `N_ma=120`, `dz=0.05`
- base physical point: `sigma0_m=0.1 cm^2/g`, `w=24.33 km/s`

## Frozen perturbations
Use central multiplicative steps in log-parameters:
- coarse `h=0.10`
- fine `h=0.05`
For each h independently evaluate `sigma0_m * exp(±h)` at fixed w and `w * exp(±h)` at fixed sigma0_m.

## Frozen response vector
Compute one exact-CDM reference at sigma0_m=0 with the same numerical profile. Use its finite positive `weightCDM` as the normalized reference population measure.
For each finite parameter point form a 5-vector of reference-weighted p95 structural response summaries relative to CDM:
`[Vmax_z0, rmax_z0, rs_z0, rhos_z0, core_ratio]`, using the same absolute symmetric node response / core definition as the weighted K4 protocols.
All five entries must be finite and strictly positive. Geometry is evaluated in log-response space.

For parameter q in {ln sigma, ln w}, define the central derivative vector `(log R(q+h)-log R(q-h))/(2h)` for coarse and fine h.

## Frozen tangent-convergence gate
Each parameter direction converges iff:
- signed cosine(coarse,fine) >= 0.995;
- relative norm mismatch <= 0.10;
- both derivative norms > 1e-6.

## Frozen local-independence gate
Using the two **fine** derivative vectors:
- principal angle >= 10 degrees;
- after normalizing each column to unit norm, singular-value ratio `s2/s1 >= 0.08`.

## Classifications
- all integrity + both tangent-convergence gates + independence gate -> `M20_K2_FINITE_BASE_LOCAL_RANK2_SIGMA_W_DIAGNOSTIC`.
- integrity + tangent convergence but independence fails -> `M20_K2_FINITE_BASE_SIGMA_W_LOCAL_DEGENERACY_DIAGNOSTIC`.
- integrity but either tangent does not converge -> `M20_K2_FINITE_BASE_SIGMA_W_TANGENT_NOT_CONVERGED_DIAGNOSTIC`.
- provider/nonfinite/shape/positive-response failure -> `M20_K2_FINITE_BASE_SIGMA_W_EXECUTION_OR_INTEGRITY_BLOCKED`.

Every outcome keeps `K2_promoted=false`, `K5_promoted=false`, `scientific_fail=false`, `physical_falsification=false`. Even rank-2 finite-base evidence does not remove the exact-null quotient/unidentifiability of w.
