# W03 M17 K7a header-contract recovery v0.1

## Status
Prospective parser-only recovery. No theory case, Planck operator, covariance, physics coordinate, provider pin, or scientific criterion changes.

## Trigger
After the preregistered `lmin_store_all_cmb=2600` output-coverage recovery, both theory cases executed and produced finite four-column spectra through ell=2600. Analysis stopped only because the parser required the literal substring `L TT TE EE`, while the provider writes the same semantic header with padded whitespace: `#    L    TT             TE             EE`.

## Frozen repair
Replace the literal-space substring check with a whitespace-insensitive exact token contract accepting only a comment header whose normalized tokens are exactly:

`L TT TE EE`

The numeric row contract remains exactly four finite columns. Coverage must still reach ell>=2508.

## Interpretation
This is formatting compatibility only. It cannot alter any spectrum value or covariance statistic and cannot itself promote K7.
