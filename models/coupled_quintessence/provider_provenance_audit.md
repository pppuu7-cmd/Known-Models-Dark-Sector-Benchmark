# M14 coupled-quintessence provider provenance audit

Date: 2026-09-10
Candidate provider: `kabeleh/iDM@dc55e59dec8f5c647df6e9d764f5c6960796e1df`
Target family: F14/M14 coupled quintessence / scalar-DM coupling

## Positive provenance evidence
The pinned public repository README identifies the model as quintessence interacting with dynamical dark matter and states that the repository contains the modified CLASS source. It gives the explicit compilation/run contract:

- `make clean; make class -j`
- `./class iDM.ini`

The repository's regression/benchmark scripts also refer to `iDM.ini`, and committed benchmark timing tables record repeated `iDM.ini` runs with exit code 0.

## Blocking inconsistency
At the exact pinned public commit, `iDM.ini` is not retrievable from the repository contents API (`404 Not Found`). Repository code search returns references to the filename in README, regression/benchmark scripts and timing records, but not a tracked `iDM.ini` file itself.

Therefore KMDSB cannot execute the author's documented model point unchanged from this GitHub pin. Reconstructing an input from README prose, internal defaults, later files or guessed parameters would violate the provider-control rule and would not establish an immutable author example.

## Classification
`BLOCKED_PROVENANCE_MISSING_AUTHOR_INPUT`

This is not physical evidence against coupled quintessence or the iDM model. It is a provider/provenance limitation for this exact public GitHub snapshot.

## Scientific promotion
No K1-K9 scientific promotion is authorized. In particular, do not infer the coupling-off/reference coordinate from parameter names until a reproducible exact configuration/source binding is established.

## Allowed recovery
1. Look for an immutable author-published exact configuration in the provider's cited archival products (e.g. the Zenodo dataset named in README) and pin the exact file/checksum if accessible.
2. Otherwise select another public coupled-quintessence implementation with a tracked executable author example.
3. Only after such provider-control passes, preregister the physical decoupling/reference gate and then any production response grid.
