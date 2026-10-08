"""Official holiday sources.

* UK: https://www.gov.uk/bank-holidays.json (england-and-wales division).
* Japan: Cabinet Office CSV (Shift-JIS) https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv
  — public holidays only; the 31 Dec / 2–3 Jan banking closures are added
  from the rule set.
* US SIFMA: https://www.sifma.org/resources/general/holiday-schedule/ (this
  year) and the U.S. holiday archive (2015+): "name / weekday, Month D, YYYY"
  full closes; early-close lines are not closes.
* US SOFR: NY Fed reference-rate API; a weekday without a SOFR publication
  (since 2 Apr 2018) is a us_sofr holiday.
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
SIFMA_US_ARCHIVE_URL = "https://www.sifma.org/resources/guides-playbooks/us-holiday-archive"
NYFED_SOFR_URL = ("https://markets.newyorkfed.org/api/rates/secured/sofr/search.json"
                  "?startDate=2018-04-02&endDate={end}")


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
    out, early, name = {}, set(), None
    for s in lines:
        m = _SIFMA_DATE_RE.search(s)
        if not m:
            name = s
            continue
        mon, d, y = m.groups()
        day = dt.date(int(y), month_number(mon), int(d))
        if re.match(r"early (?:market )?close", s, re.I) or m.start() > 0:
            early.add(day)
            continue
        out[day] = name or "SIFMA close"
    # 2015 lists "Friday, April 3, 2015" and then "Early Close (12:00 Noon) Friday, April 3, 2015"
    return {d: n for d, n in out.items() if d not in early}


def sifma_undated(text: str) -> set[tuple[int, str]]:
    """(year, holiday) pairs the archive names without a date (Presidents Day
    2015 and 2016): listed, so not evidence against the rule date."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    out, year = set(), None
    for a, b in zip(lines, lines[1:] + [""]):
        if re.fullmatch(r"(19|20)\d\d", a):
            year = int(a)
        elif year and not _SIFMA_DATE_RE.search(a) and not _SIFMA_DATE_RE.search(b) and len(a) < 60 \
                and not re.fullmatch(r"(19|20)\d\d|none", b, re.I):
            out.add((year, holiday_key(a)))
    return out


def holiday_key(name: str) -> str:
    """'Martin Luther King Jr. Day (observed)' -> 'martinlutherkingday'."""
    n = re.sub(r"\(.*?\)|\b(jr|u\.?s\.?|observed)\b|\d{4}(/\d{4})?", "", name.lower())
    return re.sub(r"[^a-z]", "", n)


def fetch_sifma() -> tuple[dict[dt.date, str], set[tuple[int, str]]]:
    """This year's schedule plus the U.S. archive (2015 onwards): full closes,
    and holidays the archive names without a date."""
    archive = fetch_text(SIFMA_US_ARCHIVE_URL, "sifma_us_archive")
    out = parse_sifma_text(archive)
    out.update(parse_sifma_text(fetch_text(SIFMA_URL, "sifma_holidays")))
    return out, sifma_undated(archive)


def parse_sofr_json(payload: str) -> set[dt.date]:
    """Dates with a SOFR publication (NY Fed API 'refRates[].effectiveDate')."""
    return {dt.date.fromisoformat(r["effectiveDate"]) for r in json.loads(payload).get("refRates", [])}


def sofr_non_publication_days(published: set[dt.date]) -> dict[dt.date, str]:
    """Weekdays between the first and last publication without a SOFR."""
    out, d = {}, min(published)
    while d <= max(published):
        if d.weekday() < 5 and d not in published:
            out[d] = "No SOFR publication"
        d += dt.timedelta(days=1)
    return out


def fetch_sofr_publication_days() -> set[dt.date]:
    payload = fetch(NYFED_SOFR_URL.format(end=dt.date.today().isoformat()))
    save_fixture("nyfed_sofr", payload)
    return parse_sofr_json(payload)
