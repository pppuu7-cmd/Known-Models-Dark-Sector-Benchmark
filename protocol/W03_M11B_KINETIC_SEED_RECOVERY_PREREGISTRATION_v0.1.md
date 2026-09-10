# W03 / M11b — covariant k-essence kinetic-seed recovery preregistration v0.1

Status: **FROZEN BEFORE RECOVERY RUN**

## Scope

This is an implementation-recovery gate only. It does **not** score B4–B8/K5–K9 and cannot promote the effective-fluid M11 result to the covariant k-essence family.

Pinned provider:

- `KunhaoZhong/CLASS_GSF`
- commit `07e015246c4b40f4e22bb50c9a0a63a621bb61f7`
- `model_gsf = 6`

The preceding probe built the binary and ran the pure LCDM control, but every model-6 GSF case stopped during background shooting/evolution with an NDF15 singular-matrix failure. That episode remains immutable evidence and is not rewritten by this recovery gate.

## Source-derived diagnosis

For `model_gsf == 6`, the pinned provider implements

\[
P(X,\phi)=\frac{X^{n+1}}{A^n}-V_0\phi^m,\qquad
n=\frac{1-c_s^2}{2c_s^2}.
\]

The preceding probe used `gsf_parameters = 6,1,0,0,0,1,1,m,cs2`. In this provider the initial conditions are read as

\[
\phi_{\rm ini}=p_1 10^{p_2},\qquad
\phi'_{\rm ini}=p_3 10^{p_4},
\]

so the previous probe set `phi'_ini = 0`. The model-6 derivatives contain powers such as `PXX ~ X^(n-1)`. Therefore the exact zero-kinetic start is a source-motivated candidate for the singular Jacobian seen by the integrator; this is a numerical/initial-state hypothesis, not a physical conclusion.

The provider's own committed DGF example uses a non-zero initial derivative scale `phi'_ini = 10^-17` (`gsf_parameters = 1,7,1,10,-18,-18,0.2,1` in its model-1 example). This motivates, but does not validate, the recovery ladder below.

## Frozen recovery ladder

No physical grid parameter from the preceding model-6 probe is changed. We test only the initial derivative seed.

Seed magnitudes:

- `1e-20`
- `1e-18`
- `1e-17`
- `1e-16`

For each magnitude test both signs where applicable.

Two diagnostic physical cases are frozen:

1. reference-like branch: `m=0`, `cs2=1.0`;
2. noncanonical branch: `m=1.0`, `cs2=0.90`.

The remaining parameters stay fixed to the previous probe conventions: `phi_ini=1`, `A=1`, `Omega_gsf=-1`, `Omega_Lambda=0`, `Omega_fld=0`, `gsf_tuning_index=6` (shoot `V0` for closure), `gsf_dxdy_guess=1`, `attractor_ic_gsf=no`, same cosmology, gauge, redshift nodes and P(k) range.

## Machine classification

For every seed/case, record the process exit code and retain the full log.

Terminal outcomes for this recovery gate:

- `RECOVERY_EXECUTABLE_REGION_FOUND`: at least one frozen non-zero seed executes both the reference-like and noncanonical diagnostic cases successfully.
- `RECOVERY_PARTIAL_EXECUTABLE_REGION`: successful non-zero seeds exist, but no single frozen seed magnitude/sign pair executes both diagnostic cases.
- `RECOVERY_NO_EXECUTABLE_REGION_IN_FROZEN_LADDER`: no frozen non-zero seed executes a diagnostic model-6 case successfully.
- `RECOVERY_BUILD_OR_CONTROL_FAILURE`: provider build or pure LCDM control fails.

These are implementation classifications only.

## Anti-promotion rule

A successful seed is **not** automatically a nuisance parameter and is **not** a scientifically authorized initial condition. If an executable region is found, the next mandatory gate must prospectively define the physical initial-state prescription (e.g. attractor/decaying-mode condition, independent shooting target, or explicit initial-state parameter with sensitivity profiling) before any covariant response comparison to M11 effective fluid is permitted.

No threshold, physical `m`, `cs2`, reference condition, response metric, or observational claim may be changed based on this recovery result.
