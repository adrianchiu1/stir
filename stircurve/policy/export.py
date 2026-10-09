"""Write a front end's results for one as-of date.

``exports/<ccy>/<family>/<as_of>/`` (shared with the team, D13): meetings.csv
(policy outputs), parcels.csv (fitted flat forwards, prior, identification),
instruments.csv (quotes, residuals, weights, status), report.md (one page).
``store_curve`` writes the parcels to the local, git-ignored curve store
``data/curves/<ccy>/<family>/front_end/<as_of>.csv`` and nothing else.
"""
from __future__ import annotations

from pathlib import Path

from .. import DATA_DIR, REPO_ROOT
from ..curves.front_end import FrontEnd
from ..quality import battery
from .outputs import meeting_table

EXPORTS_DIR = REPO_ROOT / "exports"
STORE_DIR = DATA_DIR / "curves"


def write_exports(fe: FrontEnd, root: Path = EXPORTS_DIR) -> Path:
    out = root / fe.ccy.lower() / fe.cfg["front_end"]["family"] / fe.as_of.isoformat()
    out.mkdir(parents=True, exist_ok=True)
    meeting_table(fe).to_csv(out / "meetings.csv", index=False, lineterminator="\n")
    battery.identification_table(fe).to_csv(out / "parcels.csv", index=False, lineterminator="\n")
    battery.instrument_table(fe).to_csv(out / "instruments.csv", index=False, lineterminator="\n")
    (out / "report.md").write_text(battery.report(fe), encoding="utf-8")
    return out


def store_curve(fe: FrontEnd, root: Path = STORE_DIR) -> Path:
    p = root / fe.ccy.lower() / fe.cfg["front_end"]["family"] / "front_end" / f"{fe.as_of.isoformat()}.csv"
    p.parent.mkdir(parents=True, exist_ok=True)
    battery.identification_table(fe).to_csv(p, index=False, lineterminator="\n")
    return p
