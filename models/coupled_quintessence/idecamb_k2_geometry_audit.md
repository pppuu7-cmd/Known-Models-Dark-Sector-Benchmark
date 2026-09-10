# M14 IDECAMB K2 physical geometry audit

Updated: 2026-09-10
Status: `K2_PASS_WITH_SCOPE_ONE_SIDED_BETA`

## Pinned provider

- `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`
- `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`

## Source geometry

For the only implemented coupled-quintessence branch in the pinned provider (`Class_IDE=2`, `UForm_CQ=1`, `QForm_CQ=1`),

- the potential is inverse power law, `U(phi) proportional phi^(-alpha)` with author parameter `alpha_quint`;
- the CDM coupling is exponential, with `rho_c(a,phi) proportional a^-3 exp[-beta(phi-phi0)]`;
- energy transfer is proportional to `beta rho_c phi'`;
- `beta=0` is the exact interaction-off boundary already validated by the prospectively withheld K1 invariant gate.

A formal simultaneous `phi -> -phi`, `beta -> -beta` cannot be used as a quotient identification while holding this provider branch fixed: the inverse-power potential and its initial-condition construction select the positive-field branch, and for generic non-integer positive `alpha` the reflected field is not the same real-valued model branch.

Thus source algebra does not identify `+beta` and `-beta` as the same point.

## Provider-supported domain

The exact tracked author `test_ide.ini` declares

`param[beta_cq] = 0.01 0 0.15 0.05 0.05`.

KMDSB therefore treats this pinned implementation's validated local physical domain conservatively as the **one-sided tangent cone**

`q_beta = beta_cq >= 0`, reference `q_beta=0`.

This does not claim that negative coupled-quintessence couplings are impossible in the broader literature; it only refuses to extend the pinned provider beyond its author-declared tested domain without separate provenance/stability validation.

## K2 verdict

`PASS_WITH_SCOPE_ONE_SIDED_BETA`.

- coordinate: `q_beta = beta_cq`;
- local reference: `q_beta=0`;
- allowed derivative: right derivative only;
- no `beta^2` quotient;
- negative-beta response is outside the current provider-supported benchmark domain and is masked, not imputed.

## Next gate

Prospectively test right-sided local convergence using two positive steps at a fixed scalar anchor, with the already validated theory-only output route. K4 must pass before any K5 rank/response promotion. A failure of the chosen step pair is a local numerical/linearization gate failure, not physical falsification of M14.
