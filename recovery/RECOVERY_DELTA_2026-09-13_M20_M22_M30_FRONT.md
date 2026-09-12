# KMDSB recovery delta — 2026-09-13 M20 / M22 / M30 frontier

## M20 / F20 — SIDM K4 numerical robustness closed with scope

Pinned provider: `shinichiroando/sashimi-si@e17d3664dac677b604fd4ff02fb2af105a6937fa`.

The original K4 diagnostics used ordinary p95 over flattened provider nodes while changing `N_herm`. Provider source uses Gauss-Hermite nodes and exposes effective population weights; changing `N_herm` changes the node set. The preserved unweighted asymptotic control run `34717891994`, job `103618297914`, artifact `10305575797` (`sha256:668d9d289b2877cfc0bd8de211434e4a0c2abd46451cd5cab7c77351960cf41c`) gave max discrepancies 0.9671171247950625 for 13->17 and 0.8916774732400928 for 17->21.

Prospective weighted-support recovery run `34718995720`, job `103621243622`, artifact `10305443316` (`sha256:b415963ea033c9c4b7dced8e1fcc95cd39df48cef3eccc88ff1ca1414001033d`) reduced the same high-order discrepancy to 0.014529410998643114 for 13->17 and 0.019693948085558 for 17->21; parent classification remains `M20_K4_WEIGHTING_REDUCES_SENSITIVITY_NOT_CONVERGED_DIAGNOSTIC` because its frozen monotonic clause failed. The old unweighted negative control is not relabelled.

Prospective high-order weighted confirmation run `34719071192`, job `103621453342`, artifact `10305148808` (`sha256:ddd886038e813ecd9cb16b691fe11359a210115f9b03c6c25a092245c7f42d99`) passed its frozen gate: 21->25 max=0.015358563421115096, 25->29 max=0.013049208459761123.

Prospective independent weighted-grid run `34719183403` passed both axes. Mass-grid job `103621755655`, artifact `10305633214` (`sha256:ceaf9b7afe94bb51cb25094c15bc027da45e861693fc94552bb4945b9209c25f`): N_ma 30->60 max=0.019365180558786114, 60->120 max=0.010405632254471308. Redshift-grid job `103621755505`, artifact `10305352361` (`sha256:25c87ec802e51718da0fec0a39dda105a5df0934c56ebc603778f7dc57cb6e98`): dz 0.2->0.1 max=0.042314014919695046, 0.1->0.05 max=0.005888014337777188.

The deterministic synthesis `protocol/W04_M20_K4_NUMERICAL_ROBUSTNESS_SYNTHESIS_v0.1.md` introduced no new continuous threshold; it ANDs three already-frozen classifications. Canonical result: `M20_K4_PASS_WITH_SCOPE_WEIGHTED_HERMITE_MASS_REDSHIFT_CONVERGENCE`, `K4_promoted=true`, physical falsification false. Scope is only the pinned nonlinear SASHIMI-SIDM structural-response setup. Matrix sync run `34719285328`, job `103622040331`, pushed commit `e6e2c58` and set F20 K4 to `PASS_WITH_SCOPE_WEIGHTED_HERMITE_MASS_REDSHIFT_CONVERGENCE`, coverage `K1_K4_NONLINEAR_SCOPED_PASS_K3_K5_K9_OPEN`.

## M20 / F20 — K2 sigma0/m × w finite-base geometry

Prospective protocol: `protocol/W04_M20_K2_SIGMA_W_LOCAL_GEOMETRY_PREREGISTRATION_v0.1.md`. Run `34719372299`, job `103622273138`, artifact `10305763421` (`sha256:d3e28978e7e3f996d63d9ad4f33d0e9d0aa7cc9c2b3e88d6bae2bd3e1154e145`) completed successfully at weighted-converged numerics N_herm=25, N_ma=120, dz=0.05.

Both finite-base log-parameter tangents are highly converged: sigma coarse/fine signed cosine=0.9999999148745746, relative norm mismatch=0.0002702271473803976; w cosine=0.9998745616099864, mismatch=0.0017417452375661927. But the two fine directions fail the preregistered independence gate: angle=3.9582870141455415 deg (<10), s2/s1=0.03455631573532606 (<0.08), signed cosine=0.9976145706197536. Classification `M20_K2_FINITE_BASE_SIGMA_W_LOCAL_DEGENERACY_DIAGNOSTIC`; K2 and K5 are not promoted, physical falsification false. Durable summary: `waves/wave_04_dark_matter/M20_K2_SIGMA_W_LOCAL_GEOMETRY_RESULT.json`.

Interpretation: the tested nonlinear structural-response map remains locally low-rank despite two microscopic provider parameters. At the exact CDM boundary sigma0/m=0, w is unidentifiable; this result strengthens rather than removes the quotient/degeneracy warning.

## M22 / F22 — annihilating-DM K4 precision ladder active

Run `34717830680` uses the exact pinned CLASS energy-injection provider and prospectively frozen selected strong/mid/tail p_ann points across provider precision profiles default / cl_permille / cl_ref. Default job `103618126530` and permille job `103618126597` are completed successfully. Reference job `103618126438` remains in progress executing profile cases at this checkpoint. Do not aggregate or launch a dependent M22 K4 confirmation until the reference job and aggregate barrier are terminal.

## M30 / F30 — Horndeski local-2D K4 precision ladder launched

Existing M30 K1 PASS_WITH_SCOPE uses pinned hi_class `0009f51d89e6465c79e570b496c66fc90058fa77`. Existing K2 is PARTIAL from a locally converged radial direction plus an independent c_T direction; complete covariant/source geometry remains open.

New prospective protocol `protocol/W07_M30_K4_LOCAL_2D_PRECISION_PREREGISTRATION_v0.1.md` reuses the repository-standard provider-precision gate: for TT/EE/TE/P(k), `R_fine<=1e-4` and either `R_fine<=0.5*R_coarse` or both coarse/fine <=1e-8. Three frozen physical points cover the established local 2D patch: base (q=0.100,c_T=0), radial (q=0.102,c_T=0), and cT (q=0.100,c_T=0.002). Each point runs default -> cl_permille -> cl_ref serially; points run in parallel with an explicit aggregate barrier.

Run `34719607382`, head `5e2f0763714463b83a1d96e5131d846773c2b04e`. At this checkpoint base job `103622907550` and radial job `103622907535` are in progress building/executing exact pinned hi_class; cT job `103622907454` is queued. No K4 interpretation before all three point artifacts and aggregate are terminal.

## Guardrails

- Preserve every preregistered negative control; no retroactive threshold tuning.
- Weighted M20 recovery does not erase the old unweighted result; it localizes why that statistic was inappropriate for changing quadrature node sets.
- Numerical/provider/infrastructure failure is never a physical family falsification.
- No K2/K5 promotion from M20 sigma-w because the local independence gate failed.
- No terminal known-model sufficiency/new-model verdict before the required coverage and holdout layers are complete.
