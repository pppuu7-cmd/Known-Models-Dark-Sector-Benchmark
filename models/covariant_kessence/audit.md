# M11b — covariant k-essence validation audit

Status: **BLOCKED_IMPLEMENTATION_PROVENANCE**

This record covers only the attempted covariant validation of the M11 effective sound-speed response. It does not replace the successful M11 effective-fluid theory-response result and it does not physically falsify k-essence.

## Provider

Pinned external implementation:
`KunhaoZhong/CLASS_GSF@07e015246c4b40f4e22bb50c9a0a63a621bb61f7`.

The provider describes generalized/noncanonical scalar fields evolved with full perturbation equations. For `model_gsf == 6`, source inspection gives

\[
P(X,\phi)=X^{n+1}/A^n-V_0\phi^m,\qquad
n=(1-c_s^2)/(2c_s^2).
\]

Initial conditions are encoded as

\[
\phi_{ini}=p_1 10^{p_2},\qquad
\phi'_{ini}=p_3 10^{p_4}.
\]

## Evidence chain

### Probe 1 — model-6 preregistered grid

- binary build: PASS
- pure LCDM: PASS
- all model-6 GSF cases: FAIL during background shooting/evolution
- terminal machine classification: `M11B_BLOCKED_IMPLEMENTATION_PROBE_CASE_FAILURE`
- Actions run: `34429080377`

Logs localize the first common failure to NDF15/new-linearisation LU decomposition with `Possibly singular matrix!` during the shooting trial background integration.

### Probe 2 — kinetic-seed recovery

Preregistration:
`protocol/W03_M11B_KINETIC_SEED_RECOVERY_PREREGISTRATION_v0.1.md`.

The zero-kinetic start was a source-motivated candidate because model-6 derivatives contain powers such as `PXX ~ X^(n-1)`. A frozen ladder tested both signs at `|phi'_ini|={1e-20,1e-18,1e-17,1e-16}` for a reference-like `(m=0,cs2=1)` case and a noncanonical `(m=1,cs2=.90)` case.

Result:
`RECOVERY_NO_EXECUTABLE_REGION_IN_FROZEN_LADDER`.

All 16 GSF diagnostic cases returned exit 1 while LCDM returned exit 0.
Actions run: `34429876130`.

Therefore the original singularity cannot be attributed solely to the exact `X=0` start within the frozen recovery test.

### Provider-wide control

Preregistration:
`protocol/W03_M11B_CLASS_GSF_PROVIDER_CONTROL_PREREGISTRATION_v0.1.md`.

The provider's own committed `dgf.ini` was run unmodified after deleting pre-existing committed `output/dgf_*` products.

Result:
`PROVIDER_CONTROL_PASS`.

- build exit: 0
- DGF run exit: 0
- fresh `dgf_background.dat`: present
- fresh `dgf_pk.dat`: present
- Actions run: `34429997792`

This rejects a provider-wide build/runtime incompatibility in the GitHub-hosted environment.

## Provenance gap

The pinned repository contains a committed working model-1 DGF example, but repository search found no author-supplied `gsf_parameters = 6` working example. Consequently KMDSB does not possess a provider-validated model-6 operating point or a provider-authorized physical initial-state prescription for the requested covariant k-essence branch.

Further arbitrary tuning of initial conditions or shooting seeds after the failed frozen ladder would convert implementation recovery into post-hoc model construction. That is forbidden for this benchmark record.

## Gate classification

- K0/B0 provider identity: `PASS_WITH_SCOPE`
- K1/B1 covariant model-6 reference path: `BLOCKED_IMPLEMENTATION_PROVENANCE`
- K2/B3 physical/numerical operating domain: `BLOCKED_IMPLEMENTATION_PROVENANCE`
- K3–K9 / B2,B4–B9 covariant validation: `OPEN` / not authorized

M11 effective-fluid result remains separately valid in its stated scope: the local sound-speed response survives the same-anchor CPL theory-manifold attack but has weak amplitude/rank. It is **not promoted to generic covariant k-essence**.

## Next permitted action

Search for an independent, public, pinned covariant `P(phi,X)` implementation with:
1. an author-supplied executable example or regression target;
2. explicit action/equations and initial-state prescription;
3. recoverable reference/decoupling limit;
4. perturbation evolution sufficient for the M11 response channels.

If no such implementation is found in the coverage cycle, retain M11b as `BLOCKED_IMPLEMENTATION_PROVENANCE` and continue the census. Do not remove the k-essence family and do not call it falsified.
