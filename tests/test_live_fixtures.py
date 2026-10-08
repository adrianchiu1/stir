"""Every page captured with ``update_refdata.py --save-fixtures tests/fixtures/live``
goes through its parser and must give the row count observed on the live run
of 8 Oct 2026. A site redesign that breaks a parser fails here, in CI, instead
of as a silent "no changes" dry run. New captures must be added to EXPECTED."""
from pathlib import Path

from stircurve.refdata.parsers import banks, holidays, policy_rates

LIVE = Path(__file__).parent / "fixtures" / "live"

PARSERS = {
    "fed_calendar": banks.parse_fed_text,
    "ecb_reserve_index": banks.ecb_index_links,
    "boe_upcoming_mpc_dates": banks.parse_boe_text,
    "boe_mpc_voting": banks.parse_boe_voting_text,
    "boj_mpm_schedule": banks.parse_boj_text,
    "boj_mpm_past": banks.parse_boj_text,
    "boj_minutes_checked": lambda t: [b for b in t.split("=== ")[1:] if banks.boj_minutes_unscheduled(b)],
    "fed_openmarket": policy_rates.parse_fed_openmarket_text,
    "boj_discount": policy_rates.parse_boj_discount_csv,
    "fred_iorb": policy_rates.parse_fred_csv,
    "fred_ioer": policy_rates.parse_fred_csv,
    "fred_dfedtar": policy_rates.parse_fred_csv,
    "ecb_key_rates": policy_rates.parse_ecb_key_rates_text,
    "boe_bank_rate": policy_rates.parse_boe_bank_rate_text,
    "uk_bank_holidays": holidays.parse_uk_json,
    "jp_cao_holidays": holidays.parse_jp_csv,
    "sifma_holidays": holidays.parse_sifma_text,
    "sifma_us_archive": holidays.parse_sifma_text,
    "nyfed_sofr": lambda t: holidays.sofr_non_publication_days(holidays.parse_sofr_json(t)),
}

# parser output rows per fixture (Fed: notation votes / cancelled meetings come back
# as kind "skip"; boj_minutes_checked: minutes that call the meeting unscheduled; ECB 1999-2003 releases carry no maintenance table, only PDF annexes)
EXPECTED = {
    "boe_bank_rate_20261008.txt": 258,
    "boe_mpc_voting_20261008.txt": 315,
    "boe_upcoming_mpc_dates_20261008.txt": 16,
    "boj_discount_0_20261008.txt": 43,
    "boj_discount_1_20261008.txt": 13,
    "boj_minutes_checked_20261008.txt": 9,
    "boj_minutes_index_1998_20261008.txt": 20,
    "boj_minutes_index_1999_20261008.txt": 18,
    "boj_minutes_index_2000_20261008.txt": 18,
    "boj_minutes_index_2001_20261008.txt": 17,
    "boj_minutes_index_2002_20261008.txt": 16,
    "boj_minutes_index_2003_20261008.txt": 16,
    "boj_minutes_index_2004_20261008.txt": 16,
    "boj_minutes_index_2005_20261008.txt": 15,
    "boj_minutes_index_2006_20261008.txt": 14,
    "boj_minutes_index_2007_20261008.txt": 14,
    "boj_minutes_index_2008_20261008.txt": 18,
    "boj_minutes_index_2009_20261008.txt": 15,
    "boj_minutes_index_2010_20261008.txt": 16,
    "boj_minutes_index_2011_20261008.txt": 15,
    "boj_minutes_index_2012_20261008.txt": 14,
    "boj_minutes_index_2013_20261008.txt": 14,
    "boj_minutes_index_2014_20261008.txt": 14,
    "boj_minutes_index_2015_20261008.txt": 14,
    "boj_minutes_index_2016_20261008.txt": 8,
    "boj_minutes_index_2017_20261008.txt": 8,
    "boj_minutes_index_2018_20261008.txt": 8,
    "boj_minutes_index_2019_20261008.txt": 8,
    "boj_minutes_index_2020_20261008.txt": 9,
    "boj_minutes_index_2021_20261008.txt": 8,
    "boj_minutes_index_2022_20261008.txt": 8,
    "boj_minutes_index_2023_20261008.txt": 8,
    "boj_minutes_index_2024_20261008.txt": 8,
    "boj_minutes_index_2025_20261008.txt": 8,
    "boj_minutes_index_2026_20261008.txt": 5,
    "boj_mpm_past_20261008.txt": 168,
    "boj_mpm_schedule_20261008.txt": 16,
    "boj_statement_20250919_20261008.txt": 1,
    "boj_statement_20251030_20261008.txt": 1,
    "boj_statement_20251219_20261008.txt": 4,
    "boj_statement_20260123_20261008.txt": 1,
    "boj_statement_20260319_20261008.txt": 1,
    "boj_statement_20260428_20261008.txt": 1,
    "boj_statement_20260616_20261008.txt": 4,
    "boj_statement_20260731_20261008.txt": 1,
    "boj_statement_20260918_20261008.txt": 4,
    "ecb_key_rates_20261008.txt": 50,
    "ecb_mp_1999_20261008.txt": 0,
    "ecb_mp_2000_20261008.txt": 0,
    "ecb_mp_2001_20261008.txt": 0,
    "ecb_mp_2002_20261008.txt": 0,
    "ecb_mp_2003_20261008.txt": 0,
    "ecb_mp_2004_20261008.txt": 11,
    "ecb_mp_2005_20261008.txt": 12,
    "ecb_mp_2006_20261008.txt": 12,
    "ecb_mp_2007_20261008.txt": 12,
    "ecb_mp_2008_20261008.txt": 12,
    "ecb_mp_2009_20261008.txt": 12,
    "ecb_mp_2010_20261008.txt": 24,
    "ecb_mp_2011_20261008.txt": 24,
    "ecb_mp_2012_20261008.txt": 24,
    "ecb_mp_2013_20261008.txt": 24,
    "ecb_mp_2014_20261008.txt": 24,
    "ecb_mp_2015_20261008.txt": 8,
    "ecb_mp_2016_20261008.txt": 8,
    "ecb_mp_2017_20261008.txt": 16,
    "ecb_mp_2018_20261008.txt": 16,
    "ecb_mp_2019_20261008.txt": 8,
    "ecb_mp_2020_20261008.txt": 8,
    "ecb_mp_2021_20261008.txt": 8,
    "ecb_mp_2022_20261008.txt": 9,
    "ecb_mp_2023_20261008.txt": 10,
    "ecb_mp_2024_20261008.txt": 9,
    "ecb_mp_2025_20261008.txt": 9,
    "ecb_mp_2026_20261008.txt": 9,
    "ecb_mp_2027_20261008.txt": 9,
    "ecb_mp_2028_20261008.txt": 9,
    "ecb_reserve_index_20261008.txt": 30,
    "fed_calendar_20261008.txt": 57,
    "fed_historical_1994_20261008.txt": 13,
    "fed_historical_1995_20261008.txt": 11,
    "fed_historical_1996_20261008.txt": 8,
    "fed_historical_1997_20261008.txt": 8,
    "fed_historical_1998_20261008.txt": 10,
    "fed_historical_1999_20261008.txt": 8,
    "fed_historical_2000_20261008.txt": 8,
    "fed_historical_2001_20261008.txt": 13,
    "fed_historical_2002_20261008.txt": 8,
    "fed_historical_2003_20261008.txt": 13,
    "fed_historical_2004_20261008.txt": 8,
    "fed_historical_2005_20261008.txt": 8,
    "fed_historical_2006_20261008.txt": 8,
    "fed_historical_2007_20261008.txt": 11,
    "fed_historical_2008_20261008.txt": 14,
    "fed_historical_2009_20261008.txt": 11,
    "fed_historical_2010_20261008.txt": 10,
    "fed_historical_2011_20261008.txt": 10,
    "fed_historical_2012_20261008.txt": 8,
    "fed_historical_2013_20261008.txt": 9,
    "fed_historical_2014_20261008.txt": 9,
    "fed_historical_2015_20261008.txt": 8,
    "fed_historical_2016_20261008.txt": 8,
    "fed_historical_2017_20261008.txt": 8,
    "fed_historical_2018_20261008.txt": 8,
    "fed_historical_2019_20261008.txt": 9,
    "fed_historical_2020_20261008.txt": 14,
    "fed_openmarket_20261008.txt": 60,
    "fred_dfedtar_20261008.txt": 153,
    "fred_ioer_20261008.txt": 22,
    "fred_iorb_20261008.txt": 19,
    "jp_cao_holidays_20261008.txt": 1067,
    "nyfed_sofr_20261008.txt": 95,
    "sifma_holidays_20261008.txt": 12,
    "sifma_us_archive_20261008.txt": 118,
    "uk_bank_holidays_20261008.txt": 83,
}


def _parse(path: Path):
    name = path.name
    text = path.read_text(encoding="utf-8")
    if name.startswith("fed_historical_"):
        year = name.split("_")[2]
        return banks.parse_fed_text(f"{year} FOMC Meetings\n" + text)   # as fetch_fed does
    if name.startswith("boj_minutes_index_"):
        return banks.parse_boj_minutes_index(text, int(name.split("_")[3]))
    if name.startswith("boj_statement_"):     # one row per rate the statement sets
        return [v for k, v in policy_rates.parse_boj_statement(text).items() if v is not None]
    if name.startswith("boj_discount_"):
        return policy_rates.parse_boj_discount_csv(text)
    if name.startswith("ecb_mp_"):
        return banks.parse_ecb_mp_table(text, year_hint=int(name.split("_")[2]))
    return PARSERS[name.rsplit("_", 1)[0]](text)


def test_every_live_fixture_has_an_expected_count():
    assert sorted(p.name for p in LIVE.iterdir()) == sorted(EXPECTED)


def test_live_fixture_row_counts():
    got = {name: len(_parse(LIVE / name)) for name in EXPECTED}
    assert got == EXPECTED
