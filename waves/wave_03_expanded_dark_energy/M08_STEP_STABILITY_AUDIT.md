# W03 M08 local-step stability audit

Date: 2026-09-09  
Status: **PASS_WITH_SCOPE**

## Purpose

The first controlled M08 CPL local basis used central finite-difference step `h=1e-3`. Because that basis absorbs the M07 P/H local direction to about 1.1% residual, the result is scientifically important enough that the tangent plane must not depend materially on one arbitrary finite-difference step.

Before the rerun, a second step was frozen:

`h2=5e-4`.

The workflow was also given hard preregistered stability gates; none were changed after output inspection.

## Authority

Actions run: `34395806203`  
Head: `92ae359470374823e9313f2d5958d948f8d222ae`  
Artifact digest: `sha256:97902cc12abf4e18a84dd160f53b22169ec312ecc654dd6d9626cd4e281f3405`  
Pinned CLASS: `e85808324f51fc694d12e3ed7439552a3c3f9540`.

Machine result:
`M08_STEP_STABILITY_RESULT.json`.

## Frozen gates

For `h=1e-3 -> 5e-4`:

- each combined epsilon0/wa derivative relative L2 change <= `0.01`;
- each combined direction angle change <= `0.25 deg`;
- relative change in `sigma2/sigma1` <= `0.05`;
- absolute change in M07 combined absorption residual <= `0.005`;
- relative change in fitted CPL coefficient vector <= `0.05`.

## Direction stability

### epsilon0 direction

Combined P+H:
- relative L2 change `1.20555e-5`;
- angle change `0.0006641 deg`.

Blockwise:
- P relative change `1.26188e-5`, angle `0.0006928 deg`;
- H relative change `3.79638e-7`, angle `1.716e-5 deg`.

### wa direction

Combined P+H:
- relative L2 change `5.57297e-5`;
- angle change `0.0022956 deg`.

Blockwise:
- P relative change `5.70241e-5`, angle `0.0022968 deg`;
- H relative change `8.47902e-8`, angle `4.095e-6 deg`.

All are orders of magnitude inside the frozen gates.

## Response-rank stability

At `h=1e-3`:

`singular values = {1.8829717593, 0.0945281863}`

`sigma2/sigma1 = 0.05020159536`.

At `h=5e-4`:

`singular values = {1.8829586229, 0.0945175584}`

`sigma2/sigma1 = 0.05019630132`.

Relative change in the singular-value ratio:

`1.05456e-4`.

Thus the strong anisotropy of the nominally two-dimensional CPL response is not a finite-difference-step artifact in this tested range.

## M07 absorption stability

At `h=1e-3`, best shared coefficients per unit M07 q:

- `epsilon0/q = 0.1406534871`;
- `wa/q = -0.2006790927`.

Combined residual:

`0.0110746838`.

At `h=5e-4`:

- `epsilon0/q = 0.1406589684`;
- `wa/q = -0.2007007955`;
- combined residual `0.0110683732`.

Changes:
- absorption residual absolute change `6.31e-6`;
- coefficient-vector relative change `9.13e-5`.

Therefore the central result — that the CPL local family span absorbs the M07 P/H direction to roughly 1.1% residual — is **step-stable** within the tested local range.

## Interpretation

This closes the immediate numerical concern that M08's weak second singular direction or the M07 absorption result was produced by the chosen `1e-3` finite-difference step.

It does **not** establish:
- global CPL/M07 equivalence;
- observational equivalence;
- physical truth of CPL;
- Article-2 G5 closure.

The next scientifically relevant gate is observation-space projection through one exact common operator/covariance mapping for both M07 and M08, as frozen in `protocol/W03_M07_M08_COMMON_SHAPEFIT_OPERATOR_V0_1.md`.
