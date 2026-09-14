# W04 M21 l=400 scalar-E radial-kernel geometry audit v0.1

Frozen: 2026-09-15 while serialization-recovery run `34907528331` is non-terminal and before its recovered classifier is known.

## Activation

Authorized only if the frozen successor router receives:

- `M21_L400_TRANSFER_SPIKE_RADIAL_KERNEL_LOCALIZED_WITH_SCOPE`; or
- `M21_L400_TRANSFER_SPIKE_SOURCE_AND_RADIAL_MIXED_WITH_SCOPE`.

Otherwise skip without CLASS execution.

## Exact provider authority

Provider remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

For scalar E, the transfer module selects `SCALAR_POLARISATION_E`. On the frozen M21 cosmology `Omega_k=0`, hence `K=0`, `sgnK=0` and the exact radial-coordinate setup gives

- `chi = k * (tau0-tau)`;
- `cscKgen = 1/chi`;
- `rescale_argument = 1`;
- `rescale_amplitude = 1` and therefore `rescale_function = 1`.

The scalar-E radial function is therefore

`R_l(x) = F_l * Phi_l(x) / x^2`,

with fixed `l=400`, fixed prefactor

`F_l = sqrt(3/8*(l+2)*(l+1)*l*(l-1))`,

and `Phi_l` supplied by the exact flat hyperspherical/Bessel interpolation structure.

Thus there is no dark-sector state variable inside the radial formula itself. Case dependence can enter only through the sampled physical coordinate `x=k(tau0-tau)`, support/endpoint geometry, or numerical interpolation state.

## Frozen execution

This is analysis-only on the clean recovered convolution diagnostics. No CLASS rerun is authorized by this gate.

Reuse unchanged:

- cases `ref,f2,f3,f4`;
- l=400;
- immutable parent q-weight `W_j`;
- frozen support `[0.03030247505892471,0.04401375054733766]` Mpc^-1;
- only q blocks that passed the parent reconstruction and same-q geometry integrity gates.

## Frozen comparisons

For each common q block construct two comparisons of the dumped native radial profile:

1. **u comparison**: the existing parent comparison on common `u=tau0-tau` nodes.
2. **x comparison**: transform each native row to `x=k*u`, restrict to strict four-case overlap in x, and linearly interpolate all non-reference radial profiles onto the retained reference x nodes.

Use the same normalized L2 profile distance, immutable `W_j` support weighting, and specificity definition as the parent:

`E_R = A_R(f3)/max(A_R(f2),A_R(f4),1e-300)`.

Reuse the established boundary `E>3`.

Also report without changing classification:

- maximum same-q relative k mismatch;
- common-x support fraction;
- endpoint/index_tau_max differences;
- direct reconstruction of `x=k*u` for every row;
- the ratio of common-x to common-u radial distances.

## Frozen classification

- parent/common-u `E_R>3` and common-x `E_R<=3` -> `M21_L400_RADIAL_COORDINATE_GEOMETRY_LOCALIZED_WITH_SCOPE`
- common-x `E_R>3` -> `M21_L400_RADIAL_INTERPOLATOR_OR_ENDPOINT_STATE_LOCALIZED_WITH_SCOPE`
- common-u `E_R<=3` in the recovered clean artifact -> `M21_L400_RADIAL_PARENT_SIGNAL_NOT_REPRODUCED_WITH_SCOPE`
- any malformed/non-bijective/common-support/integrity failure -> `M21_L400_RADIAL_GEOMETRY_AUDIT_BLOCKED`

A common-x residual does not by itself establish a Bessel/interpolator defect; it only authorizes a later separately preregistered exact-interpolator audit.

## Claim ceiling

No K1/K3/K4 promotion, no production precision recommendation, no CLASS defect claim, and no physical validation/falsification.
