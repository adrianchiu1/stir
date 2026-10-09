#!/usr/bin/env python
"""Print or write every listed futures contract in a date range with its
reference window, last trade date and settlement rule (manifest + committed
calendars; no network).

Examples
    python scripts/contract_table.py --start 2026-10-07 --end 2026-10-07
    python scripts/contract_table.py --start 2018-01-01 --end 2027-12-31 --instrument sofr3m_fut --out exports/sr3.csv
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from stircurve.marketdata.contracts import contract_table  # noqa: E402
from stircurve.marketdata.manifest import load_manifest  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ccy", default="usd")
    ap.add_argument("--start", required=True, type=dt.date.fromisoformat)
    ap.add_argument("--end", required=True, type=dt.date.fromisoformat)
    ap.add_argument("--instrument", action="append", help="futures instrument(s); default all")
    ap.add_argument("--out", help="CSV path (default: print)")
    args = ap.parse_args(argv)
    t = contract_table(load_manifest(args.ccy), args.start, args.end, args.instrument)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        t.to_csv(args.out, index=False)
        print(f"{len(t)} contracts -> {args.out}")
    else:
        cols = ["instrument", "contract", "bbg_ticker", "cycle", "ref_start", "ref_end", "last_trade",
                "final_settlement", "first_listed", "last_quote", "converted_on"]
        print(t[cols].to_string(index=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
