# Bloomberg WIRP documentation (reference copies)

Three documents from the Bloomberg terminal, supplied by AC on 9 Oct 2026, kept here because WIRP is the
gate standard for M2 (`docs/decisions.md`, Build plan) and the text is not available outside the terminal.
The help page is marked "prepared for the exclusive use of Adrian Chiu and may not be redistributed":
these copies are for this private repository only.

| File | What it is |
| --- | --- |
| `WIRP_help_page_20261009.pdf` | `WIRP <GO>` help page, dated 10/09/2026 (16 pages): screens, column definitions, ticker table, FAQ. Image-only PDF (no text layer). |
| `WIRP_calculations.pdf` / `.txt` | "Calculations" (17 pages): the futures model and the OIS model, worked examples (9/16/2019 futures, 9/13/2018 OIS), definitions of the implied data. |
| `WIRP_estimating_the_path_of_central_bank_hikes_and_cuts.pdf` / `.txt` | "WIRP: Estimating the Path of Central Bank Hikes and Cuts" (9 pages): why the conditional-probability grid was dropped and what the current screen shows. |

The `.txt` files are `pdftotext -layout` extracts for grep and for tests; the PDFs are the originals.

## What they establish (used in `../front_end_curve.md`)

- **Model assumption**: "only a central bank action will impact the effective interest rate of an economy";
  expected overnight rates are "pushed forward and backward through the chosen asset's tenor structure".
- **Two separate models per region** (`US - Fut`, `US - OIS`), each with its own tickers
  (`US0AFR`/`US0ANM`/`US0APR`/`US0ACR` for futures, `US0BFR`/`US0BNM`/`US0BPR`/`US0BCR` for OIS, meeting
  tail `MMMYYYY`, e.g. `US0AFR DEC2019 Index`). Nothing reconciles the two.
- **Futures model**: a monthly contract prices the arithmetic average EFFR over its month; a month without a
  meeting gives one rate; for a meeting month, `31 × avg = d_pre × pre + d_post × post`, with `pre` carried
  forward from the preceding non-meeting contract and `post` solved; "we work our way through the available
  contract prices and CB meeting dates to solve for all available forward rates". The meeting day itself is
  at the pre-meeting rate; the post-meeting rate starts the next day.
- **OIS model**: fixed `1 + r·n/360` against a daily-compounded float `∏(1 + r_i·d_i/360)` with `d_i` = 1 on
  weekdays, 3 over weekends, holidays carried; spot lag 2 days; the unknown rate on each segment is assumed
  constant and solved by Newton's method; the 1W tenor gives the pre-meeting rate, the 1M (chosen over 3W
  "as it tends to have more liquidity") the first post-meeting rate, then on through the monthly tenors.
  Curve shown as `ICVS 42`.
- **Implied data**: Current Implied O/N Rate (rate until the first meeting, from the instrument, not the
  fixing); Post-Meeting Implied Rate per meeting; Imp. Rate Δ = post − current implied; #Hikes/Cuts =
  Δ / A.R.M. (cumulative, A.R.M. = 25bp for the Fed); %Hike/Cut = (post_t − post_{t−1}) / A.R.M. (marginal).
  Percentages can exceed 100%; the conditional-probability grid was dropped in 2019.
- **Horizon**: "The calculations behind WIRP rely on a liquid OIS swaps or futures curve, with monthly
  granularity. If there is no reliable pricing on all monthly tenors beyond a certain point on the curve,
  WIRP does not show meeting dates beyond that point." The help-page screens show about 14 months of meetings.
- **Timing**: futures on a 10-minute delay (CME contract), OIS live; US futures close 6 pm ET, OIS 5 pm ET;
  post-close trades process the next day. Options and Eurodollar models removed in September 2019.
- **Overrides**: users can override implied rates and the assumed move size (e.g. the Dec 2018 20bp IOER move).
