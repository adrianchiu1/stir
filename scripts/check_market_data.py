#!/usr/bin/env python
"""Load and validate the dumped market-data CSVs against the manifest.

Reports unknown columns, malformed files, out-of-range values and futures quoted
outside their listing window (blocking: exit 2), plus missing expected columns,
stale values and values outside an instrument's first/last dates (warnings).

Examples
    python scripts/check_market_data.py --start 2026-10-07 --end 2026-10-07
    python scripts/check_market_data.py                                  # every file under data/market/usd
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from stircurve.marketdata import loader  # noqa: E402
from stircurve.marketdata.dump import MARKET_DIR  # noqa: E402
from stircurve.marketdata.manifest import load_manifest  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ccy", default="usd")
    ap.add_argument("--start", type=dt.date.fromisoformat)
    ap.add_argument("--end", type=dt.date.fromisoformat)
    ap.add_argument("--root", type=Path, default=MARKET_DIR)
    ap.add_argument("--limit", type=int, default=40, help="lines shown per check")
    args = ap.parse_args(argv)
    frame, report = loader.load(load_manifest(args.ccy), args.start, args.end, args.root)
    print(report.report(args.limit))
    if len(frame):
        print(f"\ntidy frame: {len(frame)} rows; by instrument:")
        print(frame.groupby("instrument").size().to_string())
    if report.blocking:
        print("\nBLOCKING: see the checks marked BLOCKING above.")
    return report.exit_code


if __name__ == "__main__":
    sys.exit(main())
