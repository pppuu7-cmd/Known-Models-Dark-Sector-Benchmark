#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: historical_camb_outtransf_compat.py <CAMB-tree>')

root = Path(sys.argv[1])
p = root / 'equations.f90'
s = p.read_text()
start_marker = '    subroutine outtransf(EV, y, Arr)'
end_marker = '    end subroutine outtransf'
if s.count(start_marker) != 1 or s.count(end_marker) < 1:
    raise SystemExit('frozen outtransf anchors not unique/present')
start = s.index(start_marker)
end = s.index(end_marker, start) + len(end_marker)
block = s[start:end]
if block.count('type(EvolutionVars) EV') != 1:
    raise SystemExit('unexpected EvolutionVars dummy declaration')
# Mechanical, case-preserving identifier rename only inside outtransf.
# Replace token EV when delimited by non-identifier characters.
import re
new_block, n = re.subn(r'(?<![A-Za-z0-9_])EV(?![A-Za-z0-9_])', 'EVout', block)
if n < 2:
    raise SystemExit(f'unexpected rename count {n}')
# Guard against any non-identifier transformation.
restored = re.sub(r'(?<![A-Za-z0-9_])EVout(?![A-Za-z0-9_])', 'EV', new_block)
if restored != block:
    raise SystemExit('compatibility transform is not a pure EV token rename')
p.write_text(s[:start] + new_block + s[end:])
print(f'KMDSB_HISTORICAL_CAMB_OUTTRANSF_COMPAT_RENAMES={n}')
