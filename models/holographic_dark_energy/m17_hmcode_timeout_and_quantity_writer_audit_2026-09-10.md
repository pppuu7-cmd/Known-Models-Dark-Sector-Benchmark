# M17 original HDE — HMCode timeout / `.quantity` writer root-cause audit

Updated: 2026-09-10
Status: `RECOVERY_ROUTE_IDENTIFIED_LINEAR_CONTROL_REQUIRED`
Provider: `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075` over `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`
Physical falsification: **NO**

## 1. Why this audit was reopened

The first repaired M17 HDE/ePPF provider-control route was classified `M17_IDECAMB_EPPF_BLOCKED_EXECUTION` after long runtimes, no `.theory_cl`, and NaNs in some `.quantity` columns. A dedicated c=0.8 smoke run also ended after about 700 wall seconds with shell exit 0 and the message:

`STOP SIGINT1: Integration timed out`.

The initial bookkeeping correctly avoided calling this a physical HDE failure, but the specific interpretation "invalid perturbation outputs" was too strong. Two source/log facts now separate the failure modes.

## 2. The timeout is HMCode/nonlinear-lensing linked

The c=0.8 smoke runtime log reports:

- `Doing non-linear Pk: F`
- `Doing CMB lensing: T`
- `Doing non-linear lensing: T`

and terminates internally around 700 s, before the external 900 s watchdog, with `Integration timed out`.

Independent CosmoMC/CAMB reports identify the same diagnostic string as:

`HMCode INTEGRATE, Integration timed out`.

The pinned parent `batch3/common.ini` explicitly sets:

`use_nonlinear_lensing = T`

while retaining `CMB_lensing = T`.

Therefore the failed smoke did **not** isolate linear HDE/ePPF execution from HMCode. A dedicated `use_nonlinear_lensing=F` control is required before calling the provider's linear perturbation route blocked.

This recovery changes no HDE equation, ePPF prescription, parameter or background law. It removes a nonlinear post-processing component that is unnecessary for the K3 linear-provider execution gate.

## 3. The NaN `.quantity` columns are not HDE perturbation variables

At the pinned IDECAMB source, `SetIDE` writes eleven test columns:

`a, z, grhov_t, grhoc_t, adotoa, wde, gQ, gphi, gphidot, gU, dgU`.

For every row it first calls the coupled-fluid `IDEout(...)`, but then **unconditionally** calls:

`Get_gphi_gphidot(a,gphi,gphidot)`

`Potential(gphi,0)`

`Potential(gphi,1)`.

Those latter functions belong to `CoupledQuintModels`, not the coupled-fluid HDE branch. In HDE mode (`IDE_Class=CoupFluid`, `WForm=HDE`) their CQ iteration/background arrays are not the HDE state being evolved.

Consequently columns 8–11 are CQ-only test-writer fields and are not valid HDE perturbation diagnostics. Their NaNs in the M17 smoke must not be interpreted as NaN HDE perturbations.

The HDE-relevant test-writer subset is columns 1–7:

- scale factor;
- redshift;
- DE background density variable;
- CDM background density variable;
- conformal Hubble rate;
- HDE equation of state;
- interaction `gQ` (zero in the uncoupled M17 control).

These columns were finite in the prior smoke.

## 4. Corrected interpretation of prior evidence

Retain from the prior result:

- source binding to original future-event-horizon HDE/ePPF is scoped and valid;
- build succeeded;
- the full default theory-output route did not produce `.theory_cl` because execution terminated in an integration timeout;
- no physical HDE falsification occurred.

Retract as unsupported:

- treating NaNs in `.quantity` columns 8–11 as invalid HDE perturbation products;
- inferring that the timeout necessarily occurred in HDE/ePPF perturbation evolution.

Updated provisional classification before recovery execution:

`M17_DEFAULT_ROUTE_BLOCKED_HMCODE_LINEAR_EPPF_CONTROL_OPEN`.

This is an audit diagnosis, not yet a matrix promotion.

## 5. Authorized next test

Run the exact same HDE/ePPF c=0.8, beta=0 provider with:

`use_nonlinear_lensing = F`

while keeping linear `CMB_lensing = T` and the existing theory-output route. Require a finite `.theory_cl` and finite HDE `.quantity` columns 1–7. Ignore CQ-only columns 8–11 for HDE pass/fail, but archive them unchanged.

Only a preregistered linear-control PASS may reopen K3 promotion as `PASS_WITH_SCOPE_EPPF_PRESCRIPTION`. It will still not establish a unique perturbation theory of the nonlocal future event horizon; it validates only the provider's effective ePPF prescription.
