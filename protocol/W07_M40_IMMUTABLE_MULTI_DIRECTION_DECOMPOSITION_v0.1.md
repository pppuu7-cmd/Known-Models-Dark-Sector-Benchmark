# W07 M40 immutable multi-direction response decomposition v0.1

Date: 2026-09-12
Model: M40 pinned EFTCAMB Hořava representative
Purpose: analysis-only synthesis of already-computed radial, eta, xi and lambda local response directions at the same author-shipped base point `(xi,lambda,eta)=(-1e-4,+1e-4,2.1e-3)`.

## Immutable inputs

- radial + eta: run `34695408204`, artifact `10298444789`;
- xi: run `34695841353`, artifact `10298324085`;
- lambda: run `34695841353`, artifact `10298572066`;
- pinned-source geometry: run `34695971559`, artifact `10298124024`;
- provider: `EFTCAMB/EFTCAMB@16d9c4e9f85751e30efd0a53b177941713078904`.

No new EFTCAMB execution or step-size change is authorized.

## Frozen analysis

Reconstruct fine central derivatives on one common support for CMB scalar spectra and P(k): radial from h=0.001 in q, eta from delta=2.1e-5, xi from delta=1e-6, lambda from delta=1e-6. Normalize CMB and P(k) blocks by the shared base L2 norm, then concatenate blocks.

For each coordinate retain its already-frozen derivative convergence eligibility from its parent artifact. A direction is eligible for local-rank evidence only if its own coarse/fine derivative passed the frozen <=5 degree and <=0.25 norm-mismatch criterion.

Compute pairwise principal angles among the fine radial/eta/xi/lambda derivatives, both combined and separately in CMB and P(k). The frozen independence separator remains >=10 degrees. Nonconverged directions may be reported geometrically but cannot be used to promote response rank.

## Interpretation lock

The source audit establishes three ordinary input coordinates with an optional Solar-System branch reduction; it does not establish observable rank. This workflow cannot promote K2. Its strongest allowed classifications are descriptive, including `M40_SOURCE_3D_INPUT_LOCAL_RANK2_NOT_ESTABLISHED_NUMERICAL_CONVERGENCE_OPEN` or `M40_ELIGIBLE_LOCAL_RESPONSE_REMAINS_RANK1_WITH_SCOPE`.

Always set `K2_promoted=false`, `physical_falsification=false`, `complete_Horava_family_claim=false`.