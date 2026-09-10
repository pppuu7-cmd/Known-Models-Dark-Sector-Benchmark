# W03 / M17 c=0.6 joint H(a)+CMB CPL K6 coarse-grid attack v0.1

Frozen: 2026-09-10
Status: PREREGISTERED
Provider: recovered linear IDECAMB/ePPF route
Target: M17 HDE `c=0.6`, the point that survived the fixed background-CPL transport attack with `R_equal~0.455` in TT/TE/EE.

## Question

Can one shared CPL parameter pair absorb the c=0.6 HDE response **simultaneously** in a background expansion block and all three available scalar CMB blocks, once CPL is allowed to move away from the background-only optimum?

This is a K6 theory-space nearest-family attack. It is not K7 covariance profiling.

## Provider/isolation

Exact pins:
- `cmbant/CosmoMC@eb08c2fe91d9711929802fede310ae58c020fcb4`
- `liaocrane/IDECAMB@4f1093d9efe46f28cf7e2acb4d07ae116ad5e075`

Use the successful linear route: beta=0, Use_PPF=T, nonlinear_pk=F, CMB_lensing=T, `use_nonlinear_lensing=F`, action=4 theory-output mode, external likelihood DEFAULTs disabled.

## Reference and HDE target

R0: CPL `w0=-1`, `w1=0`.
H06: HDE `c=0.6`.

Require finite common `.quantity` HDE/CPL columns 1-7 and finite common `.theory_cl` columns `L,TT,TE,EE`.

Background block is provider conformal-Hubble output `adotoa` (quantity column 5) on the full 2000-row common scale-factor grid. The scale-factor grid itself must match exactly across cases within `1e-14` absolute.

## Frozen CPL coarse grid

Center is the pre-existing background-only best fit:

`w0_c=-1.299870066355541`
`wa_c=+0.9082964747357177`.

Freeze offsets:

`delta_w0 in {-0.20,-0.10,0,+0.10,+0.20}`

`delta_wa in {-0.40,-0.20,0,+0.20,+0.40}`.

Execute all 25 Cartesian pairs. No case may be added/removed after exposure.

## Equal-block joint metric

Blocks `b={H,TT,TE,EE}`.

For every block define target response relative to R0:
`h_b = H06_b - R0_b`.

For candidate p:
`e_b(p)=H06_b-CPL_b(p)`.

If `||h_b||<=1e-20`, mask block as nonidentifiable; otherwise
`R_b(p)=||e_b(p)||_2/||h_b||_2`.

Joint metric:
`R_joint(p)=sqrt(mean_b R_b(p)^2)` over identifiable blocks.

Also record `R_max=max_b R_b`.

This gives H, TT, TE and EE equal block weight regardless of raw unit/amplitude scale. No elementwise division is used.

## Coarse-grid interpretation

Let p* be the unique smallest `R_joint`; ties within `1e-12` are retained explicitly.

Descriptive bins:
- `COARSE_JOINT_CPL_STRONG_ABSORPTION` if `R_joint<=0.10` and `R_max<=0.20`;
- `COARSE_JOINT_CPL_PARTIAL_ABSORPTION` if not strong but `R_joint<=0.30` and `R_max<=0.50`;
- `COARSE_JOINT_CPL_SURVIVOR_CANDIDATE` otherwise.

A coarse-grid survivor is **not** a final K6 survivor. It automatically authorizes one pre-defined refinement around p*.

## Pre-defined refinement rule

If the coarse run passes output gates, next grid is centered on p* with offsets:

`delta_w0 in {-0.10,-0.05,0,+0.05,+0.10}`
`delta_wa in {-0.20,-0.10,0,+0.10,+0.20}`

using the same metric and provider. This rule is frozen now before seeing p*.

If p* lies on a coarse boundary, the refinement is still centered on p*; the search is not recentered inward.

## Output classifications

- `M17_C060_K6_COARSE_STRONG_ABSORPTION`
- `M17_C060_K6_COARSE_PARTIAL_ABSORPTION`
- `M17_C060_K6_COARSE_SURVIVOR_CANDIDATE`
- `M17_C060_K6_COARSE_OUTPUT_BLOCKED`

No observational significance or physical falsification claim follows from this gate.
