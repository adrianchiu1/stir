#!/usr/bin/env python
"""M2 gate evidence -> docs/m2_gate.md.

Gate (docs/decisions.md): WIRP comparison on 10 dates within 1bp; drop list reviewed.
For each gate date: builds the EFFR front end from data/ (market CSVs, reference
data), compares implied rates per meeting with AC's WIRP capture
(tests/fixtures/live/wirp_usd_<YYYYMMDD>.txt) and lists the drop list, high-leverage
quotes and the residual summary. A date without market data or without a capture is
reported as waiting. Also: runs on other dates already on file, and the EFFR turn
evidence (D8) from every fixing on file.

    python scripts/m2_gate.py                 # writes docs/m2_gate.md
    python scripts/m2_gate.py --out /tmp/m2_gate.md --exports   # also writes exports/ for each date
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd  # noqa: E402

from stircurve.config.loader import load_config  # noqa: E402
from stircurve.curves.front_end import build  # noqa: E402
from stircurve.marketdata import loader  # noqa: E402
from stircurve.marketdata.dump import MARKET_DIR  # noqa: E402
from stircurve.marketdata.manifest import load_manifest  # noqa: E402
from stircurve.policy.export import write_exports  # noqa: E402
from stircurve.policy.outputs import meeting_table  # noqa: E402
from stircurve.policy.spread import turn_effects  # noqa: E402
from stircurve.quality import battery, wirp  # noqa: E402
from stircurve.refdata.maintenance import load_policy_rates  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
D = dt.date

GATE_DATES = [
    (D(2014, 9, 16), "zero lower bound", "day before the Sep 2014 FOMC; 2015 liftoff priced"),
    (D(2015, 12, 15), "2015-2018 hikes", "day before liftoff (16 Dec 2015)"),
    (D(2018, 9, 25), "2015-2018 hikes", "day before the Sep 2018 hike"),
    (D(2019, 7, 30), "2019 cuts", "day before the first 2019 cut"),
    (D(2020, 3, 3), "Mar 2020 emergency; unscheduled in the window",
     "close of 3 Mar: the unscheduled 50bp cut (decided 3 Mar) takes effect 4 Mar, inside the window; "
     "WIRP still shows the 18 Mar meeting the 15 Mar decision later replaced"),
    (D(2020, 3, 16), "Mar 2020 emergency", "first close after the Sunday 15 Mar cut to 0-0.25 (effective 16 Mar)"),
    (D(2022, 6, 14), "2022-2023 hikes", "day before the first 75bp hike"),
    (D(2023, 7, 25), "2022-2023 hikes", "day before the last hike of the cycle"),
    (D(2024, 9, 17), "2024-2026 cuts", "day before the 50bp cut of 18 Sep 2024"),
    (D(2026, 10, 7), "2024-2026 cuts", "latest dump on file; first meeting 28 Oct 2026"),
]
EXTRA_DATES = [D(2019, 6, 12)]      # other days on file (no WIRP capture asked for)


def md(df: pd.DataFrame | None, cols: list[str] | None = None) -> str:
    return battery._md(df, cols)


def has_market_data(day: D, root: Path = MARKET_DIR) -> bool:
    p = root / "usd" / f"{day.year}" / "ff_fut.csv"
    return p.exists() and any(line.startswith(day.isoformat()) for line in p.read_text().splitlines())


def run_date(day: D, exports: bool) -> tuple[dict, list[str]]:
    status = {"as_of": day, "data": has_market_data(day), "capture": wirp.fixture_path(day).exists()}
    out = [f"### {day}", ""]
    if not status["data"]:
        out += ["Waiting for market data (see the dump commands in the PR / README).", ""]
        return status, out
    fe = build(day)
    if exports:
        write_exports(fe)
    mt = meeting_table(fe)
    sp = fe.spread
    out += [f"{len(fe.used)} quotes, {len(fe.fit.dropped)} dropped, {fe.grid.n} parcels, "
            f"{int(mt['synthetic'].sum())} synthetic and {int((~mt['scheduled']).sum())} unscheduled meetings; "
            f"anchor {fe.anchor_now}; spread "
            + (f"{sp.value * 100:.2f}bp ({sp.n_obs} fixings)" if sp.value is not None else f"none ({sp.note})")
            + (f"; {len(fe.missing_fixings)} past rate dates without a fixing" if fe.missing_fixings else ""), ""]
    if status["capture"]:
        table = wirp.parse_wirp(wirp.fixture_path(day).read_text(encoding="utf-8"))
        cmp_ = wirp.compare(mt, table)
        status.update(meetings=len(cmp_), max_gap=cmp_["diff_bp"].abs().max(), passed=bool(cmp_["ok"].all()))
        out += ["WIRP comparison (implied rate, bp = ours - WIRP):", "", md(cmp_)]
    else:
        out += [f"Waiting for the WIRP capture `{wirp.fixture_path(day).relative_to(ROOT)}`. Front end alone:", "",
                md(mt.head(12), ["decision_date", "effective_date", "synthetic", "scheduled", "implied_rate",
                                 "implied_policy", "step_bp", "cumulative_bp", "moves", "under_identified"])]
    out += ["Drop list:", "", md(battery.drop_list(fe)),
            "High-leverage quotes (>= 0.9):", "", md(battery.high_leverage(fe)),
            "Residuals (bp):", "", md(battery.residual_summary(fe))]
    status["residuals"] = battery.residual_summary(fe)
    return status, out


def turn_section() -> list[str]:
    m = load_manifest("usd")
    frame, _ = loader.load(m)
    fx = frame[(frame["instrument"] == "EFFR") & (frame["field"] == "PX_LAST")].set_index("date")["value"]
    out = ["## EFFR turn evidence (D8: does EFFR need a turn node?)", "",
           f"Fixings on file: {len(fx)}" + (f" ({fx.index.min():%Y-%m-%d}..{fx.index.max():%Y-%m-%d})" if len(fx) else ""), ""]
    if len(fx) < 250:
        out += ["Not enough EFFR history on file to measure month/quarter/year-end effects (needs the fixings dump "
                "from 2010). Method (`stircurve.policy.spread.turn_effects`): each month-end business day's "
                "EFFR - target midpoint, minus the median of the 10 non-turn business days before it; "
                "per year and turn kind, plus the business day after. A turn node is warranted if the effect "
                "is persistent and larger than the FF quote noise (0.5bp) once averaged into a monthly contract.", ""]
        return out
    cal = m.calendar("us_fed")
    t = turn_effects(fx, load_policy_rates("fed"), "target_midpoint", cal)
    out += [md(t), ""]
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=ROOT / "docs" / "m2_gate.md")
    ap.add_argument("--exports", action="store_true", help="also write exports/usd/effr/<as_of>/ for each date")
    args = ap.parse_args(argv)
    cfg = load_config("usd")
    statuses, sections = [], []
    for day, regime, why in GATE_DATES:
        st, sec = run_date(day, args.exports)
        st.update(regime=regime, why=why)
        statuses.append(st)
        sections += sec
    extra = []
    for day in EXTRA_DATES:
        st, sec = run_date(day, args.exports)
        extra += sec

    compared = [s for s in statuses if "passed" in s]
    passed = [s for s in compared if s["passed"]]
    n_data = sum(s["data"] for s in statuses)
    n_cap = sum(s["capture"] for s in statuses)
    fe_cfg = cfg["front_end"]
    rows = []
    for s in statuses:
        res = ("✔" if s.get("passed") else "✘") if "passed" in s else "⏳"
        rows.append({"As-of": s["as_of"], "Regime": s["regime"], "Why": s["why"],
                     "Market data": "✔" if s["data"] else "⏳", "WIRP capture": "✔" if s["capture"] else "⏳",
                     "Meetings": s.get("meetings", ""),
                     "Max |gap| bp": f"{s['max_gap']:.2f}" if "max_gap" in s else "", "Within 1bp": res})
    lines = [
        "# M2 gate: USD EFFR front end", "",
        "Generated by `python scripts/m2_gate.py` from `data/` (market CSVs, reference data) and AC's WIRP captures "
        "in `tests/fixtures/live`. Gate: *WIRP comparison on 10 dates within 1bp; drop list reviewed.*", "",
        "## Status", "",
        "| Gate item | Status |", "| --- | --- |",
        f"| WIRP comparison on 10 dates within 1bp | {len(passed)}/{len(GATE_DATES)} dates within 1bp on every meeting; "
        f"{len(compared)} compared; market data on file for {n_data}/10, WIRP captures {n_cap}/10 |",
        "| Drop list reviewed | ⏳ AC (per date below) |",
        f"| Settings | horizon {fe_cfg['horizon_years']}y; Huber k {fe_cfg['fit']['huber_k']}; quote sigma "
        f"{fe_cfg['fit']['quote_sigma_bp']}bp; prior sigma {fe_cfg['fit']['prior_sigma_bp']}bp; drop below Huber "
        f"weight {fe_cfg['fit']['drop_weight']}; spread {fe_cfg['spread']['estimator']} {fe_cfg['spread']['winsor']} "
        f"over {fe_cfg['spread']['window_bd']}bd, turns {fe_cfg['spread']['turn_days']} (usd.yaml `front_end`) |",
        "",
        "## Gate dates", "", md(pd.DataFrame(rows)),
        "Implied rate = fitted EFFR of the parcel the meeting opens (flat forwards between effective dates). "
        "A miss is explained as one of: effective-date convention, synthetic meeting, spread choice, data "
        "(stale, thin, missing fixings), or a meeting WIRP shows that the reference data does not hold.", "",
        "## Per date", "",
    ] + sections + ["## Other dates on file", ""] + extra + turn_section()
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {args.out}: {len(passed)}/{len(GATE_DATES)} within 1bp, {len(compared)} compared, "
          f"data {n_data}/10, captures {n_cap}/10")
    return 0


if __name__ == "__main__":
    sys.exit(main())
