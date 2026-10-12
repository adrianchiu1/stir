"""Write a front end's results for one as-of date.

``exports/<ccy>/<family>/<as_of>/`` (shared with the team, D13): meetings.csv
(policy outputs per curve and meeting), parcels.csv (fitted flat forwards,
identification, replica), instruments.csv (quotes, residuals, weights, status),
basis.csv (FF minus OIS per meeting), report.md (one page). ``store_curve`` writes
the parcels to the local, git-ignored curve store ``data/curves/<ccy>/<family>/
<curve>/<as_of>.csv`` and nothing else.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from .. import DATA_DIR, REPO_ROOT
from ..curves.front_end import FrontEnd
from ..quality import battery
from .outputs import basis_table, meeting_table

EXPORTS_DIR = REPO_ROOT / "exports"
STORE_DIR = DATA_DIR / "curves"


def write_exports(fe: FrontEnd, root: Path = EXPORTS_DIR) -> Path:
    out = root / fe.ccy.lower() / fe.family / fe.as_of.isoformat()
    out.mkdir(parents=True, exist_ok=True)
    meeting_table(fe).to_csv(out / "meetings.csv", index=False, lineterminator="\n")
    pd.concat([battery.parcel_table(fe, c) for c in fe.curves.values()], ignore_index=True).to_csv(
        out / "parcels.csv", index=False, lineterminator="\n")
    pd.concat([battery.instrument_table(fe, c) for c in fe.curves.values()], ignore_index=True).to_csv(
        out / "instruments.csv", index=False, lineterminator="\n")
    basis_table(fe).to_csv(out / "basis.csv", index=False, lineterminator="\n")
    (out / "report.md").write_text(battery.report(fe), encoding="utf-8")
    return out


def store_curve(fe: FrontEnd, root: Path = STORE_DIR) -> list[Path]:
    paths = []
    for c in fe.curves.values():
        p = root / fe.ccy.lower() / fe.family / c.name / f"{fe.as_of.isoformat()}.csv"
        p.parent.mkdir(parents=True, exist_ok=True)
        battery.parcel_table(fe, c).to_csv(p, index=False, lineterminator="\n")
        paths.append(p)
    return paths
