# W03/M07 — prospective lambda=0.225 within-family holdout

Date: 2026-09-09  
Status: **SUPPORTED — B8 level 1 prospective within-family interpolation holdout**

## Prospective chronology

The holdout was frozen before first execution.

Preregistration commit:
- commit `b0ff43a0951458293ffb71b2dd2646a974b12cd6`;
- timestamp `2026-09-09T10:12:37Z`;
- file `M07_HOLDOUT_L0225_PREREGISTRATION.json`;
- holdout lambda `0.225` was excluded from training.

First execution commit:
- commit `2f66353acad0fe85cf570f3198e9a7785e64e783`;
- timestamp `2026-09-09T10:13:04Z`.

First Actions execution:
- run `34339027169`;
- run number `1`;
- started `2026-09-09T10:13:06Z`;
- conclusion `success`.

Therefore the repository prediction preceded the first holdout exposure. Later reruns cannot strengthen or redefine this prospective status; run #1 is the evidential run.

## Frozen prediction rule

Training source: strict production run `34338140447`, using only lambda `{0.075,0.15,0.30}`.

For each response component j:

`c_j = mean[r_j(lambda)/lambda^2]` over the three training lambdas,

then

`r_j(0.225) = c_j * (0.225)^2`.

The full 7-component lnH and 35-component lnP predictions were committed before execution.

Frozen acceptance:
- relative L2 error lnH <= `0.02`;
- angle lnH <= `0.3 deg`;
- relative L2 error lnP <= `0.05`;
- angle lnP <= `2 deg`;
- |Omega_scf-target| <= `1e-6`;
- lambda-zero reference max |lnH| <= `1e-8`;
- lambda-zero reference max |lnP| <= `1e-5`.

## Run #1 result

Artifact: `w03-m07-holdout-l0225`.  
Artifact digest: `sha256:3f7f149356f56284d137223b3e32b32992aea815400072b0be86db5e9d0fd576`.

Achieved scalar fraction:
- `Omega_scf(today)=0.6826869551832927`;
- target error `9.64387e-11`.

Actual holdout response norms:
- `||lnH||_2 = 0.002497613515`;
- `max|lnH| = 0.001272027089`;
- `||lnP||_2 = 0.005979541367`;
- `max|lnP| = 0.001709898520`.

Prediction errors:
- lnH relative L2: `0.001326277551` = **0.1326%**;
- lnH angle: `0.01999785 deg`;
- lnP relative L2: `0.009868617593` = **0.9869%**;
- lnP angle: `0.52495276 deg`.

All frozen gates pass.

Lambda-zero reference in the same run:
- max |lnH| = `1.08876e-10`;
- max |lnP| = `2.16648e-10`.

## Interpretation

This is genuine prospective predictive support for the local M07 law `r ~ q=lambda^2` **within the tested canonical family and interpolation regime**.

It is stronger than retrospective interpolation because the 0.225 response was not used to define the rule or acceptance thresholds.

It does not establish:
- a universal DSIR residual law;
- cross-family predictive closure;
- observational distinguishability;
- evidence that canonical quintessence is the physical dark-energy model;
- a discovery claim.

B8 state: `SUPPORTED`, strength level `1` (within-family withheld interpolation point).

## Future-model lesson

Candidate construction must freeze a quantitative response relation and complete prediction vector before holdout exposure. A successful within-family holdout validates local predictive regularity, but later waves must escalate to withheld regimes and mechanisms before treating the relation as a robust model-building law.

This generates DP-0811.
