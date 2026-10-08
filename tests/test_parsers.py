import datetime as dt
from pathlib import Path
from stircurve.refdata.parsers.banks import parse_fed_text, parse_ecb_mp_table, parse_boe_text, parse_boj_text, ecb_index_links
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
