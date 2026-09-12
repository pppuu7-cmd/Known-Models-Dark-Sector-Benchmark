# W07 M35 beta/lambda observable-response preregistration v0.1

Date: 2026-09-12
Provider: `Michalychforever/CLASS_LVDM@d9a20bd0c7b7a6c8957410fd245ed06b30b915c1`
Purpose: prospectively test whether source-independent gravity coordinates beta and lambda provide converged observable response directions beyond the already established local gravity-ray and Y_dm directions.

## Frozen base
`(alpha,beta,lambda,Y_dm)=(0.005,0.025,-0.01,0)`.

## Frozen central stencils
For beta, hold alpha/lambda/Y fixed and use:
- coarse beta delta = 0.0005 (2% of |beta|);
- fine beta delta = 0.00025 (1%).

For lambda, hold alpha/beta/Y fixed and use:
- coarse lambda delta = 0.0002 (2% of |lambda|);
- fine lambda delta = 0.0001 (1%).

These relative step fractions are frozen before execution. No post-hoc shrinking is authorized.

## Frozen criteria
Each axis derivative must satisfy coarse/fine principal angle <=5 degrees and relative norm mismatch <=0.25 on the same concatenated CMB+P(k) response definition used by the earlier M35 local Jacobian. Only a converged axis may be compared for independence. Independence separator is >=10 degrees relative to each immutable established direction (gravity ray and Y_dm) reconstructed from run `34668120323`, artifact `10290165068`.

A converged axis separated from both established directions is local additional-rank evidence only. It does not establish full covariant scalar/vector/tensor geometry, quotient/equivalence closure, or K2 PASS.

Always set `K2_promoted=false`, `canonical_K2_remains=PARTIAL`, `physical_falsification=false`, `full_Einstein_Aether_SVT_claim=false`.