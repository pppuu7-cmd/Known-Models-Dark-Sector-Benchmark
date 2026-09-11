# W05 M37 K0 output-root harness recovery v0.1

## Trigger
The exact-pin M37 f(T) provider probe run 34650851131 built successfully and both frozen arms exited 0, but the K0 analyzer consumed zero-byte placeholder files because CLASS interpreted `root = output/reference_` and `root = output/active_` by appending `_cl.dat` / `_pk.dat`, producing `reference__cl.dat`, `reference__pk.dat`, `active__cl.dat`, and `active__pk.dat`. The workflow had passed `reference_cl.dat` / `active_cl.dat` etc. to the analyzer and touched those missing names before analysis.

This is a harness/output-path defect, not a scientific or physical failure.

## Frozen scientific configuration
Recovery MUST retain without modification:
- provider: `Speeddemon5050/Modified-CLASS-fT-Exact-`;
- exact provider commit: `74e6a8679cdc233fb339c67127ed0921ba547894`;
- reference arm: `n_fT = 0.0`;
- active arm: `n_fT = 0.10`;
- H0=67.36, omega_b=0.02237, omega_cdm=0.1200, N_ur=3.044, N_ncdm=0, tau_reio=0.0544, A_s=2.100e-9, n_s=0.9649;
- output=tCl,mPk, l_max_scalars=2500, P_k_max_h/Mpc=1.0, z_pk=0;
- existing analyzer and response threshold 1e-6;
- source-marker requirements and exact-pin provenance requirements.

## Allowed repair
Only harness plumbing may change:
1. do not manufacture/touch placeholder scientific outputs;
2. pass the actual provider-emitted paths `reference__cl.dat`, `reference__pk.dat`, `active__cl.dat`, `active__pk.dat` to the unchanged analyzer;
3. upload those actual files and exact build/execute/source-audit evidence.

No physics parameter, provider source, threshold, comparator, or classification rule may be changed after observing the recovery result.

## Prospective interpretation
- If exact pin/build/source markers hold, both arms exit 0, all four actual outputs are finite/nonempty, and the frozen analyzer's response activity gate is satisfied, classify only `M37_K0_PASS_WITH_SCOPE_EXECUTABLE_PROVIDER`; K1-K9 remain open and publication/author provenance remains a separate K0 authority question.
- If execution/output remains blocked, classify the first causal provider/infrastructure/harness blocker. Do not infer physical falsification.
- A green GitHub workflow is not itself a scientific PASS.
