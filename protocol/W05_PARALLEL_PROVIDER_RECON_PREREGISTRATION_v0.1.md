# W05 parallel provider reconnaissance preregistration v0.1

## Purpose

Run independent, parallel public-provider discovery lanes for unresolved modified-gravity / geometry families before spending expensive compute on arbitrary implementations.

Frozen lanes:

- M34: massive/bimetric gravity
- M36: TeVeS / relativistic MOND-like
- M38: f(Q) / symmetric teleparallel gravity
- M39: nonlocal gravity
- M41: mimetic gravity
- M42: LTB/void cosmology
- M43: cosmological backreaction

## Frozen search policy

Each lane executes three predeclared GitHub repository-search queries combining the family name with at least one of `CLASS`, `CAMB`, `Boltzmann`, `cosmology` or a family-specific implementation term. For the highest-ranked unique repositories, the run records repository metadata and attempts README retrieval.

A machine score is used only to prioritize manual/provider audit. Positive evidence terms are:

- exact family/model term;
- `CLASS`, `CAMB`, `Boltzmann`;
- `arxiv`, `paper`, `publication`, or explicit scientific-use wording.

## Allowed outputs

- `PROVIDER_CANDIDATES_FOUND_REQUIRES_AUDIT`
- `NO_PROVIDER_GRADE_CANDIDATE_FOUND_IN_FROZEN_SEARCH`
- `SEARCH_BLOCKED`

No reconnaissance lane can promote K0, claim physical failure, or establish model correctness. A candidate must later pass an exact-pin source/build/execution/provenance audit before K0 can change.
