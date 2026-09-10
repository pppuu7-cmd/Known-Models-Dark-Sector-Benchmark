# W03 M14 IDECAMB K4/K5 right-sided local response — preregistration v0.1

Frozen: 2026-09-10

## Preconditions

- K0 provider provenance/execution: passed with scope.
- K1 exact interaction-off invariants: `M14_IDECAMB_K1_DECOUPLING_PASS_WITH_SCOPE`.
- K2: `q_beta=beta_cq>=0` one-sided provider-supported tangent cone; negative beta is outside current scope.
- K3 source audit: active background and perturbation coupling objects are implemented in IDECAMB; numerical closure remains scoped.

## Provider and anchor

Pinned overlay remains:
- `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`
- `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`

Fixed scalar/cosmology anchor: exact author-center coupled-quintessence theory configuration with `alpha_quint=0.02`, `Class_IDE=2`, `UForm_CQ=1`, `QForm_CQ=1`, and the previously validated theory-only output route.

Prospective beta grid:
- reference `beta=0`;
- fine step `h=0.005`;
- coarse step `2h=0.010`.

No negative beta case is run.

## Frozen response vector

All comparisons are on identical source-emitted grids. Undefined/non-finite coordinates are masked and cause failure if a required channel loses all support; they are never zero-imputed.

From `.quantity` columns `a,z,rho_de_a2,rho_c_a2,Hconf,wde,gQ,phi,phi_prime,U,dU` use:

1. `dln_rho_de = ln(rho_de(beta)/rho_de(0))` where both are positive;
2. `dln_rho_c = ln(rho_c(beta)/rho_c(0))` where both are positive;
3. `dln_H = ln(H(beta)/H(0))` where both are positive;
4. `dw = wde(beta)-wde(0)`;
5. dimensionless interaction `qhat = gQ(beta) / (abs(H(beta))*(abs(rho_de(beta))+abs(rho_c(beta))) + tiny)`; reference qhat is zero.

From `.theory_cl`, require identical multipole column and use positive channels only:

6. `dln_TT`;
7. `dln_EE`;
8. `dln_PP`.

TE is excluded prospectively because it changes sign; BB is excluded because its very small amplitude makes serialization-relative metrics unnecessarily fragile. This is a theory-response gate, not an observational covariance claim.

Concatenate these dimensionless channels in the frozen order above. The right tangent estimates are `t_h=r(h)/h` and `t_2h=r(2h)/(2h)`.

## K4 convergence thresholds

Reuse the established KMDSB local-tangent gates; do not tune them after result:

- relative norm mismatch `abs(||t_h||-||t_2h||)/max(||t_h||,||t_2h||) <= 0.10`;
- direction angle `acos[(t_h dot t_2h)/(||t_h||||t_2h||)] <= 3 deg`.

All three runs must exit 0 and emit finite required outputs.

PASS requires both thresholds. A failure is `FAIL_LOCAL_CONVERGENCE` for this grid/provider, not physical falsification of coupled quintessence.

## K5 non-null / rank scope

K5 is scored only if K4 passes.

Serialization of the author diagnostics is approximately five significant digits. Require at the fine step at least one frozen response coordinate with `abs(r_h) >= 5e-5` to classify the beta axis as numerically non-null above the serialized output floor. Report per-channel norms and maxima.

Because this gate varies exactly one physical tangent coordinate, it may establish at most `identified_local_rank=1`; parameter count is not used as evidence for rank.

K5 outcome:
- `PASS_WITH_SCOPE_RANK1` if K4 passes and response is non-null;
- `NONIDENTIFIABLE_AT_OUTPUT_FLOOR` if K4 passes but no coordinate reaches the frozen floor;
- `BLOCKED_BY_K4` if K4 fails.

## Next if K4/K5 pass

Do not claim novelty. Preregister K6 nearest-family manifold attacks against the earlier phenomenological IDE M02 response family and smooth scalar/late-DE comparators in a common response space. K7 observational projection/covariance remains separate.
