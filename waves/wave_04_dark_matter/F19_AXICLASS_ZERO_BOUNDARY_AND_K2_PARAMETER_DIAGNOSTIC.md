# F19 AxiCLASS zero-boundary and future-K2 parameter diagnostic

Date: 2026-09-14  
Provider: `PoulinV/AxiCLASS@ae9609e1f96ddebbb6cc8a46de94512514c68781`  
Status: **SOURCE DIAGNOSTIC ONLY — NOT A K0/K1 VERDICT**

## Context

The authoritative frozen F19 C0/Z0 execution is run `34846931382`. At the time of this note its author-control job is terminal PASS, while the `zero_identity` job remains non-terminal inside the combined `Frozen C0 and exact Z0 executions` shell step. No partial C0/Z0 scientific values were used here.

## Exact-zero source observation

For the pinned `n_axion=1` potential, source code implements the cosine form

`V = m^2 f^2 [1-cos(phi/f)]`

with a first derivative proportional to `sin(phi/f)`. Hence at the frozen Z0 state `phi=0`, `phi'=0`, the physical KG branch has `V=0`, `dV=0`, `rho_scf=0`, `p_scf=0`; exact zero is a formal background solution.

However, the same pinned `source/background.c` also contains

`w_scf = p_scf / rho_scf`

and labels that quantity as used for outputs. At exact Z0 this diagnostic is `0/0`. Therefore the exact-zero point is **not regular in every provider diagnostic coordinate**, even though the underlying KG field equations have an exact zero solution.

This observation does not establish the cause of the current long execution and does not authorize changing the frozen Z0 map. In particular, no claim is made yet that the NaN propagates into the evolution RHS.

## Orchestration observation

The recovery workflow places C0 and Z0 sequentially in one shell step, with no checkpoint artifact between them. While that step is non-terminal, GitHub job metadata cannot identify which of the two provider executions is active. If the authoritative run later terminates as infrastructure/provider-blocked, the first admissible recovery should preserve the exact INIs, cosmology, solver defaults and K1 thresholds while separating C0 and Z0 into independently observable jobs. No scientific threshold change is justified by this note.

## Future K2 coordinate identity

`f_axion` in the author `example_axionDM.ini` is documented as the axion decay scale (in reduced-Planck units), not as a dark-matter abundance fraction. The pinned input system separately exposes `Omega_scf` as a shooting target, and `Omega_scf_shoot_fa` compares the present scalar density against `Omega0_scf`. `fraction_axion_ac` is a distinct critical-epoch/EDE-style target and must not automatically be identified with present ULA dark-matter abundance.

Therefore, if and only if the frozen F19 K1 gate later PASSes, the K2 preregistration must first freeze an explicit abundance binding. The default candidate should be a present-day `Omega_scf` target/shooting coordinate (with `m_axion`, decay scale and initial angle treated as separate physical/model parameters), unless an author-supported F19-specific abundance coordinate is established more directly.

## Claim ceiling

- `K0_promoted`: unchanged by this diagnostic.
- `K1_promoted`: unchanged by this diagnostic.
- no K2 gate is authorized before terminal K1 authority;
- no provider failure or physical F19 falsification is inferred;
- no modification of the running C0/Z0 test is authorized while it is non-terminal.
