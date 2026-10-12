"""Bloomberg WIRP captures and the three-layer comparison (M2 gate; AC, PR #4).

Captures live in ``tests/fixtures/live/wirp_us_<model>_<YYYYMMDD>.txt`` with
``model`` = ``fut`` (WIRP US, Fed Funds Futures) or ``ois`` (WIRP US OIS), one per
gate date and model: the screen's header lines (Region, Instrument, Target Rate,
Effective Rate, Pricing Date, Cur. Imp. O/N Rate) and the meeting table
(Meeting, #Hikes/Cuts, %Hike/Cut, Imp. Rate Δ, Implied Rate, A.R.M.). The first
captures (7 Oct 2026) are AC's screenshots (``.png`` next to the text) transcribed
by hand and checked against the implied-data identities (#moves = Δ / A.R.M.,
Δ = implied - current, % = step / A.R.M.); later ones are pasted text. WIRP is a
terminal screen and is never fetched.

Comparison per meeting (``compare``): the replica of WIRP's own model against the
capture (layer 1: data, conventions, calendars), our estimator against the replica
(layer 2: what the extra quotes and the prior change) and the estimator against
the capture. The gate is |replica - WIRP| <= 1bp and |fit - WIRP| <= 1bp on the
post-meeting implied rate of every meeting WIRP shows, every miss with a reason.
"""
from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

MATCH_DAYS = 3
GATE_BP = 1.0
FIXTURE_DIR = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "live"
MODELS = {"fut": "futures", "ois": "ois"}
INSTRUMENT_MODEL = {"fed funds futures": "futures", "overnight index swaps": "ois"}

ROW_RE = re.compile(r"^\s*(\d{1,2}/\d{1,2}/\d{4})\s+([+-]?\d+(?:\.\d+)?)\s+([+-]?\d+(?:\.\d+)?)%\s+"
                    r"([+-]?\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s*$")
META_RE = {
    "instrument": re.compile(r"Instrument:\s*(.+?)\s*$", re.I),
    "region": re.compile(r"Region:\s*(.+?)\s*$", re.I),
    "target_rate": re.compile(r"Target Rate\s+([\d.]+)", re.I),
    "effective_rate": re.compile(r"Effective Rate\s+([\d.]+)", re.I),
    "pricing_date": re.compile(r"Pricing Date\s+(\d{1,2}/\d{1,2}/\d{4})", re.I),
    "current_implied": re.compile(r"Cur\.?\s*Imp\.?\s*O/N Rate\s+([\d.]+)", re.I),
}


class WirpFormatError(ValueError):
    """The text is not a WIRP capture this parser recognises."""


@dataclass
class WirpTable:
    model: str                               # 'futures' | 'ois'
    pricing_date: dt.date | None
    current_implied: float | None
    rows: pd.DataFrame                       # meeting, n_moves, pct_move, imp_rate_delta, implied_rate, arm
    meta: dict[str, str] = field(default_factory=dict)
    source: str = ""


def _mdy(tok: str) -> dt.date:
    return dt.datetime.strptime(tok, "%m/%d/%Y").date()


def parse_wirp(text: str, source: str = "") -> WirpTable:
    meta: dict[str, str] = {}
    rows = []
    for line in text.replace("\r\n", "\n").split("\n"):
        if line.startswith("#"):
            continue
        for key, rx in META_RE.items():
            mm = rx.search(line)
            if mm and key not in meta:
                meta[key] = mm.group(1).strip()
        mr = ROW_RE.match(line)
        if mr:
            rows.append({"meeting": _mdy(mr.group(1)), "n_moves": float(mr.group(2)), "pct_move": float(mr.group(3)),
                         "imp_rate_delta": float(mr.group(4)), "implied_rate": float(mr.group(5)),
                         "arm": float(mr.group(6))})
    if not rows:
        raise WirpFormatError(f"{source or 'text'}: no meeting rows (mm/dd/yyyy  #moves  %move%  delta  implied  arm)")
    if "instrument" not in meta:
        raise WirpFormatError(f"{source or 'text'}: no 'Instrument:' line naming the WIRP model")
    model = INSTRUMENT_MODEL.get(meta["instrument"].lower().rstrip(" »"))
    if model is None:
        raise WirpFormatError(f"{source or 'text'}: unknown instrument {meta['instrument']!r}")
    df = pd.DataFrame(rows)
    # the capture's own identities, to catch a transcription slip
    cur = float(meta["current_implied"]) if "current_implied" in meta else None
    if cur is not None:
        bad = (df["implied_rate"] - cur - df["imp_rate_delta"]).abs() > 0.0015
        if bad.any():
            raise WirpFormatError(f"{source}: Imp. Rate Δ != Implied Rate - Current on {list(df['meeting'][bad])}")
    bad = (df["imp_rate_delta"] / df["arm"] - df["n_moves"]).abs() > 0.006
    if bad.any():
        raise WirpFormatError(f"{source}: #Hikes/Cuts != Δ / A.R.M. on {list(df['meeting'][bad])}")
    return WirpTable(model, _mdy(meta["pricing_date"]) if "pricing_date" in meta else None, cur, df, meta, source)


def fixture_path(as_of: dt.date, model: str, directory: Path = FIXTURE_DIR) -> Path:
    short = {v: k for k, v in MODELS.items()}[model]
    return directory / f"wirp_us_{short}_{as_of:%Y%m%d}.txt"


def load_capture(as_of: dt.date, model: str, directory: Path = FIXTURE_DIR) -> WirpTable | None:
    p = fixture_path(as_of, model, directory)
    if not p.exists():
        return None
    t = parse_wirp(p.read_text(encoding="utf-8"), p.name)
    if t.model != model:
        raise WirpFormatError(f"{p.name}: file named for {model} but the Instrument line says {t.model}")
    return t


def compare(meetings: pd.DataFrame, wirp: WirpTable, current_implied: float, replica_current: float,
            gate_bp: float = GATE_BP) -> pd.DataFrame:
    """One row per WIRP meeting (plus the stub): replica, fit and WIRP implied rates with the gaps in bp.
    ``meetings``: one curve's rows from ``policy.outputs.curve_meeting_rows``."""
    out = []
    if wirp.current_implied is not None:
        out.append({"meeting": "current", "wirp": wirp.current_implied, "replica": round(replica_current, 6),
                    "fit": round(current_implied, 6),
                    "replica_minus_wirp_bp": round((replica_current - wirp.current_implied) * 100.0, 2),
                    "fit_minus_wirp_bp": round((current_implied - wirp.current_implied) * 100.0, 2),
                    "fit_minus_replica_bp": round((current_implied - replica_current) * 100.0, 2),
                    "replica_ok": abs(replica_current - wirp.current_implied) * 100.0 <= gate_bp,
                    "fit_ok": abs(current_implied - wirp.current_implied) * 100.0 <= gate_bp, "reason": ""})
    for w in wirp.rows.itertuples():
        gaps = [abs((d - w.meeting).days) for d in meetings["decision_date"]]
        j = int(np.argmin(gaps)) if gaps else -1
        row = {"meeting": w.meeting, "wirp": w.implied_rate}
        if j < 0 or gaps[j] > MATCH_DAYS:
            row.update(replica=np.nan, fit=np.nan, replica_minus_wirp_bp=np.nan, fit_minus_wirp_bp=np.nan,
                       fit_minus_replica_bp=np.nan, replica_ok=False, fit_ok=False,
                       reason="no meeting in the reference data on this date (superseded, or not yet published?)")
        else:
            o = meetings.iloc[j]
            rep, fit = o["replica_rate"], o["implied_rate"]
            reasons = []
            if o["synthetic"]:
                reasons.append("synthetic meeting (not in the published calendar)")
            if o["unscheduled"]:
                reasons.append("unscheduled meeting")
            if o["beyond_wirp_reach"]:
                reasons.append("beyond the replica's reach (no instrument WIRP would use prices it)")
            if o["under_identified"]:
                reasons.append("prior-driven parcel (equal-step split)")
            if gaps[j]:
                reasons.append(f"WIRP date {w.meeting} vs decision {o['decision_date']}")
            row.update(decision_date=o["decision_date"], replica=rep, fit=fit,
                       replica_minus_wirp_bp=round((rep - w.implied_rate) * 100.0, 2) if np.isfinite(rep) else np.nan,
                       fit_minus_wirp_bp=round((fit - w.implied_rate) * 100.0, 2),
                       fit_minus_replica_bp=round((fit - rep) * 100.0, 2) if np.isfinite(rep) else np.nan,
                       replica_ok=bool(np.isfinite(rep) and abs(rep - w.implied_rate) * 100.0 <= gate_bp),
                       fit_ok=bool(abs(fit - w.implied_rate) * 100.0 <= gate_bp), reason="; ".join(reasons))
        out.append(row)
    return pd.DataFrame(out)
