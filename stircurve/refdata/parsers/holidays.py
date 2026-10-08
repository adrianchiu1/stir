"""Official holiday sources.

* UK: https://www.gov.uk/bank-holidays.json (england-and-wales division).
* Japan: Cabinet Office CSV (Shift-JIS) https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv
  — public holidays only; the 31 Dec / 2–3 Jan banking closures are added
  from the rule set.
* US SIFMA: https://www.sifma.org/resources/general/holiday-schedule/ (HTML;
  "Full Close" lines). Parsed as text; validate on first live run.
* TARGET and US federal holidays are rule-based (no fetch).
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import re

from .common import MONTH_RE, fetch, html_to_text, month_number

UK_JSON_URL = "https://www.gov.uk/bank-holidays.json"
JP_CSV_URL = "https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv"
SIFMA_URL = "https://www.sifma.org/resources/general/holiday-schedule/"


def parse_uk_json(payload: str) -> dict[dt.date, str]:
    data = json.loads(payload)
    out = {}
    for ev in data["england-and-wales"]["events"]:
        out[dt.date.fromisoformat(ev["date"])] = ev["title"]
    return out


def fetch_uk() -> dict[dt.date, str]:
    return parse_uk_json(fetch(UK_JSON_URL))


def parse_jp_csv(payload: str) -> dict[dt.date, str]:
    """CSV with header like '国民の祝日・休日月日,国民の祝日・休日名' and rows '2026/1/1,元日'."""
    out = {}
    reader = csv.reader(io.StringIO(payload))
    for row in reader:
        if len(row) < 2:
            continue
        m = re.match(r"(\d{4})/(\d{1,2})/(\d{1,2})", row[0].strip())
        if not m:
            continue
        y, mo, d = map(int, m.groups())
        out[dt.date(y, mo, d)] = row[1].strip()
    return out


def fetch_jp() -> dict[dt.date, str]:
    import requests
    r = requests.get(JP_CSV_URL, timeout=30)
    r.raise_for_status()
    return parse_jp_csv(r.content.decode("cp932", errors="replace"))


_SIFMA_RE = re.compile(rf"{MONTH_RE}\s+(\d{{1,2}}),?\s+(20\d\d)", re.I)


def parse_sifma_text(text: str) -> dict[dt.date, str]:
    """Lines that mention a full market close. Early closes are ignored."""
    out = {}
    name = None
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if re.search(r"early close", s, re.I):
            continue
        m = _SIFMA_RE.search(s)
        if m and re.search(r"close|closed|holiday", s, re.I) or (m and name):
            mon, d, y = m.groups()
            out[dt.date(int(y), month_number(mon), int(d))] = name or s[:60]
            name = None
        elif not m and len(s) < 60 and not s[0].isdigit():
            name = s  # a holiday heading line preceding the date lines
    return out


def fetch_sifma() -> dict[dt.date, str]:
    return parse_sifma_text(html_to_text(fetch(SIFMA_URL)))
