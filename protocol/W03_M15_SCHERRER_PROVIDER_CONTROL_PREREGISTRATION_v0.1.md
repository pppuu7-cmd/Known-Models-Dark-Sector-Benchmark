# W03/W06 M15 — Scherrer unified-dark-sector provider control v0.1

Status: **FROZEN BEFORE PROVIDER-CONTROL RUN**

## Why this is M15/unified-sector evidence, not M11 promotion

Candidate provider:
`Eladio-Moreno/k-essence-dynamics@f3f010e1ed74c86ce6a431a435fa93988f749ee2`, directory `Cuadratico/`.

Source inspection shows a modified hi_class covariant scalar branch labelled Scherrer. The code defines

\[
X=y_{\rm sch}+X_0,
\]

and, for the modified `quintessence_monomial` branch,

\[
G_2=P(X,\phi)=-F_0+F_2(X-X_0)^2-\frac12 m_\phi^2\phi^2.
\]

The author-supplied `Cuadratico/hi.ini` sets `Omega_cdm=0` while supplying `DM_schm=0.26`. Thus the same scalar is intended to supply a dark-matter-like and dark-energy-like budget. This is **not** the same bookkeeping as the M11 DE-only sound-speed representative. It is therefore a candidate Scherrer/unified-dark-sector subfamily for M15/W06, not a rescue of M11b.

## Provenance limitations known before run

- Root README is nearly empty.
- Repository history is sparse.
- The nested `Cuadratico/README.md` is generic CLASS documentation rather than a model-specific validation document.
- Nevertheless, source modifications are explicit, `hi.ini` contains concrete Scherrer parameters, and standard hi_class stability controls are present.

Because provenance is mixed, the first gate is executable provider reproduction only.

## Frozen provider-control procedure

1. Clone exact commit `f3f010e1ed74c86ce6a431a435fa93988f749ee2`.
2. Enter `Cuadratico/`.
3. Build the provider's `class` binary with its committed Makefile; no source edits.
4. Delete any pre-existing `output/hi*` products so committed/stale outputs cannot satisfy the gate.
5. Run the author-supplied `hi.ini` **without changing any physical, stability or precision parameter**.
6. Record build/run exit codes and retain full logs.
7. Require at least one fresh cosmological output file from the requested output set. Prefer fresh background and matter-power products when produced, but absence of background alone is not a failure if the unmodified author file did not request it.
8. Hash/list all newly produced `output/hi*` files.

## Terminal classifications

- `SCHERRER_PROVIDER_CONTROL_PASS`: build=0, `hi.ini` run=0, and at least one fresh requested output product exists.
- `SCHERRER_PROVIDER_CONTROL_FAIL_BUILD`: exact source does not build.
- `SCHERRER_PROVIDER_CONTROL_FAIL_EXAMPLE`: build succeeds but the unmodified author example fails or produces no fresh output.

No outcome scores K1–K9/B1–B9 for the Scherrer model. PASS only authorizes a separate scientific preregistration that must define:
- the exact field/budget bookkeeping;
- stability quantities and admissible domain;
- a recoverable LCDM/known-family reference or decoupling path;
- the response channels and grids;
- comparator manifold(s), including generalized Chaplygin and effective GDM where appropriate.

If provider control fails, record a provider implementation/provenance blockage. Never retune `hi.ini` post hoc as part of this control.
