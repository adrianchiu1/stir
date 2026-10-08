import datetime as dt
from stircurve.refdata.calendars import Calendar
from stircurve.refdata.meetings import (BANKS, Meeting, effective_date, ecb_rule_effective, extrapolate_cadence,
                                       load_meetings, parcels, MeetingSchedule)
from stircurve.refdata.maintenance import load_maintenance_periods, mp_lookup, validate_maintenance_periods


def test_effective_rules():
    us = Calendar.load("us_fed"); uk = Calendar.load("uk"); jp = Calendar.load("jp"); tg = Calendar.load("target")
    assert effective_date("fed", dt.date(2025, 12, 10), us) == dt.date(2025, 12, 11)
    assert effective_date("fed", dt.date(2026, 12, 9), us) == dt.date(2026, 12, 10)
    assert effective_date("boe", dt.date(2025, 12, 18), uk) == dt.date(2025, 12, 18)
    assert effective_date("boj", dt.date(2025, 1, 24), jp) == dt.date(2025, 1, 27)   # Friday -> Monday
    assert effective_date("boj", dt.date(2025, 12, 19), jp) == dt.date(2025, 12, 22)
    assert effective_date("boj", dt.date(2024, 3, 19), jp) == dt.date(2024, 3, 21)   # 20 Mar 2024 holiday
    # ECB rule fallback: Thursday -> following Wednesday
    assert ecb_rule_effective(dt.date(2027, 2, 4), tg) == dt.date(2027, 2, 10)
    # ECB published table overrides the rule (MP 3/2027 starts Thu 6 May)
    look = mp_lookup(load_maintenance_periods())
    assert effective_date("ecb", dt.date(2027, 4, 29), tg, look) == dt.date(2027, 5, 6)
    assert ecb_rule_effective(dt.date(2027, 4, 29), tg) == dt.date(2027, 5, 5)


def test_maintenance_periods_contiguous():
    mps = load_maintenance_periods()
    assert len(mps) == 5 * 12 + 13 * 8          # monthly 2010-14, eight a year 2015-27 (live run 8 Oct 2026)
    assert validate_maintenance_periods(mps) == []
    by = {m.label: m for m in mps}
    assert by["8/2026"].length_days == 49 and by["1/2027"].length_days == 42 and by["1/2010"].length_days == 21


def test_fed_file_and_parcels():
    ms = load_meetings("fed")
    sched = [m for m in ms if m.scheduled]
    assert len(sched) == 143 and all(m.effective_date == Calendar.load("us_fed").next_business_day(m.decision_date) for m in sched)
    uns = [m for m in ms if not m.scheduled]
    assert {m.decision_date for m in uns} == {dt.date(2020, 3, 3), dt.date(2020, 3, 15)}
    ps = parcels(ms, dt.date(2026, 10, 8), dt.date(2027, 4, 1))
    assert ps[0].start == dt.date(2026, 10, 8) and ps[0].decision_date is None
    assert ps[1].start == dt.date(2026, 10, 29) and ps[1].decision_date == dt.date(2026, 10, 28)
    assert ps[-1].end == dt.date(2027, 4, 1)
    assert [p.decision_date for p in ps[1:]] == [dt.date(2026, 10, 28), dt.date(2026, 12, 9), dt.date(2027, 1, 27), dt.date(2027, 3, 17)]


def test_cadence_extrapolation_reproduces_published_year():
    """Use 2025 as template, generate 2026, compare with the published 2026 FOMC dates."""
    us = Calendar.load("us_fed")
    ms = [m for m in load_meetings("fed", include_unscheduled=False) if m.decision_date.year <= 2025]
    synth = extrapolate_cadence("fed", ms, dt.date(2026, 12, 31), us)
    gen26 = sorted(m.decision_date for m in synth if m.synthetic and m.decision_date.year == 2026)
    pub26 = sorted(m.decision_date for m in load_meetings("fed", False) if m.decision_date.year == 2026)
    assert len(gen26) == 8
    # Same weekday for every slot and never more than 10 days off. The Fed moved the
    # May 2025 slot to 29 Apr 2026, so one slot is a week out and in a different month:
    # cadence extrapolation is a research approximation, which is why rows are flagged synthetic.
    diffs = [abs((g - p).days) for g, p in zip(gen26, pub26)]
    assert all(g.weekday() == p.weekday() for g, p in zip(gen26, pub26))
    assert max(diffs) <= 10 and sum(d == 0 for d in diffs) >= 6


def test_schedule_three_year_horizon():
    sched = MeetingSchedule("fed")
    ps = sched.parcels(dt.date(2026, 10, 8), 3)
    assert ps[-1].end == dt.date(2029, 10, 8)
    syn = [p for p in ps if p.synthetic]
    assert syn and syn[0].start > dt.date(2027, 12, 9)        # synthetic only beyond the published 2027 calendar
    assert 22 <= len(ps) <= 26                                  # ~8 per year over 3 years plus stub


def test_ecb_schedule_uses_published_mp_starts():
    look = mp_lookup(load_maintenance_periods())
    sched = MeetingSchedule("ecb", mp_lookup=look)
    ps = sched.parcels(dt.date(2026, 12, 1), 1)
    assert ps[1].start == dt.date(2026, 12, 23) and ps[1].decision_date == dt.date(2026, 12, 17)
    assert ps[2].start == dt.date(2027, 2, 10)


def test_published_effective_dates_win_over_the_rule():
    from stircurve.refdata.meetings import load_published_effective, published_lookup
    jp = Calendar.load("jp")
    boj = published_lookup("boj")
    assert effective_date("boj", dt.date(2016, 1, 29), jp) == dt.date(2016, 2, 1)            # rule
    assert effective_date("boj", dt.date(2016, 1, 29), jp, boj) == dt.date(2016, 2, 16)      # published (k160129a)
    assert effective_date("boj", dt.date(2024, 3, 19), jp, boj) == dt.date(2024, 3, 21)      # rule still applies
    assert published_lookup("fed")[dt.date(2020, 3, 3)] == dt.date(2020, 3, 4)
    ecb = published_lookup("ecb")
    assert ecb[dt.date(2027, 4, 29)] == dt.date(2027, 5, 6)                                   # MP table
    for bank in BANKS:                                                                       # committed rows agree
        eff = {m.decision_date: m.effective_date for m in load_meetings(bank)}
        for d, (e, url) in load_published_effective(bank).items():
            assert url.startswith("https://") and eff.get(d, e) == e, (bank, d)


def test_policy_rate_changes_fall_on_meeting_effective_dates():
    """Fed target / ECB DFR / BoJ policy-rate changes since 2010 are implementation
    dates of committed meetings (published or rule)."""
    from stircurve.refdata.maintenance import load_policy_rates
    for bank, anchors in (("fed", {"target_upper"}), ("ecb", {"dfr", "mro"}), ("boj", {"policy_rate_balance_rate", "ioer"})):
        eff = {m.effective_date for m in load_meetings(bank)}
        miss = [(r.anchor, r.effective_date) for r in load_policy_rates(bank)
                if r.anchor in anchors and r.effective_date >= dt.date(2010, 1, 1) and r.effective_date not in eff]
        assert miss == [], bank
