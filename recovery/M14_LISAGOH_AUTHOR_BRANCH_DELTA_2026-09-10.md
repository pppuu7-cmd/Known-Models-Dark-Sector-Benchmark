# Recovery delta — M14 LisaGoh/CDE exact-reference branch audit

Updated: 2026-09-10
Authoritative evidence for this delta overrides older chat summaries.

- Latest consumed scientific-diagnostic workflow: run `34490297354`, job `102914977778`, artifact `10157548938`, digest `sha256:1e5d006704453d6d71aea4626d3c105996eee4370886cc226a270fe21f2c888e`.
- Machine classification: `M14_CDE_SPLIT_NONINTERFERENCE_AUDIT_COMPLETE`.
- Frozen result: baseline repeatability PASS; only R2 is noninterfering, but R2 exact reference exits 1. R1 opens exact execution but changes nonzero/tiny-seed observables and therefore fails noninterference. No tested regularization both preserves nonsingular physics and executes the exact full reference.
- Upstream branch audit: `LisaGoh/CDE` exposes `main@b85a675af7544a5183e402964550811aa805b698` and `7bin@2a572b39d4ae0a3c940b6f179585686ae1a03881`. The 7bin perturbation source retains the same unguarded scalar-velocity denominator and `beta_prime/phi_prime_scf` structure; no author-supported exact-beta=0 prescription was found.
- Classification: `M14_LISAGOH_CDE_AUTHOR_BRANCH_REFERENCE_REGULARIZATION_NOT_FOUND`.
- This is not a physical falsification. Exact background reference remains valid; untouched full perturbation K1 remains provider-blocked. Independent KMDSB regularization does not promote K1/K3 and does not authorize K4/K5.
- Do not continue denominator patching, seed tuning, beta shrinking or serialization changes on this route.
- Next allowed M14 gate: independent public source-complete coupled-quintessence provider with author-supported regular beta=0/reference prescription and active perturbation closure; pin exact source before execution.

Strict census bookkeeping remains 4/46 terminal/represented and 42/46 requiring strict closure unless a newer canonical matrix explicitly changes it.

Related audit commit: `4238346b01820fcee1b2954fee7a019211f81551`.
