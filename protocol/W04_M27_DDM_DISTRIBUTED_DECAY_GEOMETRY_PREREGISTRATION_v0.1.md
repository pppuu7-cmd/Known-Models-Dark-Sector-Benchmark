# W04 M27 Dynamical Dark Matter distributed-decay geometry preregistration v0.1

## Scientific role

M27 represents Dynamical Dark Matter (DDM): an ensemble of metastable dark-sector constituents whose masses, lifetimes/decay widths, and abundances are balanced across the ensemble. This first benchmark is theory-level and tests the defining distributed temporal response before any Boltzmann/likelihood implementation.

Literature basis:

- Dienes & Thomas, arXiv:1106.4546: DDM replaces component-by-component hyperstability with an ensemble-level balancing of decay widths against cosmological abundances and produces non-trivial time dependence of the total dark-matter abundance.
- DDM review parameterization summarized in arXiv:1806.07396: `m_n = m_0 + Delta_m n^delta` and `Gamma_n = Gamma_0 (m_n/m_0)^y`; benchmark mass-spectrum exponents delta=1/2,1,2 occur in explicit constructions.
- DDM abundance studies commonly parameterize ensemble abundances by a mass scaling `Omega_n propto m_n^gamma`, with viable balancing requiring abundances to fall as widths rise over the relevant ensemble portion.

This benchmark is a generic DDM scaling-family test, not an author-code reproduction.

## Frozen ensemble family

Use dimensionless units `m_0=1`, `Gamma_0=1`, `Delta_m=0.25`, and `N=64` constituents indexed n=0..63.

Independent benchmark branches:

- `delta in {0.5, 1, 2}`
- `y in {1, 2, 3}`
- abundance exponent fixed prospectively to `gamma=-y`, providing an explicit inverse lifetime-abundance balancing ray.

Thus nine `(delta,y)` branches SHOULD run concurrently.

For each branch:

`m_n = 1 + 0.25 n^delta`

`Gamma_n = m_n^y`

`w_n = m_n^gamma / sum_j m_j^gamma`

where `sum_n w_n = 1` at t=0.

## Frozen temporal observables

On a common logarithmic time grid `t Gamma_0 in [1e-4,1e4]` with 20001 points calculate:

- surviving comoving dark-matter fraction `S(t)=sum_n w_n exp(-Gamma_n t)`;
- decay-injection kernel `J(t)=sum_n w_n Gamma_n exp(-Gamma_n t)`;
- instantaneous effective decay rate `Gamma_eff(t)=J(t)/S(t)` wherever numerically supported;
- log-survival curvature `K(t)=d^2 ln S / dt^2`, which for a non-degenerate positive mixture of exponentials equals the survival-weighted variance of decay widths and is non-negative.

## Exact single-species reference gate

For every branch also evaluate an `N=1` control with the same `m_0,Gamma_0`. Require numerical identity with

`S_1(t)=exp(-t)`, `J_1(t)=exp(-t)`, `Gamma_eff,1=1`

to maximum relative error <= `1e-12` over points with analytic value >1e-250.

## Distributed-response gates

For the N=64 ensemble require:

1. positive normalized weights summing to one within 1e-14;
2. strictly ordered/non-degenerate widths;
3. S(t) monotonically non-increasing and J(t)>0 on supported points;
4. `Gamma_eff(t)` non-increasing within numerical tolerance, as expected for a positive mixture whose faster components disappear first;
5. positive log-survival curvature at some supported time and non-negative analytic variance curvature to numerical tolerance;
6. a non-zero lifetime span `max(log10 tau_n)-min(log10 tau_n)>0`.

The best least-squares single-exponential approximation `A exp(-Gamma t)` over the supported dynamic range is also recorded. Its residual is diagnostic only and is not used as a post-hoc gate.

## Classification

Per branch: `M27_DDM_DISTRIBUTED_DECAY_GEOMETRY_PASS_WITH_SCOPE` iff the exact N=1 reference and all distributed-response gates pass.

Aggregate: `M27_DDM_NINE_BENCHMARK_GEOMETRY_PASS_WITH_SCOPE` iff all nine branches pass.

This establishes only the defining ensemble temporal geometry. `K1_promoted=false`, `K4_promoted=false`, `physical_falsification=false`. A later solver-level cosmological energy-transfer benchmark is required before higher gates.
