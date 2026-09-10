# M14 coupled-quintessence radiation-era asymptotic note

Date: 2026-09-10
Scope: diagnostic derivation for the pinned IDECAMB coupled-quintessence implementation; not a promoted replacement provider.

## Source equations

For `UForm_CQ=1` and `QForm_CQ=1`, the pinned source uses

- `V(phi) proportional to phi^(-alpha)`;
- `rho_c(source) = grhoc/a * exp[-beta(phi-phi0)]`;
- `Q_source = beta * rho_c(source) * phi'`;
- `y2 = a^2 phi'`;
- `d y2/d a = [-a^2 V_,phi + Q_source/phi'] * a/Hconf`.

At sufficiently early radiation domination,

`Hconf ~= A_r/a`,

where `A_r = sqrt[(grhog+grhornomass)/3]`, equal to the radiation normalization represented by `adotrad` in the source initial tracker.

For beta small enough that the exponential mass factor is locally close to unity but nonzero,

`Q_source/phi' ~= beta grhoc/a`.

## Coupling-dominated early particular solution

If the coupling term dominates over the potential-gradient term at the initial surface, then

`d(a^2 phi')/da ~= (beta grhoc/a) * a/(A_r/a)`

and therefore

`d(a^2 phi')/da ~= beta grhoc a/A_r`.

Integrating the regular particular branch gives

`a^2 phi' ~= beta grhoc a^2/(2 A_r)`,

so

`phi' ~= beta grhoc/(2 A_r)`

and, because `dphi/da = phi'/(a Hconf) ~= phi'/A_r`,

`phi(a) ~= phi_* + beta grhoc a/(2 A_r^2)`.

If the regular branch is chosen with vanishing integration constant at the singular origin, the leading field behavior is therefore

`phi proportional to beta a`,

not the uncoupled inverse-power tracker

`phi proportional to a^[4/(2+alpha)]`.

At the M14 anchor `alpha=0.02`, the uncoupled exponent is about `1.9802`, whereas the coupling-dominated particular branch is linear in `a`.

## Consequence

This derivation makes the nonuniformity concrete. For every fixed finite `a>0`, beta->0 removes the coupling. But at a fixed extremely early source surface the term `beta rho_c` grows faster toward the origin than the uncoupled tracker restoring force. Therefore a beta-independent uncoupled tracker cannot be assumed to be a uniformly valid asymptotic initial condition for all nonzero beta.

This does **not** prove that the simple coupling-dominated particular solution above is the correct complete cosmological initial condition: the homogeneous mode, potential term, mass-factor feedback, radiation/matter composition, and perturbation initial conditions must all be treated consistently. It does prove that the current source initial condition requires a uniform-asymptotic validation before a beta finite-difference K4 failure can be interpreted physically.

## Literature consistency

The broader coupled-quintessence literature independently establishes that direct dark-sector coupling creates early scaling/attractor behavior absent in uncoupled quintessence (e.g. Amendola, arXiv:astro-ph/9908023) and that inverse-power/Ratra-Peebles coupled models are routinely evolved with the interaction included in the background dynamics (e.g. Pettorino & Baccigalupi, arXiv:0802.1086). These references motivate, but do not substitute for, the source-specific derivation and numerical control above.

## Next validation requirement

Before implementing a new coupled initial condition in KMDSB, derive it from the full pinned background equations with a controlled asymptotic expansion and validate it by overlap matching against direct numerical integration from multiple start surfaces. Any such implementation must be labelled an independent KMDSB verification implementation, not silently substituted for the upstream provider.