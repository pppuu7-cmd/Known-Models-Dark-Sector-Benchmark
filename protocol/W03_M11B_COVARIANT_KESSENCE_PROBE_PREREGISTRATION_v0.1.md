# W03 M11b covariant k-essence validation probe v0.1

Frozen: 2026-09-10
Status: PREREGISTERED BEFORE OUTPUT
Coverage family: F11 / M11b subcase
Parent evidence: M11 effective sound-speed representative + full CPL attack

## Scientific question

M11's effective-fluid sound-speed direction survived the same-anchor local CPL manifold, but with very small absolute response norm. Before promoting that direction to a k-essence-family property, test whether a genuinely covariant generalized scalar field with explicit `P(phi,X)` produces a controlled, stable sound-speed response in the same low-k P+H coordinates.

A successful probe is not yet observational novelty and is not automatically equivalence to the effective-fluid M11 direction. It only establishes that a covariant kinetic implementation can support the required branch and is ready for a stricter matched-production comparison.

## Pinned independent implementation

Solver: `KunhaoZhong/CLASS_GSF@07e015246c4b40f4e22bb50c9a0a63a621bb61f7`.

Use solver-native generalized-scalar model `model_gsf=6` from `source/background.c`:

`P(X,phi) = X^(n+1)/A^n - V0*phi^m`

`n = (1-c_s^2)/(2 c_s^2)`.

The same source computes

`c_s^2 = P_X/(P_X + 2 X P_XX)`

and exposes the kinetic coefficient

`A_gsf = P_X + 2 X P_XX`.

These source equations, not stale explanatory comments, define the frozen implementation semantics.

## Parameter bookkeeping

CLASS_GSF uses the model-specific array layout implemented in the pinned source:

`gsf_parameters = [model, phi_coeff, phi_exp, phip_coeff, phip_exp, A, V0, m, cs2]`.

Freeze:
- `model=6`;
- initial field encoding `phi=1*10^0`, `phi'=0*10^0`;
- `A=1`;
- `V0` is closure/shooting nuisance, never the physical sound-speed coordinate;
- `gsf_tuning_index=6` so the solver adjusts `V0` to close the requested present-day generalized-scalar density;
- `Omega_Lambda=0`, `Omega_fld=0`, `Omega_gsf=-1` so GSF fills the remaining flat budget;
- `attractor_ic_gsf=no`;
- physical response coordinates are `m` and `q_s=1-c_s^2`.

If the source/configuration proves that this bookkeeping interpretation is invalid, classify a probe implementation blocker; do not silently alter parameter meaning after seeing output.

## Common cosmology and response grid

- `h=0.67`
- `omega_b=0.0224`
- `omega_cdm=0.1200`
- flat
- synchronous gauge
- linear mPk
- no reionization
- z `{0.295,0.51,0.706,0.934,1.317,1.491,2.33}`
- k `{0.001,0.003,0.01,0.03,0.1} h/Mpc`
- background output enabled.

The probe records P, H, `w_gsf`, `cs2_gsf` and `A_gsf` where available.

## Reference branch

Reference GSF control:
- `m=0`
- `c_s^2=1`
- zero initial field velocity.

Then `n=0` and the Lagrangian reduces to `P=X-V0`; at zero field velocity and constant potential this should reproduce a cosmological-constant stress under matched closure.

Compare this GSF control to pure LambdaCDM.

Frozen reference gates:
- `max |ln P_GSF/P_LCDM| <= 1e-5`
- `max |ln H_GSF/H_LCDM| <= 1e-7`.

Failure is a reference/configuration result for this implementation, not a falsification of k-essence.

## Prospective anchor scan

Because the covariant scalar background is not identical to the effective fluid `w=-0.95` anchor, the first run is an implementation/geometry probe.

Before output, freeze candidate potential powers:

`m in {0.5, 1, 2, 4}`

and for each m run

`c_s^2 in {1.00, 0.95, 0.90}`.

For each `c_s^2=1` candidate, define a usable anchor only if:
1. solver exits successfully;
2. all sampled `A_gsf` values are finite and strictly positive;
3. all sampled `c_s^2_gsf` values are finite and positive;
4. present-day/lowest-z `w_gsf` lies in `[-0.99,-0.80]`.

Among usable anchors choose the m that minimizes `|w_gsf(z~0)+0.95|`; ties go to the smaller m. This selection rule is frozen before output.

If no usable anchor exists, classification is `M11B_NO_USABLE_COVARIANT_ANCHOR_WITH_SCOPE` and no parameter fishing is allowed in the same probe.

## Sound-speed direction and stability

At the selected m, define

`q_s = 1-c_s^2 >= 0`

with steps `.05` and `.10`.

Relative to the selected `c_s^2=1` anchor:

`J_s(.05)=r(c_s^2=.95)/.05`

`J_s(.10)=r(c_s^2=.90)/.10`.

Probe convergence gates:
- relative vector difference <= 0.25;
- acute direction change <= 5 deg;
- low-k P component non-null: `||J_s^P|| > 1e-8`.

The looser probe threshold is intentional because this is an independent legacy solver implementation. Passing it only authorizes a later tighter production run; it does not close K4.

## Stability diagnostics

For the selected branch report at minimum:
- minimum sampled `A_gsf`;
- minimum/max sampled `c_s^2_gsf`;
- present-day/lowest-z `w_gsf`;
- solver exit status for every preregistered case.

`A_gsf<=0`, `c_s^2<=0`, NaN/Inf or solver failure must be classified explicitly. A physically unstable sampled branch is not converted into a numerical pass.

## Diagnostic comparison to effective M11

Compare the covariant `J_s(.05)` direction to the stored M11 effective-fluid sound-speed direction on the same 35 P + 7 H coordinates.

This angle/residual is **diagnostic only** because the covariant anchor background may not exactly match the fluid `w=-0.95` anchor. It cannot by itself establish family equivalence or separation.

## Probe classification

`PROBE_PASS_READY_FOR_MATCHED_PRODUCTION` requires:
- reference regression passes;
- at least one usable anchor exists;
- selected branch stability diagnostics pass;
- q_s response is non-null;
- q_s step convergence passes.

Otherwise store the most specific blocker/failure scope, preserving configuration failure, physical instability and non-convergence as distinct outcomes.

No K7/K8 observational claim is permitted from this probe.
