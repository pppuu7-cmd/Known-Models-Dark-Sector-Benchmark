# W04 M21 conditional direct CMB-source branch-signature audit v0.1

Frozen: 2026-09-14 while `W04 M21 perturbation-state branch signature v0.1` run `34895647832` is non-terminal. No perturbation-state result from that run is used in this protocol.

Infrastructure amendment frozen while `W04 M21 perturbation-state seam recovery v0.1` run `34896737054` is still queued/non-terminal: the original parent subsequently terminalized BLOCKED solely on native duplicate `(tau,a)` approximation-switch seams. Therefore a terminal seam-recovery result may act as the parent authority **only if** it has `seam_recovery_passed=true`, `cross_lane_input_identity=true`, and classification exactly `M21_CMB_BRANCH_NOT_LOCALIZED_IN_NATIVE_PERTURBATION_STATES`. MATCH/PARTIAL/BLOCKED recovery outcomes remain non-authorizing. No source statistic, source name, k anchor, branch edge, or threshold is changed by this infrastructure amendment.

Provider: exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Conditional activation

This gate is authorized **only if** a valid terminal perturbation-state aggregate (the original aggregate, or its prospectively preregistered seam-preserving recovery described above) is classified exactly
`M21_CMB_BRANCH_NOT_LOCALIZED_IN_NATIVE_PERTURBATION_STATES`.

For MATCH/PARTIAL/BLOCKED parent outcomes this protocol remains historical preparation and MUST NOT execute.

## Question

If native perturbation states do not carry the f_w=0.003 branch map, does that map appear in the actual CMB source combinations stored by the perturbation module before the transfer/harmonic sparse-l stage?

This is numerical localization only; no K1/K3/K4 promotion or physical/defect claim is authorized.

## Exact source authority

The pinned public `classy.get_sources()` is the mandatory access path. Exact source documents that it returns the source functions stored in the perturbation module at all sampled `(k,tau)` and includes combinations later used for CMB/LSS. Returned arrays have shape `[index_k][index_tau]`, with native k in 1/Mpc and tau in Mpc.

Frozen CMB source names are exactly:

- `t0`
- `t1`
- `t2`
- `p`

No post-result source-name selection is allowed.

No CLASS C equations may be patched for this gate.

## Physical cases and numerical lanes

Use exactly the same `ref/f2/f3/f4` physical realizations and six thermodynamics numerical lanes as `protocol/W04_M21_PERTURBATION_STATE_BRANCH_SIGNATURE_v0.1.md`:

`NDF_T1E5,NDF_T1E6,NDF_T1E7,RK_T1E5,RK_T1E6,RK_T1E7`.

The branch-change and same-branch-control edge lists are inherited verbatim from that parent protocol.

## Frozen k and time coordinates

Use exactly the immutable geometry config in `verification/m21/m21_perturbation_state_gate_config.json`:

l anchors `[100,400,800,1200,2000]` and their five exact k anchors derived from `k=l/D_star`.

Unlike the native-state output gate, source arrays must **not** select nearest native k. For each tau sample, interpolate each source linearly in `log(k)` from the native full k grid to each exact frozen k anchor. Every anchor must lie strictly inside the native k range for every lane/case or the gate is BLOCKED.

Primary recombination window is frozen from the terminal capability reference thermodynamics table:

- `tau_min = 146.1893481575377 Mpc` (reference z=2500)
- `tau_max = 488.2339443484317 Mpc` (reference z=500)

For lane-to-lane comparison, interpolate the second lane source onto the first lane tau grid over strict overlap inside this window. At least 16 overlap samples are required.

## Frozen statistic

For each edge E, case C, k anchor K and source S:

`D(E,C,K,S) = ||A-B_interp||_2 / max(||A||_2, ||B_interp||_2, 1e-300)`.

With `J_FLOOR=1e-12`:

`J(E,K,S) = D(E,f3,K,S) / max(D(E,ref,K,S),D(E,f2,K,S),D(E,f4,K,S),J_FLOOR)`.

A source cell is localized iff `J>=3`.

An edge is localized iff at least one of its 20 frozen `(K,S)` cells is localized.

Report Jmax, top cell, localized-cell count and top10 for every edge.

## Frozen classification

Integrity/build/classy/schema/k-range/time-overlap failure ->
`M21_CMB_SOURCE_BRANCH_SIGNATURE_BLOCKED`.

All four branch-change edges localized and zero same-branch controls localized ->
`M21_CMB_SOURCE_BRANCH_SIGNATURE_MATCHES_CMB_MAP_WITH_SCOPE`.

At least two branch-change edges localized but the full pattern fails ->
`M21_CMB_SOURCE_BRANCH_SIGNATURE_PARTIAL`.

Fewer than two branch-change edges localized ->
`M21_CMB_BRANCH_NOT_LOCALIZED_IN_DIRECT_CMB_SOURCES`.

## Consequence

- MATCH/PARTIAL: localize source/k/tau support prospectively; no defect claim.
- NOT_LOCALIZED: upstream perturbation state and direct CMB source layers are both closed under frozen metrics. The next admissible localization is transfer/harmonic sparse-l interpolation, where independent `M21_L_GRID_PHASE_L400_SIGNATURE_SUPPORTED_WITH_SCOPE` already provides a phase-sensitive downstream signature.
- BLOCKED: infrastructure recovery only.

## Interpretation ceiling

No outcome directly establishes global convergence, a correct production precision profile, a CLASS bug, K1/K3/K4, or a physical mixed-dark-matter conclusion.