"""Capture the public documents the manifest's rules cite.

``capture(manifest, directory)`` fetches every source with a ``fixture`` name
(CME/CBOT rule filings on cftc.gov, New York Fed reference-rate pages) and
writes the text a reader would check to ``directory/<fixture>_<YYYYMMDD>.txt``.

cmegroup.com is not fetched: its terms of use forbid automated access and it
blocks scripted requests. Pages saved from a browser are converted with
``convert_saved`` instead (same text format, same fixture naming).
"""
from __future__ import annotations

import datetime as dt
import io
import logging
import re
from pathlib import Path

import requests

from ..refdata.parsers.common import USER_AGENT, TIMEOUT, html_to_text, saving_fixtures, save_fixture
from .manifest import Manifest, normalise, quotes

LIVE_FIXTURES = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "live"


def pdf_text(data: bytes) -> str:
    from pypdf import PdfReader
    logging.getLogger("pypdf").setLevel(logging.CRITICAL)
    return "\n".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(data)).pages)


def document_text(data: bytes, url_or_name: str) -> str:
    if data[:5] == b"%PDF-" or url_or_name.lower().endswith(".pdf"):
        return pdf_text(data)
    if url_or_name.lower().endswith(".txt"):      # page text copied from a browser (Ctrl+A, Ctrl+C)
        return data.decode("utf-8-sig", errors="replace").replace("\r\n", "\n")
    return html_to_text(data.decode("utf-8", errors="replace"))


def fetch_bytes(url: str) -> bytes:
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
    r.raise_for_status()
    return r.content


def capture(m: Manifest, directory: Path | str, fetch=fetch_bytes) -> dict[str, str]:
    """Fetch every source with a fixture; returns {source id: 'ok <path>' | 'failed <why>'}."""
    report: dict[str, str] = {}
    done: dict[str, Path] = {}
    with saving_fixtures(directory):
        for sid, src in m.sources.items():
            name = src.get("fixture")
            if not name or "cmegroup.com" in src["url"]:
                continue
            if name in done:
                report[sid] = f"ok {done[name]} (shared)"
                continue
            try:
                text = document_text(fetch(src["url"]), src["url"])
            except Exception as exc:  # report and carry on; the test names what is missing
                report[sid] = f"failed {exc}"
                continue
            done[name] = save_fixture(name, text)
            report[sid] = f"ok {done[name]}"
    return report


def convert_saved(paths: list[Path | str], directory: Path | str) -> list[Path]:
    """Browser-saved pages (HTML or PDF) -> text fixtures. The fixture name is the
    file stem (name the file after the manifest source id, e.g. cme_sr3_specs.html,
    cme_sr3_specs_calendar.html)."""
    out = []
    with saving_fixtures(directory):
        for p in map(Path, paths):
            out.append(save_fixture(p.stem, document_text(p.read_bytes(), p.name)))
    return out


def latest_fixture(name: str, directory: Path = LIVE_FIXTURES) -> Path | None:
    files = sorted(directory.glob(f"{name}_[0-9]*.txt"))
    files = [f for f in files if re.fullmatch(rf"{re.escape(name)}_\d{{8}}", f.stem)]
    return files[-1] if files else None


def check_quotes(m: Manifest, directory: Path = LIVE_FIXTURES) -> list[str]:
    """Every quoted rule passage must appear in its source's captured text.
    Returns problems; sources still pending capture are skipped (listed separately)."""
    problems = []
    for path, sid, quote in quotes(m):
        src = m.sources[sid]
        if src.get("status", "captured") != "captured":
            continue
        f = latest_fixture(src["fixture"], directory)
        if f is None:
            problems.append(f"{path}: no capture of {src['fixture']} in {directory}")
        elif normalise(quote) not in normalise(f.read_text(encoding="utf-8")):
            problems.append(f"{path}: quote not found in {f.name}: {quote[:80]!r}")
    return problems


def pending(m: Manifest) -> dict[str, list[str]]:
    """Sources not yet captured -> the rule paths that cite them."""
    from .manifest import _walk_rules
    out: dict[str, list[str]] = {}
    for path, node in _walk_rules(m.raw):
        src = m.sources.get(node["source"], {})
        if src.get("status", "captured") != "captured":
            out.setdefault(node["source"], []).append(path)
    return out


def today_stamp() -> str:
    return f"{dt.date.today():%Y%m%d}"
