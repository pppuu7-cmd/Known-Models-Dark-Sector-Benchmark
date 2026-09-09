#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import numpy as np


def geom(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    na=float(np.linalg.norm(a)); nb=float(np.linalg.norm(b))
    if na==0 or nb==0: raise ValueError('zero vector')
    c=float(np.dot(a,b)/(na*nb)); c=max(-1.,min(1.,c))
    return {
        'cosine':c,
        'oriented_angle_deg':math.degrees(math.acos(c)),
        'acute_angle_deg':math.degrees(math.acos(abs(c))),
        'best_scalar_projection_residual_fraction':math.sqrt(max(0.,1-c*c)),
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--probe',required=True)
    ap.add_argument('--frozen-c1',required=True)
    ap.add_argument('--json',required=True)
    args=ap.parse_args()
    p=json.loads(Path(args.probe).read_text())
    comps={x['label']:x for x in p['comparisons_to_LCDM']}
    m=comps['M07_QPOINT_0025']; c=comps['C1_EPS1E4']
    q=0.025**2; eps=1e-4
    mP=np.asarray(m['response_vector_lnP'],float)/q
    mH=np.asarray(m['response_lnH'],float)/q
    cP=np.asarray(c['response_vector_lnP'],float)/eps
    cH=np.asarray(c['response_lnH'],float)/eps

    src=json.loads(Path(args.frozen_c1).read_text())
    frozen=next(d for d in src['directions'] if d['id']=='C1_smooth_w_nonphantom')
    fP=np.asarray(frozen['vector'],float)
    if len(fP)!=len(cP): raise ValueError('frozen C1 vector length mismatch')

    # Fit one scalar using matter response only, then carry the same mapping into H.
    a=float(np.dot(cP,mP)/np.dot(cP,cP))
    h_res=mH-a*cH
    p_res=mP-a*cP
    out={
      'schema':'KMDSB-W03-M07-C1-crosschannel-v0.1',
      'scope':'unwhitened theory-response; common 7x5 lnP plus 7-node lnH; no observational claim',
      'coordinates':{'M07':'q=lambda^2','M07_q':q,'C1':'epsilon_w=1+w','C1_epsilon':eps},
      'bridge_generated_C1_vs_frozen_DSIR_C1_P':geom(cP,fP),
      'M07_vs_C1_P':geom(mP,cP),
      'M07_vs_C1_H':geom(mH,cH),
      'matter_fit':{
        'C1_to_M07_scalar_from_P':a,
        'P_residual_fraction_after_fit':float(np.linalg.norm(p_res)/np.linalg.norm(mP)),
        'H_residual_fraction_using_same_P_fit_scalar':float(np.linalg.norm(h_res)/np.linalg.norm(mH)),
        'H_absolute_residual_norm':float(np.linalg.norm(h_res)),
        'M07_H_norm':float(np.linalg.norm(mH)),
        'scaled_C1_H_norm':float(np.linalg.norm(a*cH)),
      },
      'norms':{'M07_dlnP_dq':float(np.linalg.norm(mP)),'C1_dlnP_deps':float(np.linalg.norm(cP)),'M07_dlnH_dq':float(np.linalg.norm(mH)),'C1_dlnH_deps':float(np.linalg.norm(cH))},
    }
    Path(args.json).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
