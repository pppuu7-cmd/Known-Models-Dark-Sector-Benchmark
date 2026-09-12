# W07 M40 xi/lambda coordinate-response preregistration v0.1

## Motivation

The pinned EFTCAMB Hořava input exposes `Horava_xi`, `Horava_lambda`, and `Horava_eta` as separate native inputs. The already-completed local 2D test (run `34695408204`, artifact `10298444789`) found that the prospectively tested eta-only derivative is numerically converged but nearly collinear with the original radial K1 direction (`3.877231 deg < 10 deg`). That result is immutable and remains negative for local rank-2 evidence.

To avoid post-hoc coordinate cherry-picking, this protocol prospectively tests **both remaining native coordinate axes**, xi-only and lambda-only, in one parallel batch with identical relative step structure. No axis is selected after looking at its result.

## Provider and immutable radial authority

Pinned provider: `EFTCAMB/EFTCAMB@16d9c4e9f85751e30efd0a53b177941713078904`.

Immutable radial-response authority: run `34695408204`, artifact `10298444789`.

Base point remains exactly:

- `Horava_xi = -1.0e-4`
- `Horava_lambda = +1.0e-4`
- `Horava_eta = 2.1e-3`

The native stability flags and all other provider settings remain unchanged.

## Frozen coordinate stencils

For each coordinate axis independently, keep the other two Hořava parameters fixed at the base point.

### xi-only axis

- coarse symmetric delta: `2.0e-6`
- fine symmetric delta: `1.0e-6`

### lambda-only axis

- coarse symmetric delta: `2.0e-6`
- fine symmetric delta: `1.0e-6`

Each job also reruns the exact base as a deterministic control. The new base must agree with the immutable base response within normalized L2 distance `D <= 1e-8` in both CMB and P(k); otherwise classify control blocked and do not interpret the coordinate response.

## Response vector and frozen thresholds

Use the intersection of finite support between the immutable radial arms, the new base, and the four coordinate arms. Concatenate the CMB scalar-Cl and matter-P(k) derivative blocks, each normalized by the new base L2 norm.

A coordinate derivative is converged iff coarse-vs-fine central derivatives satisfy:

- principal angle `<= 5 deg`;
- relative norm mismatch `<= 0.25`.

Compare the converged fine coordinate derivative to the **immutable fine radial derivative** from run `34695408204`. It is response-distinct iff principal angle `>= 10 deg`.

## Per-axis classifications

- `M40_<AXIS>_LOCAL_RESPONSE_DISTINCT_EVIDENCE`: control passes, derivative converges, radial-vs-axis angle >=10 deg;
- `M40_<AXIS>_LOCAL_RESPONSE_NEAR_COLLINEAR`: control passes, derivative converges, radial-vs-axis angle <10 deg;
- `M40_<AXIS>_LOCAL_RESPONSE_DERIVATIVE_NOT_CONVERGED`: coordinate derivative fails frozen convergence;
- `M40_<AXIS>_LOCAL_RESPONSE_PROVIDER_BLOCKED`: any coordinate arm fails;
- `M40_<AXIS>_LOCAL_RESPONSE_CONTROL_BLOCKED`: provider/base provenance or immutable-base identity fails.

## Aggregate interpretation

This batch does not promote K2. If at least one remaining native axis gives converged response-distinct evidence, a later immutable synthesis may consider K2=PARTIAL after source/quotient checks. If both axes are converged and near-collinear with the radial response, the local observable response at this base is effectively rank-1 across all three exposed coordinate directions under the frozen response operator.

Always set `K2_promoted=false`, `physical_falsification=false`, and `complete_Horava_family_claim=false`. No threshold changes or additional coordinate retuning are authorized by this protocol.
