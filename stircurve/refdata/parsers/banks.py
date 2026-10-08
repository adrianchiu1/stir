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
  Decision date = last day of the range, or the statement release date when a
  historical page gives a later one ("March 2 (unscheduled) Meeting", statement
  released 3 March 2020).
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

from .common import MONTH_RE, fetch, fetch_text, join_table_rows, month_number, save_fixture

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
# historical pages: "January 26-27 Meeting", "March 15 (unscheduled) Meeting", "July 31-August 1 Meeting"
_FED_HIST_RE = re.compile(
    rf"\b{MONTH_RE}(?:\s*/\s*{MONTH_RE})?\s+(\d{{1,2}})(?:\s*[-–]\s*(?:{MONTH_RE}\s+)?(\d{{1,2}}))?\*?\s*(\(([^)]*)\))?\s*Meeting\b", re.I)


_FED_RELEASED_RE = re.compile(rf"\bStatement\b.*\bReleased\s+{MONTH_RE}\w*\s+(\d{{1,2}}),\s+(\d{{4}})", re.I)


def _fed_kind(note: str | None) -> str:
    n = (note or "").lower()
    if "notation" in n or "no meeting" in n or "cancel" in n:
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
        # historical pages: "Statement (Released March 3, 2020)" under a meeting dated
        # "March 2 (unscheduled)": the decision is the announced one (AC, PR #1)
        rel = _FED_RELEASED_RE.search(line)
        if rel and out and out[-1][1] != "skip":
            rd = dt.date(int(rel.group(3)), month_number(rel.group(1)), int(rel.group(2)))
            if 0 < (rd - out[-1][0]).days <= 7:
                out[-1] = (rd, out[-1][1])
            continue
        # historical single-line form
        for m in filter(None, [_FED_HIST_RE.match(line)]):   # header lines only, not "minutes of March 15 meeting"
            ma, mb, d1, mc, d2, _, note = m.groups()
            mb = mb or mc
            month = month_number(mb) if mb else month_number(ma)
            day = int(d2 or d1)
            y = year
            if mb and month_number(ma) == 12 and month == 1:
                y = year + 1
            out.append((dt.date(y, month, day), _fed_kind(note)))
        if _FED_HIST_RE.match(line):
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
_ECB_DATE_RE = re.compile(rf"(?:(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*,?\s*)?(\d{{1,2}})[-\s.]{MONTH_RE}[-\s.]?(\d{{2,4}})", re.I)  # "4 February2025" occurs
_ECB_TBD_RE = re.compile(r"^(?:tbd|tbc|to be (?:determined|confirmed|announced))\b", re.I)
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
    """Rows of the ECB maintenance-period table(s).

    Returns dicts with keys ``label, meeting, start, end`` (dates or None).
    Accepts the markdown table form (one row per line) and the live
    ``html_to_text`` form, whose cells are spread over several lines (rows
    are re-joined with ``join_table_rows``). An unqualified label ("1", "8")
    takes the year of the MP's start date: releases covering two years hold
    one table per year, and since 2022 each opens with MP 8 of the previous
    year labelled "8". ``year_hint`` is only used if a row has no start date.
    """
    rows = _ecb_mp_rows(text.splitlines(), year_hint)
    return rows or _ecb_mp_rows(join_table_rows(text), year_hint)


def _ecb_mp_rows(lines: list[str], year_hint: int | None) -> list[dict]:
    rows = []
    for raw in lines:
        line = raw.strip().strip("|").strip()
        if "|" not in line:
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 3 or not _ECB_MP_LABEL_RE.match(cells[0]):
            continue
        first3 = [_ecb_date(c) for c in cells[1:4]]
        if len(cells) >= 4 and first3[0] and first3[1] and _ECB_TBD_RE.match(cells[3]):
            # last MP of a release: end "tbd" until the next year's release
            label = cells[0].replace(" ", "")
            if "/" not in label:
                label = f"{label}/{first3[1].year}"
            rows.append({"label": label, "meeting": first3[0], "start": first3[1], "end": None})
            continue
        dates = [d for d in (_ecb_date(c) for c in cells[1:]) if d]
        if len(dates) < 2:
            continue
        label = cells[0].replace(" ", "")
        # with a meeting column: meeting, start, end; without: start, end
        if all(first3):
            meeting, start, end = first3
        elif len(dates) >= 3:
            meeting, start, end = dates[0], dates[1], dates[2]
        else:
            meeting, start, end = None, dates[0], dates[1]
        year = start.year if start else year_hint
        if "/" not in label and year:
            label = f"{label}/{year}"
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


_ORDINALS = {w: i for i, w in enumerate(["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth",
                                         "ninth", "tenth", "eleventh", "twelfth"], start=1)}
_ECB_EXTEND_RE = re.compile(
    r"\b(\d{1,2})(?:st|nd|rd|th)?\s+(?:reserve\s+)?maintenance period of (\d{4}) will be extended\b[^.]*?\bend on "
    rf"(\d{{1,2}}\s+{MONTH_RE}\w*\s+\d{{4}})", re.I)


def parse_ecb_mp_amendments(text: str) -> dict[str, dt.date]:
    """Changes announced in the prose of a release rather than its table:
    'The 12th reserve maintenance period of 2014 will be extended by 14 days
    and end on 27 January 2015' -> {'12/2014': 2015-01-27}."""
    out = {}
    for m in _ECB_EXTEND_RE.finditer(" ".join(text.split())):
        n, y, d = m.groups()[:3]
        out[f"{int(n)}/{y}"] = _ecb_date(d)
    return out


def fetch_ecb_maintenance(years: range | None = None) -> list[tuple[dict, str]]:
    """Maintenance-period rows (with source URL) for the requested years,
    discovered from the index page; 2027 added from the known release.

    Releases overlap, so they are read oldest first and merged per label:
    * a newer release wins (2024 brought the end of MP 8/2023 forward; the
      2027 release completes MP 8/2026, whose end the 2026 one gives as "tbd");
    * a year's own release defines which MPs that year has (the 2014 release
      holds a monthly 2015 calendar, 12 MPs, superseded by the 2015 release's 8);
    * prose amendments apply last (MP 12/2014 extended to 27 Jan 2015 in the
      2015 release).
    Rows still lacking an end are dropped. Kept: label year or end year requested.
    """
    index_html = fetch(ECB_RESERVE_INDEX_URL)
    save_fixture("ecb_reserve_index", index_html)
    links = ecb_index_links(index_html)
    links.setdefault(2027, ECB_MP_2027_URL)
    wanted = set(years or links)
    fetch_years = sorted(wanted | {y + 1 for y in wanted if y + 1 in links})
    merged: dict[str, tuple[dict, str]] = {}
    own_labels: dict[int, set[str]] = {}
    amendments: list[tuple[str, dt.date, str]] = []
    seen_urls: set[str] = set()
    for y in fetch_years:
        url = links.get(y)
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)
        try:
            t = fetch_text(url, f"ecb_mp_{y}")
        except Exception as exc:  # pragma: no cover
            print(f"  ecb {y}: fetch failed ({exc})")
            continue
        for row in parse_ecb_mp_table(t, year_hint=y):
            label_year = int(row["label"].split("/")[1])
            if links.get(label_year) == url:
                own_labels.setdefault(label_year, set()).add(row["label"])
            if row["end"] is None and row["label"] in merged:
                continue
            merged[row["label"]] = (row, url)
        amendments += [(label, end, url) for label, end in parse_ecb_mp_amendments(t).items()]
    for label, end, url in amendments:
        if label in merged:
            merged[label] = (dict(merged[label][0], end=end), url)
    out = []
    for label, (row, url) in merged.items():
        label_year = int(label.split("/")[1])
        if label_year in own_labels and label not in own_labels[label_year]:
            continue
        if row["end"] is None or not (label_year in wanted or row["end"].year in wanted):
            continue
        out.append((row, url))
    return sorted(out, key=lambda ru: ru[0]["start"])


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


def parse_boj_text(text: str) -> list[tuple[dt.date, str]]:
    """Decision date = last day of the meeting cell. Rows mentioning
    'unscheduled' or 'extraordinary' are tagged unscheduled."""
    out = []
    year = None
    for row in join_table_rows(text):
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
