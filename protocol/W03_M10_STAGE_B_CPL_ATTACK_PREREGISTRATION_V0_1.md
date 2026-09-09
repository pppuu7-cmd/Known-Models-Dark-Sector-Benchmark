# W03 / M10 Stage B — same-solver CPL manifold attack preregistration v0.1

Frozen: 2026-09-10, before M10 Stage A response inspection.

## Entry condition
Run Stage B only if M10 Stage A obtains:
1. executable same-solver Lambda reference;
2. successful CLASS_EDE shooting for the frozen M10 grid;
3. at least one converged M10 local response block.

If Stage A fails, preserve this preregistration but do not force Stage B.

## Comparator authority
Use the same solver commit and same cosmological settings as M10:
`mwt5345/class_ede@5a131c91d657dd9a7c6364cc45b038710f8d0d97`.

CPL comparator branch:
- no scalar field: `Omega_scf=0`;
- `Omega_Lambda=0`;
- `Omega_fld` inferred by closure;
- `fluid_equation_of_state=CLP`;
- `cs2_fld=1`;
- `use_ppf=yes`;
- reference `(w0,wa)=(-1,0)`.

Local coordinates:
`epsilon0=1+w0`, `epsilon_a=wa`.

Frozen central step for both directions:
`h_CPL=5e-4`.

Cases:
- epsilon0 = +/-5e-4, wa=0;
- epsilon_a = +/-5e-4, w0=-1.

## Response blocks
Exactly the same M10 Stage A grids and definitions:
- P: 7x5 low-k lnP response;
- H: 7-node lnH response;
- S: z=0.51 broad-k amplitude-quotiented shape response.

No block may be silently dropped. Near-null comparator directions are reported explicitly.

## M10 target direction
Use the preregistered local M10 tangent derived from the two smallest Stage A points `fEDE={0.005,0.01}` if Stage A convergence passes. Use the componentwise mean of the two `r/fEDE` directions; do not choose whichever point fits CPL worse.

## Primary cross-channel test
Construct CPL Jacobian `J_L` from the two central CPL directions concatenated over P+H.

Fit one coefficient vector
`beta_L = argmin || r_EDE,L - J_L beta ||_2`.

Then, **without refitting**, predict the shape direction
`r_CPL,S = J_S beta_L`
and report:
- L residual fraction;
- P residual fraction;
- H residual fraction;
- S transfer residual fraction using the same `beta_L`;
- angles where norms are non-negligible.

This is the primary mechanism-separator diagnostic. Independent best fits in P, H and S cannot establish equivalence.

## Secondary S-only diagnostic
Also compute projection of M10 S onto the full CPL S span. Report its residual fraction, but label it diagnostic because its coefficient vector is allowed to differ from the primary L fit.

## Interpretation
- If L is well absorbed but the same coefficients leave a stable large S residual, M10 has a cross-channel early/shape separator in theory-response space.
- If full CPL also absorbs S, no M10 mechanism novelty is established by these blocks.
- If CPL S is near-null, this strengthens the descriptive contrast but is still not observational discrimination.
- No threshold for 'large S residual' is invented after output. Stage B reports the continuous residual fractions. A promotion claim requires later observation-space weighting or an independently frozen threshold.

## Observation-space rule
Stage B remains unwhitened theory-response geometry. Any B5/B7 observational promotion needs an exact common observation operator/covariance that admits the early/shape information. The previous late-time ShapeFit operator is insufficient merely because it exists.
