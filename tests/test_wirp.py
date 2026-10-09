"""WIRP parser and comparison (M2 gate).

The parser is pinned to AC's captures (tests/fixtures/live/wirp_usd_<YYYYMMDD>.txt)
as they land; until then only the refusal of unknown text and the comparison
logic (on a table built in code, not a fixture) are tested.
"""
import datetime as dt

import pandas as pd

from stircurve.quality import wirp

D = dt.date


def test_wirp_captures_parse():
    files = sorted(wirp.FIXTURE_DIR.glob("wirp_usd_*.txt"))
    for p in files:
        t = wirp.parse_wirp(p.read_text(encoding="utf-8"))
        asof = dt.datetime.strptime(p.stem.rsplit("_", 1)[1], "%Y%m%d").date()
        assert len(t.rows) >= 4, p.name
        assert t.rows["meeting"].is_monotonic_increasing and (t.rows["meeting"] >= asof).all(), p.name
        assert t.rows["implied_rate"].between(-1, 25).all(), p.name
    if not files:
        print("  (no WIRP captures yet: tests/fixtures/live/wirp_usd_<YYYYMMDD>.txt)")


def test_parser_refuses_text_it_does_not_know():
    for text in ("", "Meeting  Rate\n09/18/2024  5.12", "nothing here"):
        try:
            wirp.parse_wirp(text)
            raise AssertionError(f"parsed {text!r}")
        except wirp.WirpFormatError:
            pass


def test_compare_matches_meetings_and_explains_misses():
    ours = pd.DataFrame({
        "decision_date": [D(2020, 1, 29), D(2020, 4, 29), D(2020, 6, 10)],
        "implied_rate": [1.53, 1.40, 1.30], "synthetic": [False, False, True], "scheduled": [True, True, True],
        "under_identified": [False, False, False]})
    table = wirp.WirpTable(D(2019, 12, 2), pd.DataFrame({
        "meeting": [D(2020, 1, 29), D(2020, 3, 18), D(2020, 4, 29), D(2020, 6, 10)],
        "implied_rate": [1.525, 1.45, 1.42, 1.30]}))
    c = wirp.compare(ours, table).set_index("meeting")
    assert c.loc[D(2020, 1, 29), "ok"] and abs(c.loc[D(2020, 1, 29), "diff_bp"] - 0.5) < 1e-9
    assert not c.loc[D(2020, 3, 18), "ok"] and "cancelled or replaced" in c.loc[D(2020, 3, 18), "reason"]
    assert not c.loc[D(2020, 4, 29), "ok"] and abs(c.loc[D(2020, 4, 29), "diff_bp"] + 2.0) < 1e-9
    assert c.loc[D(2020, 6, 10), "ok"] and c.loc[D(2020, 6, 10), "reason"] == "synthetic meeting"
