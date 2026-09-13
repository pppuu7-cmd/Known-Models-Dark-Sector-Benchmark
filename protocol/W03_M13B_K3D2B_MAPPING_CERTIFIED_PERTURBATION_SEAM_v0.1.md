# W03 M13b K3D2-B mapping-certified perturbation seam diagnostic v0.1

Date: 2026-09-14

## Scope

This protocol is a numerical-coordinate recovery only. It does not change the frozen qcf/qpf open-interval equations, masses/signs, Einstein sources, Boltzmann hierarchy, precision tolerances, provider pin, K3C1/K3C2 z=5 IVP, or any B1/B2/B3 acceptance threshold.

Provider: `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.

Existing evidence to preserve:

- conditional background restart has strict disabled-null reduction;
- background U1/U2 seam sensitivity passed;
- native perturbation interval insertion is structurally authorized;
- direct qcf/qpf variables are explicitly copied by the adapter inside `perturbations_vector_init()`;
- A1/A2 perturbation starts obtained from `a -> z -> background_tau_of_z()` remain blocked at the first post-handoff interval;
- B1/B2/B3 remain unevaluated and no physical falsification is authorized.

## Motivation

`background_tau_of_z()` and `background_z_of_tau()` are independent spline interpolators. Therefore a 1- or 2-ULP displacement in physical scale factor need not survive the round trip used by `perturbations_derivs()`: `a_post -> z_post -> tau_post -> background_z_of_tau(tau_post) -> background_at_z(...)`.

The recovery must therefore be certified in the coordinate actually consumed by the perturbation RHS.

## Independent lanes

### S — source/remap audit

After the full frozen transformer stack, verify all of the following without running a cosmology:

1. the inserted z=5 interval duplicates the pre-existing approximation row on both sides;
2. `perturbations_vector_init()` receives the previous approximation row rather than `NULL` at the inserted boundary;
3. qcf/qpf perturbation variables are explicitly copied from the old vector to the new vector;
4. no tolerance, solver-family, Einstein-source, or Boltzmann-hierarchy equation is changed by this diagnostic.

### M — mapping certificate

For one enabled exact-pin CLASS realization, compute `tau_handoff = background_tau_of_z(z=5)` and the exact right-owned boundary `a_handoff = exp(log(1./6.))`.

Starting from `tau_handoff`, determine the *minimal representable* `tau_cert > tau_handoff` such that the same call path used by `perturbations_derivs()` — `background_at_tau(..., normal_info, inter_normal, ...)` — returns `a_cert > a_handoff`.

The search is prospective and algorithmic:

- define one local conformal-time ULP by `nextafter(tau_handoff,+inf)-tau_handoff`;
- use monotone exponential bracketing followed by integer binary search in ULP count;
- verify the immediate floating predecessor `nextafter(tau_cert,-inf)` returns `a <= a_handoff`;
- record `tau_handoff`, `tau_cert`, ULP count, `a(prev)`, `a(cert)`, and round-trip redshifts.

No manually chosen epsilon is permitted.

### R — first-RHS trace

Independently instrument the first post-handoff perturbation RHS calls without altering equations. Record at least `tau`, returned background `a`, qcf/qpf state components, qcf/qpf derivatives, and the solver lane. This lane is diagnostic only and cannot promote K3/K4/K5.

## Classification

- `M13B_K3D2B_MAPPING_CERTIFICATE_PASS_WITH_SCOPE`: M finds a finite minimal representable right-owned tau and verifies its predecessor is not right-owned.
- `M13B_K3D2B_MAPPING_CERTIFICATE_NOT_ESTABLISHED`: M cannot establish such a point within the frozen finite ULP search domain.
- `M13B_K3D2B_REMAP_AUDIT_PASS_WITH_SCOPE`: S passes all source/remap conditions.
- Any R result remains diagnostic and is not a physics verdict.

Only if S and M pass may a separately recorded implementation probe replace the post-handoff perturbation evolver lower bound by a mapping-certified tau. Full frozen B1/B2/B3 regression remains unauthorized until that implementation probe passes both default and reference solver lanes plus disabled-null reduction.

All blocker outcomes preserve `physical_falsification=false`, `K3_state_ceiling=PARTIAL`, `K4_promoted=false`, and `K5_promoted=false`.