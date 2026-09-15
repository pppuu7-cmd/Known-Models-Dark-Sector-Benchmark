# W04 M21 l=400 support-domain decomposition v0.1

Status: prospectively frozen before execution.

## Authority and activation
Authorized only after immutable run `34972611076` / artifact `10398186622` classifies `M21_L400_F3_NATIVE_GRID_SUPPORT_AND_DENSITY_CHANGE_WITH_SCOPE`. Use that immutable topology result plus the immutable convolution component artifacts from recovery run `34907528331`. No CLASS rerun, interpolation, zero-imputation, physics retuning, threshold retuning, or native-grid alignment is allowed.

## Question
Determine whether the f3-only extension of the native convolution support is sufficient, in absolute transfer amplitude, to account for a substantial part of the f3-vs-reference l=400 transfer excess. This is a solver-layer representation diagnostic, not a physical model test.

## Frozen construction
For every common q, read each case on its own native grid. Require authority-clean metadata, identical q sets, consecutive native index 0..N-1, finite strictly monotone u, stored `index_tau_max=N-1`, and transfer reconstruction `sum(C)+edge` agreeing with stored total transfer to relative error <=1e-10. Here `C` is stored column 7 (zero-based index 7), edge is column 9, and stored total transfer is column 8, as in the already-frozen convolution decomposition.

Define the reference support interval independently at each q as `[min(u_ref),max(u_ref)]`. Define f3 extended-support rows as native f3 rows with u strictly outside that closed interval. Do not interpolate any quantity. Let `X_ext(q)=sum C_f3` over those rows. Let `Delta(q)=T_f3(q)-T_ref(q)`, where T is the reconstructed total transfer. Define the exact removal counterfactual `Delta_cf(q)=T_f3(q)-X_ext(q)-T_ref(q)`. The edge term is unchanged.

Across the common q set use an equal-q Euclidean norm, fixed prospectively because this gate asks only whether the newly discovered support domain itself carries the transfer excess and does not import a new observational weighting. Define `R_cf=||Delta_cf||/max(||Delta||,1e-300)` and `R_ext=||X_ext||/max(||Delta||,1e-300)`. Also report the fraction of q with nonempty f3 extended support and whether f2/f4 have any rows outside the reference support.

## Frozen classification
Any authority, q-set, native-index, monotonicity, reconstruction, or non-finite failure -> `M21_L400_SUPPORT_DOMAIN_DECOMPOSITION_BLOCKED`.

If f3 extended support is nonempty for >=90% of q and `R_cf<=0.5` -> `M21_L400_F3_EXTENDED_SUPPORT_AMPLITUDE_SUFFICIENT_WITH_SCOPE`.

If f3 extended support is nonempty for >=90% of q and `R_cf>0.5` -> `M21_L400_F3_EXTENDED_SUPPORT_AMPLITUDE_INSUFFICIENT_WITH_SCOPE`.

Otherwise -> `M21_L400_F3_EXTENDED_SUPPORT_NOT_SYSTEMATIC_WITH_SCOPE`.

`R_ext` is diagnostic only and does not override the counterfactual classification.

## Guardrails and successor
No K1/K3/K4 promotion, physical falsification, or CLASS-defect claim is permitted. An amplitude-sufficient outcome authorizes a prospectively frozen support-trigger/grid-generation causal diagnostic. An amplitude-insufficient outcome authorizes a prospectively frozen overlap-domain density/arithmetic decomposition while preserving the support change as a representation fact. A non-systematic outcome requires cross-q topology analysis first.