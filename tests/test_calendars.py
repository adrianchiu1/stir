import datetime as dt
from stircurve.refdata.calendars import (Calendar, easter_sunday, nth_weekday, third_wednesday,
                                        parse_tenor, add_months, rules_us_fed, rules_jp, rules_uk, rules_target)


def test_easter():
    assert easter_sunday(2024) == dt.date(2024, 3, 31)
    assert easter_sunday(2026) == dt.date(2026, 4, 5)
    assert easter_sunday(2027) == dt.date(2027, 3, 28)


def test_nth_weekday_and_imm():
    assert nth_weekday(2026, 11, 3, 4) == dt.date(2026, 11, 26)   # Thanksgiving 2026
    assert nth_weekday(2026, 5, 0, -1) == dt.date(2026, 5, 25)    # Memorial Day 2026
    assert third_wednesday(2026, 12) == dt.date(2026, 12, 16)
    assert third_wednesday(2027, 3) == dt.date(2027, 3, 17)


def test_us_fed_2026_matches_chicago_fed_page():
    h = rules_us_fed(2026)
    expected = {dt.date(2026, 1, 1), dt.date(2026, 1, 19), dt.date(2026, 2, 16), dt.date(2026, 5, 25),
                dt.date(2026, 6, 19), dt.date(2026, 9, 7), dt.date(2026, 10, 12), dt.date(2026, 11, 11),
                dt.date(2026, 11, 26), dt.date(2026, 12, 25)}
    assert expected <= set(h)
    assert dt.date(2026, 7, 3) not in h          # Saturday holiday not observed by Reserve Banks
    h27 = rules_us_fed(2027)
    assert dt.date(2027, 7, 5) in h27             # Sunday -> Monday
    assert dt.date(2027, 6, 18) not in h27        # Juneteenth on Saturday


def test_target():
    h = rules_target(2026)
    assert set(h) == {dt.date(2026, 1, 1), dt.date(2026, 4, 3), dt.date(2026, 4, 6), dt.date(2026, 5, 1),
                      dt.date(2026, 12, 25), dt.date(2026, 12, 26)}


def test_uk_known_dates():
    h = rules_uk(2026)
    assert dt.date(2026, 5, 4) in h and dt.date(2026, 5, 25) in h and dt.date(2026, 8, 31) in h
    assert dt.date(2026, 12, 28) in h             # Boxing Day Saturday -> Monday substitute
    assert dt.date(2023, 5, 8) in rules_uk(2023)  # coronation
    assert dt.date(2022, 9, 19) in rules_uk(2022)


def test_jp_known_dates():
    h = rules_jp(2026)
    assert dt.date(2026, 1, 12) in h              # Coming of Age Day (2nd Monday)
    assert dt.date(2026, 2, 23) in h              # Emperor's Birthday
    assert dt.date(2026, 5, 6) in h               # substitute for Constitution Day (3 May Sunday)
    assert dt.date(2026, 1, 2) in h and dt.date(2026, 12, 31) in h
    assert dt.date(2024, 3, 20) in rules_jp(2024)  # vernal equinox
    assert dt.date(2025, 9, 23) in rules_jp(2025)  # autumnal equinox


def test_adjust_and_tenor():
    cal = Calendar.load("us_sifma")
    assert cal.adjust(dt.date(2026, 7, 4)) == dt.date(2026, 7, 6)
    assert cal.adjust(dt.date(2026, 7, 3), "preceding") == dt.date(2026, 7, 2)
    # modified following rolls back across month-end
    assert cal.adjust(dt.date(2027, 1, 31), "modified_following") == dt.date(2027, 1, 29)
    assert parse_tenor("1Y3M") == (15, 0, 0) and parse_tenor("2W") == (0, 0, 2) and parse_tenor("ON") == (0, 1, 0)
    assert add_months(dt.date(2026, 1, 31), 1) == dt.date(2026, 2, 28)
    spot = dt.date(2026, 10, 12)
    assert cal.add_tenor(spot, "1M") == dt.date(2026, 11, 12)
    # 12 Nov 2029 is Veterans Day observed (11 Nov is a Sunday) -> modified following gives 13 Nov
    assert cal.add_tenor(spot, "3Y1M") == dt.date(2029, 11, 13)
    # EOM rule: last business day of Feb 2026 (Fri 27) + 1M -> last business day of March
    assert cal.add_tenor(dt.date(2026, 2, 27), "1M") == dt.date(2026, 3, 31)


def test_business_day_count():
    cal = Calendar.load("target")
    assert cal.business_days_between(dt.date(2026, 12, 21), dt.date(2026, 12, 28)) == 4  # 21-24; 25-26 closed, 27 Sunday


def test_jp_rules_before_happy_monday_match_cabinet_office():
    """1994-2006 eras: fixed-date holidays before the Happy Monday law, Greenery Day on
    29 Apr and a citizens' holiday on 4 May before 2007, Monday-only substitutes."""
    from pathlib import Path
    from stircurve.refdata.calendars import Calendar
    from stircurve.refdata.parsers.holidays import parse_jp_csv
    live = Path(__file__).parent / "fixtures" / "live" / "jp_cao_holidays_20261008.txt"
    official = {d for d in parse_jp_csv(live.read_text()) if 1994 <= d.year <= 2027 and d.weekday() < 5}
    rules = {d for d, n in Calendar.from_rules("jp", range(1994, 2028)).holidays.items()
             if d.weekday() < 5 and n != "Bank Holiday"}
    assert rules == official
