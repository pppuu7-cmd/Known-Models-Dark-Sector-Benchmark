# W07 M40 xi/lambda finer-resolution diagnostic v0.1

Date: 2026-09-12
Provider: `EFTCAMB/EFTCAMB@16d9c4e9f85751e30efd0a53b177941713078904`.

## Motivation
The prospectively symmetric xi/lambda coordinate test used coarse/fine deltas `2e-6/1e-6` on both remaining native Hořava axes. Both derivatives failed the frozen `<=5 deg` convergence criterion; lambda was near the boundary while xi was not. To avoid post-hoc axis selection, this diagnostic tests **both xi and lambda again** with exactly half the prior stencil spacing. The earlier negative result remains authoritative for the earlier scale pair.

## Frozen base and profile
Base remains `(Horava_xi,Horava_lambda,Horava_eta)=(-1e-4,+1e-4,2.1e-3)` with unchanged author-shipped stability settings and all other EFTCAMB configuration. Immutable radial authority remains run `34695408204`, artifact `10298444789`.

## Frozen new stencil for each axis
- coarse symmetric delta: `1.0e-6`;
- fine symmetric delta: `5.0e-7`.
The other two Hořava coordinates stay fixed. The exact base is rerun and must match immutable radial-base CMB and P(k) with normalized L2 `<=1e-8`.

## Frozen response criteria
Use the same response operator as the prior coordinate protocol: common finite scalar-C_l plus P(k) support, blocks normalized by base L2, central derivatives concatenated.
A derivative is converged iff coarse/fine principal angle `<=5 deg` and relative norm mismatch `<=0.25`. A converged coordinate is response-distinct from the immutable fine radial derivative iff angle `>=10 deg`.

## Interpretation
This is a resolution/localization diagnostic, not a replacement for the prior result. No threshold changes are allowed. Both axes are tested regardless of either outcome.

Always set `K2_promoted=false`, `canonical_K2=OPEN`, `physical_falsification=false`, `complete_Horava_family_claim=false`. Any possible K2 status change requires a later immutable synthesis including both the earlier and finer-scale evidence and source/quotient scope.