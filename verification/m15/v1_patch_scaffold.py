#!/usr/bin/env python3
"""Apply the preregistered M15 V1 alpha=0-only scaffold to pinned CLASS.

This patch deliberately adds no finite-alpha physics.  It only creates an
explicit model selector/state coordinate and rejects m15_alpha != 0 so that
reference identity can be tested before any science equation is introduced.
"""
from pathlib import Path


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one anchor, found {count}: {old!r}")
    path.write_text(text.replace(old, new, 1))


root = Path(__file__).resolve().parents[2] if "verification" in str(Path(__file__).resolve()) else Path(".")
# The workflow invokes this script from the cloned CLASS root after copying it
# there; in that case prefer cwd if include/background.h exists.
if Path("include/background.h").exists():
    root = Path(".")

background_h = root / "include/background.h"
input_c = root / "source/input.c"

replace_once(
    background_h,
    "  double Omega0_lambda;    /**< \\f$ \\Omega_{0_\\Lambda} \\f$: cosmological constant */\n",
    "  double Omega0_lambda;    /**< \\f$ \\Omega_{0_\\Lambda} \\f$: cosmological constant */\n"
    "\n"
    "  /* KMDSB M15 independent-reproduction V1 scaffold. */\n"
    "  short has_m15_gcg;      /**< explicit M15 verification selector; V1 permits alpha=0 only */\n"
    "  double m15_alpha;       /**< decomposed-GCG interaction coordinate; finite values disabled at V1 */\n",
)

replace_once(
    input_c,
    "  pba->Omega0_lambda = 1.-pba->Omega0_k-pba->Omega0_g-pba->Omega0_ur-pba->Omega0_b-pba->Omega0_cdm-pba->Omega0_ncdm_tot-pba->Omega0_dcdmdr - pba->Omega0_idr -pba->Omega0_idm;\n",
    "  pba->Omega0_lambda = 1.-pba->Omega0_k-pba->Omega0_g-pba->Omega0_ur-pba->Omega0_b-pba->Omega0_cdm-pba->Omega0_ncdm_tot-pba->Omega0_dcdmdr - pba->Omega0_idr -pba->Omega0_idm;\n"
    "  /* KMDSB M15 V1 scaffold defaults: inert unless explicitly selected. */\n"
    "  pba->has_m15_gcg = _FALSE_;\n"
    "  pba->m15_alpha = 0.;\n",
)

replace_once(
    input_c,
    "  /* ** END OF BUDGET EQUATION ** */\n\n  /** 8.a) If Omega fluid is different from 0 */\n",
    "  /* ** END OF BUDGET EQUATION ** */\n\n"
    "  /* KMDSB M15 independent-reproduction V1 selector.\n"
    "     V1 intentionally contains no finite-alpha equations: any nonzero\n"
    "     value must fail before background/perturbation evolution. */\n"
    "  class_call(parser_read_double(pfc,\"m15_alpha\",&param1,&flag1,errmsg),\n"
    "             errmsg,\n"
    "             errmsg);\n"
    "  if (flag1 == _TRUE_) {\n"
    "    pba->has_m15_gcg = _TRUE_;\n"
    "    pba->m15_alpha = param1;\n"
    "    class_test(fabs(pba->m15_alpha) > 1.e-15,\n"
    "               errmsg,\n"
    "               \"KMDSB M15 V1 scaffold accepts only m15_alpha=0; finite-alpha physics is not yet authorized\");\n"
    "  }\n\n"
    "  /** 8.a) If Omega fluid is different from 0 */\n",
)

print("M15_V1_SCAFFOLD_PATCH=APPLIED")
