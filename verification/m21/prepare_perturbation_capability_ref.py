#!/usr/bin/env python3
from __future__ import annotations
import hashlib, importlib.util, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GEN = HERE / 'mixed_cold_warm_k1_reference.py'
PROTOCOL = 'protocol/W04_M21_PERTURBATION_OUTPUT_CAPABILITY_RECON_v0.1.md'
ADD = ['write_thermodynamics = yes', 'k_output_values = 0.1']

def H(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def loadmod():
    s = importlib.util.spec_from_file_location('m21_k1_gen_cap', GEN)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

def main(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    full = out / '_full'
    loadmod().prepare(full)
    src = full / 'ref.ini'
    lines = src.read_text().splitlines()
    keys = [x.split('=',1)[0].strip() for x in lines if '=' in x]
    for forbidden in ['write_thermodynamics','write thermodynamics','k_output_values']:
        if forbidden in keys:
            raise RuntimeError(f'source ref unexpectedly sets {forbidden}')
    dst_lines = lines + ADD
    dst = out / 'ref.ini'
    dst.write_text('\n'.join(dst_lines) + '\n')
    # Preserve every original line exactly and append only the two frozen capability lines.
    if dst_lines[:len(lines)] != lines or dst_lines[len(lines):] != ADD:
        raise RuntimeError('ref capability case drift')
    manifest = {
        'schema':'KMDSB.W04.M21.PerturbationCapabilityRefCase.v0.1',
        'protocol':PROTOCOL,
        'generator':str(GEN),
        'source_ref_sha256':H(src),
        'capability_ref_sha256':H(dst),
        'source_line_count':len(lines),
        'capability_line_count':len(dst_lines),
        'physical_lines_preserved':True,
        'added_lines':ADD,
        'requested_k_Mpc_inv':[0.1],
    }
    (out / 'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    for p in full.iterdir(): p.unlink()
    full.rmdir()
    print(json.dumps(manifest,indent=2,sort_keys=True))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: prepare_perturbation_capability_ref.py OUTDIR')
    main(Path(sys.argv[1]))
