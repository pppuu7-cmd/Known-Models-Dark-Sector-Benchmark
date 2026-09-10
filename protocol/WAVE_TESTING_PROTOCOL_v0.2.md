# KMDSB Wave Testing Protocol v0.2

Frozen: 2026-09-10
Status: ACTIVE
Supersedes for active planning: `WAVE_TESTING_PROTOCOL_v0.1.md`.
Companion coverage contract: `REQUIRED_PROPERTIES_COVERAGE_PROTOCOL_v0.1.md`.
Census authority: `matrices/model_family_census.csv`.

## Core change in v0.2

Waves are now **coverage-driven**. A wave cannot be declared complete merely because a convenient subset was run. Every Tier-A family assigned to that wave must reach a terminal K0-K9 state appropriate to the evidence available, including explicit blocked states.

Every tested family still keeps its B0-B9 model audit. The K0-K9 matrix is the cross-model mandatory-properties view.

## Preserved completed waves

### W00 — Calibration and semantics — COMPLETE
M00 LambdaCDM; M01 constant-w smooth DE.

### W01 — Baseline dark-sector atlas — COMPLETE
M02 IDE; M03 GDM; M04 thermal WDM; M05 designer f(R); M06 DCDM->DR.

### W02 — Same-observable degeneracy attack — COMPLETE
Pairwise/channel graph pressure including IDE/GDM, IDE/f(R), WDM alternative-suppression blocker and temporal-profile control.

## W03 — Dark-energy mechanism census — ACTIVE

Already tested:
- M07 canonical quintessence;
- M08 CPL smooth w(a);
- M09 upstream CLASS native-EDE implementation control — BLOCKED_IMPLEMENTATION;
- M10 CLASS_EDE axion-like scalar EDE — theory-response discrimination vs CPL.

Mandatory remaining Tier-A queue:
- M11 k-essence / kinetic DE;
- M12 phantom scalar DE;
- M13 quintom / phantom-divide crossing;
- M14 coupled quintessence / scalar-DM coupling;
- M15 generalized Chaplygin / unified dark fluid.

Tier-B W03 queue unless shown represented by an existing manifold:
- M16 running/interacting vacuum;
- M17 holographic DE;
- M18 ghost-condensate kinetic branch.

W03 exit criteria:
1. every Tier-A DE row has terminal K0-K6;
2. each claimed distinct survivor has K7 terminal or an explicit exact-operator blocker;
3. flexible smooth-DE CPL is not the only comparator; noncanonical/crossing/coupled/unified families are included;
4. every apparent novel DE direction is attacked by the strongest implemented DE manifold, not one ray;
5. all solver implementation gaps remain in the matrix.

## W04 — Dark-matter mechanism census — PLANNED

Already available controls carried forward:
- M03 GDM;
- M04 thermal WDM;
- M06 DCDM->DR.

Mandatory Tier-A additions:
- M19 fuzzy/ultralight axion DM;
- M20 self-interacting DM with an explicitly relevant nonlinear response block;
- M21 mixed cold+warm DM;
- M22 annihilating DM;
- M23 DM-dark-radiation scattering / dark acoustic oscillations.

Tier-B adversarial additions:
- M24 ETHOS-like interacting dark sector;
- M25 resonant sterile-neutrino-like WDM;
- M26 primordial-black-hole DM;
- M27 dynamical dark matter ensemble;
- M28 superfluid/emergent collective DM if it exhibits a distinct cosmological response.

External comparator:
- F46 massive-neutrino/hot-DM free-streaming response, explicitly preserving known-sector subtraction.

W04 exit criteria:
- thermal cutoff, wave/Jeans cutoff, mixed fraction, acoustic/drag, temporal decay/annihilation and nonlinear self-interaction channels must all be represented or explicitly blocked;
- WDM attribution cannot be promoted without alternative suppression mechanisms on common k,z grids.

## W05 — Modified-gravity census — PLANNED

Existing control:
- M05 designer f(R).

Mandatory Tier-A additions:
- M29 Brans-Dicke/scalar-tensor;
- M30 Horndeski/EFT-DE flexible scalar-tensor manifold;
- M31 beyond-Horndeski/DHOST;
- M32 DGP braneworld;
- M33 covariant Galileon;
- M34 massive/bimetric gravity;
- M35 Einstein-Aether/vector-tensor.

Tier-B/C escape queue:
- M36 TeVeS/relativistic MOND-like;
- M37 f(T);
- M38 f(Q);
- M39 nonlocal gravity;
- M40 Horava-Lifshitz;
- M41 mimetic gravity/dark matter.

W05 exit criteria:
- scalar, vector, tensor/spin-2, braneworld and torsion/nonmetricity response classes represented or explicitly blocked;
- every dark-sector survivor from W03/W04 attacked by at least one sufficiently flexible MG manifold on a valid common block;
- GW/tensor constraints included where physically defined rather than silently masked as zero.

## W06 — Unified-sector, geometry and adversarial mimicry — PLANNED

Targets:
- M15 unified dark fluid revisited against split DE+DM constructions;
- M41 mimetic unified gravity/DM;
- M42 LTB/void acceleration;
- M43 cosmological backreaction/averaging;
- deliberate mixtures/combinations of already tested known families when physically admissible.

Central question: can a combination of known mechanisms absorb every apparent single-family novelty without adding an effectively new response degree of freedom?

## W07 — Cross-family rigidity — PLANNED

Construct the valid common-block graph over all terminal Tier-A models.
For every candidate surviving response structure:
- profile full nearest-family manifolds;
- then profile physically admissible multi-family combinations;
- record minimal discriminating observable suites as a graph/set-cover problem;
- preserve theory-space and observation-space graphs separately.

## W08 — True holdout — PLANNED

Freeze any proposed common relation/architecture before opening selected mechanism families or observation blocks not used in its construction.
No within-family interpolation counts as W08 closure.

## W09+ — escape search — PLANNED/ITERATIVE

Continuously search literature and implementations for:
- response-distinct mechanisms absent from the census;
- solver/parameter-domain failures that invalidate prior comparisons;
- families that mimic a claimed survivor;
- new observation operators/covariances that change identifiability;
- models currently classified `REPRESENTED_BY` that escape the representative family in an orthogonal channel.

## Completion language

Allowed after Tier-A closure: `major known cosmological response-distinct mechanism families covered under KMDSB v0.2 census`.

Not allowed: `all theories are false`, `all conceivable models were tested`, or a percentage of theory space inferred from catalogue counts.
