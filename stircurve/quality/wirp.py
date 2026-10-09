"""Bloomberg WIRP table (copied as text by AC) and the comparison with the front end (M2 gate).

Captures live in ``tests/fixtures/live/wirp_usd_<YYYYMMDD>.txt`` (as-of date in the
name), one per gate date: the WIRP screen for that as-of date, Ctrl+A / Ctrl+C
of the page text (as for the CME pages in M1). WIRP is a terminal screen, so the
text is captured by hand and never fetched.

STATUS: written before the first capture. The parser is driven by the table's
header line and refuses text it does not recognise (``WirpFormatError``) rather
than guessing; it is pinned to the real text by ``tests/test_wirp.py`` once the
captures land (CLAUDE.md: fixtures are captured, not hand-written).

Comparison: each WIRP meeting is matched to the front end's meeting with the
same decision date (within ``MATCH_DAYS``); the gate is |ours - WIRP| <= 1bp on
the implied rate of every meeting, and every miss carries a reason.
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

# header label (normalised: lower case, letters/digits/#/% only) -> column
HEADERS = {
    "meeting": "meeting", "meetingdate": "meeting", "date": "meeting",
    "#hikes/cuts": "moves", "#hikescuts": "moves", "#ofhikes/cuts": "moves", "#hikes": "moves", "#cuts": "moves",
    "%hike/cut": "prob", "%hikecut": "prob", "%hike": "prob", "%cut": "prob",
    "imp.rated": "change", "imp.ratechange": "change", "impratechange": "change", "imp.rateΔ": "change",
    "imprated": "change",
    "impliedrate": "implied_rate", "imp.rate": "implied_rate", "imprate": "implied_rate",
    "a.r.m.": "arm", "arm": "arm",
}
DATE_FORMATS = ("%m/%d/%Y", "%m/%d/%y", "%d-%b-%y", "%d-%b-%Y", "%b %d %Y", "%d %b %Y", "%Y-%m-%d")


class WirpFormatError(ValueError):
    """The text is not a WIRP table this parser recognises."""


@dataclass
class WirpTable:
    as_of: dt.date | None
    rows: pd.DataFrame                       # meeting (date), implied_rate (percent) [, moves, prob, change, arm]
    meta: dict[str, str] = field(default_factory=dict)


def _norm(h: str) -> str:
    return re.sub(r"[^a-z0-9#%/.Δ]", "", h.lower().replace("delta", "Δ"))


def _split(line: str) -> list[str]:
    parts = re.split(r"\t+|\s{2,}", line.strip())
    return [p.strip() for p in parts if p.strip()]


def _date(tok: str) -> dt.date | None:
    tok = tok.strip()
    for f in DATE_FORMATS:
        try:
            return dt.datetime.strptime(tok, f).date()
        except ValueError:
            pass
    return None


def _num(tok: str) -> float:
    t = tok.replace("%", "").replace(",", "").replace("+", "").strip()
    if t in ("", "-", "--", "N.A.", "N/A"):
        return np.nan
    return float(t)


def parse_wirp(text: str) -> WirpTable:
    lines = [l for l in text.replace("\r\n", "\n").split("\n")]
    header_i, cols = None, None
    for i, line in enumerate(lines):
        toks = _split(line)
        mapped = [HEADERS.get(_norm(t)) for t in toks]
        if "meeting" in mapped and "implied_rate" in mapped:
            header_i, cols = i, mapped
            break
    if header_i is None:
        raise WirpFormatError("no header line with 'Meeting' and 'Implied Rate': not a WIRP table this parser knows")
    rows = []
    for line in lines[header_i + 1:]:
        toks = _split(line)
        if not toks:
            continue
        d = _date(toks[0])
        if d is None:
            if rows:
                break            # end of the table
            continue
        if len(toks) != len(cols):
            raise WirpFormatError(f"row {line!r}: {len(toks)} fields for {len(cols)} header columns")
        row = {"meeting": d}
        for c, t in zip(cols[1:], toks[1:]):
            if c:
                row[c] = _num(t)
        rows.append(row)
    if not rows:
        raise WirpFormatError("header found but no meeting rows under it")
    meta = {}
    as_of = None
    for line in lines[:header_i]:
        m = re.search(r"(as of|date)\W+(\d{1,2}/\d{1,2}/\d{2,4}|\d{4}-\d{2}-\d{2})", line, re.I)
        if m and as_of is None:
            as_of = _date(m.group(2))
        for key in ("instrument", "source", "based on", "current", "effective"):
            if key in line.lower():
                meta.setdefault(key, line.strip())
    return WirpTable(as_of, pd.DataFrame(rows), meta)


def fixture_path(as_of: dt.date, directory: Path = FIXTURE_DIR) -> Path:
    return directory / f"wirp_usd_{as_of:%Y%m%d}.txt"


def compare(meetings: pd.DataFrame, wirp: WirpTable, gate_bp: float = GATE_BP) -> pd.DataFrame:
    """One row per WIRP meeting: our implied rate, WIRP's, the gap in bp, pass/miss and a reason.
    ``meetings``: ``stircurve.policy.outputs.meeting_table``."""
    ours = meetings.copy()
    out = []
    for w in wirp.rows.itertuples():
        gaps = [abs((d - w.meeting).days) for d in ours["decision_date"]]
        j = int(np.argmin(gaps)) if gaps else -1
        row = {"meeting": w.meeting, "wirp_rate": w.implied_rate}
        if j < 0 or gaps[j] > MATCH_DAYS:
            row.update(ours_rate=np.nan, diff_bp=np.nan, ok=False,
                       reason="no meeting in the reference data on this date (cancelled or replaced?)")
        else:
            o = ours.iloc[j]
            diff = (o["implied_rate"] - w.implied_rate) * 100.0
            reasons = []
            if o["synthetic"]:
                reasons.append("synthetic meeting")
            if not o["scheduled"]:
                reasons.append("unscheduled meeting")
            if o["under_identified"]:
                reasons.append("under-identified parcel (prior split)")
            if gaps[j]:
                reasons.append(f"WIRP date {w.meeting} vs decision {o['decision_date']}")
            row.update(ours_decision=o["decision_date"], ours_rate=o["implied_rate"], diff_bp=round(diff, 3),
                       ok=bool(abs(diff) <= gate_bp), reason="; ".join(reasons))
        out.append(row)
    return pd.DataFrame(out)
