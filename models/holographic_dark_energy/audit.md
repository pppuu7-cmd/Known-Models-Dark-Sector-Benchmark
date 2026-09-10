# M17 — Original event-horizon holographic dark energy (OHDE/HDE)

Status: ACTIVE — K0 scoped provenance established; K1 structural reference audit completed; finite-background CPL attack terminal; ePPF perturbation-provider gate launched.

Date: 2026-09-10
Coverage family: F17
Wave: W03

## Scope
This record covers the original future-event-horizon holographic dark-energy mechanism of Miao Li (2004), not every model later called “holographic dark energy”. Variants with a different infrared cutoff, action completion, interaction law, entropy prescription, or perturbation closure require separate subcases if they generate a response-distinct manifold.

Primary physical definition

\[
\rho_{\rm de}=3c^2 M_P^2 L^{-2},
\]

where `L` is the future event horizon. For the original flat noninteracting model,

\[
w_{\rm de}=-\frac13-\frac{2}{3c}\sqrt{\Omega_{\rm de}},
\]

and the background evolution obeys the standard first-order OHDE evolution equation for `Omega_de`.

Primary literature authority: M. Li, *A Model of Holographic Dark Energy*, Phys. Lett. B 603 (2004) 1–5, arXiv:hep-th/0403127, DOI 10.1016/j.physletb.2004.10.014.

## K0 — provenance / model identity

Classification: `PASS_WITH_SCOPE`.

The model identity and its event-horizon IR cutoff are explicit in the primary literature. This alone does not establish a unique perturbation closure and does not cover new-HDE/action variants.

## K1 — reference/decoupling geometry

### Prospectively tested question
Does the native OHDE parameter `c` provide a physical path whose full background equation of state approaches a cosmological constant, `w=-1`, so that a local DSIR tangent at a LambdaCDM intersection can be defined by varying `c` alone?

### Structural result
Using

\[
w_{\rm de}=-\frac13-\frac{2\sqrt{\Omega_{\rm de}}}{3c},
\]

a Lambda-like value at one epoch requires

\[
c=\sqrt{\Omega_{\rm de}(a)}.
\]

But `Omega_de(a)` evolves. A single constant `c` therefore cannot enforce `w=-1` over the complete history except at an isolated epoch. In particular,

\[
\lim_{c\to\infty}w_{\rm de}=-\frac13,
\]

not `-1`.

Thus the original one-parameter OHDE family has **no native LambdaCDM reference/decoupling intersection obtained by a limit of `c`**.

K1 classification: `NO_NATIVE_LCDM_REFERENCE_INTERSECTION_WITH_SCOPE`.

This is **not** a physical falsification of HDE. It means the benchmark must not fabricate a derivative `d r / d c` at LambdaCDM or silently retune a second function/parameter to manufacture a reference point.

## Finite-background CPL manifold attack

Machine result: `waves/wave_03_expanded_dark_energy/M17_HDE_BACKGROUND_CPL_RESULT.json`.

Frozen finite HDE points `c={0.6,0.8,1.0,1.2}` were compared on the matched background node set to a fitted two-parameter CPL manifold. The terminal residual fractions were:

- `c=0.6`: `0.0256422409`
- `c=0.8`: `0.0329380808`
- `c=1.0`: `0.0165303569`
- `c=1.2`: `0.0111160299`

Thus CPL absorbs about `96.7%–98.9%` of the tested finite HDE **background** response. Classification: `BACKGROUND_ABSORBED_BY_CPL_WITH_SCOPE` at all four frozen points.

This result is deliberately narrow. It does not establish perturbation-level equivalence, an exact HDE observation operator, or absence of response-distinct structure once perturbations are included.

## K3 perturbation-provider reopening — IDECAMB/ePPF

The earlier provider search is superseded by a stronger public candidate.

Pinned candidate:

- `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`
- layered on `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`

The pinned source contains all of the following bindings:

1. coupled-fluid selector with `HDE=2`;
2. native `c_hde` parameter mapped into `CFP%c`;
3. HDE EoS branch equivalent to `w=-1/3-2 sqrt(Omega_de)/(3c)`;
4. HDE marked as perturbative (`perturDE=.true.`);
5. PPF/ePPF state `Gamma` is evolved when `Use_PPF=T`;
6. reconstructed dark-energy density and momentum perturbations are fed back into total Einstein-Boltzmann source terms;
7. coupled-fluid models default to `Use_PPF=T` unless explicitly overridden.

Independent literature corroboration: T.-N. Li et al., *Revisiting holographic dark energy after DESI 2024*, Eur. Phys. J. C 85, 608 (2025), DOI `10.1140/epjc/s10052-025-14279-7`, explicitly states that ePPF is applied to HDE/IHDE perturbations and identifies `https://github.com/liaocrane/IDECAMB/` as the modified CAMB implementation.

### Scope boundary

This evidence supports a serious source-complete **effective ePPF completion** of original-HDE background evolution. It does **not** demonstrate that the nonlocal future-event-horizon perturbation is uniquely derived from the Li-2004 definition. Therefore the strongest allowed K3 label after successful execution is:

`PASS_WITH_SCOPE_EPPF_PRESCRIPTION`.

It must not be shortened to an unqualified `PASS` for every possible HDE perturbation closure.

Preregistration: `protocol/W03_M17_IDECAMB_EPPF_PROVIDER_PREREGISTRATION_v0.1.md`.
Provider-control workflow: `.github/workflows/w03-m17-idecamb-eppf-provider-control.yml`.

## Consequence for K2–K9

1. No LambdaCDM tangent is authorized for the native `c` coordinate.
2. Finite-displacement HDE responses may be compared to LambdaCDM or smooth-DE manifolds, but must be labelled secant/global-manifold comparisons rather than local reference tangents.
3. If the IDECAMB/ePPF provider gate passes, K3 can be promoted only with the explicit ePPF scope above.
4. K4 still requires a dedicated finite-point numerical stability/convergence gate; the provider workflow's repeated `c=0.8` case is only a narrow determinism control.
5. K5 cannot be interpreted as a LambdaCDM-origin local tangent rank test in native `c`; a finite/global multichannel construction is required.
6. K6 background-only CPL absorption is already established but does not settle perturbation-level absorption.
7. K7 requires a common observation operator and covariance applied to exact HDE/ePPF and comparator outputs.

## Durable methodology lessons

A known family need not contain the benchmark reference as a parameter limit. `NO_NATIVE_REFERENCE_INTERSECTION` is a legitimate structural outcome, distinct from `BLOCKED_IMPLEMENTATION`, `NONIDENTIFIABLE`, and physical `FAIL`. Such families must be tested with finite/global response geometry rather than a fictitious local tangent at the reference origin.

A second lesson is now added: a perturbation prescription can make a background-defined family computationally testable without becoming uniquely implied by the original model definition. DSIR must preserve this distinction through a scoped K3 label rather than silently identifying an effective closure with the underlying nonlocal model.

## Next authorized gate

Consume the preregistered IDECAMB/ePPF provider-control result. If executable and deterministic on the frozen finite HDE grid, promote K3 to `PASS_WITH_SCOPE_EPPF_PRESCRIPTION`, then run a dedicated K4 finite-point precision/restart/convergence test and a perturbation-level HDE-vs-CPL response attack. No physical falsification or observational novelty claim is authorized before those gates.