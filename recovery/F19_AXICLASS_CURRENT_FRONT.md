# F19 / AxiCLASS current front

Updated: 2026-09-14  
Family: F19/M19 fuzzy / ultralight axion dark matter  
Provider: `PoulinV/AxiCLASS@ae9609e1f96ddebbb6cc8a46de94512514c68781`  
Repository evidence and Actions override this handoff if newer.

## Authoritative K0/K1 gate

Frozen protocol: `protocol/W04_F19_AXICLASS_INDEPENDENT_PROVIDER_K0K1_PROBE_v0.1.md`.

Authoritative recovery run: `34846931382`, head `249600ffd65510f8fb51156f1f300b023e37256c`.

At this handoff:

- `author_control` job `103985050637`: terminal SUCCESS;
- exact pin built and unchanged `example_axionDM.ini` executed with finite provider products;
- immutable author-control artifact `10348785556`, digest `sha256:d0d4b2f3e5875d86eaaaeeba7f2bcd59917b38e91d2496ca0490e5da036faf4b`;
- `zero_identity` job `103985050960`: still NON-TERMINAL inside step `Frozen C0 and exact Z0 executions`;
- frozen analyzer has not run;
- therefore there is **no authoritative K1 verdict yet** and no K0/K1 matrix promotion is allowed from the non-terminal branch.

Do not cancel, duplicate, or use partial C0/Z0 values while this run is non-terminal.

## Frozen K1 question

C0: vanilla same-binary control with no scalar component.

Z0: exact scalar-zero branch retaining axion code path with `scf_parameters=0,0`, no shooting, same cosmology/output/precision, scalar perturbations enabled, axionCAMB-like fluid representation enabled.

Frozen thresholds:

- H max symmetric relative difference <= `1e-10`;
- same-source CDM-density max symmetric relative difference <= `1e-10`;
- linear P(k) max symmetric relative difference <= `1e-8`.

Allowed classifications are exactly the parent protocol strings; provider blockage is not F19 physical falsification.

## Terminal independent source authority

Protocol: `protocol/W04_F19_AXICLASS_EXACT_SOURCE_AUTHORITY_AUDIT_v0.1.md`.

Run `34861348551`, head `d343225a81203f3ef85f84edf7c66d6f7783b69b`, four independent source lanes + aggregate all SUCCESS.

Aggregate artifact `10353979653`, digest `sha256:bb907bd03abe050a0a680241873cc9f48a2d00119f418a2f502cc909e1bdc92b`.

Canonical result: `waves/wave_04_dark_matter/F19_AXICLASS_EXACT_SOURCE_AUTHORITY_RESULT.json`, commit `9e7e2931fa3e19d302129116c6bfde850f5d7140`.

Classification: `F19_AXICLASS_EXACT_SOURCE_AUTHORITY_PASS_WITH_SCOPE`.

Established scope: exact pin is a genuine executable source tree with author axion example, explicit cosine axion potential and derivatives, scalar background/KG-fluid machinery, scalar perturbation states in the same solver as photon/UR Boltzmann hierarchies, and provenance independent of the blocked CLASS_GSF implementation. This result does not itself promote K0/K1.

## Exact-zero fluid-coordinate regularity

Exploratory source diagnosis identified a specific provider-coordinate issue; a separately frozen confirmation gate then verified it.

Protocol: `protocol/W04_F19_AXICLASS_EXACT_ZERO_FLUID_COORDINATE_REGULARITY_CONFIRMATION_v0.1.md`.

Run `34862292830`, head `e71e3d91c26160fbfd14bba5d341010cd377b69f`; R1-R4 and aggregate all SUCCESS.

Aggregate artifact `10355146364`, digest `sha256:cac8dbc73268e17d2f9642cf9e6997d4a7e60cdf9c59b69ac2aae50bfe51848c`.

Canonical result: `waves/wave_04_dark_matter/F19_AXICLASS_EXACT_ZERO_FLUID_COORDINATE_REGULARITY_RESULT.json`, commit `368a0ca97640b21362c1027c90ffe57debffa077`.

Classification: `F19_AXICLASS_EXACT_ZERO_FLUID_COORDINATE_SINGULARITY_CONFIRMED_WITH_SCOPE`.

Confirmed chain:

1. `scf_parameters_size != 0` activates the scalar species even when values are exactly zero;
2. n=1 axion origin has `V(0)=V_phi(0)=0`; with zero velocity, `rho_scf=p_scf=0`;
3. provider forms `w_scf=p_scf/rho_scf`, hence exact zero yields non-finite `w_scf`;
4. frozen Z0 flags select `scf_fluid_variables=true` from the start;
5. `w_scf` is consumed in executable fluid perturbation IC/stress-energy/source/gauge paths;
6. binary64 NaN propagation does not automatically reduce these expressions to a finite zero.

This confirms a singularity of the selected provider fluid coordinates. It does **not** prove that this is the unique cause of the current long execution, does not replace the K1 verdict, does not authorize patching the provider, and is not physical F19 falsification.

## Future K2 parameter identity — prepared but NOT authorized

Protocol: `protocol/W04_F19_AXICLASS_K2_PARAMETER_IDENTITY_PREPARATION_v0.1.md`.

Run `34862014570`, head `797d6ddfb7862b584a8634d890f5b01b6b4f5bc6`; P1-P4 and aggregate all SUCCESS.

Aggregate artifact `10356095722`, digest `sha256:76a9ca9657628dcc041c027ae711728defb35145ee8bdd99c86c40222249f8aa`.

Canonical result: `waves/wave_04_dark_matter/F19_AXICLASS_K2_PARAMETER_IDENTITY_PREPARATION_RESULT.json`, commit `43fbfba8908348952e65b43ad74a63a0266e27c6`.

Classification: `F19_AXICLASS_K2_PARAMETER_IDENTITY_PREPARATION_PASS_WITH_SCOPE`.

Semantic map:

- `f_axion`: potential decay scale, not abundance;
- `Omega_scf`: present scalar-density target/shooting coordinate;
- `fraction_axion_ac`: distinct critical-epoch fraction target, not present `Omega_scf`;
- `scf_parameters`: scalar initial-condition/tuning parameters.

`K2_authorized=false` until terminal K1 PASS.

## Conditional recovery if K1 run terminates without a verdict

Protocol prepared only: `protocol/W04_F19_AXICLASS_K1_CONDITIONAL_SPLIT_EXECUTION_RECOVERY_v0.1.md`, commit `37c59e31a4057a6d3517a2c7e00bdcaaa3a150e1`.

It is **not authorized to execute while run 34846931382 is non-terminal**.

If and only if that run terminally times out/cancels/fails before the frozen analyzer can classify both branches, the first recovery must preserve the exact C0/Z0 scientific INIs and thresholds and change orchestration only: C0 and Z0 in separate observable jobs with independent return-code/log/raw-product artifacts and a frozen aggregate barrier.

Forbidden in that exact replay: small nonzero field surrogate, fluid/KG switch changes, provider source regularization, tolerance/threshold changes, cosmology changes or post-hoc interpretation changes.

## Immediate decision tree

1. Recheck run `34846931382` first.
2. If it terminally yields a valid K1 classification, canonicalize that result and follow the parent protocol next-gate rule.
3. If terminally infrastructure/provider-blocked before analyzer classification, execute the already frozen split-execution recovery unchanged.
4. If exact replay also confirms exact-zero provider blockage, preserve source-authority PASS and design a **new** prospectively frozen author-supported regular zero-abundance reference or move to another independent provider. Do not silently substitute a small nonzero field.
5. Only terminal K1 PASS may authorize a new K2 geometry preregistration; use the parameter-identity preparation above to bind abundance correctly.

## Claim ceiling

- no F19 physical falsification;
- no K2 execution yet;
- no K3-K9 promotion;
- no global dark-sector conclusion from this front;
- blockers are provider/reference-coordinate evidence, not absence of the physical family.
