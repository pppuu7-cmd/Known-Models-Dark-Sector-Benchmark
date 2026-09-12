# W07 M40 Hořava local 2D response preregistration v0.1

## Motivation

The immutable M40 K2 path-geometry audit (run `34694383102`, artifact `10297569211`) shows that the successful K1 ladder spans only one joint `(Horava_xi, Horava_lambda, Horava_eta)` ray although the pinned EFTCAMB input exposes the three coefficients separately. K2 therefore remains open. The next admissible diagnostic is a prospectively frozen local two-direction response test.

## Provider and base point

Pinned provider: `EFTCAMB/EFTCAMB@16d9c4e9f85751e30efd0a53b177941713078904`.

Use the author-native Hořava mapping and exact include-path recovery already validated at K1. Base point is the successful `s01` K1 point:

- `Horava_xi = -1.0e-4`
- `Horava_lambda = +1.0e-4`
- `Horava_eta = 2.1e-3`

No other physical or stability setting may be changed.

## Frozen directions and stencil

Direction R (original radial K1 ray): parameterized by `q` with `(xi,lambda,eta)=(-0.001 q,+0.001 q,0.021 q)` around `q0=0.1`.

- coarse central step: `h_R=0.002`
- fine central step: `h_R=0.001`

Direction E (eta-only orthogonal coordinate at fixed xi/lambda):

- coarse central step: `h_E=4.2e-5`
- fine central step: `h_E=2.1e-5`

Run the base plus `R±coarse`, `R±fine`, `E±coarse`, `E±fine` using the exact pinned provider.

## Response vector

On the intersection of finite supports across every successful arm, concatenate:

1. CMB scalar Cl block normalized by the L2 norm of the base block;
2. matter P(k) block normalized by the L2 norm of the base block.

Central derivatives use `(plus-minus)/(2h)`.

## Frozen decision criteria

A direction is locally converged iff coarse-vs-fine central derivatives satisfy both:

- principal angle `<= 5 deg`;
- relative derivative-norm mismatch `<= 0.25`.

The two fine directions are response-distinct iff their principal angle is `>= 10 deg`.

Classifications:

- both directions converged and cross-angle passes: `M40_LOCAL_2D_RESPONSE_RANK_EVIDENCE`;
- either derivative convergence fails: `M40_LOCAL_2D_RESPONSE_DERIVATIVE_NOT_CONVERGED`;
- both converge but cross-angle fails: `M40_LOCAL_2D_RESPONSE_NEAR_COLLINEAR`;
- base/control fails: `M40_LOCAL_2D_RESPONSE_CONTROL_BLOCKED`;
- any non-base arm fails: `M40_LOCAL_2D_RESPONSE_PROVIDER_BLOCKED`.

## Scope guard

This diagnostic cannot promote K2 by itself. In all outcomes set `K2_promoted=false`, `physical_falsification=false`, and `complete_Horava_family_claim=false`. A positive rank result is only local response evidence in the pinned EFTCAMB representation and must later be combined with source-domain/quotient evidence before any canonical K2 promotion.
