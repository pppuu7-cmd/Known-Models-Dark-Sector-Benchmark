# M15 V2 equation-to-CLASS map

Date: 2026-09-10
Status: `BACKGROUND_AND_VELOCITY_MAP_BOUND_PERTURBATION_SOUND_SPEED_UNDERDETERMINED`
Scientific promotion: **NO**

## Purpose and provenance boundary

This record translates the published finite-alpha equations of R. F. vom Marttens et al., *Does a generalized Chaplygin gas correctly describe the cosmological dark sector?*, Physics of the Dark Universe 15 (2017) 114-124, arXiv:1702.00651, into the frozen CLASS conventions of the independent KMDSB verification implementation.

It is not an assertion that the unpublished modified CLASS implementation used by the authors has been recovered. The V0/V1 exact-reference controls remain authoritative.

Frozen upstream CLASS:

`lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

Frozen gauge: Newtonian.

## A. Background map — bound

The four-component paper defines

`rho = rho_c + rho_Lambda + rho_b + rho_r`,

with separately conserved baryons and radiation, and retains the two-component relation

`rho_Lambda/rho_Lambda0 = (H/H0)^(-2 alpha)`

as an explicit ansatz after radiation and baryons are added.

The exact four-component Hubble equation is Eq. (16):

`2 a E dE/da = -3 E^2 - 3 w_Lambda Omega_Lambda0 E^(-2 alpha) - Omega_r0 a^(-4)`.

For the frozen vacuum subcase `w_Lambda=-1`,

`2 a E dE/da = -3 E^2 + 3 Omega_Lambda0 E^(-2 alpha) - Omega_r0 a^(-4)`.

Present boundary condition: `E(a=1)=1`.

The dark-sector densities are then reconstructed without a two-component shortcut:

`rho_Lambda/rho_crit0 = Omega_Lambda0 E^(-2 alpha)`,

`rho_c/rho_crit0 = E^2 - Omega_b0 a^(-3) - Omega_r0 a^(-4) - Omega_Lambda0 E^(-2 alpha)`.

This is the preferred first finite-alpha implementation route because it follows the paper's four-component ansatz and exact Hubble ODE directly.

The approximate Eq. (26) is retained only as a validation comparator, not as the authoritative high-redshift background:

`E_approx^2 = [1-Omega_m0 + Omega_m0 a^(-3(1+alpha))]^(1/(1+alpha)) + Omega_r0 a^(-4)`

for `w_Lambda=-1`.

### Interaction sign

The paper defines

`dot(rho_Lambda)+3H(1+w_Lambda)rho_Lambda = Q`,

`dot(rho_c)+3H rho_c = -Q`.

Therefore `Q>0` means CDM loses energy and vacuum/DE gains energy. The text immediately following Eq. (11) states this explicitly and says that for `w_Lambda=-1` the transfer direction is fixed by the sign of `alpha`.

A later narrative sentence near the CMB figures reverses this verbal direction. KMDSB treats that sentence as an internal narrative inconsistency and binds the implementation to Eqs. (9)-(12), not to the later prose.

No sign convention may be altered to improve agreement with a figure.

## B. Conformal-time and velocity conventions — bound

The paper uses conformal time in its perturbation section, with `mathcal H=a'/a`, and defines each peculiar-velocity potential by

`partial_i vhat_A = a u_A^i`.

The frozen CLASS Newtonian CDM equations at the upstream pin are

`delta_cdm' = -(theta_cdm - 3 phi')`,

`theta_cdm' = -mathcal H theta_cdm + k^2 psi`.

The paper's noninteracting limit of Eq. (47) is

`delta_c' - k^2 vhat_c - 3 phi' = 0`.

Hence the Fourier convention map is fixed exactly as

`theta_cdm_CLASS = -k^2 vhat_c_paper`.

The same convention is used for every component velocity potential.

CLASS constructs the total momentum variable explicitly as

`rho_plus_p_theta = Sum_A [(rho_A+p_A) theta_A]`

and stores

`rho_plus_p_tot = Sum_A (rho_A+p_A)`.

Thus

`theta_tot_CLASS = rho_plus_p_theta/rho_plus_p_tot`,

and the paper's total peculiar-velocity potential is mapped as

`vhat_paper = -theta_tot_CLASS/k^2`.

For the vacuum subcase `rho_Lambda+p_Lambda=0`, the vacuum contributes no independent inertial velocity to this weighted total, consistent with the paper's statement that the DE peculiar velocity is not a dynamical degree of freedom at `w_Lambda=-1`.

## C. Metric convention — bound

Both systems use Newtonian/longitudinal scalar potentials with

`ds^2 = a^2[-(1+2 psi)d tau^2 + (1-2 phi) dx^i dx^i]`.

At the frozen CLASS pin:

`metric_continuity = -3 phi'`,

`metric_euler = k^2 psi`.

Therefore no phi/psi exchange is authorized when translating Eqs. (45)-(50).

## D. Expansion-scalar closure — source expression frozen, implementation deferred

The paper covariantizes the four-component ansatz as

`rho_Lambda = rho_Lambda0 (Theta/Theta0)^(-2 alpha)`

and derives

`delta_Lambda = -(2 alpha/(3H)) Thetahat`  [Eq. (49)],

with its published Newtonian-gauge expression

`Thetahat = (1/a) (psi' + phi' - k^2 vhat)`  [Eq. (50)].

Using the velocity map above, the last term becomes `+theta_tot_CLASS`, so the literal published expression maps to

`Thetahat = (1/a) (psi' + phi' + theta_tot_CLASS)`.

KMDSB deliberately preserves the published Eq. (50) literally. It will not silently replace it by a textbook expansion-scalar formula or alter signs because the expression looks unusual. Any correction would require an explicit erratum, author source, or independent derivation recorded as a separate verification branch.

## E. CDM perturbation equations — algebraic CLASS map bound

Paper Eq. (47):

`delta_c' - k^2 vhat_c - 3 phi' = -(aQ/rho_c)(psi-delta_c) + a Qhat/rho_c`.

Using `theta_c=-k^2 vhat_c`, the CLASS correction is

`delta_c' = -theta_c + 3 phi' -(aQ/rho_c)(psi-delta_c) + a Qhat/rho_c`.

Paper Eq. (48):

`vhat_c' + mathcal H vhat_c + psi = -(aQ/rho_c)(vhat-vhat_c) - a fhat/rho_c`.

Multiplying by `-k^2` gives the CLASS velocity equation

`theta_c' = -mathcal H theta_c + k^2 psi
             - (aQ/rho_c)(theta_c-theta_tot)
             + (a k^2/rho_c) fhat`.

This sign map is frozen before finite-alpha coding.

## F. Vacuum perturbation closure — one unresolved physical input

Paper Eq. (45):

`delta_Lambda' + 3 mathcal H (c_s,Lambda^2+1) delta_Lambda
 = (aQ/rho_Lambda)(psi-delta_Lambda) + a Qhat/rho_Lambda`.

Paper Eq. (46):

`fhat = c_s,Lambda^2 rho_Lambda delta_Lambda/a - Q vhat`.

The paper then states that `Qhat` is obtained by inserting Eq. (49) into Eq. (45) and solving for `Qhat`.

The comoving sound speed `c_s,Lambda^2` is therefore not cosmetic: it enters both `Qhat` and `fhat`, and after substitution it contributes to the CDM density/velocity equations. It does not algebraically cancel in general.

### Provenance finding

The accessible full text of arXiv:1702.00651 defines `c_s,A^2` as a comoving sound speed and carries it explicitly through Eqs. (42)-(48), but the numerical section inspected so far does not state the numerical value used for `c_s,Lambda^2` in the modified CLASS calculation.

The closely related same-author paper arXiv:1610.01665 likewise emphasizes that its perturbation initial conditions are valid for more general sound speeds; this does not supply a unique numerical value for the 1702.00651 implementation.

Therefore adopting upstream CLASS `cs2_fld=1` by default would be an undocumented physical assumption and is forbidden for an **exact author-numerics reproduction** claim.

## G. V2 decision

Bound before finite-alpha code:

- four-component background ODE: `BOUND`;
- present-day/reference boundary: `BOUND`;
- alpha=0 LambdaCDM identity: `PASS` from V1;
- interaction sign: `BOUND_TO_EQUATIONS`;
- paper component velocity to CLASS theta: `BOUND`;
- total velocity potential: `BOUND_TO_CLASS_WEIGHTED_TOTAL_THETA`;
- metric phi/psi convention: `BOUND`;
- Eq. (49)-(50) expansion closure: `BOUND_LITERAL_PUBLISHED_FORM`;
- CDM source-term sign map: `BOUND`;
- vacuum comoving sound speed: `UNDERDETERMINED_BY_ACCESSIBLE_AUTHOR_NUMERICS`.

Classification:

`M15_V2_PARTIAL_MAP_BLOCKED_EXACT_AUTHOR_SOUND_SPEED_PROVENANCE`

This does **not** block all scientific progress. It blocks only an unqualified claim of exact reproduction of the unpublished author perturbation implementation.

## H. Authorized split of the next V2 work

### V2a — exact published background, no sound-speed dependence

Authorized immediately. Implement the exact Eq. (16) four-component Hubble ODE and Eq. (8) density reconstruction independently of the perturbation sound-speed issue. Validate:

1. `alpha=0` against LambdaCDM;
2. nested numerical integration convergence;
3. positivity of `rho_c` and `rho_Lambda` over the frozen domain;
4. interaction sign from `d rho_Lambda/d ln a`;
5. Eq. (26) approximation error versus exact Eq. (16) over the paper's finite alpha points.

### V2b — perturbations

Not yet authorized as an **exact author numerical replication** unless `c_s,Lambda^2` is sourced.

If exhaustive provenance search remains negative, the allowed fallback is a prospectively preregistered **closure-sensitivity study**, not an author-code reproduction. At minimum it should freeze physically explicit subcases such as `c_s,Lambda^2=0` and `1`, run identical background and initial conditions, and ask whether the DSIR response classification is robust to this hidden closure degree of freedom.

That fallback must carry a distinct label and may not be used to claim the authors used either value.

## Next authorized gate

Run V2a first. It is independent of the unresolved sound-speed closure and can establish whether the finite-alpha background branch itself is numerically well-defined and whether the analytic approximation used in the paper is adequate on the exact preregistered alpha grid.