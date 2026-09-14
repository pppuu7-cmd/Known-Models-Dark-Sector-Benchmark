#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, math, pathlib, re

PIN='e85808324f51fc694d12e3ed7439552a3c3f9540'
PROTOCOL='protocol/W04_M21_AUTO_QGRID_IDENTITY_AUDIT_v0.1.md'

def patch(root:pathlib.Path, manifest:pathlib.Path):
    p=root/'source/background.c'; before=p.read_text()
    marker='    class_alloc(pba->dlnf0_dlnq_ncdm[k],\n'
    if before.count(marker)!=1: raise RuntimeError(f'anchor count {before.count(marker)}')
    ins='''    /* KMDSB M21 output-only q-grid audit. */
    fprintf(stdout,"KMDSB_QGRID_BEGIN species=%d strategy=%d qsize=%d deg=%.17g factor=%.17g\\n",
            k,(int)pba->ncdm_quadrature_strategy[k],pba->q_size_ncdm[k],pba->deg_ncdm[k],pba->factor_ncdm[k]);
    for (int kmdsb_qi=0; kmdsb_qi<pba->q_size_ncdm[k]; kmdsb_qi++) {
      fprintf(stdout,"KMDSB_QGRID_POINT species=%d i=%d q=%.17g w=%.17g\\n",
              k,kmdsb_qi,pba->q_ncdm[k][kmdsb_qi],pba->w_ncdm[k][kmdsb_qi]);
    }
    fprintf(stdout,"KMDSB_QGRID_END species=%d\\n",k);
    fflush(stdout);

'''
    after=before.replace(marker,ins+marker,1); p.write_text(after)
    m={'schema':'KMDSB.W04.M21.QGridInstrumentation.v0.1','changed_file':'source/background.c','insertions':1,'output_only':True,'changes_arrays':False,'changes_equations':False,'changes_inputs':False,'changes_tolerances':False,'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest()}
    manifest.write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')

def parse_lane(lane:str, log:pathlib.Path, rc:pathlib.Path, manifest:pathlib.Path, out:pathlib.Path):
    text=log.read_text(errors='replace')
    b=re.findall(r'KMDSB_QGRID_BEGIN species=(\d+) strategy=(\d+) qsize=(\d+) deg=([^ ]+) factor=([^\n]+)',text)
    if len(b)!=1: raise RuntimeError(f'begin records {len(b)}')
    sp,st,n,deg,factor=b[0]; n=int(n)
    pts=re.findall(r'KMDSB_QGRID_POINT species=(\d+) i=(\d+) q=([^ ]+) w=([^\n]+)',text)
    if len(pts)!=n: raise RuntimeError(f'points {len(pts)} != {n}')
    pts=sorted(pts,key=lambda x:int(x[1])); q=[float(x[2]) for x in pts]; w=[float(x[3]) for x in pts]
    vals=q+w+[float(deg),float(factor)]
    if not all(math.isfinite(x) for x in vals): raise RuntimeError('nonfinite q-grid record')
    payload={'strategy':int(st),'q_size':n,'q':q,'w':w}; canon=json.dumps(payload,sort_keys=True,separators=(',',':')).encode()
    rci=int(rc.read_text().strip())
    obj={'schema':'KMDSB.W04.M21.AutoQGridLane.v0.1','lane':lane,'provider':f'lesgourg/class_public@{PIN}','strategy':int(st),'q_size':n,'q':q,'w':w,'deg_ncdm':float(deg),'factor_ncdm':float(factor),'qgrid_sha256':hashlib.sha256(canon).hexdigest(),'provider_rc':rci,'instrumentation':json.loads(manifest.read_text()),'all_required_checks_pass':rci==0}
    out.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
    if rci!=0: raise SystemExit(1)

def aggregate(root:pathlib.Path,out:pathlib.Path):
    lanes={}
    for lane in ['f2','f3','f4','f3_manual']:
        fs=list(root.glob(f'**/{lane}.json')); lanes[lane]=json.loads(fs[0].read_text()) if len(fs)==1 else None
    required=all(v is not None and v.get('all_required_checks_pass') and v.get('provider_rc')==0 for v in lanes.values())
    exact_grid=norm_diff=negative_diff=False
    if required:
        phys=[lanes[x] for x in ['f2','f3','f4']]
        exact_grid=all((p['strategy'],p['q_size'],p['q'],p['w'])==(phys[0]['strategy'],phys[0]['q_size'],phys[0]['q'],phys[0]['w']) for p in phys[1:])
        norm_diff=len({(p['deg_ncdm'],p['factor_ncdm']) for p in phys})>1
        negative_diff=lanes['f3_manual']['qgrid_sha256']!=lanes['f3']['qgrid_sha256']
    if required and exact_grid and norm_diff and negative_diff: cls='M21_AUTO_QGRID_IDENTICAL_ACROSS_FRACTIONS'
    elif required and (not exact_grid) and negative_diff: cls='M21_AUTO_QGRID_FRACTION_DEPENDENT'
    else: cls='M21_AUTO_QGRID_AUDIT_BLOCKED'
    obj={'schema':'KMDSB.W04.M21.AutoQGridIdentityAudit.v0.1','protocol':PROTOCOL,'provider':f'lesgourg/class_public@{PIN}','lanes':lanes,'physical_grids_exactly_identical':exact_grid,'abundance_normalization_differs':norm_diff,'manual_negative_control_grid_differs':negative_diff,'classification':cls,'K1_promoted':False,'physical_falsification':False}
    out.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(json.dumps({'classification':cls,'physical_grids_exactly_identical':exact_grid,'abundance_normalization_differs':norm_diff,'manual_negative_control_grid_differs':negative_diff},indent=2))
    if cls=='M21_AUTO_QGRID_AUDIT_BLOCKED': raise SystemExit(1)

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True)
    p=sub.add_parser('patch'); p.add_argument('root',type=pathlib.Path); p.add_argument('manifest',type=pathlib.Path)
    p=sub.add_parser('parse'); p.add_argument('lane'); p.add_argument('log',type=pathlib.Path); p.add_argument('rc',type=pathlib.Path); p.add_argument('manifest',type=pathlib.Path); p.add_argument('out',type=pathlib.Path)
    p=sub.add_parser('aggregate'); p.add_argument('root',type=pathlib.Path); p.add_argument('out',type=pathlib.Path)
    a=ap.parse_args()
    if a.cmd=='patch': patch(a.root,a.manifest)
    elif a.cmd=='parse': parse_lane(a.lane,a.log,a.rc,a.manifest,a.out)
    else: aggregate(a.root,a.out)
if __name__=='__main__': main()
