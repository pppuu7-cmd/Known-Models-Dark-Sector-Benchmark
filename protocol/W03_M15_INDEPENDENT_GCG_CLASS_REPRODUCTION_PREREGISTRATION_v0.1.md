# W03 M15 independent GCG/decaying-vacuum CLASS reproduction preregistration v0.1

Date: 2026-09-10
Family: F15 / M15 generalized Chaplygin dark sector
Subcase: decomposed GCG with vacuum-like DE, `w_Lambda=-1`, interaction coordinate `alpha`
Purpose: create a transparent KMDSB verification implementation because the published modified CLASS/CAMB source trees have not been publicly bound to a reproducible commit.

## Provenance boundary

This implementation is **not** the original author code and must never be labelled as such.

Primary equation source:

- R. F. vom Marttens, L. Casarini, W. Zimdahl, W. S. Hipolito-Ricaldi, D. F. Mota, *Does a generalized Chaplygin gas correctly describe the cosmological dark sector?*, Physics of the Dark Universe 15 (2017) 114-124, arXiv:1702.00651, DOI 10.1016/j.dark.2017.02.001.

Independent related perturbation authority:

- Y. Wang et al., *Cosmological constraints on a decomposed Chaplygin gas*, Phys. Rev. D 87, 083503 (2013), arXiv:1301.5315.

Public author/coauthor solver repositories have been audited, but no accessible branch/commit inspected so far binds the published M15 perturbation implementation. See `models/generalized_chaplygin/m15_provider_search_2026-09-10.md`.

## Frozen physical subcase

We reproduce the 2017 paper's time-varying-vacuum specialization `w_Lambda=-1`.

The dark-sector background exchange is

`dot(rho_Lambda) = Q`,

`dot(rho_c) + 3 H rho_c = -Q`,

with the paper's interaction

`Q = 3 H [ alpha (1+w) + 1+w_Lambda ] rho_Lambda`.

For `w_Lambda=-1`, the sign of `alpha` controls the transfer direction. The reference is exact:

`alpha=0  =>  Q=0  =>  LambdaCDM`.

The DE density relation is frozen to the paper's covariant ansatz corresponding to Eq. (8),

`rho_Lambda / rho_Lambda0 = (H/H0)^(-2 alpha)`

for the vacuum subcase, with the four-component radiation+baryon background treated as in the paper rather than silently reverting to a two-component GCG solution.

## Frozen perturbation closure

Implementation gauge: **Newtonian gauge**, matching the explicit perturbation equations in Sec. VI of arXiv:1702.00651.

Metric convention is bound to the paper's Eq. (32). Standard baryon/photon/neutrino sectors are delegated to upstream CLASS; only the dark-sector background and perturbation closure may be modified.

For `w_Lambda=-1`, the required dark-sector closure is bound to Eqs. (45)-(50):

- vacuum density perturbation obeys the vacuum energy balance of Eq. (45);
- momentum-transfer potential obeys the reduced relation Eq. (46);
- CDM density and velocity obey Eqs. (47)-(48);
- the perturbation of the interaction is not a free sound-speed ansatz: it is determined by perturbing the covariant extension of the background relation;
- specifically, the vacuum density contrast is constrained by Eq. (49), `delta_Lambda = -(2 alpha / (3 H)) delta_Theta`, with `delta_Theta` evaluated from the Newtonian-gauge expansion scalar as in Eq. (50);
- `delta Q` is then obtained from the vacuum energy-balance equation, following the paper's stated construction.

No ePPF substitution is allowed in this verification branch. A PPF/ePPF realization may remain a separate comparator, but cannot satisfy this perturbation-identity gate.

## Frozen reference and validation hierarchy

### V0 — upstream reference preservation

Build an unmodified pinned upstream CLASS reference and the KMDSB verification branch with identical compiler/toolchain settings.

At `alpha=0` the verification branch must reduce to the same physical LambdaCDM system without manually zeroing outputs or substituting reference files.

Required comparison outputs:

- background `H(z)` and component densities;
- CMB `TT`, `TE`, `EE` spectra;
- matter transfer / linear `P(k,z=0)`;
- standard derived background quantities needed to establish matching cosmology.

### V1 — alpha=0 exact-reference gate

Pass only if all outputs are finite and matched-grid comparisons satisfy:

- background maximum symmetric relative difference <= `1e-8` away from exact-zero entries;
- CMB RMS symmetric relative difference <= `1e-5` over matched finite nonzero multipoles, reported separately for TT/TE/EE;
- linear matter-power RMS symmetric relative difference <= `1e-5` on the matched finite positive k-grid;
- no new CLASS warning/error appears only in the verification branch.

These are implementation-identity thresholds, not observational tolerances.

Failure of V1 blocks all M15 K3-K7 promotion and is classified as an implementation failure, not physical falsification.

### V2 — published finite-alpha qualitative recovery

Freeze the paper's displayed finite points:

`alpha = {-0.50, -0.25, -0.05, +0.05, +0.25}`.

At this stage we require:

- successful finite background and perturbation evolution for every point;
- correct sign of the background energy-transfer direction under the paper's convention;
- continuous approach to the alpha=0 reference;
- CMB and linear-matter responses whose ordering/sign trends are compatible with the corresponding published figures and discussion.

Because the paper does not publish machine-readable spectra, V2 is a **qualitative/structural replication gate**, not a pointwise numerical reproduction claim.

### V3 — local DSIR reference geometry

Only after V0-V2 pass may the verification implementation be used to construct a local finite-difference response around alpha=0.

The first authorized local stencil is symmetric and nested:

`alpha = +/-{1e-2, 5e-3, 2.5e-3}`.

The K4 derivative-stability gate must compare nested central derivatives channel-by-channel and demonstrate a stable numerical plateau before any tangent is admitted to K5.

Step-size agreement thresholds are to be preregistered in the dedicated K4 protocol after V1-V2 expose the actual numerical floor; they are not chosen post hoc from a favorable result.

## Gauge/closure negative controls

The verification suite must include at least these deliberate negative controls:

1. suppress `delta Q` while retaining nonzero background Q;
2. replace the Eq. (49)-(50) closure by a smooth-fluid/ePPF perturbation prescription;
3. hold the background fixed but alter only the dark-sector perturbation closure.

These controls are not candidate models. Their role is to prove that the exact perturbation prescription materially binds the M15 response and that a generic background-matched fluid is not being mistaken for the published decomposed-GCG perturbation system.

## Allowed classifications

- `M15_INDEPENDENT_REPRO_REFERENCE_PASS`
- `M15_INDEPENDENT_REPRO_REFERENCE_FAIL`
- `M15_INDEPENDENT_REPRO_FINITE_GRID_PASS_WITH_SCOPE`
- `M15_INDEPENDENT_REPRO_BLOCKED_BUILD`
- `M15_INDEPENDENT_REPRO_BLOCKED_EQUATION_MAPPING`
- `M15_INDEPENDENT_REPRO_BLOCKED_NUMERICS`

No failed verification implementation is a physical falsification of the GCG family.

## Promotion boundary

Even a successful independent reproduction does not upgrade provenance to original-provider evidence. It may establish a transparent **KMDSB-verified realization** of the published equations and thereby unlock K3/K4/K5 testing for the explicitly reproduced subcase.

A family-level terminal classification still requires common observation-space/covariance treatment, nearest-family attacks, numerical/gauge floors and the later cross-family/holdout waves.

## Next authorized implementation step

Pin a compatible upstream CLASS revision, document the exact source locations where the background and Newtonian-gauge dark-sector equations enter, and produce the minimal patch plus V0/V1 machine harness. Do not run finite-alpha science cases until the alpha=0 reference gate passes.
