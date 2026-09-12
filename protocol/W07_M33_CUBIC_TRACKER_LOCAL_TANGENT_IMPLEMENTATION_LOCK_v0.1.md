# W07 M33 cubic-tracker local tangent implementation lock v0.1

Date: 2026-09-12
Parent protocol: `protocol/W07_M33_CUBIC_TRACKER_LOCAL_TANGENT_PREREGISTRATION_v0.1.md`.

This file fixes the only implementation details not numerically explicit in the parent protocol, before execution.

For each non-base arm, define the normalized displacement blocks relative to base using the exact same global support and base L2 normalization as the derivative calculation. `cmb_displacement_norm` and `pk_displacement_norm` are the Euclidean norms of those normalized block vectors. A displacement is nonzero iff the corresponding full concatenated displacement norm is >0.

For a symmetric stencil scale, the CMB displacement scale is the arithmetic mean of the plus and minus CMB displacement norms; the P(k) displacement scale is the arithmetic mean of plus and minus P(k) displacement norms. Frozen contraction requires fine-scale mean < coarse-scale mean separately for CMB and P(k).

Principal angle is `acos(clamp(abs(cosine),-1,1))` in degrees, while the separate signed-cosine criterion uses the un-absolute cosine and must be >=0.995. Relative norm mismatch is `abs(norm_coarse-norm_fine)/max(norm_coarse,norm_fine)`.

No other metric or threshold may be introduced after execution.