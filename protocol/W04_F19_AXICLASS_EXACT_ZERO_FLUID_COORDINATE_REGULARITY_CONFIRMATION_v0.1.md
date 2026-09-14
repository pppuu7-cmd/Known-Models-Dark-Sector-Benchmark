# W04 F19 AxiCLASS exact-zero fluid-coordinate regularity confirmation v0.1

Frozen: 2026-09-14 while authoritative K0/K1 run `34846931382` remains non-terminal.
Provider: `PoulinV/AxiCLASS@ae9609e1f96ddebbb6cc8a46de94512514c68781`.

## Trigger / prior exploration disclosure

Exploratory exact-source inspection after the long-running frozen Z0 execution identified a candidate coordinate singularity: the n=1 axion minimum with `scf_parameters=0,0` has zero scalar density and pressure, while the provider forms `w_scf=p_scf/rho_scf`; the frozen Z0 flags select the axionCAMB-like fluid perturbation representation. This confirmation gate is frozen **after** that hypothesis was identified and therefore does not claim discovery-level prospective independence. Its role is to independently verify the full source-control-flow chain with frozen positive/negative controls.

It does not read partial C0/Z0 outputs and cannot issue the K1 verdict.

## Frozen hypothesis

Under the exact frozen Z0 configuration:

- `scf_parameters = 0,0`;
- `scf_potential=axion`, `n_axion=1`;
- `scf_evolve_as_fluid=yes`;
- `scf_evolve_like_axionCAMB=yes`;
- `scf_has_perturbations=yes`;
- `use_delta_scf_over_1plusw=yes`;

AxiCLASS activates the scalar species, the exact field minimum gives `V=dV=rho_scf=p_scf=0`, `w_scf=p_scf/rho_scf` is non-finite, and the perturbation code selects `scf_fluid_variables=true` and consumes `w_scf` in fluid initial conditions and/or RHS/source expressions. Therefore the frozen exact-zero reference is a singular point of the provider's selected fluid perturbation coordinates, even though the underlying KG zero-field solution is regular.

## Required independent lanes

### R1 activation + exact-zero algebra

Confirm from exact source that `scf_parameters_size != 0` sets `has_scf=true`; for n=1 the potential and derivative vanish at phi=0; scalar kinetic contribution also vanishes for phi'=0; and source forms `w_scf=p_scf/rho_scf`.

### R2 frozen flag control flow

Parse the frozen Z0 INI embedded in the KMDSB authoritative workflow and verify all listed flags. Independently confirm from exact `perturbations.c` that these flags imply `scf_fluid_variables=true`.

### R3 downstream consumption

Confirm at least two distinct executable perturbation expressions use `index_bg_w_scf` under the fluid representation, including one initial-condition/vector path and one stress-energy/RHS/source path. Comments alone are insufficient.

### R4 numerical-coordinate witness

Using only the exact source formula identities, evaluate binary64 `rho=0`, `p=0`, `w=p/rho` semantics via an explicit safe witness (construct IEEE NaN rather than relying on Python ZeroDivisionError). Verify that comparisons/products representative of the source do not turn the NaN into an ordinary finite zero automatically.

## Frozen controls

Positive control: the author nonzero example (`scf_parameters=2,0`) has a nonzero n=1 potential at its initial field and does not realize `rho=p=0` at that initial point.

Negative control A: with `scf_has_perturbations=no`, the scalar perturbation fluid state must not be selected, regardless of background diagnostic `w_scf`.

Negative control B: with `scf_evolve_as_fluid=no` and `scf_evolve_like_axionCAMB=no`, the direct KG perturbation variables rather than fluid variables are selected.

These controls are structural only and are not alternative K1 references.

## Classification

All R1-R4 and controls pass:

`F19_AXICLASS_EXACT_ZERO_FLUID_COORDINATE_SINGULARITY_CONFIRMED_WITH_SCOPE`.

Otherwise:

`F19_AXICLASS_EXACT_ZERO_FLUID_COORDINATE_SINGULARITY_NOT_CONFIRMED`.

Infrastructure inability to complete the static confirmation:

`F19_AXICLASS_ZERO_REGULARITY_AUDIT_INFRASTRUCTURE_BLOCKED`.

## Interpretation ceiling

Even on confirmation:

- the still-running authoritative K1 workflow is not cancelled, duplicated or reclassified;
- this does not prove that the coordinate singularity is the unique cause of its runtime behavior;
- this does not make F19 physically fail;
- this does not authorize a post-hoc small-nonzero-field surrogate;
- if K1 later terminates BLOCKED, a new prospectively frozen provider-regular zero-abundance/reference gate may be designed, or an independent provider used, exactly as allowed by the parent K1 protocol;
- `K0_promoted=false`, `K1_promoted=false`, `K2_authorized=false`, `physical_falsification=false`.
