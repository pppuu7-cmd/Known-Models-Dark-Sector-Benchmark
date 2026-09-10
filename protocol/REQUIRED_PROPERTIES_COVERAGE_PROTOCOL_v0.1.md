# KMDSB Required-Properties Coverage Protocol v0.1

Frozen: 2026-09-10
Status: ACTIVE
Purpose: convert the benchmark from a convenience catalogue into a coverage-driven census of known cosmological dark-sector mechanisms.

## 1. Scope and meaning of "all known models"

The literal set of named models in the literature is unbounded because many papers rename, reparameterize or slightly deform the same physical response family. KMDSB therefore defines coverage over **response-distinct model families**, not paper titles.

A new top-level benchmark ID is required when a construction introduces at least one of:
- a new propagating degree of freedom relevant to cosmology;
- a new conservation/exchange law;
- a new background history class not contained in the existing local family manifold;
- a new characteristic scale/time law;
- a new perturbation closure/sound-speed/viscosity structure;
- a new metric/slip/tensor response;
- a new interaction with dark radiation, baryons, neutrinos or gravity;
- a new nonlinear/high-k response class;
- a new observational response direction after quotienting known redundancies.

Variants that differ only by notation, parameter relabeling, potential shape inside an already-covered local response manifold, or particle realization with the same cosmological response are recorded as **subcases** of the corresponding family unless an adversarial test shows that they escape the representative span.

This makes the coverage target finite, auditable and expandable.

## 2. Mandatory properties for every known-model family

Every family is passed through the same K0-K9 checklist. These are the benchmark analogues of the future-model F0-F9 construction requirements.

### K0 — authority/provenance
Pin theory definition, solver/code commit, parameter conventions, reference cosmology, units, gauge/frame and known-sector content.

### K1 — recoverable reference/decoupling limit
Demonstrate a physically admissible path to the reference theory or classify `NOT_APPLICABLE` with explicit reason. Numerical reference-floor regression is required where a solver exists.

### K2 — physical parameter geometry
Determine positivity/stability bounds, tangent cones, one-sided rays, exact field/parameter quotients and forbidden regions before differentiation.

### K3 — conservation/gauge/frame/closure
Verify total conservation and exchange bookkeeping, closure of the cosmological budget, and gauge/frame robustness of every response used for classification.

### K4 — numerical robustness
Freeze solver tolerances, natural shooting/normalization scales, finite-difference convergence, raw-output stability and derived-residual stability. Numerical/implementation failures are not physical failures.

### K5 — multi-channel response and measured rank
Map all physically defined channels among background, growth/matter, lensing/Weyl, slip, scale dependence, temporal localization, nonlinear/high-k, tensor/GW and interaction-specific observables. Undefined channels remain masked. Measure singular spectra; never identify rank with parameter count.

### K6 — strongest nearest-family manifold attack
Profile the strongest implemented local manifold of the nearest plausible known family using one common comparator parameter vector across the claimed blocks. Pairwise angle alone is insufficient.

### K7 — exact common observation-space projection
Where an observational claim is made, every compared family must pass through the same frozen observation operator into the same coordinate order/units/masks with one covariance. Apply whitening and nuisance/comparator profiling. If the bridge does not exist, classify `BLOCKED_OPERATOR_BINDING` or the appropriate blocked status.

### K8 — quotient-surviving novelty / absolute profiled significance
Report what response survives reference subtraction, exact quotient, solver/calibration freedom, gauge/subtraction floors, nearest-family profiling, cross-family alternatives, observation projection and nuisance profiling. Geometry alone is insufficient; report absolute significance where data covariance exists.

### K9 — prospective holdout
Freeze at least one relation, scale, epoch, orientation, response ratio/profile or regime transition before opening the holdout. Record holdout strength: within-family, withheld block/regime, withheld mechanism/family, or genuinely future observation.

## 3. Uniform terminal statuses

Each K-gate uses the existing status taxonomy. In addition, the coverage matrix may use:
- `NOT_TESTED` — queued, no valid run yet;
- `REPRESENTED_BY:<ID>` — no separate top-level run because the model is currently response-equivalent to an already tested family; this must be revisited if an escape channel is found;
- `BLOCKED_OPERATOR_BINDING` — theory response exists but no exact authorized observation bridge exists.

No family is removed from the census because it is difficult to implement. It remains visible with a blocker.

## 4. Coverage tiers

### Tier A — mandatory canonical mechanism classes
These are required before any claim that existing model families are insufficient:
1. Lambda/reference and smooth-DE controls;
2. canonical scalar DE and flexible w(a);
3. noncanonical/phantom/crossing DE;
4. interacting/coupled dark sectors;
5. early-DE/scalar early-energy mechanisms;
6. unified dark fluids;
7. cold/warm/mixed/fuzzy/self-interacting/decaying/annihilating DM;
8. DM-dark-radiation / dark-acoustic mechanisms;
9. scalar-tensor/f(R)/Horndeski-like gravity;
10. braneworld/Galileon/vector-tensor/bimetric-massive-gravity response classes.

### Tier B — distinct established or widely studied escape mechanisms
Includes running vacuum, holographic DE, dynamical DM ensembles, sterile-neutrino-like WDM subfamilies when cosmologically distinct, ETHOS-like dark sectors, nonlocal gravity, beyond-Horndeski/DHOST and other response-distinct classes.

### Tier C — literature-tail / niche constructions
Added continuously. A Tier-C model is promoted to A/B if it produces a response outside all represented manifolds or exposes a new systematic/observable channel.

## 5. Coverage-completion rule

KMDSB may state **"major known cosmological mechanism families covered"** only when:
1. every Tier-A census row has a terminal status for K0-K6;
2. every Tier-A family capable of an observational test has K7 terminal (`PASS/PARTIAL/NONIDENTIFIABLE/BLOCKED_*` rather than `NOT_TESTED`);
3. every claimed survivor of K8 has at least one K9 prospective holdout or an explicit blocker;
4. W06 adversarial mimicry and W07 cross-family rigidity have attacked the surviving directions;
5. W08 true holdout is executed on mechanisms not used to construct the proposed common structure;
6. the escape-search backlog contains no known Tier-A family with `NOT_TESTED`.

This still does **not** prove that every theory ever written is false or covered. It supports only the scoped claim that the major response-distinct mechanism classes in the maintained census have been tested under the frozen protocol.

## 6. New-model necessity criterion

A future original model becomes scientifically justified by the benchmark only if, after Tier-A closure and adversarial waves, at least one empirically relevant residual structure remains that:
- is not absorbable by any tested known-family manifold;
- survives exact common observation projection and covariance/nuisance profiling;
- is above numerical/gauge/systematic floors;
- has an acceptable physical/stability domain;
- supports a prospective withheld prediction;
- cannot be reproduced by a simple physically admissible combination of already-tested known mechanisms without adding equivalent new degrees of freedom.

Until then, the verdict is "new model motivated but not proven necessary".

## 7. Maintenance rule

After each model or wave:
1. update `matrices/model_family_census.csv`;
2. update `matrices/mandatory_properties_matrix.csv`;
3. update the model audit/result and benchmark matrix;
4. update design-prior maturity only with evidence;
5. update recovery and research log;
6. add newly discovered response-distinct literature mechanisms to the census rather than silently expanding scope in prose.
