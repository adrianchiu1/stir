"""WIRP captures (AC's screenshots of 7 Oct 2026, transcribed) and the three-layer comparison."""
import datetime as dt

import numpy as np
import pandas as pd

from stircurve.quality import wirp

D = dt.date(2026, 10, 7)


def test_parse_both_captures_of_7_oct_2026():
    fut = wirp.load_capture(D, "futures")
    ois = wirp.load_capture(D, "ois")
    assert fut.model == "futures" and ois.model == "ois"
    assert fut.pricing_date == ois.pricing_date == D
    assert fut.current_implied == 3.879 and ois.current_implied == 3.878
    assert fut.meta["target_rate"] == "4.00" and fut.meta["effective_rate"] == "3.88"
    assert len(fut.rows) == 11 and len(ois.rows) == 8
    assert fut.rows["meeting"].iloc[0] == dt.date(2026, 10, 28) and fut.rows["implied_rate"].iloc[0] == 3.928
    assert fut.rows["meeting"].iloc[-1] == dt.date(2028, 1, 26) and fut.rows["n_moves"].iloc[-1] == 3.154
    assert ois.rows["implied_rate"].tolist() == [3.927, 4.128, 4.222, 4.387, 4.475, 4.570, 4.616, 4.646]
    assert (fut.rows["arm"] == 0.25).all()


def test_parser_refuses_text_it_does_not_know_and_checks_the_identities():
    try:
        wirp.parse_wirp("Meeting Implied\n10/28/2026 3.9\n")
    except wirp.WirpFormatError:
        pass
    else:
        raise AssertionError("no rows, no instrument: must refuse")
    bad = ("Instrument: Fed Funds Futures\nPricing Date 10/07/2026\nCur. Imp. O/N Rate 3.879\n"
           "10/28/2026 +0.194 +19.4% +0.048 3.999 0.250\n")
    try:
        wirp.parse_wirp(bad, "bad")
    except wirp.WirpFormatError as exc:
        assert "Imp. Rate" in str(exc)
    else:
        raise AssertionError("inconsistent delta must be refused")


def test_compare_matches_meetings_and_flags_reasons():
    cap = wirp.load_capture(D, "futures")
    rows = []
    for w in cap.rows.itertuples():
        rows.append({"decision_date": w.meeting, "implied_rate": w.implied_rate + 0.0005, "replica_rate": w.implied_rate,
                     "synthetic": w.meeting.year == 2028, "unscheduled": False, "beyond_wirp_reach": False,
                     "under_identified": False})
    rows[-1]["replica_rate"] = np.nan
    rows[-1]["beyond_wirp_reach"] = True
    mt = pd.DataFrame(rows)
    cmp_ = wirp.compare(mt, cap, 3.8795, 3.879)
    assert cmp_.iloc[0]["meeting"] == "current" and cmp_.iloc[0]["replica_ok"] and cmp_.iloc[0]["fit_ok"]
    body = cmp_[cmp_["meeting"] != "current"]
    assert len(body) == 11 and body["fit_ok"].all() and (body["fit_minus_wirp_bp"] == 0.05).all()
    last = body.iloc[-1]
    assert not last["replica_ok"] and "synthetic" in last["reason"] and "reach" in last["reason"]
