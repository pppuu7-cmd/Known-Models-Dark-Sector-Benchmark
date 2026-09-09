# KMDSB design-prior promotion log

Updated: 2026-09-09

Purpose: record explicit evidence before changing design-prior maturity from `ACTIVE` to `REINFORCED`, `CORE` or `RETIRED`.

Promotion is evidence state, not editorial preference. A prior is not promoted merely because it appears in the construction methodology.

## Promotion batch P-001 — after W03 M07/M08 common-operator control

### DP-0103 -> REINFORCED

Requirement: target covariance-whitened observable directions rather than raw theory distance.

Independent evidence:
- W00/M01: clean C1 theory deformation is `NONIDENTIFIABLE` in corrected ShapeFit despite nonzero theory response.
- W03/M08: CPL raw P+H local singular-value ratio is `0.0502`, but under the common ShapeFit covariance the whitened ratio becomes `0.1805`; the observational metric materially changes local geometry.
- W03/M07: after CPL profiling, raw/theory and observation-space interpretations differ in absolute information; covariance weighting and profiling drive `sigma_q` to `212.67`.

Decision: `REINFORCED`.

### DP-0105 -> REINFORCED

Requirement: every clean local response is compared against a real covariance scale.

Independent evidence:
- W00/M01 ShapeFit calibration: local `epsilon_w=1e-4` is only `~5.61e-4 sigma`.
- W03/M07 common ShapeFit: even the largest frozen M07 `q=.09` is only `4.23e-4 sigma` after profiling the local CPL family span.

Decision: `REINFORCED`.

### DP-0303 -> REINFORCED

Requirement: parameter count is not identified/response rank; near-collinearity must be quantified.

Independent evidence:
- W01/M03 GDM: cs2/cv2 low-k matter directions are nearly collinear (`~0.323 deg`, tiny second singular value ratio).
- W03/M08 CPL: two physical parameters produce strongly anisotropic P+H response, angle `9.179 deg`, raw `sigma2/sigma1=0.0502`; covariance whitening changes but does not erase the anisotropy.

Decision: `REINFORCED`.

### DP-0304 -> REINFORCED

Requirement: within-family holdout support is distinct from universal/cross-family support.

Independent evidence:
- W01/M03 methodology already kept within-family interpolation distinct from universal law support.
- W03/M07 has a prospectively frozen within-family lambda=.225 holdout that passes, while M08 subsequently absorbs the tested M07 P/H signature and common ShapeFit profiling finds essentially no mechanism-specific information.

The two facts coexist: predictive regularity can be real while mechanism uniqueness is absent.

Decision: `REINFORCED`.

### DP-0504 -> REINFORCED

Requirement: novel microphysics must generate a distinctive observable direction, not merely a new interpretation/action/field.

Independent evidence:
- W01/M05 generated the rule through modified-gravity comparator pressure.
- W03/M07 canonical scalar microphysics has clean equations, quotient geometry and prospective holdout support, yet the step-stable M08 CPL family absorbs the P+H response to ~1.1%, and common ShapeFit profiling leaves only `~4.23e-4 sigma` at q=.09.

Decision: `REINFORCED`.

### DP-0702 -> REINFORCED

Requirement: theory-space and observation-space comparator graphs remain separate until a pinned operator/covariance supports promotion.

Independent evidence:
- W02 explicitly maintained separate theory and observation graphs and forbade observational promotion from raw angles.
- W03 M07/M08 common ShapeFit uses one preregistered operator/covariance for both families and shows that covariance weighting changes the CPL singular spectrum and the meaningful M07 residual significance.
- DSIR AD-002 independently hardens the same rule for Article-2 G5.

Decision: `REINFORCED`.

## Not promoted yet

The following newer W03 priors remain `ACTIVE` despite strong single-wave evidence:
- DP-0815 full nearest-family manifold profiling;
- DP-0816 exact common cross-family observation-operator bridge;
- DP-0817 closure/normalization provenance;
- DP-0813 predictive-vs-identifiable axis separation;
- DP-0814 absolute profiled significance alongside geometry.

Reason: they should survive at least one additional independent mechanism/family or later wave before promotion.

No prior is `CORE` yet. `CORE` remains reserved for requirements that survive a dedicated adversarial wave and are necessary for actual future-candidate construction.
