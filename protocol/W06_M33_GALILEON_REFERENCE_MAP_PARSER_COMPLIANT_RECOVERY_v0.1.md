# W06 M33 Galileon reference-map parser-compliant recovery v0.1

## Status
Prospectively frozen before rerun. This is an implementation/configuration recovery only; it cannot promote K1.

## Parent evidence
Run `34657647905`, artifact `10286258353`, pinned `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`.

All parent arms terminated at the provider input parser. The pinned parser states that when non-negative `Omega_smg` is supplied, `Omega_Lambda` and `Omega_fld` must be left unspecified. The parent harness instead retained explicit closure entries. The plain-GR endpoint likewise retained an explicit closure assignment incompatible with provider closure semantics. This is configuration evidence only.

## Frozen provider and cosmology
Provider commit, H0, omega_cdm, omega_b, A_s, n_s, tau_reio, output channels and provider cubic Galileon model are unchanged.

## Allowed repair
Only closure-key construction is changed:

1. Positive Galileon discovery arms use `Omega_smg={0.5,0.1,0.01,0.001}` and remove both `Omega_Lambda` and `Omega_fld` lines entirely so provider closure/shooting semantics control the remaining budget.
2. Native provider control keeps the author-shipped `galileon_3.ini` closure (`Omega_Lambda=0`, `Omega_fld=0`, `Omega_smg=-1`) unchanged except output root.
3. Plain-GR control removes `Omega_smg`, `gravity_model`, `gravity_submodel`, `Omega_Lambda`, and `Omega_fld`, leaving standard CLASS closure to determine Lambda from the unchanged cosmological inputs.
4. No thresholds or physics parameters may be tuned after execution.

## Frozen classification
- `PARSER_COMPLIANT_REFERENCE_MAP_EXECUTABLE`: GR control, native provider control, and at least one positive-Omega_smg arm exit 0 with finite TT and P(k).
- `PARSER_COMPLIANT_REFERENCE_MAP_PARTIAL`: at least one arm executes finitely, but the full executable-control condition is not met.
- `PARSER_COMPLIANT_REFERENCE_MAP_BLOCKED_IMPLEMENTATION`: no arm produces finite TT and P(k).

All outcomes keep `K1_promoted=false` and `physical_falsification=false`. If executable, a separate preregistered K1 continuity/reference gate is required.
