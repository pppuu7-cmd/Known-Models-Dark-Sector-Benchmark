# W04 / M19 axionCAMB 2.0 independent zero-reference probe v0.1

Frozen: 2026-09-10
Status: PREREGISTERED
Family: F19/M19 fuzzy / ultralight axion dark matter
Independent provider: `dgrin1/axionCAMB@891e779cc0bd422e49f97533e6c2fc761149737d`

## Purpose

AxiECAMB finite ULA control (`f_ax=0.10`) executes, but both exact-zero interfaces segfault inside the axion-background path. Test whether the current upstream/legacy axionCAMB 2.0 line has an independently executable exact CDM reference.

This is a provider/reference probe only. It does not promote K2-K9 and does not interpret a crash as physical FDM falsification.

## Frozen source facts

At this pin axionCAMB documents a ULA background + perturbation implementation based on the Hlozek et al. framework and contains 2023 bug fixes plus a 2026 m/H bug fix. Its input source has the same intended fraction map:

`omegaax=axfrac*omegada`, `omegac=(1-axfrac)*omegada`

and an independent density interface `omaxh2`, `omch2`.

The source also calls `w_evolve(P,badflag)` unconditionally before regular CAMB execution, so exact-zero support must be established by execution rather than inferred from input algebra.

## Cases

Start from the pinned committed `params.ini`; set linear scalar mode, `do_lensing=F`, `do_nonlinear=0`, `axion_isocurvature=F`, `m_ax=1e-27 eV`, `OMP_NUM_THREADS=1`.

- R0F: `use_axfrac=T`, `omdah2=0.1200`, `axfrac=0`, `output_root=r0f_`.
- R0D: `use_axfrac=F`, `omch2=0.1200`, `omaxh2=0`, `output_root=r0d_`.
- P1: `use_axfrac=T`, `omdah2=0.1200`, `axfrac=0.10`, `output_root=p1_`.

## Output contract

For a case to execute, require exit 0 plus finite nonempty:

- `*_scalCls.dat`
- `*_matterpower.dat`
- `*_transfer_out.dat`

If both zero cases execute, compare R0F/R0D with the same normalized max absolute difference used in the AxiECAMB K1 preregistration, `D_inf<=1e-10` per common file.

## Build scope

System gfortran; serial make. Compatibility-only flags `-ffree-line-length-none` and, if required for this legacy source, `-fallow-argument-mismatch` are permitted and recorded. No source edits.

## Classifications

- `M19_AXIONCAMB2_K1_ZERO_REFERENCE_PASS_WITH_SCOPE`
- `M19_AXIONCAMB2_ZERO_REFERENCE_BLOCKED`
- `M19_AXIONCAMB2_FINITE_CONTROL_BLOCKED`
- `M19_AXIONCAMB2_BUILD_BLOCKED`
- `M19_AXIONCAMB2_ZERO_IDENTITY_FAIL`

No failure is a physical family falsification.
