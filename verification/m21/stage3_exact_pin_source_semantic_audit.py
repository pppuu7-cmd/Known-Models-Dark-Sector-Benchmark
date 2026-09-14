#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PIN = "e85808324f51fc694d12e3ed7439552a3c3f9540"
PARAMETERS = [
    "recfast_Nz0",
    "tol_thermo_integration",
    "recfast_x_He0_trigger_delta",
    "recfast_x_H0_trigger_delta",
    "l_logstep",
    "l_linstep",
    "hyper_sampling_flat",
    "hyper_sampling_curved_low_nu",
    "hyper_sampling_curved_high_nu",
    "hyper_nu_sampling_step",
    "hyper_phi_min_abs",
    "hyper_x_tol",
    "hyper_flat_approximation_nu",
]


def text_files(root: Path):
    for p in root.rglob('*'):
        if not p.is_file() or '.git' in p.parts:
            continue
        try:
            data=p.read_text(errors='strict')
        except Exception:
            continue
        yield p, data


def occurrences(root: Path, token: str) -> list[dict]:
    out=[]
    for p,data in text_files(root):
        for i,line in enumerate(data.splitlines(),1):
            if token in line:
                out.append({'path':str(p.relative_to(root)),'line':i,'text':line.strip()[:300]})
    return out


def runtime_occ(xs: list[dict]) -> list[dict]:
    # Declarations/defaults and user precision profiles are not runtime consumption.
    excluded_prefixes=('include/precisions.h','cl_ref.pre','pk_ref.pre','cl_permille.pre','pk_permille.pre','README','doc/')
    return [x for x in xs if not x['path'].startswith(excluded_prefixes) and not x['path'].endswith(('.pre','.ini','.param','.md','.html','.js'))]


def precision_default(precisions: str, key: str):
    pat=re.compile(r'class_precision_parameter\(\s*'+re.escape(key)+r'\s*,\s*[^,]+\s*,\s*([^\)]+)\)')
    m=pat.search(precisions)
    return None if m is None else m.group(1).strip()


def main(class_root: Path, benchmark_root: Path, out: Path):
    precisions=(class_root/'include/precisions.h').read_text()
    input_c=(class_root/'source/input.c').read_text()
    thermo=(class_root/'source/thermodynamics.c').read_text()
    transfer=(class_root/'source/transfer.c').read_text()
    cl_ref=(class_root/'cl_ref.pre').read_text()
    benchmark=(benchmark_root/'verification/m21/mixed_cold_warm_k1_reference.py').read_text()

    occ={k:occurrences(class_root,k) for k in PARAMETERS}
    runtime={k:runtime_occ(v) for k,v in occ.items()}
    defaults={k:precision_default(precisions,k) for k in PARAMETERS}

    checks={
      'cl_ref_has_recfast_Nz0': 'recfast_Nz0=100000' in cl_ref.replace(' ',''),
      'recfast_Nz0_not_declared_precision': defaults['recfast_Nz0'] is None,
      'recfast_Nz0_no_runtime_consumer': len(runtime['recfast_Nz0']) == 0,
      'input_warns_unused_not_fails': '[WARNING: input line not used:' in input_c and 'unused_parameters' in input_c,
      'tol_thermo_declared': defaults['tol_thermo_integration'] is not None,
      'tol_thermo_runtime_consumer': any(x['path']=='source/thermodynamics.c' for x in runtime['tol_thermo_integration']),
      'frozen_cosmology_flat': '"Omega_k = 0"' in benchmark,
      'transfer_flat_uses_hyper_sampling_flat': 'ppr->hyper_sampling_flat' in transfer and 'if (ptw->sgnK == 0)' in transfer,
      'transfer_flat_uses_hyper_phi_min_abs': 'ppr->hyper_phi_min_abs' in transfer,
      'curved_sampling_runtime_in_transfer': all(any(x['path']=='source/transfer.c' for x in runtime[k]) for k in ['hyper_sampling_curved_low_nu','hyper_sampling_curved_high_nu','hyper_nu_sampling_step']),
      'hyper_x_tol_runtime_in_transfer': any(x['path']=='source/transfer.c' for x in runtime['hyper_x_tol']),
      'hyper_flat_approx_runtime_in_transfer': any(x['path']=='source/transfer.c' for x in runtime['hyper_flat_approximation_nu']),
      'hyper_phi_default_is_stage3_value': defaults['hyper_phi_min_abs'] in {'1.0e-10','1.e-10'},
      'hyper_x_tol_default_is_stage3_value': defaults['hyper_x_tol'] in {'1.0e-4','1.e-4'},
    }

    result={
      'schema':'KMDSB.W04.M21.Stage3ExactPinSourceSemanticAudit.v0.1',
      'provider':f'lesgourg/class_public@{PIN}',
      'parameters':PARAMETERS,
      'defaults':defaults,
      'occurrences':occ,
      'runtime_occurrences':runtime,
      'checks':checks,
      'recfast_trigger_runtime_counts':{
        'recfast_x_He0_trigger_delta':len(runtime['recfast_x_He0_trigger_delta']),
        'recfast_x_H0_trigger_delta':len(runtime['recfast_x_H0_trigger_delta']),
      },
      'classification':'M21_STAGE3_SOURCE_SEMANTIC_AUDIT_PASS_WITH_SCOPE' if all(checks.values()) else 'M21_STAGE3_SOURCE_SEMANTIC_AUDIT_REQUIRES_REVIEW',
      'K1_promoted':False,
      'physical_falsification':False,
      'interpretation_ceiling':'Source consumption and branch reachability only; numerical stage-3 aggregate remains authoritative for sufficiency.'
    }
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({
      'classification':result['classification'],
      'checks':checks,
      'runtime_counts':{k:len(runtime[k]) for k in PARAMETERS},
      'recfast_trigger_runtime_counts':result['recfast_trigger_runtime_counts'],
    },indent=2,sort_keys=True))
    if result['classification'] != 'M21_STAGE3_SOURCE_SEMANTIC_AUDIT_PASS_WITH_SCOPE':
        raise SystemExit(1)

if __name__=='__main__':
    if len(sys.argv)!=4:
        raise SystemExit('usage: stage3_exact_pin_source_semantic_audit.py CLASS_ROOT BENCHMARK_ROOT OUT.json')
    main(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
