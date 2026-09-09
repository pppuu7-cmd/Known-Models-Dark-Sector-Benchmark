# W03/M07 — C1 smooth-w cross-channel nearest-comparator attack

Date: 2026-09-09  
Status: **PASS_WITH_SCOPE — matter-only near-degeneracy is broken by the joint expansion+growth response in unwhitened theory space**

## Scope and provenance

M07: canonical scalar-field branch with local quotient coordinate `q=lambda^2`.  
C1: smooth non-phantom fluid direction `epsilon_w=1+w -> 0+`.

Primary successful run: `34373096320`.  
Artifact: `w03-m07-c1-crosschannel-comparator-v2`.  
Artifact digest: `sha256:63db00acdd9f9ba07fefbeb96cf9bad413b08cc58dcda9d5a98e56ccf3e77237`.

Pinned solvers/authorities:
- M07/C1 paired generator: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`;
- frozen DSIR C1 tangent bridge: `Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`, `data/derived/comparison_readiness/local_response_tangents_v0_1.json`.

The first v1 run failed only because CLASS forbids simultaneously supplying positive `Omega_scf` and explicit `Omega_Lambda`. v2 changed only closure plumbing; scientific points and preregistered thresholds were unchanged.

## Frozen test

Common response:
- 35-node `ln P(k,z)` block on the frozen 7x5 DSIR low-k grid;
- 7-node `ln H(z)` block.

Coordinates:
- M07: lambda `0.025`, so `q=0.000625`;
- C1: `epsilon_w=1e-4`, `w0=-0.9999`.

Before the result, the run froze:
1. a C1 bridge control: generated C1 matter direction must match the historical frozen DSIR tangent within `1 deg` and scalar-projection residual `<0.02`;
2. fit one scalar mapping C1 -> M07 using **matter response only**;
3. carry that identical scalar into H;
4. call a cross-channel separator only if the H residual fraction is at least `0.10`.

No observational covariance is used here.

## Bridge control

Generated C1 vs historical frozen DSIR C1 matter tangent:
- acute angle: `0.37451794 deg`;
- best scalar projection residual: `0.00653652`.

Both preregistered bridge controls pass.

## Results

### Matter block

M07 vs C1:
- acute angle: `6.76393241 deg`;
- best scalar projection residual: `0.11777887`.

This reproduces the previously observed strong low-k matter-response near-alignment.

The best C1 -> M07 matter-only amplitude is

`a_P = 0.06866077867`.

### Expansion block

M07 vs C1 H directions before amplitude transfer:
- acute angle: `10.61239853 deg`;
- best scalar projection residual: `0.18416405`.

Crucially, when the **matter-fitted** amplitude `a_P` is transferred unchanged into the H block,

`||H_M07 - a_P H_C1|| / ||H_M07|| = 0.3091701900`.

This exceeds the preregistered `0.10` separator threshold by more than a factor of three.

Frozen classification: **`CROSSCHANNEL_SEPARATOR`**.

## Interpretation

The low-k matter response alone makes canonical quintessence look close to smooth phenomenological dark energy. But one scalar rescaling that best matches the matter response cannot simultaneously reproduce the expansion response. Thus the paired background-growth consistency relation supplies a real theory-space discriminator between these two branches.

This strengthens B6 and provides scoped evidence toward B7, but it does **not** by itself close B7 because:
- the result is unwhitened;
- B5 observation-space identifiability remains open;
- M07 B2 carries a measured small residual gauge/subtraction floor;
- only one phenomenological DE comparator and one joint block have been tested here.

Therefore B7 is advanced only to `PARTIAL`, not `SUPPORTED`/discovery.

## Future-model lesson

If a candidate is nearly degenerate with a known family in one observable block, preserve and test cross-channel consistency using one amplitude/parameter mapping across blocks. A mechanism that needs independent re-fitting in each block has not achieved full response equivalence.

This generates DP-0810.
