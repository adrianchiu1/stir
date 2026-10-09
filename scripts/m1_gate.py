#!/usr/bin/env python
"""Write docs/m1_gate.md (and docs/m1_gate_contracts.csv): the M1 gate evidence.

Gate: "One day of USD data loads with zero unknown columns; windows match
exchange calendars."

* Rule sources: every manifest rule, its source and whether its quoted passage
  was found in the live capture.
* Listing model vs the exchange filings (CBOT 20-321, CME 22-199).
* Generated windows for 2010-2027 FF, 2018-2027 SR1/SR3, 2010-2023 ED (CSV), and
  every contract where the calendar choice moves a date (the open questions).
* Exchange-calendar comparison: CME calendar captures, when present.
* Loader report on the real dumped days, when present.

    python scripts/m1_gate.py
"""
from __future__ import annotations

import dataclasses
import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from stircurve.marketdata import loader, sources  # noqa: E402
from stircurve.marketdata.contracts import contract_table, listed_contracts  # noqa: E402
from stircurve.marketdata.manifest import load_manifest, normalise, quotes  # noqa: E402

D = dt.date
RANGES = {"ff_fut": (2010, 2027), "sofr1m_fut": (2018, 2027), "sofr3m_fut": (2018, 2027), "ed_fut": (2010, 2023)}
GATE_DAYS = [D(2026, 10, 7), D(2019, 6, 12)]
DOC = ROOT / "docs" / "m1_gate.md"
CSV = ROOT / "docs" / "m1_gate_contracts.csv"


def _wd(d) -> str:
    return f"{d:%a} {d.isoformat()}" if d else "—"


def rule_table(m) -> list[str]:
    out = ["| Rule | Source | Status |", "| --- | --- | --- |"]
    for path, sid, quote in quotes(m):
        src = m.sources[sid]
        f = sources.latest_fixture(src["fixture"]) if src.get("fixture") else None
        ok = f is not None and normalise(quote) in normalise(f.read_text(encoding="utf-8"))
        out.append(f"| `{path}` | [{sid}]({src['url']}) | {'✔ quoted passage found in `' + f.name + '`' if ok else '✘ not found'} |")
    for sid, paths in sources.pending(m).items():
        src = m.sources[sid]
        out.append(f"| {', '.join(f'`{p}`' for p in paths)} | [{sid}]({src['url']}) | ⏳ {src.get('status')} |")
    return out


def listed_on(m, ins, day):
    return sorted(c.contract for c in listed_contracts(m, ins, day) if c.first_listed <= day <= c.last_trade)


def listing_checks(m) -> list[str]:
    ff_a, ff_b = listed_on(m, "ff_fut", D(2020, 9, 18)), listed_on(m, "ff_fut", D(2020, 9, 21))
    sr3 = listed_on(m, "sofr3m_fut", D(2022, 7, 25))
    q = [c for c in sr3 if int(c[5:]) % 3 == 0]
    s = [c for c in sr3 if int(c[5:]) % 3]
    return [
        "| Filing says | Generated | Match |", "| --- | --- | --- |",
        f"| FF: 36 consecutive months before 21 Sep 2020 (CBOT 20-321) | {len(ff_a)} listed on Fri 2020-09-18 ({ff_a[0]}..{ff_a[-1]}) | {'✔' if len(ff_a) == 36 else '✘'} |",
        f"| FF: 60 consecutive months from trade date 21 Sep 2020 | {len(ff_b)} listed on Mon 2020-09-21 ({ff_b[0]}..{ff_b[-1]}) | {'✔' if len(ff_b) == 60 else '✘'} |",
        f"| SR3 on 25 Jul 2022: quarterly June 2022 through June 2032 (CME 22-199) | {len(q)} quarterly, {q[0]}..{q[-1]} | {'✔' if (len(q), q[0], q[-1]) == (41, '2022-06', '2032-06') else '✘'} |",
        f"| SR3 on 25 Jul 2022: nearest serial months August 2022 through January 2023 | {', '.join(s)} | {'✔' if s == ['2022-08', '2022-10', '2022-11', '2023-01'] else '✘'} |",
    ]


def calendar_sensitive(m) -> list[str]:
    """Contracts where a holiday moves a date away from the plain rule."""
    rows = ["| Instrument | Contract | Ticker | Window [start, end) | Last trade | Final settlement | Why |",
            "| --- | --- | --- | --- | --- | --- | --- |"]
    sifma, sofr = m.calendar("us_sifma"), m.calendar("us_sofr")
    for ins, (a, b) in RANGES.items():
        t = contract_table(m, D(a, 1, 1), D(b, 12, 31), [ins])
        for r in t.itertuples():
            why = []
            if ins in ("ff_fut", "sofr1m_fut") and sifma.previous_business_day(r.ref_end) != r.last_trade:
                why.append("Good Friday month-end: SIFMA closed, last trade on the us_fed day (AC, PR #2)")
            if ins == "sofr3m_fut":
                why += [f"Reference Quarter {label} on a non-SOFR day ({_wd(d)})"
                        for label, d in (("starts", r.ref_start), ("ends", r.ref_end)) if not sofr.is_business_day(d)]
            if ins == "ed_fut" and r.ref_start - dt.timedelta(days=2) != r.last_trade:
                why.append("London holiday: not the Monday before the IMM date")
            if why:
                rows.append(f"| {ins} | {r.contract} | {r.bbg_ticker} | {r.ref_start}–{r.ref_end} | {_wd(r.last_trade)} | "
                            f"{_wd(r.final_settlement)} | {'; '.join(why)} |")
    return rows


def sample_windows(m) -> list[str]:
    rows = ["| Instrument | Contract | Ticker | Start (incl.) | End (excl.) | Days | Last trade | Final settlement | First listed | Last quote |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    picks = {"ff_fut": ["2010-01", "2015-12", "2018-03", "2024-03", "2026-10", "2027-12"],
             "sofr1m_fut": ["2018-05", "2020-03", "2024-03", "2026-10", "2027-12"],
             "sofr3m_fut": ["2018-06", "2022-08", "2023-12", "2024-03", "2026-09", "2027-12"],
             "ed_fut": ["2010-03", "2016-12", "2019-06", "2023-03", "2023-06", "2023-09"]}
    for ins, cs in picks.items():
        a, b = RANGES[ins]
        t = contract_table(m, D(a, 1, 1), D(b, 12, 31), [ins]).set_index("contract")
        for c in cs:
            r = t.loc[c]
            conv = f" (converted {r.converted_on})" if r.converted_on else ""
            lb = " (lower bound)" if r.first_listed_lower_bound else ""
            rows.append(f"| {ins} | {c} | {r.bbg_ticker} | {r.ref_start} | {r.ref_end} | {r.accrual_days} | {_wd(r.last_trade)} | "
                        f"{_wd(r.final_settlement)} | {r.first_listed}{lb} | {r.last_quote}{conv} |")
    return rows


def exchange_comparison(m) -> list[str]:
    caps = sorted(sources.LIVE_FIXTURES.glob("cme_*_[0-9]*.txt"))
    if not caps:
        return ["No CME calendar captures yet: cmegroup.com refuses scripted access (HTTP 403, \"This IP address is",
                "blocked due to suspected web scraping\") and its terms of use forbid it. Save the four calendar pages",
                "from a browser and convert them (README, M1 section); the comparison parser is written against the",
                "first real capture, as for every M0 parser. Until then the generated windows rest on the rule text",
                "above and the full table is in `docs/m1_gate_contracts.csv` for a side-by-side check."]
    return [f"Captured: {', '.join(p.name for p in caps)} (comparison parser pending its first fixture)."]


def loader_section(m) -> list[str]:
    out = []
    for day in GATE_DAYS:
        frame, rep = loader.load(m, day, day)
        if not rep.values:
            state = ("Dumped, but the files hold no rows (every Bloomberg request failed and the old dump wrote "
                     "headers only). Re-run on the terminal machine:" if rep.files else "Not dumped yet. On the terminal machine:")
            out += [f"### {day}", "", state, "", "```",
                    f"python scripts/dump_bloomberg.py --start {day} --end {day}            # dry run",
                    f"python scripts/dump_bloomberg.py --start {day} --end {day} --write-csv",
                    f"python scripts/check_market_data.py --start {day} --end {day}", "```", ""]
            continue
        out += [f"### {day}", "", "```", rep.report(), "```", "",
                f"Unknown columns: **{len(rep.found['unknown_columns'])}**; tidy rows: {len(frame)}.", ""]
    return out


def main() -> int:
    m = load_manifest("usd")
    tables = [contract_table(m, D(a, 1, 1), D(b, 12, 31), [ins]) for ins, (a, b) in RANGES.items()]
    import pandas as pd
    full = pd.concat(tables, ignore_index=True)
    full.to_csv(CSV, index=False, lineterminator="\n")
    counts = full.groupby("instrument").size()
    lines = [
        "# M1 gate: USD market data",
        "",
        "Generated by `python scripts/m1_gate.py` from the manifest (`stircurve/config/usd_manifest.yaml`),",
        "the committed calendars and the captures in `tests/fixtures/live`. Gate: *one day of USD data loads",
        "with zero unknown columns; windows match exchange calendars.*",
        "",
        "## Status",
        "",
        "| Gate item | Status |",
        "| --- | --- |",
        "| Windows: FF, ED, SR3 reference quarter and contract naming, FF/SR3 listing schedules | ✔ rule text captured live (cftc.gov filings) and quoted in the manifest |",
        "| Windows: SR3 last trade, SR1 (all rules), ED conversion | ⏳ CME pages only; cmegroup.com blocks scripted access |",
        "| Windows vs CME published calendars (dates) | ⏳ needs a browser capture of the CME calendar pages |",
        "| One real day loads with zero unknown columns | ⏳ needs AC's dump (commands below) |",
        "",
        "## Rule sources",
        "",
        *rule_table(m),
        "",
        "## Listing model vs the exchange filings",
        "",
        *listing_checks(m),
        "",
        "## Generated windows",
        "",
        f"Full table (`docs/m1_gate_contracts.csv`): " + ", ".join(f"{k} {v}" for k, v in counts.items())
        + " contracts (FF 2010-2027, SR1/SR3 2018-2027, ED 2010-2023, each counted if quoted in its range).",
        "Windows are [start, end); last trade and final settlement on the manifest calendars.",
        "",
        *sample_windows(m),
        "",
        "### Contracts where a holiday moves a date",
        "",
        "Exchange business days are `us_fed` (AC, PR #2). SR3 Reference Quarters keep their IMM boundaries when",
        "the IMM date is not a SOFR day (Juneteenth 2024 and 2030; open in the PR).",
        "",
        *calendar_sensitive(m),
        "",
        "## Windows vs the exchange's published calendars",
        "",
        *exchange_comparison(m),
        "",
        "## Loader report on real days",
        "",
        *loader_section(m),
    ]
    DOC.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {DOC.relative_to(ROOT)} and {CSV.relative_to(ROOT)} ({len(full)} contracts)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
