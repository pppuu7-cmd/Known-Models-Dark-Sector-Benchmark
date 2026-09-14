# W04 M21 G2B transfer-l sampling tail convergence v0.1

Frozen: 2026-09-14 after terminal run `34879864684` and before any new tail lane execution.

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Parent authority

The prerequisite terminal result is `M21_G2B_L_SAMPLING_INTERACTION_AND_DIRECTION_SUPPORTED` with cross-lane input identity true and monotone Emax contraction along:

- `LPAIR_I=(1.05,32)`, Emax `154.25643660087928`;
- `LPAIR_R=(1.026,25)`, Emax `34.305011087551506`;
- `LPAIR_T1=(1.015,20)`, Emax `13.582267651621091`;
- `LPAIR_T2=(1.010,15)`, Emax `2.543930110490425`, class `REMOVES`.

Exact source establishes that decreasing `l_logstep` and `l_linstep` gives a denser transfer multipole grid in this flat benchmark.

## Frozen tail

`LPAIR_T2` is an immutable parent anchor and is not reinterpreted or retuned.

Two new mandatory lanes:

- `LTAIL_T3`: `l_logstep=1.0075`, `l_linstep=12`;
- `LTAIL_T4`: `l_logstep=1.005`, `l_linstep=10`.

All other physical/numerical settings remain exactly the M21 baseline used by the parent: same `ref/f2/f3/f4`, exact provider pin, `cl_permille.pre + m21_ncdm_tight.pre`, generic `evolver=0`, same cosmology, outputs, k-range, ncdm settings and response metric.

No post-hoc point insertion or threshold change.

## Frozen metrics

For T2/T3/T4 report:

1. unchanged response excursion `Emax=max(E_TT,E_EE,E_TE)`;
2. direct TT/EE/TE normalized-R2 distances for each `ref/f2/f3/f4` between T2->T3 and T3->T4;
3. the maximum direct CMB distance over all cases/channels for each adjacent pair.

## Frozen classification

If parent authority, products, exact pin or cross-lane input identity fails -> `M21_G2B_L_SAMPLING_TAIL_AUDIT_BLOCKED`.

Otherwise:

- if T3 and T4 both classify `REMOVES` and max direct CMB distance satisfies `D(T3,T4) <= D(T2,T3)`, classify `M21_G2B_L_SAMPLING_TAIL_CONTRACTION_SUPPORTED_WITH_SCOPE`;
- if T3 and T4 both `REMOVES` but that contraction fails, classify `M21_G2B_L_SAMPLING_TAIL_REMOVAL_STABLE_DISTANCE_NONMONOTONE`;
- if either T3 or T4 ceases to `REMOVES`, classify `M21_G2B_L_SAMPLING_TAIL_REMOVAL_NOT_STABLE`.

No stronger global-convergence claim is allowed from this gate.

## Claim ceiling

Numerical transfer-grid convergence diagnostic only. No CLASS bug claim, production tuning recommendation, K1/K3/K4 promotion, or physical mixed-dark-matter verdict.
