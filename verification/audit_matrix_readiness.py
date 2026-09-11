#!/usr/bin/env python3
import csv, json
from pathlib import Path

path=Path('matrices/mandatory_properties_matrix.csv')
with path.open(newline='',encoding='utf-8') as f:
    rows=list(csv.DictReader(f))
gates=[c for c in rows[0] if c.startswith(tuple(f'K{i}_' for i in range(10)))]
assert len(gates)==10
open_states={'OPEN','NOT_TESTED','QUEUED','PENDING'}

def summary(rr):
    vals=[(r[c] or '').strip() for r in rr for c in gates]
    total=len(vals)
    assessed=sum(v not in open_states for v in vals)
    positive=sum(v.startswith('PASS') or v.startswith('SUPPORTED') for v in vals)
    k0=[(r[gates[0]] or '').strip() for r in rr]
    return {
      'families':len(rr),
      'gate_cells':total,
      'assessed_cells':assessed,
      'assessed_fraction':assessed/total,
      'positive_cells':positive,
      'positive_fraction':positive/total,
      'K0_assessed':sum(v not in open_states for v in k0),
      'K0_positive':sum(v.startswith('PASS') or v.startswith('SUPPORTED') for v in k0)
    }

out={
 'schema':'kmdsb_readiness_snapshot_v0.1',
 'definition_assessed':'status is not exact OPEN, NOT_TESTED, QUEUED, or PENDING; blocked/partial/not-established outcomes count as investigated, not as positive',
 'definition_positive':'status begins PASS or SUPPORTED only',
 'all_rows_including_M00_control':summary(rows),
 'mechanism_rows_excluding_M00_control':summary([r for r in rows if r['benchmark_id']!='M00'])
}
Path('audits').mkdir(exist_ok=True)
Path('audits/KMDSB_READINESS_SNAPSHOT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
