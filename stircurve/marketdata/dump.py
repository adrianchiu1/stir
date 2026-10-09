"""Bloomberg dump: manifest -> pxts.read_bdh -> wide CSVs under data/market/<ccy>/<YYYY>/.

Runs on a terminal machine; Bloomberg (via pxts/pdblp on localhost:8194) is the
only network it touches. One file per year and group (a futures/swap
instrument, ``fixings`` or ``policy_anchors``), one column per
``<ticker>|<field>`` (canonical tickers: two-digit futures years), ISO dates,
``NaN`` for missing.

Never overwrites silently. The new values are merged into the existing file
and diffed like the reference-data updaters: new dates, new columns and
NaN -> value fills are additions; a changed value or a value that disappears
is blocking (nothing is written, exit 2). Files are written only with
``write_csv=True``; an unchanged file is not rewritten (idempotent).
"""
from __future__ import annotations

import datetime as dt
import inspect
import logging
import re
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from .. import DATA_DIR
from .manifest import Manifest, Series

log = logging.getLogger("stircurve.dump")
MARKET_DIR = DATA_DIR / "market"
# seconds pdblp waits for each part of a Bloomberg response (pxts read_bdh ``timeout``).
# It bounds the wait between messages, not the whole request, so a generous value costs
# nothing on calls that succeed: 120 s covers a 50-ticker request over 16 years of daily
# history on a busy terminal.
TIMEOUT = 120
CHUNK = 1000        # tickers per read_bdh call (bulk calls are much faster than many small ones)
REL_TOL = 1e-12


@dataclass
class FileDiff:
    path: Path
    added_rows: int = 0
    added_columns: list[str] = field(default_factory=list)
    filled: int = 0
    changed: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)

    @property
    def blocking(self) -> bool:
        return bool(self.changed or self.removed)

    @property
    def empty(self) -> bool:
        return not (self.added_rows or self.added_columns or self.filled or self.blocking)

    def report(self) -> str:
        if self.empty:
            return f"{self.path}: no changes"
        lines = [f"{self.path}: +{self.added_rows} rows, +{len(self.added_columns)} columns, {self.filled} NaN->value"]
        for label, items in (("changed", self.changed), ("removed", self.removed)):
            if items:
                lines.append(f"  {label} ({len(items)}):")
                lines += [f"    {x}" for x in items[:50]]
                if len(items) > 50:
                    lines.append(f"    ... {len(items) - 50} more")
        return "\n".join(lines)


class DumpError(RuntimeError):
    """Bloomberg is unusable for this run (no pdblp, no connection, every request failing)."""


@dataclass
class DumpResult:
    diffs: list[FileDiff] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)      # tickers Bloomberg returned nothing for
    reasons: dict[str, int] = field(default_factory=dict)  # error message -> count, for the failed tickers
    empty: list[Path] = field(default_factory=list)       # files with no rows returned (not written)
    written: list[Path] = field(default_factory=list)

    @property
    def blocking(self) -> bool:
        return any(d.blocking for d in self.diffs)

    def report(self) -> str:
        lines = [d.report() for d in self.diffs]
        if self.failed:
            lines.append(f"no data from Bloomberg for {len(self.failed)} ticker-fields (written as NaN; expected for "
                         "contracts not yet listed, since the dump requests generously):")
            lines += [f"  {t}" for t in self.failed[:40]]
            if len(self.failed) > 40:
                lines.append(f"  ... {len(self.failed) - 40} more")
            lines.append("errors behind them:")
            lines += [f"  {n} x {msg}" for msg, n in sorted(self.reasons.items(), key=lambda kv: -kv[1])[:5]]
        for p in self.empty:
            lines.append(f"{p}: Bloomberg returned no rows for the range; not written")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# planning
# ---------------------------------------------------------------------------
def year_ranges(start: dt.date, end: dt.date):
    for y in range(start.year, end.year + 1):
        yield y, max(start, dt.date(y, 1, 1)), min(end, dt.date(y, 12, 31))


def plan(m: Manifest, start: dt.date, end: dt.date, groups: list[str] | None = None
         ) -> dict[tuple[int, str], tuple[dt.date, dt.date, list[Series]]]:
    """{(year, group): (start, end, series)} for every file the dump writes."""
    out = {}
    for y, a, b in year_ranges(start, end):
        for s in m.series(a, b):
            g = m.group_of(s.instrument)
            if groups and g not in groups and s.instrument not in groups:
                continue
            out.setdefault((y, g), (a, b, []))[2].append(s)
    return out


def request_ticker(m: Manifest, s: Series, as_of: dt.date) -> str:
    if m.group_of(s.instrument) in m.futures():
        p = m.parse_future_ticker(s.ticker)
        return m.request_ticker(s.instrument, p[1], p[2], s.last_date, as_of)
    return s.ticker


# ---------------------------------------------------------------------------
# fetching
# ---------------------------------------------------------------------------
def fetch(m: Manifest, series: list[Series], start: dt.date, end: dt.date, as_of: dt.date, read_bdh,
          timeout: float = TIMEOUT, chunk: int = CHUNK, reasons: dict[str, int] | None = None
          ) -> tuple[pd.DataFrame, list[str]]:
    """One wide frame (index: dates, columns: canonical ``ticker|field``) and the
    columns Bloomberg returned nothing for, with one bulk read_bdh call per field.

    pdblp aborts a whole bulk call at the first security error or field exception
    (ValueError, not naming the security; Bloomberg sends errors before data), and
    pxts raises KeyError when a valid ticker has no rows (naming it). So:
    * if read_bdh supports ``errors="ignore"`` (pxts option: skip bad securities,
      return NaN), every field is one call;
    * otherwise tickers named in a KeyError are dropped and the call repeated, and
      a ValueError is resolved by splitting the call in halves.
    A futures ticker that fails in its one-digit form is retried once in its
    two-digit form (one more bulk call). A timeout is retried once, then the run
    stops (``DumpError``)."""
    fmt = m.column_format
    reasons = {} if reasons is None else reasons
    skip = bool(getattr(read_bdh, "skips_errors", False))
    by_field: dict[str, list[tuple[str, str]]] = {}
    alt: dict[str, str] = {}          # column -> two-digit request form, for one-digit futures requests
    for s in series:
        req = request_ticker(m, s, as_of)
        for f in s.fields:
            col = fmt.format(ticker=s.ticker, field=f)
            by_field.setdefault(f, []).append((col, req))
            if req != s.ticker and m.group_of(s.instrument) in m.futures():
                alt[col] = s.ticker
    frames: list[pd.DataFrame] = []
    failed: dict[str, tuple[str, str]] = {}     # column -> (requested ticker, reason)

    def call(req: dict[str, str], f: str) -> pd.DataFrame:
        kw = {"errors": "ignore"} if skip else {}
        df = read_bdh(req, start=start.isoformat(), field=f, end=end.isoformat(), timeout=timeout, **kw)
        return df.reindex(columns=list(req))

    def bisect(items: list[tuple[str, str]], f: str) -> None:
        if not items:
            return
        try:
            frames.append(call(dict(items), f))
        except Exception as exc:
            if is_timeout(exc):
                try:
                    frames.append(call(dict(items), f))
                    return
                except Exception as again:
                    raise DumpError(f"Bloomberg timed out twice ({len(items)} tickers, {f}, {start}..{end}, "
                                    f"timeout {timeout:g}s): {type(again).__name__}: {again}. "
                                    "Re-run with a larger --timeout or a shorter range / one --group at a time.") from again
            if len(items) == 1:
                failed[items[0][0]] = (items[0][1], f"{type(exc).__name__}: {exc}"[:160])
                return
            half = len(items) // 2
            bisect(items[:half], f)
            bisect(items[half:], f)

    def bulk(items: list[tuple[str, str]], f: str) -> None:
        if not skip:
            for _ in range(3):      # valid tickers without rows: pandas names them all in a KeyError
                try:
                    frames.append(call(dict(items), f))
                    return
                except KeyError as exc:
                    missing = missing_tickers(exc, {t for _, t in items})
                    if not missing:
                        break
                    for col, tkr in items:
                        if tkr in missing:
                            failed[col] = (tkr, "no data in range (pxts KeyError)")
                    items = [(c, t) for c, t in items if t not in missing]
                    if not items:
                        return
                except Exception:
                    break
        bisect(items, f)

    def run(items_by_field: dict[str, list[tuple[str, str]]]) -> None:
        for f, items in items_by_field.items():
            for i in range(0, len(items), chunk):
                bulk(items[i:i + chunk], f)

    def assemble() -> pd.DataFrame:
        wide = pd.concat(frames, axis=1) if frames else pd.DataFrame()
        wide = wide.loc[:, ~wide.columns.duplicated(keep="last")] if len(wide.columns) else wide
        wide.index = pd.DatetimeIndex(wide.index).normalize() if len(wide) else pd.DatetimeIndex([])
        wide = wide.loc[(wide.index >= pd.Timestamp(start)) & (wide.index <= pd.Timestamp(end))]
        cols = [c for items in by_field.values() for c, _ in items]
        return wide.reindex(columns=cols).astype(float)

    run(by_field)
    wide = assemble()
    for f, items in by_field.items():       # all-NaN columns (ignored errors, or no rows in range)
        for col, tkr in items:
            if col not in failed and wide[col].isna().all():
                seen = getattr(read_bdh, "errors_seen", {})
                failed[col] = (tkr, "security error / field exception (skipped)" if tkr in seen
                               else "no data from Bloomberg (NaN)")
    retry: dict[str, list[tuple[str, str]]] = {}
    for f, items in by_field.items():
        retry[f] = [(c, alt[c]) for c, _ in items if c in failed and c in alt]
    retry = {f: v for f, v in retry.items() if v}
    if retry:
        log.info("retrying %d ticker-fields in two-digit-year form", sum(map(len, retry.values())))
        before = set(failed)
        for f, items in retry.items():
            for col, _ in items:
                failed.pop(col)
        run(retry)
        wide = assemble()
        for f, items in retry.items():
            for col, tkr in items:
                if col not in failed and wide[col].isna().all():
                    failed[col] = (tkr, "no data in either year form")
        recovered = before - set(failed)
        if recovered:
            log.info("two-digit form worked for %d (e.g. %s)", len(recovered), sorted(recovered)[0])
    for col, (tkr, why) in failed.items():
        reasons[why] = reasons.get(why, 0) + 1
    return wide.sort_index(), [f"{c} (requested {t})" for c, (t, _) in failed.items()]


def missing_tickers(exc: KeyError, requested: set[str]) -> set[str]:
    """Tickers a pandas KeyError names ("['X Comdty'] not in index" or "None of
    [Index([...])] are in the [columns]"), restricted to those requested."""
    return set(re.findall(r"'([^']+)'", str(exc))) & requested


# ---------------------------------------------------------------------------
# merge + diff + write
# ---------------------------------------------------------------------------
def read_wide(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype={"date": str})
    df.index = pd.DatetimeIndex(pd.to_datetime(df.pop("date"), format="%Y-%m-%d"), name="date")
    return df.astype(float)


def write_wide(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    out = df.copy()
    out.index = out.index.strftime("%Y-%m-%d")
    out.index.name = "date"
    out.to_csv(path, na_rep="NaN", lineterminator="\n")


def merge(existing: pd.DataFrame | None, new: pd.DataFrame, path: Path) -> tuple[pd.DataFrame, FileDiff]:
    diff = FileDiff(path)
    if existing is None:
        diff.added_rows, diff.added_columns = len(new), list(new.columns)
        return new, diff
    cols = list(existing.columns) + [c for c in new.columns if c not in existing.columns]
    idx = existing.index.union(new.index)
    diff.added_rows = len(idx) - len(existing.index)
    diff.added_columns = [c for c in new.columns if c not in existing.columns]
    old = existing.reindex(index=idx, columns=cols)
    upd = new.reindex(index=idx, columns=cols)
    in_new = pd.DataFrame(np.outer(idx.isin(new.index), pd.Index(cols).isin(new.columns)), index=idx, columns=cols)
    in_old = pd.DataFrame(np.outer(idx.isin(existing.index), pd.Index(cols).isin(existing.columns)), index=idx, columns=cols)
    close = np.isclose(old.fillna(0).to_numpy(), upd.fillna(0).to_numpy(), rtol=REL_TOL, atol=0.0)
    changed = old.notna() & upd.notna() & ~close
    removed = old.notna() & upd.isna() & in_new          # fetched again, Bloomberg no longer has it
    diff.filled = int((old.isna() & upd.notna() & in_old).to_numpy().sum())
    for mask, out, fmt in ((changed, diff.changed, "{d} {c}: {o!r} -> {n!r}"), (removed, diff.removed, "{d} {c}: {o!r} -> NaN")):
        for i, j in np.argwhere(mask.to_numpy()):
            d, c = idx[i], cols[j]
            out.append(fmt.format(d=f"{d:%Y-%m-%d}", c=c, o=old.iat[i, j], n=upd.iat[i, j]))
    return old.where(old.notna(), upd).sort_index(), diff


def market_path(root: Path, ccy: str, year: int, group: str) -> Path:
    return root / ccy.lower() / f"{year}" / f"{group}.csv"


def is_timeout(exc: Exception) -> bool:
    """pdblp raises RuntimeError('Timeout ...') when no response arrives in time."""
    return isinstance(exc, TimeoutError) or "timeout" in str(exc).lower() or "timed out" in str(exc).lower()


def timed(read_bdh):
    """read_bdh that logs each call: size, range, seconds, outcome (the run's timing record).
    ``skips_errors``: read_bdh takes ``errors="ignore"`` (skip bad securities, NaN)."""
    def wrapper(tickers, start="2000-01-01", field="PX_LAST", end=None, timeout=TIMEOUT, **kw):
        log.info("read_bdh %-9s %4d tickers %s..%s ...", field, len(tickers), start, end)
        t0 = time.perf_counter()
        try:
            df = read_bdh(tickers, start=start, field=field, end=end, timeout=timeout, **kw)
        except Exception as exc:
            log.info("    %.1fs  %s: %s", time.perf_counter() - t0, type(exc).__name__, str(exc)[:200])
            raise
        log.info("    %.1fs  ok, %d rows x %d columns", time.perf_counter() - t0, len(df), df.shape[1])
        return df
    try:
        wrapper.skips_errors = "errors" in inspect.signature(read_bdh).parameters
    except (TypeError, ValueError):
        wrapper.skips_errors = False
    wrapper.errors_seen = getattr(read_bdh, "errors_seen", {})   # PdblpReader: Bloomberg's reason per skipped security
    return wrapper


def probe(m: Manifest, read_bdh, start: dt.date, end: dt.date, timeout: float) -> None:
    """One request for a ticker that always has data (EFFR) before the real run, so a
    missing pdblp or a refused connection stops the run with its own error instead of
    turning into hundreds of 'no data' columns."""
    ticker = m.fixings["EFFR"]["ticker"]
    try:
        df = read_bdh({"probe": ticker}, start=(start - dt.timedelta(days=14)).isoformat(), field="PX_LAST",
                      end=end.isoformat(), timeout=timeout)
    except TypeError as exc:
        if "timeout" in str(exc):
            raise DumpError("pxts.read_bdh has no 'timeout' argument: upgrade pxts "
                            "(pip install -U \"pxts[bloomberg] @ git+https://github.com/adrianchiu1/pxts\")") from exc
        raise DumpError(f"Bloomberg probe ({ticker} PX_LAST) failed: {type(exc).__name__}: {exc}") from exc
    except Exception as exc:
        hint = (" Is the terminal logged in, with the API on localhost:8194? Try a larger --timeout."
                if is_timeout(exc) else "")
        raise DumpError(f"Bloomberg probe ({ticker} PX_LAST) failed: {type(exc).__name__}: {exc}.{hint}") from exc
    if df is None or len(df) == 0:
        raise DumpError(f"Bloomberg probe ({ticker} PX_LAST) returned no rows for {start - dt.timedelta(days=14)}..{end}")


def staged_file(m: Manifest, root: Path, year: int, group: str, new: pd.DataFrame,
                result: DumpResult, staged: list) -> None:
    path = market_path(root, m.currency, year, group)
    if new.empty:
        result.empty.append(path)
        return
    existing = read_wide(path) if path.exists() else None
    merged, diff = merge(existing, new, path)
    result.diffs.append(diff)
    if not diff.empty:
        staged.append((merged, path))


def dump(m: Manifest, start: dt.date, end: dt.date, read_bdh=None, *, write_csv: bool = False,
         as_of: dt.date | None = None, root: Path = MARKET_DIR, groups: list[str] | None = None,
         timeout: float = TIMEOUT, chunk: int = CHUNK, backend: str = "pdblp") -> DumpResult:
    """``read_bdh``: a pxts.read_bdh-like callable (tests); otherwise ``backend``
    'pdblp' (default: one session, bad securities skipped, see bbg.py) or 'pxts'."""
    reader = None
    if read_bdh is None and backend == "pdblp":
        from .bbg import PdblpReader
        try:
            reader = read_bdh = PdblpReader(timeout=timeout)
        except Exception as exc:
            raise DumpError(f"could not start a Bloomberg session through pdblp: {type(exc).__name__}: {exc}. "
                            "Is the terminal logged in, with the API on localhost:8194? "
                            "(pip install pdblp blpapi)") from exc
    elif read_bdh is None:
        from pxts import read_bdh   # terminal machines only (pip install -e .[bloomberg])
    try:
        return _dump(m, start, end, read_bdh, write_csv=write_csv, as_of=as_of, root=root, groups=groups,
                     timeout=timeout, chunk=chunk)
    finally:
        if reader is not None:
            reader.close()


def _dump(m: Manifest, start: dt.date, end: dt.date, read_bdh, *, write_csv: bool, as_of: dt.date | None,
          root: Path, groups: list[str] | None, timeout: float, chunk: int) -> DumpResult:
    as_of = as_of or dt.date.today()
    read_bdh = timed(read_bdh)
    probe(m, read_bdh, start, end, timeout)
    result = DumpResult()
    staged, requested = [], 0
    by_year: dict[int, list] = {}
    t0 = time.perf_counter()
    planned = plan(m, start, end, groups)
    log.info("planned %d files, %d tickers in %.1fs", len(planned),
             sum(len(v[2]) for v in planned.values()), time.perf_counter() - t0)
    for (year, group), (a, b, series) in sorted(planned.items()):
        by_year.setdefault(year, []).append((group, a, b, series))
    for year, files in by_year.items():
        a, b = files[0][1], files[0][2]
        everything = [s for *_, series in files for s in series]
        wide, failed = fetch(m, everything, a, b, as_of, read_bdh, timeout=timeout, chunk=chunk, reasons=result.reasons)
        result.failed += failed
        requested += sum(len(s.fields) for s in everything)
        for group, _, _, series in files:
            cols = [c for s in series for c in s.columns(m.column_format)]
            new = wide.reindex(columns=cols).dropna(how="all") if len(wide) else wide.reindex(columns=cols)
            staged_file(m, root, year, group, new, result, staged)
    if requested and len(result.failed) == requested:
        top = max(result.reasons, key=result.reasons.get) if result.reasons else "unknown"
        raise DumpError(f"Bloomberg returned nothing for any of {requested} ticker-fields; nothing written. "
                        f"Most common error: {top}")
    if write_csv and not result.blocking:
        for merged, path in staged:
            write_wide(merged, path)
            result.written.append(path)
    return result
