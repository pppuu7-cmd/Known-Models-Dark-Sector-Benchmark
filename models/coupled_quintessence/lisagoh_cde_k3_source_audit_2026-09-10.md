# M14 LisaGoh/CDE K3 conservation / gauge / closure audit

Updated: 2026-09-10
Provider: `LisaGoh/CDE@b85a675af7544a5183e402964550811aa805b698`
Publication anchor: Goh, Gómez-Valent, Pettorino & Kilbinger, Phys. Rev. D 107, 083503 (2023), arXiv:2211.13588v2
Status: `K3_SOURCE_EQUATION_MATCH_PASS_WITH_SYNCHRONOUS_SCOPE_NUMERICAL_REFERENCE_BLOCKED`
Physical family falsification: **NO**

## 1. Covariant interaction and conservation

The publication defines a mass-varying CDM / canonical-scalar dark sector and writes the covariant exchange as

`nabla^mu T^phi_{mu nu} = + kappa beta T_cdm nabla_nu phi`,

`nabla^mu T^cdm_{mu nu} = - kappa beta T_cdm nabla_nu phi`.

The two source terms are equal and opposite, hence the total dark-sector energy-momentum tensor is conserved. Baryons are explicitly uncoupled.

This is the intended M14 conformal/mass-varying coupled-quintessence mechanism rather than a generic phenomenological fluid interaction.

## 2. Background equation-to-source mapping

The paper gives, in conformal time,

`phi'' + 2 Hconf phi' + a^2 V_phi = kappa beta a^2 rho_c`,

`rho_c' + 3 Hconf rho_c = - kappa beta rho_c phi'`.

The pinned `background.c` actively evolves

`rho_cdm' = -3 a H rho_cdm - sqrt(6) beta rho_cdm phi'`,

and

`phi'' = -a(2 H phi' + a V_phi) + sqrt(6) beta rho_cdm a^2`.

Here the provider uses its internal dimensionless scalar normalization, producing the `sqrt(6)` convention. Signs and paired exchange structure agree: energy lost by CDM is sourced into the scalar equation.

The publication and the pinned main source both use a constant potential for this tomographic analysis, so `V_phi=V_phiphi=0` in the executed branch.

## 3. Tomographic coupling and derivative mapping

The public source defines `beta(a)` as the smooth three-bin tanh interpolation in redshift from `beta_1,beta_2,beta_3`; `beta_prime` is explicitly documented in source as `d beta/dz`.

The paper perturbation equations are written using `partial beta / partial phi`. Since

`a=1/(1+z)`, `a' = a^2 H`,

one has

`z' = -H`,

and therefore along the background trajectory

`(partial beta/partial phi) phi' = d beta/dtau = - H d beta/dz`.

This exactly explains the sign and H factor of the provider's `beta_prime` terms. They are not an ad-hoc change of the published system.

## 4. CDM perturbations

The publication's synchronous-gauge equations are

`delta_c' = -theta_c - h'/2 - kappa beta delta_phi' - kappa beta_phi phi' delta_phi`,

`theta_c' = (-Hconf + kappa beta phi') theta_c - k^2 kappa beta delta_phi`.

The pinned `perturbations.c` actively implements

`delta_c' = -(theta_c + h'/2) - sqrt(6) beta delta_phi' + sqrt(6) H beta_z delta_phi`,

`theta_c' = (-aH + sqrt(6) beta phi') theta_c - k^2 sqrt(6) beta delta_phi`.

Using `beta_phi phi' = -H beta_z`, these are the same equations in the provider normalization.

This directly resolves the key defect of the earlier `kabeleh/iDM` route, where the relevant interacting CDM perturbation correction was commented out.

## 5. Scalar perturbation equation

The paper gives

`delta_phi'' + 2 Hconf delta_phi' + (k^2 + a^2 V_phiphi) delta_phi + (h'/2) phi'`

`= kappa rho_c a^2 [ beta delta_c + beta_phi delta_phi ]`.

The pinned source evolves

`delta_phi'' = -2 aH delta_phi' - (h'/2) phi' - (k^2+a^2 V_phiphi) delta_phi`

`+ sqrt(6) beta a^2 rho_c delta_c`

`- sqrt(6) beta_z a^2 rho_c delta_phi H/phi'`.

Again, `beta_phi = -H beta_z/phi'` gives the published form exactly along a nonsingular background trajectory.

## 6. Einstein-source closure

The paper states that the perturbed Einstein equations retain the standard structure but receive the scalar density/pressure/velocity contributions. It gives

`delta rho_phi = phi' delta_phi'/a^2 + V_phi delta_phi`,

`delta p_phi = phi' delta_phi'/a^2 - V_phi delta_phi`.

The pinned source inserts these same scalar stress-energy perturbations into total `delta_rho`, `delta_p` and total momentum, and propagates them into CLASS metric/source construction. The author provider-control run `34487561326` executed this route and generated fresh perturbation, P(k), CMB Cl and transfer outputs.

Thus this is a source-complete linear interacting scalar+CDM implementation in the **synchronous gauge used by the paper**.

## 7. Initial conditions

The paper states that for the constant potential the scalar can start with `phi_ini=0`, `phi'_ini=0` in the radiation era, and the source initializes scalar perturbations `delta_phi=delta_phi'=0`. CDM velocity is initialized to zero in synchronous gauge.

However, the committed example uses tiny nonzero background scalar seeds (`1e-8`, `1e-7`). The source's exact perturbation formula contains the algebraically equivalent but numerically dangerous expression

`beta_z ... / phi'`,

and scalar velocity-source construction divides by `rho_phi+p_phi`.

The prospectively frozen K1 test confirmed that the beta=0 **tiny-seed** full route executes, while the exact-zero full route reaches perturbation integration and fails with a singular-matrix diagnostic. This is an exact-reference numerical implementation issue, not a mismatch of the published nonzero-coupling equations.

## 8. K3 decision

Evidence supports:

- covariant total dark-sector conservation: `PASS_SOURCE`;
- mechanism/frame identity: `PASS_SOURCE`;
- background equation mapping: `PASS_SOURCE`;
- CDM perturbation equation mapping: `PASS_SOURCE`;
- scalar perturbation equation mapping: `PASS_SOURCE` for nonsingular trajectories;
- Einstein-source inclusion: `PASS_SOURCE`;
- executed nonzero-coupling perturbation route: `PASS_PROVIDER_CONTROL`;
- gauge scope: `SYNCHRONOUS_ONLY_VALIDATED`;
- exact beta=0 / exact-zero-field numerical reference: `BLOCKED_IMPLEMENTATION_REFERENCE`.

Therefore strict K3 is **not promoted to an unqualified PASS**. The correct classification is

`K3_SOURCE_EQUATION_MATCH_PASS_WITH_SYNCHRONOUS_SCOPE_NUMERICAL_REFERENCE_BLOCKED`.

This is materially stronger than the two previous M14 providers for source completeness, but K1/K3 reference robustness remains a blocker to K4/K5 under the strict funnel.

## 9. Next allowed route

1. finalize the background-only exact-zero K1 invariant recovery without changing its thresholds;
2. retain the exact-full singularity as immutable evidence; do not regularize `0/0` post hoc in the author source;
3. seek an author-supported/reference-safe perturbation prescription or an independent equivalent provider whose beta->0 exact reference is numerically regular;
4. a separately preregistered independent verification implementation may algebraically simplify the beta=0 terms before numerical evaluation, but it must never be relabelled as the untouched author provider;
5. no K4/K5 production response grid from this provider until the strict K1/reference blocker is resolved or formally scoped by the benchmark protocol.