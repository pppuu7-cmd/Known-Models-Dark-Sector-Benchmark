# W04 M21 l=400 scalar-E source factorization v0.1

Frozen: 2026-09-15 while serialization-recovery run `34907528331` is non-terminal and before its recovered classifier is known.

## Activation

This gate is authorized only if the frozen successor router receives one of:

- `M21_L400_TRANSFER_SPIKE_SOURCE_PROFILE_LOCALIZED_WITH_SCOPE`; or
- `M21_L400_TRANSFER_SPIKE_SOURCE_AND_RADIAL_MIXED_WITH_SCOPE`.

Otherwise the workflow must skip without CLASS execution.

Provider remains exactly `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

## Frozen parent geometry

Reuse without change:

- physical cases `ref,f2,f3,f4`;
- l = 400;
- layout `P400_ON_TAIL_OFF`;
- k support `[0.03030247505892471, 0.04401375054733766]` Mpc^-1;
- parent non-negative q-weight `W_j` from the terminal l=400 k-support map;
- all physical inputs and precision assignments.

## Exact source authority

On the exact provider, scalar E transfer type maps to perturbation source `index_tp_p`.

For scalar perturbations the source is

`S_E(k,tau) = sqrt(6) * g(tau) * P(k,tau)`

where `g` is the visibility function. Outside RSA, `P` is:

- in TCA: `5*s_l[2]*tca_shear_g/8`;
- after TCA: `(pol0_g + pol2_g + 2*s_l[2]*shear_g)/8`.

Under RSA the scalar polarization source is zero.

## Output-only instrumentation

Patch only `source/perturbations.c` at the already-existing scalar polarization-source assignment. The patch must not alter any CLASS state, approximation switch, source value, precision, integration order, grid, or return value.

For scalar modes with k inside the frozen support, dump one row each time the native scalar E source is stored, containing at least:

- k;
- conformal time tau;
- visibility `g`;
- native `P`;
- reconstructed `sqrt(6)*g*P`;
- native stored scalar-E source;
- TCA state;
- RSA state;
- active shear quantity;
- `pol0_g` and `pol2_g` when allocated/active, with explicit validity flags otherwise.

Diagnostic execution must set `OMP_NUM_THREADS=1`, because the exact provider's `Tools::TaskSystem` uses that environment variable to select its `std::thread` worker count.

## Non-interference gates

Each of `ref,f2,f3,f4` must independently satisfy:

- CLASS return code zero;
- exact provider pin;
- only the output-only diagnostic source file modified;
- full `cl.dat` normalized L2 difference from the immutable matching parent <= `1e-12`;
- every diagnostic row schema-valid;
- native stored source and `sqrt(6)*g*P` relative reconstruction difference <= `1e-10` wherever the native source magnitude exceeds `1e-300`.

Any failure -> `M21_L400_SOURCE_FACTORIZATION_BLOCKED`.

## Frozen comparison

Use only q/k nodes belonging to the immutable parent l=400 support. In flat geometry k=q. Pair/interpolate diagnostic profiles onto the same physical k and common tau/u support used by the clean transfer-convolution parent; do not choose new k points after inspection.

For X in `{G,P,S}` define the same normalized profile distance used by the parent convolution protocol and the same support-weighted amplitude over immutable `W_j`. Define specificity

`E_X = A_X(f3) / max(A_X(f2),A_X(f4),1e-300)`.

Reuse the existing specificity boundary `E > 3`.

## Frozen classification

- `E_G > 3`, `E_P <= 3` -> `M21_L400_SOURCE_VISIBILITY_LOCALIZED_WITH_SCOPE`
- `E_G <= 3`, `E_P > 3` -> `M21_L400_SOURCE_POLARIZATION_MOMENT_LOCALIZED_WITH_SCOPE`
- `E_G > 3`, `E_P > 3` -> `M21_L400_SOURCE_VISIBILITY_AND_POLARIZATION_MIXED_WITH_SCOPE`
- `E_G <= 3`, `E_P <= 3`, but `E_S > 3` -> `M21_L400_SOURCE_MULTIPLICATIVE_INTERACTION_WITH_SCOPE`
- otherwise -> `M21_L400_SOURCE_FACTORIZATION_NOT_LOCALIZED_WITH_SCOPE`

TCA/RSA state transitions and individual photon multipoles are report-only in this gate and may authorize a later separately preregistered decomposition; they do not change this classifier.

## Claim ceiling

This gate localizes a numerical scalar-E source mechanism. It does not establish a CLASS defect, a physical WDM scale, a production precision/threading setting, K1/K3/K4 promotion, or physical validation/falsification.
