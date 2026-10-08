"""Compare rule-based calendars with QuantLib where it is installed.

Differences are printed, not asserted: QuantLib lags new holidays and
encodes some conventions differently (e.g. SIFMA Good Friday early closes),
so the official CSVs, not QuantLib, are the source of truth.
"""
import datetime as dt

from stircurve.refdata.calendars import Calendar


def test_quantlib_crosscheck():
    try:
        import QuantLib as ql
    except ImportError:
        print("QuantLib not installed; skipping cross-check")
        return
    pairs = {
        "us_fed": ql.UnitedStates(ql.UnitedStates.FederalReserve),
        "us_sifma": ql.UnitedStates(ql.UnitedStates.GovernmentBond),
        "target": ql.TARGET(),
        "uk": ql.UnitedKingdom(ql.UnitedKingdom.Settlement),
        "jp": ql.Japan(),
    }
    start, end = dt.date(2015, 1, 1), dt.date(2026, 12, 31)
    for name, qcal in pairs.items():
        ours = Calendar.load(name)
        diffs = []
        d = start
        while d <= end:
            qd = ql.Date(d.day, d.month, d.year)
            if qcal.isBusinessDay(qd) != ours.is_business_day(d):
                diffs.append((d, "ql open" if qcal.isBusinessDay(qd) else "ql closed"))
            d += dt.timedelta(days=1)
        print(f"{name}: {len(diffs)} differences vs QuantLib 2015-2026")
        for x in diffs[:15]:
            print("   ", x)
        assert len(diffs) < 40, f"{name}: too many differences vs QuantLib — check the rules"
