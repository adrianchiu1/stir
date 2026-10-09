"""dump_bloomberg.py against a fake pxts.read_bdh, and the loader on its output.

The fake mimics pxts.read_bdh: a dict {output column: Bloomberg ticker}, one
field per call, a DatetimeIndex frame back, and a KeyError when Bloomberg has
no data for one of the tickers (pxts does ``raw.loc[:, tickers]``). Values are
synthetic test values, not Bloomberg data.
"""
import datetime as dt
import socket
import tempfile
import zlib
from pathlib import Path

import numpy as np
import pandas as pd

from scripts import check_market_data, dump_bloomberg
from stircurve.marketdata import dump as dumper
from stircurve.marketdata.contracts import listed_contracts
from stircurve.marketdata import loader
from stircurve.marketdata.manifest import load_manifest

M = load_manifest("usd")
D = dt.date


WINDOWS = {c.bbg_ticker: (pd.Timestamp(c.first_listed), pd.Timestamp(c.last_trade))
           for ins in M.futures() for c in listed_contracts(M, ins, D(2027, 12, 31))}


class FakeBloomberg:
    """Futures have values only while listed, like Bloomberg."""

    def __init__(self, dead=(), bump=None):
        self.dead, self.bump, self.calls = set(dead), bump or {}, []

    def value(self, column, ticker, field, day):
        first, last = WINDOWS.get(column.split("|")[0], (pd.Timestamp.min, pd.Timestamp.max))
        if not first <= day <= last:
            return np.nan
        h = zlib.crc32(ticker.encode()) % 1000 / 1000
        if field in ("OPEN_INT", "PX_VOLUME"):
            return float(1000 + int(h * 1000))
        base = 96.0 + h if ticker.endswith("Comdty") else 3.0 + h
        return round(base + self.bump.get(ticker, 0.0), 4)

    def read_bdh(self, tickers, start="2000-01-01", field="PX_LAST", end=None, timeout=5):
        self.calls.append((dict(tickers), start, end, field))
        days = pd.bdate_range(start, end)
        for name, t in tickers.items():
            # pxts raises when Bloomberg has nothing for a ticker in the range (dead, or a
            # contract the generous dump horizon asks for before it was listed)
            if t in self.dead or all(np.isnan(self.value(name, t, field, d)) for d in days):
                raise KeyError(t)
        return pd.DataFrame({name: [self.value(name, t, field, d) for d in days] for name, t in tickers.items()},
                            index=pd.DatetimeIndex(days))


def _dump(root, start, end, fake, write_csv=True, as_of=D(2026, 10, 8)):
    return dumper.dump(M, start, end, fake.read_bdh, write_csv=write_csv, as_of=as_of, root=root)


def test_dump_writes_wide_csvs_and_is_idempotent():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        fake = FakeBloomberg()
        dry = _dump(root, D(2026, 10, 7), D(2026, 10, 7), fake, write_csv=False)
        assert not dry.blocking and not dry.written and not any(root.rglob("*.csv"))
        res = _dump(root, D(2026, 10, 7), D(2026, 10, 7), fake)
        files = sorted(p.relative_to(root).as_posix() for p in root.rglob("*.csv"))
        assert files == sorted(f"usd/2026/{g}.csv" for g in
                               ("ff_fut", "sofr1m_fut", "sofr3m_fut", "ois_effr", "ois_sofr", "fixings", "policy_anchors"))
        sr3 = (root / "usd/2026/sofr3m_fut.csv").read_text().splitlines()
        assert sr3[0].startswith("date,") and "SFRZ26 Comdty|PX_LAST" in sr3[0].split(",")
        assert sr3[1].startswith("2026-10-07,") and len(sr3) == 2
        # live contracts requested with one-digit years, columns keep two
        reqs = {t for c in fake.calls for t in c[0].values()}
        assert "SFRZ6 Comdty" in reqs and "SFRZ26 Comdty" not in reqs
        # same run again: nothing changes, nothing rewritten
        before = {p: p.read_bytes() for p in root.rglob("*.csv")}
        again = _dump(root, D(2026, 10, 7), D(2026, 10, 7), fake)
        assert all(d.empty for d in again.diffs) and not again.written
        assert before == {p: p.read_bytes() for p in root.rglob("*.csv")}
        # extending the range adds rows without touching existing ones
        more = _dump(root, D(2026, 10, 5), D(2026, 10, 7), fake)
        assert not more.blocking and all(d.added_rows == 2 for d in more.diffs)
        assert len((root / "usd/2026/sofr3m_fut.csv").read_text().splitlines()) == 4


def test_dump_refuses_to_change_values_on_file():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _dump(root, D(2026, 10, 7), D(2026, 10, 7), FakeBloomberg())
        f = root / "usd/2026/fixings.csv"
        before = f.read_bytes()
        rc = dump_bloomberg.main(["--start", "2026-10-07", "--end", "2026-10-07", "--root", str(root),
                                  "--as-of", "2026-10-08", "--write-csv"],
                                 read_bdh=FakeBloomberg(bump={"SOFRRATE Index": 0.01}).read_bdh)
        assert rc == 2 and f.read_bytes() == before
        res = _dump(root, D(2026, 10, 7), D(2026, 10, 7), FakeBloomberg(dead={"SOFRRATE Index"}))
        assert res.blocking and any("SOFRRATE Index|PX_LAST" in x for d in res.diffs for x in d.removed)
        assert f.read_bytes() == before


def test_dead_ticker_does_not_lose_the_chunk():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        res = _dump(root, D(2026, 10, 7), D(2026, 10, 7), FakeBloomberg(dead={"USOSFR12 Curncy"}))
        assert any(x.startswith("USOSFR12 Curncy|PX_LAST") for x in res.failed)
        df = dumper.read_wide(root / "usd/2026/ois_sofr.csv")
        assert df["USOSFR12 Curncy|PX_LAST"].isna().all() and df["USOSFR10 Curncy|PX_LAST"].notna().all()
        assert "NaN" in (root / "usd/2026/ois_sofr.csv").read_text()


def test_libor_era_day_uses_two_digit_expired_tickers():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        fake = FakeBloomberg()
        _dump(root, D(2019, 6, 12), D(2019, 6, 12), fake)
        groups = {p.stem for p in (root / "usd/2019").glob("*.csv")}
        assert {"ed_fut", "swap_libor3m", "sofr3m_fut", "sofr1m_fut", "ff_fut", "fixings"} <= groups
        reqs = {t for c in fake.calls for t in c[0].values()}
        assert {"EDZ19 Comdty", "US0003M Index", "USSW10 Curncy"} <= reqs
        assert not any(t.startswith("ED") and len(t.split()[0]) == 4 for t in reqs)


def test_dump_needs_no_network_besides_bloomberg():
    orig = socket.socket.connect

    def refuse(*a, **k):
        raise AssertionError("network access during dump")
    socket.socket.connect = refuse
    try:
        with tempfile.TemporaryDirectory() as tmp:
            assert not _dump(Path(tmp), D(2026, 10, 7), D(2026, 10, 7), FakeBloomberg()).blocking
    finally:
        socket.socket.connect = orig


def test_loader_on_fake_dump_zero_unknown_columns():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _dump(root, D(2026, 10, 7), D(2026, 10, 7), FakeBloomberg())
        _dump(root, D(2019, 6, 12), D(2019, 6, 12), FakeBloomberg())
        frame, rep = loader.load(M, root=root)
        assert rep.found["unknown_columns"] == [] and rep.found["missing_columns"] == []
        assert rep.exit_code == 0, rep.report()
        assert list(frame.columns) == ["date", "instrument", "contract", "field", "value"]
        assert not frame.duplicated(["date", "instrument", "contract", "field"]).any()
        row = frame[(frame.instrument == "sofr3m_fut") & (frame.contract == "2026-12") & (frame.field == "PX_LAST")]
        assert len(row) == 1 and row.date.iloc[0] == pd.Timestamp("2026-10-07")
        assert set(frame[frame.date == "2019-06-12"].instrument) >= {"ed_fut", "swap_libor3m", "USDLIBOR3M"}
        assert check_market_data.main(["--root", str(root)]) == 0


def test_loader_reports_problems():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _dump(root, D(2026, 9, 1), D(2026, 10, 7), FakeBloomberg())
        f = root / "usd/2026/sofr3m_fut.csv"
        df = dumper.read_wide(f).copy()
        df["SFRZ26 Comdty|PX_ASK"] = 96.0                               # field not in manifest
        df["XYZ Comdty|PX_LAST"] = 1.0                                 # ticker not in manifest
        df["FFZ26 Comdty|PX_LAST"] = 96.0                              # wrong file
        df.loc["2026-09-15", "SFRU26 Comdty|PX_LAST"] = 120.0           # out of range
        df.loc["2026-09-21", "SFRQ26 Comdty|PX_LAST"] = np.nan
        dumper.write_wide(df, f)
        g = root / "usd/2026/ff_fut.csv"                                # FFV26 last trade 2026-10-30; FFU26 2026-09-30
        ff = dumper.read_wide(g)
        ff.loc["2026-10-07", "FFU26 Comdty|PX_LAST"] = 96.0             # quoted after last trade
        dumper.write_wide(ff, g)
        frame, rep = loader.load(M, root=root)
        s = rep.summary()
        assert s["unknown_columns"] == 3 and s["out_of_range"] == 1 and s["outside_listing"] == 1
        assert s["stale"] > 0                                            # the fake never moves
        assert rep.exit_code == 2
        assert check_market_data.main(["--root", str(root)]) == 2
        assert not ((frame.contract == "2026-09") & (frame.instrument == "ff_fut")
                    & (frame.date == "2026-10-07")).any()
        (root / "usd/2026/ff_fut.csv").write_text("date,FFV26 Comdty|PX_LAST\n07/10/2026,96\n")
        _, rep = loader.load(M, root=root)
        assert any("non-ISO" in x for x in rep.found["malformed"])


def test_dump_requests_generously_and_isolates_unlisted_contracts():
    day = D(2018, 6, 1)
    sr3 = {s.ticker for s in M.series(day, day) if s.instrument == "sofr3m_fut"}
    sr1 = {s.ticker for s in M.series(day, day) if s.instrument == "sofr1m_fut"}
    assert len(sr3) >= 41 + 6 and len(sr1) >= 13          # dump_listing, not the 20 / 7 listed at launch
    with tempfile.TemporaryDirectory() as tmp:
        fake = FakeBloomberg()
        res = _dump(Path(tmp), day, day, fake)
        assert not res.blocking
        dead = [x for x in res.failed if x.startswith("SFR")]
        assert dead and len(dead) % 3 == 0                    # unlisted SR3s, all three fields
        sr3_calls = [c for c in fake.calls if any(t.startswith("SFR") for t in c[0].values())]
        assert len(sr3_calls) < 3 * len(sr3)                   # bisection, not one call per ticker
        df = dumper.read_wide(Path(tmp) / "usd/2018/sofr3m_fut.csv")
        assert df["SFRM18 Comdty|PX_LAST"].notna().all() and df["SFRH28 Comdty|PX_LAST"].isna().all()
        _, rep = loader.load(M, root=Path(tmp))
        assert rep.found["unknown_columns"] == [] and rep.exit_code == 0, rep.report()


def test_quotes_before_an_unsourced_listing_are_kept_and_reported():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _dump(root, D(2019, 6, 12), D(2019, 6, 12), FakeBloomberg())
        f = root / "usd/2019/sofr1m_fut.csv"
        df = dumper.read_wide(f).copy()
        far = "SERM20 Comdty|PX_LAST"          # 13th month: requested, beyond the 7 modelled at launch
        assert far in df and df[far].isna().all()
        df[far] = 98.0
        dumper.write_wide(df, f)
        frame, rep = loader.load(M, root=root)
        assert rep.exit_code == 0
        assert any("SERM20" in x for x in rep.found["outside_listing_unverified"])
        assert ((frame.instrument == "sofr1m_fut") & (frame.contract == "2020-06")).any()
