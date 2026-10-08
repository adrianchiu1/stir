import datetime as dt
import tempfile
from pathlib import Path

from stircurve.refdata.parsers import banks, common


def test_save_fixtures_writes_parser_input():
    html = "<html><body><h4>2026 FOMC Meetings</h4><p>January</p><p>27-28</p></body></html>"
    orig = common.fetch
    common.fetch = lambda url, timeout=common.TIMEOUT: html
    try:
        with tempfile.TemporaryDirectory() as tmp:
            with common.saving_fixtures(tmp):
                got = banks.fetch_fed()
            files = list(Path(tmp).iterdir())
            assert [f.name for f in files] == [f"fed_calendar_{dt.date.today():%Y%m%d}.txt"]
            text = files[0].read_text()
            assert text == common.html_to_text(html)
            assert [(d, k) for d, k, _ in got] == banks.parse_fed_text(text) == [(dt.date(2026, 1, 28), "scheduled")]
            # outside the context nothing is written
            banks.fetch_fed()
            assert len(list(Path(tmp).iterdir())) == 1
    finally:
        common.fetch = orig
