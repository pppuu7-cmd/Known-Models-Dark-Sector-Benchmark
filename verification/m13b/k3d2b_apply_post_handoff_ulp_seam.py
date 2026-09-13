#!/usr/bin/env python3
"""Move only the enabled second background segment start by N representable ln(a) points."""
from __future__ import annotations
import argparse, hashlib, json, math
from pathlib import Path


def sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('root')
    ap.add_argument('--ulps',type=int,choices=(1,2),required=True)
    ap.add_argument('--manifest')
    a=ap.parse_args()
    p=Path(a.root)/'source/background.c'
    before=p.read_text()
    anchor='    /* Restart with the exact endpoint state; evolver history is intentionally rebuilt. */\n'
    if before.count(anchor)!=1:
        raise RuntimeError(f'expected one enabled restart anchor, found {before.count(anchor)}')
    pos=before.index(anchor)+len(anchor)
    tail=before[pos:]
    marker='generic_evolver(background_derivs,'
    g=tail.index(marker)
    call_start=pos+g
    search=before[call_start:call_start+1200]
    if search.count('loga_handoff_kmdsb')<1:
        raise RuntimeError('second call does not start from handoff token')
    post_decl=(
        f'    double loga_post_handoff_kmdsb = loga_handoff_kmdsb;\n'
        + ''.join('    loga_post_handoff_kmdsb = nextafter(loga_post_handoff_kmdsb, loga_final);\n' for _ in range(a.ulps))
    )
    after=before[:pos]+post_decl+before[pos:]
    call_start_after=call_start+len(post_decl)
    w=after[call_start_after:call_start_after+1200]
    w2=w.replace('loga_handoff_kmdsb','loga_post_handoff_kmdsb',1)
    if w==w2:
        raise RuntimeError('failed to replace second-segment start')
    after=after[:call_start_after]+w2+after[call_start_after+len(w):]
    if after.count('nextafter(loga_post_handoff_kmdsb, loga_final)')!=a.ulps:
        raise RuntimeError('wrong nextafter count')
    if after.count('a <= exp(log(1./6.))')!=4:
        raise RuntimeError('floating boundary recovery missing')
    p.write_text(after)
    m={
      'schema':'KMDSB.W03.M13b.K3D2BPostHandoffULPSeamPatch.v0.1',
      'post_handoff_ulps':a.ulps,
      'same_state_vector':True,
      'first_segment_endpoint_unchanged':True,
      'changes_equations':False,
      'changes_tolerances':False,
      'changes_perturbations':False,
      'background_sha256_before':sha(before),
      'background_sha256_after':sha(after)
    }
    if a.manifest: Path(a.manifest).write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
    print(json.dumps(m,indent=2,sort_keys=True))
    return 0
if __name__=='__main__': raise SystemExit(main())
