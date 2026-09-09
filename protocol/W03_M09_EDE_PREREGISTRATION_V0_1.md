# W03 / M09 — solver-native Early Dark Energy preregistration v0.1

Frozen: 2026-09-10

## Authority and implementation
- DSIR observation-methodology overlay: `pppuu7-cmd/Dark-Sector-Influence-Reconstruction@bc28acc47cc5facba046741fd09f710ae8da9689`.
- The only delta from the prior M07/M08 overlay `864952e...` is DSIR4 angular-materialization/authority-succession work; no M07/M08 historical result is rebased.
- Solver: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.
- Solver branch: `fluid_equation_of_state = EDE`.

Pinned CLASS implements the EDE fluid through `Omega_EDE`, `w0_fld`, and `cs2_fld`; the background code constructs `Omega_ede(a)` and then `w_ede(a)`, with an equality term because the branch tracks radiation and then matter at early times.

## Scientific role
M09 is the first W03 attack deliberately chosen to probe a direction that the late-time M07/M08 ShapeFit control did not use: an early-time / scale-dependent matter-transfer imprint.

The question is not whether EDE is generally viable. The preregistered question is:

> Does a solver-native EDE deformation generate a stable response component in an amplitude-quotiented broad-k shape block that cannot be represented as only late-time smooth-DE amplitude/history variation?

## Frozen branch
The first M09 branch is one-dimensional:
- `w0_fld = -1` fixed;
- `cs2_fld = 1` fixed;
- `use_ppf = yes` fixed;
- physical coordinate `e = Omega_EDE`;
- physical local domain `e >= 0`.

No negative-`Omega_EDE` probe is allowed. Local derivatives are one-sided rays.

Reference candidates are kept distinct:
1. pure LambdaCDM solver reference: `Omega_fld=0`, Lambda inferred by closure;
2. internal EDE zero point: `fluid_equation_of_state=EDE`, `Omega_EDE=0`, `w0_fld=-1`, `Omega_Lambda=0`, fluid density inferred by closure.

The EDE-zero point is not assumed to equal pure LambdaCDM before numerical regression.

## Frozen probes
`e = {0, 1e-4, 3e-4, 1e-3, 3e-3}`.

The two smallest positive points are the local-tangent convergence pair. The larger points are descriptive finite-deformation checks only and are not B8 evidence.

## Frozen response blocks
### L — standard late-time DSIR block
- `ln H(z)` on z `{0.295,0.51,0.706,0.934,1.317,1.491,2.33}`;
- `ln P(k,z)` on the same seven z nodes and k `{0.001,0.003,0.01,0.03,0.1} h/Mpc`.

### S — amplitude-quotiented broad-k shape block
At `z=0.51`, interpolate linear matter power on
`k={0.001,0.003,0.006,0.01,0.02,0.03,0.05,0.08,0.1,0.2,0.3,0.5,0.8,1.0} h/Mpc`.

For a model/reference ratio `r(k)=ln[P_model(k)/P_ref(k)]`, define

`s(k)=r(k)-mean[r(0.001),r(0.003)]`.

This quotients a common low-k amplitude and retains scale-dependent shape/transfer information. It is a theory-response block, not yet an observational likelihood coordinate.

## Preregistered controls
### C-M09-1 — EDE-zero bridge
Report pure-Lambda versus EDE-zero mismatch separately. Promotion to a common Lambda tangent is allowed only if
- `max |ln H_EDE0/H_LCDM| <= 1e-6`, and
- `max |ln P_EDE0/P_LCDM| <= 1e-6`
on the frozen L block.

If this fails, B1 remains PARTIAL and the internal EDE branch may still be studied relative to its own zero point, but no exact Lambda-intersection claim is allowed.

### C-M09-2 — one-sided tangent convergence
For `e1=1e-4`, `e2=3e-4`, compare `r/e` separately in L-P, L-H and S.
A local direction is `PASS_WITH_SCOPE` only if for every non-negligible claimed block:
- relative L2 difference <= 0.05;
- angle <= 2 deg.

A near-zero block may be classified `NEAR_NULL` rather than forced through an angle gate.

### C-M09-3 — no hidden shape zero
The S block must be computed from the actual CLASS P(k) outputs. It may not be set to zero because previous M07/M08 ShapeFit controls assumed no early-shape coordinate.

## Initial B0-B9 ledger
- B0 `PASS_WITH_SCOPE` — exact pinned solver branch/provenance frozen.
- B1 `PARTIAL` — Lambda intersection awaits EDE-zero regression.
- B2 `PARTIAL` — fluid/PPF implementation pinned; promoted gauge/frame residual claims not yet audited.
- B3 `OPEN` — one-sided physical ray and numerical convergence pending.
- B4 `OPEN` — L and S responses pending.
- B5 `OPEN` — no observation-space promotion from S yet.
- B6 `OPEN` — M08 CPL is the primary smooth-DE comparator after M09 local control.
- B7 `OPEN`.
- B8 `OPEN` — all current finite points are implementation/local-geometry probes.
- B9 `PARTIAL` — scientific role is preregistered.

## Anti-overclaim
- This is the CLASS solver-native EDE fluid parameterization, not every model called early dark energy in the literature.
- A nonzero S response is not automatically observable or uniquely EDE.
- A successful Lambda bridge does not establish physical viability of finite EDE amplitudes.
- A failure of the bridge is bookkeeping/reference information, not proof that EDE is false.
- No finite point in this first grid is a prospective holdout.
