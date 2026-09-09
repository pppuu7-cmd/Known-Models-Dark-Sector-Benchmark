# W03 M07/M08 common ShapeFit observation-operator contract v0.1

Frozen: 2026-09-09  
Status: **PROSPECTIVELY FROZEN / SCOPED CROSS-FAMILY OBSERVATION CONTROL**  
DSIR observation-methodology overlay: `Dark-Sector-Influence-Reconstruction@864952e1520d82473a9e976edfeb69f9899d174d` (KMDSB AD-002)

## 1. Purpose

Test the step-stable local M07 canonical-quintessence direction against the step-stable M08 CPL local comparator **after both families are propagated through one exact common observation mapping and one exact covariance coordinate vector**.

This contract is frozen before executing the joint M07/M08 ShapeFit workflow.

It is not DSIR Article-2 G5 closure. It is a two-family scoped observation-control that adopts the coordinate-compatibility rules of the new G5 contract.

## 2. Scientific question

M08 absorbs the M07 local P+H direction to about 1.1% residual in unwhitened theory-response space.

The observation-space question is:

> after an identical ShapeFit mapping, covariance whitening and profiling of the full 2D local CPL span, how much covariance-weighted information remains in the M07 q=lambda^2 direction?

The primary quantity is the **absolute profiled significance**, not just angle or residual fraction.

## 3. Frozen solver/reference authority

All models in this test use the same pinned solver:

`lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Common cosmological inputs:
- `h=0.67`;
- `omega_b=0.0224`;
- `omega_cdm=0.1200`;
- `Omega_k=0`;
- `reio_parametrization=reio_none`;
- linear scalar mode;
- synchronous internal solver gauge;
- `write background=yes`.

The **single common reference** is pure LambdaCDM with both `Omega_fld=0` and `Omega_scf=0`; Lambda is inferred by closure.

Every M07 and M08 observable response is formed relative to this exact same reference output.

## 4. M07 local input branch

M07 is the controlled canonical scalar branch already audited in W03:

`V=(1+A) exp(-lambda phi)`, `phi_ini=1`, `phi_prime_ini=0`, `scf_tuning_index=2`, strict `tol_shooting_deltax_rel=1e-13`.

Local quotient coordinate:

`q=lambda^2`.

The joint workflow runs `lambda={0.025,0.075}` and defines the local M07 ShapeFit derivative as the componentwise mean

`j_q = 0.5 * [ r(lambda=.025)/(.025^2) + r(lambda=.075)/(.075^2) ]`.

The two q-scaled mapped vectors must also be reported separately; no hidden replacement by one preferred lambda is allowed.

## 5. M08 local comparator branch

M08 is the CPL/CLP fluid branch:

`w(a)=w0+wa(1-a)`

with
- `epsilon0=1+w0`;
- `epsilon_a=wa`;
- `cs2_fld=1`;
- `use_ppf=yes`;
- `Omega_Lambda=0`;
- `Omega_fld` inferred by closure.

Frozen central step for this joint observation test:

`h=1e-3`.

Directions:

`j_0 = [r(epsilon0=+h)-r(epsilon0=-h)]/(2h)`

`j_a = [r(wa=+h)-r(wa=-h)]/(2h)`.

The independent M08 step-stability audit already tests h=1e-3 vs 5e-4; this joint test does not choose its step after seeing observation-space output.

## 6. Exact common ShapeFit coordinate vector

Use five corrected DESI DR1 ShapeFit bins in this fixed order:

1. `LRG1`, z=0.51
2. `LRG2`, z=0.71
3. `LRG3`, z=0.92
4. `ELG2`, z=1.32
5. `QSO`, z=1.49

For every bin use exactly three coordinates in this order:

1. `DH_over_DM`
2. `f_sigma_s8_control`
3. `m_plus_n_control`

Global 15-coordinate order is therefore

`[LRG1:AP,growth,shape, LRG2:AP,growth,shape, LRG3:AP,growth,shape, ELG2:AP,growth,shape, QSO:AP,growth,shape]`.

No coordinate may be added, dropped, reordered or zero-filled after outputs are inspected.

## 7. Frozen common operator R

For a CLASS background output `M` and common reference `R0`, at bin redshift z:

### AP coordinate

`AP_M(z) = AP_fid(z) * [(H_R0/H_M) * (DM_R0/DM_M)]`.

Response:

`r_AP = AP_M - AP_fid`.

### Growth coordinate

Using CLASS background normalized growth `D` and growth rate `f`:

`G_M(z) = G_fid(z) * [(D_M f_M)/(D_R0 f_R0)]`.

Response:

`r_G = G_M - G_fid`.

### Shape coordinate

For this deliberately late-time scoped control:

`r_shape = 0` for both M07 and M08.

This is the same frozen late-time control assumption used by the earlier M01/M07 ShapeFit tests. It is a limitation of this operator, not a statement that the physical theories have no early-time or transfer-shape effects in every realization.

Crucially, the same operator and the same shape assumption are applied to **both families**.

## 8. Exact covariance C

Covariance source semantics are inherited from the corrected 2026 DESI DR1 ShapeFit control used by KMDSB M01/M07 and DSIR Experiment 009.

For each bin, start from the frozen 4x4 covariance table and select indices `[1,2,3]`, then multiply by `1e-4`.

The joint 15x15 covariance is the block diagonal matrix of the five selected 3x3 bin covariances in the exact order above.

No cross-bin covariance is introduced in this scoped control because the earlier frozen control does not provide one.

No covariance regularization, eigenvalue trimming, shrinkage or pseudoinverse may be introduced after output inspection.

Required controls before science scoring:
- exact shape `15x15`;
- numerical symmetry check;
- Cholesky factorization PASS;
- finite positive condition number reported;
- whitening roundtrip residual reported.

If Cholesky fails, the test is `BLOCKED_COVARIANCE`; do not regularize post hoc.

## 9. Whitening and profiling

Factor

`C = L L^T`.

Whitened directions:

`j_q^w = L^-1 j_q`

`J_CPL^w = L^-1 [j_0,j_a]`.

Fit one shared CPL parameter vector per unit q:

`c* = argmin_c || j_q^w - J_CPL^w c ||_2`.

Report:
- whitened M07 norm;
- singular values of whitened `J_CPL`;
- best coefficients `(epsilon0/q, wa/q)`;
- whitened residual norm and residual fraction;
- angle of M07 to the CPL subspace via `asin(residual_fraction)` where applicable;
- full 3x3 Fisher/Gram matrix for `[q,epsilon0,wa]`.

Profiled local information for q is the Schur complement

`F_q,prof = F_qq - F_qm F_mm^-1 F_mq`.

Report

`sigma_q,prof = 1/sqrt(F_q,prof)`

when positive and numerically resolved.

Also report unprofiled `sigma_q` and degradation factor.

## 10. Frozen interpretation threshold

Use the largest already-frozen M07 production deformation

`lambda=0.30`, `q=0.09`

only as a scale probe; it was not chosen after this observation-space result.

Define local profiled significance

`S_0.09 = 0.09/sigma_q,prof`.

Classification in this scoped common-operator control:

- if `S_0.09 < 1`: `NONIDENTIFIABLE_AFTER_CPL_PROFILING_IN_COMMON_SHAPEFIT_CONTROL`;
- if `S_0.09 >= 1`: `IDENTIFIABLE_AT_Q_0P09_AFTER_CPL_PROFILING_IN_COMMON_SHAPEFIT_CONTROL`.

This 1-sigma boundary is a benchmark identifiability screen, not a discovery threshold.

No threshold is frozen for whitened angle alone. Geometry is descriptive unless absolute information is adequate.

## 11. Fail-closed rules

The joint workflow must fail/stop classification if:
- any model run fails;
- any expected background column is missing;
- coordinate order differs between families;
- covariance shape/order is not exact;
- covariance Cholesky fails;
- M08 comparator Fisher block is singular beyond ordinary numerical precision;
- any family-specific operator substitution is attempted.

No zero imputation and no post-hoc coordinate deletion.

## 12. Scientific boundaries

Even a successful run is **not**:
- a full DESI likelihood;
- DSIR Article-2 G5 closure;
- proof that CPL and quintessence are globally equivalent;
- proof that either family is the physical dark-energy mechanism;
- permission to rebase older KMDSB evidence onto DSIR `864952e...`.

It is a controlled answer to one narrower question: whether the M07 local q direction carries observable information outside the M08 local CPL span under one common, exact, frozen ShapeFit control operator and covariance.
