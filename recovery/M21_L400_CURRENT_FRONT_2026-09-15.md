# M21 l=400 numerical-mechanism current front — 2026-09-15

## AUTHORITATIVE STATE

Repository: `pppuu7-cmd/Known-Models-Dark-Sector-Benchmark`.
Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Do not restart stage-2/stage-3, thermodynamics-column mining, direct-CMB-source branch mining, or generic l-density sweeps.

K1/K3/K4 are NOT promoted. `physical_falsification=false` throughout this front.

## ESTABLISHED TERMINAL CHAIN

### Thermodynamics numerical path

- stage-3 localized `tol_thermo_integration`, `l_logstep`, `l_linstep` as numerical controls;
- NDF15 tolerance direction is non-monotone;
- NDF15/RK cross-evolver response is mixed;
- exposed thermodynamics state tables do not reproduce the f3-specific CMB branch map.

Therefore no converged thermodynamics reference has been selected.

### Direct perturbation/CMB-source layer

Run `34897602278`, artifact `10369419717`, digest `sha256:15110d1691b36ae173a0538c98daad2471bafa984d0fbad06c22d77db8139bab`:
`M21_CMB_BRANCH_NOT_LOCALIZED_IN_DIRECT_CMB_SOURCES`.

Canonical:
`waves/wave_04_dark_matter/M21_CMB_SOURCE_BRANCH_SIGNATURE_TERMINAL.json`.

None of the four frozen branch-change edges reaches J=3 in native direct CMB source functions. This moves the branch mechanism downstream of source generation.

### Sparse transfer-l phase

Run `34887488405`:
`M21_L_GRID_PHASE_L400_SIGNATURE_SUPPORTED_WITH_SCOPE`.

At nearly fixed sparse-l node count, two independent layouts containing l=400 are HIGH and two l=400-absent layouts are CALM. High-tail membership does not explain the pattern.

### Knot-only propagation

Run `34897465426`:
`M21_L_GRID_KNOT_VALUES_CARRY_L400_SIGNATURE_WITH_SCOPE`.

Run `34901952566`, artifact `10371520158`, digest `sha256:c203bf7a4943d270779069c17b1f0887ff41c25629e340d0b829ea6d0f5cc2a6`:
`M21_L400_SINGLE_KNOT_VALUE_SUFFICIENT_FOR_HIGH_STATE_WITH_SCOPE`.

Canonical:
`waves/wave_04_dark_matter/M21_L400_KNOT_PROPAGATION_TERMINAL.json`.

Removing exactly the direct sparse l=400 knot from each of two independent HIGH supports makes it CALM; common non-400 support remains CALM.

### Local direct-knot smoothness

Run `34903783469`, artifact `10372080830`, digest `sha256:724130c3a35f97dea9b6c3bcf42bd8070fab0958335b7be8c6ff111191fb8ba2`:
`M21_L400_ISOLATED_LOCAL_RESPONSE_SPIKE_SUPPORTED_WITH_SCOPE`.

Canonical:
`waves/wave_04_dark_matter/M21_L400_LOCAL_LEAVE_ONE_OUT_TERMINAL.json`.

Two independent directly-computed sparse neighborhoods:
- A: 399,400,401;
- B: 398,400,402.

Both give:
- direct EE response specificity at l=400 E~178.515;
- symmetric-neighbor predicted E~1.42;
- f3 residual-specificity J ~8.1e4 (A) and ~1.26e5 (B);
- f2/f4 local residuals ~1e-3;
- absolute reference EE curve remains locally smooth.

The f3 response itself is ~4.07e-18 at neighboring knots and ~5.10e-16 exactly at l=400.

This establishes an isolated computed sparse-harmonic-knot numerical spike with scope, not a CLASS bug or physical model failure.

## EXACT SOURCE PATH

At the exact provider pin:

1. perturbation module constructs native sources;
2. transfer module computes `Delta_l^X(q)` on sparse `ptr->l`;
3. harmonic module copies `ptr->l` to `phr->l` and directly computes each sparse C_l;
4. for EE the pointwise harmonic integrand is `P_R(k) * Delta_E(k)^2 * 4*pi/k`;
5. only after direct sparse C_l values exist does CLASS spline C_l in l for arbitrary integer output.

Thus the 398/399/400/401/402 values used above are direct sparse harmonic knots when present, not l-interpolated output values.

## ACTIVE GATE — TRANSFER VS HARMONIC

Protocol:
`protocol/W04_M21_L400_TRANSFER_VS_HARMONIC_DIAGNOSTIC_v0.1.md`.

Workflow:
`.github/workflows/w04-m21-l400-transfer-vs-harmonic-v01.yml`.

Run: `34904313450`.

Two lanes execute independently in parallel:
- A `P400_ON_TAIL_OFF` with direct knots 399,400,401;
- B `P400_EVEN_TAIL_OFF` with direct knots 398,400,402.

An output-only exact-source instrumentation block is inserted only after `harmonic_cls()` returns. It reads and writes diagnostic tables containing native `Delta_E`, exact primordial P_R, exact pointwise EE integrand and direct sparse C_l. It must not alter CLASS state.

Mandatory non-interference gate: instrumented vs immutable factorial C_l normalized L2 `R_null <= 1e-12` for every ref/f2/f3/f4 case.

Frozen layer classifier distinguishes:
- spike already in E transfer kernel;
- spike first visible after EE integrand formation;
- spike first visible only in harmonic q/k accumulation;
- mixed;
- blocked.

Do NOT inspect partial lane values. Wait for the terminal aggregate.

## CLAIM CEILING

The current evidence strongly localizes the historical M21 CMB excursion to a numerical sparse-harmonic l=400 mechanism. It does not yet identify whether the transfer kernel or harmonic accumulation is the first anomalous layer. It does not prove a provider defect, does not select production precision, and does not authorize K1/K3/K4 promotion or physical validation/falsification.

## NEXT ACTION

1. Check terminal aggregate of run `34904313450` only.
2. Verify artifact digest and non-interference controls.
3. Materialize its terminal result in `waves/wave_04_dark_matter/`.
4. If transfer-localized, next analysis should localize the k/q support of the l=400 transfer-response excess using the immutable diagnostic tables.
5. If integrand-localized, localize the k/q support after quadratic/primordial weighting.
6. If accumulation-localized, audit the exact harmonic k/q integration path before any new numerical tuning.
7. Preserve K1/K3/K4 and physical claim ceilings.
