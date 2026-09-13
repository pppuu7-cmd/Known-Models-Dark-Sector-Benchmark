#!/usr/bin/env python3
"""Apply the prospectively frozen K3D2-B exact two-segment background restart.

This transformer changes only source/background.c.  It can be used in two modes:

* default: split the existing background generic_evolver call at log(a)=log(1/6);
* --recover-handoff-boundary: additionally assign the exact a=1/6 point to
  the already-frozen pre-handoff qcf/qpf branch by changing the four
  background guards from '<' to '<='.

No equation on any open interval, solver family, tolerance, sampling table,
or perturbation source is changed here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

PIN = "64bbab707faf4de4779a9e04edd180fef18d98fa"
HANDOFF = math.log(1.0 / 6.0)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def find_outer_class_call(text: str) -> tuple[int, int, str]:
    marker = "class_call(generic_evolver(background_derivs,"
    if text.count(marker) != 1:
        raise RuntimeError(f"expected exactly one background generic_evolver class_call, found {text.count(marker)}")
    start = text.index(marker)
    open_pos = text.index("(", start)
    depth = 0
    in_string = False
    escaped = False
    i = open_pos
    while i < len(text):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
            elif ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    j = i + 1
                    while j < len(text) and text[j].isspace():
                        j += 1
                    if j >= len(text) or text[j] != ";":
                        raise RuntimeError("matched class_call does not terminate with semicolon")
                    return start, j + 1, text[start:j + 1]
        i += 1
    raise RuntimeError("unterminated background generic_evolver class_call")


def split_call(block: str) -> str:
    required = {
        "loga_ini": 1,
        "loga_final": 1,
        "pvecback_integration": 1,
        "used_in_output": 1,
        "pba->loga_table": 1,
        "pba->bt_size": 1,
        "background_sources": 1,
    }
    for token, minimum in required.items():
        count = block.count(token)
        if count < minimum:
            raise RuntimeError(f"background call missing required token {token}: {count}")
    first = block.replace("loga_final", "loga_handoff_kmdsb", 1)
    second = block.replace("loga_ini", "loga_handoff_kmdsb", 1)
    return (
        "  /* KMDSB K3D2-B exact two-segment NDF15 restart at the frozen z=5 IVP. */\n"
        "  double loga_handoff_kmdsb = log(1./6.);\n"
        f"{first}\n\n"
        "  /* Restart with the exact endpoint state; evolver history is intentionally rebuilt. */\n"
        f"{second}"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("--recover-handoff-boundary", action="store_true")
    ap.add_argument("--manifest")
    args = ap.parse_args()

    root = Path(args.root)
    path = root / "source/background.c"
    before = path.read_text(encoding="utf-8")
    start, end, block = find_outer_class_call(before)
    replacement = split_call(block)
    after = before[:start] + replacement + before[end:]

    guard_replacements = 0
    if args.recover_handoff_boundary:
        guard_replacements = after.count("a < 1./6.")
        if guard_replacements != 4:
            raise RuntimeError(
                f"enabled boundary recovery expected exactly four background handoff guards, found {guard_replacements}"
            )
        after = after.replace("a < 1./6.", "a <= 1./6.")
    else:
        if "a < 1./6." in after or "a <= 1./6." in after:
            raise RuntimeError("segment-only mode found unexpected qcf/qpf handoff guards")

    if after.count("generic_evolver(background_derivs,") != 2:
        raise RuntimeError("restart transform did not produce exactly two background evolver calls")
    if after.count("loga_handoff_kmdsb") < 3:
        raise RuntimeError("restart handoff token not wired into both calls")

    path.write_text(after, encoding="utf-8")
    manifest = {
        "schema": "KMDSB.W03.M13b.K3D2BPiecewiseBackgroundRestartPatch.v0.1",
        "provider_commit": PIN,
        "handoff_loga": HANDOFF,
        "changed_files": ["source/background.c"],
        "generic_evolver_calls_before": before.count("generic_evolver(background_derivs,"),
        "generic_evolver_calls_after": after.count("generic_evolver(background_derivs,"),
        "same_state_vector_retained": block.count("pvecback_integration") >= 1,
        "same_global_output_grid_retained": block.count("pba->loga_table") >= 1 and block.count("pba->bt_size") >= 1,
        "same_output_callback_retained": block.count("background_sources") >= 1,
        "boundary_recovery_enabled": bool(args.recover_handoff_boundary),
        "boundary_guard_replacements": guard_replacements,
        "background_sha256_before": sha256_text(before),
        "background_sha256_after": sha256_text(after),
        "changes_perturbations": False,
        "changes_solver_family": False,
        "changes_tolerances": False,
        "changes_open_interval_equations": False,
    }
    if args.manifest:
        Path(args.manifest).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
