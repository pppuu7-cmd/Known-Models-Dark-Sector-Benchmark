# W04 M21 conditional l=400 k-support mapping v0.1

Frozen: 2026-09-15 while transfer-vs-harmonic run `34904313450` is non-terminal and before any of its transfer/integrand scientific values are inspected.

Provider remains `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Activation

This gate is **analysis-only** and may activate only if the terminal aggregate from run `34904313450` is input/null clean and has exactly one of:

- `M21_L400_SPIKE_PRESENT_IN_E_TRANSFER_KERNEL_WITH_SCOPE`;
- `M21_L400_SPIKE_EMERGES_IN_EE_INTEGRAND_WITH_SCOPE`.

It MUST NOT activate for BLOCKED, MIXED, or `...HARMONIC_ACCUMULATION...` outcomes.

No CLASS rerun is permitted. Reuse the immutable diagnostic tables of both A/B lane artifacts from the parent run.

## Active diagnostic quantity

- For transfer-kernel parent class: `X = Delta_E`.
- For EE-integrand parent class: `X = EE_integrand`.

Use l=400 only for the support map. Neighboring sparse l values remain controls inherited from the parent and are not used to choose a k window.

## Frozen common-k grid

For each lane use the reference-case native k nodes within the strict intersection of the k ranges of `ref,f2,f3,f4`, exactly as in the parent transfer-vs-harmonic protocol. Other cases are interpolated linearly in `log(k)` onto those reference nodes. At least 100 nodes are required.

## Frozen f3-specific excess density

Define response vectors

`r_c(k) = X_c(k) - X_ref(k)` for c in `{f2,f3,f4}`.

Define the non-negative f3-specific excess density

`W(k) = max( r_f3(k)^2 - max(r_f2(k)^2,r_f4(k)^2), 0 )`.

The cumulative support measure is the trapezoidal integral of W with respect to `ln(k)`. This weights equal logarithmic k intervals equally and introduces no chosen physical k window.

Require finite positive total excess integral. Otherwise classify the support map BLOCKED because the parent specificity cannot be represented by this frozen non-negative excess measure.

## Frozen support summaries

For each lane report the k values at cumulative excess fractions:

- `k05` = 5%;
- `k50` = 50%;
- `k95` = 95%.

Also report:

- support width `log10(k95/k05)`;
- k of maximum W;
- fraction of total excess within one factor of two of the maximum-W k;
- fraction of total excess below/above `k50` as an internal numerical check;
- direct comparison of A/B `k05,k50,k95`.

No narrow/broad threshold is defined post hoc.

## Frozen classification

- both lanes valid -> `M21_L400_K_SUPPORT_MAPPED_WITH_SCOPE`;
- either lane authority/table/common-grid/excess failure -> `M21_L400_K_SUPPORT_MAPPING_BLOCKED`.

The support coordinates are descriptive numerical localization, not a new physical scale claim.

## Interpretation ceiling

This gate identifies where in native k/q support the already-established l=400 numerical excess lives. It does not by itself identify the underlying Bessel/source interpolation cause, establish a provider defect, select production precision, promote K1/K3/K4, or physically validate/falsify mixed cold+warm dark matter.
