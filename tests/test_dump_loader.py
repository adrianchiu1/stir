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

    def __init__(self, dead=(), bump=None, one_digit_until=None):   # (year, month) of the last one-digit contract Bloomberg resolves
        self.dead, self.bump, self.calls = set(dead), bump or {}, []
        self.one_digit_until = one_digit_until    # last contract year Bloomberg resolves in one-digit form

    def invalid(self, column, ticker):
        if ticker in self.dead:
            return True
        canon = column.split("|")[0]
        if self.one_digit_until and ticker != canon and canon.endswith("Comdty"):
            _, y, mo = M.parse_future_ticker(canon)
            return (y, mo) > self.one_digit_until
        return False

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
        rows = []
        for name, t in tickers.items():          # pdblp: invalid security -> ValueError(rows so far)
            if self.invalid(name, t):
                raise ValueError(rows)
            rows += [(d, t, field, self.value(name, t, field, d)) for d in days]
        # pxts does raw.loc[:, tickers]: pandas raises KeyError naming every ticker Bloomberg
        # had nothing for (dead, or a contract the generous dump horizon asks for before listing)
        missing = [t for name, t in tickers.items()
                   if all(np.isnan(self.value(name, t, field, d)) for d in days)]
        if missing and len(missing) == len(tickers):
            raise KeyError(f"None of [Index({missing!r}, dtype='object')] are in the [columns]")
        if missing:
            raise KeyError(f"{missing!r} not in index")
        return pd.DataFrame({name: [self.value(name, t, field, d) for d in days] for name, t in tickers.items()},
                            index=pd.DatetimeIndex(days))


class FakeBloombergIgnore(FakeBloomberg):
    """pxts with errors="ignore": bad securities come back as NaN columns, never an exception."""

    def read_bdh(self, tickers, start="2000-01-01", field="PX_LAST", end=None, timeout=5, errors="raise"):
        self.calls.append((dict(tickers), start, end, field))
        days = pd.bdate_range(start, end)
        return pd.DataFrame({name: [np.nan if self.invalid(name, t) else self.value(name, t, field, d) for d in days]
                             for name, t in tickers.items()}, index=pd.DatetimeIndex(days))


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
        assert dead
        # probe + per field (PX_LAST, OPEN_INT, PX_VOLUME): one bulk call naming the missing
        # tickers, one bulk call without them
        assert len(fake.calls) <= 1 + 3 * 2 * 2, len(fake.calls)   # + one two-digit retry round per field
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


def test_broken_bloomberg_stops_the_run_and_writes_nothing():
    def no_pdblp(*a, **k):
        raise ImportError("pdblp required for read_bdh()")
    with tempfile.TemporaryDirectory() as tmp:
        rc = dump_bloomberg.main(["--start", "2026-10-07", "--end", "2026-10-07", "--root", tmp, "--write-csv"],
                                 read_bdh=no_pdblp)
        assert rc == 1 and not any(Path(tmp).rglob("*.csv"))

    fake = FakeBloomberg()

    def only_probe(tickers, **kw):           # connection fine for the probe, then every request errors
        if list(tickers) == ["probe"]:
            return fake.read_bdh(tickers, **kw)
        raise RuntimeError("Bloomberg request timed out")
    with tempfile.TemporaryDirectory() as tmp:
        try:
            dumper.dump(M, D(2026, 10, 7), D(2026, 10, 7), only_probe, write_csv=True, root=Path(tmp))
            raise AssertionError("expected DumpError")
        except dumper.DumpError as exc:
            assert "RuntimeError: Bloomberg request timed out" in str(exc)
        assert not any(Path(tmp).rglob("*.csv"))


def test_loader_blocks_on_files_without_rows():
    # what a dump that silently got nothing used to write: header only
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "usd/2026").mkdir(parents=True)
        (root / "usd/2026/fixings.csv").write_text("date,FEDL01 Index|PX_LAST,SOFRRATE Index|PX_LAST\n")
        _, rep = loader.load(M, D(2026, 10, 7), D(2026, 10, 7), root=root)
        assert rep.found["no_data"] and rep.exit_code == 2
        assert check_market_data.main(["--root", str(root), "--start", "2026-10-07", "--end", "2026-10-07"]) == 2


def test_timeouts_retry_once_then_stop_and_default_timeout_is_passed():
    fake, seen, flaky = FakeBloomberg(), [], {"left": 1}

    def slow_once(tickers, **kw):
        seen.append(kw["timeout"])
        if list(tickers) != ["probe"] and flaky["left"]:
            flaky["left"] -= 1
            raise RuntimeError("Timeout waiting for Bloomberg response")
        return fake.read_bdh(tickers, **kw)
    with tempfile.TemporaryDirectory() as tmp:
        res = dumper.dump(M, D(2026, 10, 7), D(2026, 10, 7), slow_once, write_csv=True, root=Path(tmp))
        assert not res.failed or all("Timeout" not in r for r in res.reasons)   # the retry succeeded
        assert set(seen) == {dumper.TIMEOUT} and dumper.TIMEOUT == 120

    def old_pxts(tickers, start="2000-01-01", field="PX_LAST", end=None):
        return fake.read_bdh(tickers, start=start, field=field, end=end)
    with tempfile.TemporaryDirectory() as tmp:
        rc = dump_bloomberg.main(["--start", "2026-10-07", "--end", "2026-10-07", "--root", tmp], read_bdh=old_pxts)
        assert rc == 1


def test_request_tickers_never_collide_and_far_contracts_skip_count_fields():
    day, asof = D(2026, 10, 7), D(2026, 10, 9)
    plan = [s for s in M.series(day, day) if M.group_of(s.instrument) in M.futures()]
    req = [dumper.request_ticker(M, s, asof) for s in plan]
    assert len(req) == len(set(req))                      # one Bloomberg ticker per contract
    by = {s.ticker: (r, s.fields) for s, r in zip(plan, req)}
    assert by["SFRU35 Comdty"][0] == "SFRU35 Comdty"       # 'SFRU5' would be Sep 2025 (AC's dump)
    assert by["SFRZ27 Comdty"][0] == "SFRZ7 Comdty" and by["SFRU28 Comdty"][0] == "SFRU28 Comdty"
    assert by["SFRZ26 Comdty"][0] == "SFRZ6 Comdty"
    assert by["SFRZ26 Comdty"][1] == ("PX_LAST", "OPEN_INT", "PX_VOLUME")
    assert by["SFRU35 Comdty"][1] == ("PX_LAST",)
    assert by["FFF29 Comdty"][1] == ("PX_LAST",) and by["FFF28 Comdty"][1][1:] == ("OPEN_INT", "PX_VOLUME")


def test_invalid_securities_isolated_by_halving():
    # pdblp raises ValueError (naming nothing) at the first bad security: halving finds them
    with tempfile.TemporaryDirectory() as tmp:
        fake = FakeBloomberg(dead={"USOSFR12 Curncy", "FFZ7 Comdty", "FFZ27 Comdty"})
        res = _dump(Path(tmp), D(2026, 10, 7), D(2026, 10, 7), fake)
        bad = {x.split("|")[0] for x in res.failed}
        assert {"USOSFR12 Curncy", "FFZ27 Comdty"} <= bad
        df = dumper.read_wide(Path(tmp) / "usd/2026/ois_sofr.csv")
        assert df["USOSFR10 Curncy|PX_LAST"].notna().all()


def test_one_digit_years_bloomberg_rejects_are_retried_in_two_digits():
    # Bloomberg resolved SFRH8/SFRM8 (2028) but not SFRU8..SFRZ4 (Sep 2028 - 2034) on 2026-10-07
    with tempfile.TemporaryDirectory() as tmp:
        fake = FakeBloomberg(one_digit_until=(2028, 6))
        res = _dump(Path(tmp), D(2026, 10, 7), D(2026, 10, 7), fake)
        df = dumper.read_wide(Path(tmp) / "usd/2026/sofr3m_fut.csv")
        assert df["SFRU30 Comdty|PX_LAST"].notna().all()                # recovered as 'SFRU30 Comdty'
        assert "SFRU30 Comdty" in {t for c in fake.calls for t in c[0].values()}
        assert not any(x.startswith("SFRU30") for x in res.failed)


def test_pxts_errors_ignore_means_one_call_per_field():
    with tempfile.TemporaryDirectory() as tmp:
        fake = FakeBloombergIgnore(dead={"USOSFR12 Curncy"}, one_digit_until=(2028, 6))
        res = _dump(Path(tmp), D(2026, 10, 7), D(2026, 10, 7), fake)
        main = [c for c in fake.calls if c[1] == "2026-10-07"]
        assert len(main) <= 3 * 2, len(main)      # one per field + one two-digit retry per field
        assert any(x.startswith("USOSFR12 Curncy|PX_LAST") for x in res.failed)
        df = dumper.read_wide(Path(tmp) / "usd/2026/sofr3m_fut.csv")
        assert df["SFRU30 Comdty|PX_LAST"].notna().all()



class _FakeBCon:
    """The slice of pdblp.BCon the PdblpReader uses, answering like Bloomberg: one
    message per security; invalid ones carry securityError, missing fields a fieldException."""
    starts = stops = 0

    def __init__(self, port=8194, timeout=5000):
        self.timeout, self._identity, self.fake, self.requests = timeout, None, _FakeBCon.fake, []
        self._session = self

    def start(self):
        _FakeBCon.starts += 1

    def stop(self):
        _FakeBCon.stops += 1

    def _create_req(self, rtype, tickers, flds, ovrds, setvals):
        return {"tickers": tickers, "field": flds[0], **dict(setvals)}

    def sendRequest(self, request, identity=None):
        self.requests.append(request)

    def _receive_events(self):
        req = self.requests[-1]
        days = pd.bdate_range(req["startDate"], req["endDate"])
        self.fake.calls.append(({t: t for t in req["tickers"]}, req["startDate"], req["endDate"], req["field"]))
        for t in req["tickers"]:
            sd = {"security": t, "fieldExceptions": [], "fieldData": []}
            canon = {r: c for c, r in _FakeBCon.columns.items()}.get(t, t)
            if self.fake.invalid(canon + "|", t):
                sd["securityError"] = {"message": "Unknown/Invalid security"}
            else:
                vals = [(d, self.fake.value(canon + "|" + req["field"], t, req["field"], d)) for d in days]
                sd["fieldData"] = [{"fieldData": {"date": d.date(), req["field"]: v}} for d, v in vals if not np.isnan(v)]
            yield {"element": {"HistoricalDataResponse": {"securityData": sd}}}


def test_pdblp_backend_one_session_one_request_per_field():
    import sys, types
    fake = FakeBloomberg(dead={"USOSFR12 Curncy"}, one_digit_until=(2028, 6))
    day, asof = D(2026, 10, 7), D(2026, 10, 9)
    _FakeBCon.fake, _FakeBCon.starts, _FakeBCon.stops = fake, 0, 0
    _FakeBCon.columns = {s.ticker: dumper.request_ticker(M, s, asof) for s in M.series(day, day)}
    sys.modules["pdblp"] = types.SimpleNamespace(BCon=_FakeBCon)
    try:
        with tempfile.TemporaryDirectory() as tmp:
            res = dumper.dump(M, day, day, write_csv=True, root=Path(tmp), as_of=asof, backend="pdblp")
            assert _FakeBCon.starts == 1 and _FakeBCon.stops == 1           # one session for the run
            main = [c for c in fake.calls if c[1] == "20261007"]
            assert len(main) <= 3 * 2, len(main)        # one request per field (+ one two-digit retry each)
            assert any(x.startswith("USOSFR12 Curncy|PX_LAST") for x in res.failed)
            assert "security error / field exception (skipped)" in res.reasons
            df = dumper.read_wide(Path(tmp) / "usd/2026/sofr3m_fut.csv")
            assert df["SFRZ26 Comdty|PX_LAST"].notna().all() and df["SFRU30 Comdty|PX_LAST"].notna().all()
            _, rep = loader.load(M, day, day, root=Path(tmp))
            assert rep.exit_code == 0 and rep.found["unknown_columns"] == [], rep.report()
    finally:
        del sys.modules["pdblp"]


def test_committed_bloomberg_days_have_zero_unknown_columns():
    # the M1 gate on AC's real dumps (data/market/usd)
    for day in (D(2026, 10, 7), D(2019, 6, 12)):
        frame, rep = loader.load(M, day, day)
        if not rep.files:
            continue
        assert rep.values > 250 and rep.found["unknown_columns"] == [] and rep.found["no_data"] == [], rep.report()
        assert rep.found["outside_listing"] == [] and rep.found["outside_listing_unverified"] == []
