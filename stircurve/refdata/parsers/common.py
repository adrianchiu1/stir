"""Shared helpers for the reference-data parsers.

All parsers are text-based: the page is reduced to plain text with one
block element per line, and dates are found with regular expressions anchored
on nearby year / month context. That is deliberately less precise than XPath
but far more robust to site redesigns, which is the main failure mode of
calendar scrapers. Each parser exposes ``parse_text(text)`` (pure, tested
against fixtures) and ``fetch_*()`` (network).
"""
from __future__ import annotations

import contextlib
import datetime as dt
import re
from pathlib import Path
from typing import Iterable, Iterator

import requests

USER_AGENT = "stircurve-refdata-updater/0.0.1 (+https://github.com/)"
TIMEOUT = 30

MONTHS = {m.lower(): i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July", "August",
     "September", "October", "November", "December"], start=1)}
MONTHS.update({k[:3]: v for k, v in list(MONTHS.items())})
MONTHS.update({"sept": 9})
MONTH_RE = r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"


def month_number(name: str) -> int:
    return MONTHS[name.strip(". ").lower()]


def fetch(url: str, timeout: int = TIMEOUT) -> str:
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    r.raise_for_status()
    r.encoding = r.encoding or "utf-8"
    return r.text


def html_to_text(html: str) -> str:
    """Plain text with block elements separated by newlines; table cells by ' | '."""
    try:
        from lxml import html as lh
    except ImportError:  # pragma: no cover
        return re.sub(r"<[^>]+>", "\n", html)
    doc = lh.fromstring(html)
    for bad in doc.xpath("//script|//style|//nav|//header|//footer"):
        bad.drop_tree()
    for el in doc.iter():
        tag = el.tag if isinstance(el.tag, str) else ""
        if tag in ("td", "th"):
            el.tail = (" | " if el.getnext() is not None else "") + (el.tail or "")
        elif tag in ("br", "p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "table", "section", "article", "strong", "b"):
            el.tail = "\n" + (el.tail or "") if tag != "strong" and tag != "b" else (el.tail or "")
            if tag in ("p", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "table", "section", "article"):
                el.text = "\n" + (el.text or "")
    text = doc.text_content()
    text = re.sub(r"[ \t\xa0]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


# ---------------------------------------------------------------------------
# fixture capture (``update_refdata.py --save-fixtures DIR``)
# ---------------------------------------------------------------------------
_FIXTURE_DIR: Path | None = None


@contextlib.contextmanager
def saving_fixtures(directory: Path | str | None) -> Iterator[None]:
    """While active, every page a parser reads is also written to
    ``directory/<source>_<YYYYMMDD>.txt`` (see ``save_fixture``)."""
    global _FIXTURE_DIR
    prev = _FIXTURE_DIR
    _FIXTURE_DIR = Path(directory) if directory else None
    try:
        yield
    finally:
        _FIXTURE_DIR = prev


def save_fixture(source: str, text: str) -> Path | None:
    """Write the exact text a parser consumes: the ``html_to_text`` output for
    HTML pages, the raw payload for JSON/CSV sources and for the ECB index
    (whose parser reads hrefs). No-op unless ``saving_fixtures`` is active."""
    if _FIXTURE_DIR is None:
        return None
    _FIXTURE_DIR.mkdir(parents=True, exist_ok=True)
    p = _FIXTURE_DIR / f"{source}_{dt.date.today():%Y%m%d}.txt"
    p.write_text(text, encoding="utf-8")
    return p


def fetch_text(url: str, source: str) -> str:
    """``html_to_text(fetch(url))``, saved as fixture ``source`` when capturing."""
    text = html_to_text(fetch(url))
    save_fixture(source, text)
    return text


def today_iso() -> str:
    return dt.date.today().isoformat()


def dedupe_sorted(dates: Iterable[dt.date]) -> list[dt.date]:
    return sorted(set(dates))
