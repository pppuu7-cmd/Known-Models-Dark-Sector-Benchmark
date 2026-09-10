# M17 HDE/ePPF frontier recovery delta — 2026-09-10

Repository evidence overrides chat memory.

## What changed

The prior statement that M17 lacked a public perturbation-capable provider is no longer the best available evidence.

A pinned public candidate has been identified:

- base `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`
- overlay `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`

The 2025 EPJC paper *Revisiting holographic dark energy after DESI 2024* explicitly applies ePPF to HDE/IHDE perturbations and identifies IDECAMB as the modified CAMB implementation. The original IDECAMB paper is Y.-H. Li and X. Zhang, JCAP 09 (2023) 046, arXiv:2306.01593.

## Source-binding audit

Actions run `34496402502` built the exact pinned overlay successfully. Before any physics case was executed, its frozen source-binding audit returned TRUE for all 9 checks:

- HDE enum/selector present;
- `c_hde` mapped into provider HDE parameter;
- original-HDE EoS branch present;
- HDE perturbations enabled;
- PPF/ePPF Gamma state evolved;
- DE density perturbation reconstructed;
- DE momentum perturbation reconstructed;
- reconstructed DE perturbations fed back into total source terms;
- coupled-fluid branch defaults to PPF and the test ini exposes the HDE selector.

This is strong evidence for a source-complete **effective ePPF perturbation prescription**, not a proof that the future-event-horizon perturbation closure is uniquely derived from Li-2004.

Allowed K3 label after executable provider control: `PASS_WITH_SCOPE_EPPF_PRESCRIPTION` only.

## First provider-control attempt

Run `34496402502` stopped at ini preparation because the harness required exactly one occurrence of the text `WForm_CF = 1`, while the pinned author's ini contains it both in a comment and on the active configuration line. Build and all source checks had already passed. No HDE physics case executed.

Classification: `INFRASTRUCTURE_HARNESS_ONLY`; no model/provider physical interpretation.

Immutable artifact from failed harness attempt: `10159998668`.

## Recovery attempt

The repair changes only selector targeting: it now replaces the exact active line `\nWForm_CF = 1\n`. Physics cases, commits, ePPF setting and thresholds are unchanged.

Recovery workflow: `.github/workflows/w03-m17-idecamb-eppf-provider-control-r1.yml`.
Recovery run: `34496665472`.

At this handoff the recovery run has:

- build: PASS;
- source audit + case preparation: PASS;
- frozen finite HDE/ePPF execution grid: IN PROGRESS.

Frozen cases are `c={0.6,0.8,1.0,1.2}`, `beta_cf=0`, `Use_PPF=T`, plus a repeated `c=0.8` determinism control. There is no authorized LambdaCDM-origin local c-tangent because M17 has no native LambdaCDM reference intersection.

## Background result retained

The already terminal finite-background result is unchanged: the fitted CPL manifold absorbs about 96.7–98.9% of the tested OHDE background response at `c={0.6,0.8,1.0,1.2}`. This is a background-only result and must not be used as perturbation-level equivalence.

## Next authorized action

Consume run `34496665472` when terminal. If it returns `M17_IDECAMB_EPPF_PROVIDER_EXECUTABLE_WITH_SCOPE`, promote only K3 to `PASS_WITH_SCOPE_EPPF_PRESCRIPTION`; K4 remains open except for the frozen same-input repeatability check. Then preregister a dedicated finite-point solver-precision K4 gate and a perturbation-level HDE-vs-CPL attack. If the run blocks, classify the exact infrastructure/provider failure without physical falsification.
