# W04 M21 l=400 conditional scalar-E source factorization v0.1

Frozen: 2026-09-15 while serialization-recovery run `34907528331` is non-terminal and before its recovered source/radial/convolution classification is known.

Provider remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Authorization

This gate is executable only if the terminal artifact from `W04 M21 l400 convolution successor router v0.1` authorizes `SOURCE_FACTORIZATION`.

If not authorized, skip without CLASS execution or scientific output.

## Exact source authority

On the exact provider, scalar CMB E maps transfer type `index_tt_e` to perturbation source `index_tp_p`.

For scalar modes outside RSA the source construction is exactly

`S_E(k,tau) = sqrt(6) * g(tau) * P(k,tau)`.

For TCA on,

`P = 5*s_l[2]*tca_shear_g/8`.

For TCA off,

`P = (pol0_g + pol2_g + 2*s_l[2]*shear_g)/8`.

For RSA on, `P=0`.

The parent internal-path audit also established that scalar-E transfer uses the perturbation polarization source without an additional CMB-E tau window/resampling: at each transfer k the perturbation source is spline-interpolated in k and then copied on the native perturbation tau sampling.

## Purpose

Factor an authorized f3-specific transfer source response into:

1. visibility history `g(tau)`;
2. polarization source factor `P(k,tau)`;
3. their multiplicative combination;
4. only if needed afterward, the perturbation-k -> transfer-k spline layer.

This gate must not use physical interpretation of the WDM fraction to choose windows, k nodes, tau nodes or thresholds.

## Frozen execution design

Execute `ref,f2,f3,f4` in four independent jobs at the same exact physical inputs and `P400_ON_TAIL_OFF` precision profile as the recovered parent.

Use `OMP_NUM_THREADS=1` because this gate is diagnostic instrumentation and the provider TaskSystem consumes that environment variable.

The only provider source modification allowed is an output-only diagnostic patch in `source/perturbations.c` anchored at the exact scalar assignment to `index_tp_p`. It may write, for scalar modes and native perturbation k values spanning the frozen parent support plus exactly one native k node on each side:

- native k index and k;
- native tau index and tau;
- RSA state;
- TCA state;
- `g`;
- `P`;
- `sqrt(6)*g*P`;
- when defined, the primitive terms entering P (`tca_shear_g` or `pol0_g`, `pol2_g`, `shear_g`, `s_l[2]`).

The patch must be placed after these values have been computed and must not modify any provider array, approximation state, integration state, precision, source value or execution order.

Each job must reproduce the immutable parent full `cl.dat` with normalized L2 <= `1e-12` or BLOCK.

## Frozen matching to transfer source

Use only q nodes accepted by the recovered parent integrity gate.

For each parent transfer q/k, use the exact native perturbation k grid to spline-interpolate the recorded native scalar source factor data onto the parent target k with the provider's already-authoritative k-spline rule. Do not nearest-neighbor match.

Because `g(tau)` is k-independent at fixed tau, define target-k polarization factor by the same spline interpolation of native P values. Reconstruct

`S_recon = sqrt(6) * g * P_target`.

Require relative reconstruction error against the parent recovered transfer source <= `1e-10` over all retained finite rows; otherwise `M21_L400_SOURCE_FACTORIZATION_BLOCKED`.

Use the same common-u overlap and immutable support weights `W_q` as the parent analyzer.

## Frozen specificity metrics

For X in `{g,P,S_recon}` define profile distances and support-weighted amplitudes with the same L2 and W-weighting convention as the parent source analyzer.

Let `E_g`, `E_P`, `E_Srecon` denote f3 specificity against max(f2,f4). Reuse the frozen boundary `E > 3`.

The parent recovered source specificity is `E_Sparent` and must be read, not recomputed with altered rules.

Also report approximation-state transition locations and primitive-P component distances, but they are report-only and cannot change classification.

## Frozen classification

Provided parent `E_Sparent > 3` and reconstruction passes:

- `E_g > 3`, `E_P <= 3` -> `M21_L400_SOURCE_VISIBILITY_LOCALIZED_WITH_SCOPE`;
- `E_g <= 3`, `E_P > 3` -> `M21_L400_SOURCE_POLARIZATION_FACTOR_LOCALIZED_WITH_SCOPE`;
- `E_g > 3`, `E_P > 3` -> `M21_L400_SOURCE_VISIBILITY_AND_POLARIZATION_MIXED_WITH_SCOPE`;
- `E_g <= 3`, `E_P <= 3`, but `E_Srecon > 3` -> `M21_L400_SOURCE_MULTIPLICATIVE_INTERACTION_WITH_SCOPE`;
- `E_Srecon <= 3` while parent `E_Sparent > 3` -> `M21_L400_SOURCE_K_SPLINE_LAYER_LOCALIZED_WITH_SCOPE`.

Any authority, null, schema, support, reconstruction or finite-value failure -> `M21_L400_SOURCE_FACTORIZATION_BLOCKED`.

## Interpretation ceiling

This gate localizes a numerical response within the scalar-E source path. It does not establish a CLASS defect, a production precision recommendation, a physical WDM scale or resonance, K1/K3/K4 promotion, or physical validation/falsification.
