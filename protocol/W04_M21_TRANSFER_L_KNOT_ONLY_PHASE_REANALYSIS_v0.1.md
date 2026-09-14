# W04 M21 transfer-l knot-only phase reanalysis v0.1

Frozen: 2026-09-14 after terminal `M21_L_GRID_PHASE_L400_SIGNATURE_SUPPORTED_WITH_SCOPE` and after a clearly labeled post-terminal exploratory check of two contrast lanes (`P400_EVEN_TAIL_OFF`, `P400_OFF_TAIL_OFF`) suggested that their HIGH/CALM contrast is already present on sparse-l knot values. The remaining two mandatory factorial lanes have not been used in any knot-only classifier before this preregistration.

This gate reuses immutable artifacts from parent run `34887488405`; it performs no CLASS rerun and changes no physics or numerical profile.

## Question

Is the established l=400 phase signature already carried by the computed C_l values at the sparse transfer/harmonic l knots themselves, or does it emerge only when CLASS interpolates from those sparse knots to the full integer-l output grid?

## Parent authority

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.
Parent protocol: `protocol/W04_M21_TRANSFER_L_GRID_PHASE_FACTORIAL_v0.1.md`.
Parent run: `34887488405`.
Parent aggregate artifact: `10366460225`, digest `sha256:07a99a5e539c06d0df3608933b4df9ee4234d9fcf3b5a57eb6fa36eed237b113`.

Mandatory reused lane artifacts:

- `P400_OFF_TAIL_ON`: artifact `10366295676`, digest `sha256:a0169764cc155e55a0908c61a4b26673b5986cf6a5946f3f58e65285acf017ad`;
- `P400_OFF_TAIL_OFF`: artifact `10365669355`, digest `sha256:bb2934875f92a84db8341cd2541e466b1d1fd52296e6ae2a1204aa0a14614afa`;
- `P400_EVEN_TAIL_OFF`: artifact `10365598517`, digest `sha256:a8f16fcc7a7476abd542595a21161210781484fda9474f47f34548c1db64e62b`;
- `P400_ON_TAIL_OFF`: artifact `10365592822`, digest `sha256:628b8a4e6c33e715cd36484e4a7a17416c2b7f5310f984cfbfec64955cb74980`.

Every reused lane must retain exact parent provider/input/profile identity and `ref/f2/f3/f4` rc=0.

## Frozen sparse-l reconstruction

For each lane, regenerate the exact flat `transfer_get_l_list()` sequence from its immutable `(l_logstep,l_linstep)` and `l_max=2500`:

1. start at `l=2`;
2. logarithmic increment `max(int(l*(l_logstep-1)),1)` while the next point remains below l_max and increment remains below l_linstep;
3. then use linear increment `l_linstep` while the next point is <= l_max;
4. append exact `l_max` if not already present.

The regenerated list must exactly match the parent lane manifest node count, l=400/l=2499 flags, nodes 394--406, and final-eight-node signature. Any mismatch is BLOCKED.

## Frozen knot-only observable

For each lane and CMB channel `TT,EE,TE`, read the immutable integer-l `cl.dat` tables and select **only rows whose l belongs to the regenerated sparse-l list**.

For each warm case `f2/f3/f4`, relative to the same-lane exact-CDM `ref`, compute normalized response

`R2_knot(case,channel)=||C_case-C_ref||_2/max(||C_ref||_2,1e-300)`

over the full sparse-knot vector.

Primary knot excursion:

`E_EE_knot = R2_knot(f3,EE)/max(R2_knot(f2,EE),R2_knot(f4,EE),1e-300)`.

Reuse the exact parent state boundary:

- HIGH if `E_EE_knot > 3`;
- CALM otherwise.

TT/TE knot excursions are report-only.

## Frozen knot pattern classifier

Classify `M21_L_GRID_KNOT_VALUES_CARRY_L400_SIGNATURE_WITH_SCOPE` if:

- `P400_ON_TAIL_OFF` knot state HIGH;
- `P400_EVEN_TAIL_OFF` knot state HIGH;
- `P400_OFF_TAIL_ON` knot state CALM;
- `P400_OFF_TAIL_OFF` knot state CALM.

If that exact knot pattern fails while the immutable parent full-output pattern remains the established l=400 signature, classify `M21_L_GRID_PHASE_SIGNATURE_EMERGES_OR_CHANGES_BETWEEN_KNOTS`.

Artifact/input/list/table failure -> `M21_L_GRID_KNOT_ONLY_REANALYSIS_BLOCKED`.

## Frozen report-only support bands

For EE knot-only response, also report the same four predeclared l bands:

- 2--399
- 400--800
- 801--1500
- 1501--2500

For each lane/band report knot count and E_EE_knot_band. These bands cannot alter the primary classifier.

## Consequence

- CARRY_L400_SIGNATURE: final integer-l harmonic spline is not necessary for the phase signature; localization moves upstream to transfer/harmonic integral values evaluated at sparse l knots.
- EMERGES_OR_CHANGES_BETWEEN_KNOTS: final sparse-l interpolation remains a required part of the phase mechanism.
- BLOCKED: infrastructure recovery only.

## Interpretation ceiling

This is a numerical mechanism reanalysis of already-generated data. It does not establish a CLASS bug, a globally converged spectrum, a production precision setting, K1/K3/K4, or a physical mixed-dark-matter conclusion.