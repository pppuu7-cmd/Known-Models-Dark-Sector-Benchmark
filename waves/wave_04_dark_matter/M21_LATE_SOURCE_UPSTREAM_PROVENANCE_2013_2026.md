# M21 late-source approximation upstream provenance — 2013 to pinned CLASS

Provider under benchmark: `lesgourg/class_public@e85808324f51fc694d12e3ed7439552a3c3f9540`.

This note is provenance only. It does not alter any benchmark classification or claim a provider defect.

## History established from public upstream commits

1. `c41de4ad7aa555521fe862b6ceed84f1beaccdb8` (2013-09-24), `implemented late source approximation`
   - introduced the late-source truncation approximation;
   - the predicate was initially `l > transfer_neglect_late_source`, without angular-rescaling multiplication.

2. `f104f5e33d635c186e94cd6f0975c78e46adb27f` (2013-09-26), `added scaling of l/k relation with curvature`
   - introduced/used `angular_rescaling` as a curvature-related l/k scaling quantity;
   - the late-source predicate in that snapshot still did not multiply its threshold by `angular_rescaling`.

3. `7d93c1bb239a356ee4410fd82bc22f73566594b9` (2013-10-31), `late source cut approximation removed for t0 source for better Tphi, Ephi`
   - upstream already changed the applicability of the approximation for accuracy reasons;
   - the late-source threshold remained unscaled in that snapshot.

4. `558f43e792c7f02fd65d42ab8209136a47dd6a25` (2013-11-25), `updated the flat rescaling approximation`
   - the late-source threshold remained unscaled in that snapshot.

5. `97aacf5eca29f314c02dd9f6dd3316b3eb000457` (2013-11-26 11:40 UTC), `improved time cut approximation`
   - this is the exact upstream commit that changed:
     `if (l > ppr->transfer_neglect_late_source)`
     to
     `if (l > ppr->transfer_neglect_late_source*ptr->angular_rescaling)`;
   - the same commit also changed which transfer types use the approximation.

By the pinned modern provider, the same scaled-threshold form remains present.

## Interpretation ceiling

The benchmark-local ULP sensitivity therefore arises in a historical speed/accuracy time-cut approximation whose threshold was explicitly modified upstream to include curvature-related angular rescaling. Public history also shows that the approximation's applicability has been changed before for accuracy reasons.

This history does **not** establish that the current implementation is a known upstream bug, does not show that the 2013 authors intended exact-flat binary64 identity handling, and does not authorize a production patch. A defect/fix claim still requires broader prospective regression across independent flat cosmologies and, ideally, provider versions.