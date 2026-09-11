# W05 M30/M31/M40 parallel K1 reference-limit batch — preregistration v0.1

This contract is frozen before any K1 outputs are inspected.

## Exact providers
- M30/M31: `hiclass-code/hi_class_public@0009f51d89e6465c79e570b496c66fc90058fa77`.
- M40: `EFTCAMB/EFTCAMB@16d9c4e9f85751e30efd0a53b177941713078904`.

## Coordinates and ladders
- M30 Horndeski/EFT-DE: use `gravity_models/propto_omega_bh.ini` with the already-K0-frozen active coefficients `(c_K,c_B,c_M,c_T,c_H,M2_ini)=(1,0.5,0.2,0,0,1)`. Scale the first five coefficients jointly by `s={1,0.1,0.01,0.001}`; same-model reference is `s=0`, with `M2_ini=1` and `expansion_model=lcdm` unchanged.
- M31 beyond-Horndeski: same provider/config with native coefficients `(1,0.5,0.2,0,0.3,1)`. Scale the first five jointly by the same `s` ladder; reference `s=0`, `M2_ini=1`, LCDM expansion unchanged.
- M40 Hořava-Lifshitz: start from native EFTCAMB test `5_Horava_eta_3.ini`, coefficients `(xi,lambda,eta)=(-0.001,0.001,0.021)`. Scale all three jointly by `s={1,0.1,0.01,0.001}`. Same-model reference is the native Hořava mapping with all three equal zero. Separately execute provider `1_EFT_GR.ini` as an endpoint identity control.

## Frozen observables and statistic
Use unlensed/native scalar TT-like first CMB spectrum column and linear z=0 matter P(k) from the provider outputs. For each active point relative to its same-provider zero reference define `D=max(d_TT,d_Pk)`, normalized L2 on overlapping x-grid. Active points are ordered coarse to fine by decreasing `s`.

Scoped K1 PASS requires: exact commit; all reference/active executions zero-exit and finite; `D_fine < D_coarse`; every finer D <= 1.20 times immediately coarser D; `D_fine/D_coarse <= 0.25`; log10(s)-log10(D) Pearson >=0.90. M40 additionally requires native-zero and explicit EFT-GR control to be numerically consistent at `max(d_TT,d_Pk) <= 1e-4`; failure of that endpoint identity makes K1 NOT_ESTABLISHED, not physical FAIL.

Classification: all criteria -> `PASS_WITH_SCOPE`; executable but convergence/endpoint criterion misses -> `PARTIAL/NOT_ESTABLISHED`; build/execution/output failure -> implementation/numerical block. No result is a physical family falsification. K2-K9 remain open.