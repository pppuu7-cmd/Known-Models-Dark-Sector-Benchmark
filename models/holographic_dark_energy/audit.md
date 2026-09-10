# M17 — Original event-horizon holographic dark energy (OHDE/HDE)

Status: ACTIVE — K0 scoped provenance established; K1 structural reference audit completed.

Date: 2026-09-10
Coverage family: F17
Wave: W03

## Scope
This record covers the original future-event-horizon holographic dark-energy mechanism of Miao Li (2004), not every model later called “holographic dark energy”.  Variants with a different infrared cutoff, action completion, interaction law, entropy prescription, or perturbation closure require separate subcases if they generate a response-distinct manifold.

Primary physical definition

\[
\rho_{\rm de}=3c^2 M_P^2 L^{-2},
\]

where `L` is the future event horizon.  For the original flat noninteracting model,

\[
w_{\rm de}=-\frac13-\frac{2}{3c}\sqrt{\Omega_{\rm de}},
\]

and the background evolution obeys the standard first-order OHDE evolution equation for `Omega_de`.

Primary literature authority: M. Li, *A Model of Holographic Dark Energy*, Phys. Lett. B 603 (2004) 1–5, arXiv:hep-th/0403127, DOI 10.1016/j.physletb.2004.10.014.

## K0 — provenance / model identity

Classification: `PASS_WITH_SCOPE`.

The model identity and its event-horizon IR cutoff are explicit in the primary literature.  This does **not** establish a perturbation-capable public solver implementation, and does not cover new-HDE/action variants.

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

But `Omega_de(a)` evolves.  A single constant `c` therefore cannot enforce `w=-1` over the complete history except at an isolated epoch.  In particular,

\[
\lim_{c\to\infty}w_{\rm de}=-\frac13,
\]

not `-1`.

Thus the original one-parameter OHDE family has **no native LambdaCDM reference/decoupling intersection obtained by a limit of `c`**.

K1 classification: `NO_NATIVE_LCDM_REFERENCE_INTERSECTION_WITH_SCOPE`.

This is **not** a physical falsification of HDE.  It means the benchmark must not fabricate a derivative `d r / d c` at LambdaCDM or silently retune a second function/parameter to manufacture a reference point.

## Consequence for K2–K9

1. No LambdaCDM tangent is authorized for the native `c` coordinate.
2. Finite-displacement HDE responses may still be compared to LambdaCDM or to smooth-DE manifolds, but must be labelled secant/global-manifold comparisons rather than local reference tangents.
3. K3–K5 require an explicit perturbation prescription/provider.  A background-only OHDE solver cannot close them.
4. K6 should attack the finite OHDE response against the full smooth-DE/CPL manifold on a matched domain.
5. K7 requires a common observation operator and covariance applied to both OHDE and comparators; fitting an effective `w0,wa` and reusing a CPL observable vector is not an exact HDE operator.

## Durable methodology lesson
A known family need not contain the benchmark reference as a parameter limit.  `NO_NATIVE_REFERENCE_INTERSECTION` is a legitimate structural outcome, distinct from `BLOCKED_IMPLEMENTATION`, `NONIDENTIFIABLE`, and physical `FAIL`.  Such families must be tested with finite/global response geometry rather than a fictitious local tangent at the reference origin.

## Next authorized gate
Find and pin a public, source-complete OHDE implementation with an explicit perturbation prescription (or preregister a verification implementation directly from published covariant/effective perturbation equations).  Before any K3/K5 promotion, freeze its stress-energy closure, gauge/frame convention, stability domain, and exact finite comparator points.  Do not use a background-only effective `w(a)` substitution as perturbation evidence.