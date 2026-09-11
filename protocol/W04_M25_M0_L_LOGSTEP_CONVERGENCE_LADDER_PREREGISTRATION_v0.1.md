# W04 M25 m0 `l_logstep` convergence ladder preregistration v0.1

## Trigger

The combined M25 m0 multipole-sampling diagnostic reduced the eta=0.003 CMB excursion strongly but did not recover the original eta-tail power-law gate. Parameter isolation then showed that `l_logstep=1.026` carries almost the entire effect: eta=0.003 improvement factors are about 16.9 (TT), 144.6 (EE), and 106.8 (TE), while `l_linstep=25` gives only about 5--6x improvement. P(k) is unchanged by either multipole-sampling parameter and is explicitly outside this CMB ladder gate.

The purpose of this ladder is to test whether the residual CMB behavior converges to a stable numerical floor as logarithmic multipole sampling is refined.

## Frozen setup

Use pinned CLASS `e85808324f51fc694d12e3ed7439552a3c3f9540`, quadrature capacities 4000/4000, the original m0 ref/e2/e3/e4 cases, and the source-matched common profile:

- `tol_ncdm_bg=1e-6`
- `tol_ncdm=1e-6`
- `ncdm_fluid_approximation=3`

Run seven independent `l_logstep` values in parallel:

`{1.10,1.08,1.06,1.04,1.03,1.026,1.02}`.

Provider default `l_linstep=40` remains untouched. No PSD, sterile-DM abundance, eta value, cosmological parameter or physical model parameter is changed.

## Frozen measurements

For each value use the existing M25 precision-floor analyzer and record TT/EE/TE/P(k) r95 values at eta={0.01,0.003,0.001}, the original tail exponent and original `tail_scaling_recovered` Boolean.

For CMB only define:

- `excursion_collapse`: baseline/source-matched eta=0.003 p95 divided by ladder-point eta=0.003 p95 >=5 in TT, EE and TE;
- `floor_flatness`: for each of TT/EE/TE, `max(r95_eta)/min(r95_eta) <= 2.0` across the three eta values;
- `fine_pair_stability`: between l_logstep=1.026 and 1.02, symmetric relative difference of each eta-specific r95 <=0.25 for every TT/EE/TE point;
- `stable_floor_localization`: 1.026 and 1.02 both satisfy excursion_collapse and floor_flatness, and fine_pair_stability passes.

The above is a numerical-localization gate, not a replacement for physical K1. P(k) is measured but cannot cause this CMB ladder to pass or fail.

## Interpretation

`M25_M0_L_LOGSTEP_STABLE_NUMERICAL_FLOOR_LOCALIZED` means the deterministic eta=0.003 CMB excursion has been traced to multipole sampling and the remaining CMB residual is stable under further refinement with a bounded eta-floor spread. It does NOT promote K1 or K4. The separate P(k) numerical tail and a final floor-aware K1 decision remain open.

`K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false`.
