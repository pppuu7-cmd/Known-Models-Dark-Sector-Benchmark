# W04 F19 AxiCLASS K1 conditional split-execution recovery v0.1

Frozen: 2026-09-14 while authoritative run `34846931382` is still non-terminal.

Status: **CONDITIONAL / NOT AUTHORIZED TO EXECUTE YET**.

Parent scientific contract: `protocol/W04_F19_AXICLASS_INDEPENDENT_PROVIDER_K0K1_PROBE_v0.1.md`.
Provider: `PoulinV/AxiCLASS@ae9609e1f96ddebbb6cc8a46de94512514c68781`.

## Activation condition

This recovery may be executed only if run `34846931382` becomes terminal without a valid frozen K1 verdict because the combined `Frozen C0 and exact Z0 executions` step is cancelled, times out, is externally terminated, or otherwise ends before the unchanged frozen metric analyzer can classify both raw branches.

If run `34846931382` completes and yields a valid K1 classification, this recovery is **not authorized** and must remain historical preparation only.

## Recovery scope

The recovery changes orchestration/observability only:

1. fresh exact-pin build identity remains unchanged;
2. C0 INI is byte-identical in all scientific fields to the parent recovery workflow;
3. Z0 INI is byte-identical in all scientific fields to the parent recovery workflow;
4. C0 and Z0 execute in separate jobs/runners instead of sequentially inside one shell step;
5. each branch uploads provider return code, stdout/stderr, INI hash, background product and P(k) product immediately after its own execution when available;
6. a barrier/aggregate waits for both branch jobs, then applies exactly the parent frozen K1 metrics and thresholds;
7. no branch may inspect the other branch's substantive values before its own execution;
8. source audit and already terminal author-control evidence may be reused by immutable artifact/hash identity when allowed by GitHub retention, otherwise repeated without changing source or inputs.

## Explicitly forbidden changes

- no small nonzero `scf_parameters` surrogate;
- no switch from fluid variables to KG variables;
- no change to `scf_evolve_as_fluid`, `scf_evolve_like_axionCAMB`, `scf_has_perturbations`, `use_delta_scf_over_1plusw`, `use_big_theta_scf`, `use_ppf`, or include-scf flags;
- no change to `m_axion`, `f_axion`, gauge, cosmological parameters, primordial parameters, k range, precision defaults, output products or CDM density;
- no tolerance or K1 threshold change;
- no provider source patch to regularize `w_scf`;
- no interpretation of infrastructure termination as physical F19 failure.

## Frozen branch identities

C0 remains vanilla AxiCLASS with no scalar-field component and standard CDM carrying the frozen matter density.

Z0 remains the exact scalar-zero branch with:

- `scf_potential=axion`;
- `n_axion=1`;
- `f_axion=0.02`;
- `m_axion=1e8`;
- `scf_parameters=0,0`;
- `scf_tuning_index=0`;
- `scf_evolve_as_fluid=yes`;
- `scf_evolve_like_axionCAMB=yes`;
- `threshold_scf_fluid_m_over_H=3`;
- `do_shooting=no`;
- `do_shooting_scf=no`;
- `scf_has_perturbations=yes`;
- `use_big_theta_scf=no`;
- `use_delta_scf_over_1plusw=yes`;
- `attractor_ic_scf=no`;
- `use_ppf=no`;
- `include_scf_in_delta_m=yes`;
- `include_scf_in_delta_cb=no`.

## Frozen metric authority

Unchanged parent thresholds:

- max symmetric relative difference in background `H [1/Mpc]` <= `1e-10`;
- max symmetric relative difference in same-source CDM density <= `1e-10`;
- max symmetric relative difference in linear P(k) <= `1e-8`.

Classification strings remain exactly those of the parent contract:

- PASS: `F19_AXICLASS_EXACT_ZERO_FIELD_K1_PASS_WITH_SCOPE`;
- finite identity failure: `F19_AXICLASS_EXACT_ZERO_FIELD_K1_FAIL_NUMERICAL_IDENTITY`;
- Z0 cannot execute / nonfinite: `F19_AXICLASS_EXACT_ZERO_FIELD_REFERENCE_BLOCKED_IMPLEMENTATION`.

## Relation to the exact-zero coordinate singularity result

`F19_AXICLASS_EXACT_ZERO_FLUID_COORDINATE_REGULARITY_RESULT.json` confirms a structural provider-coordinate singularity under the frozen Z0 flags. That result may motivate observability and later provider-regular reference design, but it does **not** alter this exact-replay recovery. The split recovery intentionally asks the original frozen question once more with branch-level observability before any new reference object is defined.

## Interpretation ceiling

This document authorizes no execution while run `34846931382` is non-terminal. It is a conditional control-only recovery plan. `K0`, `K1`, `K2` and physical F19 status do not change by creating this document.
