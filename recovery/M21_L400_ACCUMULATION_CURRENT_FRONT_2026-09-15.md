# M21 l=400 accumulation current front — 2026-09-15

## Authoritative terminal parent

Recovery run `34907528331` is terminal success at head `2338fb5a4ee92c8b94a1583089465e42d164f439`.

Aggregate artifact:
- id `10373467959`
- digest `sha256:ba86f18e1a57f4b8dd16652976e0d015fb912fdaaca5848685476bf64017883e`
- classification `M21_L400_TRANSFER_SPIKE_CONVOLUTION_ACCUMULATION_WITH_SCOPE`.

All frozen integrity gates passed. The support contains 73 q nodes spanning `k=0.03030247505892471..0.04401375054733766 Mpc^-1`.

Frozen specificity values are:
- source S: `1.2846611791553475`
- radial R: `1.1273489553368872`
- pointwise S*R: `1.2375373459930303`
- signed weighted contribution S*R*w: `1.549367287605997`
- threshold: `3.0`.

Therefore no standalone profile reaches the established f3-specificity threshold; specificity appears only after the full signed tau accumulation at this decomposition level.

## Current gate

Frozen successor router run `34908508458` is the formal authority for the next branch. Its preregistered routing table maps the terminal parent classification above only to `CONVOLUTION_SIGN_CANCELLATION`.

Do not execute source-factorization or radial-geometry branches unless the terminal router artifact explicitly authorizes them. Prepared code/protocols are not authorization.

When router `34908508458` becomes terminal, allow `.github/workflows/w04-m21-l400-analysis-successors-v01.yml` to read its artifact. For the current parent, only the `convolution` job should execute; `radial` must be skipped.

The convolution analysis is analysis-only on clean recovered artifacts; it must not rerun CLASS or alter physical inputs, grids, thresholds or provider state.

## Next after convolution result

Use `protocol/W04_M21_L400_CONVOLUTION_ACCUMULATION_SUCCESSOR_ROUTER_v0.1.md`, frozen before the convolution result, to choose the subsequent mechanism gate.

## Claim ceiling

K1/K3/K4 remain unpromoted. No physical falsification. Current results localize a numerical mechanism in the CLASS scalar-E transfer path only.
