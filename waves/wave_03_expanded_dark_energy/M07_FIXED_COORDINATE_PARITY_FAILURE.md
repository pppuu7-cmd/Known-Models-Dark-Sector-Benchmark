# M07 fixed-coordinate lambda-parity audit

Date: 2026-09-09  
Actions run: `34358465646`  
Artifact: `w03-m07-parity-coordinate-audit`  
Artifact digest: `sha256:807e935cfa758df81c251531a672c829f430ab41a44e3219fe67a0fbbbe6cb40`  
Status: **FAIL_WITH_INTERPRETATION — frozen parity gate fails on the fixed `phi_ini=+1` coordinate branch; this is not yet a failure of the field-reflection quotient symmetry.**

## Frozen question

The strict production norms suggested approximately quadratic scaling with `lambda`. A preregistered test therefore asked whether, while keeping all other branch coordinates fixed,

`r(+lambda) ~= r(-lambda)`

with hard gate

`||r_odd|| / ||r_even|| <= 1e-3`.

Common block: strict-shooting, unwhitened 7x5 low-k `r_Delta(k,z)` response.

## Results

| abs(lambda) | lnP odd/even | lnH odd/even | plus/minus lnP angle | hard parity gate |
|---:|---:|---:|---:|---|
| 0.025 | `7.4666e-3` | `8.5235e-6` | `0.78187 deg` | FAIL |
| 0.075 | `2.0277e-3` | `2.0187e-8` | `0.214997 deg` | FAIL |

Both frozen lnP parity gates fail. The workflow failure is therefore a scientific test failure within its stated fixed-coordinate scope, not an infrastructure failure.

The descriptive `r/lambda^2` comparison also does not yet show converged local geometry: the two q-scaled response vectors differ by relative norm `0.2177` and angle `12.475 deg`; no threshold had been preregistered for this diagnostic, so no pass/fail is assigned to q-convergence.

## Why this does not settle the physical quotient coordinate

The tested branch held `phi_ini=+1` fixed while sending `lambda -> -lambda`.

For the canonical pure-exponential subset

`V(phi)=(1+A) exp(-lambda phi)`

with `B=0`, the exact field-reflection map is instead

`(lambda, phi) -> (-lambda, -phi)`

with the canonical kinetic term unchanged. Therefore the fixed-coordinate parity test is not the same question as parity after quotienting an exact field-coordinate reflection.

A second preregistered audit, `.github/workflows/w03-m07-field-reflection-quotient-audit.yml`, tests the paired branches

`(+lambda, phi_ini=+1)` versus `(-lambda, phi_ini=-1)`

using the same strict shooting and common response block. Its hard odd-fraction threshold is frozen at `1e-6` before execution.

## Methodological consequence

Local-coordinate discovery must occur **after quotienting exact parameter/field redundancies**. A failed symmetry test in an unreduced coordinate chart cannot by itself establish that the physical model manifold lacks the corresponding quotient symmetry.

Do not retrospectively loosen the failed `1e-3` threshold. Preserve this result as evidence that coordinate-chart parity and physical quotient parity are different tests.
