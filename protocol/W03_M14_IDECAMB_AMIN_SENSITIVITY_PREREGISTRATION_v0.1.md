# W03 M14 IDECAMB initial-surface sensitivity preregistration v0.1

Date: 2026-09-10
Target: M14 coupled quintessence
Purpose: test whether the remaining source-scaled K4 angular failure is caused by a nonuniform beta->0 limit at the hard-coded early integration surface rather than by physical loss of differentiability.

## Frozen provider and model

- base: `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`
- overlay: `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`
- `Class_IDE=2`
- `UForm_CQ=1`
- `QForm_CQ=1`
- fixed `alpha_quint=0.02`
- external likelihoods disabled; theory-output mode only

The upstream coupled-quintessence Broyden update is retained unchanged in this diagnostic because the completed patched-control run showed that correcting it changes the K4 angle negligibly (`8.04172 deg` -> `8.04154 deg`) and all three shooting points already terminate after one iteration.

The already-audited high-precision `.quantity` serialization (`11ES25.15E3`) is used for every surface to avoid reintroducing known diagnostic rounding.

## Frozen beta grid

For every start surface:

`beta_cq = {0, 5e-8, 1e-7}`

No smaller-beta search is authorized.

## Diagnostic start-surface ladder

Run the same model with only the coupled-quintessence hard-coded

`amin = {1e-12, 1e-8, 1e-6, 1e-5}`.

`1e-12` reproduces the upstream start surface inside the same workflow and is the baseline for reference-drift measurements.

The later surfaces are diagnostic controls only. A pass at later `amin` is not a physically promotable model result because the early history has been truncated.

## Source-derived prior prediction

For the uncoupled power-law tracker at alpha=0.02,

`beta_star(a) = a^2 |dU/dphi|/rho_c(a) proportional to a^[(2-alpha)/(2+alpha)]`,

with exponent `0.9801980198019802`.

Using the previously measured `beta_star(1e-4)=7.813256771938583e-7`, the frozen prior predictions are approximately:

- `beta_star(1e-12)=1.1252471939903163e-14`;
- `beta_star(1e-8)=9.376484939207142e-11`;
- `beta_star(1e-6)=8.559258877595895e-9`;
- `beta_star(1e-5)=8.177750829217472e-8`.

For the fine step beta=5e-8, the corresponding beta/beta_star ratios are approximately:

- `4.4435e6` at `1e-12`;
- `5.3325e2` at `1e-8`;
- `5.8416` at `1e-6`;
- `0.6114` at `1e-5`.

Thus the ladder deliberately crosses from strongly coupling-dominated initial force balance to a surface where the fine beta step is below the source-derived crossover.

## Frozen response vector

Exactly the prior M14 vector:

- dln rho_de(a)
- dln rho_c(a)
- dln H(a)
- dw(a)
- qhat(a)
- dln TT(ell)
- dln EE(ell)
- dln PP(ell)

The exported diagnostic grid remains the provider's usual `a >= 1e-4`; no observable/output coordinate is redefined.

## Frozen K4 thresholds

For derivative vectors from h=5e-8 and 2h=1e-7:

- relative tangent-norm mismatch <= 0.10;
- tangent angle <= 3.0 deg.

K5 is not scientifically scored from any altered-`amin` diagnostic.

## Additional controls

For each start surface record:

- build and process exit codes;
- K4 mismatch and angle;
- fine-step response amplitude by channel;
- beta=0 reference drift relative to the `amin=1e-12` beta=0 output in the same workflow;
- output shapes and finiteness.

Reference drift is diagnostic: a later surface that materially changes the beta=0 control cannot be interpreted as isolating coupling sensitivity cleanly even if K4 passes.

## Predeclared decision rules

1. `SUPPORTS_NONUNIFORM_INITIAL_ASYMPTOTIC_CAUSE` if the `amin=1e-5` surface satisfies both frozen K4 thresholds while the `amin=1e-12` baseline fails the angle threshold, provided all cases execute and remain finite. This is causal diagnostic support, not physical model promotion.
2. `PARTIAL_SUPPORT_AMIN_TREND` if `amin=1e-5` still fails K4 but its tangent angle is less than half the `amin=1e-12` baseline angle and the sequence shows a systematic reduction as the predicted beta/beta_star ratio approaches/below unity.
3. `AMIN_SENSITIVITY_NOT_SUFFICIENT` if the `amin=1e-5` angle remains greater than or equal to half the baseline angle or the sequence lacks the predicted systematic reduction.
4. `DIAGNOSTIC_BLOCKED_REFERENCE_DRIFT` if the later start surfaces substantially corrupt the beta=0 reference/output domain so that the test no longer isolates initial-asymptotic sensitivity. No post-hoc physical threshold is attached to this label; all drift metrics must be reported.
5. Any build/execution/shape failure is implementation-blocked and cannot be interpreted as physical falsification.

No observational claim, K5 promotion, or M14 family falsification is authorized by this diagnostic.