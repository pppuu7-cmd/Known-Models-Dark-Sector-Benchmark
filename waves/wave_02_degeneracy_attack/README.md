# Wave 02 — Same-observable degeneracy attack

Status: **ACTIVE**  
Opened: 2026-09-08  
Protocol: `protocol/WAVE_TESTING_PROTOCOL_v0.1.md`  
Starting DSIR authority: `e3276e2193f6a5200b541a194e3175356ae5a1c1`

## Scientific question

Given that Wave 01 proved no single response block is universally sufficient, which apparently similar known-model responses remain distinguishable when each unresolved pair is tested on the **smallest valid common multi-channel block**?

The objective is not to maximize the number of separations. The objective is to determine whether a claimed degeneracy is:

- genuine in the identifiable common subspace;
- an artifact of looking at one channel;
- caused by a missing response cell / incompatible block;
- observationally unresolved after whitening;
- or simply not yet testable with pinned provenance.

## Positive-control edge

### W02-PC1 — M03 GDM vs M05 designer f(R)

Wave 01 already contains a hard theory-response separator:
- scale-mode angles near zero (`0.07813–0.10169 deg`);
- time-mode angles about `25 deg`;
- full oriented ray angles about `154.5–154.8 deg`.

Wave 02 must reproduce the semantic result that **scale-only mimicry != full-response equivalence**. This positive control calibrates the pairwise edge machinery.

## Primary unresolved edges

### W02-E1 — M02 IDE vs M03 GDM
Required common information:
- admissible IDE tangent-cone direction(s);
- GDM local direction(s);
- common low-k structure block;
- metric/slip block if available for both;
- covariance/operator projection before observational claims.

Initial status: `OPEN`.

### W02-E2 — M02 IDE vs M05 designer f(R)
Required common information:
- structure + time evolution on common k,z nodes;
- slip/metric response where implementation allows;
- preservation of IDE physical-domain mask and f(R) near-GR solver threshold.

Initial status: `OPEN`.

### W02-E3 — M04 WDM vs alternative small-scale suppression mechanisms
A comparator must be pinned before testing. Candidate mechanisms may include other dark-matter cutoff/suppression families, but KMDSB will not select a winner by convenience; implementation/provenance and valid high-k overlap are prerequisites.

Initial status: `BLOCKED_IMPLEMENTATION` until at least one alternative suppression model is pinned into the KMDSB/DSIR response conventions.

### W02-E4 — M06 DCDM vs alternative temporal/interaction histories
Need a common temporal-localization observable that can be evaluated without redefining the coordinate per model.

Initial status: `OPEN`.

## Frozen Wave-02 hypotheses

### W02-H1 — restricted-block degeneracy is not equivalence
At least one pair with a very small angle/distance in one block will remain clearly separated in a second valid block.

Positive-control expectation: PASS from M03/M05; new unresolved pairs must be tested independently.

### W02-H2 — missing common channels create legitimate BLOCKED edges
At least one unresolved pair will remain unscored until a common response block is computed. `BLOCKED_*` is a valid scientific result and must not be zero-filled.

### W02-H3 — minimum discriminating suite is a graph problem
The required observable set depends on which comparator edge is being broken; there is no presumption that one universal scalar discriminator exists.

### W02-H4 — observation-space promotion is separate
A hard theory-response edge is promoted to observational discrimination only after a pinned response operator/covariance and consistent whitening.

## Exit criteria

Wave 02 is complete when:
1. W02-PC1 semantic positive control is encoded/reproduced;
2. E1–E4 each receive a defensible hard state (`PASS_WITH_SCOPE`, `NONIDENTIFIABLE`, `BLOCKED_*`, `INCONCLUSIVE`, etc.);
3. the minimum observed channel set for every scored edge is recorded;
4. no missing channel is zero-imputed;
5. theory-space and observation-space edge graphs are reported separately.

## Immediate next computation

**W02-E1 IDE vs GDM common-block audit.** First determine whether the frozen DSIR repository contains a common pinned response product beyond low-k matter/growth for both C2 and C3. If not, freeze the missing-channel specification required for a new hard run rather than inferring the edge from unrelated angles.
