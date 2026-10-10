# stir-policy-pricing

Meeting-date aware STIR / OIS curve construction for central-bank policy pricing
(Fed, ECB, BoE, BoJ first; built so the next 18 currencies fit). Design spec and
decision log live in the team doc *STIR Policy-Pricing Tool — Design Spec v0.1*.

**Status: M2 in progress (USD EFFR front end) on top of M1 (USD market data) and M0 (reference data).** M0: business-day
calendars, meeting schedules with effective-date rules and cadence extrapolation, ECB
reserve maintenance periods, policy-rate histories for all four banks, deterministic
updaters and tests. M1: USD market-data manifest, contract-table generator, Bloomberg
dump script and CSV loader/validator (see below). No curve code yet. Nothing in the
package calls Bloomberg or any AI service at runtime; `scripts/dump_bloomberg.py` is the
only Bloomberg caller and runs on a terminal machine.

## Layout

```
stircurve/            package (config/, refdata/, marketdata/, instruments/, curves/, policy/, quality/ live)
data/refdata/         committed reference data (CSV) — the source of truth at runtime
  holidays/           us_fed, us_sifma, target, uk, jp  (rules, overridden by official sources)
  meetings/           <bank>.csv, <bank>_unscheduled.csv
  maintenance_periods/ecb.csv
  policy_rates/       <bank>.csv with a confidence column (primary | derived | memory:<how to verify>)
data/market/usd/<YYYY>/<group>.csv  Bloomberg dumps (M1): one column per <ticker>|<field>
data/curves/          local parquet store, git-ignored
exports/<ccy>/<family>/<as_of>/  analytics shared with the team (M2: meetings, parcels, instruments, basis, report)
scripts/              update_refdata.py, run_tests.py, dump_bloomberg.py, check_market_data.py,
                      contract_table.py, capture_exchange_specs.py, front_end.py, m0_gate.py, m1_gate.py, m2_gate.py
tests/                fixtures/live: pages captured by --save-fixtures on 8 Oct 2026
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
python scripts/update_refdata.py --bank boe --dry-run --save-fixtures tests/fixtures/live
python scripts/update_refdata.py --bank fed --historical 2010-2020 --commit
python scripts/update_refdata.py --ecb-maintenance --years 2010-2027 --commit
python scripts/update_refdata.py --bank ecb --commit                 # ECB meetings come from the MP tables
python scripts/update_refdata.py --bank boe --bank boj --dry-run     # validate these parsers on first run
python scripts/update_refdata.py --holidays uk jp us_sifma us_sofr --commit
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
| Fed | decision + 1 `us_fed` business day; before 2009 the decision day (D18) | decision = statement date (2020-03-03, meeting 2–3 Mar) |
| ECB | start of the maintenance period attached to the meeting | published table wins; Wednesday-after rule is the fallback for synthetic meetings |
| BoE | decision date | |
| BoJ | next `jp` business day; before 19 Mar 2024 the decision day (D18) | confirmed: 2024-03-19→21 Mar (20 Mar holiday), 2025-12-19→22 Dec, 2026-06-16→17 Jun; published: 2016-01-29→16 Feb |

For every bank a published implementation date wins over the rule: the ECB maintenance-period
table, and `meetings/published_effective.csv` (one row per decision, with `source_url`).

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

## Reference data after the first live run (8 Oct 2026)

Every published decision date is included (AC, PR #1):

* Fed 1994–2027: FOMC meetings and every conference call / unscheduled meeting from the
  historical pages; a call announced the next day takes the announcement date (21 Jan 2008
  call -> 22 Jan cut). Target 1982+ (FRED DFEDTAR, then the open-market table).
* ECB Mar 2004–2028 from every maintenance-table release; 8 Oct 2008 coordinated cut unscheduled.
* BoE Jun 1997–2027 from the MPC voting-history workbook and the dates page; special meetings
  (18 Sep 2001, 8 Oct 2008, 11 and 19 Mar 2020) in `boe_unscheduled.csv`.
* BoJ Jan 1998–2027 from the minutes indexes and schedule pages; nine unscheduled meetings,
  each named so in its minutes, in `boj_unscheduled.csv`. Policy rates 1998–2026 from the
  statements (call-rate target, complementary deposit facility, policy-rate balance rate) and
  the basic loan rate CSV; new meetings are read by `--policy-rates boj`.
* Published implementation dates win over the rules (D16): the ECB maintenance table,
  policy-rate change dates (Fed target changes took effect on the decision day until 2008;
  BoJ changes 'effective immediately' 2006–2010), and `meetings/published_effective.csv`.
* Calendars from 1994. `us_sifma` = SIFMA full closes (SIFMA archive 2015+); `us_sofr` = days
  without a SOFR publication (= us_sifma + every Good Friday; matches the NY Fed record).
* No `memory` policy-rate rows remain.
* `docs/m0_gate.md` (`python scripts/m0_gate.py`): effective-date spot checks for the M0 gate.

`--save-fixtures DIR` writes the text of every fetched page to `DIR/<source>_<YYYYMMDD>.txt`;
`tests/fixtures/live` holds the 8 Oct 2026 capture and `tests/test_live_fixtures.py` pins
each parser's row count on it.

## M1: USD market data

| Piece | What it does |
| --- | --- |
| `stircurve/config/usd_manifest.yaml` | Every instrument the `usd.yaml` families use (`ff_fut`, `sofr1m_fut`, `sofr3m_fut`, `ed_fut`, `ois_effr`, `ois_sofr`, `swap_libor3m`), the EFFR / SOFR / USD LIBOR 3M fixings and the policy anchors: Bloomberg ticker pattern, fields, quote convention (mids, D10), window, accrual, day count, calendars (named, never hard-coded), last trade, final settlement, listing schedule, first/last dates, valid range, staleness threshold, and the source of every rule. |
| `stircurve/marketdata/manifest.py` | Loads and validates the manifest against `usd.yaml`; ticker naming; the column plan for any date range. |
| `stircurve/marketdata/contracts.py`, `scripts/contract_table.py` | Contract table: every listed future in a range with reference window [start, end), last trade, final settlement, first listed, last quote, settlement rule. |
| `stircurve/marketdata/sources.py`, `scripts/capture_exchange_specs.py` | Captures the rule documents (CME/CBOT filings on cftc.gov, NY Fed, FCA) into `tests/fixtures/live`; every quoted rule passage must appear in its capture. |
| `stircurve/marketdata/dump.py`, `scripts/dump_bloomberg.py` | Terminal machine only: manifest -> Bloomberg via pdblp (one session, one bulk request per field, bad securities skipped; `--backend pxts` for `pxts.read_bdh`) -> wide CSVs. Dry run by default; `--write-csv` writes the files (committing them to git is a separate step); a changed or vanished value blocks (exit 2); re-runs are no-ops. |
| `stircurve/marketdata/loader.py`, `scripts/check_market_data.py` | Tidy frame keyed by (date, instrument, contract, field) plus a report: unknown columns, malformed files, out-of-range values and quotes outside a contract's listing window block (exit 2); missing columns, stale values and values outside first/last dates warn. |
| `scripts/m1_gate.py` -> `docs/m1_gate.md` | Gate evidence: rule sources, listing checks against the filings, generated windows, the loader report on real days. |

The dump requests futures generously (`dump_listing` in the manifest: FF 60 months, SR1 13,
SR3 41 quarterly + 6 serial, ED 44 + 6, from the first date). Contracts Bloomberg has nothing
for come back as NaN columns. The loader checks listing dates against the exchange schedule
(`listing`); where that schedule has no source, early quotes are kept and reported.

Column names: `<ticker>|<field>`, e.g. `SFRZ26 Comdty|PX_LAST`, `USOSFR2 Curncy|PX_LAST`,
`SOFRRATE Index|PX_LAST`. Futures columns always carry the two-digit year; the dump asks
Bloomberg for the one-digit form while a contract trades (`SFRZ6 Comdty`).

On a Bloomberg terminal machine (`pip install -e .[bloomberg]`, plus `blpapi` from Bloomberg's index). Every Bloomberg request is logged with its size, time and outcome:

```
python scripts/dump_bloomberg.py --start 2026-10-07 --end 2026-10-07              # dry run: diff only
python scripts/dump_bloomberg.py --start 2026-10-07 --end 2026-10-07 --write-csv
python scripts/dump_bloomberg.py --start 2019-06-12 --end 2019-06-12 --write-csv  # LIBOR era
python scripts/check_market_data.py --start 2026-10-07 --end 2026-10-07           # exit 0 = no blocking problem
python scripts/m1_gate.py                                                         # refresh docs/m1_gate.md
```

Rule documents (any machine with internet):

```
python scripts/capture_exchange_specs.py --save-fixtures tests/fixtures/live
python scripts/capture_exchange_specs.py --check
```

cmegroup.com is never fetched by script (its terms forbid it and it answers 403). Its tables
(contract specs, calendars) are loaded by JavaScript, so a saved .html misses them: open the
page, wait for the table, then Ctrl+A, Ctrl+C and paste into a text file (or print to PDF),
named after the manifest source, e.g.
`cme_sr3_specs_table.txt`, `cme_sr3_specs_calendar.txt`, `cme_sr1_specs.txt`, `cme_sr1_specs_calendar.txt`,
`cme_ff_calendar.txt`, and run
`python scripts/capture_exchange_specs.py --from-saved <files> --save-fixtures tests/fixtures/live`.

See `CLAUDE.md` for working rules and `docs/decisions.md` for the decision log and build plan.

## M2: USD EFFR front end

Design: `docs/research/front_end_curve.md` (the state-of-the-art review AC decided from) and the Bloomberg
WIRP documents in `docs/research/wirp/` (the gate standard); decisions D20-D23. Gate evidence:
`docs/m2_gate.md` (`python scripts/m2_gate.py`).

| Piece | What it does |
| --- | --- |
| `stircurve/instruments/` | Day counts by name; average-rate futures (FF arithmetic; SR1/SR3 later) and overnight-index swaps priced from a flat-forward curve, every convention from the manifest and the contract table. A switchable, measured month-end adjustment lives in the FF model (off by default; never a curve node). |
| `stircurve/curves/flat_forward.py`, `nodes.py` | Parcels between effective dates (D2) with past fixings; nodes: published, synthetic (flagged), decided unscheduled meetings from their decision date, superseded meetings (`superseded_on`) until their supersession. |
| `stircurve/curves/wirp_replica.py` | WIRP's two models (futures, OIS) as a sequential bootstrap: one quote per parcel, a later more direct quote overrides, joint solve when a month holds two unknowns, nothing beyond the instruments' reach. The gate reference. |
| `stircurve/curves/robust.py`, `front_end.py` | Per instrument (`front_end.curves`: `effr_fut`, `effr_ois`): global weighted least squares on the step levels, Huber IRLS, weights from open interest / volume / staleness, exclusion of FF prices with no open interest and no volume (derived settlement prices), a very weak step prior with equal-step ties where nothing in the data tells two meetings apart and flat steps beyond the last instrument, drops by Huber weight and by leave-one-out residual, identification, leverage and posterior sigma per parcel. |
| `stircurve/policy/spread.py`, `outputs.py`, `export.py` | D7 policy spread; per meeting the WIRP columns (Current Implied O/N Rate, Post-Meeting Implied Rate, Imp. Rate Δ, #Hikes/Cuts, %Hike/Cut), the replica's values, the implied policy rate and the cumulative change vs the current target, flags; FF/OIS basis; exports and the local curve store. |
| `stircurve/quality/battery.py`, `wirp.py` | Residuals in bp, drop list with reasons, high-leverage quotes with their leave-one-out residuals, stale / outside-listing inputs, parcel identification, the replica's inputs, a one-page report; the WIRP capture parser (checks the capture's own identities) and the three-layer comparison. |
| `scripts/front_end.py`, `scripts/m2_gate.py` | Build and export any as-of date; the gate document (replica vs capture, fit vs replica, fit vs capture, basis, drop lists, residuals, month-end evidence). |

```
python scripts/front_end.py --as-of 2026-10-07            # exports/usd/effr/2026-10-07/
python scripts/front_end.py --as-of 2026-10-07 --store    # + data/curves/ (local)
python scripts/m2_gate.py --exports                       # docs/m2_gate.md and the exports for every gate date
```

WIRP captures: one per gate date and model, `tests/fixtures/live/wirp_us_fut_<YYYYMMDD>.txt` (WIRP US,
Fed Funds Futures) and `wirp_us_ois_<YYYYMMDD>.txt` (WIRP US OIS): the header lines (Instrument, Target
Rate, Effective Rate, Pricing Date, Cur. Imp. O/N Rate) and the meeting table. The 7 Oct 2026 captures are
AC's screenshots (`.png` alongside) transcribed by hand; the parser checks the capture's own identities.

Settings: `stircurve/config/usd.yaml` `front_end` (curves, horizon, spread, month-end adjustment, fit, wirp).
