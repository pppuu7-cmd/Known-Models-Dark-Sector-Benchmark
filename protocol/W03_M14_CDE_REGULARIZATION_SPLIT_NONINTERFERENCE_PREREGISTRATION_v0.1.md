# W03 M14 CDE regularization split / non-interference audit preregistration v0.1

Date: 2026-09-10
Upstream: `LisaGoh/CDE@b85a675af7544a5183e402964550811aa805b698`
Parent regularization run: `34489805857`

## Motivation

The preregistered combined R1+R2 independent verification layer made the exact beta=0 / exact-zero-field full forward model executable and its immutable exact-reference artifacts satisfy the frozen background and perturbation null conditions. However the original-vs-patched non-interference test failed at the `1e-12` threshold, with differences reaching `~1.2e-2` symmetric-relative in the lensed Cl table on the author branch.

Before concluding that the exact-null regularization changes physical predictions, separate three possibilities prospectively:

1. baseline run-to-run / OpenMP nondeterminism of this old CLASS fork;
2. R1 effect: exact `beta_z==0` branch before literal `beta_z/phi'` evaluation;
3. R2 effect: exact `rho_phi+p_phi==0` convention for the derived scalar velocity source/output.

No parent threshold or patch semantics may be relaxed.

## Frozen source variants

Create four copies from the exact upstream pin:

- `O`: untouched original;
- `R1`: only the previously preregistered exact `beta_prime==0.0 ? 0.0 : original_expression` change in scalar perturbation RHS;
- `R2`: only the two previously preregistered exact `rho_scf+p_scf==0.0 ? 0.0 : original_theta_ratio` changes;
- `R12`: both R1 and R2, byte-equivalent in semantics to the parent combined regularization.

No epsilon branch, source equation, IC, precision or physical parameter change is allowed.

## Frozen inputs

For each source variant use two physical workloads:

1. `AUTHOR`: committed author CDE.ini physics unchanged;
2. `B0TINY`: `beta_1=beta_2=beta_3=0`, committed scalar seeds retained.

Output roots alone distinguish cases.

Also run the untouched `O` AUTHOR and B0TINY workloads twice from the same executable (`O_A`, `O_B`) to measure same-binary repeatability.

## Frozen runtime controls

Primary comparison mode: set `OMP_NUM_THREADS=1` for **all** runs in this audit. This changes only numerical scheduling, not physics, and is frozen prospectively to remove parallel reduction/order ambiguity.

Record SHA256 of all four compiled standalone executables. Build all with the same `make class -j2` command; execution itself is OMP=1.

## Frozen output comparison

For each AUTHOR and B0TINY pair compare O_A against O_B, R1, R2 and R12 for:

- background.dat;
- pk.dat;
- pk_cb.dat;
- cl.dat;
- cl_lensed.dat;
- tk.dat.

Require same numeric shape, all finite values and

`max symmetric relative difference <= 1e-12`

per file, using the already frozen

`srel(x,y)=|x-y|/max(|x|,|y|,1e-300)`.

Do not compare raw scalar `theta_scf` diagnostic for R2/R12 because that is the intentionally regularized undefined coordinate.

## Frozen exact-reference split test

Run exact beta=0, exact `phi=phi'=0` under `R1` and `R2` separately, in addition to the already demonstrated R12 behavior:

- `R1_EXACT` full committed outputs;
- `R2_EXACT` full committed outputs.

For this split diagnostic, execution exit and required-output presence answer which transformation is necessary for the exact forward route. No new physical thresholds are introduced.

## Predeclared interpretation

- If O_A vs O_B itself violates `1e-12`, classify `BASELINE_NUMERICAL_REPEATABILITY_FAIL`; parent non-interference cannot be attributed uniquely to the patch and K4 numerical robustness becomes a first-order issue.
- If O_A vs O_B passes but a patch variant differs, that variant is `NONINTERFERING_FAIL` even if the difference is small compared with observations.
- A variant is `NONINTERFERING_PASS` only if every frozen physical output in both AUTHOR and B0TINY stays within `1e-12`.
- R1_EXACT/R2_EXACT results identify necessity/sufficiency only; they cannot override non-interference failure.

No source variant is authorized for K4/K5 unless a non-interfering exact-reference solution is demonstrated under the frozen rule.

No physical M14 family falsification is authorized.