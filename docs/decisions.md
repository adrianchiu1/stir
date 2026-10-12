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
| D16 | Decision date = the day the decision is announced; implementation date is separate. A published implementation date wins over the bank's rule for every bank (ECB maintenance table; `meetings/published_effective.csv`: Fed 2020-03-03→04, BoJ 2016-01-29→02-16). Reference data includes every published date. AC, PR #1 |
| D17 | Reference data holds every published monetary-policy decision date (Fed 1994+, ECB 2004+, BoE 1997+, BoJ 1998+); unscheduled meetings are those the bank itself calls so (BoJ minutes, Fed conference calls) or that AC designates (BoE 8 Oct 2008); `us_sifma` (SIFMA closes) and `us_sofr` (SOFR publication days) are separate calendars; BoJ policy rates are sourced from the statements and auto-updated. AC, PR #1 |
| D18 | Era-dependent effective-date rule: Fed decisions before 2009 and BoJ decisions before 19 Mar 2024 take effect on the decision day (rolled to a business day); later ones the next business day. Published implementation dates still win. BoJ spread anchor under QQE (4 Apr 2013 – 15 Feb 2016) is `ioer` (0.1%). AC, PR #1 |
| D19 | USD market data (M1): Bloomberg via pdblp, one session, bad securities skipped (`--backend pxts` kept); PX_LAST throughout (mids, D10); CME futures business days `us_sifma` (CME closed on Good Friday: month-end last trade the Thursday, as CME's calendar); SOFR OIS on `us_sofr` (SIFMA full trading days; early-close days such as 24 Dec are business days); ED window end London+NY; ED last price 16 Jun 2023, contracts expiring after 30 Jun 2023 last priced 14 Apr 2023 (converted to SR3); SR3 Reference Quarters keep IMM boundaries on non-SOFR days, final settlement on the next SOFR publication day (SFRH24: 18 Jun last trade, 20 Jun settlement); the dump requests futures generously; IORB anchor ticker `IRRBIOER Index`. AC, PR #2 |
| D20 | M2 front end (research memo `docs/research/front_end_curve.md`, Bloomberg WIRP documents in `docs/research/wirp/`): D2 confirmed, with node types scheduled effective dates, a decided unscheduled meeting's effective date from its decision date, and a superseded scheduled meeting until its supersession date (`superseded_on` in `meetings/fed.csv`: 17-18 Mar 2020). A month-end is never a node; the FF instrument model may carry a measured, switchable month-end adjustment (off by default and for the gate). Unscheduled meetings are not priced ahead. AC, PR #4 |
| D21 | FF futures and EFFR OIS are separate instruments: one step curve each within the EFFR family (`front_end.curves`), each gated against its own WIRP model; the FF/OIS basis per meeting is a stored diagnostic (as D5 treats families). No blended curve in M2. AC, PR #4 |
| D22 | M2 fit (D4 applied per curve): global weighted least squares on the step levels, Huber k 1.345 with the quote sigma as the scale, weights from open interest, volume and staleness; an FF price with no open interest and no volume is a derived settlement price and is excluded; a very weak step prior, equal-step ties between consecutive meetings nothing in the data tells apart (D-C: equal steps in time), flat beyond the last instrument; drops by Huber weight and by leave-one-out residual (the quote whose removal leaves the smallest loss); leverage, identification and posterior sigma reported. AC, PR #4 |
| D23 | Gate reference: a replica of WIRP's two sequential-bootstrap models (`curves/wirp_replica.py`) on our own quotes; three layers per date and curve: replica vs capture, fit vs replica, fit vs capture; outputs in WIRP's definitions (Current Implied O/N Rate, Post-Meeting Implied Rate, Imp. Rate Δ, #Hikes/Cuts, %Hike/Cut) plus the D7 policy conversion. `USSO*` is fed by ICVS 42; ICVS 85 (Fed Funds) is on a par for Fed pricing. AC, PR #4 |

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
