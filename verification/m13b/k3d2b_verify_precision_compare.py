#!/usr/bin/env python3
"""Frozen default-vs-cl_ref precision comparator for K3D2-B."""
from __future__ import annotations
import argparse,bisect,json,math,re
from pathlib import Path
H0=67.15/299792.458

def rows(p): return [[float(x) for x in l.split()] for l in Path(p).read_text().splitlines() if l.strip() and not l.lstrip().startswith('#')]
def one(root,pat):
    a=sorted(Path(root).glob(pat)); assert len(a)==1,(pat,[str(x) for x in a]); return a[0]
def header(p,req):
    hs=[l for l in Path(p).read_text().splitlines() if l.lstrip().startswith('#') and all(x in l for x in req)]; assert len(hs)==1,(p,req,hs[:3]); return {m.group(2).strip():int(m.group(1))-1 for m in re.finditer(r'(\d+):(.+?)(?=\s+\d+:|$)',hs[0].lstrip('#').strip())}
def bg_summary(root,prefix):
    p=one(root,f'{prefix}*_background.dat'); h=header(p,['phi_qcf','psi_qpf']); a=[]
    for r in rows(p):
        z=r[h['z']]; aa=1/(1+z); H=r[h['H [1/Mpc]']]; pp=r[h["phi'_qcf"]]/(aa*H); qq=r[h["psi'_qpf"]]/(aa*H); a.append({'a':aa,'D':pp*pp-qq*qq,'x':r[h['phi_qcf']],'p':pp,'y':r[h['psi_qpf']],'q':qq,'H':H})
    a.sort(key=lambda d:d['a']); cr=[]
    for u,v in zip(a[:-1],a[1:]):
        if u['D']<0<=v['D'] and u['a']>=1/6:
            f=-u['D']/(v['D']-u['D']); ac=u['a']+f*(v['a']-u['a']); cr.append(1/ac-1)
    t=min(a,key=lambda d:abs(d['a']-1)); assert len(cr)==1,(prefix,cr)
    return {'crossing':cr[0],'today':{k:t[k] for k in ['x','p','y','q','H']}}
def loginterp(arr,x):
    xs=[r[0] for r in arr]; i=bisect.bisect_left(xs,x)
    if i==0:return arr[0][1]
    if i>=len(arr):return arr[-1][1]
    x0,y0=arr[i-1][:2]; x1,y1=arr[i][:2]; f=(math.log(x)-math.log(x0))/(math.log(x1)-math.log(x0)); return math.exp(math.log(y0)+f*(math.log(y1)-math.log(y0)))
def l2_pk(a,b):
    b=[r for r in b if r[0]>0 and r[1]>0]; common=[r for r in a if r[0]>0 and r[1]>0 and b[0][0]<=r[0]<=b[-1][0]]; return math.sqrt(sum((r[1]-loginterp(b,r[0]))**2 for r in common)/max(sum(r[1]**2 for r in common),1e-300)),len(common)
def l2_tt(a,b):
    da={int(round(r[0])):r[1] for r in a if len(r)>1 and 30<=r[0]<=1200}; db={int(round(r[0])):r[1] for r in b if len(r)>1 and 30<=r[0]<=1200}; ell=sorted(set(da)&set(db)); assert ell
    return math.sqrt(sum((da[l]-db[l])**2 for l in ell)/max(sum(da[l]**2 for l in ell),1e-300)),len(ell)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--default-root',required=True); ap.add_argument('--ref-root',required=True); ap.add_argument('--result',required=True); a=ap.parse_args()
    bd=bg_summary(a.default_root,'default'); br=bg_summary(a.ref_root,'ref')
    pkd=rows(one(a.default_root,'default*_pk.dat')); pkr=rows(one(a.ref_root,'ref*_pk.dat')); cld=rows(one(a.default_root,'default*_cl.dat')); clr=rows(one(a.ref_root,'ref*_cl.dat'))
    pkl2,npk=l2_pk(pkd,pkr); ttl2,nell=l2_tt(cld,clr)
    c={'crossing_abs_le_2e_3':abs(bd['crossing']-br['crossing'])<=2e-3,'today_fields_each_le_1e_3':max(abs(bd['today'][k]-br['today'][k]) for k in ['x','p','y','q'])<=1e-3,'pk_L2_le_5e_3':pkl2<=5e-3,'TT_L2_le_5e_3':ttl2<=5e-3,'ref_pk_finite_positive':all(len(r)>=2 and r[0]>0 and r[1]>0 and all(math.isfinite(x) for x in r) for r in pkr),'ref_cl_finite':all(all(math.isfinite(x) for x in r) for r in clr)}
    out={'schema':'KMDSB.W03.M13b.K3D2BPrecisionCompare.v0.1','checks':c,'all_required_checks_pass':all(c.values()),'default_background':bd,'reference_background':br,'crossing_abs_difference':abs(bd['crossing']-br['crossing']),'today_field_absolute_differences':{k:abs(bd['today'][k]-br['today'][k]) for k in ['x','p','y','q']},'pk_normalized_L2':pkl2,'pk_common_rows':npk,'TT_normalized_L2':ttl2,'TT_common_ell_count':nell,'K3_state_ceiling':'PARTIAL'}
    Path(a.result).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(json.dumps(out,indent=2,sort_keys=True)); assert out['all_required_checks_pass'],out
if __name__=='__main__': main()
