import datetime as dt
from pathlib import Path
from stircurve.refdata.parsers.banks import (parse_fed_text, parse_ecb_mp_table, parse_ecb_mp_amendments, parse_boe_text,
                                            parse_boj_text, ecb_index_links)
from stircurve.refdata.parsers.holidays import parse_uk_json, parse_jp_csv
from stircurve.refdata.parsers.common import html_to_text

FIX = Path(__file__).parent / "fixtures"


def test_fed_calendar_page():
    got = parse_fed_text((FIX / "fed_calendar_2026_2027.txt").read_text())
    sched = sorted(d for d, k in got if k == "scheduled")
    assert dt.date(2026, 1, 28) in sched and dt.date(2026, 12, 9) in sched
    assert dt.date(2024, 5, 1) in sched                 # Apr/May 30-1
    assert dt.date(2023, 2, 1) in sched                 # Jan/Feb 31-1
    assert dt.date(2027, 12, 8) in sched
    assert all(k != "scheduled" for d, k in got if d == dt.date(2025, 8, 22))   # notation vote skipped
    assert len([d for d in sched if d.year == 2026]) == 8


def test_fed_historical_page():
    got = parse_fed_text((FIX / "fed_historical_2020.txt").read_text())
    assert (dt.date(2020, 3, 15), "unscheduled") in got
    assert (dt.date(2020, 3, 18), "scheduled") in got
    assert len([d for d, k in got if k == "scheduled"]) == 8


def test_ecb_mp_table():
    rows = parse_ecb_mp_table((FIX / "ecb_mp_2027.txt").read_text(), year_hint=2027)
    assert len(rows) == 9
    assert rows[0]["label"] == "8/2026" and rows[0]["start"] == dt.date(2026, 12, 23)
    assert rows[3]["label"] == "3/2027" and rows[3]["start"] == dt.date(2027, 5, 6) and rows[3]["meeting"] == dt.date(2027, 4, 29)
    assert rows[-1]["end"] == dt.date(2028, 2, 8)


def test_ecb_mp_table_from_html():
    html = "<table><tr><th>MP</th><th>Relevant Governing Council meeting</th><th>Start of MP</th><th>End of MP</th></tr>" \
           "<tr><td>1</td><td>Thu, 4-Feb-27</td><td>Wed, 10-Feb-27</td><td>Tue, 23-Mar-27</td></tr></table>"
    rows = parse_ecb_mp_table(html_to_text(html), year_hint=2027)
    assert rows == [{"label": "1/2027", "meeting": dt.date(2027, 2, 4), "start": dt.date(2027, 2, 10), "end": dt.date(2027, 3, 23)}]


def test_ecb_index_links():
    html = '<a href="/press/pr/date/2016/html/pr160914.en.html">Indicative operational calendars for 2017 and 2018</a>' \
           '<a href="https://www.ecb.europa.eu/press/pr/date/2025/html/ecb.pr250424~2643533670.en.html">Indicative operational calendars for 2026</a>'
    links = ecb_index_links(html)
    assert links[2017] == links[2018] == "https://www.ecb.europa.eu/press/pr/date/2016/html/pr160914.en.html"
    assert links[2026].endswith("ecb.pr250424~2643533670.en.html")


def test_boe_and_boj_text():
    boe = parse_boe_text((FIX / "boe_dates.txt").read_text())
    assert [d for d, _ in boe] == [dt.date(2026, 2, 5), dt.date(2026, 3, 19), dt.date(2026, 4, 30), dt.date(2026, 6, 18)]
    boj = parse_boj_text((FIX / "boj_schedule.txt").read_text())
    assert [d for d, _ in boj] == [dt.date(2026, 1, 23), dt.date(2026, 3, 19), dt.date(2026, 4, 28), dt.date(2026, 6, 16)]


def test_holiday_sources():
    uk = parse_uk_json('{"england-and-wales":{"events":[{"title":"Good Friday","date":"2026-04-03"}]}}')
    assert uk == {dt.date(2026, 4, 3): "Good Friday"}
    jp = parse_jp_csv("国民の祝日・休日月日,国民の祝日・休日名\n2026/1/1,元日\n2026/1/12,成人の日\n")
    assert jp[dt.date(2026, 1, 12)] == "成人の日"


LIVE = FIX / "live"


def test_boe_live_page():
    got = [d for d, k in parse_boe_text((LIVE / "boe_upcoming_mpc_dates_20261008.txt").read_text())]
    assert got == [dt.date(2026, 2, 5), dt.date(2026, 3, 19), dt.date(2026, 4, 30), dt.date(2026, 6, 18),
                   dt.date(2026, 7, 30), dt.date(2026, 9, 17), dt.date(2026, 11, 5), dt.date(2026, 12, 17),
                   dt.date(2027, 2, 4), dt.date(2027, 3, 18), dt.date(2027, 4, 29), dt.date(2027, 6, 17),
                   dt.date(2027, 7, 29), dt.date(2027, 9, 16), dt.date(2027, 11, 4), dt.date(2027, 12, 16)]
    assert all(d.weekday() == 3 for d in got)        # MPC announcements are Thursdays


def test_boj_live_schedule_page():
    got = parse_boj_text((LIVE / "boj_mpm_schedule_20261008.txt").read_text())
    assert [d for d, _ in got] == [
        dt.date(2026, 1, 23), dt.date(2026, 3, 19), dt.date(2026, 4, 28), dt.date(2026, 6, 16),
        dt.date(2026, 7, 31), dt.date(2026, 9, 18), dt.date(2026, 10, 30), dt.date(2026, 12, 18),
        dt.date(2027, 1, 22), dt.date(2027, 3, 18), dt.date(2027, 4, 28), dt.date(2027, 6, 11),   # "Mar. 17\n(Wed.), 18"
        dt.date(2027, 7, 22), dt.date(2027, 9, 22), dt.date(2027, 10, 29), dt.date(2027, 12, 17)]
    assert {k for _, k in got} == {"scheduled"}


def test_boj_live_past_page():
    got = parse_boj_text((LIVE / "boj_mpm_past_20261008.txt").read_text())
    by_year = {}
    for d, _ in got:
        by_year.setdefault(d.year, []).append(d)
    assert {y: len(v) for y, v in by_year.items()} == {
        2010: 16, 2011: 15, 2012: 14, 2013: 14, 2014: 14, 2015: 14, 2016: 8, 2017: 8, 2018: 8,
        2019: 8, 2020: 9, 2021: 8, 2022: 8, 2023: 8, 2024: 8, 2025: 8}
    dates = {d for d, _ in got}
    # README / D15 confirmations; one-day and moved meetings
    assert {dt.date(2024, 3, 19), dt.date(2025, 12, 19), dt.date(2010, 8, 30), dt.date(2020, 3, 16),
            dt.date(2020, 5, 22), dt.date(2011, 3, 14)} <= dates
    assert dt.date(2020, 3, 19) not in dates           # brought forward to 16 Mar 2020


def test_fed_live_historical_pages():
    counts = {}
    for y in range(2010, 2021):
        got = parse_fed_text(f"{y} FOMC Meetings\n" + (LIVE / f"fed_historical_{y}_20261008.txt").read_text())
        counts[y] = len([d for d, k in got if k == "scheduled"])
        if y == 2012:
            assert dt.date(2012, 8, 1) in [d for d, _ in got]                 # "July 31-August 1 Meeting"
        if y == 2020:
            assert (dt.date(2020, 3, 18), "skip") in got                     # "March 17-18 (cancelled)"
            # "March 2 (unscheduled) Meeting", statement released March 3: decision = 3 Mar;
            # "minutes of March 15 meeting" is not a meeting
            assert [d for d, k in got if k == "unscheduled"] == [dt.date(2020, 3, 3), dt.date(2020, 3, 15)]
    assert counts == {**{y: 8 for y in range(2010, 2020)}, 2020: 7}


def test_ecb_live_two_year_release_and_tbd_rows():
    rows = parse_ecb_mp_table((LIVE / "ecb_mp_2010_20261008.txt").read_text(), year_hint=2010)
    assert [r["label"] for r in rows] == [f"{i}/2010" for i in range(1, 13)] + [f"{i}/2011" for i in range(1, 13)]
    assert rows[0] == {"label": "1/2010", "meeting": dt.date(2010, 1, 14), "start": dt.date(2010, 1, 20), "end": dt.date(2010, 2, 9)}
    rows = parse_ecb_mp_table((LIVE / "ecb_mp_2022_20261008.txt").read_text(), year_hint=2022)
    assert rows[0]["label"] == "8/2021" and rows[-1] == {"label": "8/2022", "meeting": dt.date(2022, 12, 15),
                                                        "start": dt.date(2022, 12, 21), "end": None}   # end "tbd"
    rows = parse_ecb_mp_table((LIVE / "ecb_mp_2025_20261008.txt").read_text(), year_hint=2025)
    assert rows[0]["label"] == "8/2024" and rows[0]["end"] == dt.date(2025, 2, 4)          # "4 February2025"
    assert parse_ecb_mp_amendments((LIVE / "ecb_mp_2015_20261008.txt").read_text()) == {"12/2014": dt.date(2015, 1, 27)}
    assert parse_ecb_mp_amendments((LIVE / "ecb_mp_2005_20261008.txt").read_text()) == {dt.date(2005, 1, 19): dt.date(2005, 1, 18)}
    rows = parse_ecb_mp_table((LIVE / "ecb_mp_2004_20261008.txt").read_text(), year_hint=2004)   # no MP column
    assert rows[0] == {"label": "1/2004", "meeting": None, "start": dt.date(2004, 1, 24), "end": dt.date(2004, 3, 9)}
    assert rows[1] == {"label": "2/2004", "meeting": dt.date(2004, 3, 4), "start": dt.date(2004, 3, 10), "end": dt.date(2004, 4, 6)}


def test_ecb_live_replay_merges_releases_without_gaps():
    """fetch_ecb_maintenance replayed offline from the captured fixtures."""
    from stircurve.refdata.parsers import banks
    from stircurve.refdata.maintenance import MaintenancePeriod, validate_maintenance_periods
    index = (LIVE / "ecb_reserve_index_20261008.txt").read_text()
    links = ecb_index_links(index)
    links.setdefault(2027, banks.ECB_MP_2027_URL)
    by_url = {}
    for y, url in links.items():
        if 2010 <= y <= 2027:
            by_url.setdefault(url, (LIVE / f"ecb_mp_{y}_20261008.txt").read_text())
    orig = banks.fetch, banks.fetch_text
    banks.fetch = lambda url, timeout=30: index
    banks.fetch_text = lambda url, source: by_url[url]
    try:
        got = banks.fetch_ecb_maintenance(range(2010, 2028))
    finally:
        banks.fetch, banks.fetch_text = orig
    labels = [r["label"] for r, _ in got]
    assert len(got) == 5 * 12 + 13 * 8
    assert labels[0] == "1/2010" and labels[-1] == "8/2027"
    assert not any(l.endswith("/2015") and int(l.split("/")[0]) > 8 for l in labels)   # superseded monthly 2015
    mps = [MaintenancePeriod(r["label"], r["meeting"], r["start"], r["end"]) for r, _ in got]
    assert validate_maintenance_periods(mps) == []
    ends = {r["label"]: r["end"] for r, _ in got}
    assert ends["12/2014"] == dt.date(2015, 1, 27) and ends["8/2023"] == dt.date(2024, 1, 30)


def test_holiday_live_sources():
    from stircurve.refdata.parsers.holidays import parse_sifma_text
    sifma = parse_sifma_text((LIVE / "sifma_holidays_20261008.txt").read_text())
    assert len(sifma) == 12 and min(sifma) == dt.date(2026, 1, 1) and max(sifma) == dt.date(2027, 1, 1)
    assert dt.date(2026, 4, 3) not in sifma          # Good Friday 2026: early close only
    assert dt.date(2026, 4, 6) not in sifma          # Easter Monday is in the U.K. section
    uk = parse_uk_json((LIVE / "uk_bank_holidays_20261008.txt").read_text())
    assert len(uk) == 83 and uk[dt.date(2026, 12, 28)] == "Boxing Day"
    jp = parse_jp_csv((LIVE / "jp_cao_holidays_20261008.txt").read_text())
    assert len(jp) == 1067 and jp[dt.date(2026, 9, 22)] == "休日"
