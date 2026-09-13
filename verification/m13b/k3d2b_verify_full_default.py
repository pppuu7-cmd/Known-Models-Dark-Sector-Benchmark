#!/usr/bin/env python3
"""Frozen verifier for K3D2-B default full-Boltzmann B1+B2+B3 gates."""
from __future__ import annotations
import argparse,bisect,hashlib,json,math,re
from pathlib import Path

K1=0.00022398828992555914
K10=0.0022398828992555913
H0=67.15/299792.458
REF={'zx':1.1978720736725847,'x':1.3910277872721561,'p':0.3117003532815687,'y':0.7979144626637236,'q':-0.02751848184245475,'OmegaDE':0.6885076999845492}


def rows(p:Path):
    return [[float(x) for x in l.split()] for l in p.read_text().splitlines() if l.strip() and not l.lstrip().startswith('#')]

def one(root:Path,pat:str):
    a=sorted(root.glob(pat)); assert len(a)==1,(pat,[str(x) for x in a]); return a[0]

def numbered_header(p:Path,required):
    hs=[l for l in p.read_text().splitlines() if l.lstrip().startswith('#') and all(x in l for x in required)]
    assert len(hs)==1,(p,required,hs[:3])
    return {m.group(2).strip():int(m.group(1))-1 for m in re.finditer(r'(\d+):(.+?)(?=\s+\d+:|$)',hs[0].lstrip('#').strip())}

def lin(arr,a,key):
    xs=[d['a'] for d in arr]; i=bisect.bisect_left(xs,a)
    if i==0:return arr[0][key]
    if i>=len(arr):return arr[-1][key]
    u,v=arr[i-1],arr[i]; f=(a-u['a'])/(v['a']-u['a']) if v['a']!=u['a'] else 0.
    return u[key]+f*(v[key]-u[key])

def sign(x): return 1 if x>0 else (-1 if x<0 else 0)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path,default=Path('out')); ap.add_argument('--result',type=Path,default=Path('result')); ap.add_argument('--canonical',type=Path,required=True); ap.add_argument('--prefix',default='default'); a=ap.parse_args()
    root=a.out; result=a.result; prefix=a.prefix
    bg=one(root,f'{prefix}*_background.dat'); pk=one(root,f'{prefix}*_pk.dat'); cl=one(root,f'{prefix}*_cl.dat')
    bt=numbered_header(bg,['phi_qcf','psi_qpf']); br=rows(bg)
    pts=[]
    for r in br:
        z=r[bt['z']]; aa=1/(1+z); H=r[bt['H [1/Mpc]']]; p=r[bt["phi'_qcf"]]/(aa*H); q=r[bt["psi'_qpf"]]/(aa*H)
        pts.append({'a':aa,'z':z,'H':H,'E':H/H0,'x':r[bt['phi_qcf']],'p':p,'y':r[bt['psi_qpf']],'q':q,'D':p*p-q*q,'rqcf':r[bt['(.)rho_qcf']],'rqpf':r[bt['(.)rho_qpf']],'phip':r[bt["phi'_qcf"]],'psip':r[bt["psi'_qpf"]],'dVqcf':r[bt["V'_qcf"]],'dVqpf':r[bt["V'_qpf"]]})
    pts.sort(key=lambda d:d['a']); assert pts and all(all(math.isfinite(v) for v in d.values()) and d['H']>0 for d in pts)
    def bi(aa,key): return lin(pts,aa,key)
    z5={k:bi(1/6,k) for k in ['x','p','y','q','D','E']}; d49=bi(1/5.9,'D'); today=min(pts,key=lambda d:abs(d['a']-1))
    evo=[d for d in pts if 1/6<=d['a']<=1]; crosses=[]
    for u,v in zip(evo[:-1],evo[1:]):
        if u['D']<0<=v['D']:
            f=-u['D']/(v['D']-u['D']); ac=u['a']+f*(v['a']-u['a']); crosses.append(1/ac-1)
    omega=(today['rqcf']+today['rqpf'])/(today['H']**2)
    b1={
      'finite_positive_background':True,'z5_x':abs(z5['x']-.92)<=2e-4,'z5_y':abs(z5['y']-1.02)<=2e-4,'z5_p':abs(z5['p'])<=2e-3,'z5_q':abs(z5['q'])<=2e-3,
      'one_crossing':len(crosses)==1,'crossing_match':len(crosses)==1 and abs(crosses[0]-REF['zx'])<=.02,
      'today_x':abs(today['x']-REF['x'])<=5e-3,'today_y':abs(today['y']-REF['y'])<=5e-3,'today_p':abs(today['p']-REF['p'])<=5e-3,'today_q':abs(today['q']-REF['q'])<=2e-3,
      'E0':abs(today['E']-1)<=3e-3,'OmegaDE0':abs(omega-REF['OmegaDE'])<=3e-3,'phantom_after_start':d49<0,'quintessence_today':today['D']>0,
    }
    pr=rows(pk); cr=rows(cl)
    b2={'pk_positive_finite':bool(pr) and all(len(r)>=2 and r[0]>0 and r[1]>0 and all(math.isfinite(x) for x in r) for r in pr),'cl_finite':bool(cr) and all(all(math.isfinite(x) for x in r) for r in cr),'cl_tt_ee_nonnegative':all(len(r)<3 or (r[1]>=-1e-30 and r[2]>=-1e-30) for r in cr)}

    cb=a.canonical.read_bytes(); csha=hashlib.sha256(cb).hexdigest(); canon=json.loads(cb)
    target={'khat_1':K1,'khat_10':K10}; fs=sorted(root.glob(f'{prefix}*_perturbations_k*_s.dat')); assert len(fs)==2,[str(x) for x in fs]
    mapped={}
    for f in fs:
        m=re.search(r'k\s*=\s*([0-9.eE+-]+)',f.read_text().splitlines()[0]); assert m,(f,f.read_text().splitlines()[:2]); kv=float(m.group(1)); key=min(target,key=lambda k:abs(target[k]-kv)); assert abs(target[key]-kv)/target[key]<1e-8; mapped[key]=f
    assert set(mapped)==set(target)
    b3_modes={}; max_scaled_direct=0.; hierarchy_present=True
    for key,kv in target.items():
        f=mapped[key]; ht=numbered_header(f,['delta_qcf_S','alpha_sync_to_newt']); rr=rows(f)
        required=['a','phi','psi','delta_g','theta_g','delta_ur','theta_ur','shear_ur','delta_qcf_S','delta_prime_qcf_S','delta_qpf_S','delta_prime_qpf_S','alpha_sync_to_newt','alpha_prime_sync_to_newt']
        hierarchy_present=hierarchy_present and all(x in ht for x in required)
        tr=[]
        for r in rr:
            aa=r[ht['a']]; H=bi(aa,'H'); ah=aa*H; phip=bi(aa,'phip'); psip=bi(aa,'psip'); dVx=bi(aa,'dVqcf'); dVy=bi(aa,'dVqpf'); alpha=r[ht['alpha_sync_to_newt']]; alphap=r[ht['alpha_prime_sync_to_newt']]
            dxs=r[ht['delta_qcf_S']]; dxps=r[ht['delta_prime_qcf_S']]; dys=r[ht['delta_qpf_S']]; dyps=r[ht['delta_prime_qpf_S']]
            dx=dxs+alpha*phip; dy=dys+alpha*psip
            dxp=dxps+(-2*ah*alpha*phip-aa*aa*dVx*alpha+phip*alphap); dyp=dyps+(-2*ah*alpha*psip+aa*aa*dVy*alpha+psip*alphap)
            tr.append({'a':aa,'Phi':r[ht['phi']],'Psi':r[ht['psi']],'delta_x':dx,'r':dxp/ah,'delta_y':dy,'t':dyp/ah})
        tr.sort(key=lambda d:d['a']); finite=bool(tr) and all(all(math.isfinite(v) for v in d.values()) for d in tr)
        phi5=lin(tr,1/6,'Phi'); scale=1e-5/phi5 if math.isfinite(phi5) and phi5!=0 else float('nan')
        ep={k:scale*lin(tr,1.,k) for k in ['Phi','delta_x','r','delta_y','t']}
        cref=canon['modes'][key]['fine']['endpoint']; signs={k:(sign(ep[k])==sign(cref[k])) for k in ep}
        ratios={k:abs(ep[k]/cref[k]) for k in ep}
        nonzero_x=max(abs(d['delta_x']) for d in tr)>0; nonzero_y=max(abs(d['delta_y']) for d in tr)>0
        localmax=max(abs(scale*d[k]) for d in tr for k in ['delta_x','r','delta_y','t']) if math.isfinite(scale) else float('inf'); max_scaled_direct=max(max_scaled_direct,localmax)
        checks={'finite':finite,'scale_defined':math.isfinite(scale) and scale!=0,'signs':all(signs.values()),'Phi_ratio':.5<=ratios['Phi']<=2.,'field_ratios':all(.2<=ratios[k]<=5. for k in ['delta_x','r','delta_y','t']),'qcf_nonzero':nonzero_x,'qpf_nonzero':nonzero_y}
        b3_modes[key]={'checks':checks,'all_required_checks_pass':all(checks.values()),'scale':scale,'today_scaled':ep,'canonical_today':{k:cref[k] for k in ep},'ratios':ratios,'sign_matches':signs,'max_scaled_direct':localmax}
    b2.update({'two_mode_hierarchies_present':hierarchy_present,'direct_fields_linear':max_scaled_direct<0.1})
    b3_ok=all(v['all_required_checks_pass'] for v in b3_modes.values())
    result_obj={'schema':'KMDSB.W03.M13b.K3D2BFullDefaultVerify.v0.1','B1':{'checks':b1,'all_required_checks_pass':all(b1.values()),'crossings':crosses,'z5':z5,'today':today,'OmegaDE0':omega},'B2_default':{'checks':b2,'all_required_checks_pass':all(b2.values()),'pk_rows':len(pr),'cl_rows':len(cr),'max_scaled_direct_field_perturbation':max_scaled_direct},'B3':{'modes':b3_modes,'all_required_checks_pass':b3_ok,'canonical_sha256':csha},'all_default_required_checks_pass':all(b1.values()) and all(b2.values()) and b3_ok,'K3_state_ceiling':'PARTIAL','K4_promoted':False,'K5_promoted':False,'author_model_reproduced':False,'published_V0_reproduced':False,'author_normalization_map_claimed':False,'physical_falsification':False}
    result.mkdir(parents=True,exist_ok=True); (result/'default_verify.json').write_text(json.dumps(result_obj,indent=2,sort_keys=True)+'\n'); print(json.dumps(result_obj,indent=2,sort_keys=True))
    if not result_obj['all_default_required_checks_pass']: raise SystemExit(1)
if __name__=='__main__': main()
