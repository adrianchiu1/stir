"""Bloomberg historical data through pdblp, for the dump only (terminal machines).

``PdblpReader`` is called like pxts.read_bdh (``{column: ticker}``, start, field,
end) but
* keeps one Bloomberg session open for the whole dump (pxts opens and closes one
  per call, about 1.4 s each), and
* skips a security that Bloomberg answers with a security error or field exception
  (``errors="ignore"``, the default) instead of aborting the whole bulk request,
  as pdblp's own ``bdh`` does. Skipped securities come back as NaN columns and are
  listed in ``last_errors``.
It uses pdblp's request plumbing (``_create_req``, ``_receive_events``), the same
calls ``pdblp.BCon.bdh`` makes.
"""
from __future__ import annotations

import pandas as pd

DEFAULT_PORT = 8194


class PdblpReader:
    def __init__(self, timeout: float = 120, port: int = DEFAULT_PORT):
        import pdblp   # terminal machines only (pip install -e .[bloomberg])
        self.con = pdblp.BCon(port=port, timeout=int(timeout * 1000))
        self.con.start()
        self.last_errors: dict[str, str] = {}
        self.errors_seen: dict[str, str] = {}      # every skipped security in this session

    def __call__(self, tickers: dict[str, str], start="2000-01-01", field: str = "PX_LAST", end=None,
                 timeout: float | None = None, errors: str = "ignore") -> pd.DataFrame:
        if timeout is not None:
            self.con.timeout = int(timeout * 1000)
        names: dict[str, list[str]] = {}
        for name, tkr in tickers.items():
            names.setdefault(tkr, []).append(name)
        setvals = [("startDate", pd.Timestamp(start).strftime("%Y%m%d")),
                   ("endDate", pd.Timestamp(end or pd.Timestamp.today()).strftime("%Y%m%d"))]
        request = self.con._create_req("HistoricalDataRequest", list(names), [field], [], setvals)
        self.con._session.sendRequest(request, identity=self.con._identity)
        rows, self.last_errors = [], {}
        for msg in self.con._receive_events():
            sd = msg["element"]["HistoricalDataResponse"]["securityData"]
            sec = sd["security"]
            if "securityError" in sd or len(sd["fieldExceptions"]) > 0:
                why = sd.get("securityError") or sd["fieldExceptions"]
                if errors == "raise":
                    raise ValueError(f"{sec}: {why}")
                self.last_errors[sec] = self.errors_seen[sec] = str(why)[:200]
                continue
            for fd in sd["fieldData"]:
                values = fd["fieldData"]
                if field in values:
                    rows.append((values["date"], sec, values[field]))
        long = pd.DataFrame(rows, columns=["date", "ticker", "value"])
        long["date"] = pd.to_datetime(long["date"])
        wide = long.pivot_table(index="date", columns="ticker", values="value", aggfunc="last")
        index = pd.DatetimeIndex(wide.index, name="date")
        cols = {col: (wide[tkr].to_numpy() if tkr in wide.columns else float("nan"))
                for tkr, names_ in names.items() for col in names_}
        return pd.DataFrame(cols, index=index).reindex(columns=list(tickers))

    def close(self) -> None:
        self.con.stop()
