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

from .common import MONTH_RE, fetch, fetch_text, join_table_rows, month_number, save_fixture

FED_OPENMARKET_URL = "https://www.federalreserve.gov/monetarypolicy/openmarket.htm"
FRED_CSV_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
ECB_KEY_RATES_URL = "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html"
BOE_BANK_RATE_URL = "https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp"

_YEAR_HDR = re.compile(r"^\s*#*\s*(20\d\d|19\d\d)\s*$")
_FED_ROW = re.compile(rf"^\s*\|?\s*{MONTH_RE}\s+(\d{{1,2}})(?:\*|\[[^\]]*\]\([^)]*\))?\s*\|\s*([\d.]*|\.\.\.)\s*\|\s*([\d\-.]*|\.\.\.)\s*\|\s*([\d.]+)(?:\s*-\s*([\d.]+))?\s*\|?\s*$", re.I)


def parse_fed_openmarket_text(text: str) -> list[dict]:
    """Rows: effective_date, lower, upper (single-target years have lower == upper).
    Accepts one row per line (markdown) or the live page's one cell per line."""
    return _fed_openmarket_rows(text.splitlines()) or _fed_openmarket_rows(join_table_rows(text))


def _fed_openmarket_rows(lines: list[str]) -> list[dict]:
    out, year = [], None
    for line in lines:
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
    return parse_fed_openmarket_text(fetch_text(FED_OPENMARKET_URL, "fed_openmarket"))


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
    payload = fetch(FRED_CSV_URL.format(series=series))
    save_fixture(f"fred_{series.lower()}", payload)
    return parse_fred_csv(payload)


_ECB_DATE = re.compile(rf"(\d{{1,2}})(?:st|nd|rd|th)?\s+{MONTH_RE}\w*\s+(20\d\d|19\d\d)", re.I)
_NUM = re.compile(r"^-?\d+(?:[.,]\d+)?$")


def parse_ecb_key_rates_text(text: str) -> list[dict]:
    """Rows: effective_date, dfr, mro, mlf. Column order taken from the header
    line that mentions 'deposit'; defaults to ECB order (DFR, MRO, MLF).
    Falls back to the live ECB page layout (``_ecb_key_rates_cells``)."""
    return _ecb_key_rates_lines(text) or _ecb_key_rates_cells(text)


_ECB_DAYMON = re.compile(rf"^(\d{{1,2}})\s+{MONTH_RE}\.?\s*\d?$", re.I)   # "16 Sep.", "18 Sep.5" (footnote), "4 Jan. 1"
_ECB_LIVE_START = dt.date(2004, 3, 10)   # before this, MRO changes applied from the next operation (page footnote)


def _ecb_key_rates_cells(text: str) -> list[dict]:
    """Live ECB page: one cell per line, the year cell spans all rows of that
    year, then '16 Sep.' | DFR | MRO fixed rate | MRO minimum bid rate | MLF,
    '-' where not applicable and U+2212 for minus. MRO is the fixed rate, else
    the minimum bid rate; when both are '-' (8-9 Oct 2008) the row has no MRO.
    Rows before 10 March 2004 are dropped (different MRO effective-date convention)."""
    start = text.find("with effect from")
    if start < 0:
        return []
    cells = [c.strip().replace("\u2212", "-") for line in text[start:].splitlines() for c in line.split("|")]
    cells = [c for c in cells if c]
    out, year, i = [], None, 0
    while i < len(cells):
        c = cells[i]
        if re.fullmatch(r"(19|20)\d\d", c):
            year = int(c)
            i += 1
            continue
        m = _ECB_DAYMON.match(c)
        if not (m and year) or i + 4 >= len(cells):
            i += 1
            continue
        vals = cells[i + 1:i + 5]
        num = [float(v) if _NUM.match(v) else None for v in vals]
        if num[0] is None or num[3] is None:
            i += 1
            continue
        d = dt.date(year, month_number(m.group(2)[:3]), int(m.group(1)))
        if d >= _ECB_LIVE_START:
            row = {"effective_date": d, "dfr": num[0], "mlf": num[3]}
            mro = num[1] if num[1] is not None else num[2]
            if mro is not None:
                row["mro"] = mro
            out.append(row)
        i += 5
    return sorted(out, key=lambda r: r["effective_date"])


def _ecb_key_rates_lines(text: str) -> list[dict]:
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
    return parse_ecb_key_rates_text(fetch_text(ECB_KEY_RATES_URL, "ecb_key_rates"))


_BOE_ROW = re.compile(rf"^\s*\|?\s*(\d{{1,2}})\s+{MONTH_RE}\s+(\d{{2,4}})\s*\|\s*(-?[\d.]+)\s*\|?\s*$", re.I)


def parse_boe_bank_rate_text(text: str) -> list[tuple[dt.date, float]]:
    """'18 Dec 25 | 3.75' rows, one per line or one cell per line (live page)."""
    return _boe_rows(text.splitlines()) or _boe_rows(join_table_rows(text))


def _boe_rows(lines: list[str]) -> list[tuple[dt.date, float]]:
    out = []
    for line in lines:
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
    return parse_boe_bank_rate_text(fetch_text(BOE_BANK_RATE_URL, "boe_bank_rate"))
