# W03 M13b K3D2-D self-consistent reference-precision re-entry v0.1

Date frozen: 2026-09-14

## Trigger

The prospectively frozen self-consistent gauge-IVP successor completed run `34793433652` with classification

`M13B_K3D2C_SELF_CONSISTENT_GAUGE_IVP_DEFAULT_B123_PASS_WITH_SCOPE`.

The exact default NDF15 lane now has a same-initial-surface full-Boltzmann B1+B2+B3 PASS. The historical pre-IVP-fix `cl_ref.pre` explicit-RK result remains a numerical blocker localized to three intermediate k modes, but it cannot be carried forward unchanged because the qfield perturbation initial surface has now changed prospectively and materially.

## Purpose

Re-enter the exact upstream `cl_ref.pre` precision profile on the **same self-consistent gauge-mapped z=5 IVP** that passed the default lane, without changing any provider precision entry, solver selection, equation, cosmology, certified seam, target mode, scientific threshold, or gauge-map identity.

This gate answers two mutually exclusive questions in one frozen run:

1. Does exact `cl_ref.pre` now execute the self-consistent-IVP realization to completion and satisfy the already-frozen B1/B2/B3 + default/reference reproducibility criteria?
2. If not, what exact RK collapse geometry remains after the IVP correction?

## Frozen provider and stack

Provider remains exactly:

`lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`.

Apply, in the same order as the K3D2-C PASS:

1. independent qcf+qpf adapter;
2. conditional/floating-boundary background restart;
3. background U1 seam;
4. native perturbation z=5 interval split;
5. mapping-certified perturbation seam requiring exactly 12 tau ULP;
6. pure-undamped self-consistent gauge-IVP fixed point, max 16 iterations, exact zero target <= `1e-12`;
7. output-only diagnostics.

For the reference job only, the already source-audited error-reporting patches may additionally be applied:

- `verification/m13b/k3d2b_apply_solver_collapse_geometry_probe.py`;
- `verification/m13b/k3d2b_apply_direct_mode_failure_trace.py`.

These patches may change only error text/wrapping and must preserve the exact `generic_evolver` numerical arguments and original error buffer.

## Exact reference precision profile

Use the provider's exact pinned `cl_ref.pre` unchanged. In particular preserve:

- `evolver=0` (explicit RK);
- `tol_perturbations_integration=1.e-6`;
- all hierarchy cutoffs, approximation triggers, sampling settings, transfer thresholds and lensing accuracy settings exactly as shipped at the provider pin.

No copied or edited precision file is permitted.

## Frozen cosmology and output request

Identical to the K3D2-C default PASS:

- `h=0.6715`;
- `omega_b=0.0224`;
- `Omega_cdm=0.26172292868512664`;
- `Omega_g=5.4572897176151613e-05`;
- `Omega_ur=3.772710282384838e-05`;
- `N_ncdm=0`;
- `Omega_Lambda=Omega_fld=Omega_scf=Omega_k=0`;
- `qcf_U0=qpf_U0=0.3362232603714306`;
- `qcf_phi_ini=0.92`, `qcf_phi_prime_ini=0`;
- `qpf_psi_ini=1.02`, `qpf_psi_prime_ini=0`;
- synchronous runtime gauge;
- `A_s=2.1e-9`, `n_s=0.965`, `tau_reio=0.054`;
- `output=tCl,pCl,lCl,mPk,dTk`;
- `lensing=yes`;
- `l_max_scalars=1200`;
- `P_k_max_1/Mpc=1.0`;
- `z_pk=0`;
- frozen direct trajectories `K1=0.00022398828992555914` and `K10=0.0022398828992555913` 1/Mpc.

## Immutable default authority

The default comparison authority is the immutable successful artifact from run `34793433652`:

- artifact `10328826973`;
- digest `sha256:714380b4da09a3ddaf6f27448f844eec2e1d431422812bf84c2c1f3a5d50dbbc`.

The reference lane must not recompute or replace the default authority.

## Lane S — source/precision guard

Run independently from the reference solve. Require all of:

1. exact provider pin;
2. exact 12-ULP certified seam;
3. fixed-point algorithm remains pure undamped Picard, max 16, target `1e-12`;
4. provider `cl_ref.pre` file hash/content is unmodified by the workflow;
5. `evolver=0` and `tol_perturbations_integration=1.e-6` are present in exact `cl_ref.pre`;
6. collapse-geometry patch changes error text only and does not change solver logic/tolerances;
7. direct-mode failure wrapper preserves `generic_evolver` arguments and original error buffer;
8. no protected equation/module/cosmology parameter is changed.

## Lane R — exact reference execution

Execute the frozen full qcf+qpf cosmology with the exact `cl_ref.pre` profile.

### If provider rc = 0

Require:

- self-consistent boundary fixed point converged <= `1e-12` within 16 iterations;
- run the unchanged `verification/m13b/k3d2b_verify_full_default.py` on reference outputs with prefix `ref` in an isolated result directory;
- reference B1, B2 and B3 must all pass the same historical scientific gates.

Then compare reference against immutable default authority with the **already frozen K3D2-B two-precision thresholds**:

- crossing redshift absolute difference <= `2e-3`;
- each today `x,p,y,q` absolute difference <= `1e-3`;
- linear P(k) normalized L2 on the common reported k range <= `5e-3`;
- TT normalized L2 on common `30<=ell<=1200` <= `5e-3`.

No new precision threshold is introduced.

### If provider rc != 0

Do not evaluate or infer B1/B2/B3 or default/reference reproducibility. Instead parse the already authorized diagnostic-only source output and record:

- failing mode count and k range;
- whether frozen K1 or K10 fail;
- collapse tau range/statistics;
- `hdid`, `hnext`, normalized step ratio and minimum ratio where available;
- step indices and native interval geometry.

This is a numerical/provider blocker, not physical falsification.

## Aggregate classifications

If S passes, provider rc=0, fixed-point identity passes, reference B1/B2/B3 pass, and all four frozen default/reference numerical thresholds pass:

`M13B_K3D2D_SELF_CONSISTENT_REFERENCE_PRECISION_PASS_WITH_SCOPE`.

If S passes but exact reference provider rc!=0 with diagnostic geometry captured:

`M13B_K3D2D_SELF_CONSISTENT_REFERENCE_RK_NUMERICAL_BLOCKER_LOCALIZED`.

If provider executes and scientific reference B1/B2/B3 or frozen default/reference comparison fails:

`M13B_K3D2D_SELF_CONSISTENT_REFERENCE_PRECISION_SCIENTIFIC_OR_NUMERICAL_GAP`.

If source/precision provenance guard fails:

`M13B_K3D2D_REFERENCE_REENTRY_IMPLEMENTATION_BLOCKED`.

## Claim ceiling

Even a full two-precision PASS here means only a scoped independent CLASS-adapter numerical reproducibility result. It does not reproduce the unavailable author code or public `V0` normalization map.

All outcomes preserve:

- historical synchronous-zero B3 gap;
- historical one-step gauge-IVP blocker;
- old pre-IVP-fix RK geometry result as immutable history;
- `K3_state_ceiling=PARTIAL` unless a separate explicit K3 closure promotion is prospectively authorized;
- `K4_promoted=false` in this gate;
- `K5_promoted=false`;
- `author_model_reproduced=false`;
- `published_V0_reproduced=false`;
- `author_normalization_map_claimed=false`;
- `physical_falsification=false`.
