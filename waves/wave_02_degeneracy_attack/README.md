# Wave 02 — Same-observable degeneracy attack

Status: **COMPLETE**  
Opened: 2026-09-08  
Closed: 2026-09-09  
Protocol: `protocol/WAVE_TESTING_PROTOCOL_v0.1.md`  
Frozen DSIR authority for this wave: `e3276e2193f6a5200b541a194e3175356ae5a1c1`

## Scientific question

Given that Wave 01 proved no single response block is universally sufficient, which apparently similar known-model responses remain distinguishable when each unresolved pair is tested on the **smallest valid common multi-channel block**?

The objective is not to maximize separations. It is to distinguish genuine response separation from missing implementations, lossy summaries, masks and lack of observational whitening.

## Final edge ledger

### W02-PC1 — M03 GDM vs M05 designer f(R)

`PASS_WITH_SCOPE`.

Frozen positive control reproduces the semantic result that scale-only mimicry is not full-response equivalence:
- scale-mode angles about `0.07813–0.10169 deg`;
- time-mode angles about `25 deg`;
- full oriented ray angles about `154.5–154.8 deg`.

See `PC1_GDM_vs_fR.md`.

### W02-E1 — M02 IDE vs M03 GDM

`PASS_WITH_SCOPE` in the unwhitened frozen 7x5 low-k `r_Delta(k,z)` tangent block.

Closest frozen pair: IDE alpha-negative vs GDM cv2, acute angle `24.786398 deg`. Exact directional collinearity is rejected within scope.

See `E1_IDE_vs_GDM.md` and `E1_result.json`.

### W02-E2 — M02 IDE vs M05 designer f(R)

`PASS_WITH_SCOPE` in the same class of common low-k theory-response geometry.

Acute angles against the minimum-resolved designer-f(R) production ray are `42.450273 deg` and `59.404101 deg` for the two frozen IDE directions.

See `E2_IDE_vs_fR.md` and `E2_result.json`.

### W02-E3 — M04 WDM vs alternative small-scale suppression

`BLOCKED_IMPLEMENTATION`.

The WDM high-k block is pinned, but the frozen DSIR C0-C6 authority contains no second non-WDM suppression family implemented on a valid same-convention high-k block. This is not evidence of WDM uniqueness.

See `E3_WDM_vs_alt_suppression.md` and `E3_result.json`.

### W02-E4 — M06 DCDM vs alternative temporal histories

`INCONCLUSIVE`.

A common amplitude-invariant temporal centroid exists:

`q_z(z)=sum_k r(k,z)^2/sum_{z,k} r(k,z)^2`

`z_R=exp[sum_z q_z ln(1+z)]-1`.

DCDM spans `z_R=0.6304573..0.6562403`; frozen alternative centroids include C1 `0.6214183`, GDM `0.7315737/0.7362246`, IDE `0.9516949/1.0839530`, and designer-f(R) `0.4547904`.

The scalar coordinate is portable, but no preregistered separation threshold or observational covariance exists and the nearest C1 value is close. Therefore a one-number characteristic epoch is not a hard mechanism discriminator.

See `E4_DCDM_vs_temporal_histories.md`, `E4_result.json`, and `code/wave02_temporal_centroid_comparator.py`.

## Frozen Wave-02 hypotheses — final states

- **W02-H1 restricted-block degeneracy is not equivalence:** `SUPPORTED`.
- **W02-H2 missing common channels/implementations create legitimate BLOCKED edges:** `SUPPORTED`.
- **W02-H3 minimum discriminating suite is a graph problem:** `SUPPORTED`.
- **W02-H4 observation-space promotion is separate:** `SUPPORTED`.

## Separate graphs

- `THEORY_SPACE_GRAPH.md` — frozen response-geometry statements and blocked/inconclusive theory edges.
- `OBSERVATION_SPACE_GRAPH.md` — only claims that survive an explicit observational operator/covariance; no new W02 edge is promoted there.

## Scientific conclusion

Wave 02 establishes that pairwise distinguishability is a graph over **model pair x valid response block x mask x observational operator**. Restricted-block similarity, missing comparator implementation and lossy scalar compression are distinct failure modes.

The future-model methodology therefore must:
1. attack nearest alternatives rather than compare only with LambdaCDM;
2. never infer uniqueness from an unimplemented comparator;
3. preserve fuller temporal/multi-channel profiles when scalar summaries are close;
4. keep theory-space and observation-space graphs separate.

Exact machine-readable closure: `result.json`.
