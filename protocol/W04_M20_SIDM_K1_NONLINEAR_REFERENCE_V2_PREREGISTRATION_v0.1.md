# W04 M20 SIDM nonlinear K1 reference v2 preregistration v0.1

## Motivation
The frozen v1 ladder is preserved as `M20_K1_NONLINEAR_REFERENCE_LIMIT_NOT_ESTABLISHED`. A post-run source audit showed that its universal `p>0.5` requirement is not a valid generic continuity criterion: the pinned SASHIMI-SIDM source has `rc/rs0 = 2.555 sqrt(tt) + O(tt)` and `tt ∝ sigma0_m` near the CDM boundary, so the physical core response is expected to approach zero with leading exponent 1/2.

V2 therefore tests K1 as a reference-limit/continuity gate and leaves differentiability/tangent regularity to later gates. V2 does not overwrite or reinterpret the v1 result.

## Provider, physics and catalog — unchanged
Provider:
`shinichiroando/sashimi-si@e17d3664dac677b604fd4ff02fb2af105a6937fa`

Interaction:
- `w = 24.33 km/s`;
- `sigma0_m` in `cm^2/g`.

Exact reference:
- `sigma0_m = 0`.

Catalog:
- `M0 = 1e12 Msun`;
- `redshift=0`;
- `M0_at_redshift=True`;
- `dz=0.2`;
- `N_herm=3`;
- `zmax=4`;
- `logmamin=9`;
- `N_ma=30`;
- all other provider defaults unchanged.

Reference support remains the exact-zero entries with finite positive `weightCDM`.

## Frozen v2 ladder
Retain every v1 point and append a smaller tail:

`sigma0_m = {10, 3, 1, 0.3, 0.1, 0.03, 0.01, 0.003} cm^2/g`.

No point may be removed after execution.

## Gated continuous blocks — unchanged
- `Vmax_z0`;
- `rmax_z0`;
- `rs_z0`;
- `rhos_z0`;
- `core_ratio = |rcSIDM_z0|/|rsCDM_z0|`.

Use the same symmetric relative residual for the four structural pairs and the same direct positive ratio for the core as in v1. Report median, RMS, p95, and maximum.

Population weight and survival responses remain diagnostic only.

## Corrected K1 continuity gate
A continuous block passes K1-v2 only if all are true:

1. all retained physical outputs are finite for every ladder point;
2. p95 deviation is non-increasing at every consecutive decrease in sigma, allowing 2% relative numerical slack;
3. the smallest finite point has lower p95 deviation than the largest finite point;
4. a log-log fit over the four smallest points `{0.1,0.03,0.01,0.003}` has a strictly positive exponent `p>0` when all values are positive;
5. the smallest finite p95 deviation is at most one quarter of the p95 deviation at `sigma0_m=1`, ensuring that the appended tail materially advances toward the exact boundary rather than merely fluctuating around a numerical floor;
6. the exact-zero structural identity remains within `1e-10` and exact-zero core ratio remains `<=1e-10`.

### Source-level core asymptote check
Because the provider source explicitly predicts a leading square-root core response, `core_ratio` has an additional diagnostic/source-consistency check:

- its four-smallest-points exponent must lie in `0.25 <= p <= 0.75`.

Failure of this source-consistency check blocks K1-v2 even if the generic continuity conditions pass, because it would indicate that the chosen tail has not reached behavior compatible with the provider's own zero-boundary equation.

No universal exponent interval is imposed on the other structural channels.

## Classification
Overall PASS only if every continuous block passes:

`M20_K1_V2_NONLINEAR_REFERENCE_LIMIT_PASS_WITH_SCOPE`

K1 value on PASS:

`PASS_WITH_SCOPE_NONLINEAR_HALO_EXACT_CDM_LIMIT`

Otherwise:

`M20_K1_V2_NONLINEAR_REFERENCE_LIMIT_NOT_ESTABLISHED`.

## K2
On K1 PASS only:
`ONE_SIDED_SIGMA_GE_0_NO_SIGN_QUOTIENT`.

## Guardrails
- V1 remains part of the audit trail.
- K1-v2 establishes continuity only; it does not establish a differentiable tangent at sigma=0.
- No K4 numerical-robustness promotion.
- No K6 attribution against WDM/FDM/baryonic alternatives.
- No K7 observational claim.
- No SIDM preference/falsification claim.
