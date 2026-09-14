# W03 F18 independent ghost-condensate provider discovery v0.1

Status: FROZEN BEFORE EXECUTION
Date: 2026-09-14
Family: F18 / M18 ghost condensate / kinetic vacuum branch

## Motivation

The current CLASS_GSF route is provider-specifically blocked at the prospectively defined `lambda=0` condensate reference because the pinned shooting implementation has a singular `f1/fabs(f1)` path near an already-good root. This is not a physical failure of the ghost-condensate family. The next allowed action is an independent public implementation or an author-supported numerically regular reference prescription.

## Scope

This gate is provenance/source discovery only. It may identify candidate repositories/files but cannot promote K0/K1 or infer physical viability.

A candidate can reach `SOURCE_COMPLETE_REVIEW` only if the fetched source itself contains evidence for all of:

1. ghost-condensate / dilatonic-ghost / kinetic-condensate law (e.g. `P=-X+c exp(lambda phi) X^2`, `P(X)` with `P_X=0`, or an equivalent explicitly named ghost-condensate branch);
2. cosmological background or Friedmann evolution rather than only formal notes;
3. perturbation/Boltzmann/gauge implementation or an explicitly executable cosmological perturbation solver;
4. an executable implementation signal (source code, solver integration, parameter parser/example), not only paper text;
5. no obvious toy/scaffolding-only disclaimer.

A source that is background-only, literature text, EFT discussion without an executable cosmological realization, or particle-physics use of the words `ghost`/`condensate` is only a provenance lead or reject.

## Frozen independent search lanes

0. `"ghost condensate" CLASS cosmology`
1. `"ghost condensate" CAMB cosmology`
2. `"dilatonic ghost condensate" code`
3. `"P=-X" "X^2" cosmology`
4. `"P_X" "ghost condensate" perturbation`
5. `"ghost condensate" Boltzmann perturbation`
6. `"kinetic condensate" cosmology perturbation`
7. `"dilatonic ghost" CLASS_GSF`

Each lane is independent and runs under matrix `fail-fast:false`. API rate-limit failures are infrastructure-only and must not be treated as no-candidate scientific evidence.

## Frozen classifications

- `F18_INDEPENDENT_PROVIDER_SOURCE_COMPLETE_CANDIDATE_FOUND`: at least one fetched source satisfies the mechanical source-completeness signals. Requires manual exact-source audit before any K0/K1 action.
- `F18_INDEPENDENT_PROVIDER_PROVENANCE_LEADS_ONLY`: no source-complete candidate, but at least one plausible provenance lead.
- `F18_INDEPENDENT_PROVIDER_NO_QUALIFYING_PUBLIC_SOURCE_IN_FROZEN_TRANCHE`: successful search coverage with no qualifying source.
- `F18_INDEPENDENT_PROVIDER_DISCOVERY_INFRASTRUCTURE_BLOCKED`: all lanes unavailable/failed so no source conclusion is permitted.

## Prohibitions

- no patching or retuning the existing CLASS_GSF shooting algorithm;
- no changing the frozen M18 physical reference to avoid the singularity;
- no K1 execution before exact candidate commit/source, reference map, stability conditions, and parameters are preregistered;
- no family falsification from search failure/provider scarcity;
- no duplicate provider branch if the candidate is merely the same CLASS_GSF lineage.
