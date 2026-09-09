# M07 raw-lambda parity / local-coordinate audit — result

Date: 2026-09-09  
Status: **FAIL_WITH_INFORMATION / RAW COORDINATE PARITY REJECTED**  
Run: `34358465646`  
Artifact: `w03-m07-parity-coordinate-audit`  
Artifact digest: `sha256:807e935cfa758df81c251531a672c829f430ab41a44e3219fe67a0fbbbe6cb40`.

## Frozen question

The production response approximately scaled as `lambda^2`. Before declaring `q=lambda^2` to be the near-reference coordinate, W03 preregistered a direct parity test using the same strict shooting realization and the same frozen cosmology.

Pairs tested with the same `phi_ini=+1`:
- `lambda=+/-0.025`;
- `lambda=+/-0.075`.

Hard parity criterion, frozen before the negative-lambda runs:

`||r_odd|| / ||r_even|| <= 1e-3`,

where

`r_even = [r(+lambda)+r(-lambda)]/2`

`r_odd  = [r(+lambda)-r(-lambda)]/2`.

No hard convergence threshold for `r/lambda^2` was preregistered.

## Results

| abs(lambda) | lnP plus/minus angle | lnP odd fraction | lnH odd fraction | frozen parity gate |
|---:|---:|---:|---:|---|
| 0.025 | `0.781868 deg` | `7.4666e-3` | `8.5235e-6` | FAIL |
| 0.075 | `0.214997 deg` | `2.0277e-3` | `2.0187e-8` | FAIL |

Both scalar-density targets remain extremely well matched between signs, and `w_scf(today)` agrees to better than the displayed precision. The parity failure therefore resides primarily in the low-k matter perturbation response, not in the background expansion.

The q-scaled even response comparison between abs(lambda)=0.025 and 0.075 is descriptive only:
- relative difference `0.217714`;
- angle `12.4750 deg`.

## Interpretation

The simple statement

> `r(+lambda)=r(-lambda)` at fixed `phi_ini=+1`, therefore q=lambda^2 is the exact local coordinate

is rejected at the preregistered `1e-3` level.

This does **not** establish that the sign of lambda is a physical observable. For the pure exponential potential

`V=(1+A) exp(-lambda phi)`,

the field reflection

`lambda -> -lambda`, `phi -> -phi`, `delta_phi -> -delta_phi`

leaves the scalar action/background stress invariant after the normalization nuisance is matched. The raw parity test kept `phi_ini=+1` on both branches and therefore did not quotient this field-coordinate redundancy.

The next hard test is consequently a **quotient-aware field-reflection audit** comparing

`(+lambda, phi_ini=+1)`

with

`(-lambda, phi_ini=-1)`

under the same strict target and response grid.

## Methodology consequence

Raw parameter parity is not sufficient to identify the physical local coordinate when a field redefinition maps nominally different parameter signs into the same theory.

Before Jacobian/rank construction, model parameter space must be quotiented by exact field-coordinate redundancies. Only then may the surviving coordinate be tested for first-order versus higher-order response.

## Anti-overclaim

- This FAIL is not a physical failure of canonical quintessence.
- It is not evidence that lambda sign is observable.
- It is not permission to declare q=lambda^2 after the fact.
- It creates a new mandatory quotient-aware audit before the M07 tangent is frozen.
