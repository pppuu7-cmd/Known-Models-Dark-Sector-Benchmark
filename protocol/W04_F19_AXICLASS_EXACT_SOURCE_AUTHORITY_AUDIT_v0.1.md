# W04 F19 AxiCLASS exact-source authority audit v0.1

Frozen: 2026-09-14 while authoritative F19 K0/K1 run `34846931382` is still non-terminal.

Provider: `PoulinV/AxiCLASS@ae9609e1f96ddebbb6cc8a46de94512514c68781`.

## Purpose

This is an outcome-independent static source/provenance audit. It does **not** read partial C0/Z0 outputs, does not compete with the non-terminal F19 K0/K1 verdict, and cannot promote K0 or K1. It asks only whether the exact pinned repository is a genuine executable axion scalar-field Einstein–Boltzmann source rather than a text/provenance false positive.

## Frozen hypothesis

At the exact pin, AxiCLASS contains all of the following in real source code:

1. immutable repository identity and executable CLASS build structure;
2. an explicit axion scalar potential and its first/second derivative machinery;
3. scalar-field background state/evolution with KG/fluid-switch support;
4. scalar perturbation state variables and an explicit switch enabling scalar perturbations;
5. the ordinary CLASS photon/relativistic perturbation hierarchy in the same solver tree;
6. an author-provided axion-DM example/input surface using the same implementation lineage.

## Required lanes

Run four independent jobs from fresh clones of the exact pin.

### S1 identity/example

Require exact HEAD identity; `Makefile`, `source/background.c`, `source/perturbations.c`, `source/input.c`, `include/background.h`, `include/perturbations.h`, and `example_axionDM.ini`; and axion/scalar-field keys in the example/input parser.

### S2 model law/background

Require in `source/background.c` an explicit cosine axion potential proportional to `m^2 f^2 [1-cos(phi/f)]^n` (including the `n=1` branch), derivative machinery using `sin(phi/f)`, and background scalar/KG or KG-to-fluid state machinery. Merely mentioning `axion` in comments fails this lane.

### S3 perturbation/Boltzmann coexistence

Require independent scalar perturbation indices (`phi_scf`, `phi_prime_scf` or their fluid equivalents) in the perturbation structures, source-level scalar perturbation support in `source/perturbations.c`, and simultaneous ordinary photon/ultra-relativistic Boltzmann hierarchy symbols in that same solver module. This is a structural coexistence test, not a numerical perturbation PASS.

### S4 lineage/provenance

Require origin repository `PoulinV/AxiCLASS`, exact commit identity, no dependence on the previously blocked KMDSB `CLASS_GSF` provider lineage in build/source paths, and source files rather than review/article/metadata-only artifacts. A CLASS ancestry is allowed; reuse of the blocked provider implementation is not.

## Frozen controls

Positive control: terminal author-control job from run `34846931382` already built the exact pin and ran unchanged `example_axionDM.ini`; its artifact is `10348785556`, digest `sha256:d0d4b2f3e5875d86eaaaeeba7f2bcd59917b38e91d2496ca0490e5da036faf4b`. This audit may record that identity but must not use any partial zero-identity evidence.

Negative controls, all mandatory inside the verifier:

- a text blob containing the word `axion` but none of the executable source anchors must fail S2/S3;
- removing the exact commit match must fail S1/S4;
- absence of scalar perturbation indices must fail S3.

## Classification

All four lanes plus all negative controls PASS:

`F19_AXICLASS_EXACT_SOURCE_AUTHORITY_PASS_WITH_SCOPE`.

Any missing mandatory source object:

`F19_AXICLASS_EXACT_SOURCE_AUTHORITY_NOT_ESTABLISHED`.

Infrastructure failure before the static audit is complete:

`F19_AXICLASS_SOURCE_AUDIT_INFRASTRUCTURE_BLOCKED`.

## Interpretation ceiling

A PASS means only that the pinned provider is source-complete enough to justify the already-running frozen F19 execution test. It is **not** K0/K1 promotion, not numerical identity, not proof of the F19 family mapping, not observational support, and not physical falsification. The authoritative K0/K1 run remains the only authority for its own frozen C0/Z0 gate.

`K0_promoted=false`, `K1_promoted=false`, `physical_falsification=false` for every outcome.
