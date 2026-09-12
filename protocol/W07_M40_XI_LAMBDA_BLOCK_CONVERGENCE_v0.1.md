# W07 M40 xi/lambda immutable block-convergence audit v0.1

Date: 2026-09-12
Model: M40 pinned EFTCAMB Hořava representative
Purpose: localize the already-observed coarse/fine derivative nonconvergence of the xi and lambda coordinate probes into CMB versus P(k) response blocks without any new EFTCAMB execution.

## Immutable inputs
- xi artifact: run `34695841353`, artifact `10298324085`;
- lambda artifact: run `34695841353`, artifact `10298572066`;
- provider commit `16d9c4e9f85751e30efd0a53b177941713078904`.

For each coordinate reconstruct coarse (`delta=2e-6`) and fine (`delta=1e-6`) central derivatives independently for the CMB scalar-spectrum block and the P(k) block. Use one common support per coordinate and normalize each block by the base L2 norm.

Reuse the frozen convergence rule: principal angle <=5 degrees AND relative norm mismatch <=0.25. No step change, threshold change, parameter retuning or rank promotion is authorized.

Output is descriptive only. `K2_promoted=false`, `physical_falsification=false`, `complete_Horava_family_claim=false`.