# W03 M14 IDECAMB K1 decoupling invariants — preregistration v0.1

Frozen: 2026-09-10

## Scope

This gate tests K1 for the independently pinned IDECAMB coupled-quintessence implementation. It does **not** claim an independent cross-solver equivalence test. The K1 promotion, if successful, is `PASS_WITH_SCOPE`: exact source-level interaction-off identities plus prospectively withheld numerical invariants on two scalar anchors not inspected in the prior infrastructure output.

## Provider

- `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`
- overlaid with `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`
- build compatibility only: `-fallow-argument-mismatch`; no source-physics edits.

## Frozen source identities

For `Class_IDE=2`, `UForm_CQ=1`, `QForm_CQ=1` the pinned source gives

- `Coup_CQ = beta * grhoc_t * gphidot`;
- `grhoca2_CQ = grhoc/a * exp[-beta (gphi-gphi0)]`;
- perturbative `gC` is built from `gQ=Coup_CQ`;
- perturbative `gD(1)=gQ`, `gD(2)=0`.

Therefore at exact `beta_cq=0`:

1. background energy transfer is exactly zero: `gQ=0`;
2. CDM returns to its uncoupled dilution law `grhoca2=grhoc/a`, so `a*grhoc_t` is constant;
3. active perturbation interaction-source coefficients vanish, subject to finite denominators on the tested nonzero-slope scalar anchors.

The author diagnostic `.quantity` rows are source-bound as:
`a, z, grhov_t, grhoc_t, adotoa, wde, gQ, gphi, gphidot, gU, dgU`.

## Prospective withheld anchors

The previous infrastructure route inspected only the author-center scalar slope `alpha_quint=0.02`. K1 uses two distinct anchors that have not been numerically inspected in KMDSB before this preregistration:

- A: `alpha_quint=0.2`, `beta_cq=0`;
- B: `alpha_quint=0.8`, `beta_cq=0`.

Both lie inside the author-declared prior `alpha_quint in [0,1.4]`. All other cosmological/theory settings use the already validated theory-only route unchanged. External likelihood DEFAULTs remain disabled only because this is a theory/reference gate, while `batch3/common.ini`, `action=4`, `get_sigma8=T`, H0 parameterization and CQ selectors remain unchanged.

## Frozen numerical conditions

For each anchor independently:

- build and run exit 0;
- log confirms coupled-quintessence class;
- `.quantity` exists with exactly 2000 numeric rows and 11 numeric columns;
- `.theory_cl` exists with numeric rows and all parsed values finite;
- every serialized `gQ` value (column 7) is exactly `0.0`;
- define `m_i = a_i * grhoc_t_i` from columns 1 and 4. Require `(max(m)-min(m))/mean(abs(m)) <= 2e-4`.

The `2e-4` tolerance is frozen from the known author diagnostic serialization `write(1,'(11E15.5)')`, not from either withheld K1 anchor. No threshold changes are allowed after execution.

## Classification

- `M14_IDECAMB_K1_DECOUPLING_PASS_WITH_SCOPE` iff both withheld anchors satisfy every condition.
- Any numerical invariant failure is `M14_IDECAMB_K1_DECOUPLING_FAIL` for this implementation/gate, not physical falsification of coupled quintessence.
- Build/configuration failures remain `BLOCKED_IMPLEMENTATION` and cannot be promoted to physics evidence.

If PASS: K2 can source-bind the signed/one-sided geometry of `beta_cq` using the author prior and equations, then a separately preregistered K4/K5 local response grid can be launched. The prior kabeleh/iDM K4 failure remains authoritative for that provider and is never overwritten.
