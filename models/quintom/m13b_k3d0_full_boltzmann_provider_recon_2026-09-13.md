# M13b K3D0 full Einstein–Boltzmann provider capability reconnaissance — 2026-09-13

Protocol: `protocol/W03_M13B_K3D0_FULL_BOLTZMANN_PROVIDER_CAPABILITY_RECON_v0.1.md`  
Target: F13/M13b true two-field quintom  
Classification: `M13B_K3D0_NO_DIRECT_FULL_BOLTZMANN_PROVIDER_ADAPTER_BASE_REQUIRED`  
Physical falsification: **NO**

## Frozen search outcome

The preregistered public GitHub tranche was executed for quintom/CLASS, two-field dark-energy/CLASS, multi-scalar perturbation and multi-field Boltzmann terms. No public repository was located that simultaneously exposes a full late-time Einstein–Boltzmann hierarchy and a source-complete canonical+phantom two-field quintom implementation.

The 2026 Goh–Taylor paper remains the strongest scientific evidence that such an implementation exists: it explicitly states that CLASS was modified for a two-field quintom model and used for full Bayesian inference. However, the corresponding immutable modified CLASS source/commit is not publicly identified in the inspected author repositories, so it remains `RELATED_NOT_GRADE` for reproducible KMDSB execution rather than `DIRECT_PROVIDER_GRADE`.

## Candidate audit

### 1. `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`

Classification: **`ADAPTER_GRADE` — strongest / selected base**.

Evidence:

- public source-complete CLASS master, current inspected pin dated 2026-09-07;
- complete Einstein–Boltzmann architecture, including photon/polarization and ultra-relativistic hierarchies, Newtonian/synchronous gauges, recombination/thermodynamics, transfer functions and CMB/matter outputs;
- an explicit scalar-field (`scf`) species already exists at both background and perturbation-state level;
- background source uses canonical signs `rho_scf ~ +phi_prime^2/(2a^2)+V` and `p_scf ~ +phi_prime^2/(2a^2)-V`;
- the architecture exposes one scalar field through singular `phi_scf`, `phi_prime_scf`, `Omega_scf` and one pair of perturbation indices, not a two-field container;
- therefore unmodified CLASS is **not** a direct quintom provider and has no native phantom-sign second field;
- nevertheless it is the minimal-intrusion adapter base because the full Boltzmann/recombination/Einstein machinery should remain untouched while a second direct scalar species and its stress-energy signs are added at the species layer.

The K3C1 normalization and K3C2 ideal-fluid bridge provide independent regression controls for the future adapter and do not require importing the blocked Goh–Taylor numerical normalization.

### 2. `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`

Classification: **`ADAPTER_GRADE_SECONDARY`** (semantically `ADAPTER_GRADE`, lower priority).

It is a public CLASS-based full Einstein–Boltzmann solver and the inspected 2026 release is built on CLASS v3.3.4, but its extra dynamical scalar is the single Horndeski/modified-gravity degree of freedom. A canonical+phantom minimally coupled pair is not exposed as two independent direct matter scalar species. Using hi_class would add modified-gravity machinery irrelevant to the minimal quintom target and increase source intrusion relative to standard CLASS.

### 3. `mcataneo/mochi_class_public@2b0b16e4601effe416714ad330d2ee8cad289e4c`

Classification: **`ADAPTER_GRADE_SECONDARY`** (semantically `ADAPTER_GRADE`, lower priority).

The public README identifies mochi_class as an extension of hi_class/CLASS with a stable basis for a Horndeski scalar and full CMB/matter-spectrum execution. It is not a two-independent-field canonical+phantom realization. Its stability-basis scalar infrastructure is therefore not a direct replacement for the K3C2 field pair, and it offers no minimality advantage over standard CLASS for this task.

### 4. public LisaGoh repositories / Goh–Taylor trail

Classification: **`RELATED_NOT_GRADE_SOURCE_PROVENANCE_BLOCKED`**.

A public quintom modified-CLASS source is still absent. Adjacent public CLASS/mochi_class work cannot be reassigned as the missing quintom implementation. The K3C0 normalization blocker remains independent and unchanged.

### 5. `ja-vazquez/SimpleMC@a268fe5e2545428ddcf76b37b166a55dbf692fb0`

Classification: **`RELATED_NOT_GRADE_BACKGROUND_ONLY`**.

Useful existing M13b two-field background true-crossing evidence, but no source-complete photon/neutrino Boltzmann perturbation hierarchy.

### 6. `ja-vazquez/Scalar_Fields@a4ddce6049f601e090040889b4bb7af371c22921` and `igomezv/cosmo_tools@6f82a0dd6966ee2ab5abde2eb5c35dd0720b6ea1`

Classification: **`RELATED_NOT_GRADE_BACKGROUND_ONLY`**.

Both expose canonical/phantom-style background evolution but no full Einstein–Boltzmann perturbation closure.

## Decision

No `DIRECT_PROVIDER_GRADE` public implementation was found in the frozen tranche.

The selected independent adapter base is:

`lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.

Selection reason: it already supplies the required source-complete standard Einstein–Boltzmann hierarchy and one direct canonical scalar species while avoiding the additional single-scalar modified-gravity layers of hi_class/mochi_class. The future modification can therefore be constrained to a second direct scalar species plus the required canonical/phantom sign logic, with K3C1/K3C2 serving as external regression judges.

This decision does **not** modify CLASS, does not close K3, does not claim author-code reproduction and does not authorize K4/K5.

## Next authorized gate

Preregister an executable `K3D1` exact-pin CLASS adapter-base structural audit before writing the quintom patch. K3D1 must mechanically establish:

1. pinned CLASS builds/runs its standard control;
2. the full thermodynamics/Boltzmann/output stack is present;
3. the current `scf` implementation is singular (one field) and canonical-sign;
4. the exact source files/symbol families that must be extended are enumerated;
5. no modification to photon/neutrino hierarchy or recombination is required by the planned two-field species-layer adapter;
6. the adapter remains explicitly independent and uses K3C1/K3C2, not Goh–Taylor hidden normalization, as regression authority.
