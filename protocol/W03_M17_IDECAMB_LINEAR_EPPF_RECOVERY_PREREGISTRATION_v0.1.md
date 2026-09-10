# W03 / M17 IDECAMB linear-ePPF recovery preregistration v0.1

Frozen: 2026-09-10
Status: PREREGISTERED
Family: F17/M17 original future-event-horizon holographic dark energy
Provider: `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075` over `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`

## 1. Purpose

Test whether the prior M17 execution blocker belongs to the linear HDE/ePPF route or to the parent CosmoMC nonlinear-lensing/HMCode layer.

The prior c=0.8 smoke retained `use_nonlinear_lensing=T` through `batch3/common.ini` and terminated internally with the HMCode-class diagnostic `Integration timed out`. Source audit also shows that NaN `.quantity` columns 8-11 are coupled-quintessence-only writer fields and are not HDE perturbation variables.

This recovery therefore removes **only nonlinear lensing/HMCode** while preserving the original HDE background law, uncoupled beta=0 branch, ePPF prescription, scalar CMB lensing and the same pinned sources.

## 2. Frozen model point

Starting from the provider `test_ide.ini` at the frozen overlay pin:

- disable external Planck/BAO/Pantheon likelihood DEFAULT lines exactly as in the prior provider-control harness;
- retain `DEFAULT(batch3/common.ini)`;
- override after that include with `use_nonlinear_lensing = F`;
- retain `CMB_lensing = T` from common.ini;
- `Class_IDE = 1` (coupled-fluid class);
- `WForm_CF = 2` (HDE);
- `Use_PPF = T`;
- `param[c_hde] = 0.8`;
- `param[beta_cf] = 0`;
- `CovQForm_CF = 1` remains unchanged but is inert at beta=0;
- `action = 4`;
- activate `test_output_root = m17_linear_c080`;
- disable the stale expected-likelihood scalar `test_check_compare` because likelihood DEFAULTs are disabled.

No HDE/ePPF source code, initial condition, precision setting, parameter value or closure equation may be changed.

## 3. Execution isolation gate

The runtime log must explicitly report:

- `Doing non-linear Pk: F`;
- `Doing CMB lensing: T`;
- `Doing non-linear lensing: F`.

If nonlinear lensing remains T, the test is invalid and classified as a harness/configuration failure, not a provider result.

External watchdog: 900 s. A normal exit must occur before the watchdog. The workflow records elapsed wall time.

## 4. Required HDE outputs

Require:

1. non-empty `m17_linear_c080.theory_cl`;
2. non-empty `m17_linear_c080.quantity`;
3. every numeric entry in `.theory_cl` finite;
4. at least 1000 finite numeric rows in `.theory_cl`;
5. `.quantity` has exactly 2000 numeric rows and at least 11 columns as written by the provider;
6. HDE-relevant `.quantity` columns 1-7 are finite on all 2000 rows;
7. column 7 (`gQ`) is zero within maxabs `1e-14` for beta=0.

Columns 8-11 of `.quantity` are archived but explicitly **masked from HDE pass/fail**, because the source writer unconditionally evaluates coupled-quintessence-only `gphi/gphidot/gU/dgU` fields even in the coupled-fluid HDE branch.

No missing/NaN entry in columns 8-11 is zero-imputed.

## 5. Scientific interpretation

If all gates pass, classify:

`M17_IDECAMB_LINEAR_EPPF_PROVIDER_PASS_WITH_SCOPE`

and interpret K3 only as:

`PASS_WITH_SCOPE_EPPF_PRESCRIPTION`.

This means the public pinned provider can execute a finite linear scalar HDE model with its ePPF effective closure. It does **not** prove that ePPF is the unique physical perturbation theory of the nonlocal future event horizon.

The prior full/default route remains recorded as HMCode/nonlinear-lensing blocked. It is not deleted.

If the linear route still times out or fails before producing finite theory spectra, classify:

`M17_IDECAMB_LINEAR_EPPF_BLOCKED_EXECUTION`.

If execution succeeds but required outputs are nonfinite/missing, classify:

`M17_IDECAMB_LINEAR_EPPF_OUTPUT_FAIL`.

If the runtime isolation flags are not as frozen, classify:

`M17_IDECAMB_LINEAR_EPPF_INVALID_HARNESS`.

No outcome is a direct physical falsification of original HDE.

## 6. Next gate if PASS

A PASS authorizes a finite global perturbation-level geometry/nearest-manifold attack at the already frozen HDE points `c={0.6,0.8,1.0,1.2}` using the linear-ePPF route. Because M17 has no native LambdaCDM intersection in `c`, no local LambdaCDM tangent is manufactured.

The existing background result (96.7-98.9% CPL absorption) remains valid but insufficient for perturbation-level equivalence.
