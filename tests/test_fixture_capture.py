import datetime as dt
import tempfile
from pathlib import Path

from stircurve.refdata.parsers import banks, common


def test_save_fixtures_writes_parser_input():
    html = "<html><body><h2>Upcoming MPC dates</h2><p>Thursday 5 February 2026</p></body></html>"
    orig = common.fetch
    common.fetch = lambda url, timeout=common.TIMEOUT: html
    try:
        with tempfile.TemporaryDirectory() as tmp:
            with common.saving_fixtures(tmp):
                got = banks.fetch_boe()
            files = list(Path(tmp).iterdir())
            assert [f.name for f in files] == [f"boe_upcoming_mpc_dates_{dt.date.today():%Y%m%d}.txt"]
            text = files[0].read_text()
            assert text == common.html_to_text(html)
            assert [(d, k) for d, k, _ in got] == banks.parse_boe_text(text)
            # outside the context nothing is written
            banks.fetch_boe()
            assert len(list(Path(tmp).iterdir())) == 1
    finally:
        common.fetch = orig
