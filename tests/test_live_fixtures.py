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
    "boj_mpm_schedule": banks.parse_boj_text,
    "boj_mpm_past": banks.parse_boj_text,
    "fed_openmarket": policy_rates.parse_fed_openmarket_text,
    "fred_iorb": policy_rates.parse_fred_csv,
    "fred_ioer": policy_rates.parse_fred_csv,
    "ecb_key_rates": policy_rates.parse_ecb_key_rates_text,
    "boe_bank_rate": policy_rates.parse_boe_bank_rate_text,
    "uk_bank_holidays": holidays.parse_uk_json,
    "jp_cao_holidays": holidays.parse_jp_csv,
    "sifma_holidays": holidays.parse_sifma_text,
}

# parser output rows per fixture (Fed: notation votes / cancelled meetings come back
# as kind "skip")
EXPECTED = {
    "boe_bank_rate_20261008.txt": 258,
    "boe_upcoming_mpc_dates_20261008.txt": 16,
    "boj_mpm_past_20261008.txt": 168,
    "boj_mpm_schedule_20261008.txt": 16,
    "ecb_key_rates_20261008.txt": 50,
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
    "fed_historical_2010_20261008.txt": 8,
    "fed_historical_2011_20261008.txt": 8,
    "fed_historical_2012_20261008.txt": 8,
    "fed_historical_2013_20261008.txt": 8,
    "fed_historical_2014_20261008.txt": 8,
    "fed_historical_2015_20261008.txt": 8,
    "fed_historical_2016_20261008.txt": 8,
    "fed_historical_2017_20261008.txt": 8,
    "fed_historical_2018_20261008.txt": 8,
    "fed_historical_2019_20261008.txt": 8,
    "fed_historical_2020_20261008.txt": 10,
    "fed_openmarket_20261008.txt": 60,
    "fred_ioer_20261008.txt": 22,
    "fred_iorb_20261008.txt": 19,
    "jp_cao_holidays_20261008.txt": 1067,
    "sifma_holidays_20261008.txt": 12,
    "uk_bank_holidays_20261008.txt": 83,
}


def _parse(path: Path):
    name = path.name
    text = path.read_text(encoding="utf-8")
    if name.startswith("fed_historical_"):
        year = name.split("_")[2]
        return banks.parse_fed_text(f"{year} FOMC Meetings\n" + text)   # as fetch_fed does
    if name.startswith("ecb_mp_"):
        return banks.parse_ecb_mp_table(text, year_hint=int(name.split("_")[2]))
    return PARSERS[name.rsplit("_", 1)[0]](text)


def test_every_live_fixture_has_an_expected_count():
    assert sorted(p.name for p in LIVE.iterdir()) == sorted(EXPECTED)


def test_live_fixture_row_counts():
    got = {name: len(_parse(LIVE / name)) for name in EXPECTED}
    assert got == EXPECTED
