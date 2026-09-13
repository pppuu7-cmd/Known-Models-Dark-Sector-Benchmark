# W07 M35 / F35 K4 execution recovery v0.1

Status: FROZEN BEFORE RECOVERY EXECUTION

## Trigger
Initial run `34719730375` built the exact pinned provider successfully but all nine solver cases returned nonzero before any scientific K4 comparison. The artifact shows two execution-layer causes: (1) default cases were launched from the repository root, so the provider could not resolve its relative `bbn/sBBN.dat`; (2) `Misha.ini` and provider precision `.pre` files contain overlapping numerical keys (observed `evolver`), and this CLASS parser rejects duplicate entries instead of overriding them. The original generated input also did not explicitly request the preregistered mandatory EE/TE outputs.

## Frozen science
No physical point, provider pin, numerical profile, mandatory observable, metric, threshold, or classification rule from `W07_M35_K4_LOCAL_2D_PRECISION_PREREGISTRATION_v0.1.md` may change.

## Permitted process-only repair
1. Execute the provider from its own working directory so provider-relative data files resolve.
2. For `permille` and `reference`, construct one merged parser input by removing from the tuned base `.ini` any numerical keys also defined by the corresponding provider `.pre`, then appending that exact `.pre` content. This is a parser-compatible representation of the same frozen precision profile; physical keys `alpha`, `beta`, `lambda`, `Y_dm` are protected and any overlap with a `.pre` fails closed.
3. Explicitly request `tCl,pCl,lCl,mPk`, because TT/EE/TE/P(k) were mandatory in the original frozen protocol. This changes requested outputs only, not physics.
4. Reuse the unchanged analyzer and unchanged frozen gate.

Any further parser/provider failure remains `M35_K4_PROVIDER_OR_PRECISION_EXECUTION_BLOCKED`, never physical falsification.
