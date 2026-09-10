# W04 / M19 axionCAMB2 exact-zero neutrino isolation control v0.1

Frozen: 2026-09-10
Status: DIAGNOSTIC_ONLY
Scientific promotion: NONE

Provider: `dgrin1/axionCAMB@891e779cc0bd422e49f97533e6c2fc761149737d`.

Pre-existing evidence: finite axion fraction executes; exact axfrac=0 crashes. Runtime-checked diagnostic run 34511569527 localizes the first hard failure to `MassiveNu::Nu_rho` (`modules.f90:1663`) with integer index `-2147483648` while called from the axion-background evolution. This does not yet identify whether massive neutrinos are causal or merely receive a non-finite argument from an earlier exact-zero axion state.

Frozen isolation change relative to the previous exact-zero diagnostic case: keep `use_axfrac=T`, `omdah2=0.1200`, `axfrac=0`, `m_ax=1e-27 eV` and all other generated settings unchanged except set the known-sector massive-neutrino density and count to zero (`omnuh2=0`, `massive_neutrinos=0`, `nu_mass_eigenstates=0`). Do not edit axion equations, initial conditions, thresholds, or provider source.

Build serially with the same runtime-check flags. Execute exactly one case and archive the generated ini, build log, run log and status.

Interpretation frozen prospectively:
- if the exact-zero case executes, classify the prior crash as `KNOWN_SECTOR_NEUTRINO_PATH_INTERACTION_ISOLATED_WITH_SCOPE`; this is diagnostic evidence only and does not itself promote M19 K1 because the comparator cosmology has changed;
- if the exact-zero case still fails outside the disabled massive-neutrino path, classify `AXION_ZERO_REFERENCE_PROVIDER_BLOCKER_PERSISTS` and use the first line-resolved failure only to define a separately preregistered diagnostic;
- if the build/configuration fails before execution, classify infrastructure failure only.

No physical FDM falsification is authorized by any branch of this diagnostic.
