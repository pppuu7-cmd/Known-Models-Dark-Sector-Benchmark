# F16 focused running-vacuum discovery — exact-source review

Date: 2026-09-14
Parent workflow run: `34811832435`
Aggregate artifact: `10335835986`
Aggregate digest: `sha256:a3941f868182a69b38b255529add82339363584923b89c0aab0ed09376112571`
Frozen protocol: `protocol/W03_F16_FOCUSED_RUNNING_VACUUM_PROVIDER_DISCOVERY_v0.1.md`

## Machine outcome

The aggregate machine classifier returned `F16_FOCUSED_DISCOVERY_SOURCE_COMPLETE_CANDIDATE_FOUND`. This label is a triage label only: by protocol it does not promote K0/K1 and requires exact-source review.

Two search lanes remained rate-limited after bounded retries; this does not invalidate the successful lanes and is not a scientific negative result.

## Exact-source review of the mechanically strongest hits

### `CyrilPitrou/primat@4bf97d5082eee54b9df50d88f43182bb651fea80`, `primat/background.py`

Reject as an F16 provider. The file is PRIMAT's BBN cosmological-background abstraction and standard neutrino/thermal-history machinery. Its documented extension seam allows custom expansion histories / extra energy density, but the inspected source does not implement a running-vacuum `rho_Lambda(H,Hdot,...)` law, dark-sector exchange closure, or late-time linear perturbation realization for F16. Keyword co-occurrence caused the triage false positive.

Classification: `NOT_F16_PROVIDER`.

### `instituto-Rafael/relativity-living-light@8b196ee7c62f57d8993b24d391f2ace700d384c2`, `tools/run_g4_background_tournament.py`

This is a real cosmology implementation, but not a new response-distinct F16 running-vacuum provider. Its declared IDE model is `Q=3 beta H rho_Lambda`; the same file explicitly describes the exercise as a **background tournament** and states that growth/CMB are not reused because IDE requires model-specific perturbation closure before fair comparison. The companion contract cites the same interaction law.

For KMDSB this is therefore:

- a background-only implementation of the already-covered interacting-vacuum subcase;
- `REPRESENTED_BY:M02_WITH_SCOPE` at the family level;
- not a source-complete genuine `Lambda(H)`, `H^2`, `Hdot`, or derivative-law running-vacuum provider;
- not eligible for a new K0/K1 promotion for the still-open response-distinct F16 running-vacuum branch.

Classification: `REAL_IDE_BACKGROUND_BUT_REPRESENTED_BY_M02_AND_PERTURBATION_INCOMPLETE`.

### Remaining mechanically high-priority hits

The remaining high-priority rows are text corpora, literature mirrors/notes, KMDSB's own files, or speculative/non-provider repositories selected through keyword co-occurrence. None inspected establishes an independently executable source-complete late-time running-vacuum Boltzmann provider with all of: explicit `rho_Lambda(H,Hdot,...)` law, conservation/exchange split, perturbation prescription, and a frozen LambdaCDM reference map.

## Canonical classification

`F16_FOCUSED_DISCOVERY_NO_NEW_SOURCE_COMPLETE_RESPONSE_DISTINCT_PROVIDER_AFTER_SOURCE_REVIEW`

Consequences:

- F16 remains open for genuine running-vacuum `Lambda(H)`, `H^2`, `Hdot`, or derivative-law response families.
- The interacting-vacuum `Q=beta H rho_vac` subcase remains `REPRESENTED_BY:M02_WITH_SCOPE` and should not be duplicated.
- K0/K1 are **not** promoted for the open running-vacuum branch.
- No physical falsification is inferred from provider scarcity or search-rate limits.
- Do not weaken source-completeness criteria post hoc.

Next allowed F16 action is a different independent provenance route (author/paper repositories or known solver forks) if one is identified; repeated broad GitHub keyword search is not justified without new search information.
