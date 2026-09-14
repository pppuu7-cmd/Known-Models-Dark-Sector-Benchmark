# W04 M21 l=400 knot propagation diagnostic v0.1

Frozen: 2026-09-15 after terminal run `34897465426` classified `M21_L_GRID_KNOT_VALUES_CARRY_L400_SIGNATURE_WITH_SCOPE`, and after terminal direct-CMB-source run `34897602278` classified `M21_CMB_BRANCH_NOT_LOCALIZED_IN_DIRECT_CMB_SOURCES`. No result from this diagnostic was inspected before freezing this protocol.

This is analysis-only and reuses immutable four-lane artifacts from parent run `34887488405`; no CLASS rerun and no physics retuning.

## Question
Does the HIGH EE excursion in l=400-containing sparse-l grids come primarily from the l=400 knot value itself, or does l=400 grid membership alter C_l values at other sparse knots as well?

## Frozen authority
Provider `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`; parent factorial classification `M21_L_GRID_PHASE_L400_SIGNATURE_SUPPORTED_WITH_SCOPE`; knot-only child classification `M21_L_GRID_KNOT_VALUES_CARRY_L400_SIGNATURE_WITH_SCOPE`.

Immutable parent lane artifacts: P400_ON_TAIL_OFF `10365592822`; P400_EVEN_TAIL_OFF `10365598517`; P400_OFF_TAIL_OFF `10365669355`; P400_OFF_TAIL_ON `10366295676`.

## Two independent frozen pair lanes
A: HIGH=`P400_ON_TAIL_OFF`, CALM=`P400_OFF_TAIL_OFF`.
B: HIGH=`P400_EVEN_TAIL_OFF`, CALM=`P400_OFF_TAIL_OFF`.

For each lane regenerate its exact sparse-l sequence from immutable `(l_logstep,l_linstep)` exactly as in the knot-only protocol and require exact manifest agreement, provider pin, all four case rc=0 and cross-case ini identity.

For EE define d_c(l)=C_c(l)-C_ref(l) for c=f2,f3,f4. For any selected l-set S define E(S)=||d_f3||_2/max(||d_f2||_2,||d_f4||_2,1e-300).

For each pair report:
1. HIGH full sparse-knot E;
2. HIGH E after removing exactly l=400 from its sparse set;
3. the exact intersection S_common of HIGH and CALM sparse-knot sets with l=400 excluded, and E_high_common / E_calm_common on that identical l support;
4. the same quantities restricted to the predeclared localization band 400<=l<=800.

Frozen state boundary: HIGH iff E>3, CALM otherwise.

## Frozen classifier
`M21_L400_GRID_MEMBERSHIP_PROPAGATES_TO_OTHER_KNOT_VALUES_WITH_SCOPE` iff for both pair lanes: (a) HIGH remains HIGH after removing l=400, and (b) on identical common sparse-knot support HIGH remains HIGH while CALM remains CALM, either on the full support or on the 400--800 band.

`M21_L400_SINGLE_KNOT_VALUE_SUFFICIENT_FOR_HIGH_STATE_WITH_SCOPE` iff for both pair lanes removing l=400 makes HIGH CALM and the identical common-support HIGH/CALM contrast is absent.

Otherwise classify `M21_L400_KNOT_INFLUENCE_MIXED_WITH_SCOPE`.

Any authority/list/table failure -> `M21_L400_KNOT_PROPAGATION_DIAGNOSTIC_BLOCKED`.

## Interpretation ceiling
This diagnostic localizes a numerical mechanism only. It does not establish a CLASS bug, a converged production precision, K1/K3/K4 promotion, or physical falsification of mixed cold+warm dark matter. No post-hoc threshold changes are allowed.