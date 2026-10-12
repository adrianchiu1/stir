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
    # era rule (D18): same day before 2009 (Fed) / 19 Mar 2024 (BoJ), rolled to a business day
    assert effective_date("fed", dt.date(2006, 8, 8), us) == dt.date(2006, 8, 8)
    assert effective_date("fed", dt.date(2009, 1, 28), us) == dt.date(2009, 1, 29)
    assert effective_date("boj", dt.date(2016, 9, 21), jp) == dt.date(2016, 9, 21)
    assert effective_date("boj", dt.date(2024, 1, 23), jp) == dt.date(2024, 1, 23)
    # ECB rule fallback: Thursday -> following Wednesday
    assert ecb_rule_effective(dt.date(2027, 2, 4), tg) == dt.date(2027, 2, 10)
    # ECB published table overrides the rule (MP 3/2027 starts Thu 6 May)
    look = mp_lookup(load_maintenance_periods())
    assert effective_date("ecb", dt.date(2027, 4, 29), tg, look) == dt.date(2027, 5, 6)
    assert ecb_rule_effective(dt.date(2027, 4, 29), tg) == dt.date(2027, 5, 5)


def test_maintenance_periods_contiguous():
    mps = load_maintenance_periods()
    assert len(mps) == 11 + 10 * 12 + 13 * 8 + 7   # 2004 (from 24 Jan), monthly 2005-14, eight a year 2015-27, 1-7/2028
    assert validate_maintenance_periods(mps) == []
    by = {m.label: m for m in mps}
    assert by["8/2026"].length_days == 49 and by["1/2027"].length_days == 42 and by["1/2010"].length_days == 21


def test_fed_file_and_parcels():
    ms = load_meetings("fed")
    sched = [m for m in ms if m.scheduled]
    from stircurve.refdata.meetings import published_lookup
    us, pub = Calendar.load("us_fed"), published_lookup("fed")
    assert len(sched) == 33 * 8 + 9         # 1994-2027, 2003 lists 15 and 16 Sep; the cancelled 17-18 Mar 2020 meeting is
    sup = [m for m in sched if m.superseded_on]  # kept with superseded_on = 15 Mar 2020 (AC, PR #4)
    assert [(m.decision_date, m.superseded_on) for m in sup] == [(dt.date(2020, 3, 18), dt.date(2020, 3, 15))]
    assert sup[0].in_force_on(dt.date(2020, 3, 13)) and not sup[0].in_force_on(dt.date(2020, 3, 15))
    assert all(m.effective_date == effective_date("fed", m.decision_date, us, pub) for m in ms)
    # target changes took effect on the decision day until 2008, the next business day since 2015
    assert pub[dt.date(2008, 12, 16)] == dt.date(2008, 12, 16) and pub[dt.date(2015, 12, 16)] == dt.date(2015, 12, 17)
    uns = {m.decision_date for m in ms if not m.scheduled}
    assert {dt.date(2008, 1, 22), dt.date(2008, 10, 8), dt.date(2020, 3, 3), dt.date(2020, 3, 15)} <= uns
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
    assert effective_date("boj", dt.date(2016, 1, 29), jp) == dt.date(2016, 1, 29)           # rule (same day pre-2024)
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
    """Fed target / ECB DFR, MRO / BoE Bank Rate / BoJ policy-rate changes since 2010 are implementation
    dates of committed meetings (published or rule)."""
    from stircurve.refdata.maintenance import load_policy_rates
    for bank, anchors in (("fed", {"target_upper"}), ("ecb", {"dfr", "mro"}), ("boe", {"bank_rate"}),
                          ("boj", {"policy_rate_balance_rate", "ioer"})):
        eff = {m.effective_date for m in load_meetings(bank)}
        miss = [(r.anchor, r.effective_date) for r in load_policy_rates(bank)
                if r.anchor in anchors and r.effective_date >= dt.date(2010, 1, 1) and r.effective_date not in eff]
        assert miss == [], bank
