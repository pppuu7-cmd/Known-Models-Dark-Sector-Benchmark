# W03 M13b K3D2 pre-execution architecture amendment v0.1

Date frozen: 2026-09-14
Parent preregistration: `protocol/W03_M13B_K3D2_CLASS_TWO_FIELD_SPECIES_ADAPTER_PREREGISTRATION_v0.1.md`
Base: `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`
Status: prospective amendment frozen before any K3D2 patched-build or two-field output is inspected.

## Trigger

The post-preregistration source-architecture audit found a structural mismatch that makes the literal `existing scf + new qpf` implementation unsuitable for the already frozen K3C1/K3C2 regression target:

- K3C1 evolves **both** direct fields with the same independent tanh potential family
  `U_i(x)=U0[tanh(29(1-x))+1]`;
- upstream CLASS `scf` uses its existing exponential/power potential family and must remain unchanged under the K3D2 protected-upstream requirement.

Therefore an adapter that leaves upstream `scf` unchanged and adds only `qpf` could satisfy a null/build audit but could not represent the same two-field realization used by K3C1/K3C2. Proceeding with that implementation would knowingly create a non-regressable branch.

## Amended implementation architecture

Keep upstream `scf` completely unchanged and use it only as an upstream regression-control species.

Add two **independent adapter species**:

- `qcf`: canonical direct scalar used by the independent M13b benchmark;
- `qpf`: phantom direct scalar used by the independent M13b benchmark.

Both use the frozen K3C1 tanh shape and normalization map. No upstream `scf` input, equation, potential, stress-energy expression, or perturbation path is redefined for the benchmark.

This amendment deliberately increases the adapter state by one additional canonical species in order to preserve upstream semantics exactly and make the later K3C1/K3C2 regression well-defined.

## Frozen qcf semantics

Background variables:

- `phi_qcf`;
- `phi_prime_qcf`.

Canonical stress-energy in CLASS density units:

`rho_qcf = [phi_prime^2/(2a^2)+V_qcf]/3`

`p_qcf   = [phi_prime^2/(2a^2)-V_qcf]/3`.

Background equation:

`phi'' + 2 a H phi' + a^2 dV_qcf/dphi = 0`.

Newtonian-gauge perturbation stress-energy:

`delta_rho_qcf = [phi' delta_phi'/a^2 - phi'^2 psi_metric/a^2 + dV_qcf delta_phi]/3`

`delta_p_qcf = [phi' delta_phi'/a^2 - phi'^2 psi_metric/a^2 - dV_qcf delta_phi]/3`

`[(rho+p)theta]_qcf = +(1/3) k^2 phi' delta_phi/a^2`.

Perturbed qcf KG equation must follow the same covariant canonical sign branch already frozen by K3B1/K3B2.

## Frozen qpf semantics

The qpf semantics remain exactly those in the parent preregistration:

`rho_qpf = [-psi_prime^2/(2a^2)+V_qpf]/3`

`p_qpf   = [-psi_prime^2/(2a^2)-V_qpf]/3`

`psi'' + 2 a H psi' - a^2 dV_qpf/dpsi = 0`

with direct `delta_psi_qpf`, `delta_psi_prime_qpf` perturbations and the frozen phantom Newtonian-gauge stress-energy signs.

## Shared frozen potential and normalization

For `s=29` and `U0=0.3362232603714306`:

`U(z)=U0[tanh(29(1-z))+1]`

for the corresponding reduced-Planck field coordinate `z`.

For both qcf and qpf:

`V_class = 3 H0^2 U`

`dV_class/dz = 3 H0^2 dU/dz`

`d2V_class/dz2 = 3 H0^2 d2U/dz2`.

The public Goh-Taylor amplitude is not used. `published_V0_reproduced=false` and `author_normalization_map_claimed=false` remain mandatory.

## K3D2-A gates after amendment

All numerical and scope gates of the parent preregistration remain unchanged or become stricter:

1. exact frozen CLASS base only;
2. patched build succeeds;
3. protected Boltzmann/thermodynamics/primordial/nonlinear files unchanged;
4. qcf/qpf absent: standard LambdaCDM matter-power normalized L2 versus exact unpatched pin <= `1e-10`;
5. upstream `scf` source/input/potential/stress-energy path remains byte-identical except mechanically shifted shared declarations if unavoidable;
6. qcf source signs match the canonical formulas frozen above;
7. qpf source signs match the phantom formulas frozen in the parent preregistration;
8. no qcf/qpf/effective-DE evolution divides by combined scalar `rho+p`;
9. qcf, qpf and upstream scf have distinct background and perturbation state indices;
10. adapter source records the exact K3C1 `U0` and `V_class=3H0^2U` map;
11. K3 remains at most PARTIAL; K4/K5 remain closed; physical_falsification=false.

The K3D2-A PASS label remains:

`M13B_K3D2_CLASS_TWO_FIELD_SPECIES_ADAPTER_BUILD_AND_REDUCTION_PASS_WITH_SCOPE`

where `TWO_FIELD` now refers specifically to the independent `qcf+qpf` realization; upstream `scf` is a protected regression-control and is not part of that realization.

## K3D2-B authorization

Only K3D2-A PASS authorizes K3D2-B. K3D2-B must run `qcf+qpf`, not upstream `scf+qpf`, and compare the same realization against K3C1/K3C2. Its thresholds remain prospectively frozen after K3D2-A and before two-field outputs are inspected.
