# M15 IDECAMB decomposed-NGCG candidate audit

Updated: 2026-09-10
Status: `BACKGROUND_EQUIVALENT_MOMENTUM_FRAME_BOUND_EXACT_PERTURBATION_BINDING_REJECTED`
Scientific promotion as an exact M15 provider: **NO**
Physical falsification of NGCG: **NO**

## Candidate provenance

Pinned provider/infrastructure:

- `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`
- intended overlay base: `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`
- IDECAMB methodology: arXiv:2306.01593 and the extended PPF framework arXiv:1404.5220.

No M14 coupled-quintessence scientific result is reused here. Only pinned build/provenance infrastructure is shared.

## 1. Input and source binding

The author `test_ide.ini` documents:

- `Class_IDE = 1` for coupled-fluid models;
- `WForm_CF = 1` for CPL and `WForm_CF = 2` for HDE;
- `QForm_CF = 1..4` for the four documented linear interaction forms;
- `CovQForm_CF = 1` for `Q_mu = Q u_mu,c` and `CovQForm_CF = 2` for `Q_mu = Q u_mu,de`.

In the pinned source `camb/equations_ppfi.f90`, the `default` branch of `Coup_CF` is explicitly labelled as the NGCG model and evaluates

`Q = -3 w_de beta_cf H rho_de rho_c/(rho_de + rho_c)`

(up to the source conformal/8-pi-G normalization). The source comment states that `beta_cf` represents the NGCG `alpha`.

Important provenance limitation: the author INI documents only `QForm_CF=1..4`; the NGCG branch is reachable only through the Fortran `default` case, i.e. an out-of-enumeration integer value. Therefore this branch is **source-addressable but author-interface-undocumented**. KMDSB does not invent a canonical selector value and does not promote this fact alone to an executable M15 prescription.

## 2. Frozen background parameter map

For the constant-w decomposed NGCG used in Li & Zhang, arXiv:1312.6328, the interaction is

`Q_pub = 3 beta_pub H rho_de rho_c/(rho_de + rho_c)`

with the NGCG relation

`beta_pub = -alpha_NGCG w`.

Comparing this with the IDECAMB source branch gives the convention map

`beta_cf = alpha_NGCG`,

`beta_pub = -w beta_cf`.

Thus the source branch has the correct decomposed-NGCG **background interaction form** for fixed constant `w`.

The corresponding reference limit is now source-bound:

`beta_cf -> 0` at fixed `w` -> uncoupled constant-w XCDM.

Only the special choice `w=-1` further collapses this comparator to LambdaCDM. The M15 reference must therefore not be silently replaced by LambdaCDM for a general fixed-w NGCG/XCDM anchor.

## 3. Momentum-transfer prescription binding

Li & Zhang (arXiv:1312.6328) choose the geodesic decomposed-NGCG prescription with energy-momentum transfer parallel to the dark-matter four-velocity, i.e. no momentum transfer in the dark-matter rest frame.

The IDECAMB source implements

- `CovQForm_CF=1`: `gD(1)=0`, `gD(2)=gQ`, corresponding to `Q_mu = Q u_mu,c`;
- `CovQForm_CF=2`: the alternative DE-frame transfer.

Therefore `CovQForm_CF=1` is the correct momentum-frame choice for the published geodesic decomposed-NGCG comparator. This closes the momentum-frame part of the binding.

For the equation of state, `WForm_CF=1` with `w1=0` supplies the constant-w XCDM component required by the same decomposition. This closes the background EoS selector part of the binding.

## 4. Exact perturbation-closure comparison

The decisive obstruction is the energy-transfer perturbation closure.

For the direct gauge-invariant geodesic decomposed-NGCG treatment in arXiv:1312.6328, writing

`R_c = rho_c/(rho_de + rho_c)`,

the perturbed transfer contains

`delta Q = Q [delta H/H + R_c delta_de + (1-R_c) delta_c]`.

The paper explicitly notes that the perturbation of the expansion rate, `delta H`, is required for the fully gauge-invariant equations of an H-dependent interaction.

By contrast, the IDECAMB extended-PPF parametrization in arXiv:2306.01593 treats the nonlinear interaction `Q proportional to H rho_de rho_c/(rho_de+rho_c)` with the five-function assignment

`C1=Q, C2=Q, C3=0`,

and, for the DM-frame choice,

`D1=0, D2=Q`.

Equivalently, its parametrized transfer perturbation uses the density terms but omits an explicit `delta H` contribution; the IDECAMB paper states that this omission is part of its adopted parametrization while noting the gauge-invariance issue for an H-dependent interaction.

The pinned source agrees with that mapping: the NGCG/default branch sets `gC(1)=gQ`, `gC(2)=gQ`, `gC(3)=0`.

Therefore:

- the **background interaction** is NGCG-equivalent;
- the **momentum-transfer frame** can be bound to the geodesic decomposed-NGCG choice;
- but the pinned IDECAMB perturbation closure is **not the same explicit gauge-invariant delta-Q closure** used by the published geodesic decomposed-NGCG model.

Extended PPF may be a useful stable interacting-fluid representation, but that does not prove exact perturbation-level equivalence to the M15 NGCG response family. KMDSB must not promote a background equivalence into an exact perturbation-family equivalence.

## 5. M15 decision

For this provider candidate:

- K0 provenance: `PARTIAL_SOURCE_ONLY_SELECTOR`;
- background family identity: `PASS_WITH_SCOPE`;
- EoS selector: `BOUND_CONSTANT_W` (`WForm_CF=1`, `w1=0`);
- parameter convention: `BOUND` (`beta_cf=alpha_NGCG`, `beta_pub=-w beta_cf`);
- reference comparator: `BOUND_UNCOUPLED_CONSTANT_W_XCDM`;
- momentum-transfer frame: `BOUND_GEODESIC_DM_FRAME` (`CovQForm_CF=1`);
- exact perturbation-family identity: `REJECTED_EXACT_BINDING`;
- K1-K9 numerical M15 scoring from this provider: **NOT AUTHORIZED**.

Classification:

`M15_IDECAMB_BACKGROUND_EQUIVALENT_BUT_EXACT_PERTURBATION_PROVIDER_REJECTED`

This is a **provider/representation rejection, not a falsification of generalized Chaplygin gas or decomposed NGCG physics**.

## 6. Next allowed M15 route

Do not spend compute on an IDECAMB M15 grid merely by assigning an undocumented `QForm_CF` integer. Instead search for an independent provider that exposes one of the two physically defined decomposed/unified Chaplygin perturbation prescriptions explicitly:

1. geodesic decomposed NGCG/GCG with the corresponding gauge-complete transfer perturbation; or
2. barotropic/unified GCG/NGCG with its stated nonzero effective/adiabatic sound-speed closure.

Only after a provider, exact commit/version, parameter map, reference limit, and perturbation prescription are frozen should M15 K1/K2/K3/K4 be preregistered.

## Methodological lesson retained for future DSIR/KMDSB model construction

Background duality is insufficient for response-family identity. A candidate model can share `H(a)` and the homogeneous interaction law with a known model while differing in `delta Q`, momentum transfer, sound-speed closure, or gauge completion. The DSIR funnel therefore needs an explicit **perturbation-closure identity gate before numerical multichannel rank/discrimination tests** whenever a background-equivalent decomposition is used.
