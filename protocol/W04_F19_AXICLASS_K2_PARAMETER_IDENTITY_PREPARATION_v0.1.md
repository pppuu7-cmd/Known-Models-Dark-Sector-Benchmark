# W04 F19 AxiCLASS K2 parameter-identity preparation v0.1

Frozen: 2026-09-14 while the authoritative F19 K0/K1 execution remains non-terminal.

Provider: `PoulinV/AxiCLASS@ae9609e1f96ddebbb6cc8a46de94512514c68781`.

## Purpose

Outcome-independent source preparation only. This audit maps the meanings of AxiCLASS axion parameters so that a future K2 gate, **if separately authorized by terminal K1 PASS**, does not confuse decay scale, field initial condition, present-day abundance, or critical-epoch fraction.

This audit cannot open K2, cannot promote K0/K1, and cannot select a numerical K2 anchor.

## Frozen semantic questions

P1. Is `f_axion` a field/potential decay scale rather than an abundance fraction?

P2. Does `Omega_scf` / `Omega_scf_shoot_fa` provide a present-day scalar-density target by comparing the final scalar density to `Omega0_scf`?

P3. Is `fraction_axion_ac` a distinct critical-epoch fraction target coupled to an axion critical scale/epoch rather than an alias for present-day `Omega_scf`?

P4. Do `scf_parameters` encode scalar initial-condition parameters (field/angle and velocity, with tuning variants) rather than a direct present-day abundance coordinate?

## Required evidence

Use only exact-pin source plus committed provider examples/configuration. Record exact files and source snippets/substring identities supporting each semantic statement. At least two independent source surfaces must support the overall map (e.g. input parser/target code plus author example/configuration).

## Negative controls

The verifier must reject these false equivalences:

- `f_axion == dark-matter abundance`;
- `fraction_axion_ac == Omega_scf`;
- `scf_parameters[0] == Omega_scf`.

The negative-control result is semantic inequality, not a numerical comparison.

## Classification

All P1-P4 and negative controls established:

`F19_AXICLASS_K2_PARAMETER_IDENTITY_PREPARATION_PASS_WITH_SCOPE`.

Otherwise:

`F19_AXICLASS_K2_PARAMETER_IDENTITY_PREPARATION_INCOMPLETE`.

## Interpretation ceiling

Even on PASS, `K2_authorized=false`. A future K2 preregistration may use this map only after terminal K1 PASS. The preferred abundance coordinate should then be explicitly chosen from an author-supported present-density target such as `Omega_scf`, while `m_axion`, `f_axion`, and field initial angle/velocity remain separate unless the future preregistration freezes a different author-supported map.

`K0_promoted=false`, `K1_promoted=false`, `K2_authorized=false`, `physical_falsification=false`.
