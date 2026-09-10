# W03 M14 IDECAMB coupled-quintessence execution control preregistration v0.1

Status: FROZEN BEFORE EXECUTION
Date: 2026-09-10

## Purpose
Establish that the pinned IDECAMB overlay has an executable *coupled quintessence* (CQ) path before any numerical K1/K2-K5 scientific promotion.

## Exact providers
- `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`
- overlay `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`

## Author configuration binding
Pinned `test_ide.ini` explicitly documents:
- `Class_IDE = 1`: coupled fluid model;
- `Class_IDE = 2`: coupled quintessence model;
- CQ controls `UForm_CQ`, `QForm_CQ`, `alpha_quint`, `beta_cq` are already present in the same author file.

The previously executed unmodified author input selected `Class_IDE=1` and therefore demonstrated runtime/provider infrastructure only, not M14 CQ family identity.

## Frozen transformation
Copy the pinned author `test_ide.ini` and change exactly the active line `Class_IDE = 1` to `Class_IDE = 2`. No likelihood, cosmological, CQ, numerical, prior, or output settings may be changed for this control.

## Compiler compatibility
Use the already independently established build-only compatibility flag `-fallow-argument-mismatch`; this is not a physics modification.

## Gate
PASS only if:
1. overlay/base SHAs are exact;
2. build succeeds;
3. execution exits 0;
4. preserved stdout/stderr identifies the run as coupled quintessence (or otherwise unambiguously confirms `Class_IDE=2` CQ path).

If build passes but CQ execution fails, classify the failure by preserved log as runtime/configuration/provider blocker. Do not infer physical failure of coupled quintessence.

## Scientific authority
This control can promote provider provenance/executable CQ scope only. It cannot promote K1-K9, B4-B9, observational novelty, or family sufficiency.

## Next authorized gate after PASS
Prospectively preregister a numerical K1 decoupling regression at `beta_cq=0` against the same scalar model with the interaction switched off, keeping the correct quintessence potential/initial-condition branch fixed and defining exact compared outputs/tolerances before execution.
