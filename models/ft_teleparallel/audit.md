# M37 / F37 f(T) teleparallel gravity audit

## Current classification
`M37_K0_PARTIAL_EXECUTABLE_FT_PROVIDER_PROVENANCE_OPEN`

This is **not** a physical failure. K0 is `PARTIAL`; K1-K9 are open.

## Executable provider evidence
- Provider: `Speeddemon5050/Modified-CLASS-fT-Exact-`
- Exact pin: `74e6a8679cdc233fb339c67127ed0921ba547894`
- Canonical recovery run: `34652066337`
- Job: `103436265579`
- Artifact: `10284291219`
- Artifact digest: `sha256:e885cda93e26c13268f86e58e667aa8596d0cbeff4e26ff8f80a4edece32f4b5`
- Reference arm: `n_fT=0.0`, exit 0
- Active arm: `n_fT=0.10`, exit 0
- TT normalized-L2 response: `0.011484175401063655`
- P(k) normalized-L2 response: `0.015756960779908492`
- Frozen activity threshold: `1e-6`
- All four reference/active TT/P(k) products used by the recovered analyzer are finite and nonempty.

## Harness recovery
Parent run `34650851131` was not a physical/provider execution failure: CLASS emitted `reference__cl.dat`, `reference__pk.dat`, `active__cl.dat`, `active__pk.dat`, while the harness touched and analyzed zero-byte single-underscore placeholder names. The repair was preregistered in `protocol/W05_M37_K0_OUTPUT_ROOT_RECOVERY_v0.1.md` at commit `77ab1dc653de2f749a0ff60088b8d67c80391b78` and changed only output-path plumbing. Provider pin, cosmology, `n_fT` arms and frozen response threshold were unchanged.

## Why K0 is not promoted
The pinned repository README is generic upstream CLASS documentation and does not establish publication/author provenance for the f(T) modification itself. Executable code plus response activity is therefore insufficient for full K0 authority/provenance closure. An independently authoritative publication/repository linkage or equivalent provenance evidence is required before K0 promotion.

## Next allowed gate
Resolve publication/author provenance for this exact implementation or pin an independently authoritative f(T) cosmology implementation. Only after K0 authority closure may a prospective K1/reference-limit gate be defined. Do not infer physical falsification from provenance incompleteness.
