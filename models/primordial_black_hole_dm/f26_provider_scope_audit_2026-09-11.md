# F26 primordial-black-hole dark matter — provider/scope audit

Date: 2026-09-11
Status: K0/SCOPE AUDIT — NO K1 PROMOTION
Census family: F26 primordial-black-hole dark matter

## 1. Why F26 must not be represented by one generic `f_PBH` direction

PBH phenomenology contains several physically and observationally distinct response mechanisms. A single abundance parameter does not define a unique cosmological response unless the PBH mass function and the relevant radiative/gravitational mechanism are fixed.

At minimum the W04 census must distinguish the following scoped representatives.

### F26a — evaporating PBH / Hawking-energy-injection response

Public source-bound provider candidate:
- `lesgourg/class_public`, `ExoCLASS` branch
- pinned branch head inspected on 2026-09-11: `42e8f9418e3442d1ea3f26ff84dc9f0e856a0f1d`
- associated method: Stöcker, Krämer, Lesgourgues & Poulin, *Exotic energy injection with ExoCLASS: Application to the Higgs portal model and evaporating black holes*, JCAP 03 (2018) 018, arXiv:1801.01871.

The pinned `explanatory.ini` explicitly exposes `PBH_fraction` and `PBH_evaporating_mass` and states that built-in DarkAges can compute PBH evaporation. ExoCLASS couples this exotic injection to recombination/CMB transfer through the bundled DarkAges machinery.

Current classification: `F26A_EXOCLASS_EVAPORATION_PROVIDER_PINNED_K0_EXECUTION_CONTROL_OPEN`.

No K1 claim is made yet. A provider-control must first establish a modern reproducible execution at the exact pin and identify a source-bound/paper-bound PBH example without inventing an anchor.

### F26b — accreting massive-PBH CMB response

This response is not equivalent to F26a, but the same pinned ExoCLASS branch does contain a built-in accretion forward path. Its `explanatory.ini` exposes:
- `PBH_fraction`
- `PBH_accreting_mass` in solar masses
- `PBH_accretion_recipe = spherical_accretion` for the Ali-Haïmoud–Kamionkowski prescription (arXiv:1612.05644), or `disk_accretion` for the Poulin et al. prescription (arXiv:1707.04206).

Thus the earlier provisional statement that no accretion forward provider had been located is superseded. ExoCLASS is a source-complete candidate for these two legacy accretion prescriptions.

However, modern work such as Agius et al., arXiv:2403.18895 / JCAP 07 (2024) 003, shows that local gas ionization/heating feedback can materially modify PBH accretion and the inferred CMB bound. Therefore a successful ExoCLASS spherical/disk execution would validate those scoped prescriptions, not all modern accreting-PBH physics.

The public `bradkav/PBHbounds` repository contains tabulated CMB accretion bounds, including the Agius-2024 Park–Ricotti-based result, but remains a bounds/plotting collection rather than the underlying forward solver.

Current classification: `F26B_EXOCLASS_LEGACY_ACCRETION_PROVIDER_PINNED_MODERN_FEEDBACK_COVERAGE_OPEN`.

Do not infer equivalence between spherical, disk and modern feedback-aware/Park–Ricotti accretion responses unless a common forward comparison proves it.

### F26c — discrete/Poisson/gravitational structure response

Even in a regime with negligible radiative injection/accretion, compact PBHs are discrete massive objects and can introduce a small-scale Poisson/isocurvature contribution and nonlinear structure effects. This response is not represented by either F26a or F26b and may require a separate perturbation/structure provider or analytic bridge.

Current classification: `F26C_POISSON_STRUCTURE_RESPONSE_PROVIDER_OPEN`.

## 2. Coverage semantics

For census purposes F26 remains one top-level physical family, but terminal coverage cannot be granted from a single scoped child unless the other response-distinct PBH mechanisms are either:
1. shown to be observationally/physically represented by the tested child in the benchmark domain, or
2. explicitly masked outside the scope of the family claim, with a separately justified census decision.

A future family-level PBH status must therefore record the PBH mass range, mass function, physical mechanism, accretion/evaporation prescription and observation channel. `PBH DM` without these qualifiers is not a valid benchmark coordinate.

## 3. Immediate allowed steps

1. F26a: inspect pinned ExoCLASS/DarkAges for the exact author/paper evaporation anchor and preregister a provider-control only after the input contract is source-bound.
2. F26b: separately inspect the built-in spherical and disk accretion paths; do not merge them. Then search for a public modern feedback-aware/Park–Ricotti forward implementation and determine whether it adds a response-distinct child or supersedes an old prescription in the benchmark domain.
3. F26c: locate a source-bound linear/structure implementation for the PBH Poisson/isocurvature term; keep it independent of radiative-injection validation.

## 4. Guardrails

- No physical PBH falsification from provider, code-age or provenance blockers.
- No family-level PASS/FAIL from one mass point or one radiative mechanism.
- Do not treat an exclusion-curve repository as a substitute for the underlying forward model.
- Do not treat successful ExoCLASS legacy accretion as validation of later feedback-aware prescriptions without a response-equivalence test.
- Do not use thermal-WDM or smooth-CDM transfer functions as PBH surrogates merely for implementation convenience.
- Keep `NEW_MODEL: DESIGN_AUTHORIZED / NOT_YET_REQUIRED`; F26 coverage cannot by itself decide new-model necessity.
