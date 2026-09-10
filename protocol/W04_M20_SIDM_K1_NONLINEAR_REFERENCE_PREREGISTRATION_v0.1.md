# W04 M20 SIDM nonlinear K1 reference-limit preregistration v0.1

## Question
Does the pinned SASHIMI-SIDM nonlinear halo/subhalo response approach the simultaneously defined CDM boundary continuously as the interaction cross section tends to zero?

This is an M20 K1 reference-limit test in nonlinear response space. It does not establish observational distinguishability, unique attribution against other small-scale-suppression/core-forming families, or a full cosmological linear-perturbation closure.

## Provider
`shinichiroando/sashimi-si@e17d3664dac677b604fd4ff02fb2af105a6937fa`

The preceding provider-control run `34538139137` established that the upstream physics suite passes and that an exact `sigma0_m=0` execution returns finite physical catalog outputs with exact SIDM=CDM identity for Vmax, rmax, rs and rhos and exactly zero core radius on 615 retained entries. This preregistration does not modify that provider.

## Frozen interaction realization
Use the velocity-dependent Rutherford-like realization already exposed by the provider with

- `w = 24.33 km/s`;
- cross-section normalization `sigma0_m` in `cm^2/g`.

Run the exact reference `sigma0_m = 0` plus the finite ladder

`sigma0_m = {10, 3, 1, 0.3, 0.1} cm^2/g`.

No ladder point may be removed or replaced after execution.

## Frozen catalog
Use the reduced deterministic end-to-end catalog geometry inherited from the upstream physics regression and the exact-zero provider control:

- `M0 = 1e12 Msun`;
- `redshift = 0`;
- `M0_at_redshift = True`;
- `dz = 0.2`;
- `N_herm = 3`;
- `zmax = 4`;
- `logmamin = 9`;
- `N_ma = 30`;
- all other provider defaults unchanged.

The retained comparison support is the exact-zero reference set with finite positive `weightCDM`. Finite cases must have the same array shapes. No case-specific support trimming is allowed except exclusion of entries non-finite in either member of a compared pair, which automatically fails the finite-output requirement.

## K1-gated continuous nonlinear blocks
For each finite sigma compare the SIDM output to the exact-zero reference CDM output in:

1. `Vmax_z0`: `VmaxSIDM_z0` versus reference `VmaxCDM_z0`;
2. `rmax_z0`: `rmaxSIDM_z0` versus reference `rmaxCDM_z0`;
3. `rs_z0`: `rsSIDM_z0` versus reference `rsCDM_z0`;
4. `rhos_z0`: `rhosSIDM_z0` versus reference `rhosCDM_z0`;
5. `core_ratio`: `|rcSIDM_z0| / |rsCDM_z0|`, whose exact-CDM reference is zero.

For the four structural pairs use the pointwise symmetric relative residual

`r = 2 (X_sidm-X_cdm) / (|X_sidm|+|X_cdm|+floor)`

with `floor=1e-14*max(|X_sidm|,|X_cdm|)` per block/case. Report median absolute, RMS and p95 absolute residual.

For `core_ratio` report median, RMS, p95 and maximum of the positive dimensionless ratio.

## Frozen K1 convergence gate
Each of the five continuous blocks passes only if:

1. all retained physical outputs are finite for every finite sigma;
2. p95 response is non-increasing at every consecutive reduction in sigma, with 2% relative numerical slack;
3. p95 at sigma=0.1 is lower than at sigma=10;
4. a log-log fit to the three smallest finite points `{1,0.3,0.1}` has positive exponent `p > 0.5` when all three p95 values are positive;
5. the exact-zero provider-control identity remains exact within `1e-10` for the structural pairs and `core_ratio <= 1e-10`.

Overall K1 classification is

`M20_K1_NONLINEAR_REFERENCE_LIMIT_PASS_WITH_SCOPE`

only if all five continuous blocks pass.

Otherwise use

`M20_K1_NONLINEAR_REFERENCE_LIMIT_NOT_ESTABLISHED`

and preserve failing blocks. Failure is not automatically physical falsification; numerical/provider causes must be separated first.

## Population diagnostics — explicitly not K1-gated
For each finite sigma also report:

- p95 and maximum symmetric relative residual of `weightSIDM` versus reference `weightCDM` on the reference-positive support;
- fraction of entries where `surviveSIDM` differs from reference `surviveCDM`.

These are threshold/discrete population responses and are not required to exhibit a differentiable power-law approach. They cannot overturn a continuous-block K1 result but must be retained for later nonlinear attribution and observation-space design.

## K2 geometry
If K1 passes, record K2 only as

`ONE_SIDED_SIGMA_GE_0_NO_SIGN_QUOTIENT`.

Negative scattering cross section is outside the physical parameter domain.

## Guardrails
- Do not infer K4 from a single ladder; a separate step-size/numerical-robustness gate is required.
- Do not infer K6 against WDM/FDM/baryonic-core alternatives from this test.
- Do not infer K7 observational significance.
- Do not claim SIDM is favored or falsified.
