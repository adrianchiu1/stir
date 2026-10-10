#!/usr/bin/env python
"""M2 gate evidence -> docs/m2_gate.md.

Gate (docs/decisions.md): WIRP comparison on 10 dates within 1bp; drop list reviewed.
For each gate date and each curve (FF futures, EFFR OIS), from data/ (market CSVs,
reference data) and AC's WIRP captures (tests/fixtures/live/wirp_us_<fut|ois>_<YYYYMMDD>.txt):

1. the replica of WIRP's own model against the capture (data, conventions, calendars),
2. our estimator against the replica (what the extra quotes and the prior change),
3. our estimator against the capture; plus the FF/OIS basis, the drop list, high-leverage
   quotes and the residual summary. A date without market data or without a capture is
   reported as waiting. Also: other dates on file, and the EFFR turn evidence (D-F) from
   every fixing on file.

    python scripts/m2_gate.py                 # writes docs/m2_gate.md
    python scripts/m2_gate.py --out /tmp/m2_gate.md --exports   # also writes exports/ for each date
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from stircurve.config.loader import load_config  # noqa: E402
from stircurve.curves.front_end import build  # noqa: E402
from stircurve.marketdata import loader  # noqa: E402
from stircurve.marketdata.dump import MARKET_DIR  # noqa: E402
from stircurve.marketdata.manifest import load_manifest  # noqa: E402
from stircurve.policy.export import write_exports  # noqa: E402
from stircurve.policy.outputs import basis_table, curve_meeting_rows  # noqa: E402
from stircurve.policy.spread import turn_effects  # noqa: E402
from stircurve.quality import battery, wirp  # noqa: E402
from stircurve.refdata.maintenance import load_policy_rates  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
D = dt.date

GATE_DATES = [
    (D(2014, 9, 16), "zero lower bound", "day before the Sep 2014 FOMC; 2015 lift-off priced"),
    (D(2015, 12, 15), "2015-2018 hikes", "day before lift-off (16 Dec 2015)"),
    (D(2018, 9, 25), "2015-2018 hikes", "day before the Sep 2018 hike"),
    (D(2019, 7, 30), "2019 cuts", "day before the first 2019 cut"),
    (D(2020, 3, 3), "Mar 2020 emergency; unscheduled in the window",
     "close of 3 Mar: the unscheduled 50bp cut (decided 3 Mar) takes effect 4 Mar, a known step inside the window; "
     "the 18 Mar meeting is still in force (superseded on 15 Mar)"),
    (D(2020, 3, 16), "Mar 2020 emergency", "first close after the Sunday 15 Mar cut to 0-0.25 (effective 16 Mar)"),
    (D(2022, 6, 14), "2022-2023 hikes", "day before the first 75bp hike"),
    (D(2023, 7, 25), "2022-2023 hikes", "day before the last hike of the cycle"),
    (D(2024, 9, 17), "2024-2026 cuts", "day before the 50bp cut of 18 Sep 2024"),
    (D(2026, 10, 7), "2024-2026 cuts", "latest dump on file; first meeting 28 Oct 2026"),
]
EXTRA_DATES = [D(2019, 6, 12)]      # other days on file (no WIRP capture asked for)


def md(df, cols=None) -> str:
    return battery._md(df, cols)


def has_market_data(day: D, root: Path = MARKET_DIR) -> bool:
    p = root / "usd" / f"{day.year}" / "ff_fut.csv"
    return p.exists() and any(line.startswith(day.isoformat()) for line in p.read_text().splitlines())


def run_date(day: D, exports: bool) -> tuple[dict, list[str]]:
    status = {"as_of": day, "data": has_market_data(day), "captures": {}}
    out = [f"### {day}", ""]
    if not status["data"]:
        out += ["Waiting for market data (see the dump commands in the PR / README).", ""]
        return status, out
    fe = build(day)
    if exports:
        write_exports(fe)
    sp = fe.spread
    out += [f"Anchor {fe.anchor_now}; spread " + (f"{sp.value * 100:.2f}bp ({sp.n_obs} fixings)" if sp.value is not None
                                                 else f"none ({sp.note})") + ".", ""]
    for c in fe.curves.values():
        model = fe.cfg["front_end"]["curves"][c.name]["wirp_model"]
        cap = wirp.load_capture(day, model)
        status["captures"][c.name] = cap is not None
        mt = pd.DataFrame(curve_meeting_rows(fe, c))
        out += [f"#### `{c.name}` ({', '.join(c.instruments)}; WIRP model: {model})", "",
                f"{len(c.used)} quotes used, {len(c.dropped)} dropped, {len(c.excluded)} excluded (metadata); "
                f"replica on {len(c.replica.used)} quotes reaches {c.wirp_reach} meetings; "
                f"current implied O/N: fit {c.curve.rates[0]:.4f}, replica {c.replica.rates[0]:.4f}"
                + (f"; {len(c.missing_fixings)} past rate dates without a fixing" if c.missing_fixings else "") + ".", ""]
        if cap is not None:
            cmp_ = wirp.compare(mt, cap, float(c.curve.rates[0]), float(c.replica.rates[0]))
            rows = cmp_[cmp_["meeting"] != "current"]
            status[c.name] = {"meetings": len(rows),
                              "replica_max": rows["replica_minus_wirp_bp"].abs().max(),
                              "fit_max": rows["fit_minus_wirp_bp"].abs().max(),
                              "replica_pass": bool(rows["replica_ok"].all()), "fit_pass": bool(rows["fit_ok"].all())}
            out += [f"WIRP capture `{wirp.fixture_path(day, model).name}` (pricing date {cap.pricing_date}, "
                    f"current implied {cap.current_implied}). Gaps in bp:", "", md(cmp_)]
        else:
            out += [f"Waiting for the WIRP capture `{wirp.fixture_path(day, model).name}`. Fit and replica alone:", "",
                    md(mt.head(14), ["decision_date", "synthetic", "unscheduled", "implied_rate", "n_moves", "pct_move",
                                     "replica_rate", "fit_minus_replica_bp", "under_identified", "beyond_wirp_reach"])]
        out += ["Drop list:", "", md(battery.drop_list(fe, c)),
                "High-leverage quotes:", "", md(battery.high_leverage(fe, c)),
                "Residuals (bp):", "", md(battery.residual_summary(fe, c)), ""]
    out += ["FF / OIS basis (bp, fit and replica):", "", md(basis_table(fe), ["decision_date", "parcel", "basis_fit_bp",
                                                                              "basis_replica_bp"]), ""]
    return status, out


def turn_section() -> list[str]:
    m = load_manifest("usd")
    frame, _ = loader.load(m)
    fx = frame[(frame["instrument"] == "EFFR") & (frame["field"] == "PX_LAST")].set_index("date")["value"]
    out = ["## EFFR month-end evidence (D-F: a fixing effect, never a node; switchable adjustment in the FF model)", "",
           f"Fixings on file: {len(fx)}" + (f" ({fx.index.min():%Y-%m-%d}..{fx.index.max():%Y-%m-%d})" if len(fx) else ""), ""]
    if len(fx) < 250:
        out += ["Not enough EFFR history on file to measure month/quarter/year-end effects (needs the fixings dump "
                "from 2010). Method (`stircurve.policy.spread.turn_effects`): each month-end business day's "
                "EFFR - target midpoint, minus the median of the 10 non-turn business days before it; per year and "
                "turn kind, plus the business day after. The adjustment (`front_end.month_end_adjustment`) stays off "
                "until the effect is measured, and off for the WIRP gate because WIRP makes none.", ""]
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
    curves = list(cfg["front_end"]["curves"])
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

    def cell(st, name, key):
        r = st.get(name)
        if r is None:
            return "⏳"
        return ("✔" if r[key + "_pass"] else "✘") + f" {r[key + '_max']:.2f}"

    n_data = sum(s["data"] for s in statuses)
    n_cap = sum(all(s["captures"].get(c, False) for c in curves) for s in statuses)
    passed = {c: sum(1 for s in statuses if s.get(c, {}).get("replica_pass") and s[c].get("fit_pass")) for c in curves}
    rows = []
    for s in statuses:
        row = {"As-of": s["as_of"], "Regime": s["regime"], "Market data": "✔" if s["data"] else "⏳"}
        for c in curves:
            row[f"{c}: replica vs WIRP (max |bp|)"] = cell(s, c, "replica")
            row[f"{c}: fit vs WIRP (max |bp|)"] = cell(s, c, "fit")
        rows.append(row)
    fe_cfg = cfg["front_end"]
    lines = [
        "# M2 gate: USD EFFR front end", "",
        "Generated by `python scripts/m2_gate.py` from `data/` (market CSVs, reference data) and AC's WIRP captures "
        "in `tests/fixtures/live`. Gate: *WIRP comparison on 10 dates within 1bp; drop list reviewed.* Two curves per "
        "date (FF futures, EFFR OIS; separate instruments, AC) each against its own WIRP model; three layers: the "
        "replica of WIRP's model vs the capture, our fit vs the replica, our fit vs the capture.", "",
        "## Status", "",
        "| Gate item | Status |", "| --- | --- |",
        f"| WIRP comparison on 10 dates within 1bp | market data on file for {n_data}/10 dates; captures for both models "
        f"on {n_cap}/10; within 1bp (replica and fit, every meeting): "
        + ", ".join(f"{c} {passed[c]}/10" for c in curves) + " |",
        "| Drop list reviewed | ⏳ AC (per date below) |",
        f"| Settings | horizon {fe_cfg['horizon_years']}y; Huber k {fe_cfg['fit']['huber_k']}; quote sigma "
        f"{fe_cfg['fit']['quote_sigma_bp']}bp; step prior sigma {fe_cfg['fit']['step_prior_sigma_bp']}bp; stub prior "
        f"sigma {fe_cfg['fit']['stub_prior_sigma_bp']}bp; drop below Huber weight {fe_cfg['fit']['drop_weight']}; FF "
        f"liquidity {fe_cfg['fit']['liquidity']['ff_fut']}; spread {fe_cfg['spread']['estimator']} "
        f"{fe_cfg['spread']['winsor']} over {fe_cfg['spread']['window_bd']}bd, turns {fe_cfg['spread']['turn_days']}; "
        f"month-end adjustment {'on' if fe_cfg['month_end_adjustment']['enabled'] else 'off'} (usd.yaml `front_end`) |",
        "",
        "## Gate dates", "", md(pd.DataFrame(rows)),
        "Implied rate = the overnight rate of the parcel the meeting opens (flat forwards between effective dates), "
        "compared with WIRP's Post-Meeting Implied Rate. A miss is explained as one of: price snapshot/timing, "
        "convention or calendar, synthetic or unscheduled meeting, a meeting beyond the replica's reach, a "
        "prior-driven parcel, a named quote the fit and the replica treat differently, or a meeting WIRP shows "
        "that the reference data does not hold.", "",
        "## Per date", "",
    ] + sections + ["## Other dates on file", ""] + extra + turn_section()
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {args.out}: data {n_data}/10, captures {n_cap}/10, within 1bp: "
          + ", ".join(f"{c} {passed[c]}/10" for c in curves))
    return 0


if __name__ == "__main__":
    sys.exit(main())
