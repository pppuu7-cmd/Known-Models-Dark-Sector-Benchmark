# M14 LisaGoh/CDE source-complete provider candidate audit

Updated: 2026-09-10
Target: F14/M14 coupled quintessence / conformal scalar-DM coupling
Status: `HIGH_PRIORITY_SOURCE_COMPLETE_PROVIDER_CANDIDATE`
Execution promotion: **provider control preregistration required**
Physical falsification: **NO**

## Immutable candidate

Public repository: `LisaGoh/CDE`

Pinned main commit:

`b85a675af7544a5183e402964550811aa805b698`

The repository README states that it contains the modified CLASS code used for the tomographic coupled-dark-energy analysis of Goh, Gómez-Valent, Pettorino & Kilbinger (arXiv:2211.13588), extending code used for constant-coupling analyses in arXiv:2004.00610 and arXiv:2207.14487. The included main implementation uses three coupling bins with transitions around z=100 and z=1000.

This is independent of both prior M14 routes used in KMDSB (`kabeleh/iDM` and `liaocrane/IDECAMB`).

## Family identity

The provider evolves a canonical scalar field plus cold dark matter with direct field-mediated energy-momentum exchange. The main input uses a constant scalar potential controlled by `kappa` and three redshift-dependent coupling amplitudes `beta_1,beta_2,beta_3`.

The background source explicitly evolves CDM as

`rho_c' = -3 a H rho_c - sqrt(6) beta rho_c phi'`

and the scalar equation contains the compensating source

`phi'' = ... + sqrt(6) beta rho_c a^2`.

Therefore the source implements an interacting scalar-DM system with energy transfer between the two sectors. This is a valid response-distinct representative of the M14 coupled-quintessence/conformal-scalar-DM family even though its potential/parameterization differs from the previous IDECAMB inverse-power-law branch.

## Perturbation completeness advantage

Unlike the first `kabeleh/iDM` M14 route, whose interacting CDM perturbation correction was found commented out, `LisaGoh/CDE` actively evolves the coupled CDM and scalar perturbations.

In synchronous gauge the pinned source contains active equations of the form

`delta_c' = -(theta_c + h'/2) - sqrt(6) beta delta_phi' + sqrt(6) H beta' delta_phi`,

`theta_c' = (-aH + sqrt(6) beta phi') theta_c - k^2 sqrt(6) beta delta_phi`,

and an active scalar perturbation equation including both the `beta rho_c delta_c` source and a `beta' rho_c delta_phi` term.

The scalar stress-energy perturbations are also explicitly inserted into the total Einstein-source variables. Hence this provider is a serious K3 candidate rather than merely a background comparator.

## Coupling function

For the main three-bin implementation,

`beta(a)`

is a smooth tanh-interpolated function of redshift defined by `beta_1,beta_2,beta_3`. Setting all three amplitudes to zero algebraically gives

`beta(a)=0`, `beta'(a)=0`

for the full history. This supplies a clean total interaction-off transformation without mixing interaction axes.

The author input explicitly states that for its constant potential one may set

`phi_ini_scf=0`, `phi_prime_ini_scf=0`.

The committed example instead uses tiny nonzero values (`1e-8`, `1e-7`), apparently as a numerical seed. Any K1 reference test must preregister whether it retains the committed seed or uses the documented exact-zero author-supported state; it must not switch after seeing results.

## Current gate decision

- K0 repository provenance: `PASS_CANDIDATE`, exact public commit pinned;
- family identity: `PASS_CANDIDATE`;
- source-complete background exchange: `PASS_SOURCE_AUDIT`;
- source-complete linear perturbation exchange: `PASS_SOURCE_AUDIT_WITH_GAUGE_SCOPE` (synchronous implementation explicitly active);
- numerical execution of exact pin: `NOT_YET_TESTED`;
- K1 numerical reference regression: `NOT_YET_TESTED`;
- K2-K9: not authorized until provider control and K1 pass.

This candidate is currently stronger for M14 K3 than the two earlier routes because it is public, paper-linked, and contains active coupled CDM + scalar perturbation equations.

## Immediate next allowed steps

1. prospectively preregister and execute the unmodified committed `class_CDE/CDE.ini` provider control at the exact pin;
2. only if provider control passes, preregister the all-`beta_i=0` K1 interaction-off regression with a frozen scalar initial-state prescription;
3. if K1 passes, audit the three-dimensional physical coupling geometry and define a local response coordinate before K4/K5;
4. do not transfer K4 failures from the IDECAMB potential/coupling branch to this independent provider.

No scientific pass beyond source-level K0/K3 candidacy and no family falsification is authorized by this audit alone.