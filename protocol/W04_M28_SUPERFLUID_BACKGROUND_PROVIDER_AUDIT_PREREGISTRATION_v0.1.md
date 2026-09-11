# W04 M28 superfluid/emergent DM background-provider audit preregistration v0.1

Status: prospectively frozen before hosted execution.

## Purpose
Audit whether `azieg/Superfluid-Dark-Matter-Cosmo` can serve as a public M28 superfluid/emergent-DM representative and whether its committed background notebook is reproducibly executable. This is a provider/provenance/representation gate only. It cannot promote K1-K9 and cannot falsify superfluid DM.

## Immutable provider
- repository: `azieg/Superfluid-Dark-Matter-Cosmo`
- commit: `860818c776bf8f000c08e4f02c1a23c5f48a8f52`
- target notebook: `Superfluid DM Hubble.ipynb`
- README and notebook are consumed unmodified.

## Frozen questions
1. Does the pinned source explicitly describe a superfluid-DM cosmological background and expose the implemented evolution equation in committed source?
2. Is the target computation background-only, or does it contain perturbation / Boltzmann / Einstein metric closure adequate for K3/K5?
3. Is there an explicit parameterized CDM/reference/decoupling map in the committed notebook suitable for a K1 gate?
4. Does the committed notebook execute on a modern hosted runner after installing only its declared scientific-Python dependencies (`numpy`, `scipy`, `matplotlib`, `jupyter`)? No physics edits are allowed.
5. Are the computed `sfdm_sol` values finite and non-empty under the committed parameter point?

## Source classification rules
- `M28_BACKGROUND_PROVIDER_CANDIDATE_WITH_SCOPE` only if the source explicitly implements a superfluid-DM background evolution equation and the notebook is not merely plotting precomputed external data.
- `M28_REPRESENTATIVE_MISMATCH` if the source is not actually a superfluid/emergent-DM cosmology representative.
- `M28_PROVENANCE_SOURCE_BLOCKED` if the pinned source cannot establish what equations/model are implemented.

Separately record:
- `perturbation_closure = PRESENT` only if source contains an implemented perturbation/Boltzmann/Einstein closure, otherwise `ABSENT`.
- `explicit_k1_reference_map = PRESENT` only if a model parameter is explicitly defined whose reference/decoupling value returns the same workload to CDM/LambdaCDM without replacing the model equation by hand; otherwise `ABSENT`.

## Execution classification rules
- `M28_BACKGROUND_PROVIDER_CONTROL_PASS` iff notebook execution exits zero and the executed notebook contains a non-empty, finite `sfdm_sol` output generated from the committed equations.
- Otherwise `M28_BACKGROUND_PROVIDER_CONTROL_BLOCKED` with first causal execution failure recorded.

## Aggregate rule
- If source candidate scope is established and execution control passes: `M28_BACKGROUND_ONLY_PROVIDER_EXECUTABLE_K1_K3_K5_OPEN`.
- If source candidate scope is established but execution blocks: `M28_BACKGROUND_PROVIDER_EXECUTION_BLOCKED`.
- If source is a representation mismatch: `M28_REPRESENTATIVE_MISMATCH_NO_PROMOTION`.
- If provenance is blocked: `M28_PROVIDER_PROVENANCE_BLOCKED`.

In every outcome: `K1_promoted=false`, `K3_promoted=false`, `K5_promoted=false`, `physical_falsification=false`.

## Scientific boundary
A successful background notebook is not perturbation closure, observational discrimination, or proof that M28 is response-distinct from CDM. In particular, absence of an explicit decoupling/reference coordinate leaves K1 open. A background-only provider may support scoped K0/provenance and representation bookkeeping only.
