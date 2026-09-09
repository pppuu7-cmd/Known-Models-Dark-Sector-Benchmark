# M07 small-lambda order audit — precision-conditioned rerun protocol

Date frozen: 2026-09-09  
Status: **FROZEN BEFORE TIGHT SMALL-LAMBDA OUTPUTS**

## Why a rerun is allowed

The original small-lambda order audit used strict scalar-density shooting but default perturbation integration/sampling precision. It rejected the preregistered quadratic-order hypothesis with `p=1.16024` even though the background H response followed nearly exact quadratic scaling.

Independently, the already-preregistered perturbation-precision q audit `34359536106` changed only the perturbation tier and demonstrated that, for lambda `.025` versus `.075`,

- baseline q-scaled matter-response relative difference: `0.218493`;
- tight-tier relative difference: `0.000551889`;
- baseline q angle: `12.5058 deg`;
- tight-tier angle: `0.0273111 deg`.

That independent PASS establishes numerical justification for a precision-conditioned rerun. It is not permission to alter the scientific acceptance criteria.

## Frozen rerun rule

Repeat exactly the original new local-geometry points

`lambda={0.005,0.010,0.020,0.040}`

with unchanged:
- physical branch;
- `Omega_scf_target`;
- shooting tolerance `1e-13`;
- response grid;
- reference controls;
- `100 x reference floor` signal rule;
- fitted-power interval `1.8 <= p <= 2.2`;
- monotone q-convergence rule.

The **only** newly selected numerical settings are those already validated independently by run `34359536106`:

`tol_perturbations_integration = 1e-8`

`perturbations_sampling_stepsize = 0.01`.

No further precision escalation or threshold change is allowed after seeing this rerun.

## Interpretation

- If the unchanged order/convergence gates PASS under the independently validated tight tier, freeze `q=lambda^2` as the local M07 response coordinate in the scoped low-k theory-response block.
- If they still FAIL, reject or leave inconclusive the q-linearity hypothesis in this scale range; do not tune thresholds or precision again in this wave.
- Neither outcome is an observational-identifiability or B8 claim.
