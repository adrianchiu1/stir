import datetime as dt
from pathlib import Path
from stircurve.refdata.maintenance import load_policy_rates, rate_in_effect
from stircurve.refdata.parsers.policy_rates import (parse_fed_openmarket_text, parse_ecb_key_rates_text,
                                                    parse_boe_bank_rate_text, parse_fred_csv)

FIX = Path(__file__).parent / "fixtures"


def test_fed_openmarket_table():
    rows = parse_fed_openmarket_text((FIX / "fed_openmarket.txt").read_text())
    by = {r["effective_date"]: r for r in rows}
    assert by[dt.date(2026, 9, 17)] == {"effective_date": dt.date(2026, 9, 17), "lower": 3.75, "upper": 4.00}
    assert by[dt.date(2020, 3, 4)]["upper"] == 1.25             # footnoted date still parsed
    assert by[dt.date(2008, 10, 29)]["lower"] == by[dt.date(2008, 10, 29)]["upper"] == 1.00


def test_ecb_key_rates_both_column_orders():
    ecb = {r["effective_date"]: r for r in parse_ecb_key_rates_text((FIX / "ecb_key_rates.txt").read_text())}
    assert ecb[dt.date(2026, 6, 17)]["dfr"] == 2.25 and ecb[dt.date(2026, 6, 17)]["mro"] == 2.40
    assert ecb[dt.date(2019, 9, 18)]["dfr"] == -0.50
    bdf = {r["effective_date"]: r for r in parse_ecb_key_rates_text((FIX / "ecb_key_rates_bdf.txt").read_text())}
    assert bdf[dt.date(2025, 6, 11)]["dfr"] == 2.00 and bdf[dt.date(2025, 6, 11)]["mro"] == 2.15
    assert bdf[dt.date(2024, 12, 18)]["mlf"] == 3.40


def test_boe_bank_rate_table():
    rows = dict(parse_boe_bank_rate_text((FIX / "boe_bank_rate.txt").read_text()))
    assert rows[dt.date(2025, 12, 18)] == 3.75 and rows[dt.date(2009, 3, 5)] == 0.50


def test_fred_csv_changes_only():
    csv = "DATE,IORB\n2025-12-10,3.90\n2025-12-11,3.65\n2025-12-12,3.65\n2025-12-15,.\n2026-09-17,3.90\n"
    assert parse_fred_csv(csv) == [(dt.date(2025, 12, 10), 3.90), (dt.date(2025, 12, 11), 3.65), (dt.date(2026, 9, 17), 3.90)]


def test_rate_in_effect_all_banks():
    fed = load_policy_rates("fed")
    assert rate_in_effect(fed, "target_midpoint", dt.date(2025, 12, 10)) == 3.875   # decision day: old range
    assert rate_in_effect(fed, "target_midpoint", dt.date(2025, 12, 11)) == 3.625
    assert rate_in_effect(fed, "target_upper", dt.date(2026, 10, 8)) == 4.00
    assert rate_in_effect(fed, "iorb", dt.date(2026, 10, 8)) == 3.90
    assert rate_in_effect(fed, "target_midpoint", dt.date(2010, 6, 1)) == 0.125
    ecb = load_policy_rates("ecb")
    assert rate_in_effect(ecb, "dfr", dt.date(2027, 1, 1)) == 2.50          # 16 Sep 2026 change (live key-rates page)
    assert rate_in_effect(ecb, "dfr", dt.date(2026, 9, 15)) == 2.25
    assert rate_in_effect(ecb, "dfr", dt.date(2025, 6, 10)) == 2.25 and rate_in_effect(ecb, "dfr", dt.date(2025, 6, 11)) == 2.00
    assert rate_in_effect(ecb, "dfr", dt.date(2015, 1, 1)) == -0.20
    boe = load_policy_rates("boe")
    assert rate_in_effect(boe, "bank_rate", dt.date(2025, 12, 18)) == 3.75 and rate_in_effect(boe, "bank_rate", dt.date(2025, 12, 17)) == 4.00
    boj = load_policy_rates("boj")
    assert rate_in_effect(boj, "ioer", dt.date(2026, 6, 16)) == 0.75 and rate_in_effect(boj, "ioer", dt.date(2026, 6, 17)) == 1.00
    assert rate_in_effect(boj, "policy_rate_balance_rate", dt.date(2020, 1, 1)) == -0.10
    assert all(r.confidence for r in fed + ecb + boe + boj)


LIVE = Path(__file__).parent / "fixtures" / "live"


def test_policy_rate_live_pages():
    fed = parse_fed_openmarket_text((LIVE / "fed_openmarket_20261008.txt").read_text())
    assert len(fed) == 60
    assert {"effective_date": dt.date(2020, 3, 4), "lower": 1.0, "upper": 1.25} in fed      # corrected from 3 Mar (footnote)
    assert {"effective_date": dt.date(2008, 12, 16), "lower": 0.0, "upper": 0.25} in fed    # "0-0.25"
    ecb = parse_ecb_key_rates_text((LIVE / "ecb_key_rates_20261008.txt").read_text())
    assert len(ecb) == 50 and ecb[0]["effective_date"] == dt.date(2005, 12, 6)
    by = {r["effective_date"]: r for r in ecb}
    assert by[dt.date(2019, 9, 18)] == {"effective_date": dt.date(2019, 9, 18), "dfr": -0.5, "mro": 0.0, "mlf": 0.25}  # U+2212
    assert by[dt.date(2024, 9, 18)]["mro"] == 3.65                                    # "18 Sep.5" footnote
    assert "mro" not in by[dt.date(2008, 10, 8)] and by[dt.date(2008, 10, 15)]["mro"] == 3.75
    assert by[dt.date(2007, 6, 13)]["mro"] == 4.0                                     # minimum bid rate era
    boe = parse_boe_bank_rate_text((LIVE / "boe_bank_rate_20261008.txt").read_text())
    assert len(boe) == 258 and boe[-1] == (dt.date(2025, 12, 18), 3.75) and (dt.date(2020, 3, 19), 0.1) in boe
    assert len(parse_fred_csv((LIVE / "fred_iorb_20261008.txt").read_text())) == 19
    assert len(parse_fred_csv((LIVE / "fred_ioer_20261008.txt").read_text())) == 22


def test_boj_statements_and_history():
    import math
    from stircurve.refdata.parsers.policy_rates import parse_boj_statement, parse_boj_discount_csv
    p = parse_boj_statement((LIVE / "boj_statement_20260918_20261008.txt").read_text())
    assert p == {"call_rate_target": (1.25, 1.25), "cdf_rate": 1.25, "basic_loan_rate": 1.5,
                 "effective": dt.date(2026, 9, 24)}
    blr = parse_boj_discount_csv((LIVE / "boj_discount_1_20261008.txt").read_text())
    assert blr[0] == (dt.date(2001, 1, 4), 0.5) and (dt.date(2006, 7, 14), 0.4) in blr
    boj = load_policy_rates("boj")
    assert math.isnan(rate_in_effect(boj, "call_target_midpoint", dt.date(2015, 6, 1)))     # QQE: no call-rate target
    assert rate_in_effect(boj, "call_target_midpoint", dt.date(2010, 10, 5)) == 0.05         # "effective immediately"
    assert rate_in_effect(boj, "policy_rate_balance_rate", dt.date(2016, 2, 16)) == -0.1
    assert math.isnan(rate_in_effect(boj, "policy_rate_balance_rate", dt.date(2024, 3, 21)))
    assert rate_in_effect(boj, "ioer", dt.date(2026, 9, 24)) == 1.25
    assert all(r.source_url.startswith("https://www.boj.or.jp/") for r in boj)
    assert not [r for r in boj if r.confidence.startswith("memory")]


def test_boj_statement_ignores_defeated_proposal():
    from stircurve.refdata.parsers.policy_rates import parse_boj_statement
    p = parse_boj_statement((LIVE / "boj_statement_20260123_20261008.txt").read_text())
    assert p["call_rate_target"] == (0.75, 0.75)          # a member's proposal of 1.0 percent was defeated
