# KMDSB authority deltas

Updated: 2026-09-09

## Rule

Existing benchmark evidence is immutable with respect to its pinned scientific authority. A newer DSIR `main` may be adopted only by a new wave, a new audit revision, or an explicit authority-delta validation. Never silently reinterpret an old result under a newer DSIR commit.

## AD-001 — W00-W02 to W03

### Frozen authority used by W00-W02

`pppuu7-cmd/Dark-Sector-Influence-Reconstruction@e3276e2193f6a5200b541a194e3175356ae5a1c1`

### DSIR main checked on 2026-09-09

`pppuu7-cmd/Dark-Sector-Influence-Reconstruction@328f2ca80b724870b851c7fe6366cce1ca5086cd`

The newer commit is 11 commits ahead of the W00-W02 authority.

### Delta inspection

The inspected delta contains DSIR4 ordered-join / radial-support / process-recovery work, including:
- `EXP073IL` C2 ordered-join structural-admission workflow/authority;
- DSIR4 ordered-join definition;
- DSIR4 radial-support input requirements;
- current-process and recovery updates.

No change in this inspected delta was used to recompute or silently alter the frozen C1-C6 response products underlying W00-W02.

### Decision

- W00, W01 and W02 remain pinned to `e3276e...`.
- W03 may use `328f2ca...` as its starting DSIR authority.
- Any W03 comparison against a W00-W02 numerical artifact must cite the artifact's own older authority/provenance explicitly.
- If a DSIR4 change later proves to alter a shared convention relevant to C1-C6, create a dedicated migration/regression audit rather than rewriting history.

## Recovery instruction

A fresh chat must read this file before assuming that the newest DSIR `main` is the authority for every KMDSB result.
