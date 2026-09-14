# M21 CLASS reference-profile monotonicity audit — 2026-09-14

Provider authority: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540` (CLASS v3.3.4).

Purpose: outcome-independent interpretation audit performed while M21 stage-3 numerical jobs are non-terminal. It changes no frozen stage-3 input, threshold, or classifier.

## Exact profile facts

At the exact pin, `cl_permille.pre` contains only a small set of scalar-Cl precision overrides, notably `hyper_flat_approximation_nu=7000`, transfer-neglect thresholds, and `delta_l_max=1000`.

The exact `cl_ref.pre` labels itself as a profile giving CMB spectra stable at the 0.01% level, but it is a composite profile rather than a componentwise monotone tightening of current defaults. In particular it contains:

- active transfer/sampling refinements such as `l_logstep=1.026`, `l_linstep=25`, `hyper_sampling_flat=12`;
- legacy/unconsumed entries such as `recfast_Nz0=100000` at this pin;
- declared but runtime-unconsumed `recfast_x_He0_trigger_delta=0.01` and `recfast_x_H0_trigger_delta=0.01` at this pin;
- `tol_thermo_integration=1e-5` while exact `include/precisions.h` default is `1e-6`.

For a tolerance defined as the allowed relative integration error, `1e-5` is numerically looser, not tighter, than `1e-6`.

## Historical persistence

Commit `45195306dac09fab6bd9cf23320974f418c81f27` (2023-10-10, `cl_ref.pre in agreement with new perturbations denominations`) already has the same `cl_ref.pre` blob SHA `ccb86d11f72d9fa754b18dca40d23378b90c0699` as the exact M21 pin. At that same 2023 commit, `include/precisions.h` already defines `tol_thermo_integration=1e-6` by default.

Thus the `cl_ref` thermodynamics tolerance being looser than the default is not a transient 2025 pin mismatch introduced after the profile was created; it has coexisted with the profile for at least the checked 2023→2025 interval.

## Consequence for M21 precision interpretation

Stage-1/stage-2 use of CLASS reference-profile components is valid as a numerical path-decomposition experiment, but `cl_ref.pre` must not be interpreted as an ordered convergence ladder in which every changed key increases precision.

Therefore:

1. a subgroup that removes the f3 CMB excursion shows sensitivity to that reference-profile path;
2. it does not by itself establish that the baseline was under-resolved;
3. an individual setting that removes the excursion does not become an authorized production setting;
4. if stage-3 identifies `tol_thermo_integration=1e-5` as sufficient, a separate prospective tolerance-direction/convergence gate is required to determine whether the effect represents convergence, a solver-path branch, or a non-monotone numerical artifact;
5. K1/K3/K4 and physical mixed-DM conclusions remain unchanged.

## Interpretation ceiling

This audit establishes only that the exact CLASS `cl_ref` profile is not componentwise monotone relative to exact-pin defaults. It does not call the profile erroneous, does not claim a CLASS bug, does not decide stage-3, and does not establish any physical property of mixed cold+warm dark matter.
