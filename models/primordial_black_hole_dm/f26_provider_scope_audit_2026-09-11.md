# F26 primordial-black-hole dark matter — provider/scope audit

Date: 2026-09-11
Status: K0/SCOPE AUDIT — NO K1 PROMOTION
Census family: F26 primordial-black-hole dark matter

## 1. Why F26 must not be represented by one generic `f_PBH` direction

PBH phenomenology contains several physically and observationally distinct response mechanisms. A single abundance parameter does not define a unique cosmological response unless the PBH mass function and the relevant radiative/gravitational mechanism are fixed.

At minimum the W04 census must distinguish the following scoped representatives:

### F26a — evaporating PBH / Hawking-energy-injection response

Public source-bound provider candidate:
- `lesgourg/class_public`, `ExoCLASS` branch
- pinned branch head inspected on 2026-09-11: `42e8f9418e3442d1ea3f26ff84dc9f0e856a0f1d`
- associated method: Stöcker, Krämer, Lesgourgues & Poulin, *Exotic energy injection with ExoCLASS: Application to the Higgs portal model and evaporating black holes*, JCAP 03 (2018) 018, arXiv:1801.01871.

ExoCLASS couples exotic injection to recombination/CMB transfer through the bundled DarkAges machinery. This route is relevant to evaporating PBHs, especially light PBHs whose Hawking products alter ionization/heating histories.

Current classification: `F26A_EXOCLASS_EVAPORATION_PROVIDER_CANDIDATE_PINNED_K0_OPEN_EXECUTION_CONTROL`.

No K1 claim is made yet. A provider-control must first establish a modern reproducible execution at the exact pin and identify a stock/reference PBH example or reproduce a paper-bound configuration without inventing parameters.

### F26b — accreting massive-PBH CMB response

This is not equivalent to F26a. Massive PBHs accrete baryons and generate high-energy emission. The resulting CMB response depends on the accretion prescription, radiative efficiency, local ionization/heating and possible DM mini-halo feedback. Modern work (Agius et al., arXiv:2403.18895 / JCAP 07 (2024) 003) explicitly shows that local ionization feedback can materially change the accretion/CMB bound.

The public `bradkav/PBHbounds` repository contains tabulated CMB accretion bounds, including the Agius-2024 Park–Ricotti-based result, but it is a bounds/plotting collection rather than a source-complete cosmological forward provider. It therefore cannot by itself close K0-K5 for an accreting-PBH response.

Current classification: `F26B_ACCRETION_FORWARD_PROVIDER_PROVENANCE_OPEN`.

Do not substitute the evaporation ExoCLASS implementation for accretion, and do not infer an accretion transfer function from a published exclusion curve.

### F26c — discrete/Poisson/gravitational structure response

Even in a regime with negligible radiative injection/accretion, compact PBHs are discrete massive objects and can introduce a small-scale Poisson/isocurvature contribution and nonlinear structure effects. This response is not represented by either F26a or F26b and may require a separate perturbation/structure provider or analytic bridge.

Current classification: `F26C_POISSON_STRUCTURE_RESPONSE_PROVIDER_OPEN`.

## 2. Coverage semantics

For census purposes F26 remains one top-level physical family, but terminal coverage cannot be granted from a single scoped child unless the other response-distinct PBH mechanisms are either:
1. shown to be observationally/physically represented by the tested child in the benchmark domain, or
2. explicitly masked outside the scope of the family claim, with a separately justified census decision.

A future family-level PBH status must therefore record the mass range, mass function, physical mechanism, and observation channel. `PBH DM` without these qualifiers is not a valid benchmark coordinate.

## 3. Immediate allowed steps

1. F26a: inspect the pinned ExoCLASS/DarkAges tree for an author-supplied evaporating-PBH model/example and exact input contract. If an author configuration is present, preregister a provider-control before execution. If the public branch lacks a paper-bound runnable PBH example or requires unavailable legacy assets, record the blocker rather than fabricating a configuration.
2. F26b: continue provenance search for a public source-complete accretion forward model associated with a published CMB calculation. `PBHbounds` is useful for literature/census provenance but not sufficient as a forward solver.
3. F26c: locate a source-bound linear/structure implementation for the PBH Poisson/isocurvature term; keep it independent of radiative-injection validation.

## 4. Guardrails

- No physical PBH falsification from provider, code-age or provenance blockers.
- No family-level PASS/FAIL from one mass point or one radiative mechanism.
- Do not treat an exclusion-curve repository as a substitute for the underlying forward model.
- Do not use thermal-WDM or smooth-CDM transfer functions as PBH surrogates merely for implementation convenience.
- Keep `NEW_MODEL: DESIGN_AUTHORIZED / NOT_YET_REQUIRED`; F26 coverage cannot by itself decide new-model necessity.
