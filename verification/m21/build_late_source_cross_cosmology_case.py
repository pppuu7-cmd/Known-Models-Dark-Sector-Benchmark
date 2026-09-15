#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path

PROTOCOL='protocol/W04_M21_LATE_SOURCE_CROSS_COSMOLOGY_PROVIDER_REGRESSION_v0.1.md'
F_W=0.003
M_WDM_EV=3000.0
T_NCDM=0.71611
COSMOLOGIES={
 'base':  {'h':0.6731,'omega_b':0.02222,'omega_dm':0.1200},
 'h95':   {'h':0.639445,'omega_b':0.02222,'omega_dm':0.1200},
 'h105':  {'h':0.706755,'omega_b':0.02222,'omega_dm':0.1200},
 'ob95':  {'h':0.6731,'omega_b':0.021109,'omega_dm':0.1200},
 'ob105': {'h':0.6731,'omega_b':0.023331,'omega_dm':0.1200},
 'odm95': {'h':0.6731,'omega_b':0.02222,'omega_dm':0.1140},
 'odm105':{'h':0.6731,'omega_b':0.02222,'omega_dm':0.1260},
}
LANES=('clean_native','patched_native','flat_identity_predicate')

def lines(cid:str,lane:str):
 c=COSMOLOGIES[cid]; odm=c['omega_dm']; own=F_W*odm; ocdm=(1-F_W)*odm
 root={'clean_native':'clean_output','patched_native':'native_output','flat_identity_predicate':'cf_output'}[lane]
 return [
  f'root = {root}/{cid}_',
  'output = tCl,pCl',
  'headers = yes','format = class','lensing = no','non linear = none','modes = s','ic = ad','gauge = synchronous',
  f"h = {c['h']:.12g}",f"omega_b = {c['omega_b']:.12g}",f'omega_cdm = {ocdm:.12g}',
  'N_ur = 3.046','Omega_k = 0','Omega_fld = 0','Omega_scf = 0','YHe = 0.24','T_cmb = 2.725',
  'A_s = 2.196e-9','n_s = 0.9655','k_pivot = 0.05','tau_reio = 0.054','l_max_scalars = 450',
  'N_ncdm = 1','use_ncdm_psd_files = 0',f'm_ncdm = {M_WDM_EV:.12g}',f'T_ncdm = {T_NCDM:.12g}',f'omega_ncdm = {own:.12g}',
 ]

def main(cid:str,out:Path):
 if cid not in COSMOLOGIES: raise SystemExit(f'bad cosmology {cid}')
 out.mkdir(parents=True,exist_ok=True)
 for lane in LANES:(out/f'{cid}_{lane}.ini').write_text('\n'.join(lines(cid,lane))+'\n')
 c=COSMOLOGIES[cid]; odm=c['omega_dm']
 m={'schema':'KMDSB.W04.M21.CrossCosmologyInput.v0.1','protocol':PROTOCOL,'cosmology_id':cid,
    'h':c['h'],'omega_b':c['omega_b'],'omega_dm':odm,'warm_fraction':F_W,
    'omega_cdm':(1-F_W)*odm,'omega_ncdm':F_W*odm,'m_ncdm_eV':M_WDM_EV,'T_ncdm':T_NCDM,
    'Omega_k':0.0,'l_max_scalars':450,'lanes':list(LANES)}
 (out/f'{cid}_manifest.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n');print(json.dumps(m,indent=2,sort_keys=True))
if __name__=='__main__':
 if len(sys.argv)!=3:raise SystemExit('usage: build_late_source_cross_cosmology_case.py COSMOLOGY_ID OUTDIR')
 main(sys.argv[1],Path(sys.argv[2]))
