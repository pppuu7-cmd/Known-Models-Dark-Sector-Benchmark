# M21 l=400 transfer-excess support vs scalar-E neglect geometry — 2026-09-15

Provider: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Parent numerical authority:
`waves/wave_04_dark_matter/M21_L400_K_SUPPORT_MAPPING_TERMINAL.json`.

This is an exact-source geometry comparison, not a parameter scan.

## Frozen excess support

The parent transfer-localized excess has identical A/B support:

- k05 = `0.03030247505892471` Mpc^-1;
- k50 = `0.03182575113595699` Mpc^-1;
- k95 = `0.04401375054733766` Mpc^-1;
- k_peak = `0.030913138222910114` Mpc^-1;
- 99.7189249206765% of the frozen excess measure lies within a factor two of k_peak.

The factor-two interval has upper edge

`2*k_peak = 0.06182627644582023` Mpc^-1.

## Exact scalar-E neglect condition

Exact `source/transfer.c` checks scalar E with

`l < (k - ppr->transfer_neglect_delta_k_S_e) * ra_rec`.

The active `cl_permille.pre` sets

`transfer_neglect_delta_k_S_e = 0.13`.

For recombination distance `ra_rec > 0` and direct multipole `l=400 > 0`, this inequality cannot be true for any `k <= 0.13`, because its right-hand side is non-positive while its left-hand side is positive.

Therefore the scalar-E neglect branch is provably inactive throughout:

- the entire 5--95% parent support interval;
- the entire factor-two interval around k_peak containing 99.7189% of the frozen excess measure.

This conclusion does not require a numerical value of `ra_rec`; the positivity of `ra_rec` is sufficient.

## Interpretation

The active scalar-E neglect cutoff is not a viable **direct dominant-support trigger** for the established l=400 transfer spike. This is consistent with the earlier full-G3 precision bundle being insufficient to remove the excursion.

The statement is intentionally scoped: it does not prove that the cutoff has zero indirect effect in all k tails, does not identify the actual cause, and does not establish a CLASS bug.

The high-information next layer is the already-preregistered source/radial/convolution decomposition inside `transfer_integrate()` over the frozen k05--k95 support.
