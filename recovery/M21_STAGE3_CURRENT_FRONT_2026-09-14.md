# M21 numerical CMB precision current front — 2026-09-14

## STATE_READ

Authoritative repository: `pppuu7-cmd/Known-Models-Dark-Sector-Benchmark`.
Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Do not rerun stage-2/stage-3 or consume the first cross-evolver run as science.

## TERMINAL STAGE-2 / STAGE-3

Stage-2 run `34872522336`: `M21_CMB_PRECISION_STAGE2_COMPLETE`; G1A removes the excursion and G2B reduces it.

Stage-3 run `34878158930`, artifact `10361784318`, digest `sha256:733e995346926ebbb3dd7355a33fbc0090fb5cc027b66eea0c7c968bc86453a9`: `M21_CMB_PRECISION_STAGE3_COMPLETE`.

Stage-3 numerical localization:
- `tol_thermo_integration=1e-5`: `Emax=0.03431664516144772`, removes;
- `l_logstep=1.026`: `Emax=70.53199679337801`, reduces;
- `l_linstep=25`: `Emax=78.37222398394675`, reduces;
- other frozen G1A/G2B single controls are insufficient/no-op for this flat benchmark.

Canonical stage-3:
`waves/wave_04_dark_matter/M21_CMB_PRECISION_STAGE3_SINGLE_PARAMETER_DECOMPOSITION_TERMINAL.json`.

## TERMINAL THERMODYNAMICS TOLERANCE DIRECTION

Run `34879598732`; artifact `10363062831`; digest `sha256:4a91404ff0ea4cfd13d6287bab7d04a01a9ecb4083a71897df4828ca686b1c51`.

Classification: `M21_THERMO_TOL_NONMONOTONE_DIRECTIONAL_RESPONSE`.

Frozen NDF15 tolerance ladder Emax:
- `1e-4`: `0.3390877059308329` REMOVES
- `3e-5`: `0.013135340186788207` REMOVES
- `1e-5`: `0.03431664516144772` REMOVES
- `3e-6`: `0.01087788199580774` REMOVES
- `1e-6`: `534.8355868817356` INSUFFICIENT
- `3e-7`: `417.69996905927826` INSUFFICIENT
- `1e-7`: `1.000009046588933` REMOVES

Therefore decreasing `tol_thermo_integration` is not a monotone convergence path. Exact source confirms thermodynamics uses separate default `thermo_evolver=ndf15`; generic `evolver=0` does not change that. NDF15 uses rtol in initial-step, Newton acceptance, step rejection, and step/order selection. See `models/mixed_cold_warm/m21_thermodynamics_adaptive_path_source_audit_2026-09-14.md`.

Canonical terminal:
`waves/wave_04_dark_matter/M21_THERMO_TOLERANCE_DIRECTION_AUDIT_TERMINAL.json`.

## TERMINAL TRANSFER-L DIRECTION / INTERACTION

Run `34879864684`; artifact `10364145887`; digest `sha256:9e87c183e5827ec160e40c69e0ba6002be53e76bc123252fd3b66a9e48dbe344`.

Classification: `M21_G2B_L_SAMPLING_INTERACTION_AND_DIRECTION_SUPPORTED`.

Ordered denser transfer-l path:
- `(1.05,32)`: Emax `154.25643660087928`
- `(1.026,25)`: `34.305011087551506`
- `(1.015,20)`: `13.582267651621091`
- `(1.010,15)`: `2.543930110490425`, REMOVES

Interaction supported and direction monotone. Exact source establishes decreasing `l_logstep/l_linstep` is genuine denser l sampling for flat K=0. This supports transfer-l under-resolution as a numerical contributor, but not yet a global limit.

Canonical terminal:
`waves/wave_04_dark_matter/M21_G2B_L_SAMPLING_DIRECTION_INTERACTION_AUDIT_TERMINAL.json`.

## CROSS-EVOLVER FIRST RUN — HARNESS BLOCKED ONLY

Parent preregistration:
`protocol/W04_M21_CONDITIONAL_THERMO_EVOLVER_CROSSCHECK_v0.1.md`.

First execution run `34883668337` is terminal blocked. All six lanes failed before scientific output because the harness serialized `thermo_evolver` as strings (`rk` / `ndf15`) while exact CLASS reads the field with `parser_read_int`.

Exact enum mapping is `rk=0`, `ndf15=1`.

Canonical blocker:
`waves/wave_04_dark_matter/M21_THERMO_EVOLVER_CROSSCHECK_HARNESS_BLOCKED.json`.

This run has no solver/physics verdict.

## ACTIVE GATE A — ENUM-SERIALIZATION RECOVERY

Recovery protocol:
`protocol/W04_M21_THERMO_EVOLVER_ENUM_SERIALIZATION_RECOVERY_v0.1.md`.

Run: `34884124030`.
Activation PASS. Six recovery lanes are in scientific execution:
- NDF15 at `1e-5,1e-6,1e-7`, serialized `thermo_evolver=1`;
- RK at `1e-5,1e-6,1e-7`, serialized `thermo_evolver=0`.

Only enum serialization changed. Original 2x3 matrix, physical inputs, precision baselines, thresholds and classifier are unchanged. Do not consume partial lane values; wait for terminal aggregate.

## ACTIVE GATE B — TRANSFER-L TAIL CONVERGENCE

Protocol:
`protocol/W04_M21_G2B_L_SAMPLING_TAIL_CONVERGENCE_v0.1.md`.

Run: `34883823728`.
Activation PASS. New mandatory lanes in scientific execution:
- `LTAIL_T3=(l_logstep=1.0075,l_linstep=12)`;
- `LTAIL_T4=(1.005,10)`.

Immutable anchor is terminal `LPAIR_T2=(1.010,15)` with Emax `2.543930110490425`.
The gate tests both stable REMOVES status and contraction of direct CMB distances `T2->T3` versus `T3->T4`.
Do not use partial tail values before aggregate terminal.

## K1 RE-ENTRY BOUNDARY

K1 remains OPEN. Current f2/f3/f4 diagnostics cannot directly promote K1.
Any future K1-v2 must return to the full frozen warm-fraction ladder `{0.10,0.03,0.01,0.003,0.001}` plus exact CDM, fix the historical descending-H interpolation defect, use prospectively frozen support-aware P(k) treatment, and include a numerical-floor/convergence control for CMB. The old v1 result remains historical, not physical falsification.

## CLAIM CEILING

No current result establishes a CLASS bug or production tuning rule. K1/K3/K4 are not promoted. No physical falsification or validation of mixed cold+warm dark matter follows from these numerical diagnostics.

## NEXT_ACTION

1. Check recovery run `34884124030` and l-tail run `34883823728`.
2. If either is non-terminal, do not duplicate it or inspect partial scientific values.
3. On terminal aggregate, verify artifact identity/digest and materialize canonical result.
4. Use the cross-evolver classification to decide whether thermodynamics sensitivity is NDF15-specific, solver-independent at tight tolerance, mixed, or unsupported.
5. Use l-tail classification to decide whether transfer-l removal is stable with adjacent-grid contraction.
6. Only after both terminal results may a prospectively frozen K1-v2 numerical-reference selection rule be opened.
