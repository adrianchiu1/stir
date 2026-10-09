# Front-end curve construction: state of the art and a recommendation (M2, phase A)

Purpose: a review AC can decide from, on two questions, before any M2 curve code is written.

1. How to build the front-end forward curve when there are more instruments than nodes.
2. How to treat unreliable forward-rate observations (illiquid, stale or derived prices that put kinks in the curve).

Scope: the USD EFFR family (FF futures and EFFR OIS, mids only, eight scheduled FOMC meetings a year plus
unscheduled ones), with an eye to the other three banks and the next 18 currencies. Everything below is
sourced where it can be; where a statement is my own judgement it says so. Paywalled sources are marked
*(paywalled)*; everything else links to a free copy. Section 7 lists every source with a link.

Revision 2 (9 Oct 2026): AC supplied Bloomberg's own WIRP documentation (`docs/research/wirp/`), which is the
gate standard and is treated as such throughout; AC also answered three points from revision 1 (unscheduled
meetings, month-end, FF versus OIS). Sections 1.4, 1.5, 2.6, 2.7, 3.5, 4 and 6 changed; the rest is as before.

Decisions this memo asks AC to take are collected in section 6.

---

## 0. Summary

**Keep D2.** Piecewise-flat forwards between policy effective dates is what WIRP does (Bloomberg: "only a
central bank action will impact the effective interest rate"; the meeting day is at the pre-meeting rate and
the post-meeting rate starts the next day, which is our Fed effective-date rule), and what CME FedWatch, the
Fed Board's own notes, the Riksbank's RIBA method, the ECB's maintenance-period-dated OIS forwards, the R
`copom` package for BRL and QuantLib's `GlobalBootstrap` do. The classic objection to flat forwards (Hagan and
West 2006: discontinuous forwards "imply implausible expectations about future short-term interest rates")
does not apply when the discontinuities sit where the policy rate can change. Smooth interpolants (monotone
convex, PCHIP, tension or smoothing splines) are the right tool beyond the meeting horizon (D3), not inside
it: they smear a step across neighbouring parcels and would fail a 1bp WIRP gate by construction.

**WIRP is a sequential exact bootstrap, run separately on FF futures and on OIS, with no reconciliation
between the two, no weights, no robust loss, no regularisation and no turn adjustment**, and it stops where
monthly liquidity stops (about a year). That settles the validation design: first replicate WIRP's two models
exactly from our own data (a few hundred lines; the gate is then a like-for-like comparison per instrument),
then run our estimator and report how far, and why, it departs from the replica. The 1bp gate is a test of
the data, conventions and calendars; everything we add on top is a deliberate, reported departure.

**Treat FF futures and EFFR OIS as separate instruments, as WIRP does and as AC proposes.** Two step curves
per as-of date within the EFFR family (FF-based, OIS-based), each gated against its own WIRP model, and the
FF/OIS basis per meeting stored as a diagnostic, in the spirit of D5. The literature (section 1.5) finds the
two comparable on average inside a year but different day by day for structural reasons (compounding versus
averaging is a convention we model exactly; liquidity profile, participants, marking times and margining are
not), and no published method models the basis explicitly. A blended curve is a later option, not an M2
deliverable.

**Keep D4, applied per instrument, with two additions and one change of emphasis.** A robust IRLS fit (Huber)
with liquidity and staleness weights is the standard way to use an over-identified strip; what the literature
and our own two days of data say is that (a) the weights should do most of the work and the robust loss should
be a backstop, because the unreliable quotes are predictable from open interest, volume and staleness rather
than surprising (43 of the 60 FF prices on 2026-10-07 are derived settlement prices, not quotes); (b) a Huber
loss cannot protect a parcel that only one quote identifies (leverage one): those quotes need a prior and a
leave-one-out diagnostic, not a loss function; and (c) a weak Gaussian prior on the steps (a Tikhonov/ridge
penalty, or a Gaussian-process posterior) is the cheapest way to make the region beyond WIRP's horizon
well-posed, to give every meeting a credible interval, and to stop one bad quote from bending its neighbours.
Inside WIRP's horizon the prior must be weak enough to move an identified step by far less than 1bp.

**What to drop, and what to keep as diagnostics only.** Least-trimmed-squares, quantile (LAD) fits and
fused-lasso (sparse 25bp step) fits are worth running as *diagnostics* (an independent drop list and a
"number of moves" reading) but not as the estimator, because each is biased against partially-priced moves.
Kalman filtering across days is an M9 stability tool, not an M2 estimator: WIRP is a same-day exact read.

**Two points AC settled.** Month-end dips in EFFR are a fixing effect, not a meeting, so not a node (D8
stands); if the 2010+ fixings show the effect is material it can be a switchable adjustment inside the FF
instrument model, off for the WIRP gate because WIRP makes none. Unscheduled meetings are not something the
curve prices ahead: the only things the design matrix needs are the known step between a decision and its
effective date (one day for the Fed) and, in reference data, the scheduled meeting that an emergency meeting
superseded (section 2.7).

---

## 1. The problem in our terms

### 1.1 What the instruments identify

A front-end curve for the EFFR family is a function of the daily EFFR forward. Under D2 it is piecewise
constant between effective dates, so its parameters are: one stub level (EFFR from the as-of date to the first
effective date) and one post-meeting level per meeting inside the horizon. Each FF contract prices the
arithmetic average of the daily EFFR over a calendar month (CBOT chapter 22, captured in the M1 manifest); each
EFFR OIS prices the compounded EFFR from spot to maturity. Both are linear (FF) or very nearly linear (OIS, in
the rates) in the step levels, so the fit is a small linear or mildly non-linear least-squares problem.

Counting on the two real days on file (a scratch script over the dumps under `data/market/usd`; counts include
the meetings that were later known, which a "from decision date" rule would exclude):

| As-of | FF contracts quoted | with open interest | with volume | effective dates in first 12 / 18 / 24 contracts | spare degrees of freedom at 12 / 18 / 24 |
| --- | --- | --- | --- | --- | --- |
| 2019-06-12 | 36 | 24 (OI < 1,000 beyond the 18th) | 20 | 10 / 14 / 18 | +1 / +3 / +5 |
| 2026-10-07 | 60 | 17 | 24 (seven of them zero) | 8 / 10 / 10 | +3 / +7 / +13 |

"Spare degrees of freedom" is quotes minus (stub + steps). The first year is always over-identified by the FF
strip alone, and the EFFR OIS has 17 quotes inside two years (1W, 2W, 3W, 1M to 11M, 1Y, 18M, 2Y). Beyond the
published FOMC calendar the count of steps is set by cadence extrapolation (synthetic meetings, D2), and
beyond about 18 months the FF strip stops carrying information (next paragraph), so each curve is
over-identified in the first 12 to 18 months and under-identified beyond, where only 18M, 2Y and 3Y OIS remain
and each parcel between them holds four meetings. WIRP covers only the first region (1.4).

### 1.2 What the far FF strip actually is

On 2026-10-07 the dump has 60 FF prices but open interest on only 17 and non-zero volume on 17. From the 19th
contract on, the month-to-month changes repeat with a 12-month period (+4bp into April, +8bp into August, 0
into September, +0.5 into October, ...) in 2028, 2029, 2030 and 2031 identically. Those are not quotes; they
are the exchange's derived daily settlement prices for untraded months (the front-month procedure is
documented in CME's 2018 notice SER-8105; the deferred-month procedure is not public as far as I can find).
This is the single most important fact for question 2: the unreliable observations in this family are mostly
*known in advance* from the liquidity fields and from the listing model, and the fit should treat them as
missing, not as noisy. Lloyd (2018, BoE SWP 709) says the same from the research side: FF futures "have
historically been illiquid at horizons in excess of 1 year", while OIS "tend to be liquid out to at least the
3-year horizon". WIRP's own rule is the same: it stops at the last reliably priced monthly tenor.

### 1.3 What the previous attempt found (PR #3, closed by AC with "redoing this stage")

Those numbers are still informative about the data even though the code was discarded:

- A joint Huber fit on 2026-10-07 with 0.5bp quote noise on both families left FF residuals with an RMS of
  0.97bp and OIS residuals of 1.37bp. Fitting FF alone moved implied meeting rates by up to 1.5bp in the first
  year (0.85bp on 2019-06-12); fitting OIS alone moved them by up to 10bp inside two years. The two families
  disagree by more than the gate tolerance: one more reason to fit and gate them separately (1.5).
- On 2019-06-12 the only large FF residuals were February 2020 (+3.0bp) and April 2020 (-2.8bp), on either
  side of the scheduled 17-18 March 2020 meeting, which is absent from `data/refdata/meetings/fed.csv` because
  the 15 March emergency meeting superseded it. A missing node shows up as a residual pair of opposite sign: a
  useful signature for the quality battery.
- A quote that alone pins a parcel has leverage near one; its error moves the curve rather than the residual,
  and a Huber loss then blames its neighbours.

### 1.4 What WIRP does (from Bloomberg's documentation, `docs/research/wirp/`)

Three Bloomberg documents (help page dated 9 Oct 2026, "Calculations", "Estimating the Path of Central Bank
Hikes and Cuts") replace the conflicting public descriptions in revision 1. The facts that matter here:

- **One assumption**: "only a central bank action will impact the effective interest rate of an economy",
  so expected overnight rates are "pushed forward and backward through the chosen asset's tenor structure".
  This is D2.
- **Two separate models per region**, `US - Fut` and `US - OIS`, each with its own ticker family (futures
  `US0AFR`, `US0ANM`, `US0APR`, `US0ACR`; OIS `US0BFR`, `US0BNM`, `US0BPR`, `US0BCR`; meeting tail `MMMYYYY`).
  Nothing reconciles them; the help page shows them side by side with different numbers for the same meeting
  (e.g. 29 Jul 2026: +33.7% futures, +32.7% OIS).
- **Futures model**: a non-meeting month gives one rate; for a meeting month `31 × avg = d_pre × pre +
  d_post × post`, with `pre` carried forward from the preceding non-meeting contract ("we can carry the
  November rate forward into the Dec2019 contract") and `post` solved; then "we work our way through the
  available contract prices and CB meeting dates". The meeting day is at the pre-meeting rate and the post
  rate starts the next day (11 days at 1.790, 20 days at 1.658 for a 11 Dec 2019 meeting), which is our
  Fed effective-date rule (D15).
- **OIS model**: fixed `1 + r·n/360` against the daily-compounded float `∏(1 + r_i d_i/360)`, `d_i` = 1 on
  weekdays and 3 over weekends, holidays carried; spot lag 2 days; the unknown rate on each segment is
  assumed constant and found by Newton's method; the 1W tenor gives the pre-meeting rate, the 1M tenor
  (chosen over 3W "as it tends to have more liquidity than the similar three-week security") the first
  post-meeting rate, and so on through the monthly tenors. The curve is `ICVS 42` (D14 names Fed Funds curve
  85; to check on the terminal).
- **Outputs**: Current Implied O/N Rate (the rate until the first meeting, read from the instrument, not from
  the EFFR fixing: 3.628 against an effective rate of 3.63 on the help-page screen), Post-Meeting Implied
  Rate, Imp. Rate Δ = post − current implied, #Hikes/Cuts = Δ / A.R.M. (cumulative; A.R.M. = 25bp),
  %Hike/Cut = (post_t − post_{t−1}) / A.R.M. (marginal). Percentages may exceed 100%. The conditional
  probability grid was dropped in 2019 because "the percent of a hike/cut is not the same as a probability".
- **Horizon**: "If there is no reliable pricing on all monthly tenors beyond a certain point on the curve,
  WIRP does not show meeting dates beyond that point"; the screens show about 14 months of meetings.
- **Timing**: futures on a 10-minute delay, OIS live; futures close 6 pm ET, OIS 5 pm ET; "post-close trades
  generally process the next day". Options and Eurodollar models removed September 2019.
- **No** weights, robust loss, smoothing, turn or month-end adjustment, risk-premium adjustment, or
  treatment of inter-meeting moves. A small futures-only "hike" on 25 Nov 2019 is described as "noise within
  the market, as the same noise didn't occur in the OIS market".

Consequences: the gate target is the Post-Meeting Implied Rate per meeting (and the two derived columns),
per instrument; the gate horizon is WIRP's, about a year; and WIRP's method is cheap to replicate exactly,
which is how the gate should be run (section 4). The exact tenor-selection rules beyond the first meeting
("work our way through") are not spelled out, so the replica will need the captures to pin them down.

### 1.5 FF futures versus EFFR OIS: what the literature says about the basis

AC's position: the two are fundamentally different instruments (fed funds are traded by institutions with
Federal Reserve accounts; OIS are collateralised dealer swaps) and should be treated as separate, with a
natural basis between them. What the sources say:

- **Both are risk-neutral reads of the same EFFR path and are comparable on average inside a year.** Lloyd
  (2018) builds FF-futures portfolios with the same horizon as OIS and finds "1 to 12-month OIS rates provide
  measures of investors' interest rate expectations that are comparable to those from corresponding-horizon
  FFFs contracts". Kısacıkoğlu (2024) finds OIS risk premia "negligible ... up to 1 year"; Hamilton (2009)
  finds the short-horizon FF premium small and outlier-sensitive; Durham (2003, FEDS) finds estimates of the
  FF term premium from near-dated contracts "highly volatile"; Piazzesi and Swanson (2008) find FF excess
  returns positive and countercyclical. None of these estimates a FF-versus-OIS basis as such.
- **Known structural differences.** (i) Conventions: FF settles to an arithmetic average, OIS to a daily
  compounded rate; on a flat 4% path the 1M OIS fixed rate is about 0.6bp above the FF average and the 1Y
  about 8bp above. This is not a basis, and the instrument models remove it exactly. (ii) Liquidity profile:
  FF liquid to 12-18 months, OIS to 3 years (Lloyd; Kim and Tanaka switch instruments at two years; WIRP
  stops each model at its own liquidity limit). (iii) Marking: FF settlement at the CME close, OIS BGN
  composite mids at 5 pm; WIRP's own note that futures carry noise the OIS did not on 25 Nov 2019. (iv)
  Margining and convexity: futures are variation-margined, cleared OIS are collateralised; the convexity
  difference is of order ½σ²T², under 1bp inside a year and a few bp at two years (judgement, Hull-White
  order of magnitude). (v) Participants and supply: fed funds themselves trade between institutions with
  reserve accounts (FHLBs lend, foreign banks borrow: Bowman 2025), futures are used by asset managers,
  leveraged funds and dealers (the CFTC legacy report shows roughly two-thirds commercial open interest),
  OIS by dealers and banks; demand imbalances can leave different premia in the two markets (Piazzesi and
  Swanson's mechanism). (vi) Skov and Skovmand (2023) model bases *between* benchmark rates (SOFR, EFFR,
  LIBOR) jointly from futures; the FF-futures-versus-OIS basis on the same index is not, as far as I found,
  modelled anywhere in print.
- **Practice.** Bloomberg runs two models and reconciles nothing; the Fed Board's notes pick one instrument
  per horizon; our previous attempt measured 1-1.5bp differences in implied meeting rates in the first year
  after conventions were modelled.

Conclusion for M2 (agreeing with AC): one step curve per instrument within the EFFR family, each gated against
its own WIRP model; the basis per meeting (FF-implied minus OIS-implied post-meeting rate) stored and plotted
as a diagnostic, exactly as D5 treats the EFFR/SOFR basis. A blended curve (both families with a slowly
varying spread term) is a later option; it is not needed for the gate and would obscure it.

---

## 2. Question 1: more instruments than nodes

### 2.1 Piecewise-flat forwards between effective dates (D2)

**What it assumes.** The overnight rate can change only on policy effective dates (and on dates we add
deliberately: turns for the RFR families under D8, a decided unscheduled meeting's effective date), and is
otherwise expected to be constant. The expectation is risk-neutral: risk premia are not removed (2.9).

**Who uses it.** WIRP (1.4). CME FedWatch: "rate hikes/cuts are uniformly sized in increments of 25bps", "for
months with meetings, the corresponding monthly Fed Funds futures contract price is used to calculate the
probabilities", and "the projected end rate for EFFR in each month should be equal to the start rate for EFFR
in the subsequent month" (CME methodology page; cmegroup.com refuses scripted access, so these quotes come
from search snippets). Kim and Tanaka (FEDS Notes, 2016): "the federal funds target rate/range changes are
discrete and occur only on FOMC meeting dates"; they use FF futures and switch to OIS "for horizons beyond
about two years" on liquidity grounds. Riksbank (Ceh 2022): the policy rate "can shift solely at the very few
predetermined dates -- implementation dates, and in predetermined, regular, discrete sized steps, and is
therefore better suited to be described by the step-function instead of via the smooth curve"; a RIBA quarter
with two meetings is split by day-weighting both steps, with the identification closed by a probability tree.
The ECB's Money Market Contact Group reads the terminal rate as "the maximum of the Maintenance Period-dated
OIS forward contracts". The R `copom` package (Freitas) implements flat-forward interpolation on COPOM dates
for BRL DI futures and lists four ways to resolve two futures between the same pair of meetings (first,
second, forward between them, or an optimisation), a precedent for a currency on our list. QuantLib's
`GlobalBootstrap` (SoftSolutions 2019, Caspers 2025) solves all nodes at once by Levenberg-Marquardt on a
weighted vector of quote errors with optional `additionalDates` (meeting dates) and `additionalPenalties`.

**Properties.** Hagan and West (2006) call it "raw interpolation" (linear in log discount factors): "This method
is very stable, is trivial to implement, and is usually a base method one implements in a system before any
others." It is perfectly local (a quote can only move the steps whose parcels it covers) and its hedges are
local. Its one defect in their framework, discontinuous forwards, is the feature we want: McCulloch and
Kochin's objection that a discontinuous forward curve "implies either implausible expectations about future
short-term interest rates, or implausible expectations about holding period returns" is an objection to jumps
at arbitrary instrument maturities, not at dates when the central bank meets.

**Behaviour on our data.** Exact (bootstrapped) version, which is WIRP's: N quotes, N nodes, so in the
over-identified first year some quotes must be left out, and the result depends on which (WIRP's rule: the
non-meeting-month contract supplies the pre-meeting rate; 1M over 3W in OIS). Global version (one
least-squares problem): uses all quotes, leaves residuals in bp per instrument, and is the natural host for
weights, a robust loss and priors. Either way a meeting inside a month is handled by day-weighting the pre-
and post-meeting levels (Kuttner 2001; FedWatch; WIRP's worked example). The stub level and the first step are
identified mostly by the front contract, whose remaining days shrink through the month; the quality report
should show the front contract's weight in days.

**Cost.** Low: a design matrix (days of each parcel inside each instrument window, from the contract table and
the fixing calendar), weighted least squares, Gauss-Newton for the OIS compounding. Everything needed exists
after M0/M1.

**WIRP validation.** This is WIRP's own model, so the comparison is clean: per meeting, per instrument, our
implied rate minus WIRP's. Differences come from (i) quote timestamps, (ii) which contracts each side uses,
(iii) anything we add (weights, robust loss, prior), (iv) the stub (WIRP reads it from the instrument).

### 2.2 Exact bootstrap versus global least squares

An exact bootstrap (QuantLib's `PiecewiseYieldCurve` with `BackwardFlat` forwards, Ametrano and Bianchetti
2013 for the multi-curve version; WIRP) needs one instrument per node and a rule for choosing which. A global
fit (Hagan and West 2006 on "best fit" curves, QuantLib `GlobalBootstrap`, Andersen and Piterbarg 2010 vol. 1
ch. 6 *(paywalled book)*) minimises a weighted sum of squared quote errors over all nodes at once. With the
step model the global fit is linear in the FF quotes and the bootstrap is the special case of zero residuals
on the selected subset. Recommendation: implement both. The bootstrap with WIRP's selection rules is the
replica and the gate reference; the global fit is the estimator; the difference between them, per meeting,
is the price of using all the quotes, and it is reported. (Judgement.)

### 2.3 Regularised fits: Tikhonov, ridge and smoothing penalties

**What they are.** Add λ·‖L θ‖² to the weighted sum of squares, where θ are the step levels (or the steps
themselves) and L encodes a belief: L = I on the steps shrinks every move toward zero ("no change" prior,
which is what a flat extrapolation of the last identified level amounts to); L = first differences of the steps
shrinks toward a constant pace ("continue the cycle"); L = second differences shrinks toward a linear path. λ
is chosen by generalised cross-validation (Fisher, Nychka and Zervos 1995; Tanggaard 1997), by the L-curve
(Hansen 1992 *(paywalled)*; Hansen and O'Leary 1993), or by fixing the prior standard deviation in bp, which
is the same thing in Bayesian clothing (2.5). Waggoner (1997) and the Bank of England's variable roughness
penalty (BIS Papers 25, 2005) let λ vary with maturity: small where instruments are dense, large where they
are sparse, which is precisely our shape (dense FF strip, then three OIS points).

**What they assume.** That the true path is closer to the penalised shape than the data alone say. In the
over-identified region a small λ barely moves the fit (the data dominate); in the under-identified region the
penalty is what picks the solution, so its form *is* the answer there.

**Behaviour on our data.** With L = I and a prior σ of, say, 10bp per step, a step identified by a liquid FF
pair with 0.5bp noise moves by about (0.5/10)² ≈ 0.25% of its value, well inside 1bp. Beyond 18 months, where
only 18M, 2Y and 3Y OIS exist, a parcel's total change is identified but its split across four meetings is
not; the ridge gives the minimum-norm split (equal steps), the first-difference penalty continues the last
pace. Neither is "right", and WIRP does not go there. The penalty also fixes the leverage problem of 1.3: a
parcel pinned by one bad quote is pulled back toward the prior in proportion to the quote's weight.

**Cost.** Trivial on top of 2.1: one extra block in the least-squares system. GCV or the L-curve are a loop
over λ; fixing σ in bp needs no loop and is more legible in a report.

**WIRP validation.** The penalty must be small enough that the gate passes inside WIRP's horizon; the report
prints, per meeting, the fitted value with and without the penalty so that the departure is visible. Beyond
WIRP's horizon there is no gate and the prior-versus-fitted split is printed instead.

### 2.4 Shape-preserving and smooth interpolation

**Monotone convex** (Hagan and West 2006): local, preserves positivity and monotonicity of the forwards, is the
default in several vendor systems; known defect: with the unameliorated version the forward can be
discontinuous at nodes, and later work (du Preez and Maré 2013) proposes monotone-preserving alternatives.
**PCHIP / Fritsch-Carlson / Fritsch-Butland** (SIAM 1980, 1984 *(paywalled)*; SciPy `PchipInterpolator`):
local cubic Hermite with shape-preserving slopes, C1, no overshoot; D3 already picks it for forwards beyond 3y.
**Tension splines** (Andersen 2007 *(paywalled)*; Andersen and Piterbarg vol. 1): a tension parameter moves
continuously between a cubic spline and linear interpolation and bounds how far a perturbation propagates.
**Maximum smoothness forwards** (Adams and van Deventer 1994 *(paywalled)*, corrected in van Deventer and Imai
1996; Lim and Xiao 2002 *(paywalled)*; positivity in Manzano and Blomvall, arXiv math/0305307): quartic
forwards minimising ∫f''² subject to exact pricing.

**What they assume.** A continuous (C0 to C2) forward curve. That is the wrong assumption inside the meeting
horizon: an expected 25bp step at a meeting becomes a ramp spread over the surrounding months, so the
post-meeting rate at the meeting date is off by a sizeable fraction of the step. They also need one node per
instrument (interpolation), so they inherit the thinning problem of 2.2 unless combined with a least-squares
or penalised fit (which is then 2.3 on a spline basis: Fisher-Nychka-Zervos, Waggoner, the BoE's VRP).

**Behaviour on our data.** Ramps instead of steps; residuals on FF contracts that straddle a meeting; a 1bp WIRP
gate fails by construction wherever a move is priced. Useful for the synthetic tail (beyond the last published
meeting the step dates are themselves guesses, so a smooth shape loses little) and for the junction (D3).

**Cost.** Low (SciPy has PCHIP; monotone convex and tension splines are a few hundred lines) but it buys nothing
inside the horizon.

**WIRP validation.** Would fail. Keep for the back end only.

### 2.5 Parametric and Bayesian approaches

**Gaussian-process (GP) priors on forwards.** Kimeldorf and Wahba (1970) showed that a smoothing spline is the
posterior mean under a Gaussian-process prior; Rasmussen and Williams (2006, free online) is the standard
reference; Filipović's slides show the Smith-Wilson curve used by EIOPA is a GP posterior mean. A GP with a
smooth kernel on the daily forward is the Bayesian form of 2.4 and has the same problem (it smears steps). A
GP on the *step levels* with an independent (white) kernel is the ridge of 2.3; with a random-walk kernel it is
the first-difference penalty. The useful part of the GP view is not a new estimator but what comes free with
it: a posterior standard deviation per meeting (the quality battery's "how well is this step identified"
column), and a principled way to combine two families (if a blended curve is ever wanted, 1.5). The
hyperparameters (prior σ, noise σ per instrument) can be set by marginal likelihood on the history, which is a
one-off M9 exercise, or fixed in bp and reported.

**Meeting-step priors with sparsity.** A Laplace prior on the steps is the fused lasso (Tibshirani et al. 2005)
or, on the levels, ℓ1 trend filtering (Kim, Koh, Boyd and Gorinevsky 2009): the fit is piecewise constant
with few non-zero steps. It is an attractive reading of "how many 25bp moves are priced", solvable as a small
linear programme (SciPy `linprog`, HiGHS). But it is biased by design: a step the market prices at 12bp (half a
move) is pulled to zero or to a full move depending on λ, so it cannot meet a 1bp gate and should be a
diagnostic column, not the estimator. (Judgement.)

**Binary and multinomial trees** (CME FedWatch, the pre-2019 WIRP, Kim and Tanaka 2016, Ceh 2022): the step
path plus an assumption that each meeting is a 0/25bp coin flip with level-independent probabilities.
Bloomberg's own paper on dropping the grid gives the failure modes (percentages above 100% cannot be
probabilities; a 141%-of-a-cut day in August 2019 was shown as 41% of two cuts and 59% of one; a 4.1% futures
blip in November 2019 became a "phantom hike" at every later meeting); Priebsch (2019) shows the same from the
Fed Board side. The tree adds nothing to the expected path, and WIRP no longer shows one. Our deliverable is
WIRP's: post-meeting implied rate, Δ, cumulative number of moves, marginal percent of a move. Probabilities
need option prices (Carlson, Craig and Melick 2005), and D9 rules out option vols.

**Parametric curves** (Nelson-Siegel, Svensson; BIS Papers 25 documents their use by most central banks for
*bond* curves): three to six parameters cannot represent eight dated steps. Not applicable inside the horizon.

**Cost.** GP-as-ridge: nil beyond 2.3. Fused lasso diagnostic: an afternoon. Trees: not needed.

### 2.6 Turn and month-end effects (settled: not nodes)

AC: expected pricing is per meeting; a month-end is not a meeting, so it is not a curve node. Agreed, and WIRP
makes no adjustment either. What remains is a measurement question inside the FF instrument model. The fed
funds rate has calendar effects (Hamilton 1996 *(paywalled)*; Kuttner's revisit in the St Louis Fed Review 2008
finds no month-end effect except on the very last day of the month). Post-2015 the pattern is a month-end dip:
Bowman (FEDS Notes, September 2025) reports that "EFFR declined by about 10 basis points on every month end
from 2016 to February 2018, after which this pattern suddenly stopped in March 2018", because the bill supply
after the debt-limit resolution lifted repo rates and "eliminated the wedge between EFFR and the TGCR". Kim and
Tanaka (2016) simply assumed a 5bp month-end depression when reading FF futures. Arithmetic: a 10bp dip on one
day of a 31-day month lowers the FF monthly average by 0.32bp, a 5bp dip by 0.16bp. Proposal: measure it from
the 2010+ fixings (D7's spread estimator already identifies turn days; the previous attempt's `turn_effects`
table is the right evidence); if it is persistent in some period, the FF instrument model can carry a
per-month expected dip as a switchable deterministic adjustment, reported, and **off** for the WIRP gate.

For the OIS turn of year, Burghardt and Kirshner's "One Good Turn" (RISK 1994 *(paywalled)*) is the classic
treatment and Ametrano and Bianchetti (2013, section 4.8) show it in a bootstrapped OIS curve as a
discount-factor jump; D8 reserves turn nodes for SOFR, €STR, SONIA and TONA. The same fixing measurement says
whether EFFR year-ends matter at all.

### 2.7 Unscheduled meetings (settled: not priced ahead)

AC's point is right and revision 1 overstated this: the curve prices announced meetings, and an unscheduled
decision has no bearing on the curve before it happens precisely because it is unexpected. What survives,
all of it bookkeeping rather than pricing:

1. **A decided unscheduled meeting is a known step at a known date**, not a node to price. For the Fed the
   decision takes effect the next business day (3 Mar 2020 decided, 4 Mar effective), so on the decision day
   itself the stub parcel contains one known step; after the effective date it is in the fixings. The design
   matrix must accept that date (the same code path as any effective date) and the step is flagged
   `unscheduled` in the outputs (CLAUDE.md). No look-ahead: it enters on its decision date.
2. **A scheduled meeting that an emergency meeting superseded** (17-18 March 2020) was an announced meeting
   until 15 March, and the market priced it: for as-of dates before the supersession the curve needs the
   node. This is reference data (M0), not curve logic; the fix is a `superseded_on` column (D-E).
3. **If the market prices a move before the next announced meeting**, as in late February 2020, the step
   model attributes it to the next scheduled node. WIRP does exactly that too ("pushed forward and backward"),
   so the gate is unaffected. The only thing worth doing is to say so in the report when the signature appears
   (a large residual on the current-month contract that no step at the next scheduled date can absorb), as a
   flag, not a node. The provisional-node idea of revision 1 is withdrawn.

### 2.8 Beyond WIRP's horizon: the under-identified region and the OIS-split prior (D4)

Beyond the FF strip's liquid horizon (12 to 18 months) the EFFR OIS at 18M, 2Y and 3Y each span several
meetings, and WIRP shows nothing. D4 says such parcels "take the OIS family's split as prior". My reading, to
be confirmed: the total change across a parcel comes from the OIS quotes, and the division of that change among
the meetings inside it comes from a prior rather than from the data. Candidate priors, all expressible as the
penalty of 2.3:

- *Equal steps in time* (the ridge's minimum-norm solution; what a linear interpolation of the implied path
  gives).
- *Continue the last identified pace* (first-difference penalty).
- *Take the split from the other family* (the SOFR OIS curve has the same tenor grid, so it adds nothing;
  SR3 futures identify quarterly averages to five years, so from M3 on they could inform the split, net of
  their convexity, which is why the SOFR family comes later).
- *Zero steps beyond the last liquid quote* (the "no change" prior), which is what a flat extrapolation of
  the last level does and is clearly wrong when the OIS curve slopes.

For M2 I recommend the equal-step (ridge) prior with the prior-versus-fitted split printed per parcel, because
it is the least informative choice and there is no gate there; the pace prior is one line to switch to if AC
prefers it for the exports. Synthetic meetings beyond the published calendar are nodes like any other,
flagged, and in practice sit entirely in this region. Every meeting beyond WIRP's last shown meeting is
flagged `beyond_wirp_horizon` in the outputs.

### 2.9 Risk premia

The step path is a risk-neutral expectation. The evidence on how far it is from the physical expectation:
Piazzesi and Swanson (2008) find positive and countercyclical excess returns on FF futures; Hamilton (2009)
finds the short-horizon term premium "more sensitive to outliers than earlier research seemed to recognize";
Lloyd (2018) finds 1 to 12-month OIS and FF futures comparably accurate; Kısacıkoğlu (CEPR DP19143, 2024)
finds OIS risk premia "negligible ... up to 1 year, but sizable in longer maturities"; Schmeling, Schrimpf and
Steffensen (BIS WP 996, 2022) attribute excess returns "primarily [to] expectation errors, whereas term premia
are negligible"; Diercks and Carl (FEDS Notes 2019) show that the *choice* of premium model swings an implied
hike probability from 0% to 100%; D'Amico, Kurakula and Sordo Palacios (Chicago Fed Letter 432, 2020) and the
Bank of England (Lengyel and Walker, July 2026) build survey-anchored adjustments. WIRP makes no adjustment.
Conclusion for M2: none in the curve; an optional, clearly labelled adjustment is an analytics layer for later,
and the spec should say the outputs are risk-neutral.

---

## 3. Question 2: unreliable forward-rate observations

### 3.1 What "unreliable" means in this family

From the two days on file and the manifest:

- **Derived, not quoted**: FF settlement prices beyond the traded horizon (1.2). Zero or missing open
  interest and volume identify them. These should be excluded, not down-weighted, and listed in the drop list
  with the reason "no open interest / no volume". WIRP's horizon rule has the same effect.
- **Thin**: FF contracts with open interest in the hundreds or low thousands (the 13th to 18th months in both
  dumps). Their prices are real but move in 0.5bp ticks and lag; weights belong here.
- **Stale**: an unchanged price for several days with no volume (the loader already flags runs beyond
  `stale_days`); OIS tenors that Bloomberg carries from the previous day. Mids only means no bid-ask width to
  read liquidity from, so staleness must be inferred from runs and from volume where it exists.
- **Structurally special**: the front FF contract in its last days (very few days left to average, so the
  quote is almost a fixing); a contract spanning a month-end dip (2.6); the stub parcel.
- **Outside listing**: handled in M1 (blocking) and not a fitting matter.

The common feature is that most unreliability is *predictable from metadata* (OI, volume, days remaining,
staleness run, listing window) before any residual is computed. The literature on robust regression is about
the remaining, unpredictable case.

### 3.2 M-estimators and IRLS: Huber (D4) and Tukey

**What they are.** Replace the squared loss by ρ(r/σ): Huber (1964) is quadratic inside a threshold k and
linear outside (k = 1.345σ gives 95% efficiency at the normal); Tukey's biweight (Beaton and Tukey 1974
*(paywalled)*) is redescending: its weight falls to zero beyond about 4.7σ, so gross outliers are dropped
entirely rather than merely capped. Both are solved by iteratively reweighted least squares (Holland and Welsch
1977 *(paywalled)*): weight w(r) = ψ(r)/r, refit, repeat; σ is the MAD of the residuals, rescaled. Implementations:
`statsmodels.robust.robust_linear_model.RLM` (Huber, Tukey, Hampel and others, with scale estimation) and
`scipy.optimize.least_squares(loss='huber' | 'soft_l1')` for the non-linear OIS case.

**What they assume.** That the bad observations are a minority and show up as large residuals under a fit
dominated by the good ones. Two known failures: *leverage* (a point that alone determines a parameter has a
small residual whatever its error, so no residual-based loss can see it; Rousseeuw 1984 discusses this
"masking"), and *scale* (with 10 to 30 observations the MAD is noisy, and in a quiet strip where all residuals
are 0.2bp a 1bp residual is "an outlier" of 5σ although it is one tick). Both bite in our setting: parcels
pinned by one quote (leverage one), and strips that are often very quiet.

**Behaviour on our data.** On 2026-10-07 the previous attempt's joint Huber fit gave residual RMS of about 1bp,
consistent with tick size and the FF/OIS basis; per instrument the residuals will be smaller still, and Huber
will mostly act as plain weighted least squares and only cap the odd 3bp residual. Tukey would drop such a
quote outright, which is what the drop list is for anyway; the difference matters only for the two-of-a-kind
case (a missing node produces a +3/-3 residual pair, 1.3), where Tukey would drop both quotes and hide the
diagnostic. I prefer Huber for the fit and a reported Tukey-style drop (weight below a threshold after
convergence) for the list, which is D4 as written.

**Cost.** Low; the IRLS loop is ten lines around the weighted solve of 2.1 to 2.3.

**WIRP validation.** Neutral where the strip is clean (the loss is inactive); on a date with a genuinely bad
quote it is the reason we match WIRP rather than the bad quote, and the report must say which quote and why.

### 3.3 High-breakdown estimators: LMS, LTS, MM

Rousseeuw (1984) introduced least median of squares and least trimmed squares (fit the best h of n
observations), which survive up to 50% contamination; Rousseeuw and Van Driessen (2006) give FAST-LTS; an
MM-estimator uses an LTS start and a redescending M-step. For n of 12 to 30 and p of 10 to 20, exhaustive
subset search is feasible, and `sklearn.linear_model.RANSACRegressor` is a cheap stand-in. They solve the
leverage/masking problem of 3.2 by construction.

**But** they are designed for data where half the points may be garbage; ours has a known-good core (the
liquid strip) and a known-bad tail (metadata). With the tail removed by the weights, trimming h of n means
discarding real quotes whose residual is one tick, which biases the fit at exactly the 1bp scale of the gate.
Recommendation: run LTS (or exhaustive leave-k-out) as a diagnostic that produces an independent drop list and
flag disagreements with the Huber list; do not use it as the estimator.

### 3.4 Quantile and LAD regression

Koenker and Bassett (1978 *(paywalled)*; Koenker 2005 *(paywalled book)*): minimise Σ|r| (median regression) or
an asymmetric version; a linear programme, no scale estimate needed, 50% breakdown in the residual direction
but no protection against leverage. On our problem the median fit interpolates p of the n quotes exactly and
ignores the rest, so it is an exact bootstrap with a data-chosen instrument subset: a good diagnostic of which
subset a robust procedure would choose, not a 1bp-accurate estimator (it ignores information from the other
quotes and is non-unique when quotes tie, which at tick granularity they do).

### 3.5 Weights from open interest, volume and staleness; instrument selection

WIRP uses no weights: it *selects* (the non-meeting-month contract for the pre-meeting rate; 1M over 3W "as
it tends to have more liquidity") and stops at the last reliably priced monthly tenor. Precedent for
metadata-driven weights and exclusions in curve fitting: Gürkaynak, Sack and Wright (2007) weight bond prices
by "the inverse of the duration of each individual security" and *exclude* bills, securities under three
months, callables and the two most recently issued securities at each maturity for liquidity reasons rather
than down-weighting them; Lloyd (2018) and Kim and Tanaka (2016) switch from FF futures to OIS beyond one to
two years for the same reason; CME's own liquidity reviews report FF volume and open interest in aggregate
only, so the per-contract numbers in our dumps are the evidence. The previous attempt used
weight = clip(max(OI/50k, volume/20k), 0.05, 1) and stale ×0.1, which is a reasonable shape: saturating (a
contract with 400k open interest is not 20 times better than one with 20k), floored (so that a thin but real
quote still contributes), and multiplicative in staleness. Two refinements:

- Treat "no open interest and no volume" as *missing*, not as the floor weight: those prices are derived
  (1.2) and the floor lets 40 of them vote together.
- Scale the weight into a quote-noise σ in bp (σ_i = σ_instr / sqrt(w_i)) rather than a bare weight, so that
  the prior σ of 2.3 and the Huber k are in the same units and the report can print "this quote was trusted to
  ±x bp".

For OIS, with no OI or volume, the weight comes from staleness alone plus a per-instrument σ; with separate
curves per instrument (1.5) the FF/OIS σ ratio no longer decides anything inside the gate, which removes the
previous attempt's open question 1.

**Cost.** Nil beyond the loader fields (already dumped for the 24 months with `count_fields_months`); the
history is needed to calibrate thresholds, not to run the fit.

### 3.6 Outlier detection and the drop list

Standard regression diagnostics apply, and all are cheap at this size: (i) robust standardised residuals
(residual over MAD scale) after the IRLS converges; (ii) leave-one-out prediction residuals (refit without the
quote and price it), which is the only test that works for a leverage-one quote; (iii) leverage itself (the
diagonal of the hat matrix in the weighted problem), reported so that a reviewer sees which quotes the curve
depends on; (iv) the opposite-sign pair signature of a missing node (1.3); (v) the replica-versus-estimator
difference per meeting, which says what the extra quotes changed. The drop list should carry: the quote, its
weight, its residual before and after dropping, the rule that dropped it (metadata rule, Huber weight below
threshold, leave-one-out beyond tolerance), and what the curve looked like with it in. A drop should trigger a
refit, once. Drops by metadata rules will dominate; drops by residual should be rare and each one is something
AC reviews ("drop list reviewed" is the gate).

### 3.7 State-space and Kalman filtering across days

Durbin and Koopman (2012 *(paywalled book)*) is the reference; Diebold, Rudebusch and Aruoba (2006) is the
yield-curve application (latent factors measured by yields, estimated by the Kalman filter). For us the states
would be the step levels, following random walks between days with a jump on FOMC announcement days, and the
daily quotes are the measurements. Benefits: it smooths tick noise, detects stale quotes as ones whose
innovation is persistently zero while their neighbours move, and gives a time-consistent history. Costs: a
transition noise to tune per state (and much larger on announcement days, or the filter lags by days exactly
when it must not); for as-of use only the *filtered* estimate is admissible (the smoother looks ahead); and the
gate is a same-day comparison with WIRP, which uses no history, so any cross-day pull is a gate miss on event
days. Recommendation: not in M2; use the daily history for what it is needed for now (D7 spread, staleness and
weight calibration), and consider a filter in M9 as a stability diagnostic.

### 3.8 Smoothness priors that stop one bad quote bending its neighbours

Under the step model a quote is local by construction: an FF contract touches at most the two or three parcels
inside its month, an OIS all parcels to its maturity. So a bad FF quote in an over-identified region produces
a residual, not a kink, once the fit is global; a bad quote in a parcel it alone identifies produces a kink that
no loss function can see (3.2) and that only a prior (2.3) or a leave-one-out rule (3.6) can limit. A bad OIS
quote is the dangerous one, because its error is spread over every parcel to its maturity; here the
first-difference penalty of 2.3 limits how much a single long OIS can bend the steps between the previous and
next quoted tenor. Quantifying "how much can one quote move each step" is the hat matrix again (Hagan and West's
"forward stability" measure is the same idea for interpolation), and it should be a standard column: for each
step, the maximum move per bp of each input.

---

## 4. Validation against WIRP

Three layers, per instrument (FF, OIS) and per gate date:

1. **Replication.** Implement WIRP's two models from the Bloomberg documents (sequential bootstrap, its
   selection rules, its conventions: 2-day spot lag, weekend day counts, holidays carried, meeting day at the
   pre-meeting rate) on our own dump data. Compare the replica's Current Implied O/N Rate, Post-Meeting
   Implied Rate, Imp. Rate Δ, #Hikes/Cuts and %Hike/Cut with the WIRP capture for the same pricing date and
   instrument. Pass: every meeting within 1bp. A miss here is a data, convention, calendar or timestamp
   problem (futures 10-minute delay and 6 pm close versus OIS 5 pm; which day a late print belongs to), or a
   selection rule the documents do not spell out; each is explained in `docs/m2_gate.md`.
2. **Estimator versus replica.** Same table for our global weighted Huber fit with the weak prior. The
   difference is the effect of using all the quotes; inside WIRP's horizon it must also be within 1bp, or each
   miss is explained by a named quote the two methods treat differently (listed with its weight and residual).
3. **Basis.** FF-implied minus OIS-implied post-meeting rate per meeting, from both the replica and the
   estimator, stored as a time series. Not gated; it is the diagnostic D5 asks for.

Beyond WIRP's last shown meeting there is no gate; the outputs are flagged and the prior-versus-fitted split
is printed.

Ten dates (as proposed before): 2014-09-16 (zero lower bound), 2015-12-15 (lift-off), 2018-09-25 (hikes),
2019-07-30 (cuts), 2020-03-03 (unscheduled cut decided that day; also tests the superseded 18 March node),
2020-03-16 (first close after the Sunday cut), 2022-06-14, 2023-07-25 (hikes), 2024-09-17 (cuts), 2026-10-07
(already on file). Captures: both models (`WIRP US` and `WIRP US OIS`) per date, with the pricing date set and
the screen showing the instrument. Since WIRP data is tickerised (`US0AFR DEC2019 Index` and so on, with
`BDH` history), a dump of the WIRP tickers for every meeting and day since 2010 would turn the 10-date gate
into a continuous one and would make the replica testable on every day; this is an option for AC (licensing
and effort), not a requirement, and the text captures remain the fixtures the parser is written against.

Which methods can pass layer 1: only the replica. Which can pass layer 2: the step model with weighted (and
lightly robust and lightly penalised) least squares. Which cannot, by design: any smooth interpolant inside the
horizon, sparse-step fits, trimmed fits, and cross-day filters on event days. That is not a criticism of those
methods; it says the gate tests fidelity to the market's step pricing per instrument, which is what D1's
policy-pricing deliverable wants.

---

## 5. Comparison table

| Method | Assumes | On our data (FF monthly averages, EFFR OIS, 8+ meetings, mids) | Cost | WIRP gate | Verdict |
| --- | --- | --- | --- | --- | --- |
| WIRP's sequential bootstrap, per instrument (replica) | rate moves only at effective dates; one quote per node by WIRP's selection rules | exact; ignores the spare quotes; sensitive to the selected quote | low | the reference | **build first; gate layer 1** |
| Flat forwards, global weighted least squares per instrument (D2 + global fit) | same path; quote noise ~ tick; weights from metadata | uses every quote; residuals in bp; local by construction | low | within 1bp of the replica inside the horizon | **estimator** |
| + Tikhonov / ridge on steps or step differences (prior σ in bp) | true steps are small / pace continues; prior weak vs data | negligible inside the liquid strip; selects the split beyond WIRP's horizon; limits leverage | trivial | passes if σ large vs tick; departure printed | **recommended, weak** |
| Joint FF + OIS fit with a basis term | a slowly varying FF/OIS spread | blends two instruments WIRP keeps apart; obscures the gate | low-medium | neither model | later option, not M2 |
| Smoothing splines / VRP on forwards (FNZ, Waggoner) | continuous forwards | smears steps into ramps | low-medium | fails inside horizon | back end only |
| Monotone convex, PCHIP, tension splines | continuous, shape-preserving forwards; one node per quote | same smearing; needs thinning | low | fails inside horizon | D3 junction and beyond (already) |
| Maximum-smoothness forwards | C2 forwards, exact pricing | same, plus known overshoot | low | fails | no |
| GP posterior on step levels | Gaussian prior on steps (= ridge) | same as ridge; adds a σ per meeting | trivial (closed form) | as ridge | report the posterior σ |
| Fused lasso / ℓ1 steps | few non-zero steps of similar size | rounds half-priced moves to 0 or 25bp | low (LP) | fails by design | diagnostic column only |
| Binary trees (FedWatch, pre-2019 WIRP, Riksbank) | 0/25bp per meeting, level-independent p | same path as D2; Bloomberg dropped it for the reasons in its paper | n/a | n/a | not needed |
| Nelson-Siegel / Svensson | 3-6 smooth parameters | cannot hold 8 dated steps | low | fails | no |
| Huber IRLS (D4) | few large residuals; scale from MAD | mostly inactive at ~1bp RMS; caps odd 3bp residual; blind to leverage | low | neutral / protective | **keep** |
| Tukey biweight | as Huber, redescending | drops a +3/-3 missing-node pair, hiding the diagnostic | low | neutral | its threshold for the drop list only |
| LTS / LMS / MM | up to 50% garbage | discards tick-level-good quotes; biased at 1bp scale | medium (small n: cheap) | risks misses | diagnostic drop list |
| Quantile / LAD | median fit, LP | interpolates p quotes exactly; non-unique at tick ties | low | risks misses | diagnostic |
| Metadata weights and exclusions (OI, volume, staleness, days remaining) | unreliability is predictable | identifies the derived far strip and thin months before fitting | nil | protective | **do most of the work**; no-OI/no-volume = missing |
| Leave-one-out, leverage, residual-pair signature, replica difference | standard diagnostics | finds the leverage-one and missing-node cases | low | explains misses | **in the battery** |
| Kalman filter across days | random-walk steps, jumps on FOMC days | smooths tick noise; lags on event days unless tuned; look-ahead if smoothed | medium | misses on event days | M9 stability diagnostic |
| Month-end dip adjustment in the FF model | measured fixing effect, ~0.2-0.3bp on a monthly average 2016-18 | not a node (AC); WIRP makes none | low | off for the gate | measure; switchable |
| Provisional node for an expected inter-meeting move | — | withdrawn (2.7) | — | — | no; flag in the report |

---

## 6. Recommendation and decisions needed

**On D2 (flat forwards between effective dates; synthetic meetings to 3y, flagged): agree, unchanged.** The
design matrix accepts, besides scheduled effective dates, a decided unscheduled meeting's effective date from
its decision date and a superseded scheduled meeting until its supersession date. No other node types.

**On D4 (OIS split as prior for under-identified parcels; Huber IRLS with liquidity/staleness weights and a
reported drop list): agree, applied per instrument, with these changes of emphasis.**

1. Two step curves per as-of date within the EFFR family, FF-based and OIS-based, as WIRP's two models; the
   basis per meeting is a stored diagnostic (D5's treatment, one level down). No blended curve in M2.
2. Each curve is one global weighted least-squares problem on the step levels with a per-instrument quote σ
   in bp and per-quote weights from open interest, volume, days remaining and staleness. Quotes with no open
   interest and no volume are excluded as derived prices, not floored.
3. Huber IRLS on top, k = 1.345, scale from the MAD with a floor at the tick size. The drop list is built
   from the metadata rules first, then from Huber weights below a threshold, then from leave-one-out
   residuals, each with its reason; one refit after dropping.
4. A weak Gaussian prior on each step (σ_prior of order 10bp, reported), which makes the region beyond WIRP's
   horizon well-posed with an equal-step split, caps the damage from a leverage-one quote, and yields a
   posterior σ per meeting. The prior-versus-fitted split is printed wherever it binds.
5. WIRP's own sequential bootstrap is implemented per instrument as the replica and is gate layer 1; the
   estimator is gate layer 2 against the replica; leverage, leave-one-out and the replica difference are
   standard columns in the quality battery.
6. Outputs per meeting follow WIRP's definitions (Current Implied O/N Rate from the instrument, Post-Meeting
   Implied Rate, Imp. Rate Δ, cumulative #moves, marginal %move) plus the brief's "cumulative change versus
   the current target" and the D7 policy-rate conversion, each labelled; meetings beyond WIRP's horizon,
   synthetic meetings and unscheduled steps flagged.

**Decisions needed from AC** (also listed in the PR):

- D-A. Confirm D2 as read above (two extra node types, nothing else).
- D-B. Confirm items 1-6 as the M2 fit: separate FF and OIS curves; exclusion of no-OI/no-volume FF prices;
  Huber with a tick-size scale floor; the weak ridge prior with an equal-step split beyond WIRP's horizon;
  the WIRP replica as the gate reference; WIRP's output definitions plus ours.
- D-C. What "OIS family's split" in D4 means beyond WIRP's horizon: equal steps in time (my default), continue
  the last pace, or the SOFR family's split (then it is an M3 input).
- D-D. Resolved by AC: separate instruments. Remaining question: should `usd.yaml` express this as two
  sub-curves of the `effr` family (`effr_fut`, `effr_ois`) or as a per-instrument flag? (Config shape only.)
- D-E. M0 schema: add a `superseded_on` column to `data/refdata/meetings/fed.csv` so that 17-18 March 2020
  exists for as-of dates before 15 March 2020 (and equivalents for other banks if any).
- D-F. Resolved by AC: month-end is not a node. Remaining: the FF instrument model may carry a switchable,
  measured month-end adjustment, off by default and off for the gate. OK?
- D-G. The ten gate dates (section 4), or substitutes; captures for both models per date.
- D-H. Diagnostics to include in the battery as extra columns (fused-lasso move count, LTS drop list,
  quantile fit) versus leaving them out of M2.
- D-I. Optional: dump the WIRP tickers (both models, all meeting tails) from 2010 via `dump_bloomberg.py`
  (a `wirp` group in the manifest) so the replica can be checked on every day, not ten. Licensing and effort
  are AC's call; the text captures stay the fixtures either way.
- D-J. The Bloomberg "Calculations" document builds the OIS model on `ICVS 42`; D14 names Fed Funds curve 85.
  Which curve feeds `USSO*` and which should the replica match?

---

## 7. Sources

Free copies are linked where I found one; *(paywalled)* marks the ones I could not open and cite from the
abstract or from secondary descriptions. cmegroup.com pages are not fetched by script (see README); their
quotes above come from search snippets and should be checked against the page.

**Bloomberg WIRP (gate standard; copies in `docs/research/wirp/`, terminal-only, not redistributable)**

- Bloomberg, *WIRP <GO> World Interest Rate Probability Help Page*, prepared 10/09/2026 (16 pages).
- Bloomberg, *Calculations* (WIRP futures and OIS models, 17 pages).
- Bloomberg, *WIRP: Estimating the Path of Central Bank Hikes and Cuts* (9 pages).

**Step functions, meeting-dated expectations, practitioner tools**

- CME Group, *Understanding the CME Group FedWatch Tool methodology* (2023), https://www.cmegroup.com/articles/2023/understanding-the-cme-group-fedwatch-tool-methodology.html ; and the *Fed Funds futures probability tree calculator* page, https://www.cmegroup.com/education/demos-and-tutorials/fed-funds-futures-probability-tree-calculator.html (not fetched by script).
- CME Group, SER-8105 (2018), 30-Day Fed Funds daily settlement amendment, https://www.cmegroup.com/notices/ser/2018/04/SER-8105.pdf
- Kim, D. H. and H. Tanaka (2016), "Front-end term premiums in federal funds futures rates and implied probabilities of future rate hikes", FEDS Notes, 18 Nov 2016, https://federalreserve.gov/econresdata/notes/feds-notes/2016/front-end-term-premiums-in-federal-funds-futures-rates-and-implied-probabilities-of-future-rate-hikes-20161118.html
- Priebsch, M. A. (2019), "A new way to visualize the evolution of monetary policy expectations", FEDS Notes, 20 Sep 2019, https://www.federalreserve.gov/econres/notes/feds-notes/new-way-to-visualize-the-evolution-of-monetary-policy-expectations-20190920.html
- Ceh, A. M. (2022), "How much is priced in? Market expectations of monetary policy lift", Sveriges Riksbank Staff Memo, Dec 2022, https://www.riksbank.se/globalassets/media/rapporter/staff-memo/svenska/2022/staff-memo-how-much-is-priced-in-market-expectations-of-monetary-policy-lift.pdf
- Syrstad, O. and D. Rime (2014), Norges Bank Staff Memo 6/2014 (FRA-based expectations, IMM dates), https://www.norges-bank.no/contentassets/a642411c06344dd180beaf3dd613ba7b/staff_memo_2014_6.pdf
- ECB Money Market Contact Group (2023), "Drivers of euro interest rate expectations" (maintenance-period-dated OIS forwards), https://www.ecb.europa.eu/paym/groups/pdf/mmcg/20230302/Drivers_of_euro_interest_rate_expectations.en.pdf
- Lengyel, A. and D. Walker (2026), "Bank Rate expectations in the UK curve following the war in Iran", Bank of England Bank Insights, 17 Jul 2026, https://www.bankofengland.co.uk/bank-insights/2026/bank-rate-expectations-uk-curve-following-the-war-in-iran
- Freitas, W., R package `copom`: flat-forward interpolation on COPOM dates, https://wilsonfreitas.github.io/copom/articles/copom.html
- QuantLib, `ql/termstructures/globalbootstrap.hpp` (SoftSolutions 2019, Caspers 2025), https://github.com/lballabio/QuantLib/blob/master/ql/termstructures/globalbootstrap.hpp
- Ametrano, F. M. and M. Bianchetti (2013), "Everything you always wanted to know about multiple interest rate curve bootstrapping but were afraid to ask", SSRN 2219548, https://ssrn.com/abstract=2219548 ; QuantLib Python Cookbook, EONIA chapter (turn-of-year jumps), https://leanpub.com/read/quantlibpythoncookbook/leanpub-auto-eonia-curve-bootstrapping
- Carlson, J. B., B. R. Craig and W. R. Melick (2005), "Recovering market expectations of FOMC rate changes with options on federal funds futures", Cleveland Fed WP 05-07 (options; excluded by D9), https://www.clevelandfed.org/publications/working-paper/wp-0507-recovering-market-expectations-of-fomc-rate-changes

**FF futures and OIS as measures of expectations; risk premia; the FF/OIS comparison**

- Kuttner, K. N. (2001), "Monetary policy surprises and interest rates: evidence from the Fed funds futures market", JME 47(3) *(paywalled)*; NY Fed Staff Report 99 (free), https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr99.pdf
- Gürkaynak, R. S. (2005), "Using federal funds futures contracts for monetary policy analysis", FEDS 2005-29, https://www.federalreserve.gov/econres/feds/using-federal-funds-futures-contracts-for-monetary-policy-analysis.htm
- Gürkaynak, R. S., B. Sack and E. T. Swanson (2007), "Market-based measures of monetary policy expectations", JBES 25(2) *(paywalled)*; FRBSF WP 2006-04 (free), https://www.frbsf.org/wp-content/uploads/wp06-04bk.pdf
- Durham, J. B. (2003), "Estimates of the term premium on near-dated federal funds futures contracts", FEDS 2003-19, https://www.federalreserve.gov/econres/feds/estimates-of-the-term-premium-on-near-dated-federal-funds-futures-contracts.htm
- Piazzesi, M. and E. T. Swanson (2008), "Futures prices as risk-adjusted forecasts of monetary policy", JME 55 *(paywalled)*; author copy, https://web.stanford.edu/~piazzesi/fff.pdf
- Hamilton, J. D. (2009), "Daily changes in Fed funds futures prices", JMCB 41(4) *(paywalled)*; NBER WP 13112, https://www.nber.org/papers/w13112.pdf
- Lloyd, S. P. (2018), "Overnight index swap market-based measures of monetary policy expectations", Bank of England SWP 709, https://www.bankofengland.co.uk/-/media/boe/files/working-paper/2018/overnight-index-swap-market-based-measures-of-monetary-policy-expectations.pdf
- Joyce, M., J. Relleen and S. Sorensen (2008), "Measuring monetary policy expectations from financial market instruments", Bank of England WP 356 / ECB WP 978, https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp978.pdf
- Priebsch, M. A. (2017), "A shadow rate model of intermediate-term policy rate expectations", FEDS Notes, https://www.federalreserve.gov/econres/notes/feds-notes/shadow-rate-model-of-intermediate-term-policy-rate-expectations-20171004.htm
- Diercks, A. and E. Carl (2019), "A simple macro-finance measure of risk premia in fed funds futures", FEDS Notes, https://www.federalreserve.gov/econres/notes/feds-notes/simple-macro-finance-measure-of-risk-premia-in-fed-funds-futures-20190108.htm
- D'Amico, S., V. Kurakula and S. I. Sordo Palacios (2020), "A risk-premium adjustment to the policy rate path", Chicago Fed Letter 432, https://www.chicagofed.org/publications/chicago-fed-letter/2020/432
- Schmeling, M., A. Schrimpf and S. A. M. Steffensen (2022), "Monetary policy expectation errors", BIS WP 996, https://www.bis.org/publ/work996.htm
- Kısacıkoğlu, B. (2024), "Overnight index swaps and monetary policy expectations in the US", CEPR DP19143 *(paywalled)*, https://cepr.org/publications/dp19143
- Skov, J. B. and D. Skovmand (2023), "Decomposing LIBOR in transition: evidence from the futures markets", Quantitative Finance 23(6) *(paywalled)*; arXiv 2201.06930 (free), https://arxiv.org/abs/2201.06930
- CFTC Commitments of Traders, legacy futures report, CBOT Fed Funds (code 045601), https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm

**Fed funds calendar and month-end effects**

- Bowman, D. (2025), "The fed funds market during the quantitative tightening of 2017-19", FEDS Notes, 19 Sep 2025, https://www.federalreserve.gov/econres/notes/feds-notes/the-fed-funds-market-during-the-quantitative-tightening-of-2017-19-20250919.html
- Hamilton, J. D. (1996), "The daily market for federal funds", JPE 104(1) *(paywalled)*; Kuttner's revisit, St Louis Fed Review (2008), https://files.stlouisfed.org/research/publications/review/08/07/Kuttner.pdf
- Burghardt, G. and S. Kirshner (1994), "One good turn", RISK, Nov 1994 *(paywalled)*; summary at Clarus, https://www.clarusft.com/year-end-turn-rates

**Interpolation and regularisation**

- Hagan, P. S. and G. West (2006), "Interpolation methods for curve construction", Applied Mathematical Finance 13(2) *(paywalled)*; free copy, https://bank.uni-hohenheim.de/uploads/media/Hagan_and_West__2006__-_Interpolation_Methods_for_Curve_Construction.pdf ; and (2008) "Methods for constructing a yield curve", Wilmott, May 2008.
- du Preez, P. F. and E. Maré (2013), "Interpolating yield curve data in a manner that ensures positive and continuous forward curves", SAJEMS 16(4), https://scielo.org.za/pdf/sajems/v16n4/03.pdf
- Fritsch, F. N. and R. E. Carlson (1980), "Monotone piecewise cubic interpolation", SIAM J. Numer. Anal. 17(2) *(paywalled)*; Fritsch, F. N. and J. Butland (1984), SIAM J. Sci. Stat. Comput. 5 *(paywalled)*; SciPy `PchipInterpolator`, https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.PchipInterpolator.html
- Andersen, L. (2007), "Discount curve construction with tension splines", Review of Derivatives Research 10(3) *(paywalled)*, https://link.springer.com/article/10.1007/s11147-008-9021-2 ; Andersen, L. and V. Piterbarg (2010), *Interest Rate Modeling*, vol. 1 *(paywalled book)*
- Adams, K. J. and D. R. van Deventer (1994), "Fitting yield curves and forward rate curves with maximum smoothness", J. Fixed Income 4(1) *(paywalled)*; Lim, K. G. and Q. Xiao (2002), Statistics and Computing 12 *(paywalled)*; Manzano, J. and J. Blomvall, "Positive forward rates in the maximum smoothness framework", https://arxiv.org/abs/math/0305307
- Fisher, M., D. Nychka and D. Zervos (1995), "Fitting the term structure of interest rates with smoothing splines", FEDS 95-1, https://www.fedinprint.org/item/fedgfe/34856/original
- Waggoner, D. F. (1997), "Spline methods for extracting interest rate curves from coupon bond prices", Atlanta Fed WP 97-10, https://www.frbatlanta.org/research/publications/wp/1997/10
- BIS (2005), *Zero-coupon yield curves: technical documentation*, BIS Papers 25, https://www.bis.org/publ/bppdf/bispap25.htm
- Tanggaard, C. (1997), "Nonparametric smoothing of yield curves", Review of Quantitative Finance and Accounting 9(3) *(paywalled)*; Linton, O., E. Mammen, J. Nielsen and C. Tanggaard (2001), "Yield curve estimation by kernel smoothing methods", J. Econometrics 105 *(paywalled)*; LSE eprint, https://eprints.lse.ac.uk/1640/
- Hansen, P. C. (1992), "Analysis of discrete ill-posed problems by means of the L-curve", SIAM Review 34(4) *(paywalled)*; Hansen, P. C. and D. P. O'Leary (1993), "The use of the L-curve in the regularization of discrete ill-posed problems", https://www.cs.umd.edu/users/oleary/reprints/j37.pdf
- Gürkaynak, R. S., B. Sack and J. H. Wright (2007), "The U.S. Treasury yield curve: 1961 to the present", JME 54(8) *(paywalled)*; FEDS 2006-28 (free), https://www.federalreserve.gov/PUBS/feds/2006/200628/200628pap.pdf

**Bayesian, Gaussian-process and sparse priors**

- Kimeldorf, G. S. and G. Wahba (1970), "A correspondence between Bayesian estimation on stochastic processes and smoothing by splines", Ann. Math. Statist. 41(2), https://projecteuclid.org/euclid.aoms/1177697089
- Wahba, G. (1990), *Spline Models for Observational Data*, SIAM *(paywalled book)*
- Rasmussen, C. E. and C. K. I. Williams (2006), *Gaussian Processes for Machine Learning*, MIT Press (free online), https://gaussianprocess.org/gpml/chapters
- Filipović, D., "Smith-Wilson as a Gaussian process posterior" (AFIR slides), https://actuaries.ch/de/downloads/aid!b9f3124e-8a75-4721-b157-1fc861a86858/id!1110/AFIR-D.%20Filipovic.pdf
- Tibshirani, R., M. Saunders, S. Rosset, J. Zhu and K. Knight (2005), "Sparsity and smoothness via the fused lasso", JRSS B 67(1) *(paywalled)*, https://ideas.repec.org/a/bla/jorssb/v67y2005i1p91-108.html
- Kim, S.-J., K. Koh, S. Boyd and D. Gorinevsky (2009), "ℓ1 trend filtering", SIAM Review 51(2), https://web.stanford.edu/~boyd/papers/l1_trend_filter.html
- Diebold, F. X., G. D. Rudebusch and S. B. Aruoba (2006), "The macroeconomy and the yield curve: a dynamic latent factor approach", J. Econometrics 131, https://www.sas.upenn.edu/~fdiebold/papers/paper55/DRAfinal.pdf ; Durbin, J. and S. J. Koopman (2012), *Time Series Analysis by State Space Methods*, 2nd ed., OUP *(paywalled book)*

**Robust estimation**

- Huber, P. J. (1964), "Robust estimation of a location parameter", Ann. Math. Statist. 35(1), https://projecteuclid.org/euclid.aoms/1177703732 ; Huber, P. J. and E. M. Ronchetti (2009), *Robust Statistics*, 2nd ed., Wiley *(paywalled book)*
- Holland, P. W. and R. E. Welsch (1977), "Robust regression using iteratively reweighted least-squares", Communications in Statistics 6(9) *(paywalled)*
- Beaton, A. E. and J. W. Tukey (1974), "The fitting of power series, meaning polynomials, illustrated on band-spectroscopic data", Technometrics 16(2) *(paywalled)*
- Rousseeuw, P. J. (1984), "Least median of squares regression", JASA 79 *(paywalled)*; free copy, https://www.eecs.yorku.ca/course_archive/2010-11/W/6338/lectures/LeastMedianOfSquares.pdf ; Rousseeuw, P. J. and K. Van Driessen (2006), "Computing LTS regression for large data sets", Data Mining and Knowledge Discovery 12 *(paywalled)*, https://doi.org/10.1007/S10618-005-0024-4
- Koenker, R. and G. Bassett (1978), "Regression quantiles", Econometrica 46(1) *(paywalled)*, https://www.econometricsociety.org/publications/econometrica/1978/01/01/regression-quantiles ; Koenker, R. (2005), *Quantile Regression*, CUP *(paywalled book)*
- statsmodels `RLM` (Huber, Tukey, Hampel norms with scale estimation), https://www.statsmodels.org/stable/rlm.html ; SciPy `least_squares` robust losses, https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html

**Data facts used above**

- `data/market/usd/2019/*.csv`, `data/market/usd/2026/*.csv` (two dump days), `data/refdata/meetings/fed*.csv`, the M1 manifest (`stircurve/config/usd_manifest.yaml`); PR #3 (closed) for the previous attempt's residual and leverage findings.
