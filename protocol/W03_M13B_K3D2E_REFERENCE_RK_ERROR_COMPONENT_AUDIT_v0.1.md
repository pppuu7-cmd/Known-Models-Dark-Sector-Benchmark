# W03 M13b K3D2-E reference-RK first-step error-component audit v0.1

Date frozen: 2026-09-14

## Trigger

Canonical K3D2-D result:

`M13B_K3D2D_SELF_CONSISTENT_REFERENCE_RK_NUMERICAL_BLOCKER_LOCALIZED`.

The exact pinned `cl_ref.pre` reaches the self-consistent gauge-IVP boundary fixed point and then explicit RK fails on the first post-handoff RK step for 388 intermediate-k modes. Frozen K1/K10 do not fail. Reference B1/B2/B3 and default/reference reproducibility were therefore not evaluated.

## Purpose

Determine which integrated perturbation-vector components dominate the explicit RK Cash-Karp local-error control at the first post-handoff collapse, without changing the solver, tolerance, minimum variation, equations, state, seam, cosmology, or initial surface.

This is diagnostic only. It does not attempt to rescue `cl_ref.pre`.

## Exact authority and stack

Preserve exactly:

- provider `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`;
- exact upstream `cl_ref.pre` unchanged (`evolver=0`, `tol_perturbations_integration=1.e-6`);
- self-consistent qcf/qpf gauge-IVP fixed point (pure undamped Picard, max 16, target <=`1e-12`);
- mapping-certified perturbation seam at exactly 12 local tau ULP;
- full cosmology/output request from K3D2-D;
- existing diagnostic-only collapse-geometry and mode-failure wrappers.

## Output-only RK instrumentation

The diagnostic patch may modify only:

- `include/dei_rkck.h` to add diagnostic workspace fields;
- `tools/dei_rkck.c` to populate those fields and enrich the existing minimum-step error text;
- `source/perturbations.c` to append a runtime perturbation-vector index map to the existing mode-failure line.

It MUST NOT modify any numerical branch or quantity used by the integrator.

### Required error-control decomposition

Inside `rkqs()` retain the original calculation

`errmax = max_i |yerr[i]/yscal[i]| / eps`

unchanged.

In addition, for each call record diagnostically:

- number of Cash-Karp attempts before acceptance;
- component index maximizing `|yerr_i/yscal_i|` on the first attempt;
- first-attempt raw max `|yerr_i/yscal_i|` and normalized `errmax`;
- component index maximizing the ratio on the final accepted attempt;
- final raw max ratio and normalized `errmax`;
- at the final dominant index: `yerr`, `yscal`, current `y`, and start-of-generic-step `dydx`.

The existing `hnext/minimum/hdid/step_index` geometry remains unchanged.

### Required perturbation-vector runtime map

For each `KMDSB_MODE_FAIL`, append at least:

- `pt_size`;
- `index_pt_eta`;
- photon `delta_g,theta_g,shear_g,l3_g,l_max_g,pol0_g,l_max_pol_g`;
- baryon `delta_b,theta_b`;
- CDM `delta_cdm,theta_cdm`;
- ur `delta_ur,theta_ur,shear_ur,l3_ur,l_max_ur`;
- qcf `phi_qcf,phi_prime_qcf`;
- qpf `psi_qpf,psi_prime_qpf`.

No perturbation values are changed by this map.

## Frozen analysis

Parse every unique failing mode. For strict-clean diagnostic records report:

1. frequency distribution of first-attempt dominant component index;
2. frequency distribution of final accepted-attempt dominant component index;
3. fraction of failures dominated by qcf or qpf direct-field indices;
4. fraction dominated by standard metric/matter/photon/ur hierarchy indices or ranges when identifiable from the runtime map;
5. Cash-Karp attempt-count range/distribution;
6. first and final normalized errmax ranges;
7. whether the dominant component changes during shrinkage;
8. k-dependence of the dominant component over the already-established failure island.

Malformed/interleaved stderr diagnostics must be retained as provenance and excluded only from quantitative component-frequency denominators when the required fields are not parseable.

## Frozen classifications

If provider reproduces the same numerical blocker and at least 100 strict-clean failures contain valid first/final component decomposition:

`M13B_K3D2E_REFERENCE_RK_ERROR_COMPONENTS_LOCALIZED`.

If provider unexpectedly completes, do not infer a reference PASS from this diagnostic workflow; classify

`M13B_K3D2E_REFERENCE_DIAGNOSTIC_EXECUTION_CHANGED_UNEXPECTEDLY`

and require a separate preregistered scientific reference run.

If instrumentation/provenance fails:

`M13B_K3D2E_REFERENCE_RK_COMPONENT_AUDIT_IMPLEMENTATION_BLOCKED`.

## Claim ceiling

This audit may identify a numerical stiffness/error-control sector but cannot authorize tolerance relaxation, `minimum_variation` changes, solver replacement, equation changes, or K4 promotion.

All outcomes preserve:

- default NDF15 B1/B2/B3 PASS_WITH_SCOPE;
- reference B1/B2/B3 NOT_EVALUATED while provider rc != 0;
- `K3_state_ceiling=PARTIAL`;
- `K4_promoted=false`;
- `K5_promoted=false`;
- `physical_falsification=false`.
