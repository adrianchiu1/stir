# Front-end curve construction: state of the art and a recommendation (M2, phase A)

Purpose: a review AC can decide from, on two questions, before any M2 curve code is written.

1. How to build the front-end forward curve when there are more instruments than nodes.
2. How to treat unreliable forward-rate observations (illiquid, stale or derived prices that put kinks in the curve).

Scope: the USD EFFR family (FF futures and EFFR OIS, mids only, eight scheduled FOMC meetings a year plus
unscheduled ones), with an eye to the other three banks and the next 18 currencies. Everything below is
sourced where it can be; where a statement is my own judgement it says so. Paywalled sources are marked
*(paywalled)*; everything else links to a free copy. Section 7 lists every source with a link.

Decisions this memo asks AC to take are collected in section 6.

---

## 0. Summary

**Keep D2.** Piecewise-flat forwards between policy effective dates is what every practitioner tool and every
central-bank note I found uses to read meeting-by-meeting expectations from FF futures and OIS: CME FedWatch,
Bloomberg WIRP (a binary tree on the same step path), the Fed Board's own notes (Kim and Tanaka 2016, Priebsch
2019), the Riksbank's RIBA method (Ceh 2022), the ECB's maintenance-period-dated OIS forwards, the R `copom`
package for BRL and QuantLib's `GlobalBootstrap`. The classic objection to flat forwards (Hagan and West 2006:
discontinuous forwards "imply implausible expectations about future short-term interest rates") does not apply
here, because the discontinuities sit exactly where the policy rate can change. Smooth interpolants (monotone
convex, PCHIP, tension or smoothing splines) are the right tool beyond the meeting horizon (D3), not inside it:
they smear a step across neighbouring parcels and would fail a 1bp WIRP gate by construction.

**Keep D4, with two additions and one change of emphasis.** A robust IRLS fit (Huber) with liquidity and
staleness weights is the standard way to use an over-identified strip; what the literature and our own two
days of data say is that (a) the weights should do most of the work and the robust loss should be a backstop,
because the unreliable quotes are predictable from open interest, volume and staleness rather than surprising;
(b) a Huber loss cannot protect a parcel that only one quote identifies (leverage one): those quotes need a
prior and a leave-one-out diagnostic, not a loss function; and (c) a weak Gaussian prior on the steps
(equivalently a Tikhonov/ridge penalty, or a Gaussian-process posterior) is the cheapest way to make the
under-identified region well-posed, to give every meeting a credible interval, and to stop one bad quote from
bending its neighbours. The prior should be weak enough that where the market identifies a step the posterior
moves by far less than 1bp (the gate), and it should be reported next to the fitted value wherever it binds.

**What to drop, and what to keep as diagnostics only.** Least-trimmed-squares, quantile (LAD) fits and
fused-lasso (sparse 25bp step) fits are worth running as *diagnostics* in the quality battery (they give an
independent drop list and a "number of moves" reading) but not as the estimator, because each is biased
against partially-priced moves and so would fail the gate. Kalman filtering across days is a sensible M9
stability tool, not an M2 estimator: WIRP is a same-day exact read, and any cross-day smoothing moves us away
from it on exactly the FOMC days that matter.

**Two things the step model cannot do, which the gate dates must expose:** an unscheduled meeting that has not
yet been announced has no node (the market's inter-meeting pricing lands on the next scheduled node, as in
late February 2020), and the EFFR month-end dip (about 10bp on month-ends from 2016 to February 2018 per
Bowman 2025, roughly 0.3bp on a monthly FF average) is a fixing effect, not a policy step, and belongs in the
instrument model as a measured adjustment rather than in the curve as a turn node (D8 already excludes an EFFR
turn node; I recommend measuring it from the 2010+ fixings before confirming that).

---

## 1. The problem in our terms

### 1.1 What the instruments identify

A front-end curve for the EFFR family is a function of the daily EFFR forward. Under D2 it is piecewise
constant between effective dates, so its parameters are: one stub level (EFFR from the as-of date to the first
effective date) and one post-meeting level per meeting inside the horizon. Each FF contract prices the
arithmetic average of the daily EFFR over a calendar month (CBOT chapter 22, captured in the M1 manifest); each
EFFR OIS prices the compounded EFFR from spot to maturity. Both are linear (FF) or very nearly linear (OIS, in
the rates) in the step levels, so the fit is a small linear or mildly non-linear least-squares problem.

Counting on the two real days on file (a scratch script over the dumps under `data/market/usd`; counts include the
meetings that were later known, which the previous attempt's "from decision date" rule would exclude):

| As-of | FF contracts quoted | with open interest | with volume | effective dates in first 12 / 18 / 24 contracts | spare degrees of freedom at 12 / 18 / 24 |
| --- | --- | --- | --- | --- | --- |
| 2019-06-12 | 36 | 24 (OI < 1,000 beyond the 18th) | 20 | 10 / 14 / 18 | +1 / +3 / +5 |
| 2026-10-07 | 60 | 17 | 24 (seven of them zero) | 8 / 10 / 10 | +3 / +7 / +13 |

"Spare degrees of freedom" is quotes minus (stub + steps). The first year is always over-identified by the FF
strip alone, and the EFFR OIS adds 17 more quotes inside two years (1W, 2W, 3W, 1M to 11M, 1Y, 18M, 2Y). Beyond
the published FOMC calendar the count of steps is set by cadence extrapolation (synthetic meetings, D2), and
beyond about 18 months the FF strip stops carrying information (next paragraph), so the curve is
over-identified in the first 12 to 18 months and under-identified beyond, where only 18M, 2Y and 3Y OIS remain
and each parcel between them holds four meetings. Both halves of D4 are therefore needed on every date.

### 1.2 What the far FF strip actually is

On 2026-10-07 the dump has 60 FF prices but open interest on only 17 and non-zero volume on 17. From the 19th
contract on, the month-to-month changes repeat with a 12-month period (+4bp into April, +8bp into August, 0
into September, +0.5 into October, ...) in 2028, 2029, 2030 and 2031 identically. Those are not quotes; they
are the exchange's derived daily settlement prices for untraded months (CME settles deferred months by a
procedure rather than by trades; the front-month procedure is documented in CME's 2018 notice SER-8105 and the
client-systems wiki, and the deferred-month procedure is not public as far as I can find). This is the single
most important fact for question 2: the unreliable observations in this family are mostly *known in advance*
from the liquidity fields and from the listing model, and the fit should treat them as missing, not as noisy.
Lloyd (2018, BoE SWP 709) states the same from the research side: FF futures "have historically been illiquid
at horizons in excess of 1 year", while OIS "tend to be liquid out to at least the 3-year horizon".

### 1.3 What the previous attempt found (PR #3, closed by AC with "redoing this stage")

Those numbers are still informative about the data even though the code was discarded:

- A joint Huber fit on 2026-10-07 with 0.5bp quote noise on both families left FF residuals with an RMS of
  0.97bp and OIS residuals of 1.37bp. Fitting FF alone moved implied meeting rates by up to 1.5bp in the first
  year (0.85bp on 2019-06-12); fitting OIS alone moved them by up to 10bp inside two years. The two families
  disagree by a basis that is itself larger than the gate tolerance, so the gate must know which instrument
  each WIRP capture is based on.
- On 2019-06-12 the only large FF residuals were February 2020 (+3.0bp) and April 2020 (-2.8bp), on either
  side of the scheduled 17-18 March 2020 meeting, which is absent from `data/refdata/meetings/fed.csv` because
  the 15 March emergency meeting superseded it. A missing node shows up as a residual pair of opposite sign: a
  useful signature for the quality battery.
- A quote that alone pins a parcel has leverage near one; its error moves the curve rather than the residual,
  and a Huber loss then blames its neighbours.

### 1.4 What WIRP is, as far as public sources say

Bloomberg does not publish the WIRP methodology; the terminal help page is the only primary source and AC will
need to read it there. Public descriptions conflict on the input: the HKMA (Research Memorandum 01/2019,
footnote 7) says WIRP derives "FOMC decision probability ... from OIS by assuming i) the outcome of future FOMC
is either no change or a fixed hike/cut, ii) the EFFR after a rate change is the mid-point of the target range,
and iii) linear interpolation"; the Fed Board's Priebsch (2019) describes "Bloomberg's binary tree model fit to
federal funds futures rates" and groups WIRP with CME FedWatch as models that "rely on a single piece of
information per FOMC meeting", the futures-implied rate after that meeting; a 2015 practitioner note (Chandler)
says it also used FF options. My reading: the instrument is a user setting (OIS or FF futures), the path is a
step function at meeting dates, the "implied rate" column is the post-meeting rate under that step function,
and the probabilities come from a binary tree on top of it. Two consequences for the gate:

- The comparison target is the per-meeting implied rate (and the cumulative change in 25bp units), not the
  probabilities. A method that reproduces the step path reproduces WIRP's probabilities as well.
- WIRP's path is an *exact* read of its instrument (one value per meeting, linear interpolation between quoted
  tenors where a parcel holds more than one meeting). Any regularisation we add is a deliberate departure from
  WIRP, so it must be small where WIRP's input is liquid and only bind where WIRP itself is interpolating.

Each WIRP capture must therefore include the line that names its source instrument (previous attempt, item 1),
and the gate should compare like with like: our FF-weighted fit against an FF-based WIRP, our OIS-weighted fit
against an OIS-based one, with the cross-comparison reported as the basis.

---

## 2. Question 1: more instruments than nodes

### 2.1 Piecewise-flat forwards between effective dates (D2)

**What it assumes.** The overnight rate can change only on policy effective dates (and on dates we add
deliberately: turns, unscheduled meetings once announced), and is otherwise expected to be constant. The
expectation is risk-neutral: risk premia are not removed (section 2.9).

**Who uses it.** CME FedWatch: "rate hikes/cuts are uniformly sized in increments of 25bps", "for months with
meetings, the corresponding monthly Fed Funds futures contract price is used to calculate the probabilities",
and "the projected end rate for EFFR in each month should be equal to the start rate for EFFR in the subsequent
month" (CME methodology page; cmegroup.com refuses scripted access, so these quotes come from search snippets
and AC may want to copy the page by hand as with the M1 pages). Kim and Tanaka (FEDS Notes, 2016): "the federal
funds target rate/range changes are discrete and occur only on FOMC meeting dates"; they use FF futures and
switch to OIS "for horizons beyond about two years" on liquidity grounds, and assume the EFFR is depressed 5bp
at month-ends. Riksbank (Ceh 2022): the policy rate "can shift solely at the very few predetermined dates --
implementation dates, and in predetermined, regular, discrete sized steps, and is therefore better suited to be
described by the step-function instead of via the smooth curve"; a RIBA quarter with two meetings is split by
day-weighting both steps inside the quarter, with the identification closed by the probability tree. The ECB's
Money Market Contact Group reads the terminal rate as "the maximum of the Maintenance Period-dated OIS forward
contracts". The R `copom` package (Freitas) implements flat-forward interpolation on COPOM dates for BRL DI
futures and lists four ways to resolve two futures between the same pair of meetings (first, second, forward
between them, or an optimisation), a precedent for a currency on our list. QuantLib's `GlobalBootstrap`
(SoftSolutions 2019, Caspers 2025) solves all nodes at once by Levenberg-Marquardt on a weighted vector of
quote errors with optional `additionalDates` (meeting dates) and `additionalPenalties`, which is the exact
structure of a regularised step fit.

**Properties.** Hagan and West (2006) call it "raw interpolation" (linear in log discount factors): "This method
is very stable, is trivial to implement, and is usually a base method one implements in a system before any
others." It is perfectly local (a quote can only move the steps whose parcels it covers) and its hedges are
local. Its one defect in their framework, discontinuous forwards, is the feature we want: McCulloch and
Kochin's objection that a discontinuous forward curve "implies either implausible expectations about future
short-term interest rates, or implausible expectations about holding period returns" is an objection to jumps
at arbitrary instrument maturities, not at dates when the central bank meets.

**Behaviour on our data.** Exact (bootstrapped) version: N quotes, N nodes, so in the over-identified first year
some quotes must be left out, and the result depends on which (the `copom` package's four options). Global
version (one least-squares problem): uses all quotes, leaves residuals in bp per instrument, and is the natural
host for weights, a robust loss and priors. Either way a meeting inside a month is handled by day-weighting the
pre- and post-meeting levels, which is exactly the Kuttner (2001) decomposition and the FedWatch formula. Both
the stub level and the first step are identified mostly by the front contract, whose remaining days shrink
through the month; the quality report should show the front contract's weight in days.

**Cost.** Low: a design matrix (days of each parcel inside each instrument window, from the contract table and
the fixing calendar), weighted least squares, Gauss-Newton for the OIS compounding. Everything needed exists
after M0/M1.

**WIRP validation.** This is WIRP's own model, so the comparison is clean: per meeting, our implied rate minus
WIRP's, on the same instrument. Differences come from (i) quote timestamps (settlement versus WIRP's snapshot),
(ii) which contracts each side uses, (iii) regularisation and weights, (iv) the stub (WIRP uses the current
EFFR; we use the fixing plus the D7 spread for the stub parcel).

### 2.2 Exact bootstrap versus global least squares

An exact bootstrap (QuantLib's `PiecewiseYieldCurve` with `BackwardFlat` forwards, Ametrano and Bianchetti
2013 for the multi-curve version) needs one instrument per node and raises an error otherwise; practitioners
then thin the instrument set by hand. A global fit (Hagan and West 2006 section on "best fit" curves, QuantLib
`GlobalBootstrap`, Andersen and Piterbarg 2010 vol. 1 ch. 6 *(paywalled book)*) minimises a weighted sum of
squared quote errors over all nodes at once. With the step model the global fit is linear in the FF quotes and
the "bootstrap" is just the special case of zero residuals. I see no reason to thin by hand when the weights
and the drop list can do it reproducibly, and every method in this memo is a choice of loss, weights and
penalty inside the global fit. (Judgement.)

### 2.3 Regularised fits: Tikhonov, ridge and smoothing penalties

**What they are.** Add λ·‖L θ‖² to the weighted sum of squares, where θ are the step levels (or the steps
themselves) and L encodes a belief: L = I on the steps shrinks every move toward zero ("no change" prior, which
is what a flat extrapolation of the last identified level amounts to); L = first differences of the steps
shrinks toward a constant pace ("continue the cycle"); L = second differences shrinks toward a linear path. λ
is chosen by generalised cross-validation (Fisher, Nychka and Zervos 1995; Tanggaard 1997), by the L-curve
(Hansen 1992 *(paywalled)*; Hansen and O'Leary 1993), or by fixing the prior standard deviation in bp, which
is the same thing in Bayesian clothing (section 2.5). Waggoner (1997) and the Bank of England's variable
roughness penalty (BIS Papers 25, 2005) let λ vary with maturity: small where instruments are dense, large
where they are sparse, which is precisely our shape (dense FF strip, then three OIS points).

**What they assume.** That the true path is closer to the penalised shape than the data alone say. In the
over-identified region a small λ barely moves the fit (the data dominate); in the under-identified region the
penalty is what picks the solution, so its form *is* the answer there.

**Behaviour on our data.** With L = I and a prior σ of, say, 10bp per step (the previous attempt's default),
a step identified by a liquid FF pair with 0.5bp noise moves by about (0.5/10)² ≈ 0.25% of its value, well
inside 1bp. Beyond 18 months, where only 18M, 2Y and 3Y OIS exist, a parcel's total change is identified but
its split across four meetings is not; the ridge gives the minimum-norm split (equal steps), the
first-difference penalty continues the last pace. Neither is "right"; WIRP's linear interpolation is the
equal-step answer. The penalty also fixes the leverage problem of 1.3: a parcel pinned by one bad quote is
pulled back toward the prior in proportion to the quote's weight.

**Cost.** Trivial on top of 2.1: one extra block in the least-squares system. GCV or the L-curve are a loop
over λ; fixing σ in bp needs no loop and is more legible in a report.

**WIRP validation.** The penalty must be small enough that the gate passes where WIRP's input is liquid; the
report should print, per meeting, the fitted value with and without the penalty so that the departure is
visible. Where WIRP interpolates (beyond the FF strip), our prior and WIRP's linear interpolation differ by
design, and the gate note should explain each miss in those terms.

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
column), and a principled way to combine two families (FF and OIS as two measurement equations with their own
noise). The hyperparameters (prior σ, noise σ per family) can be set by marginal likelihood on the history,
which is a one-off M9 exercise, or fixed in bp and reported.

**Meeting-step priors with sparsity.** A Laplace prior on the steps is the fused lasso (Tibshirani et al. 2005)
or, on the levels, ℓ1 trend filtering (Kim, Koh, Boyd and Gorinevsky 2009): the fit is piecewise constant
with few non-zero steps. It is an attractive reading of "how many 25bp moves are priced", solvable as a small
linear programme (SciPy `linprog`, HiGHS). But it is biased by design: a step the market prices at 12bp (half a
move) is pulled to zero or to a full move depending on λ, so it cannot meet a 1bp gate and should be a
diagnostic column, not the estimator. (Judgement.)

**Binary and multinomial trees** (CME FedWatch, WIRP, Kim and Tanaka 2016, Ceh 2022): the step path plus an
assumption that each meeting is a 0/25bp coin flip with level-independent probabilities. Priebsch (2019) shows
the failure mode: when the market assigns probability to both a hike and a cut, the tree reads it as "a high
likelihood of no rate move". The tree adds nothing to the expected path (it is the same step function) and is
the right place to *stop*: our deliverable is the expected post-meeting rate and the cumulative change in 25bp
units, which the step path gives directly; probabilities need either the tree's assumptions or option prices
(Carlson, Craig and Melick 2005), and D9 rules out option vols.

**Parametric curves** (Nelson-Siegel, Svensson; BIS Papers 25 documents their use by most central banks for
*bond* curves): three to six parameters cannot represent eight dated steps. Not applicable inside the horizon.

**Cost.** GP-as-ridge: nil beyond 2.3. Fused lasso diagnostic: an afternoon. Trees: not needed.

### 2.6 Turn and month-end effects

**EFFR.** The fed funds rate has calendar effects (Hamilton 1996 *(paywalled)*; Kuttner's revisit in the
St Louis Fed Review 2008 finds no month-end effect except on the very last day of the month). Post-2015 the
pattern is a month-end dip: Bowman (FEDS Notes, September 2025) reports that "EFFR declined by about 10 basis
points on every month end from 2016 to February 2018, after which this pattern suddenly stopped in March
2018", because the bill supply after the debt-limit resolution lifted repo rates and "eliminated the wedge
between EFFR and the TGCR". Kim and Tanaka (2016) simply assumed a 5bp month-end depression when reading FF
futures. Arithmetic: a 10bp dip on one day of a 31-day month lowers the FF monthly average by 0.32bp, a 5bp
dip by 0.16bp; two affected days double it. This is below the gate tolerance but not negligible when summed
with other noise, and it is a *fixing* effect (the average includes the dip) rather than a policy step, so the
right place for it is the FF instrument model: a per-month expected dip, measured from the fixing history
(D7's spread estimator already drops turn days; the same code can measure them), applied as a deterministic
adjustment to the contract's implied average with the size reported. That keeps D8 as written (no EFFR turn
node) while not ignoring the effect. Whether it matters at all should be decided from the 2010+ fixings; the
previous attempt's `turn_effects` table is the right evidence and should be regenerated.

**OIS turn of year.** Burghardt and Kirshner's "One Good Turn" (RISK 1994 *(paywalled)*) is the classic
treatment: identify an instrument that spans the turn and neighbours that do not, and attribute the difference
to a jump; Ametrano and Bianchetti (2013, section 4.8) and the QuantLib cookbook's EONIA chapter show it in a
bootstrapped OIS curve as a discount-factor jump at the turn date. D8 reserves turn nodes for SOFR, €STR,
SONIA and TONA. For EFFR the fixing history will say whether year-ends move the rate; the same measurement as
above answers it.

### 2.7 Unscheduled meetings

Three cases, each needing a different rule:

1. **Realised unscheduled meetings** (3 and 15 March 2020, the 2008 cuts): known nodes for any as-of date on or
   after the decision date; the previous attempt's "from decision date" rule (no look-ahead) is the only
   defensible one and should stay. Their steps are flagged `unscheduled` in every output (CLAUDE.md).
2. **A scheduled meeting that an unscheduled one superseded** (17-18 March 2020): for as-of dates before the
   emergency decision the market priced the scheduled node, so the curve needs it. This is M0 reference data;
   the previous attempt proposed a `superseded_on` column in `fed.csv`. I support that (section 6).
3. **Inter-meeting moves the market expects but no bank has announced** (late February 2020, when FF futures
   priced "a 50bp cut" before 3 March): under the step model the pricing lands on the next scheduled node, so
   the implied March step overstates the *meeting* and the stub parcel is mis-timed. No published tool handles
   this differently (FedWatch and WIRP show the same scheduled nodes), so the gate should *expect* the step
   model to match WIRP on such a date and the report should flag the signature: a large residual on the
   current-month contract that a step at the next scheduled date cannot absorb. Adding a provisional
   mid-parcel node when that signature appears is possible (the design matrix allows any date) but is a
   judgement call AC should make per episode, not an automatic rule. (Judgement.)

### 2.8 The under-identified region and the OIS-split prior (D4)

Beyond the FF strip's liquid horizon (12 to 18 months) the EFFR OIS at 18M, 2Y and 3Y each span several
meetings. D4 says such parcels "take the OIS family's split as prior". My reading, to be confirmed: the total
change across a parcel comes from the OIS quotes, and the division of that change among the meetings inside
it comes from a prior rather than from the data. Candidate priors, all expressible as the penalty of 2.3:

- *Equal steps in time* (WIRP's "linear interpolation" per the HKMA; the ridge's minimum-norm solution).
- *Continue the last identified pace* (first-difference penalty).
- *Take the split from the other family* (the SOFR OIS curve has the same tenor grid, so it adds nothing;
  SR3 futures identify quarterly averages to five years, so from M3 on they could inform the split, net of
  their convexity, which is why the SOFR family comes later).
- *Zero steps beyond the last liquid quote* (the "no change" prior), which is what a flat extrapolation of
  the last level does and is clearly wrong when the OIS curve slopes.

For M2 I recommend the equal-step (ridge) prior with the prior-versus-fitted split printed per parcel, because
it is what WIRP does and the gate is against WIRP; the pace prior is one line to switch to if AC prefers it
for the exports. Synthetic meetings beyond the published calendar are nodes like any other, flagged, and in
practice sit entirely in this region.

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

- **Derived, not quoted**: FF settlement prices beyond the traded horizon (section 1.2). Zero or missing open
  interest and volume identify them. These should be excluded, not down-weighted, and listed in the drop list
  with the reason "no open interest / no volume".
- **Thin**: FF contracts with open interest in the hundreds or low thousands (the 13th to 18th months in both
  dumps). Their prices are real but move in 0.5bp ticks and lag; weights belong here.
- **Stale**: an unchanged price for several days with no volume (the loader already flags runs beyond
  `stale_days`); OIS tenors that Bloomberg carries from the previous day. Mids only means no bid-ask width to
  read liquidity from, so staleness must be inferred from runs and from volume where it exists.
- **Structurally special**: the front FF contract in its last days (very few days left to average, so the
  quote is almost a fixing); a contract spanning a month-end dip (2.6); the stub parcel, whose level is a
  fixing plus a spread, not a quote.
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
consistent with tick size and the FF/OIS basis; Huber will therefore mostly act as plain weighted least squares
and only cap the odd 3bp residual. Tukey would drop such a quote outright, which is what the drop list is for
anyway; the difference matters only for the two-of-a-kind case (a missing node produces a +3/-3 residual pair,
1.3), where Tukey would drop both quotes and hide the diagnostic. I prefer Huber for the fit and a reported
Tukey-style drop (weight below a threshold after convergence) for the list, which is D4 as written.

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

### 3.5 Weights from open interest, volume and staleness

Precedent for metadata-driven weights and exclusions: Gürkaynak, Sack and Wright (2007) weight bond prices by
"the inverse of the duration of each individual security" and *exclude* bills, securities under three months,
callables and the two most recently issued securities at each maturity for liquidity reasons rather than
down-weighting them; Lloyd (2018) and Kim and Tanaka (2016) switch from FF futures to OIS beyond one to two
years for the same reason; CME's own liquidity reviews report FF volume and open interest in aggregate only, so
the per-contract numbers in our dumps are the evidence. The previous attempt used
weight = clip(max(OI/50k, volume/20k), 0.05, 1) and stale ×0.1, which is a reasonable shape: saturating (a
contract with 400k open interest is not 20 times better than one with 20k), floored (so that a thin but real
quote still contributes), and multiplicative in staleness. Two refinements I would make:

- Treat "no open interest and no volume" as *missing*, not as the floor weight: those prices are derived
  (1.2) and the floor lets 40 of them vote together.
- Scale the weight into a quote-noise σ in bp (σ_i = σ_fam / sqrt(w_i)) rather than a bare weight, so that the
  prior σ of 2.3 and the Huber k are in the same units and the report can print "this quote was trusted to
  ±x bp".

For OIS, with no OI or volume, the weight comes from staleness alone plus a per-family σ (the previous
attempt's open question 1: 0.5bp for both families fits FF to 1bp and OIS to 1.4bp; the FF/OIS basis is a
real market feature, not noise, so the family σ should reflect which one the gate is against).

**Cost.** Nil beyond the loader fields (already dumped for the 24 months with `count_fields_months`); the
history is needed to calibrate thresholds, not to run the fit.

### 3.6 Outlier detection and the drop list

Standard regression diagnostics apply, and all are cheap at this size: (i) robust standardised residuals
(residual over MAD scale) after the IRLS converges; (ii) leave-one-out prediction residuals (refit without the
quote and price it), which is the only test that works for a leverage-one quote; (iii) leverage itself (the
diagonal of the hat matrix in the weighted problem), reported so that a reviewer sees which quotes the curve
depends on; (iv) the opposite-sign pair signature of a missing node (1.3). The drop list should carry: the
quote, its weight, its residual before and after dropping, the rule that dropped it (metadata rule, Huber
weight below threshold, leave-one-out beyond tolerance), and what the curve looked like with it in. A drop
should trigger a refit, once (the previous attempt did this). Drops by metadata rules will dominate; drops by
residual should be rare and each one is something AC reviews ("drop list reviewed" is the gate).

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
weight calibration), and consider a filter in M9 as a stability diagnostic (a plot of filtered versus daily
fitted steps would show which parcels are noisy).

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

## 4. Validation against WIRP: how each method would be tested

For each gate date: run the method, take the per-meeting implied post-meeting rate (and the cumulative change
in 25bp units), parse the WIRP capture, and tabulate the difference per meeting with the instrument WIRP used,
the number of quotes used and dropped, the weights, and the prior-versus-fitted split where the prior binds.
Pass: every meeting within 1bp, or each miss explained by one of: a timestamp difference (documented by the
capture time), a contract set difference (WIRP used a quote we dropped, or vice versa; both listed), a
regularisation difference in the under-identified region (prior named), a stub difference (WIRP's current
EFFR versus our fixing plus spread), or a missing node (unscheduled or superseded meeting, 2.7).

Which methods can pass: the step model with weighted (and lightly robust and lightly penalised) least squares;
possibly the exact bootstrap if WIRP's instrument subset is reproduced. Which cannot, by design: any smooth
interpolant inside the horizon, sparse-step fits, trimmed fits, and cross-day filters on event days. That is
not a criticism of those methods; it says the gate tests fidelity to the market's step pricing, which is what
D1's policy-pricing deliverable wants.

Ten dates (the previous attempt's proposal, which I would keep): 2014-09-16 (zero lower bound), 2015-12-15
(lift-off), 2018-09-25 (hikes), 2019-07-30 (cuts), 2020-03-03 (unscheduled cut decided that day, inside the
window; also tests the superseded 18 March node), 2020-03-16 (first close after the Sunday cut), 2022-06-14,
2023-07-25 (hikes), 2024-09-17 (cuts), 2026-10-07 (already on file). The previous attempt's parser was written
before any capture existed and refused unknown text; this time the parser is written against AC's real
captures, as with the CME pages in M1.

---

## 5. Comparison table

| Method | Assumes | On our data (FF monthly averages, EFFR OIS, 8+ meetings, mids) | Cost | WIRP gate | Verdict |
| --- | --- | --- | --- | --- | --- |
| Flat forwards between effective dates, exact bootstrap | one quote per node; rate moves only on effective dates | over-identified first year forces an ad-hoc instrument subset; unstable to which subset | low | passes if the subset matches WIRP's | base case; keep as a check |
| Flat forwards, global weighted least squares (D2 + global fit) | same path; quote noise ~ tick, weights from metadata | uses every quote; residuals in bp; local by construction | low | passes where input is liquid | **recommended core** |
| + Tikhonov / ridge on steps or step differences (prior σ in bp) | true steps are small / pace continues; prior weak vs data | negligible inside liquid strip; selects the split beyond 18M; limits leverage | trivial | passes if σ large vs tick; prints departure | **recommended, weak** |
| Smoothing splines / VRP on forwards (FNZ, Waggoner) | continuous forwards | smears steps into ramps | low-medium | fails inside horizon | back end only |
| Monotone convex, PCHIP, tension splines | continuous, shape-preserving forwards; one node per quote | same smearing; needs thinning | low | fails inside horizon | D3 junction and beyond (already) |
| Maximum-smoothness forwards | C2 forwards, exact pricing | same, plus known overshoot | low | fails | no |
| GP posterior on step levels | Gaussian prior on steps (= ridge) | same as ridge; adds a σ per meeting and family noise σ | trivial (closed form) | as ridge | report the posterior σ |
| Fused lasso / ℓ1 steps | few non-zero steps of similar size | rounds half-priced moves to 0 or 25bp | low (LP) | fails by design | diagnostic column only |
| Binary trees (FedWatch, WIRP, Riksbank) | 0/25bp per meeting, level-independent p | same path as D2; adds nothing to the expected path; mis-reads two-sided risk | n/a | n/a (it *is* WIRP) | not needed |
| Nelson-Siegel / Svensson | 3-6 smooth parameters | cannot hold 8 dated steps | low | fails | no |
| Huber IRLS (D4) | few large residuals; scale from MAD | mostly inactive at ~1bp RMS; caps odd 3bp residual; blind to leverage | low | neutral / protective | **keep** |
| Tukey biweight | as Huber, redescending | drops a +3/-3 missing-node pair, hiding the diagnostic | low | neutral | use its threshold for the drop list only |
| LTS / LMS / MM | up to 50% garbage | discards tick-level-good quotes; biased at 1bp scale | medium (small n: cheap) | risks misses | diagnostic drop list |
| Quantile / LAD | median fit, LP | interpolates p quotes exactly; non-unique at tick ties | low | risks misses | diagnostic |
| Metadata weights (OI, volume, staleness, days remaining) | unreliability is predictable | identifies the derived far strip and thin months before fitting | nil | protective | **do most of the work**; treat no-OI/no-volume as missing |
| Leave-one-out, leverage, residual-pair signature | standard diagnostics | finds the leverage-one and missing-node cases | low | explains misses | **in the battery** |
| Kalman filter across days | random-walk steps, jumps on FOMC days | smooths tick noise; lags on event days unless tuned; look-ahead if smoothed | medium | misses on event days | M9 stability diagnostic |
| Month-end dip adjustment in the FF model | measured fixing effect, ~0.2-0.3bp on a monthly average 2016-18 | removes a bias WIRP may or may not remove | low | explains sub-bp misses | measure first (keeps D8) |
| Provisional node for an expected inter-meeting move | AC judgement per episode | fixes 2.7 case 3 timing | low | WIRP has no such node | by hand, flagged |

---

## 6. Recommendation and decisions needed

**On D2 (flat forwards between effective dates; synthetic meetings to 3y, flagged): agree, unchanged.** The
only additions are node types the design matrix must accept beyond scheduled effective dates: unscheduled
meetings from their decision date, superseded scheduled meetings until their supersession date, and (by hand)
a provisional node.

**On D4 (OIS split as prior for under-identified parcels; Huber IRLS with liquidity/staleness weights and a
reported drop list): agree, with these changes of emphasis.**

1. The fit is one global weighted least-squares problem on the step levels, both families together, with a
   per-family quote σ in bp and per-quote weights from open interest, volume, days remaining and staleness.
   Quotes with no open interest and no volume are excluded as derived prices, not floored.
2. Huber IRLS on top, k = 1.345, scale from the MAD with a floor at the tick size so that a quiet strip does
   not manufacture outliers. The drop list is built from the metadata rules first, then from Huber weights
   below a threshold, then from leave-one-out residuals, each with its reason; one refit after dropping.
3. A weak Gaussian prior on each step (σ_prior of order 10bp, reported) rather than an unconditioned fit,
   which (a) makes the under-identified region well-posed with the equal-step split that WIRP's interpolation
   also implies, (b) caps the damage from a leverage-one quote, and (c) yields a posterior σ per meeting for the
   report. The prior-versus-fitted split is printed wherever the prior binds. This is the "OIS split as prior"
   of D4 made explicit; if D4 meant taking the split from the SOFR family instead, that is an M3 input and the
   equal-step prior is the M2 placeholder.
4. Leverage and the maximum move of each step per bp of each input are standard columns in the quality battery.

**Decisions needed from AC** (also listed in the PR):

- D-A. Confirm D2 as read above, including the three extra node types.
- D-B. Confirm the fit of D4 as items 1-4 above, in particular: exclusion (not down-weighting) of
  no-OI/no-volume FF prices; the weak ridge prior with equal-step split as the M2 placeholder for the OIS
  split; and the leverage/leave-one-out diagnostics in the battery.
- D-C. What "OIS family's split" in D4 means: equal steps in time (WIRP-like), continue the pace, or the SOFR
  family's split (then M3).
- D-D. Gate instrument: whether WIRP captures will be FF-based, OIS-based, or both, and therefore which family
  the fit should trust more (σ per family). My default: FF where liquid, OIS beyond; report the basis.
- D-E. M0 schema: add a `superseded_on` column to `data/refdata/meetings/fed.csv` so that 17-18 March 2020
  exists for as-of dates before 15 March 2020 (and equivalents for the other banks if any).
- D-F. Month-end dip: measure it from the 2010+ EFFR fixings and decide then whether the FF instrument model
  applies a deterministic adjustment (D8 stays: no EFFR turn node in the curve).
- D-G. The ten gate dates (section 4), or substitutes.
- D-H. Diagnostics to include in the battery as extra columns (fused-lasso move count, LTS drop list,
  quantile fit) versus leaving them out of M2.

---

## 7. Sources

Free copies are linked where I found one; *(paywalled)* marks the ones I could not open and cite from the
abstract or from secondary descriptions. cmegroup.com pages are not fetched by script (see README); their
quotes above come from search snippets and should be checked against the page.

**Step functions, meeting-dated expectations, practitioner tools**

- CME Group, *Understanding the CME Group FedWatch Tool methodology* (2023), https://www.cmegroup.com/articles/2023/understanding-the-cme-group-fedwatch-tool-methodology.html ; and the *Fed Funds futures probability tree calculator* page, https://www.cmegroup.com/education/demos-and-tutorials/fed-funds-futures-probability-tree-calculator.html (not fetched by script).
- CME Group, SER-8105 (2018), 30-Day Fed Funds daily settlement amendment, https://www.cmegroup.com/notices/ser/2018/04/SER-8105.pdf ; client-systems wiki "Fed Fund" settlement page, https://cmegroupclientsite.atlassian.net/wiki/spaces/EPICSANDBOX/pages/457088183/Fed+Fund
- Kim, D. H. and H. Tanaka (2016), "Front-end term premiums in federal funds futures rates and implied probabilities of future rate hikes", FEDS Notes, 18 Nov 2016, https://federalreserve.gov/econresdata/notes/feds-notes/2016/front-end-term-premiums-in-federal-funds-futures-rates-and-implied-probabilities-of-future-rate-hikes-20161118.html
- Priebsch, M. A. (2019), "A new way to visualize the evolution of monetary policy expectations", FEDS Notes, 20 Sep 2019, https://www.federalreserve.gov/econres/notes/feds-notes/new-way-to-visualize-the-evolution-of-monetary-policy-expectations-20190920.html
- Hong Kong Monetary Authority (2019), Research Memorandum 01/2019, "Interpreting survey-based federal funds rate forecasts", footnote 7 on WIRP, https://www.hkma.gov.hk/media/eng/publication-and-research/research/research-memorandums/2019/RM01-2019.pdf
- Chandler, M. (2015), "Why I don't use Bloomberg's WIRP function" (practitioner note), https://www.marctomarket.com/2015/09/why-i-dont-use-bloombergs-wirp-function.html
- Ceh, A. M. (2022), "How much is priced in? Market expectations of monetary policy lift", Sveriges Riksbank Staff Memo, Dec 2022, https://www.riksbank.se/globalassets/media/rapporter/staff-memo/svenska/2022/staff-memo-how-much-is-priced-in-market-expectations-of-monetary-policy-lift.pdf
- Syrstad, O. and D. Rime (2014), Norges Bank Staff Memo 6/2014 (FRA-based expectations, IMM dates), https://www.norges-bank.no/contentassets/a642411c06344dd180beaf3dd613ba7b/staff_memo_2014_6.pdf
- ECB Money Market Contact Group (2023), "Drivers of euro interest rate expectations" (maintenance-period-dated OIS forwards), https://www.ecb.europa.eu/paym/groups/pdf/mmcg/20230302/Drivers_of_euro_interest_rate_expectations.en.pdf
- Lengyel, A. and D. Walker (2026), "Bank Rate expectations in the UK curve following the war in Iran", Bank of England Bank Insights, 17 Jul 2026, https://www.bankofengland.co.uk/bank-insights/2026/bank-rate-expectations-uk-curve-following-the-war-in-iran
- Freitas, W., R package `copom`: flat-forward interpolation on COPOM dates, https://wilsonfreitas.github.io/copom/articles/copom.html
- QuantLib, `ql/termstructures/globalbootstrap.hpp` (SoftSolutions 2019, Caspers 2025), https://github.com/lballabio/QuantLib/blob/master/ql/termstructures/globalbootstrap.hpp
- Ametrano, F. M. and M. Bianchetti (2013), "Everything you always wanted to know about multiple interest rate curve bootstrapping but were afraid to ask", SSRN 2219548, https://ssrn.com/abstract=2219548 ; QuantLib Python Cookbook, EONIA chapter (turn-of-year jumps), https://leanpub.com/read/quantlibpythoncookbook/leanpub-auto-eonia-curve-bootstrapping
- Carlson, J. B., B. R. Craig and W. R. Melick (2005), "Recovering market expectations of FOMC rate changes with options on federal funds futures", Cleveland Fed WP 05-07 (options; excluded by D9), https://www.clevelandfed.org/publications/working-paper/wp-0507-recovering-market-expectations-of-fomc-rate-changes

**FF futures and OIS as measures of expectations; risk premia**

- Kuttner, K. N. (2001), "Monetary policy surprises and interest rates: evidence from the Fed funds futures market", JME 47(3) *(paywalled)*; NY Fed Staff Report 99 (free), https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr99.pdf
- Gürkaynak, R. S. (2005), "Using federal funds futures contracts for monetary policy analysis", FEDS 2005-29, https://www.federalreserve.gov/econres/feds/using-federal-funds-futures-contracts-for-monetary-policy-analysis.htm
- Gürkaynak, R. S., B. Sack and E. T. Swanson (2007), "Market-based measures of monetary policy expectations", JBES 25(2) *(paywalled)*; FRBSF WP 2006-04 (free), https://www.frbsf.org/wp-content/uploads/wp06-04bk.pdf
- Piazzesi, M. and E. T. Swanson (2008), "Futures prices as risk-adjusted forecasts of monetary policy", JME 55 *(paywalled)*; author copy, https://web.stanford.edu/~piazzesi/fff.pdf
- Hamilton, J. D. (2009), "Daily changes in Fed funds futures prices", JMCB 41(4) *(paywalled)*; NBER WP 13112, https://www.nber.org/papers/w13112.pdf
- Lloyd, S. P. (2018), "Overnight index swap market-based measures of monetary policy expectations", Bank of England SWP 709, https://www.bankofengland.co.uk/-/media/boe/files/working-paper/2018/overnight-index-swap-market-based-measures-of-monetary-policy-expectations.pdf
- Joyce, M., J. Relleen and S. Sorensen (2008), "Measuring monetary policy expectations from financial market instruments", Bank of England WP 356 / ECB WP 978, https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp978.pdf
- Priebsch, M. A. (2017), "A shadow rate model of intermediate-term policy rate expectations", FEDS Notes, https://www.federalreserve.gov/econres/notes/feds-notes/shadow-rate-model-of-intermediate-term-policy-rate-expectations-20171004.htm
- Diercks, A. and E. Carl (2019), "A simple macro-finance measure of risk premia in fed funds futures", FEDS Notes, https://www.federalreserve.gov/econres/notes/feds-notes/simple-macro-finance-measure-of-risk-premia-in-fed-funds-futures-20190108.htm
- D'Amico, S., V. Kurakula and S. I. Sordo Palacios (2020), "A risk-premium adjustment to the policy rate path", Chicago Fed Letter 432, https://www.chicagofed.org/publications/chicago-fed-letter/2020/432
- Schmeling, M., A. Schrimpf and S. A. M. Steffensen (2022), "Monetary policy expectation errors", BIS WP 996, https://www.bis.org/publ/work996.htm
- Kısacıkoğlu, B. (2024), "Overnight index swaps and monetary policy expectations in the US", CEPR DP19143 *(paywalled)*, https://cepr.org/publications/dp19143

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
