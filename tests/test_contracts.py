"""Contract-table generator: rules applied to the committed calendars, and the
listing model checked against what the exchange's filings say was listed."""
import datetime as dt

from stircurve.marketdata.contracts import contract_table, listed_contracts
from stircurve.marketdata.manifest import load_manifest
from stircurve.refdata.calendars import third_wednesday

M = load_manifest("usd")
D = dt.date


def _table(ins, a, b):
    return contract_table(M, D(a, 1, 1), D(b, 12, 31), [ins])


def _listed_on(ins, day):
    return {c.contract for c in listed_contracts(M, ins, day) if c.first_listed <= day <= c.last_trade}


def test_ff_windows_2010_2027():
    t = _table("ff_fut", 2010, 2027)
    fed = M.calendar("us_fed")
    assert t.contract.str[:4].astype(int).between(2010, 2032).all()
    for r in t.itertuples():
        assert r.ref_start.day == 1 and r.ref_end.day == 1 and r.ref_end.month % 12 == (r.ref_start.month + 1) % 12
        assert r.last_trade.month == r.ref_start.month and fed.is_business_day(r.last_trade)
        assert not any(fed.is_business_day(r.last_trade + dt.timedelta(days=k))
                       for k in range(1, (r.ref_end - r.last_trade).days))
        assert fed.is_business_day(r.final_settlement) and r.final_settlement >= r.ref_end_inclusive
    by = t.set_index("contract")
    # Good Friday month-ends are us_fed business days (AC, PR #2)
    assert by.loc["2024-03", "last_trade"] == D(2024, 3, 29)
    assert by.loc["2018-03", "last_trade"] == D(2018, 3, 30)
    assert by.loc["2024-03", "final_settlement"] == D(2024, 4, 1)
    assert by.loc["2026-10", "last_trade"] == D(2026, 10, 30)


def test_ff_listing_36_then_60_months():
    # CBOT 20-321: 36 consecutive months, 60 from trade date 21 Sep 2020
    assert len(_listed_on("ff_fut", D(2020, 9, 18))) == 36
    assert len(_listed_on("ff_fut", D(2020, 9, 21))) == 60
    assert len(_listed_on("ff_fut", D(2026, 10, 7))) == 60


def test_sr3_windows_2018_2027():
    t = _table("sofr3m_fut", 2018, 2027)
    fed = M.calendar("us_fed")
    for r in t.itertuples():
        y, mo = map(int, r.contract.split("-"))
        assert r.ref_start == third_wednesday(y, mo)       # named for the month its Reference Quarter starts (19-366)
        end_m = (mo + 2) % 12 + 1
        assert r.ref_end == third_wednesday(y + (mo + 3 > 12), end_m)
        assert r.accrual_days in (84, 91, 98)               # 12-14 weeks (24-204)
        assert r.last_trade == fed.previous_business_day(r.ref_end)
    by = t.set_index("contract")
    assert (by.loc["2024-03", "ref_start"], by.loc["2024-03", "ref_end"]) == (D(2024, 3, 20), D(2024, 6, 19))
    assert by.loc["2024-03", "last_trade"] == D(2024, 6, 18)
    assert by.loc["2024-03", "final_settlement"] == D(2024, 6, 20)   # 19 Jun 2024 (Juneteenth) is not a SOFR day
    assert by.loc["2018-06", "first_listed"] == D(2018, 5, 7)
    assert not by.loc["2018-06", "first_listed_lower_bound"]
    # no serial SR3 before the July 2022 listing change
    assert (t[t.cycle == "serial"].first_listed >= D(2022, 7, 25)).all()


def test_sr3_listed_set_25_jul_2022_matches_cme_22_199():
    # "quarterly contract months June 2022 through June 2032 plus the nearest serial
    #  months August 2022 through January 2023" (tests/fixtures/live/cftc_22-199_*.txt)
    text = open(sorted(__import__("glob").glob("tests/fixtures/live/cftc_22-199_*.txt"))[-1]).read()
    assert "June 2022 through June 2032" in " ".join(text.split())
    listed = _listed_on("sofr3m_fut", D(2022, 7, 25))
    quarterly = {f"{y}-{m:02d}" for y in range(2022, 2033) for m in (3, 6, 9, 12)
                 if D(2022, 6, 1) <= D(y, m, 1) <= D(2032, 6, 1)}
    assert len(quarterly) == 41
    assert listed == quarterly | {"2022-08", "2022-10", "2022-11", "2023-01"}
    before = _listed_on("sofr3m_fut", D(2022, 7, 22))     # "June 2022 through December 2031"
    assert before == {c for c in quarterly if c <= "2031-12"}


def test_sr1_windows_2018_2027():
    t = _table("sofr1m_fut", 2018, 2027)
    fed = M.calendar("us_fed")
    for r in t.itertuples():
        assert r.ref_start.day == 1 and r.ref_end.day == 1
        assert r.last_trade == fed.previous_business_day(r.ref_end)
    assert t.first_listed.min() == D(2018, 5, 7)
    assert len(_listed_on("sofr1m_fut", D(2018, 5, 7))) == 7


def test_ed_windows_2010_2023():
    t = _table("ed_fut", 2010, 2023)
    uk = M.calendar("uk")
    for r in t.itertuples():
        y, mo = map(int, r.contract.split("-"))
        imm = third_wednesday(y, mo)
        assert r.ref_start == imm and r.final_settlement == r.last_trade
        assert r.last_trade == uk.advance_business_days(imm, -2)    # 2nd London business day before (Ch. 452)
        assert 89 <= r.accrual_days <= 93
    by = t.set_index("contract")
    assert by.loc["2019-06", "last_trade"] == D(2019, 6, 17)
    assert by.loc["2023-06", "last_trade"] == D(2023, 6, 19) and by.loc["2023-06", "last_quote"] == D(2023, 6, 16)
    # contracts expiring after 30 Jun 2023 were converted to SR3 on 14 Apr 2023
    late = t[t.last_trade > D(2023, 6, 30)]
    assert len(late) and (late.last_quote == D(2023, 4, 14)).all() and (late.converted_on == D(2023, 4, 14)).all()
    assert t.last_quote.max() == D(2023, 6, 16)   # last ED price (AC)


def test_contract_table_is_deterministic_and_unique():
    a = contract_table(M, D(2019, 6, 12), D(2019, 6, 12))
    b = contract_table(M, D(2019, 6, 12), D(2019, 6, 12))
    assert a.equals(b)
    assert not a.duplicated(["instrument", "contract"]).any()
    assert (a.first_quote <= D(2019, 6, 12)).all() and (a.last_quote >= D(2019, 6, 12)).all()


def test_listing_model_matches_bloomberg_dumps():
    # contracts with a PX_LAST in AC's dumps (data/market/usd): FF 36 then 60 months, SR1 7 then 13,
    # SR3 20 quarterly then 39 quarterly + 6 serial (incl. two in their Reference Quarter), ED 40 + 4
    def counts(ins, day):
        listed = _listed_on(ins, day)
        q = sum(int(c[5:]) % 3 == 0 for c in listed)
        return q, len(listed) - q
    assert len(_listed_on("ff_fut", D(2019, 6, 12))) == 36 and len(_listed_on("ff_fut", D(2026, 10, 7))) == 60
    assert len(_listed_on("sofr1m_fut", D(2019, 6, 12))) == 7 and len(_listed_on("sofr1m_fut", D(2026, 10, 7))) == 13
    assert counts("sofr3m_fut", D(2019, 6, 12)) == (20, 0)
    assert counts("sofr3m_fut", D(2026, 10, 7)) == (39, 6)
    assert {"2026-07", "2026-08", "2027-01", "2027-02"} <= _listed_on("sofr3m_fut", D(2026, 10, 7))
    assert not {"2027-04", "2027-05"} & _listed_on("sofr3m_fut", D(2026, 10, 7))
    assert counts("ed_fut", D(2019, 6, 12)) == (40, 4)
