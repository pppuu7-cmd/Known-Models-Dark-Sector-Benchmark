# M18 ghost condensate / dilatonic-ghost audit

Updated: 2026-09-10
Status: `BLOCKED_IMPLEMENTATION_REFERENCE_PROVIDER`

## Scope

Candidate provider: `KunhaoZhong/CLASS_GSF@07e015246c4b40f4e22bb50c9a0a63a621bb61f7`, model selector 1.

This audit covers only the provider/reference gate. It does not establish or reject the physical M18 family.

## K0 provenance

PASS_WITH_SCOPE.

The pinned source and committed author `dgf.ini` are public and the author point executes on GitHub Actions. The implementation states

`P(X,phi) = -X + c1 exp(lambda phi) X^2`.

The committed example encodes `lambda=0.2`, with `c1` at `gsf_parameters[6]` used as the closure-shooting parameter.

## Prospective K1 reference candidate

Preregistered before execution in
`protocol/W03_M18_GHOST_CONDENSATE_REFERENCE_PROBE_PREREGISTRATION_v0.1.md`.

For `lambda=0`,

`P(X)=-X+c1 X^2`, `P_X=-1+2 c1 X`.

The ghost-condensate stationary locus is `P_X=0`, so `c1 X=1/2`; then `P=-X/2`, `rho=2 X P_X-P=X/2`, and `w=-1`.

This supplied a physically motivated Lambda-like diagnostic reference path without changing the provider's initial-condition entries or closure-shooting index.

## Execution chronology

### Run 34435874904

Infrastructure only. Pinned solver build PASS. The harness failed before cosmological cases because it expected the wrong literal output-root string (`root = output/dgf_` rather than the author's `root = output/dgf`). No scientific conclusion. Physical preregistration was unchanged.

### Run 34435998290

Plumbing-only repair; same frozen physical cases.

Case exits:
- LCDM control: 0;
- unchanged author DGF point: 0;
- lambda-zero reference branch: 139 (segmentation fault).

Canonical result:
`waves/wave_03_expanded_dark_energy/M18_GHOST_CONDENSATE_REFERENCE_PROBE_RESULT.json`.

Immutable artifact:
`w03-m18-ghost-condensate-reference-probe`, Actions run `34435998290`.

The artifact contains fresh LCDM and author-DGF background/P(k) products, but no lambda-zero outputs.

## Source-level failure localization

The provider's shooting routine in `source/input.c` contains an explicit comment:

`BUG: problem if the guess is very good (f1~0) => no variation and no bracketing`.

Immediately afterward, for `fabs(f1)<1e-5`, it evaluates a step containing `f1/fabs(f1)`. At exact `f1=0` this is undefined. The lambda-zero symmetric reference can plausibly expose precisely this shooting singularity.

This is implementation evidence, not evidence that ghost condensate physics fails.

## Gate states

- K0: PASS_WITH_SCOPE
- K1: BLOCKED_IMPLEMENTATION_REFERENCE_PROVIDER
- K2-K9: NOT_TESTED
- B0: PASS_WITH_SCOPE
- remaining B-gates: not promoted

## Interpretation

The same pinned provider successfully builds and executes its author model-1 DGF point, so there is no provider-wide failure. The prospectively motivated lambda-zero reference branch is not executable under the provider's current closure-shooting implementation. KMDSB will not tune ICs post hoc or patch the third-party shooting algorithm to manufacture a passing K1 control.

M18 remains in the census and requires either:
1. an independently justified public ghost-condensate implementation with a clean reference/decoupling map; or
2. an author-supported reference prescription/version that avoids the shooting singularity.

No physical falsification, no observational claim, and no new-model necessity claim follows.