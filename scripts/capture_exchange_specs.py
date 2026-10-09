#!/usr/bin/env python
"""Capture the documents behind the market-data manifest's rules as text fixtures.

Fetches every manifest source that has a fixture name (CME/CBOT rule filings on
cftc.gov, New York Fed reference-rate pages) and writes
DIR/<fixture>_<YYYYMMDD>.txt, then checks that every quoted rule passage
appears in its capture. cmegroup.com is never fetched (its terms forbid
scripted access); save those pages from a browser and convert them with
--from-saved.

Examples
    python scripts/capture_exchange_specs.py --save-fixtures tests/fixtures/live
    python scripts/capture_exchange_specs.py --check                     # quotes vs committed captures
    python scripts/capture_exchange_specs.py --from-saved ~/Downloads/cme_sr3_specs_calendar.html \
        --save-fixtures tests/fixtures/live
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from stircurve.marketdata import sources  # noqa: E402
from stircurve.marketdata.manifest import load_manifest  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ccy", default="usd")
    ap.add_argument("--save-fixtures", metavar="DIR", help="capture every fetchable source into DIR")
    ap.add_argument("--from-saved", nargs="+", metavar="FILE", help="convert browser-saved pages (HTML/PDF) into DIR")
    ap.add_argument("--check", action="store_true", help="check quoted passages against the captures in tests/fixtures/live")
    args = ap.parse_args(argv)
    m = load_manifest(args.ccy)
    rc = 0
    if args.from_saved:
        if not args.save_fixtures:
            ap.error("--from-saved needs --save-fixtures DIR")
        for p in sources.convert_saved(args.from_saved, args.save_fixtures):
            print(f"wrote {p}")
    elif args.save_fixtures:
        for sid, outcome in sources.capture(m, args.save_fixtures).items():
            print(f"{sid}: {outcome}")
            rc |= outcome.startswith("failed")
    if args.check or args.save_fixtures:
        directory = Path(args.save_fixtures) if args.save_fixtures else sources.LIVE_FIXTURES
        problems = sources.check_quotes(m, directory)
        print("\n".join(problems) if problems else "every quoted rule found in its capture")
        for sid, paths in sources.pending(m).items():
            print(f"pending {sid} ({m.sources[sid].get('status')}): {', '.join(paths)}")
        if problems:
            return 2
    return 1 if rc else 0


if __name__ == "__main__":
    sys.exit(main())
