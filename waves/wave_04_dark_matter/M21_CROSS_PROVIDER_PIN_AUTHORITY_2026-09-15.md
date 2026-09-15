# M21 adjacent provider-pin authority — 2026-09-15

This note was frozen before the cross-cosmology/provider regression produced any scientific cell result.

## Immutable pins

- P0: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`
- P1: `lesgourg/class_public@64bbab707faf4de4779a9e04edd180fef18d98fa`

P1 was the public `master` HEAD observed on 2026-09-15. GitHub comparison reports P1 8 commits ahead of P0 with P0 as the merge base. The intervening provider changes include substantial perturbation/CMB work and modifications in `source/transfer.c`, `source/thermodynamics.c`, precision headers and related modules, so the pins are not merely duplicate labels.

## Mechanism source identity

Direct exact-pin source inspection on P1 confirms that it retains:

- `pth->angular_rescaling=pth->ra_rec/(pba->conformal_age-pth->tau_rec);`
- late-source outer predicate `l > ppr->transfer_neglect_late_source*ptr->angular_rescaling`.

Thus the structural mechanism identified on P0 remains present in P1 and is eligible for a prospective version regression.

## Scope

This note establishes provider identities and source comparability only. It makes no statement about numerical ULP signs, counterfactual response, relative accuracy, or whether either pin contains a defect.