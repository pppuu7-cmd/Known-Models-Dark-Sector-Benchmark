# M20 SIDM K1 v1 diagnostic audit — 2026-09-11

## Frozen v1 outcome
The prospectively frozen nonlinear K1 ladder returned `M20_K1_NONLINEAR_REFERENCE_LIMIT_NOT_ESTABLISHED`. The failure is narrow: every continuous block decreases monotonically toward the exact CDM boundary, but the frozen requirement `p>0.5` over the three smallest finite cross sections rejects `core_ratio` (p=0.44696), `rhos_z0` (p=0.45427), and `rmax_z0` (p=0.49275). `Vmax_z0` (p=0.99826) and `rs_z0` (p=0.52234) pass.

The exact-zero provider control remains exact: the pinned provider returns SIDM=CDM and zero core radius on the frozen reference support.

## Source-level interpretation of the exponent threshold
The provider implements the Yang et al. (2023) core-radius relation as

`rc/rs0 = 2.555*sqrt(tt) - 3.632*tt + 2.131*tt^2 - 1.415*tt^3 + 0.4683*tt^4`,

where `tt=(t-t_f)/t_c`. The effective cross section is linear in the normalization `sigma0_m` at fixed velocity parameter `w`, and the collapse time is inversely proportional to the effective cross section. Hence near the CDM boundary `tt ∝ sigma0_m` and the leading source-level core response is generically

`rc ∝ sqrt(sigma0_m)`.

Therefore a K1 rule that requires a convergence exponent strictly greater than 1/2 for every observable excludes the provider's own physically defined continuous reference limit in the core channel by construction. This is a **gate-semantics defect**, not a SIDM physical failure.

The structural density/radius relations are also nonlinear functions of `tt`, including logarithmic terms such as `log(tt+0.001)`, so a finite ladder need not be in the asymptotic linear-in-sigma regime even though the exact zero boundary is well defined and all responses decrease monotonically.

## Methodological lesson
K1 is a **reference-limit/continuity** gate. It must establish that a model approaches its reference boundary. It must not silently impose differentiability or a universal scaling exponent. Differentiability, tangent stability and step-size geometry belong to later numerical/geometry gates.

For K1, the appropriate generic requirements are:

- exact or independently validated reference boundary;
- finite source-complete execution;
- monotonic decay of the deviation along a prospectively frozen one-sided ladder;
- strictly positive convergence exponent when a power-law diagnostic is meaningful, not an arbitrary universal lower bound above zero;
- explicit preservation of known non-analytic source behavior rather than treating it as failure.

## Allowed v2
A v2 K1 test may be preregistered without overwriting v1. It should preserve the exact reference, provider pin, catalog, w, all original sigma points and response blocks, append a smaller tail, and change only the K1 exponent semantics from `p>0.5` to `p>0` because K1 tests continuity rather than differentiability. The core channel should additionally be checked for consistency with the source-predicted square-root approach rather than forced above it.

No K1 promotion is authorized by this audit alone.
