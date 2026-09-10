# M15 V2b perturbation-closure sensitivity preregistration

Date: 2026-09-10
Status: `FROZEN_BEFORE_V2B_IMPLEMENTATION`
Scientific scope: **independent KMDSB verification only; not author-code reproduction**

## 1. Authority and reason for this gate

Family: F15 / M15 generalized Chaplygin / unified dark fluid, decomposed into CDM plus vacuum-like DE for the `w_Lambda=-1` subcase.

Primary equations: R. F. vom Marttens et al., *Does a generalized Chaplygin gas correctly describe the cosmological dark sector?*, Physics of the Dark Universe 15 (2017) 114-124, arXiv:1702.00651, especially Eqs. (45)-(50).

Independent solver base remains pinned to:

`lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`

Gauge: Newtonian.

The exact finite-alpha background is already validated by V2a. The published perturbation system explicitly retains the DE comoving sound speed `c_s,Lambda^2` in Eqs. (45)-(46), while the accessible numerical section does not fix its value. Therefore an unqualified reconstruction of the unpublished author CLASS numerics is not authorized.

This gate asks a narrower and prospectively frozen question: **does the KMDSB response classification of the published perturbation closure depend materially on the otherwise undocumented sound-speed choice?**

## 2. Frozen closure subcases

Only two explicit sensitivity endpoints are authorized in V2b:

- `CS0`: `c_s,Lambda^2 = 0`;
- `CS1`: `c_s,Lambda^2 = 1`.

Neither endpoint may be described as the value used by the paper authors.

No fitting or threshold tuning may choose an intermediate `c_s,Lambda^2` after seeing the result. Intermediate values require a new preregistration.

## 3. Frozen model points

Reference point:

- `alpha = 0`.

Finite-alpha points for the first perturbation sensitivity pass:

- `alpha = -0.05`;
- `alpha = +0.05`.

These points are chosen before implementation because they bracket the near-LambdaCDM range emphasized by the source paper while preserving both transfer directions. Wider points such as +/-0.25 or -0.50 remain validation/diagnostic cases only until this gate is consumed.

Background constants and boundary conditions must be exactly those of the validated V2a branch. No background retuning is allowed between CS0 and CS1.

## 4. Frozen equation map

The implementation must use the already-bound conventions in `models/generalized_chaplygin/m15_v2_equation_to_class_map.md`:

- exact four-component background Eq. (16) and density reconstruction;
- paper-to-CLASS velocity map `theta_A = -k^2 vhat_A`;
- unchanged Newtonian `phi/psi` identification;
- literal published Eq. (49)-(50) expansion-scalar closure;
- CDM continuity and Euler source-term signs already frozen there.

The DE density contrast remains algebraically constrained by Eq. (49). `Qhat` must be obtained by substituting Eq. (49) into Eq. (45), as stated by the paper. `fhat` must follow Eq. (46). No textbook replacement for Eq. (50), no PPF substitution, and no silent geodesic/barotropic reinterpretation is permitted.

## 5. Mandatory structural checks before production

Before any finite-alpha spectra are scientifically consumed, the implementation must demonstrate:

1. **Reference identity:** at `alpha=0`, both CS0 and CS1 recover the same LambdaCDM reference products. Any finite sound-speed dependence at alpha=0 is an implementation failure.
2. **Background identity across closure:** for fixed finite alpha, CS0 and CS1 must have bitwise/numerically identical background histories, because this gate changes perturbation closure only.
3. **Finite values:** no NaN/Inf in background, scalar perturbation state, CMB spectra, transfer or linear matter spectrum over the frozen output ranges.
4. **Closure bookkeeping:** every interaction source added to the CDM perturbation equations must be paired with the corresponding DE source implied by Eqs. (45)-(48); undefined channels remain masked.
5. **No hidden retuning:** cosmological/background parameters, initial-condition prescription, output grids, precision settings and normalization must be identical between CS0 and CS1 at each alpha.

A failure of implementation/configuration is `BLOCKED_IMPLEMENTATION` or a more specific blocker, never a physical failure of M15.

## 6. Frozen output products

At minimum, each successful finite-alpha case must emit and archive:

- background table;
- TT, TE and EE spectra;
- linear matter `P(k)`;
- transfer functions containing the available density/velocity/metric channels used by the modified branch;
- run log and exact source diff relative to the pinned upstream CLASS commit.

If a physically required M15 channel is not available in the output schema, it is masked and recorded as unavailable; it must never be filled with zero.

## 7. Frozen numerical/reference thresholds

The alpha=0 differential control inherits the already validated V1 thresholds:

- background max symmetric relative difference <= `1e-8`;
- TT/TE/EE channel RMS symmetric relative difference <= `1e-5`;
- linear P(k) RMS symmetric relative difference <= `1e-5`;
- transfer RMS symmetric relative difference <= `1e-5` on common finite entries.

Finite-alpha CS0-vs-CS1 differences are **not** assigned a pass/fail amplitude threshold. They are the scientific quantity being measured, not a numerical-control tolerance.

## 8. Frozen sensitivity metrics

For each of `alpha=-0.05,+0.05`, compute on exact common masks/grids:

- background CS0-vs-CS1 max and RMS symmetric relative difference (expected numerical zero within the reference floor);
- TT, TE, EE RMS and max symmetric relative difference;
- linear P(k) RMS and max symmetric relative difference;
- transfer-channel RMS/max symmetric relative difference for every jointly defined finite channel;
- combined response-vector acute angle and best one-dimensional projection residual between the CS0 and CS1 alpha-response directions, reported in theory space only;
- singular values/rank of the two closure-conditioned response vectors, explicitly not equated with parameter count.

No theory-space angle may be promoted to observational discrimination.

## 9. Interpretation frozen before result

Possible classifications:

- `M15_V2B_CLOSURE_INSENSITIVE_WITH_SCOPE`: CS0 and CS1 yield numerically stable, effectively coincident multichannel response directions on the frozen finite-alpha points. This supports robustness to these endpoint closure choices but does not identify the authors' value.
- `M15_V2B_CLOSURE_RESPONSE_DISTINCT`: CS0 and CS1 produce numerically robust materially different response directions/channels. Then the sound-speed closure is a genuine response-family axis that must be retained in M15 K2/K5/K6 attacks; one endpoint cannot stand for the whole family.
- `M15_V2B_BLOCKED_IMPLEMENTATION`: the independent perturbation implementation cannot be validated under the frozen structural/reference gates.
- `M15_V2B_NONIDENTIFIABLE` is reserved for a later exact common observation-space/covariance result, not for small theory amplitudes.

No outcome of this V2b gate alone can falsify generalized Chaplygin/unified-dark-fluid physics, establish observational novelty, or close K6-K9.

## 10. K-gate promotion policy

If both endpoint implementations pass the structural/reference controls:

- K3 may advance from provenance-blocked only to a scoped **independent-reproduction closure** status; it may not be called exact author-code closure.
- K4 may be scored only after a separate finite-step/precision convergence test is frozen and passed.
- K5 may be opened only after K3 and K4 are sufficiently established.
- K6-K9 remain closed until their own prospectively frozen comparator/operator/holdout gates.

## Exact next gate

Implement the smallest source-complete V2b scaffold necessary to realize the published Eqs. (45)-(50) on top of the already validated V2a background, first run `alpha=0` for CS0 and CS1 against untouched pinned CLASS, and consume that reference artifact before opening the `alpha=+/-0.05` production sensitivity cases.
