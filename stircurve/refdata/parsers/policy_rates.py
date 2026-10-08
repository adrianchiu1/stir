"""Policy-rate parsers.

* Fed: https://www.federalreserve.gov/monetarypolicy/openmarket.htm — per-year
  tables "Date | Increase | Decrease | Level (%)" where Date is the *effective*
  date and Level is "3.75-4.00" (range) or "1.00" (single target pre-2008).
* FRED CSV: https://fred.stlouisfed.org/graph/fredgraph.csv?id=<SERIES>
  (DFEDTARU, DFEDTARL, IORB, IOER) — daily levels; changes are extracted.
* ECB: https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html
  — table "Date (with effect from) | Deposit facility | Main refinancing
  operations | Marginal lending facility"; column order is read from the header.
* BoE: https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp —
  "Date Changed | Rate" with dates like "18 Dec 25".
* BoJ: no machine-readable table; rows are maintained by hand from the
  Statement on Monetary Policy PDFs (effective date in the footnote).
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import re

from .common import MONTH_RE, fetch, html_to_text, month_number

FED_OPENMARKET_URL = "https://www.federalreserve.gov/monetarypolicy/openmarket.htm"
FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
ECB_KEY_RATES_URL = "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html"
BOE_BANK_RATE_URL = "https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp"

_YEAR_HDR = re.compile(r"^\s*#*\s*(20\d\d|19\d\d)\s*$")
_FED_ROW = re.compile(rf"^\s*\|?\s*{MONTH_RE}\s+(\d{{1,2}})(?:\*|\[[^\]]*\]\([^)]*\))?\s*\|\s*([\d.]*|\.\.\.)\s*\|\s*([\d\-.]*|\.\.\.)\s*\|\s*([\d.]+)(?:\s*-\s*([\d.]+))?\s*\|?\s*$", re.I)


def parse_fed_openmarket_text(text: str) -> list[dict]:
    """Rows: effective_date, lower, upper (single-target years have lower == upper)."""
    out, year = [], None
    for line in text.splitlines():
        ym = _YEAR_HDR.match(line.strip())
        if ym:
            year = int(ym.group(1))
            continue
        if year is None:
            continue
        m = _FED_ROW.match(line)
        if not m:
            continue
        mon, day, _inc, _dec, lo, hi = m.groups()
        lo = float(lo)
        hi = float(hi) if hi else lo
        out.append({"effective_date": dt.date(year, month_number(mon), int(day)), "lower": lo, "upper": hi})
    return sorted(out, key=lambda r: r["effective_date"])


def fetch_fed_openmarket() -> list[dict]:
    return parse_fed_openmarket_text(html_to_text(fetch(FED_OPENMARKET_URL)))


def parse_fred_csv(payload: str) -> list[tuple[dt.date, float]]:
    """(date, level) for each day on which the level changed (first row kept)."""
    out, prev = [], None
    for row in csv.reader(io.StringIO(payload)):
        if len(row) < 2 or not re.match(r"\d{4}-\d{2}-\d{2}", row[0]):
            continue
        if row[1] in ("", "."):
            continue
        v = float(row[1])
        if prev is None or v != prev:
            out.append((dt.date.fromisoformat(row[0]), v))
            prev = v
    return out


def fetch_fred(series: str) -> list[tuple[dt.date, float]]:
    return parse_fred_csv(fetch(FRED_CSV_URL.format(series=series)))


_ECB_DATE = re.compile(rf"(\d{{1,2}})(?:st|nd|rd|th)?\s+{MONTH_RE}\w*\s+(20\d\d|19\d\d)", re.I)
_NUM = re.compile(r"^-?\d+(?:[.,]\d+)?$")


def parse_ecb_key_rates_text(text: str) -> list[dict]:
    """Rows: effective_date, dfr, mro, mlf. Column order taken from the header
    line that mentions 'deposit'; defaults to ECB order (DFR, MRO, MLF)."""
    order = ["dfr", "mro", "mlf"]
    out = []
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        low = line.lower()
        if "deposit" in low and ("refinanc" in low or "tender" in low):
            keys = []
            for c in cells:
                cl = c.lower()
                if "deposit" in cl:
                    keys.append("dfr")
                elif "refinanc" in cl or "tender" in cl:
                    keys.append("mro")
                elif "marginal" in cl:
                    keys.append("mlf")
            if len(keys) == 3:
                order = keys
            continue
        if len(cells) < 4:
            continue
        dm = _ECB_DATE.search(cells[0])
        nums = [c.replace(",", ".") for c in cells[1:4]]
        if not dm or not all(_NUM.match(n) for n in nums):
            continue
        d = dt.date(int(dm.group(3)), month_number(dm.group(2)[:3]), int(dm.group(1)))
        row = {"effective_date": d}
        for k, n in zip(order, nums):
            row[k] = float(n)
        out.append(row)
    return sorted(out, key=lambda r: r["effective_date"])


def fetch_ecb_key_rates() -> list[dict]:
    return parse_ecb_key_rates_text(html_to_text(fetch(ECB_KEY_RATES_URL)))


_BOE_ROW = re.compile(rf"^\s*\|?\s*(\d{{1,2}})\s+{MONTH_RE}\s+(\d{{2,4}})\s*\|\s*(-?[\d.]+)\s*\|?\s*$", re.I)


def parse_boe_bank_rate_text(text: str) -> list[tuple[dt.date, float]]:
    out = []
    for line in text.splitlines():
        m = _BOE_ROW.match(line)
        if not m:
            continue
        d, mon, y, rate = m.groups()
        y = int(y)
        if y < 100:
            y += 2000 if y < 70 else 1900
        out.append((dt.date(y, month_number(mon), int(d)), float(rate)))
    return sorted(out)


def fetch_boe_bank_rate() -> list[tuple[dt.date, float]]:
    return parse_boe_bank_rate_text(html_to_text(fetch(BOE_BANK_RATE_URL)))
