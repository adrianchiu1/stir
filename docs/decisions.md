# Decisions (ADR-style, newest last)

Full log with rejected alternatives: design spec, "Decision log". Confirmed by AC, 8 Oct 2026.

| # | Decision |
| --- | --- |
| D1 | Policy pricing and full zero curve are both first-class deliverables |
| D2 | Front end: flat forwards between effective dates; cadence-extrapolated synthetic meetings to 3y, flagged |
| D3 | Junction: C0 forward-continuous stitch at the 3y swap node; Fritsch–Butland PCHIP forwards beyond |
| D4 | Under-identified parcels take the OIS family's split as prior; over-identified front end uses robust IRLS (Huber) with liquidity/staleness weights and a reported drop list |
| D5 | One curve per instrument family; USD builds both EFFR and SOFR; basis is a diagnostic |
| D6 | Default family per era: IBOR-based until the first date the RFR futures family's rolling 3-month average open interest exceeds the IBOR family's (never before 2022-04-01; no switching back); EUR by hand |
| D7 | Policy spread = fixing − anchor in effect, turn days dropped, trailing 63 business days, winsorised 10/90 mean (median alternative); anchors: Fed target midpoint, ECB DFR, BoE Bank Rate, BoJ policy-rate-balance rate then IOER |
| D8 | Turn nodes for SOFR, €STR, SONIA, TONA; steps fitted net of turns |
| D9 | Convexity: HW1F closed forms per contract type; σ from 60-day realised vol, strip-implied cross-check (±30%); no option vols available |
| D10 | Quotes are mids; tolerances in bp |
| D11 | History from 2010; IBOR projection curves dual-bootstrapped on OIS; unscheduled decisions included |
| D12 | Data: Bloomberg via pxts dumps to wide CSVs (committed, licensing cleared); public APIs for fixings; reference data from public sources via deterministic updaters |
| D13 | Store local and git-ignored; analytics exports shared |
| D14 | Validation: ICVS points (curve IDs SOFR 490, Fed Funds 85, €STR 514, SONIA 141, JPY OIS 195) and WIRP samples |
| D15 | Effective dates: Fed +1 business day; ECB maintenance-period start (published table wins); BoE same day; BoJ next business day (confirmed on 2024-03-19→21, 2025-12-19→22, 2026-06-16→17) |

## Build plan and gates

| Milestone | Scope | Gate (AC signs off) |
| --- | --- | --- |
| M0 | Skeleton, calendars, meetings, maintenance periods, policy rates, updaters, tests | AC spot-checks ten effective dates per bank; first live updater run clean |
| M1 | USD manifest validated, `dump_bloomberg.py`, CSV loader/validator, contract-table generator | One day of USD data loads with zero unknown columns; windows match exchange calendars |
| M2 | USD EFFR family front end: instrument models, robust IRLS, priors, turns, spread, policy outputs, quality battery | WIRP comparison on 10 dates within 1bp; drop list reviewed |
| M3 | USD SOFR family + convexity (HW1F, Monte Carlo validation, σ ladder) | SR3-vs-OIS residual beyond 2y explained within ±30% σ |
| M4 | Back end PCHIP bootstrap, junction, ICVS comparison, Eurodollar/LIBOR multi-curve, curve store | ICVS RMSE targets on mimic config; 2010–2026 USD history builds |
| M5 | Visualisation: three time-series modes, as-of curve, 3D surface, diagnostics notebook | AC uses notebooks for a week |
| M6–M8 | EUR, GBP, JPY | As M2–M4 |
| M9 | Full history rebuild, stability report, tolerance reset, methodology white paper | AC review |
