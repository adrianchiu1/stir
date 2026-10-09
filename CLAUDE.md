# CLAUDE.md — working rules for this repo

Read `docs/decisions.md` and `README.md` before changing anything. The design
spec (a Claude Doc, exported to `docs/spec.md` when updated) is the authority;
if the spec and the code disagree, the spec wins and the code gets a fix.

## What this is
A team tool that prices every upcoming central-bank meeting from STIR futures
and OIS and builds the RFR/IBOR zero curves behind them (Fed, ECB, BoE, BoJ;
daily history from 2010). Owner: AC. Users: AC's team, via Jupyter notebooks.

## Hard rules
- No AI and no Bloomberg calls at runtime. The curve code reads CSVs under
  `data/` only. Bloomberg pulls happen in `scripts/dump_bloomberg.py` via
  pdblp (one session, bad securities skipped; `--backend pxts` for
  `pxts.read_bdh`; AC, PR #2) on a terminal machine; reference-data pulls happen in
  `scripts/update_refdata.py` on a machine with internet. Both write files.
- Committed CSVs under `data/refdata/` are the source of truth. Updaters diff
  and never overwrite silently; a blocking diff exits 2. Never hand-edit a
  committed reference file without a `source_url`.
- Every instrument is a window + accrual rule + day count + calendar + quote
  convention. Never hard-code ACT/360 or IMM; the next 18 currencies include
  ACT/365 bills and BUS/252 (BRL).
- Synthetic (cadence-extrapolated) meetings are flagged everywhere they appear.
- Curve store (`data/curves/`) is local and git-ignored; `exports/` is shared.
- Quotes are mids (no bid/ask); no option vols (convexity σ from realised vol,
  strip-implied cross-check).

## How to work
- One milestone per branch (`m1-usd-market-data`), one PR per milestone, tests
  green before review. Milestones and gates: `docs/decisions.md` → Build plan.
- Bite-size commits; raise a question in the PR rather than guessing when a
  convention is unclear. AC answers in the PR.
- Tests: `python scripts/run_tests.py` (or `pytest`). Add a fixture under
  `tests/fixtures/` for every parser change; fixtures are text captured from
  the live page, not hand-written.
- Python ≥ 3.10, pandas, numpy, scipy, QuantLib optional (cross-checks only).

## Layout
`stircurve/config` YAML per currency · `stircurve/refdata` calendars, meetings,
maintenance periods, policy rates, parsers, updater · `stircurve/marketdata`
manifest + CSV loaders (M1) · `instruments`, `curves`, `convexity`, `policy`,
`quality`, `store`, `viz` (M2+) · `scripts/` CLIs · `notebooks/` parameter
cells only · `tests/`.
