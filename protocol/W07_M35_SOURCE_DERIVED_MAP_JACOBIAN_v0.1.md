# W07 M35 source-derived map Jacobian preregistration v0.1

Date: 2026-09-12
Model: M35 pinned CLASS_LVDM scoped representation
Purpose: quantify the local rank of a frozen set of source-explicit derived combinations, without confusing source-map rank with observable rank or full Einstein-Aether quotient closure.

## Immutable prerequisite
Use source audit run `34702581954`, artifact `10301010746`, provider `d9a20bd0c7b7a6c8957410fd245ed06b30b915c1`.

## Frozen base and map
At the previously tested q=0.1 gravity point `(alpha,beta,lambda,Y)=(0.005,0.025,-0.01,0)`, define only combinations explicitly visible in pinned production source, dropping irrelevant positive constants:
- `G = 1/(1 + beta/2 + 3 lambda/2)`;
- `C = (beta+lambda)/alpha` (`c_sq_chi`);
- `B = (beta+3 lambda)/alpha`;
- `H = alpha^(-1/2)` (`H_alpha/H0`);
- `K = Y/[alpha*G*(1-Y)]` (proportional to `k_y_0_sq`).

Compute the exact analytic 5x4 Jacobian with respect to `(alpha,beta,lambda,Y)` at the frozen base, its singular values and numerical rank using tolerance `max(shape)*eps*sigma_max`.

## Interpretation lock
A local rank of 4 means only that these five source-derived combinations locally retain all four nominal input directions at this base. It does NOT establish four observable directions, full covariant SVT geometry, absence of field-redefinition equivalences, or K2 PASS.

Always set `K2_promoted=false`, `canonical_K2_remains=PARTIAL`, `physical_falsification=false`, `full_Einstein_Aether_SVT_claim=false`.