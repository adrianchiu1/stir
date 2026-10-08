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
  (current and next year only); every past decision since June 1997 is in the
  MPC voting-history workbook (mpcvoting.xlsx, sheet "Bank Rate Decisions").
* BoJ: https://www.boj.or.jp/en/mopo/mpmsche_minu/index.htm (current and next
  year) and .../past.htm (2010+): one table per year whose first column is
  "Jan. 22 (Thurs.), 23 (Fri.)" (decision on the last day; one-day meetings
  occur, e.g. "Apr. 30 (Fri.)"). Every meeting since January 1998 is in the
  minutes indexes .../minu_<YYYY>/index.htm ("Meeting on May 10, 2010"); the
  minutes of an unscheduled meeting say so ("the Unscheduled Monetary Policy
  Meeting"), which is how unscheduled meetings are classified.

All four parsers are validated against live pages captured 8 Oct 2026
(``tests/fixtures/live``).
"""
from __future__ import annotations

import datetime as dt
import re

from .common import MONTH_RE, fetch, fetch_text, html_to_text, join_table_rows, month_number, save_fixture

FED_CALENDAR_URL = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
FED_HISTORICAL_URL = "https://www.federalreserve.gov/monetarypolicy/fomchistorical{year}.htm"
ECB_RESERVE_INDEX_URL = "https://www.ecb.europa.eu/press/calendars/reserve/html/index.en.html"
ECB_MP_2027_URL = "https://www.ecb.europa.eu/press/pr/date/2026/html/ecb.pr260630~9f54a0a4fb.en.html"
BOE_UPCOMING_URL = "https://www.bankofengland.co.uk/monetary-policy/upcoming-mpc-dates"
BOE_VOTING_XLSX_URL = "https://www.bankofengland.co.uk/-/media/boe/files/monetary-policy-summary-and-minutes/mpcvoting.xlsx"
BOJ_SCHEDULE_URL = "https://www.boj.or.jp/en/mopo/mpmsche_minu/index.htm"
BOJ_PAST_URL = "https://www.boj.or.jp/en/mopo/mpmsche_minu/past.htm"
BOJ_MINUTES_INDEX_URL = "https://www.boj.or.jp/en/mopo/mpmsche_minu/minu_{year}/index.htm"
BOJ_FIRST_MINUTES_YEAR = 1998


# ---------------------------------------------------------------------------
# Fed
# ---------------------------------------------------------------------------
_FED_YEAR_RE = re.compile(r"\b(20\d\d|19\d\d)\s+FOMC\s+Meetings\b", re.I)
_FED_MONTH_RE = re.compile(rf"^\s*\*?\*?\s*{MONTH_RE}(?:\s*/\s*{MONTH_RE})?\s*\*?\*?\s*$", re.I)
_FED_DAYS_RE = re.compile(r"^\s*(\d{1,2})(?:\s*[-–]\s*(\d{1,2}))?\*?\s*(\(([^)]*)\))?\s*(Meeting)?\s*$", re.I)
# historical pages: "January 26-27 Meeting", "March 15 (unscheduled) Meeting", "July 31-August 1 Meeting"
# also "January 21 Conference Call - 2008" and "October 4 (unscheduled) - 2019"
_FED_HIST_RE = re.compile(
    rf"\b{MONTH_RE}(?:\s*/\s*{MONTH_RE})?\s+(\d{{1,2}})(?:\s*[-–]\s*(?:{MONTH_RE}\s+)?(\d{{1,2}}))?\*?\s*(\(([^)]*)\))?"
    r"\s*(Meeting\b|Conference Call\b|(?=-\s*\d{4}\s*$))", re.I)


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
            ma, mb, d1, mc, d2, _, note, what = m.groups()
            if what.lower().startswith("conference") or (not what and not note):
                note = f"{note or ''} conference call"
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


_FED_STATEMENT_LINK_RE = re.compile(
    r'<a\b[^>]*href="[^"]*?/(?:monetary/|monetary)(\d{4})(\d{2})(\d{2})[a-z0-9]*(?:/default)?\.htm"[^>]*>\s*Statement\s*</a>', re.I)
_MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                "October", "November", "December"]


def fed_inline_statement_dates(html: str) -> str:
    """Historical pages link each block's statement to a dated press release
    (``/newsevents/press/monetary/20080122b.htm``); write that date into the
    link text, "Statement (Released January 22, 2008)", so the text parser sees
    when a conference-call decision was announced (21 Jan call -> 22 Jan)."""
    def repl(m: re.Match) -> str:
        y, mo, d = (int(g) for g in m.groups())
        return f"{m.group(0)[:-4].rsplit('>', 1)[0]}>Statement (Released {_MONTH_NAMES[mo - 1]} {d}, {y})</a>"
    return _FED_STATEMENT_LINK_RE.sub(repl, html)


def fetch_fed(years_historical: range | None = None) -> list[tuple[dt.date, str, str]]:
    """Current calendar page plus historical pages for ``years_historical``.
    Returns (decision_date, kind, source_url)."""
    out = []
    text = fetch_text(FED_CALENDAR_URL, "fed_calendar")
    out += [(d, k, FED_CALENDAR_URL) for d, k in parse_fed_text(text)]
    for y in years_historical or []:
        url = FED_HISTORICAL_URL.format(year=y)
        try:
            t = fetch_text(url, f"fed_historical_{y}", prepare=fed_inline_statement_dates)
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
        if len(cells) < 3:
            continue
        if not _ECB_MP_LABEL_RE.match(cells[0]):
            # 2004-2006 releases: no MP column; meeting ("-" for the transitional
            # MP of 24 Jan 2004) | start | end. Numbered by start date below.
            meeting, start, end = (_ecb_date(c) for c in cells[:3])
            if start and end and (meeting or cells[0] == "-"):
                rows.append({"label": None, "meeting": meeting, "start": start, "end": end})
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
    counter: dict[int, int] = {}
    for r in sorted((r for r in rows if r["label"] is None), key=lambda r: r["start"]):
        counter[r["start"].year] = counter.get(r["start"].year, 0) + 1
        r["label"] = f"{counter[r['start'].year]}/{r['start'].year}"
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


_ECB_EXTEND_RE = re.compile(
    r"\b(\d{1,2})(?:st|nd|rd|th)?\s+(?:reserve\s+)?maintenance period of (\d{4}) will be extended\b[^.]*?\bend on "
    rf"(\d{{1,2}}\s+{MONTH_RE}\w*\s+\d{{4}})", re.I)


_ECB_NEW_END_RE = re.compile(
    rf"\blast day of the [^.]*?maintenance period is now (\d{{1,2}}\s+{MONTH_RE}\w*\s+\d{{4}}),?\s+instead of "
    rf"(\d{{1,2}}\s+{MONTH_RE}\w*\s+\d{{4}})", re.I)


def parse_ecb_mp_amendments(text: str) -> dict[str | dt.date, dt.date]:
    """Changes announced in the prose of a release rather than its table, as
    {MP label or old end date: new end date}:
    'The 12th reserve maintenance period of 2014 will be extended by 14 days
    and end on 27 January 2015' -> {'12/2014': 2015-01-27};
    'the last day of the last maintenance period is now 18 January 2005,
    instead of 19 January 2005' -> {2005-01-19: 2005-01-18}."""
    flat = " ".join(text.split())
    out: dict[str | dt.date, dt.date] = {}
    for m in _ECB_EXTEND_RE.finditer(flat):
        n, y, d = m.groups()[:3]
        out[f"{int(n)}/{y}"] = _ecb_date(d)
    for m in _ECB_NEW_END_RE.finditer(flat):
        out[_ecb_date(m.group(3))] = _ecb_date(m.group(1))
    return out


def fetch_ecb_maintenance(years: range | None = None, include_open: bool = False) -> list[tuple[dict, str]]:
    """Maintenance-period rows (with source URL) for the requested years,
    discovered from the index page; 2027 added from the known release.

    Releases overlap, so they are read oldest first and merged per label:
    * a newer release wins (2024 brought the end of MP 8/2023 forward; the
      2027 release completes MP 8/2026, whose end the 2026 one gives as "tbd");
    * a year's own release defines which MPs that year has (the 2014 release
      holds a monthly 2015 calendar, 12 MPs, superseded by the 2015 release's 8);
    * prose amendments apply last (MP 12/2014 extended to 27 Jan 2015 in the
      2015 release; MP 11/2004 shortened to 18 Jan 2005 in the 2005 release).
    Rows still lacking an end ("tbd": the last MP of the newest release) are
    dropped unless ``include_open``; their meeting and start date are published,
    so the meeting updater uses them. Kept: label year or end year requested.
    """
    index_html = fetch(ECB_RESERVE_INDEX_URL)
    save_fixture("ecb_reserve_index", index_html)
    links = ecb_index_links(index_html)
    links.setdefault(2027, ECB_MP_2027_URL)
    wanted = set(years or links)
    fetch_years = sorted(wanted | {y + 1 for y in wanted if y + 1 in links})
    merged: dict[str, tuple[dict, str]] = {}
    own_labels: dict[int, set[str]] = {}
    amendments: list[tuple[str | dt.date, dt.date, str]] = []
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
    for key, end, url in amendments:
        label = key if isinstance(key, str) else next(
            (lb for lb, (r, _) in merged.items() if r["end"] == key), None)     # matched by its old end date
        if label in merged:
            merged[label] = (dict(merged[label][0], end=end), url)
    out = []
    for label, (row, url) in merged.items():
        label_year = int(label.split("/")[1])
        if label_year in own_labels and label not in own_labels[label_year]:
            continue
        if row["end"] is None:
            if include_open and label_year in wanted:
                out.append((row, url))
            continue
        if not (label_year in wanted or row["end"].year in wanted):
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


def boe_voting_xlsx_to_text(content: bytes) -> str:
    """The 'Bank Rate Decisions' sheet as text, one decision per line:
    '2020-03-11 | 0.25' (decision date | Bank Rate decided, percent). This text
    is what the parser reads and what --save-fixtures stores."""
    import io

    import openpyxl
    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    ws = wb["Bank Rate Decisions"]
    lines = ["MPC voting history - Bank Rate decisions", "Decision date | Bank Rate (%)"]
    for row in ws.iter_rows(values_only=True):
        d, rate = (row[1], row[2]) if len(row) > 2 else (None, None)
        if isinstance(d, dt.datetime) and isinstance(rate, (int, float)):
            lines.append(f"{d.date().isoformat()} | {round(rate * 100, 4):g}")
    return "\n".join(lines) + "\n"


_BOE_VOTE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}) \| (-?[\d.]+)$")


def parse_boe_voting_text(text: str) -> list[tuple[dt.date, str]]:
    """Every MPC Bank Rate decision in the workbook. The workbook does not mark
    special (unscheduled) meetings; those are kept in boe_unscheduled.csv and
    the updater leaves them there."""
    return [(dt.date.fromisoformat(m.group(1)), "scheduled")
            for m in map(_BOE_VOTE_RE.match, text.splitlines()) if m]


def fetch_boe() -> list[tuple[dt.date, str, str]]:
    """Upcoming-dates page (this year and next) plus the voting-history workbook (1997+)."""
    import requests
    from .common import TIMEOUT, USER_AGENT
    text = fetch_text(BOE_UPCOMING_URL, "boe_upcoming_mpc_dates")
    out = [(d, k, BOE_UPCOMING_URL) for d, k in parse_boe_text(text)]
    r = requests.get(BOE_VOTING_XLSX_URL, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
    r.raise_for_status()
    vtext = boe_voting_xlsx_to_text(r.content)
    save_fixture("boe_mpc_voting", vtext)
    out += [(d, k, BOE_VOTING_XLSX_URL) for d, k in parse_boe_voting_text(vtext)]
    return out


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


_BOJ_MINUTES_LINK_RE = re.compile(
    r'(<a\b[^>]*href="([^"]*/minu_\d{4}/g\d{6}[a-z]?\.(?:htm|pdf))"[^>]*>)(.*?)</a>', re.I | re.S)
_BOJ_MINUTES_ROW_RE = re.compile(
    rf"Meeting on {MONTH_RE}\.?\s+(\d{{1,2}})(?:\s*(?:and|-|–)\s*(?:{MONTH_RE}\.?\s+)?(\d{{1,2}})(?!\d))?(?:,\s*(\d{{4}}))?"
    r".*?\[minutes: (\S+)\]", re.I)
# the minutes' own statement of purpose, not a mention in the discussion ("the Bank
# could take timely actions, including an unscheduled Monetary Policy Meeting")
_BOJ_UNSCHEDULED_RE = re.compile(
    r"\b(?:Purpose\s+of\s+(?:the|this)\s+Unscheduled|call(?:ed)?\s+(?:an|the|this)\s+unscheduled)\s+"
    r"Monetary\s+Policy\s+Meeting\b", re.I)


def boj_inline_minutes_links(html: str) -> str:
    """Keep each minutes link in the text: 'Meeting on May 10, 2010 [minutes: <url>]'."""
    def repl(m: re.Match) -> str:
        url = m.group(2) if m.group(2).startswith("http") else "https://www.boj.or.jp" + m.group(2)
        return f"{m.group(1)}{m.group(3)} [minutes: {url}]</a>"
    return _BOJ_MINUTES_LINK_RE.sub(repl, html)


def parse_boj_minutes_index(text: str, year: int) -> list[tuple[dt.date, str, bool]]:
    """(decision date, minutes URL, one-day meeting) for every meeting in one
    year's minutes index. 'Meeting on December 18 and 19' (1998-2005 omit the
    year) -> 19 Dec."""
    out = []
    for line in text.splitlines():
        m = _BOJ_MINUTES_ROW_RE.search(line)
        if not m:
            continue
        ma, d1, mb, d2, y, url = m.groups()
        month = month_number(mb or ma)
        out.append((dt.date(int(y or year), month, int(d2 or d1)), url, d2 is None))
    return sorted(out)


def boj_minutes_unscheduled(text: str) -> bool:
    """True when the minutes call the meeting unscheduled ('Remarks on the Purpose
    of the Unscheduled Monetary Policy Meeting'; 'call an unscheduled ...')."""
    return bool(_BOJ_UNSCHEDULED_RE.search(" ".join(text.split())))


def boj_minutes_text(url: str) -> str:
    """Plain text of one set of minutes (HTML until 2005 and again from 2025, PDF otherwise)."""
    if url.lower().endswith(".pdf"):
        import io

        import requests
        import logging

        from pypdf import PdfReader
        from .common import TIMEOUT, USER_AGENT
        logging.getLogger("pypdf").setLevel(logging.CRITICAL)   # font-encoding chatter
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
        r.raise_for_status()
        texts = []
        for page in PdfReader(io.BytesIO(r.content)).pages[:8]:   # the purpose comes after the attendance list
            texts.append(page.extract_text() or "")
            if boj_minutes_unscheduled(texts[-1]):
                break
        return "\n".join(texts)
    return html_to_text(fetch(url))


def fetch_boj_minutes(years: range | None = None, classify=None) -> list[tuple[dt.date, str, str]]:
    """Meetings from the minutes indexes (default: 1998 to this year) as
    (decision, kind, source_url); an unscheduled meeting's source is its
    minutes. Minutes are read only for one-day meetings (an unscheduled meeting
    is called for one day), and of those only where ``classify(date)`` is true
    when a predicate is given. Each document read goes into the 'boj_minutes_checked'
    fixture (url, opening 400 characters and the passage naming the meeting
    unscheduled, if any)."""
    years = years or range(BOJ_FIRST_MINUTES_YEAR, dt.date.today().year + 1)
    out, checked = [], []
    for y in years:
        try:
            t = fetch_text(BOJ_MINUTES_INDEX_URL.format(year=y), f"boj_minutes_index_{y}", prepare=boj_inline_minutes_links)
        except Exception as exc:  # pragma: no cover
            print(f"  boj minutes {y}: fetch failed ({exc})")
            continue
        for d, url, one_day in parse_boj_minutes_index(t, y):
            kind = "scheduled"
            if one_day and (classify is None or classify(d)):
                body = " ".join(boj_minutes_text(url).split())
                hit = _BOJ_UNSCHEDULED_RE.search(body)
                excerpt = body[:400] + (" ... " + body[max(0, hit.start() - 300):hit.end() + 300] if hit else "")
                checked.append(f"=== {d} {url}\n{excerpt}")
                if boj_minutes_unscheduled(body):
                    kind = "unscheduled"
            out.append((d, kind, url if kind == "unscheduled" else BOJ_MINUTES_INDEX_URL.format(year=y)))
    if checked:
        save_fixture("boj_minutes_checked", "\n".join(checked) + "\n")
    return out
