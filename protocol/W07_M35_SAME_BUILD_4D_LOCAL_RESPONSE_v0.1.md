# W07 M35 same-build 4D local observable-response preregistration v0.1

Date: 2026-09-12
Provider: `Michalychforever/CLASS_LVDM@d9a20bd0c7b7a6c8957410fd245ed06b30b915c1`
Purpose: eliminate cross-run/base reproducibility ambiguity by computing the established gravity-ray and Y_dm directions together with beta and lambda coordinate probes in one pinned provider build and one output environment.

## Frozen base
`(alpha,beta,lambda,Y_dm)=(0.005,0.025,-0.01,0)`.

## Frozen central stencils
- gravity ray q around q0=0.1 on `(alpha,beta,lambda)=(0.05q,0.25q,-0.10q)`: coarse dq=0.002, fine dq=0.001;
- Y_dm: coarse dY=0.002, fine dY=0.001;
- beta only: coarse dbeta=0.0005, fine dbeta=0.00025;
- lambda only: coarse dlambda=0.0002, fine dlambda=0.0001.

All plus/minus arms and the base are executed in the same job after one exact provider build. No post-hoc step change is authorized.

## Frozen response and convergence rule
Use one common CMB ell support and one common P(k) interval across all 17 arms. Normalize CMB and P(k) derivative blocks by the same base L2 norms and concatenate them. For each direction independently, coarse/fine central derivatives converge only if principal angle <=5 degrees AND relative norm mismatch <=0.25.

Only converged fine derivatives are eligible for local response-rank analysis. Compute SVD of the matrix whose columns are the eligible normalized fine derivatives. Numerical rank uses `max(shape)*eps*sigma_max`. Also report pairwise angles and each candidate's angle to the span of earlier eligible columns in the fixed order `[gravity,Y_dm,beta,lambda]`.

## Interpretation lock
A local rank >=3 or rank 4 is stronger scoped observable-response evidence, but it does not close full covariant scalar/vector/tensor Einstein-Aether geometry, field-redefinition equivalences, or quotient structure. Therefore this workflow cannot promote canonical K2 beyond PARTIAL.

Always set `K2_promoted=false`, `canonical_K2_remains=PARTIAL`, `physical_falsification=false`, `full_Einstein_Aether_SVT_claim=false`.