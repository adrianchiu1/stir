"""Meeting-calendar parsers for the Fed, ECB, BoE and BoJ.

Each ``parse_*_text`` function takes plain text (see ``common.html_to_text``)
and returns a list of ``(decision_date, kind)`` where ``kind`` is
``"scheduled"``, ``"unscheduled"`` or ``"skip"``. The ECB parser also returns
maintenance-period rows. Network access only happens in ``fetch_*``.

Sources
-------
* Fed: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm (2021+)
  and https://www.federalreserve.gov/monetarypolicy/fomchistorical<YYYY>.htm.
  Layout: "#### 2026 FOMC Meetings", then a month label ("January", "Apr/May",
  "Jan/Feb"), then "27-28" / "30-1" / "22 (notation vote)" / "15 (unscheduled)".
  Decision date = last day of the range.
* ECB: index https://www.ecb.europa.eu/press/calendars/reserve/html/index.en.html
  links one press release per year ("Indicative operational calendars for
  YYYY") holding a table: MP | Relevant Governing Council meeting | Start of MP
  | End of MP | ... with cells like "Thu, 17-Dec-26".
* BoE: https://www.bankofengland.co.uk/monetary-policy/upcoming-mpc-dates
  lists "Thursday 5 February" lines under "2026 confirmed dates" headings
  (current and next year only; no historical page).
* BoJ: https://www.boj.or.jp/en/mopo/mpmsche_minu/index.htm (current and next
  year) and .../past.htm (2010+): one table per year whose first column is
  "Jan. 22 (Thurs.), 23 (Fri.)" (decision on the last day; one-day meetings
  occur, e.g. "Apr. 30 (Fri.)").

All four parsers are validated against live pages captured 8 Oct 2026
(``tests/fixtures/live``).
"""
from __future__ import annotations

import datetime as dt
import re

from .common import MONTH_RE, fetch, fetch_text, month_number, save_fixture

FED_CALENDAR_URL = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
FED_HISTORICAL_URL = "https://www.federalreserve.gov/monetarypolicy/fomchistorical{year}.htm"
ECB_RESERVE_INDEX_URL = "https://www.ecb.europa.eu/press/calendars/reserve/html/index.en.html"
ECB_MP_2027_URL = "https://www.ecb.europa.eu/press/pr/date/2026/html/ecb.pr260630~9f54a0a4fb.en.html"
BOE_UPCOMING_URL = "https://www.bankofengland.co.uk/monetary-policy/upcoming-mpc-dates"
BOJ_SCHEDULE_URL = "https://www.boj.or.jp/en/mopo/mpmsche_minu/index.htm"
BOJ_PAST_URL = "https://www.boj.or.jp/en/mopo/mpmsche_minu/past.htm"


# ---------------------------------------------------------------------------
# Fed
# ---------------------------------------------------------------------------
_FED_YEAR_RE = re.compile(r"\b(20\d\d|19\d\d)\s+FOMC\s+Meetings\b", re.I)
_FED_MONTH_RE = re.compile(rf"^\s*\*?\*?\s*{MONTH_RE}(?:\s*/\s*{MONTH_RE})?\s*\*?\*?\s*$", re.I)
_FED_DAYS_RE = re.compile(r"^\s*(\d{1,2})(?:\s*[-–]\s*(\d{1,2}))?\*?\s*(\(([^)]*)\))?\s*(Meeting)?\s*$", re.I)
# historical pages: "January 26-27 Meeting", "March 15 (unscheduled) Meeting"
_FED_HIST_RE = re.compile(
    rf"\b{MONTH_RE}(?:\s*/\s*{MONTH_RE})?\s+(\d{{1,2}})(?:\s*[-–]\s*(\d{{1,2}}))?\*?\s*(\(([^)]*)\))?\s*Meeting\b", re.I)


def _fed_kind(note: str | None) -> str:
    n = (note or "").lower()
    if "notation" in n or "no meeting" in n:
        return "skip"
    if "unscheduled" in n or "conference call" in n or "videoconference" in n:
        return "unscheduled"
    return "scheduled"


def parse_fed_text(text: str) -> list[tuple[dt.date, str]]:
    out: list[tuple[dt.date, str]] = []
    year = None
    month_a = month_b = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        ym = _FED_YEAR_RE.search(line)
        if ym:
            year = int(ym.group(1))
            month_a = month_b = None
            continue
        if year is None:
            continue
        # historical single-line form
        for m in _FED_HIST_RE.finditer(line):
            ma, mb, d1, d2, _, note = m.groups()
            month = month_number(mb) if mb else month_number(ma)
            day = int(d2 or d1)
            y = year
            if mb and month_number(ma) == 12 and month == 1:
                y = year + 1
            out.append((dt.date(y, month, day), _fed_kind(note)))
        if _FED_HIST_RE.search(line):
            continue
        mm = _FED_MONTH_RE.match(line)
        if mm:
            month_a = month_number(mm.group(1))
            month_b = month_number(mm.group(2)) if mm.group(2) else None
            continue
        dm = _FED_DAYS_RE.match(line)
        if dm and month_a:
            d1, d2, _, note, _ = dm.groups()
            month = month_b if (d2 and month_b) else month_a
            day = int(d2 or d1)
            out.append((dt.date(year, month, day), _fed_kind(note)))
            month_a = month_b = None
    return out


def fetch_fed(years_historical: range | None = None) -> list[tuple[dt.date, str, str]]:
    """Current calendar page plus historical pages for ``years_historical``.
    Returns (decision_date, kind, source_url)."""
    out = []
    text = fetch_text(FED_CALENDAR_URL, "fed_calendar")
    out += [(d, k, FED_CALENDAR_URL) for d, k in parse_fed_text(text)]
    for y in years_historical or []:
        url = FED_HISTORICAL_URL.format(year=y)
        try:
            t = fetch_text(url, f"fed_historical_{y}")
        except Exception as exc:  # pragma: no cover
            print(f"  fed {y}: fetch failed ({exc})")
            continue
        if f"{y} FOMC" not in t:
            t = f"{y} FOMC Meetings\n" + t   # historical pages carry the year in the title
        out += [(d, k, url) for d, k in parse_fed_text(t)]
    return out


# ---------------------------------------------------------------------------
# ECB
# ---------------------------------------------------------------------------
_ECB_DATE_RE = re.compile(rf"(?:(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*,?\s*)?(\d{{1,2}})[-\s.]{MONTH_RE}[-\s.](\d{{2,4}})", re.I)
_ECB_MP_LABEL_RE = re.compile(r"^\s*(\d{1,2}(?:\s*/\s*\d{4})?)\s*(\||$)")


def _ecb_date(s: str) -> dt.date | None:
    m = _ECB_DATE_RE.search(s)
    if not m:
        return None
    d, mon, y = m.groups()
    y = int(y)
    if y < 100:
        y += 2000 if y < 70 else 1900
    return dt.date(y, month_number(mon), int(d))


def parse_ecb_mp_table(text: str, year_hint: int | None = None) -> list[dict]:
    """Rows of the ECB maintenance-period table.

    Returns dicts with keys ``label, meeting, start, end`` (dates or None).
    Accepts the text form produced by ``html_to_text`` (cells joined by ' | ')
    and the markdown table form (cells separated by '|').
    """
    rows = []
    for raw in text.splitlines():
        line = raw.strip().strip("|").strip()
        if "|" not in line:
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 3 or not _ECB_MP_LABEL_RE.match(cells[0]):
            continue
        dates = [_ecb_date(c) for c in cells[1:]]
        dates = [d for d in dates if d]
        if len(dates) < 2:
            continue
        label = cells[0].replace(" ", "")
        # with a meeting column: meeting, start, end; without: start, end
        if len(dates) >= 3:
            meeting, start, end = dates[0], dates[1], dates[2]
        else:
            meeting, start, end = None, dates[0], dates[1]
        if "/" not in label and year_hint:
            label = f"{label}/{year_hint}"
        rows.append({"label": label, "meeting": meeting, "start": start, "end": end})
    return rows


def ecb_index_links(text_or_html: str) -> dict[int, str]:
    """Year -> press-release URL from the reserve-calendar index page.
    Handles 'for 2017 and 2018' by mapping both years to the same URL."""
    out: dict[int, str] = {}
    for m in re.finditer(r'href="([^"]+)"[^>]*>\s*Indicative operational calendars for ([^<]+)<', text_or_html, re.I):
        url, yrs = m.group(1), m.group(2)
        for y in re.findall(r"(19\d\d|20\d\d)", yrs):
            out[int(y)] = url if url.startswith("http") else "https://www.ecb.europa.eu" + url
    return out


def fetch_ecb_maintenance(years: range | None = None) -> list[tuple[dict, str]]:
    """Maintenance-period rows (with source URL) for the requested years,
    discovered from the index page; 2027 added from the known release."""
    index_html = fetch(ECB_RESERVE_INDEX_URL)
    save_fixture("ecb_reserve_index", index_html)
    links = ecb_index_links(index_html)
    links.setdefault(2027, ECB_MP_2027_URL)
    out = []
    for y in sorted(years or links):
        url = links.get(y)
        if not url:
            continue
        try:
            t = fetch_text(url, f"ecb_mp_{y}")
        except Exception as exc:  # pragma: no cover
            print(f"  ecb {y}: fetch failed ({exc})")
            continue
        for row in parse_ecb_mp_table(t, year_hint=y):
            out.append((row, url))
    return out


# ---------------------------------------------------------------------------
# BoE
# ---------------------------------------------------------------------------
# The live page groups dates under "2026 confirmed dates" headings and lists
# each meeting as "Thursday 5 February" (no year). Other dates on the page
# ("Next due: 5 November 2026", news items "17 September 2026", "last updated")
# carry no weekday and are ignored.
_BOE_YEAR_RE = re.compile(r"^\s*(20\d\d)\s+(?:confirmed|provisional)?\s*(?:MPC\s+)?dates\b", re.I)
_BOE_RE = re.compile(rf"^\s*(?:Thursday|Wednesday|Tuesday|Monday|Friday)\s+(\d{{1,2}})\s+{MONTH_RE}(?:\s+(20\d\d))?\b", re.I)


def parse_boe_text(text: str) -> list[tuple[dt.date, str]]:
    """Lines that start with 'Thursday 5 February [2026]'; the year comes from
    the line itself or the latest '<YYYY> confirmed dates' heading."""
    found: set[dt.date] = set()
    year = None
    for line in text.splitlines():
        ym = _BOE_YEAR_RE.match(line)
        if ym:
            year = int(ym.group(1))
            continue
        m = _BOE_RE.match(line)
        if not m:
            continue
        d, mon, y = m.groups()
        y = int(y) if y else year
        if y is None:
            continue
        found.add(dt.date(y, month_number(mon), int(d)))
    return [(d, "scheduled") for d in sorted(found)]


def fetch_boe() -> list[tuple[dt.date, str, str]]:
    text = fetch_text(BOE_UPCOMING_URL, "boe_upcoming_mpc_dates")
    return [(d, k, BOE_UPCOMING_URL) for d, k in parse_boe_text(text)]


# ---------------------------------------------------------------------------
# BoJ
# ---------------------------------------------------------------------------
# One table per year ("Table : 2026"); the first cell of each row is the
# meeting: "Jan. 22 (Thurs.), 23 (Fri.) [PDF 171KB]", one-day meetings
# "Apr. 30 (Fri.)", sometimes broken across lines ("Mar. 17\n(Wed.), 18 (Thurs.)").
# The other cells are release dates (Outlook Report, minutes, ...).
_BOJ_YEAR_RE = re.compile(r"^(?:Table\s*:\s*)?(20\d\d)$")
_WKD = r"(?:\s*\([A-Za-z.]+\))?"
_BOJ_MEETING_RE = re.compile(
    rf"^{MONTH_RE}\.?\s+(\d{{1,2}}){_WKD}(?:\s*[,\-–]\s*(?:{MONTH_RE}\.?\s+)?(\d{{1,2}}){_WKD})?(?:,\s*(20\d\d))?", re.I)


def _boj_rows(text: str) -> list[str]:
    """Re-join table rows: a cell ends with '|', the last cell of a row does
    not; a line followed by '(' or '|' is a cell broken across lines."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    rows, cur = [], ""
    for i, line in enumerate(lines):
        cur = f"{cur} {line}" if cur else line
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if line.endswith("|") or nxt.startswith(("(", "|")):
            continue
        rows.append(cur)
        cur = ""
    if cur:
        rows.append(cur)
    return rows


def parse_boj_text(text: str) -> list[tuple[dt.date, str]]:
    """Decision date = last day of the meeting cell. Rows mentioning
    'unscheduled' or 'extraordinary' are tagged unscheduled."""
    out = []
    year = None
    for row in _boj_rows(text):
        ym = _BOJ_YEAR_RE.match(row)
        if ym:
            year = int(ym.group(1))
            continue
        first = row.split("|")[0].strip()
        m = _BOJ_MEETING_RE.match(first)
        if not m:
            continue
        ma, d1, mb, d2, y = m.groups()
        y = int(y) if y else year
        if y is None:
            continue
        month = month_number(mb) if mb else month_number(ma)
        if mb and month < month_number(ma):
            y += 1
        kind = "unscheduled" if re.search(r"unscheduled|extraordinary", row, re.I) else "scheduled"
        out.append((dt.date(y, month, int(d2 or d1)), kind))
    return out


def fetch_boj() -> list[tuple[dt.date, str, str]]:
    """Current schedule page (this year and next) plus the past-meetings page (2010+)."""
    out = []
    for url, source in ((BOJ_SCHEDULE_URL, "boj_mpm_schedule"), (BOJ_PAST_URL, "boj_mpm_past")):
        out += [(d, k, url) for d, k in parse_boj_text(fetch_text(url, source))]
    return out
