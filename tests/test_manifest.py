import copy
import datetime as dt

from stircurve.config.loader import load_config
from stircurve.marketdata import sources
from stircurve.marketdata.manifest import load_manifest, validate_manifest


def test_manifest_complete_against_usd_yaml():
    m = load_manifest("usd")
    assert validate_manifest(m) == []
    cfg = load_config("usd")
    family_instruments = {i for f in cfg["families"].values() for i in f["instruments"]}
    assert family_instruments == set(m.instruments) == {
        "ff_fut", "sofr1m_fut", "sofr3m_fut", "ed_fut", "ois_effr", "ois_sofr", "swap_libor3m"}
    assert {f["index"] for f in cfg["families"].values()} <= set(m.fixings) == {"EFFR", "SOFR", "USDLIBOR3M"}
    # policy anchors cross-check the M0 policy-rate file's anchors
    anchors = {line.split(",")[1] for line in open("data/refdata/policy_rates/fed.csv").read().splitlines()[1:]}
    assert {a["refdata_anchor"] for a in m.anchors.values()} <= anchors


def test_manifest_validation_catches_gaps():
    m = load_manifest("usd")
    m.raw = copy.deepcopy(m.raw)
    del m.raw["instruments"]["ed_fut"]
    m.raw["instruments"]["ois_sofr"]["spot_lag"]["calendar"] = "us_nyse"
    m.raw["instruments"]["ff_fut"]["last_trade"]["source"] = "a_blog"
    m.raw["instruments"]["ff_fut"]["quote"]["mid"] = False
    problems = "\n".join(validate_manifest(m))
    assert "instrument ed_fut missing" in problems
    assert "unknown calendar 'us_nyse'" in problems
    assert "unknown source 'a_blog'" in problems
    assert "mids (D10)" in problems


def test_quoted_rules_appear_in_live_captures():
    m = load_manifest("usd")
    assert sources.check_quotes(m) == []
    # sources still to be captured by hand (cmegroup.com) or confirmed on the terminal
    assert set(sources.pending(m)) == {"bbg_des", "cme_sr1_specs", "cme_sr3_specs", "cme_ed_fallback"}


def test_tickers_and_columns():
    m = load_manifest("usd")
    assert m.future_ticker("sofr3m_fut", 2024, 3) == "SFRH24 Comdty"
    assert m.future_ticker("ff_fut", 2026, 10, two_digit=False) == "FFV6 Comdty"
    assert m.parse_future_ticker("EDZ19 Comdty") == ("ed_fut", 2019, 12)
    assert m.parse_future_ticker("SERF26 Comdty") == ("sofr1m_fut", 2026, 1)
    assert m.parse_future_ticker("FFV6 Comdty") is None        # columns carry two-digit years only
    assert m.swap_ticker("ois_sofr", "18M") == "USOSFR1F Curncy"
    assert m.swap_ticker("ois_effr", "3M") == "USSOC Curncy"
    # live contracts are requested with one-digit years, expired ones with two
    asof = dt.date(2026, 10, 7)
    assert m.request_ticker("sofr3m_fut", 2026, 12, dt.date(2027, 3, 16), asof) == "SFRZ6 Comdty"
    assert m.request_ticker("sofr3m_fut", 2019, 12, dt.date(2020, 3, 17), asof) == "SFRZ19 Comdty"


def test_series_plan_respects_first_and_last_dates():
    m = load_manifest("usd")
    plan = m.series(dt.date(2019, 6, 12), dt.date(2019, 6, 12))
    names = {s.instrument for s in plan}
    assert {"ed_fut", "swap_libor3m", "USDLIBOR3M", "sofr3m_fut", "ff_fut", "SOFR"} <= names
    plan = m.series(dt.date(2026, 10, 7), dt.date(2026, 10, 7))
    names = {s.instrument for s in plan}
    assert not names & {"ed_fut", "swap_libor3m", "USDLIBOR3M"}
    assert len({s.ticker for s in plan}) == len(plan)
