"""CME product calendars (page text copied from cmegroup.com) and the comparison
with the contract-table generator.

A calendar page lists one row per listed contract: contract month, product
code, First Trade, Last Trade, Settlement (then holding/notice/delivery columns,
'-' for these cash-settled products). Copied as text, each row is a
"Mon YYYY<TAB>CODE" line followed by one date per line ("05 May 2025").
"""
from __future__ import annotations

import datetime as dt
import re

import pandas as pd

from ..refdata.parsers.common import month_number
from .contracts import listed_contracts
from .manifest import Manifest

ROW_RE = re.compile(r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{4})\t(\S+)")
DATE_RE = re.compile(r"^(\d{2}) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (\d{4})")


def _date(line: str) -> dt.date | None:
    m = DATE_RE.match(line.strip())
    return dt.date(int(m.group(3)), month_number(m.group(2)), int(m.group(1))) if m else None


def parse_cme_calendar(text: str) -> list[dict]:
    """[{contract: 'YYYY-MM', code, first_trade, last_trade, settlement}] in page order."""
    lines = text.splitlines()
    out = []
    for i, line in enumerate(lines):
        m = ROW_RE.match(line)
        if not m:
            continue
        dates = [_date(x) for x in lines[i + 1:i + 4]]
        if None in dates:
            continue
        out.append({"contract": f"{m.group(2)}-{month_number(m.group(1)):02d}", "code": m.group(3),
                    "first_trade": dates[0], "last_trade": dates[1], "settlement": dates[2]})
    return out


def compare(m: Manifest, instrument: str, rows: list[dict], as_of: dt.date) -> pd.DataFrame:
    """One row per CME contract: CME vs generated last trade, final settlement and
    first listing (first trade). ``first_listed`` is compared only where the model's
    date is not a lower bound and falls inside a listing-schedule row we hold."""
    gen = {c.contract: c for c in listed_contracts(m, instrument, max(r["first_trade"] for r in rows))}
    out = []
    for r in rows:
        g = gen.get(r["contract"])
        out.append({
            "instrument": instrument, "contract": r["contract"], "code": r["code"],
            "cme_first_trade": r["first_trade"], "gen_first_listed": g.first_listed if g else None,
            "cme_last_trade": r["last_trade"], "gen_last_trade": g.last_trade if g else None,
            "cme_settlement": r["settlement"], "gen_final_settlement": g.final_settlement if g else None,
            "first_comparable": bool(g) and not g.first_listed_lower_bound,
        })
    df = pd.DataFrame(out)
    df["last_trade_ok"] = df.cme_last_trade == df.gen_last_trade
    df["settlement_ok"] = df.cme_settlement == df.gen_final_settlement
    df["first_trade_ok"] = (df.cme_first_trade == df.gen_first_listed) | ~df.first_comparable
    return df
