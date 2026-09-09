#!/usr/bin/env python3
"""W03/M07 B5: scoped DESI DR1 ShapeFit identifiability for q=lambda^2.

Uses the same corrected ShapeFit covariance/control semantics as M01/B5, but
reads M07 and LambdaCDM CLASS background outputs directly. This is an
optimistic unmarginalized AP+growth control, not a full DESI likelihood.
"""
from __future__ import annotations
import argparse, json, math, re
from pathlib import Path
import numpy as np

COV_SCALE=1e-4
USE=("LRG1","LRG2","LRG3","ELG2","QSO")
BINS={
"LRG1":{"z":0.51,"fid_ap":1.6858,"fid_g":0.4733,"cov":[[541.309833,48.425593,-4.652853,-37.707751],[48.425593,97.249820,-34.923265,-14.418597],[-4.652853,-34.923265,41.295470,15.405508],[-37.707751,-14.418597,15.405508,48.918910]]},
"LRG2":{"z":0.71,"fid_ap":1.1399,"fid_g":0.4608,"cov":[[762.457717,39.781004,-1.896006,-62.812849],[39.781004,36.344098,-17.341350,-8.333900],[-1.896006,-17.341350,28.119682,8.865225],[-62.812849,-8.333900,8.865225,47.624520]]},
"LRG3":{"z":0.92,"fid_ap":0.8162,"fid_g":0.4398,"cov":[[847.499793,26.038900,3.257324,-37.016091],[26.038900,16.251088,-10.044074,-3.698790],[3.257324,-10.044074,22.370314,6.467510],[-37.016091,-3.698790,6.467510,34.883220]]},
"ELG2":{"z":1.32,"fid_ap":0.5029,"fid_g":0.3944,"cov":[[2342.506886,26.159601,13.521001,-95.336060],[26.159601,10.309303,-6.654663,-5.183903],[13.521001,-6.654663,13.997473,9.109619],[-95.336060,-5.183903,9.109619,43.575710]]},
"QSO":{"z":1.49,"fid_ap":0.4228,"fid_g":0.3750,"cov":[[3013.788566,-2.205101,36.332110,-98.167826],[-2.205101,5.845806,-6.747133,-1.913326],[36.332110,-6.747133,19.785658,5.357546],[-98.167826,-1.913326,5.357546,26.266260]]},
}

def titles(path:Path):
    text=''
    with path.open() as f:
        for _ in range(30):
            s=f.readline()
            if not s: break
            if s.startswith('#'): text+=' '+s[1:].strip()
            else: break
    ms=list(re.finditer(r'(?:^|\s)(\d+):',text)); out={}
    for i,m in enumerate(ms):
        out[int(m.group(1))-1]=text[m.end():(ms[i+1].start() if i+1<len(ms) else len(text))].strip()
    return out

def load_bg(path:Path):
    tt=titles(path); a=np.loadtxt(path,comments='#')
    def col(prefix): return next(i for i,t in tt.items() if t.startswith(prefix))
    iz=col('z'); ih=col('H [1/Mpc]'); idm=col('comov. dist.'); iD=col('gr.fac. D'); iff=col('gr.fac. f')
    order=np.argsort(a[:,iz])
    return {'z':a[order,iz],'H':a[order,ih],'DM':a[order,idm],'D':a[order,iD],'f':a[order,iff]}

def at(bg,key,z): return float(np.interp(z,bg['z'],bg[key]))

def prediction(bg,ref,name):
    b=BINS[name]; z=b['z']
    H,DM,D,f=(at(bg,k,z) for k in ('H','DM','D','f'))
    Hr,DMr,Dr,fr=(at(ref,k,z) for k in ('H','DM','D','f'))
    ap_ratio=(Hr/H)*(DMr/DM)
    growth_ratio=(D*f)/(Dr*fr)
    # Same scoped late-time assumption as M01: no early shape-coordinate shift.
    return np.array([b['fid_ap']*ap_ratio,b['fid_g']*growth_ratio,0.0])

def p0(name):
    b=BINS[name]; return np.array([b['fid_ap'],b['fid_g'],0.0])

def cov3(name):
    c=np.asarray(BINS[name]['cov'],float)*COV_SCALE
    return c[np.ix_([1,2,3],[1,2,3])]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--ref',required=True)
    ap.add_argument('--case',action='append',required=True,help='lambda:path')
    ap.add_argument('--json',required=True)
    args=ap.parse_args()
    ref=load_bg(Path(args.ref))
    cases=[]
    for spec in args.case:
        ls,path=spec.split(':',1); lam=float(ls); q=lam*lam; bg=load_bg(Path(path))
        total=0.0; per={}
        for name in USE:
            r=prediction(bg,ref,name)-p0(name); C=cov3(name)
            chi=float(r@np.linalg.solve(C,r)); total+=chi
            der=r/q; Fi=float(der@np.linalg.solve(C,der))
            per[name]={'response':r.tolist(),'delta_chi2':chi,'derivative_per_q':der.tolist(),'local_fisher':Fi}
        F=total/(q*q)
        cases.append({'lambda':lam,'q':q,'delta_chi2':total,'sqrt_delta_chi2':math.sqrt(total),'F_q_from_case':F,'sigma_q_from_case':1/math.sqrt(F),'per_bin':per})
    # Smallest two q values are the local-coordinate robustness pair.
    cases.sort(key=lambda x:x['q'])
    local=cases[:2]
    F_local=sum(x['F_q_from_case'] for x in local)/len(local)
    sigma=1/math.sqrt(F_local)
    largest=cases[-1]
    classification='NONIDENTIFIABLE_IN_FROZEN_LOCAL_CONTROL_SCOPE' if largest['sqrt_delta_chi2']<1.0 else 'IDENTIFIABLE_AT_LARGEST_TESTED_DEFORMATION_IN_FROZEN_CONTROL_SCOPE'
    out={
      'schema':'KMDSB.W03.M07.B5.ShapeFitQFisher.v0.1',
      'coordinate':'q=lambda^2 after field-reflection quotient',
      'scope':'corrected DESI DR1 ShapeFit AP+growth+shape covariance; optimistic unmarginalized local control, not full likelihood',
      'classification':classification,
      'sigma_q_optimistic_unmarginalized_local':sigma,
      'local_F_q':F_local,
      'cases':cases,
      'assumptions':[
        'CLASS background H, comoving distance, normalized growth D and f are used directly',
        'AP coordinate is DH/DM ratio relative to LambdaCDM',
        'growth coordinate scales as (D f)_M07/(D f)_LCDM with present normalization held fixed',
        'late canonical-DE local deformation has zero ShapeFit early-shape coordinate in this scoped control',
        'no nuisance marginalization; sensitivity is optimistic'
      ],
      'anti_overclaim':[
        'not a full DESI likelihood',
        'NONIDENTIFIABLE here is not physical falsification',
        'no conclusion about all quintessence potentials',
        'no observational mechanism discrimination against smooth-w without a joint comparator projection'
      ]
    }
    Path(args.json).write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
