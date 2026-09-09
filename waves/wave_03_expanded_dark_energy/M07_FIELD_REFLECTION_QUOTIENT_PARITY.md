# M07 field-reflection quotient parity audit

Date: 2026-09-09  
Actions run: `34359042959`  
Artifact: `w03-m07-field-reflection-quotient-parity`  
Artifact digest: `sha256:d5e747fc54aee3a8fe3c50372f5788d6c95bcddc47b3598cf1646d114ff041b1`  
Status: **PASS_WITH_SCOPE**

## Frozen quotient map

For the alpha-zero canonical exponential branch with `B=0`, test the exact field-reflection pair

`(+lambda, +phi_ini, phi_prime_ini=0)`

against

`(-lambda, -phi_ini, phi_prime_ini=0)`.

The kinetic term is unchanged and the product `lambda*phi` is invariant, so this is the appropriate exact field-coordinate reflection to quotient before local-coordinate inference.

Hard preregistered gate for both `lnP` and `lnH` odd fractions:

`||r_odd||/||r_even|| <= 1e-6`.

## Results

| abs(lambda) | lnP odd/even | lnH odd/even | lnP angle | result |
|---:|---:|---:|---:|---|
| 0.025 | `0` | `0` | `0 deg` | PASS |
| 0.075 | `0` | `0` | `0 deg` | PASS |

The paired background histories also match under field reflection: `phi(z)` and `phi_prime(z)` flip sign while `H(z)`, `w_scf(z)`, `Omega_scf(today)` and matter response remain identical.

## Interpretation

The previous fixed-chart parity failure is real but coordinate-specific. After quotienting the exact field reflection, the response is exactly even in the sign of `lambda` at the tested points.

Therefore sign(`lambda`) is not an independent physical response direction in this frozen M07 branch. The local physical coordinate may be expressed through a nonnegative invariant such as `q=lambda^2`, but **linearity in q is a separate question** and is not established by parity alone.

The q-scaled low-k matter vectors at abs(lambda)=0.025 and 0.075 still differ by relative norm `0.21849` and angle `12.5058 deg`. This diagnostic had no preregistered convergence threshold and remains descriptive. In contrast, the q-scaled H response is already much more stable, motivating a dedicated perturbation-precision q-convergence audit.

## Methodological consequence

Exact redundancies must be quotiented before:
- assigning physical parameter count;
- constructing Jacobians/ranks;
- inferring odd/even derivative order;
- declaring a natural local coordinate.

Parity of a coordinate chart is not automatically parity of the physical quotient manifold.
