# M07 field-reflection quotient audit — result

Date: 2026-09-09  
Status: **PASS**  
Run: `34359050388`  
Artifact: `w03-m07-field-reflection-audit`  
Artifact digest: `sha256:42668e816a2d14293043250eea85f3b6561f5fedaf4a2c70a01ab5569bb68c82`.

## Frozen question

The raw parity audit at fixed `phi_ini=+1` rejected the naive statement `r(+lambda)=r(-lambda)`. That test did not quotient the exact field-coordinate reflection of the pure-exponential scalar branch.

This audit instead compares the physically reflected pairs

`(+lambda, phi_ini=+1)`

and

`(-lambda, phi_ini=-1)`

with zero initial field velocity, identical strict shooting, identical target density and the same frozen 7x5 low-k response grid.

Preregistered hard gate:

- `lnP odd_fraction <= 1e-4`;
- `lnH odd_fraction <= 1e-4`.

## Results

| abs(lambda) | Omega plus | Omega reflected-minus | lnP odd fraction | lnH odd fraction | max abs ΔlnP | max abs ΔlnH | gate |
|---:|---:|---:|---:|---:|---:|---:|---|
| 0.025 | 0.6826869808187135 | 0.6826869808187135 | 0 | 0 | 0 | 0 | PASS |
| 0.075 | 0.6826869550524842 | 0.6826869550524842 | 0 | 0 | 0 | 0 | PASS |

The two reflected branches are identical to the stored numerical precision in both background and low-k matter response.

## Interpretation

For the frozen M07 pure-exponential branch, the transformation

`(lambda, phi, phi_prime, delta_phi) -> (-lambda, -phi, -phi_prime, -delta_phi)`

is a genuine field-coordinate redundancy for the tested observables. The sign of `lambda` is therefore not a distinct physical branch in this benchmark scope.

The physical local parameter space must first be quotiented by this reflection. A convenient representative is `lambda >= 0`.

This PASS does **not** by itself prove that the correct smooth local coordinate is `q=lambda^2`. It only removes the duplicated sign branch. The leading response order near the reference still has to be measured above the solver/reference floor.

## Relation to the failed raw parity audit

The prior run `34358465646` intentionally kept `phi_ini=+1` for both signs and failed its preregistered parity threshold. That result remains valid as a coordinate-warning control. It is not deleted or rewritten.

The quotient-aware PASS explains why raw parameter parity was the wrong physical equivalence test.

## Methodology consequence

Exact field redefinitions must be quotiented **before**:
- local Jacobian construction;
- rank/identifiability claims;
- parity tests;
- choosing a local theory coordinate.

A parameter-sign difference that disappears under an exact field redefinition must never be counted as an independent model direction.

## Next hard task

Run a preregistered small-lambda order audit on the quotient representative `lambda >= 0` to determine whether the first nonzero response is linear, quadratic, or higher order. Only after that audit may the M07 local response coordinate/tangent be frozen.
