# W05 M30 independent EFTCAMB K0 provider preregistration v0.1

Date: 2026-09-11
Family: F30 / M30 Horndeski-EFT-DE manifold
Gate: independent K0 provider/provenance cross-check

Pinned second provider: `EFTCAMB/EFTCAMB` at `16d9c4e9f85751e30efd0a53b177941713078904`.
Native shipped test: `fortran/eftcamb_test/parameters/3_RPH_MB_OmegaDE_1.ini`.
Same-provider GR control: `fortran/eftcamb_test/parameters/1_EFT_GR.ini`.

The native test uses `EFTflag=2`, `AltParEFTmodel=1` (reparametrized Horndeski), LCDM background (`RPHwDE=0`) and active `alpha_M`, `alpha_B` functions proportional to the dark-energy fraction with amplitudes `RPHalphaM_ODE0=1`, `RPHbraiding_ODE0=-1`.

Two arms run independently with `fail-fast:false`.

PASS_WITH_SCOPE requires exact pin, successful documented `make camb`, exit 0 for both arms, finite non-empty scalar-CMB and matter-power outputs, and a branch-active difference >1e-6 in at least one common output sample. This proves only an independent executable Horndeski effective subspace and cannot establish exhaustive Horndeski coverage, K1-K9, or physical falsification.