# W04 M21 l=400 support-domain extension audit v0.1

Frozen: 2026-09-15 after terminal recovery `34907528331` established `M21_L400_TRANSFER_SPIKE_CONVOLUTION_ACCUMULATION_WITH_SCOPE`, and before any authoritative support-domain audit execution.

A local implementation-QA inspection of the already-authoritative clean recovery artifact showed that the four cases have substantially different native integration support lengths even though all common-overlap profile specificities are below the frozen threshold. This protocol is a new prospective follow-up; it does not modify the parent convolution or signed-cancellation classifiers.

## Inputs

Use only clean recovered case artifacts from run `34907528331`. No CLASS execution is authorized.

For each common accepted q block and case c, use native rows containing

`u=tau0-tau`, signed weighted contribution `C=S*R*w`, total transfer `T`, and edge correction.

Retain all parent integrity requirements: exact provider, authority-clean cases, same q set, same-q k relative difference <= `1e-6`, consecutive native tau indices, and transfer reconstruction relative error <= `1e-10`.

## Frozen common-support construction

For each q define the strict four-case common-u interval:

`u_lo(q) = max_c min_i u_c,i`

`u_hi(q) = min_c max_i u_c,i`.

For each case define native signed contributions outside this common interval, without interpolation or reordering:

`X_low,c(q)  = sum_{i: u_c,i < u_lo} C_c,i`

`X_high,c(q) = sum_{i: u_c,i > u_hi} C_c,i`

`X_all,c = X_low,c + X_high,c`.

Use differences from reference:

`x_region,c = X_region,c - X_region,ref`.

## Frozen parent target

For total transfer differences

`r_c(q)=T_c(q)-T_ref(q)`, c in `{f2,f3,f4}`,

define exactly the parent f3-specific excess power

`W_T(q)=max(r_f3^2-max(r_f2^2,r_f4^2),0)`.

Require `sum_q W_T(q)>0`.

For each region in `{low,high,all}`, define candidate excess power

`W_X,region(q)=max(x_region,f3^2-max(x_region,f2^2,x_region,f4^2),0)`

and candidate amplitude ratio

`R_X,region=sqrt(sum W_X,region / sum W_T)`.

## Frozen counterfactual

For each non-reference case construct the exact additive counterfactual

`T_cf,region,c(q)=T_c(q)-x_region,c(q)`.

Reference is unchanged. Recompute the same f3-specific excess power `W_cf,region(q)` from the counterfactual total transfers.

Report

`R_resid,region=sqrt(sum W_cf,region / sum W_T)`

and

`reduction_fraction_region = 1 - sum W_cf,region / sum W_T`.

No fitted threshold is introduced.

## Frozen classification

First require all integrity gates and positive parent excess, otherwise
`M21_L400_SUPPORT_DOMAIN_EXTENSION_BLOCKED`.

Then compare the exact counterfactual residual powers:

- if `sum W_cf,low < sum W_T` and `sum W_cf,low <= sum W_cf,high` and `sum W_X,low >= sum W_cf,low` -> `M21_L400_LOWER_U_SUPPORT_EXTENSION_DOMINANT_WITH_SCOPE`
- else if `sum W_cf,high < sum W_T` and `sum W_cf,high < sum W_cf,low` and `sum W_X,high >= sum W_cf,high` -> `M21_L400_UPPER_U_SUPPORT_EXTENSION_DOMINANT_WITH_SCOPE`
- else if `sum W_cf,all < sum W_T` and `sum W_X,all >= sum W_cf,all` -> `M21_L400_NONCOMMON_SUPPORT_MIXED_DOMINANT_WITH_SCOPE`
- else if `sum W_cf,all < sum W_T` -> `M21_L400_NONCOMMON_SUPPORT_PARTIAL_WITH_SCOPE`
- otherwise -> `M21_L400_NONCOMMON_SUPPORT_NOT_EXPLANATORY_WITH_SCOPE`.

These comparisons use only algebraic dominance between candidate and residual powers; no post-hoc numerical cutoff is fitted.

## Required report-only geometry

For every q report:
- row count per case;
- min/max u per case;
- `u_lo`, `u_hi`;
- low/high/all native signed contribution per case;
- total transfer differences;
- low/high/all candidate and counterfactual powers.

Also report q-weighted distributions of row-count excess and endpoint displacement but do not use them to change classification.

## Claim ceiling

This gate can establish that case-specific native integration-domain extension is numerically sufficient/dominant for the frozen l=400 transfer excess. It does not yet identify the provider condition causing the endpoint difference, establish a CLASS defect, recommend production precision settings, promote K1/K3/K4, or physically validate/falsify the model.
