# stir-policy-pricing

Meeting-date aware STIR / OIS curve construction for central-bank policy pricing
(Fed, ECB, BoE, BoJ first; built so the next 18 currencies fit). Design spec and
decision log live in the team doc *STIR Policy-Pricing Tool — Design Spec v0.1*.

**Status: M0 (parts 1 and 2).** Reference data layer only: business-day calendars,
meeting schedules with effective-date rules and cadence extrapolation, ECB
reserve maintenance periods, policy-rate histories for all four banks,
deterministic updaters and tests. No curve code yet. Nothing here calls Bloomberg or any AI service.

## Layout

```
stircurve/            package (config/, refdata/ live; other modules are stubs for M1+)
data/refdata/         committed reference data (CSV) — the source of truth at runtime
  holidays/           us_fed, us_sifma, target, uk, jp  (rules, overridden by official sources)
  meetings/           <bank>.csv, <bank>_unscheduled.csv
  maintenance_periods/ecb.csv
  policy_rates/       <bank>.csv with a confidence column (primary | derived | memory:<how to verify>)
data/market/          Bloomberg CSV dumps written by pxts (M1)
data/curves/          local parquet store, git-ignored
exports/              analytics shared with the team
scripts/              update_refdata.py, run_tests.py
tests/                fixtures captured from the central-bank pages on 8 Oct 2026
```

## Install

```
pip install -e .[dev]            # core: pandas, numpy, scipy, pyyaml, requests, lxml
pip install -e .[quantlib]       # optional cross-checks
pip install -e .[bloomberg,plot] # pxts for dumps and charts (M1+)
```

## Reference data: how it is kept current

The committed CSVs are what the curve code reads. Updaters refresh them from
public sources on a machine with outbound internet and never write silently:

```
python scripts/update_refdata.py --bank fed --dry-run               # diff only
python scripts/update_refdata.py --bank fed --historical 2010-2020 --commit
python scripts/update_refdata.py --ecb-maintenance --years 2010-2027 --commit
python scripts/update_refdata.py --bank ecb --commit                 # ECB meetings come from the MP tables
python scripts/update_refdata.py --bank boe --bank boj --dry-run     # validate these parsers on first run
python scripts/update_refdata.py --holidays uk jp us_sifma --commit
```

A run exits with code 2 and writes nothing if the diff removes a row, changes
a past date, or fails validation (e.g. non-contiguous maintenance periods).

Sources: Fed FOMC calendar pages; ECB "indicative operational calendars"
press releases (index page links every year back to 1999); BoE upcoming MPC
dates page; BoJ MPM schedule page; gov.uk bank-holidays JSON; Japan Cabinet
Office holiday CSV; SIFMA holiday schedule; TARGET and US federal holidays by rule.

## Effective-date rules

| Bank | Rule | Notes |
| --- | --- | --- |
| Fed | decision + 1 `us_fed` business day | |
| ECB | start of the maintenance period attached to the meeting | published table wins; Wednesday-after rule is the fallback for synthetic meetings |
| BoE | decision date | |
| BoJ | next `jp` business day | confirmed: 2024-03-19→21 Mar (20 Mar holiday), 2025-12-19→22 Dec, 2026-06-16→17 Jun |

## Cadence extrapolation

Beyond the last published meeting, synthetic meetings out to as-of + 3y
replicate the (month, ordinal weekday, weekday) slots of the latest fully
published year, rolled to the next business day if they land on a holiday.
They are flagged `synthetic` everywhere. The Fed test shows the limit of the
idea: the May 2025 slot became 29 April 2026, one week and one month away.

## Tests

```
python scripts/run_tests.py      # or: pytest
```

## Seeded data (8 Oct 2026)

* `meetings/fed.csv`: 2021–2027 scheduled meetings from the Fed calendar page;
  2020 unscheduled cuts in `fed_unscheduled.csv`. 2010–2020 come from
  `--historical 2010-2020`.
* `maintenance_periods/ecb.csv` and `meetings/ecb.csv`: MP 8/2026 and 1–8/2027
  from the 30 Jun 2026 press release. Earlier years come from `--ecb-maintenance`.
* `meetings/boe.csv`, `meetings/boj.csv`: headers only; first updater run fills them.
* Holidays: rule-generated 2005–2035; `--holidays` overlays the official sources.
* Policy rates: Fed target range 2008–2026 from the Fed's open-market table (IORB derived as top−10bp
  from Mar 2022; IOER 2010–21 from memory until `--policy-rates fed` pulls FRED); ECB 2019–2026 from the
  key-rates table (2009–2016 rows from memory, confidence `memory`, confirmed on the first `--policy-rates ecb`
  run); BoE 2009–2025 from the Bank Rate database; BoJ from the Statements on Monetary Policy.

See `CLAUDE.md` for working rules and `docs/decisions.md` for the decision log and build plan.
