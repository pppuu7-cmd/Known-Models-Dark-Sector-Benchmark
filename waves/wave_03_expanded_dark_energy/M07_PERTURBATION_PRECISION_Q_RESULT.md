# M07 perturbation-precision q-convergence audit — result

Date: 2026-09-09  
Status: **PASS_WITH_SCOPE**  
Run: `34359536106`  
Artifact: `w03-m07-perturbation-precision-q-audit`  
Artifact digest: `sha256:6cd91f54d94982425cbec2055c42f7e087458ae3a4e350796f9a661623240b5d`.

## Question

After quotient-aware field reflection, `q=lambda^2` is invariant under the redundant sign. Background `H(z)` already showed clean q scaling, while default-precision low-k `P(k,z)` did not. This audit asked whether the low-k discrepancy is perturbation numerical precision rather than physical q-nonlinearity.

Physical branch, shooting target and lambda values were held fixed. The audit changed only the perturbation numerical tier.

Baseline: CLASS defaults.

Tight tier frozen before output:

`tol_perturbations_integration = 1e-8`

`perturbations_sampling_stepsize = 0.01`.

Preregistered tight-tier q gates for lambda `.025` versus `.075`:
- relative q-vector difference <= `0.05`;
- q-vector angle <= `2 deg`.

## Results

For `q(lambda)=r_Delta(lambda)/lambda^2`:

| tier | q relative difference | q angle | norm q(.025) | norm q(.075) |
|---|---:|---:|---:|---:|
| baseline | `0.2184932813` | `12.505781 deg` | `0.1105023962` | `0.1166732567` |
| tight | `0.0005518893` | `0.027311 deg` | `0.1174847722` | `0.1174521158` |

Both preregistered tight-tier gates pass by large margins.

## Interpretation

The large baseline mismatch is not evidence against q-linearity. It is dominated by the default perturbation integration/sampling realization in the small-response regime.

The tight-tier result shows that the same physical branch produces essentially the same q-scaled low-k response at lambda .025 and .075:
- relative mismatch about `5.5e-4`;
- direction mismatch about `0.027 deg`.

Therefore the tight perturbation tier is justified as the response authority for the next local-order audit. This does not permit changing any previously frozen science threshold.

## Numerical-methodology consequence

A near-zero reference residual tests an exact origin but does not by itself bound numerical error on a small nonzero derivative/directional response. Local-response work must include a **nonzero precision-tier convergence test** whenever the inferred tangent/order is comparable to solver interpolation/integration structure.

This is distinct from the earlier shooting-conditioning problem:
- shooting precision controls the physical target point;
- perturbation precision controls the response vector at that point.

Both must be audited separately.

## Next hard task

Repeat the already-preregistered small-lambda order grid `{.005,.010,.020,.040}` at this independently validated tight perturbation tier while keeping the original order criteria unchanged.
