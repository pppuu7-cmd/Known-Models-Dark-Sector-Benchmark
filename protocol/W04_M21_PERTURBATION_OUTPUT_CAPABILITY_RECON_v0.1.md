# W04 M21 perturbation-output capability recon v0.1

Frozen: 2026-09-14 after terminal thermodynamics secondary-state classification `M21_CMB_BRANCH_NOT_LOCALIZED_IN_EXPOSED_THERMO_STATE_COLUMNS` and terminal transfer-l phase classification `M21_L_GRID_PHASE_L400_SIGNATURE_SUPPORTED_WITH_SCOPE`, before any M21 perturbation/source branch-comparison output is generated.

Provider is exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Purpose and scope

This is a **non-scientific capability/schema recon**. It may inspect only the exact-CDM `ref` realization and MUST NOT compare `f2/f3/f4`, solver branches, tolerance branches, or transfer-l phase lanes. Its sole purpose is to freeze the native perturbation-output schema and a deterministic reference geometry before the next scientific branch-signature gate.

No result here may promote K1/K3/K4, select a production precision profile, establish a CLASS bug, or support a physical mixed-dark-matter verdict.

## Frozen realization

Generate the exact `ref.ini` with repository-owned `verification/m21/mixed_cold_warm_k1_reference.py prepare`.

Preserve its complete physical realization and standard output request. Add only:

- `write_thermodynamics = yes`;
- `k_output_values = 0.1` Mpc^-1.

The capability k value is a schema probe only and is not a scientific source anchor.

Precision profile is the exact M21 common baseline:

1. exact provider `cl_permille.pre`;
2. repository `verification/m21/m21_ncdm_tight.pre`;
3. `evolver = 0`;
4. no `thermo_evolver`, `tol_thermo_integration`, `l_logstep`, or `l_linstep` override beyond values already present in the two frozen baseline files.

Any unexpected duplicate/conflict in this merge is BLOCKED.

## Frozen outputs to inspect

The run must produce exactly one scalar native perturbation file corresponding to the requested `k_output_values=0.1`, plus the native background and thermodynamics tables already requested above.

Capability analysis may inspect only:

- perturbation header/title strings and numeric table shape;
- actual k reported by CLASS;
- whether all numeric perturbation rows are finite;
- exact background/thermodynamics title strings;
- reference conformal age `tau0` from the z=0 background row;
- reference recombination conformal time `tau_star`, defined prospectively as the thermodynamics row at maximum visibility `g`;
- `D_star = tau0 - tau_star`.

## Prospectively defined geometry anchors

If `D_star` is finite and positive, report-only candidate source anchors are defined **before any branch comparison** by

`k_l = l / D_star`

for exactly

`l_anchor = [100, 400, 800, 1200, 2000]`.

These five anchors are the only geometry-derived k values this recon may propose to the successor perturbation/source branch gate. No anchor may be added, removed, or moved after source-branch results are available.

The successor gate may round only to 12 significant decimal digits for serialization; the unrounded values must remain in its manifest.

## Capability PASS / BLOCKED

PASS classification:
`M21_PERTURBATION_OUTPUT_CAPABILITY_RECON_PASS_WITH_SCOPE`

requires all of:

1. exact provider HEAD;
2. exact-CDM ref case generated from the frozen repository generator;
3. common-baseline precision identity and duplicate-free profile;
4. CLASS rc=0;
5. exactly one scalar `perturbations_k*_s.dat` product;
6. a parseable non-empty title list and at least three finite numeric rows;
7. finite positive `D_star`;
8. five finite positive geometry anchors in strictly increasing order.

Any failure -> `M21_PERTURBATION_OUTPUT_CAPABILITY_RECON_BLOCKED`.

## Interpretation ceiling and successor authority

PASS establishes only that the exact pinned provider exposes a reproducible pre-transfer perturbation table and fixes a deterministic five-k reference geometry for a later preregistered scientific gate.

After PASS, a new protocol may freeze the perturbation/source branch-signature comparison across the already-terminal thermodynamics branch map. The capability result itself is not scientific evidence for or against M21.