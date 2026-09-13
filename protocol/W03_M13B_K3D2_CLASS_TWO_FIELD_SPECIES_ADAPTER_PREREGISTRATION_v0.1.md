# W03 M13b K3D2 independent CLASS two-field species adapter preregistration v0.1

Date frozen: 2026-09-13  
Target: F13/M13b true two-field quintom  
Base: `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`  
Scope: first source adapter adding one independent phantom scalar species beside the existing canonical `scf`  
Author-model reproduction: **NO**

## Trigger

K3D1 proves that the exact CLASS pin builds/runs, contains the full Einstein-Boltzmann/recombination/output stack, and exposes exactly one direct canonical scalar-field background/perturbation species. K3C1/K3C2 independently define the cosmology-scale tanh mechanism and its crossing/perturbation regression targets.

K3D2 is the first authorized source modification. It must be minimal: extend the existing direct scalar species layer and summed stress-energy, while leaving the protected Boltzmann/thermodynamics machinery unchanged.

## Frozen normalization map for the independent adapter

This map is derived from CLASS's public units and K3C1, **not** from the blocked Goh-Taylor public V0 label.

CLASS documents:

- scalar field values in reduced-Planck units;
- internal cosmological dimensions primarily in Mpc powers;
- canonical scalar background density stored as
  `rho_scf = [phi_prime^2/(2a^2)+V_class]/3`.

K3C1 uses `U=V/rho_crit,0`, with `rho_crit,0=3 M_P^2 H0^2`.

Therefore the independent adapter freezes

`V_class(phi) = 3 H0^2 U_phi(phi)`

and similarly for `psi`, so that `V_class/3 = H0^2 U` in CLASS density units.

For the K3C1 tanh shape:

`U_i(x)=U0 [tanh(29(1-x))+1]`,

with exact canonical K3C1 fine value

`U0 = 0.3362232603714306`.

Hence

- `V_class = 3 H0^2 U`;
- `dV_class/dx = 3 H0^2 dU/dx`;
- `d2V_class/dx2 = 3 H0^2 d2U/dx2`.

No public Goh-Taylor amplitude or K3C0 diagnostic rescale is used.

## Frozen new species semantics

Keep upstream canonical `scf` semantics unchanged.

Add one independent phantom species, named `qpf` in the adapter to avoid implying upstream support.

Background variables:

- `psi_qpf`;
- `psi_prime_qpf`.

Phantom stress-energy in CLASS density units:

`rho_qpf = [-psi_prime^2/(2a^2)+V_qpf]/3`

`p_qpf   = [-psi_prime^2/(2a^2)-V_qpf]/3`.

Background equation:

`psi'' + 2 a H psi' - a^2 dV_qpf/dpsi = 0`.

Perturbation variables:

- `delta_psi_qpf`;
- `delta_psi_prime_qpf`.

In Newtonian gauge with CLASS metric variable `psi_metric`, phantom stress-energy contribution must be

`delta_rho_qpf = [-psi' delta_psi'/a^2 + psi'^2 psi_metric/a^2 + dV_qpf delta_psi]/3`

`delta_p_qpf = [-psi' delta_psi'/a^2 + psi'^2 psi_metric/a^2 - dV_qpf delta_psi]/3`

`[(rho+p)theta]_qpf = -(1/3) k^2 psi' delta_psi/a^2`.

Perturbed phantom KG equation must be the K3B1 covariant sign branch, expressed in the same CLASS gauge conventions as the existing canonical `scf`. No effective-fluid `theta_DE` or division by the combined dark-energy `rho+p` is permitted.

## Protected upstream semantics

The existing canonical `scf` equations, stress-energy signs and input meanings must remain byte-equivalent except where a shared array/index declaration must be extended mechanically.

The first K3D2 patch may modify only:

- `include/background.h`;
- `source/background.c`;
- `source/input.c` and associated input structure only for new qpf parameters/flags;
- `include/perturbations.h`;
- `source/perturbations.c`;
- output/background exposure only to emit qpf regression columns if required.

It may not modify physics inside:

- photon hierarchy;
- polarization hierarchy;
- ur/ncdm hierarchy;
- thermodynamics/recombination;
- primordial;
- nonlinear.

## Frozen K3D2-A gates: patch construction / reduction

Before a full two-field cosmology is interpreted, all must pass.

1. **Exact base integrity**: patch applies only to the frozen CLASS commit.
2. **Build**: patched CLASS builds successfully.
3. **Protected-subsystem diff**: no protected source file is changed.
4. **Standard-control regression**: with qpf absent and ordinary upstream inputs, the same frozen LambdaCDM control returns rc=0; its matter-power output agrees with unpatched exact-pin CLASS to normalized L2 <=`1e-10` on the common k-grid.
5. **Canonical-only reduction**: with qpf absent, the canonical `scf` source sign/equations remain identical to upstream by source audit; no new qpf code path executes.
6. **Phantom source-sign audit**: exact source expressions reproduce all frozen qpf background and perturbation signs above.
7. **No combined-rho+p denominator**: qpf evolution/source code contains no denominator built from total scalar `rho+p`, `rho_scf+p_scf+rho_qpf+p_qpf`, or an effective DE theta.
8. **Two-field indices distinct**: qpf gets independent background and perturbation state indices; no alias with `scf`.
9. **Independent normalization only**: adapter source/INI records K3C1 `U0=0.3362232603714306` and the CLASS map `V_class=3H0^2 U`; it must set `published_V0_reproduced=false` and `author_normalization_map_claimed=false`.
10. **Scope**: `K3` stays at most PARTIAL; no K4/K5 promotion; no physical falsification.

PASS classification:

`M13B_K3D2_CLASS_TWO_FIELD_SPECIES_ADAPTER_BUILD_AND_REDUCTION_PASS_WITH_SCOPE`.

This only establishes a source-clean executable adapter and exact null/control reduction. It does not yet prove that the two-field cosmology matches K3C1/K3C2.

If patch builds but any source/reduction/control gate fails:

`M13B_K3D2_CLASS_ADAPTER_REDUCTION_NOT_ESTABLISHED`.

If the patch cannot build/execute:

`M13B_K3D2_CLASS_ADAPTER_IMPLEMENTATION_BLOCKED`.

## Post-K3D2-A authorization

Only a K3D2-A PASS authorizes K3D2-B, which must run the full two-field adapter and compare:

- background crossing and E(a) against K3C1;
- direct field/metric response at selected modes against K3C2;
- CLASS full hierarchy outputs for finiteness/reproducibility.

K3D2-B thresholds must be prospectively frozen after K3D2-A but before its two-field outputs are inspected.
