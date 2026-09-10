# M14 LisaGoh/CDE author-branch exact-reference audit

Updated: 2026-09-10

## Question
After the prospectively frozen regularization-split audit, check whether the upstream author repository already contains an independent author-supported branch that regularizes the exact beta=0 scalar perturbation reference. This is a provenance/source audit only; it does not authorize a new numerical K1/K4/K5 gate.

## Upstream branches inspected

Upstream repository: `LisaGoh/CDE`.

- `main` head: `b85a675af7544a5183e402964550811aa805b698` (2023-03-22, `fixed CDE.ini file`).
- `7bin` head: `2a572b39d4ae0a3c940b6f179585686ae1a03881` (2023-03-30, `updates`).

The relevant `class_CDE/source/perturbations.c` blob on `7bin` is `e1b9d12b807994871906dd0b11ff84b52bc091cc`, i.e. the inspected code retains the same exact-zero singular structures relevant to the current blocker.

## Relevant source findings on 7bin

The scalar velocity source still evaluates

`rho_plus_p_theta_scf / (rho_scf + p_scf)`

without an exact-rigid-vacuum guard. At the exact beta=0, phi'=0 reference, `rho_scf+p_scf` vanishes.

The scalar perturbation Klein-Gordon equation still contains the term proportional to

`beta_prime * ... * H / phi_prime_scf`

without an author-supplied exact-zero branch prescription. At the exact reference both numerator and denominator vanish, leaving the same removable/degenerate numerical structure identified on main.

No author-supported alternate exact-reference prescription was found in the only other visible upstream branch.

## Relation to the frozen split audit

The immutable split audit from Actions run `34490297354`, job `102914977778`, artifact `10157548938` (`sha256:1e5d006704453d6d71aea4626d3c105996eee4370886cc226a270fe21f2c888e`) found:

- baseline repeatability PASS;
- R2 is the only noninterfering patch component on author and beta=0 tiny-seed controls;
- R2 alone still fails the exact full-reference execution (`R2_exact` exit 1);
- R1 permits an exact route but measurably changes nonzero/tiny-seed spectra and therefore fails the frozen noninterference requirement;
- combined R12 inherits the R1 interference and is not admissible as a transparent verification regularization.

Hence no prospectively tested regularization is both (a) noninterfering away from the singular null and (b) sufficient to execute the exact full reference.

## Classification

`M14_LISAGOH_CDE_AUTHOR_BRANCH_REFERENCE_REGULARIZATION_NOT_FOUND`

This is a provider/reference-implementation and provenance result, not a family-level physical failure. The exact background reference remains valid; the untouched full perturbation exact-reference route remains blocked. The independent KMDSB regularization attempt is not promoted to K1/K3 evidence.

## Consequences

- Do not keep patching denominators or retune scalar seeds post hoc.
- Do not use the beta=0 tiny-seed run as the exact K1 reference.
- Do not reopen K4/K5 on this provider from the verification layer.
- Retain the earlier IDECAMB and iDM provider-specific records unchanged.

## Next allowed M14 gate

Search a genuinely independent, public, source-complete coupled-quintessence implementation with an author-supported regular beta=0/reference prescription and active perturbation closure. Pin the exact commit/release before any execution. If such a provider is found, preregister provider control and K1 before inspecting nonzero-coupling response.
