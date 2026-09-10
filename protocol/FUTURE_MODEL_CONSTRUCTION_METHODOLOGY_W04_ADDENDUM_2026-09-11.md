# Future-model construction methodology — W04 addendum (2026-09-11)

Status: EVIDENCE-FED ADDENDUM to `FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.2.md`.

This file records durable rules discovered after the v0.2 document was written. It does not rewrite older frozen gates.

## A1 — Parameter-presence semantics are part of the physical reference map

A numerical control parameter is not defined only by its floating-point value. In solver interfaces, the *presence of the input key* can select a branch, alter defaults, change approximation schemes, or modify auxiliary physical assumptions.

Before declaring an omitted-key configuration and an explicit-zero configuration equivalent:
1. audit the parser/source path for presence-dependent defaults;
2. freeze every induced auxiliary setting explicitly on both sides;
3. verify zero-versus-omitted identity numerically when the solver permits it;
4. if identity fails, classify input/reference semantics before interpreting physics.

M23 calibration: supplying `Gamma_0_nadm` in CLASS switches the default interaction temperature index to `nindex_idm_dr=0` and the interacting-radiation nature to `fluid`; omitting the key restores different defaults. The clean decoupling reference therefore explicitly fixes those properties while varying only the interaction strength.

Construction consequence for a future model: the reference-limit test harness must store not only parameter values but also branch selectors and all presence-dependent defaults. A reference is a complete physical configuration, not a sparse parameter dictionary.

## A2 — Qualitative 'unaffected' statements do not establish a strict null response

A provider example, plot caption, README statement or visual claim that an observable is 'not affected' does not justify a numerical zero-response threshold unless the source equations or an independent precision study establish that null.

M22 calibration: a provider example described P(k) as not affected by p_ann at the example level, but a prospectively frozen same-solver test measured a small, smooth P(k) response. The response decreased monotonically toward the exact no-injection limit with a small-tail power near 0.92. The frozen v1 negative-control threshold correctly remained failed; the scientific interpretation changed only in a separately preregistered v2.

Construction consequence:
- distinguish an exact symmetry/selection-rule null from a visually or practically negligible response;
- use continuity/scaling tests for the latter;
- promote a strict negative control only from an equation-level null, exact source path, or dedicated precision bound;
- never loosen a frozen threshold after observing a nonzero channel.

## A3 — Decoupling preserves species content unless species removal is itself the tested coordinate

For an interaction family, K1 normally sends the interaction strength to zero while keeping the participating species, background densities, radiation nature, masses and closure prescription fixed. Deleting a species at the same time probes a different composite path.

M23 calibration: the correct simple DM-DR scattering reference retains `f_idm=1` and nonzero `N_idr`, and removes only the DM-DR scattering rate. Comparison to ordinary LambdaCDM belongs to later nearest-family/observation-space gates, not the interaction-decoupling identity itself.

Construction consequence: future-model reference maps should expose separate coordinates for species content and coupling strength and test each decoupling path independently.

## Promotion status
These rules are durable methodological constraints supported by controlled W04 cases, but their design-prior ledger level must still be governed by the normal evidence/promotion policy. They do not by themselves establish `NEW_REQUIRED`.
