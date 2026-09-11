# M26 PBH native CLASS K1 dual-channel preregistration v0.1

Frozen before execution. Provider `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

Two independent energy-injection subchannels are required:
1. evaporation: mass `1e15`, K0 anchor fraction `1e-7`;
2. disk accretion: mass `30`, `PBH_accretion_recipe=disk_accretion`, ADAF_delta `1e-3`, eigenvalue `0.1`, refined K0 anchor fraction `1e-3`.

For each channel run exact-zero fraction reference and active scale ladder `s={1,0.1,0.01,0.001}` times the channel anchor. Other cosmology and PBH channel are held at zero/fixed exactly as in the canonical K0 configuration.

Analyze native scalar TT and linear z=0 P(k) with `verification/k1/decoupling_ladder.py`. Per-channel scoped PASS requires exact pin, all finite zero-exit arms, Dfine<Dcoarse, adjacent finer D <=1.20 previous, Dfine/Dcoarse<=0.25 and log-log Pearson>=0.90. M26 K1 may be promoted to PASS_WITH_SCOPE only if BOTH subchannels pass. A miss is PARTIAL/NOT_ESTABLISHED; execution failure is implementation/numerical block. No result is physical falsification.

Scope guard: this K1 concerns native CLASS PBH evaporation/accretion energy-injection response only. It does not establish PBH Poisson/discreteness/isocurvature physics. K2-K9 remain open.