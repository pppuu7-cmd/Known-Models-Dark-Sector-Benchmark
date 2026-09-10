# Future Dark-Sector Model Construction Methodology v0.2

Updated: 2026-09-09  
Status: LIVING / evidence-fed from KMDSB Waves 00-03  
Supersedes for active work: `FUTURE_MODEL_CONSTRUCTION_METHODOLOGY_v0.1.md`  
Historical authority rules: `recovery/AUTHORITY_DELTAS.md`

## Purpose

This document converts controlled benchmark failures, degeneracies, successful controls and holdouts into a construction pipeline for a future original dark-sector model.

It is not itself a physical theory. It must not turn every current design prior into an axiom.

The governing rule is:

> build only from requirements that survive repeated model-family and observation-space stress; treat a beautiful microphysical construction as insufficient until it produces a response that survives the strongest implemented comparator manifold and a real common observation operator.

Machine-readable current requirements: `matrices/design_prior_ledger.csv`.

## 1. Canonical DSIR embedding

The future candidate must embed unambiguously into the DSIR bookkeeping

`X_{mu nu} = M0^2 G_{mu nu} - T^{known}_{mu nu}`

under frozen conventions for:
- known-sector subtraction;
- background and perturbation variables;
- gauge/frame;
- units;
- solver/version authority;
- observable masks;
- reference cosmology.

Interpretive novelty is not a gate. Observable, reproducible residual structure is.

---

# Construction pipeline F0-F10

## F0 — authority, provenance and succession

Before deriving or fitting the candidate:

1. pin the DSIR authority commit;
2. pin solver/code versions;
3. bind parameter names, units, gauge/frame and known-sector content;
4. record which object is authoritative when multiple exact or near-exact routes exist;
5. record authority succession explicitly rather than inferring it from numerical equality.

A newer successful recomputation does not silently replace an older admitted scientific authority.

If authority is ambiguous, fail closed and resolve provenance before scientific scoring.

Evidence: AD-001, AD-002 and the DSIR authority-succession hardening at `864952e...`.

## F1 — recoverable reference / decoupling limit

The candidate must possess a physically admissible path to the chosen reference theory.

Required:
- analytic existence of the limit where possible;
- numerical regression of the limit;
- explicit solver floor;
- no hidden parameter retuning that changes the physical branch;
- exact/matched bookkeeping at the reference intersection.

A clean reference limit is necessary but does not imply novelty or identifiability.

M07 demonstrates this sharply: its LambdaCDM intersection is accurate at roughly `1e-10` in lnH/lnP, yet its finite response is observationally weak and strongly absorbable by flexible smooth DE.

## F2 — physical parameter geometry and exact quotient before differentiation

Do not assume the local physical parameter space is an unconstrained Euclidean box.

First determine:
- physical boundaries;
- stability/positivity constraints;
- tangent cones and one-sided rays;
- exact parameter/field redundancies.

Only after quotienting exact redundancies may one define the local coordinate and Jacobian.

For an admissible local ray `v`, use

`J_v = d r(p0 + epsilon v)/d epsilon | epsilon -> 0+`

when the reverse direction is forbidden.

M07 example:
- fixed-chart lambda-sign parity failed;
- exact `(lambda,phi)->(-lambda,-phi)` field reflection passed;
- after quotient, the correct local coordinate is `q=lambda^2`, not naive `lambda`.

## F3 — conservation, gauge, frame and closure bookkeeping

Before interpreting response:
- close total conservation;
- distinguish internal exchange from net stress-energy nonconservation;
- bind gauge/frame conventions;
- make cosmological budget closure explicit;
- record which density/normalization is solver-inferred.

An inconsistent closure assignment is an implementation failure, not a physical falsification.

M08 run #1 is the control: simultaneously specifying `Omega_Lambda` and `Omega_fld` was configuration-invalid; the corrected pure-CPL branch fixes `Omega_Lambda=0` and lets `Omega_fld` be inferred.

## F4 — numerical conditioning and derived-residual robustness

Solver defaults do not define the physical manifold.

For every sensitive nuisance/closure coordinate:
- estimate the natural scale analytically where possible;
- initialize near that scale;
- audit tolerance dependence;
- distinguish raw observable stability from small derived-residual stability.

If

`r = f(model) - f(reference)`

or an equivalent ratio/log residual is much smaller than either raw solution, it receives its own convergence and gauge/frame audit.

M07 examples:
- raw shooting tolerance distorted the response by tens of percent;
- tightening the physically resolved shooting coordinate restored the intended branch;
- raw P/d_m/phi/psi passed cross-gauge regression while small derived residuals retained percent-level gauge/representation floors.

A channel that fails this test is not eligible to support mechanism novelty.

## F5 — multi-channel response architecture and measured response rank

The candidate should predict multiple physically meaningful response axes where available:
- expansion/background;
- growth/matter;
- Weyl/lensing;
- slip/metric;
- characteristic scale dependence;
- time evolution/localization;
- nonlinear/high-k structure;
- tensor/GW propagation;
- couplings or other sector-specific channels.

Undefined channels remain masked, never zero-imputed.

Parameter count is not response rank.

For local response matrix `J`, inspect its singular spectrum rather than declaring rank from the number of parameters.

M08 example:
- two physical CPL coordinates;
- local P+H direction angle only `9.179 deg`;
- `sigma2/sigma1=0.05020`.

The second direction is weak but scientifically decisive because it absorbs the M07 residual left by constant-w.

Therefore weak singular directions cannot be discarded merely because they carry low norm; their role in comparator degeneracy must be tested.

## F6 — nearest-family manifold attack

**This is the major v0.2 change.**

A candidate is not attacked only by one nearby model or ray. It is attacked by the strongest implemented local response span/manifold of the nearest plausible family.

Let candidate local target be `t` and comparator-family Jacobian be

`J_C = [j1 ... jm]`.

Use one shared comparator parameter vector `c` across every claimed response block:

`c* = argmin_c || t - J_C c ||`

in the chosen theory-space metric, or its observation-space analogue after F7.

Do not fit P, H, slip, lensing etc. independently and then call the family equivalent. The same physical comparator parameters must explain all included blocks.

Report:
- fitted parameter vector;
- combined residual fraction;
- residual fraction per block;
- singular spectrum/conditioning of `J_C`;
- physical admissibility of the fitted local direction.

### M08 calibration result

For M07 `dr/dq`:

Same-solver constant-w-like one-direction residual:
- combined P+H `15.82%`;
- P `12.06%`;
- H `29.15%`.

Two-dimensional CPL span with one shared `(epsilon0,wa)` fit:
- combined P+H `1.107%`;
- P `0.864%`;
- H `1.993%`.

Best coefficients per unit M07 q:

`epsilon0/q = 0.1406535`

`wa/q = -0.2006791`.

Therefore the earlier constant-w cross-channel separator is **not** mechanism-level novelty.

Construction consequence: separation from one representative ray is insufficient. The future candidate needs a response outside the flexible nearest-family span.

## F7 — exact common observation operator, covariance and whitening

**Second major v0.2 change from DSIR AD-002 / Article-2 G5.**

A real covariance by itself does not authorize an observational claim.

For any cross-family observation-space comparison, bind prospectively:

1. immutable model/family IDs and provenance;
2. one exact common-valid theory response block;
3. one observation/operator bridge `R` mapping every compared response into the **same exact observable coordinate vector**;
4. one covariance `C` defined on that exact vector/order/units;
5. masks and coordinate order;
6. positive-definiteness or a prospectively frozen regularization rule.

A covariance defined on different observables must be rejected rather than interpolated, padded or relabelled.

Whitening:

`C = L L^T`

`r_w = L^{-1} R r`.

Record factorization/roundtrip diagnostics and the exact whitened feature order.

For candidate Jacobian `J`:

`J_w = L^{-1} R J`

and nuisance-free Fisher information is schematically

`F = J^T R^T C^{-1} R J`.

When nuisance/comparator directions exist, profile or marginalize them before claiming identifiability.

### Cross-family robustness requirements

For a classifying multi-family geometry/rank stress, adopt the current DSIR G5 discipline:
- catalog-multiplicity sensitivity;
- equal-family weighting;
- one prospectively defined alternative within-family weighting;
- family-stratified bootstrap;
- leave-one-family-out diagnostics;
- full singular spectra/noise diagnostics;
- no post-hoc integer rank cutoff.

The ACT x unWISE 26-coordinate chain is a promising real bridge, but current DSIR authority explicitly says the multi-family provider -> exact 26-coordinate matrix is not yet bound. Do not insert theory-atlas vectors directly into that covariance.

## F8 — quotient-surviving novelty

After F1-F7, ask what remains that cannot be removed by:
- exact reparameterization/field quotient;
- solver/calibration freedom;
- numerical subtraction/gauge floor;
- nearest-family manifold profiling;
- modified-gravity or other cross-family alternatives;
- observational projection/covariance;
- nuisance profiling;
- bookkeeping identities.

Only the surviving component is eligible to be called a candidate novel response.

A large theory-space angle is insufficient.
A large whitened angle is also insufficient if the absolute profiled signal is tiny.

M07 calibration:
- whitened C1-profiled direction existed;
- largest tested q carried only about `0.022 sigma` in the scoped ShapeFit control.

Therefore always report both geometry and absolute profiled significance.

## F9 — prospective holdout prediction

Before opening the holdout, freeze at least one:
- relation;
- characteristic scale;
- characteristic epoch;
- sign/orientation;
- cross-channel mapping;
- response ratio/profile;
- regime transition.

Strength ladder:
1. within-family interpolation;
2. withheld regime/block;
3. withheld model family/mechanism;
4. genuinely future/new observation.

M07 has level-1 support only. This proves local predictive regularity, not mechanism uniqueness.

A candidate should not be promoted toward a general law until it survives higher holdout levels.

## F10 — candidate promotion package

Only after F0-F9 should an original model move to its own dedicated theory repository.

Minimum package:

1. explicit action/equations/degrees of freedom;
2. reference/decoupling limit;
3. physical/stability domain;
4. authority and provenance chain;
5. conservation/gauge/frame/closure bookkeeping;
6. natural local quotient coordinates;
7. numerically conditioned multi-channel response;
8. measured local response rank;
9. nearest-family manifold profile, not only pairwise ray comparisons;
10. modified-gravity and other relevant cross-family comparators;
11. exact common observation-operator/covariance projection;
12. absolute profiled identifiability estimate;
13. at least one prospective holdout stronger than retrospective interpolation where feasible;
14. explicit mapping of satisfied, violated and retired KMDSB design priors.

---

# Design-prior promotion policy

Current ledger states are evidence, not doctrine.

Conceptual levels:
- `ACTIVE` — generated by at least one controlled benchmark result;
- `REINFORCED` — independently supported by multiple families/waves;
- `CORE` — survives a dedicated adversarial stress and is required for candidate construction;
- `RETIRED` — contradicted, redundant or shown scope-specific.

Wave 03 now gives independent reinforcement to several older rules:
- DP-0303 parameter count != response rank;
- DP-0504 new microphysics != new observable direction;
- DP-0701/0704 comparator coverage and sufficient common blocks;
- DP-0103 observation-space rather than raw theory distance.

New v0.2 rules:
- DP-0815 full nearest-family manifold profiling;
- DP-0816 exact common observation operator/covariance bridge;
- DP-0817 explicit closure/normalization provenance.

Do not promote these to CORE solely because they are written here; promotion requires the ledger/evidence process.

# Current provisional architecture for the future original model

The benchmark increasingly favors a model with:

- a clean recoverable reference limit;
- physically non-pathological local geometry;
- no hidden solver-tuned physical parameters;
- robust residuals above numerical/gauge subtraction floors;
- multiple response channels with measured independent rank;
- at least one signature that cannot be absorbed by flexible smooth-DE `w(a)` histories;
- separation from modified-gravity and alternative dark-sector family manifolds;
- characteristic scale/time structure when physically motivated;
- an exact path through realistic observation operators;
- covariance-weighted signal that is not merely geometrically orthogonal but absolutely detectable;
- prospective withheld predictions not used to construct the model.

The strongest new warning from M08 is:

> do not design the future theory around a signature that is only distinct from LambdaCDM or constant-w. A modest two-parameter smooth history can erase such apparent novelty.

# Forbidden anti-patterns

- zero-imputing undefined channels;
- differentiating through forbidden parameter space;
- rank = parameter count;
- choosing solver defaults as physical geometry;
- interpreting configuration/closure failure as theory failure;
- declaring pairwise angle to be family-level uniqueness;
- fitting comparator parameters independently in each block;
- using a covariance without proving exact operator-coordinate compatibility;
- mixing family-specific observation coordinates in one whitening claim;
- post-hoc covariance regularization or singular-value cutoff;
- treating predictive interpolation as observational detection;
- treating whitened orthogonality with near-zero amplitude as novelty;
- silently rebasing old evidence to newest DSIR main;
- changing a preregistered threshold after seeing the output.

# Update rule

After every scientifically meaningful frontier change:

1. preserve raw run/artifact provenance;
2. update model audit/result;
3. update benchmark/wave matrices;
4. update design-prior ledger;
5. update this methodology only when a durable rule changes;
6. update `recovery/STATE.md`, `RESTORE_FROM_NEW_CHAT.md` and authority deltas;
7. append research chronology;
8. keep failed/blocked evidence rather than rewriting it away.

KMDSB remains the evidence-producing benchmark. The future original model should be moved to a separate repository only when enough requirements have matured from ACTIVE evidence into a stable architecture.


---

## Provider execution versus representative validity (2026-09-10)

A successful build and author example is only an infrastructure/provenance control. Before K1/K5 or family-level promotion, independently audit that the executed source branch and stress-energy bookkeeping actually instantiate the intended census family. In particular, verify which sector supplies matter-like density, acceleration/vacuum energy, interaction terms and closure. A similar Lagrangian label or scalar-field implementation is insufficient if a separate Lambda/CDM component supplies the target behaviour.

Conversely, a README command or benchmark timing is not a reproducible provider control when the referenced author input is absent from the immutable pinned source. Never reconstruct a missing author configuration post hoc from defaults, prose or nearby files and call it provider validation. Recover an immutable archival configuration or choose another provider.

Durable rule: **executable provider != valid representative; documented-but-missing input != reproducible provider.**


### Reference-path regularity rule (M18-derived)
A mathematically exact symmetry/decoupling reference is not sufficient if the numerical implementation is singular precisely on that locus. Before using a reference for family promotion, require both a physically justified map and a numerically regular executable path. If a third-party shooting algorithm is singular at an exact symmetry point, classify the provider/reference as blocked and seek an independent implementation or author-supported prescription; do not perturb the reference, retune initial conditions, or patch the solver after seeing the failure merely to manufacture a passing control.

### Multi-mechanism decoupling rule (M14-derived)
When a provider contains more than one independent interaction law, a reference/decoupling gate must zero every interaction branch source-by-source. An author/config label such as "uncoupled" is not sufficient if it refers only to one subcoupling. Each interaction law should subsequently receive its own physical coordinate/quotient audit rather than being combined into an undifferentiated coupling parameter.

