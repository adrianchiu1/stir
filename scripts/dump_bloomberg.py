#!/usr/bin/env python
"""Dump the manifest's market data from Bloomberg to wide CSVs.

Run on a Bloomberg terminal machine (pip install -e .[bloomberg]); pxts.read_bdh
is the only network call. Writes data/market/<ccy>/<YYYY>/<group>.csv, one
column per <ticker>|<field>, ISO dates, NaN for missing. Nothing is written
without --commit; a run that would change or remove a value already in a file
writes nothing and exits 2. Re-running the same range is a no-op.

Examples
    python scripts/dump_bloomberg.py --start 2026-10-07 --end 2026-10-07              # dry run: diff only
    python scripts/dump_bloomberg.py --start 2026-10-07 --end 2026-10-07 --commit
    python scripts/dump_bloomberg.py --start 2019-06-12 --end 2019-06-12 --commit
    python scripts/dump_bloomberg.py --start 2010-01-01 --end 2026-10-07 --group sofr3m_fut --commit
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
    ap.add_argument("--timeout", type=float, default=30, help="read_bdh timeout per request, seconds")
    ap.add_argument("--commit", action="store_true", help="write files when the diff is non-blocking")
    ap.add_argument("--dry-run", action="store_true", help="(default) show the diff only")
    args = ap.parse_args(argv)
    if args.end < args.start:
        ap.error("--end before --start")
    m = load_manifest(args.ccy)
    res = dumper.dump(m, args.start, args.end, read_bdh, commit=args.commit and not args.dry_run,
                      as_of=args.as_of, root=args.root, groups=args.group, timeout=args.timeout)
    print(res.report())
    if res.blocking:
        print("\nBLOCKING diff: a value already on file would change or disappear; nothing written.")
        return 2
    if res.written:
        print(f"\nwritten: {len(res.written)} file(s)")
    else:
        print("\nok" + (" (nothing to write)" if args.commit else " (dry run; add --commit to write)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
