# W07 M35 robust local response-rank conditioning audit v0.1

Date: 2026-09-12
Purpose: distinguish algebraic/numerical SVD rank from geometrically robust local response rank using the immutable same-build artifact from run `34703069517`, artifact `10301610297`.

## Immutable prerequisite
The parent must report all four directions `gravity,Y_dm,beta,lambda` converged under the frozen <=5 degree / <=0.25 derivative rule. No provider rerun or step change is allowed.

## Frozen robust-rank rule
The already-established response span is `[gravity,Y_dm]`. It must have numerical rank 2. Use the previously frozen independence separator of 10 degrees from the earlier beta/lambda preregistration.

1. Compute each candidate (`beta`,`lambda`) principal angle to the established 2D gravity/Y span.
2. Candidates with angle <10 degrees do not count as a robust third local direction, even if the full response matrix is algebraically full rank.
3. If one or both candidates pass >=10 degrees, add the passing candidate with the larger angle first, then test the remaining candidate against the expanded span using the same 10-degree separator.
4. Report full singular values, ratios to sigma_max, condition number, algebraic numerical rank, and the resulting robust geometric rank.

## Interpretation lock
This audit cannot promote K2. Algebraic rank 4 with robust rank 2 or 3 indicates weak/near-degenerate extra directions, not a contradiction. Even robust rank 4 would remain scoped scalar-observable evidence and would not close full covariant SVT quotient/equivalence geometry.

Always set `K2_promoted=false`, `canonical_K2_remains=PARTIAL`, `physical_falsification=false`, `full_Einstein_Aether_SVT_claim=false`.