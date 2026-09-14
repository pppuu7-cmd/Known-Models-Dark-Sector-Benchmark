#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np
from classy import Class

SOURCES=['t0','t1','t2','p']
TAU_MIN=146.1893481575377
TAU_MAX=488.2339443484317
CASES=['ref','f2','f3','f4']

def H(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def parse(p:Path):
 out=[]
 for raw in p.read_text(errors='replace').splitlines():
  s=raw.split('#',1)[0].strip()
  if not s: continue
  if '=' not in s: raise RuntimeError(f'unparsed {p}: {raw!r}')
  k,v=(x.strip() for x in s.split('=',1)); out.append((k,v))
 return out

def main(case_dir:Path,profile:Path,config:Path,outdir:Path,lane:str):
 cfg=json.load(open(config)); anchors=np.asarray(cfg['k_anchors_unrounded_Mpc_inv'],float)
 if anchors.shape!=(5,) or np.any(~np.isfinite(anchors)) or np.any(anchors<=0) or np.any(np.diff(anchors)<=0): raise RuntimeError('invalid frozen k anchors')
 outdir.mkdir(parents=True,exist_ok=True); summary={'schema':'KMDSB.W04.M21.DirectCMBSourcesLane.v0.1','protocol':'protocol/W04_M21_CONDITIONAL_CMB_SOURCE_BRANCH_SIGNATURE_v0.1.md','lane':lane,'profile_sha256':H(profile),'config_sha256':H(config),'cases':{}}
 pitems=parse(profile); pkeys=[k for k,_ in pitems]
 if len(pkeys)!=len(set(pkeys)): raise RuntimeError('duplicate profile keys')
 for case in CASES:
  ini=case_dir/f'{case}.ini'; items=parse(ini); keys=[k for k,_ in items]
  if len(keys)!=len(set(keys)): raise RuntimeError(f'duplicate ini keys {case}')
  overlap=set(keys)&set(pkeys)
  if overlap: raise RuntimeError(f'ini/profile duplicate key(s) {case}: {sorted(overlap)}')
  pars={k:v for k,v in items+pitems}
  cosmo=Class(); cosmo.set(pars)
  try:
   sources,k,tau=cosmo.get_sources()
   k=np.asarray(k,float); tau=np.asarray(tau,float)
   if k.ndim!=1 or tau.ndim!=1 or k.size<3 or tau.size<16 or np.any(~np.isfinite(k)) or np.any(~np.isfinite(tau)) or np.any(k<=0) or np.any(np.diff(k)<=0) or np.any(np.diff(tau)<=0): raise RuntimeError(f'invalid native grid {case}')
   if anchors[0]<=k[0] or anchors[-1]>=k[-1]: raise RuntimeError(f'anchor outside strict native k range {case}: {k[0]}..{k[-1]}')
   mask=(tau>=TAU_MIN)&(tau<=TAU_MAX); tw=tau[mask]
   if tw.size<16: raise RuntimeError(f'insufficient source tau window {case}: {tw.size}')
   lk=np.log(k); lka=np.log(anchors); saved={'tau_Mpc':tw,'k_anchor_Mpc_inv':anchors}
   for name in SOURCES:
    if name not in sources: raise RuntimeError(f'missing source {name} in {case}: {sorted(sources)}')
    arr=np.asarray(sources[name],float)
    if arr.shape!=(k.size,tau.size) or np.any(~np.isfinite(arr)): raise RuntimeError(f'invalid source array {case}/{name}: {arr.shape}')
    vals=[]
    for x in lka:
     j=int(np.searchsorted(lk,x));
     if j<=0 or j>=lk.size: raise RuntimeError('interpolation bracket failure')
     w=(x-lk[j-1])/(lk[j]-lk[j-1]); vals.append(((1.0-w)*arr[j-1,:]+w*arr[j,:])[mask])
    saved[name]=np.asarray(vals,float)
   np.savez_compressed(outdir/f'{case}_cmb_sources.npz',**saved)
   summary['cases'][case]={'ini_sha256':H(ini),'native_k_size':int(k.size),'native_tau_size':int(tau.size),'native_k_min_Mpc_inv':float(k[0]),'native_k_max_Mpc_inv':float(k[-1]),'window_tau_count':int(tw.size),'source_names':SOURCES,'output_sha256':H(outdir/f'{case}_cmb_sources.npz')}
  finally:
   try: cosmo.struct_cleanup()
   except Exception: pass
   try: cosmo.empty()
   except Exception: pass
 (outdir/'lane_sources_meta.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
 print(json.dumps(summary,indent=2,sort_keys=True))

if __name__=='__main__':
 ap=argparse.ArgumentParser(); ap.add_argument('case_dir',type=Path); ap.add_argument('profile',type=Path); ap.add_argument('config',type=Path); ap.add_argument('outdir',type=Path); ap.add_argument('lane'); a=ap.parse_args(); main(a.case_dir,a.profile,a.config,a.outdir,a.lane)
