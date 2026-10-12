#!/usr/bin/env python
"""Build the USD EFFR-family front end (FF-futures and OIS curves) for as-of dates and write the results.

Reads data/ only (market CSVs, reference data). Writes exports/usd/effr/<as_of>/
(meetings.csv, parcels.csv, instruments.csv, basis.csv, report.md); --store also writes
the parcels to the local, git-ignored curve store data/curves/.

Examples
    python scripts/front_end.py --as-of 2026-10-07
    python scripts/front_end.py --as-of 2019-06-12 --as-of 2026-10-07 --store
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from stircurve.curves.front_end import build  # noqa: E402
from stircurve.policy.export import EXPORTS_DIR, store_curve, write_exports  # noqa: E402
from stircurve.policy.outputs import meeting_table  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--as-of", action="append", required=True, type=dt.date.fromisoformat)
    ap.add_argument("--ccy", default="usd")
    ap.add_argument("--exports", type=Path, default=EXPORTS_DIR)
    ap.add_argument("--store", action="store_true", help="also write the local curve store (data/curves)")
    args = ap.parse_args(argv)
    rc = 0
    for d in args.as_of:
        try:
            fe = build(d, args.ccy)
        except ValueError as exc:
            print(f"{d}: {exc}")
            rc = 1
            continue
        out = write_exports(fe, args.exports)
        for c in fe.curves.values():
            print(f"{d} {c.name}: {len(c.used)} quotes, {len(c.dropped)} dropped, {len(c.excluded)} excluded; "
                  f"replica reaches {c.wirp_reach} meetings -> {out}")
        if args.store:
            print("  store:", ", ".join(str(p) for p in store_curve(fe)))
        mt = meeting_table(fe)
        print(mt[["curve", "decision_date", "synthetic", "implied_rate", "n_moves", "pct_move", "replica_rate",
                  "fit_minus_replica_bp"]].groupby("curve").head(12).to_string(index=False))
    return rc


if __name__ == "__main__":
    sys.exit(main())
