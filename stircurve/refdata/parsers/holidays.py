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

from .common import MONTH_RE, fetch, fetch_text, month_number, save_fixture

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
    payload = fetch(UK_JSON_URL)
    save_fixture("uk_bank_holidays", payload)
    return parse_uk_json(payload)


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
    payload = r.content.decode("cp932", errors="replace")
    save_fixture("jp_cao_holidays", payload)
    return parse_jp_csv(payload)


_SIFMA_DATE_RE = re.compile(rf"(?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day,\s+{MONTH_RE}\s+(\d{{1,2}}),\s+(20\d\d)", re.I)


def parse_sifma_text(text: str) -> dict[dt.date, str]:
    """US full-close recommendations: within the 'U.S. Holiday Recommendations'
    section (the page also carries U.K. and Japan sections), a holiday-name
    line followed by 'Thursday, January 1, 2026'. 'Early Close' lines are
    ignored, so a holiday with only an early close (Good Friday 2026) is not a
    full close."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    start = next((i for i, l in enumerate(lines) if re.match(r"U\.?S\.? Holiday Recommendations", l, re.I)), None)
    if start is not None:
        end = next((i for i in range(start + 1, len(lines)) if re.search(r"Holiday Recommendations", lines[i], re.I)),
                   len(lines))
        lines = lines[start + 1:end]
    out, name = {}, None
    for s in lines:
        m = _SIFMA_DATE_RE.search(s)
        if not m:
            name = s
            continue
        if re.match(r"early close", s, re.I) or m.start() > 0:
            continue
        mon, d, y = m.groups()
        out[dt.date(int(y), month_number(mon), int(d))] = name or "SIFMA close"
    return out


def fetch_sifma() -> dict[dt.date, str]:
    return parse_sifma_text(fetch_text(SIFMA_URL, "sifma_holidays"))
