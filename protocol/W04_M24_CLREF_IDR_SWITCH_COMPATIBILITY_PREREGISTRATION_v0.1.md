# W04 M24 cl_ref IDR-switch compatibility recovery preregistration v0.1

## Trigger

The global M24 precision diagnostic established that `cl_permille.pre` leaves the a_idm_dr=6000 excursion insensitive. The `cl_ref.pre` branch did not execute because CLASS requires `idr_streaming_trigger_tau_over_tau_k` and `ur_fluid_trigger_tau_over_tau_k` to differ. At the pinned CLASS version the IDR default is 50, while `cl_ref.pre` sets the UR trigger to 50.

## Frozen compatibility intervention

CLASS remains pinned to `e85808324f51fc694d12e3ed7439552a3c3f9540`. All M24 physical inputs and the five diagnostic cases remain unchanged.

For both sides of the comparison, set exactly:

`idr_streaming_trigger_tau_over_tau_k = 49`

The default-control side receives only this one compatibility precision override. The high-precision side receives the complete unmodified provider `cl_ref.pre` plus the same IDR trigger override. Thus the IDR switch timing is identical on both sides and cannot masquerade as a cl_ref precision effect.

All five cases on each side may execute concurrently because their output roots are unique.

## Classification

Reuse the existing `global_numerical_precision_diagnostic.py` classification without threshold changes. This recovery is diagnostic-only and cannot promote K1/K4 or constitute physical falsification.
