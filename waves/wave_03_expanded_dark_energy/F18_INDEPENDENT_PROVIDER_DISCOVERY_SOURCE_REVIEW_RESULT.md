# F18 independent-provider discovery — exact-source review result

Date: 2026-09-14
Parent protocol: `protocol/W03_F18_INDEPENDENT_GHOST_CONDENSATE_PROVIDER_DISCOVERY_v0.1.md`
Parent run: `34816391227`
Aggregate artifact: `10337075318`
Aggregate digest: `sha256:1e79cfd3b0a7bb00e8ce757fd37617d75179c8e2547bf8fb5f32c83ca61fb7fa`

## Classification

`F18_INDEPENDENT_PROVIDER_DISCOVERY_FALSE_POSITIVE_SOURCE_COMPLETE_SET_AFTER_MANUAL_REVIEW`

`K0_promoted=false`, `K1_promoted=false`, `physical_falsification=false`.

## Review

The v0.1 mechanical triage returned many `SOURCE_COMPLETE_REVIEW` hits because generic prose/review/corpus files can simultaneously contain words matching the frozen law/cosmology/perturbation/executable regexes. Manual exact-source review rejects these as provider evidence.

Representative examples:

- `houstongolden/bigbounce@13ee4a99ed254544d4a3de51124e141c61f0a7c6`, `project-context/peer-reviews/2026-06-02_R-upgraded-round6_P3_R-round_direct_Gemini25Pro_cosmology.md`: a reviewer transcript discussing NEC violation and mentioning ghost-condensate models. It is not a ghost-condensate cosmological solver or implementation.
- `kartheikiyer/lodestone@0674837aa5db0fbbae753d3efea04b79aeb5c892`, `content/Cosmology/friedmann-equations.md`: educational/reference prose on Friedmann cosmology, not an executable ghost-condensate implementation.
- `carlzimmerman/zimmerman-formula@ecc44b6d0b4541cae77f0087012f13f2aaed726b`, `real_research/reviews/keating_darkenergy_doors.py`: an executable phenomenology/review script that asserts a ghost-condensate sector but does not implement the F18 Lagrangian, background field equations, perturbation closure, or a Boltzmann solver for that sector.
- corpus/RSS/arXiv metadata and review-text hits are provenance noise, not implementations.

No manually reviewed candidate in this frozen tranche establishes all of: an explicit ghost/kinetic-condensate law, cosmological background evolution of that law, source-complete perturbation/gauge equations, executable solver integration, and an independently usable reference path distinct from the already-blocked CLASS_GSF lineage.

## Consequence

F18 remains `BLOCKED_IMPLEMENTATION_REFERENCE_PROVIDER_SEARCH`. The CLASS_GSF lambda=0 singular reference path remains a provider-specific numerical blocker and is not a physical failure of ghost-condensate physics. No K0/K1 promotion is allowed from run `34816391227`.

The next permitted action is a narrower code-biased independent-public-source search, prospectively frozen before execution, designed to reject documentation/corpus/review files and require implementation-bearing file types/signatures before manual review.