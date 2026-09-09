# W02-E3 — thermal WDM vs alternative small-scale suppression

Status: **BLOCKED_IMPLEMENTATION**  
Wave: W02 — Same-observable degeneracy attack  
Frozen DSIR authority: `e3276e2193f6a5200b541a194e3175356ae5a1c1`

## Question

Can the pinned M04 thermal-WDM high-k suppression response be distinguished from a different small-scale suppression mechanism on a valid common high-k response block?

## Available pinned WDM block

DSIR Exp050A provides a solver-native thermal-WDM high-k time atlas with:

- masses 2, 3 and 5 keV;
- `k = {0.1, 0.3, 1, 3, 10, 20} h/Mpc`;
- the seven standard DSIR redshifts;
- matched CDM reference bookkeeping;
- pinned official CLASS provenance.

Exp050B separately validates monotonic motion of the WDM cutoff scale under withheld masses within the WDM family.

## Comparator audit

The frozen C0-C6 DSIR atlas contains no second non-WDM dark-matter suppression family with a pinned response product on the same high-k grid and matched baseline conventions. Repository/provenance checks did not identify a frozen fuzzy/axion/SIDM-like comparator satisfying the Wave-02 prerequisites.

A comparator is not allowed to be introduced post hoc merely because it gives a convenient separation.

## Hard state

`BLOCKED_IMPLEMENTATION`

This state means:

- the WDM response itself is implemented and controlled;
- the pairwise adversarial question is scientifically well-posed;
- KMDSB currently lacks the second implementation needed to score the edge;
- the result is **not evidence that WDM is unique** and is **not a physical failure of any alternative theory**.

## Requirements to unblock E3

A future comparator must provide all of:

1. explicit physical model/family identity and parameter domain;
2. pinned solver/code provenance;
3. matched CDM/reference conventions or an explicit baseline map;
4. common high-k support covering a nontrivial overlap with `{0.1,0.3,1,3,10,20} h/Mpc`;
5. common or explicitly mapped redshift support;
6. no zero-imputation for unavailable nonlinear/high-k cells;
7. frozen discriminator before inspecting the new comparator output;
8. observation-space promotion only after a corresponding operator/covariance exists.

## Methodological lesson

Comparator coverage is itself part of experimental design. A future original dark-sector model must not be called distinctive merely because a competing mechanism has not yet been implemented in the same response coordinates.
