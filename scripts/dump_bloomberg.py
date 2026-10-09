#!/usr/bin/env python
"""Dump the manifest's market data from Bloomberg to wide CSVs.

Run on a Bloomberg terminal machine (pip install -e .[bloomberg]); pxts.read_bdh
is the only network call. Writes data/market/<ccy>/<YYYY>/<group>.csv, one
column per <ticker>|<field>, ISO dates, NaN for missing. Nothing is written
without --write-csv; a run that would change or remove a value already in a file
writes nothing and exits 2. Re-running the same range is a no-op.

Examples
    python scripts/dump_bloomberg.py --start 2026-10-07 --end 2026-10-07              # dry run: diff only
    python scripts/dump_bloomberg.py --start 2026-10-07 --end 2026-10-07 --write-csv
    python scripts/dump_bloomberg.py --start 2019-06-12 --end 2019-06-12 --write-csv
    python scripts/dump_bloomberg.py --start 2010-01-01 --end 2026-10-07 --group sofr3m_fut --write-csv
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from stircurve.marketdata import dump as dumper  # noqa: E402
from stircurve.marketdata.manifest import load_manifest  # noqa: E402


def main(argv=None, read_bdh=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ccy", default="usd")
    ap.add_argument("--start", required=True, type=dt.date.fromisoformat)
    ap.add_argument("--end", required=True, type=dt.date.fromisoformat)
    ap.add_argument("--group", action="append", help="instrument key, 'fixings' or 'policy_anchors' (default: all)")
    ap.add_argument("--as-of", type=dt.date.fromisoformat, help="date deciding live vs expired ticker form (default today)")
    ap.add_argument("--root", type=Path, default=dumper.MARKET_DIR, help="market-data root (default data/market)")
    ap.add_argument("--timeout", type=float, default=dumper.TIMEOUT,
                    help=f"seconds pdblp waits for each part of a response (default {dumper.TIMEOUT:g})")
    ap.add_argument("--write-csv", action="store_true", help="write the CSV files when the diff is non-blocking (git add/commit is separate)")
    ap.add_argument("--dry-run", action="store_true", help="(default) show the diff only")
    args = ap.parse_args(argv)
    if args.end < args.start:
        ap.error("--end before --start")
    m = load_manifest(args.ccy)
    try:
        res = dumper.dump(m, args.start, args.end, read_bdh, write_csv=args.write_csv and not args.dry_run,
                          as_of=args.as_of, root=args.root, groups=args.group, timeout=args.timeout)
    except dumper.DumpError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(res.report())
    if res.blocking:
        print("\nBLOCKING diff: a value already on file would change or disappear; nothing written.")
        return 2
    if res.written:
        print(f"\nwritten: {len(res.written)} file(s)")
    else:
        print("\nok" + (" (nothing to write)" if args.write_csv else " (dry run; add --write-csv to write)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
