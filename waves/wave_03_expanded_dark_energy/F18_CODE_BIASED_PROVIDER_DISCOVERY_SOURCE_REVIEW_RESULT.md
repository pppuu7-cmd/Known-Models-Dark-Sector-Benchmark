# F18 code-biased provider discovery v0.2 — source review

Date: 2026-09-14
Family: F18 / M18 ghost condensate / kinetic vacuum branch
Parent protocol: `protocol/W03_F18_CODE_BIASED_PROVIDER_DISCOVERY_v0.2.md`
Parent Action run: `34820792370`
Aggregate artifact: `10337808801`
Aggregate digest: `sha256:d824ba2afdcac0020e15228504f0eeeb986d0049e0a46ba5fcd43753b4cb4e78`
Parent head: `143f04589f8caaeaaed733226a9f6e2b1602df18`

## Machine result

The frozen aggregate mechanically returned `F18_CODE_BIASED_SOURCE_COMPLETE_CANDIDATE_FOUND` and promoted seven paths to `SOURCE_COMPLETE_REVIEW`. This was a triage label only: `K0_promoted=false`, `K1_promoted=false`, `physical_falsification=false` in the artifact itself.

## Manual exact-source review

The promoted set does **not** supply an independent source-complete late-time ghost-condensate Boltzmann/reference provider.

- `Igrekess/PersistenceTheory@d6f53911640296d4c8c6c88924c14ee584c3ca26`, `scripts/ch13_relativity/cosmology/pt_mu_cosmology_A.py`: an unrelated Persistence-Theory dark-energy/CPL fitting script. Its use of `ghost` refers to an internal `mu` evolution ansatz/prime-coherence construction, not the F18 kinetic-condensate Lagrangian `P(X)` with a `P_X=0` branch and cosmological perturbation closure.
- `houstongolden/bigbounce@13ee4a99ed254544d4a3de51124e141c61f0a7c6`, `reproducibility/quintom_fnl_verification.py`: matter-bounce bispectrum/Mukhanov-Sasaki verification. It tests bounce-mechanism independence and does not implement a late-time ghost-condensate dark-energy provider or the F18 reference map.
- `carlzimmerman/zimmerman-formula@ecc44b6d0b4541cae77f0087012f13f2aaed726b` promoted paths are review/research-analysis scripts rather than a source-complete CLASS/CAMB-equivalent F18 background+linear-perturbation solver with a documented exact condensate reference prescription. The same repository does contain ghost-condensate consequence/VEV calculation leads, but the aggregate itself classifies those mainly as `PROVENANCE_LEAD`, not provider validation.
- obvious non-cosmology lexical collisions (`dmilakovic/harpslfc` and mathematical optimization repositories) are not F18 providers.
- frozen direct CLASS/CAMB implementation lanes returned zero hits for `"ghost condensate" extension:c CLASS`, `"ghost condensate" extension:f90 CAMB`, and `"ghost condensate" "perturbations.c"`.

## Classification

`F18_CODE_BIASED_DISCOVERY_NO_INDEPENDENT_SOURCE_COMPLETE_PROVIDER_AFTER_MANUAL_REVIEW`

`K0_promoted=false`, `K1_promoted=false`, `physical_falsification=false`.

The existing CLASS_GSF model-1 author DGF point and its lambda=0 shooting singularity remain immutable provider-specific evidence. This v0.2 search does not convert that blocker into a family-level failure. F18 remains `BLOCKED_IMPLEMENTATION_REFERENCE_PROVIDER_SEARCH`.

## Consequence / next allowed gate

Do not continue broad lexical GitHub searching as though more hits alone increase scientific coverage. Future F18 reopening requires either (a) a genuinely independent public implementation with explicit kinetic-condensate equations, background and linear perturbations plus a documented regular reference map, or (b) an author-supported regular reference prescription for an already pinned implementation. Until then, use compute capacity on a different prospectively defined open family/gate.
