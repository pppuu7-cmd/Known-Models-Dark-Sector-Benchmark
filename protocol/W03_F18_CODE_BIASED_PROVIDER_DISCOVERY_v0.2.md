# W03 F18 code-biased independent provider discovery v0.2

Status: FROZEN BEFORE EXECUTION
Date: 2026-09-14
Family: F18 / M18 ghost condensate / kinetic vacuum branch

## Motivation

The v0.1 search completed successfully but its broad lexical classifier promoted many review, educational, corpus and metadata files to manual review. Exact-source review found no usable independent source-complete F18 provider. This v0.2 tranche narrows discovery toward implementation-bearing source files without changing the F18 physical target or the blocked CLASS_GSF reference.

## Scope

Provenance/source discovery only. No K0/K1 promotion, no physics verdict, no patching/tuning of CLASS_GSF.

## Frozen code-biased lanes

0. `"ghost condensate" extension:py cosmology`
1. `"ghost condensate" extension:c CLASS`
2. `"ghost condensate" extension:f90 CAMB`
3. `"dilatonic ghost" extension:py cosmology`
4. `"P=-X" "X^2" extension:py`
5. `"ghost condensate" "perturbations.c"`
6. `"ghost condensate" "background.c"`
7. `"kinetic condensate" extension:jl cosmology`

Run lanes independently with `fail-fast:false`. Rate-limit/fetch errors are infrastructure-only.

## Frozen file/source requirements

A candidate reaches `SOURCE_COMPLETE_REVIEW` only when all hold:

1. implementation-bearing extension/path (`.py`, `.c`, `.cc`, `.cpp`, `.h`, `.f`, `.f90`, `.jl`) rather than markdown/text/html/xml/json/bib/corpus metadata;
2. explicit ghost/dilatonic/kinetic-condensate law or equivalent P(X) kinetic stationary branch in executable source;
3. cosmological background/Friedmann integration for that sector;
4. perturbation/gauge/Boltzmann implementation in source, not merely a comment asserting it;
5. executable solver integration or callable numerical routine;
6. no toy/scaffolding-only disclaimer;
7. not the already-blocked `KunhaoZhong/CLASS_GSF` lineage and not KMDSB itself.

## Frozen classifications

- `F18_CODE_BIASED_SOURCE_COMPLETE_CANDIDATE_FOUND`
- `F18_CODE_BIASED_PROVENANCE_LEADS_ONLY`
- `F18_CODE_BIASED_NO_QUALIFYING_PUBLIC_SOURCE_IN_FROZEN_TRANCHE`
- `F18_CODE_BIASED_DISCOVERY_INFRASTRUCTURE_BLOCKED`

Any machine `SOURCE_COMPLETE_REVIEW` remains only a manual-review candidate. It does not imply K0/K1 PASS.

## Prohibitions

No physical retuning, no change of the lambda=0 reference target, no inference of family falsification from provider scarcity, no duplication of CLASS_GSF lineage, and no K1 execution before exact source/commit/reference/stability/parameter preregistration.