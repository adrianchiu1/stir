#!/usr/bin/env python
"""Refresh reference data from public sources.

Run on a machine with outbound internet. Nothing is written unless --commit
is given and the diff contains no removed rows, no changed past dates and no
validation problems. Exit code 2 signals a blocking diff.

Examples
    python scripts/update_refdata.py --bank fed --dry-run
    python scripts/update_refdata.py --bank fed --historical 2010-2020 --commit
    python scripts/update_refdata.py --ecb-maintenance --years 2010-2027 --commit
    python scripts/update_refdata.py --holidays uk jp us_sifma us_sofr --commit
    python scripts/update_refdata.py --policy-rates fed --policy-rates ecb --policy-rates boe --commit
    python scripts/update_refdata.py --bank boe --dry-run --save-fixtures tests/fixtures/live
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from stircurve.refdata import updater  # noqa: E402


def _years(s: str | None) -> range | None:
    if not s:
        return None
    a, _, b = s.partition("-")
    return range(int(a), int(b or a) + 1)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bank", choices=["fed", "ecb", "boe", "boj"], action="append", help="meeting calendar(s) to refresh")
    ap.add_argument("--historical", help="year range for historical pages, e.g. 2010-2020 (fed, ecb)")
    ap.add_argument("--ecb-maintenance", action="store_true", help="refresh ECB maintenance periods")
    ap.add_argument("--years", help="year range for --ecb-maintenance, e.g. 2015-2027")
    ap.add_argument("--holidays", nargs="*", help="calendars to refresh from official sources: uk jp us_sifma us_sofr (target/us_fed are rule-based)")
    ap.add_argument("--policy-rates", choices=["fed", "ecb", "boe", "boj"], action="append", help="policy-rate file(s) to refresh")
    ap.add_argument("--commit", action="store_true", help="write files when the diff is non-blocking")
    ap.add_argument("--dry-run", action="store_true", help="(default) show the diff only")
    ap.add_argument("--save-fixtures", metavar="DIR",
                    help="write the text of every fetched page to DIR/<source>_<YYYYMMDD>.txt (regression fixtures)")
    args = ap.parse_args(argv)
    commit = args.commit and not args.dry_run
    blocking = False

    if args.ecb_maintenance:
        print("== ECB maintenance periods")
        d = updater.update_ecb_maintenance(commit=commit, years=_years(args.years), save_fixtures=args.save_fixtures)
        print(d.report()); blocking |= d.blocking
    for bank in args.bank or []:
        print(f"== {bank} meetings")
        d = updater.update_meetings(bank, commit=commit, historical_years=_years(args.historical),
                                   save_fixtures=args.save_fixtures)
        print(d.report()); blocking |= d.blocking
    for bank in args.policy_rates or []:
        print(f"== {bank} policy rates")
        d = updater.update_policy_rates(bank, commit=commit, save_fixtures=args.save_fixtures)
        print(d.report()); blocking |= d.blocking
    for name in args.holidays or []:
        print(f"== holidays {name}")
        d = updater.update_holidays(name, commit=commit, save_fixtures=args.save_fixtures)
        print(d.report()); blocking |= d.blocking
    if blocking:
        print("\nBLOCKING diff: nothing written. Inspect, fix the committed file or the parser, re-run.")
        return 2
    print("\nok" + (" (written)" if commit else " (dry run; add --commit to write)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
