# USD EFFR front end, 2019-06-12

Anchor (target_midpoint) in effect: 2.375. Policy spread (winsorised_mean, D7): 2.82bp (winsorised mean 2.82bp, median 2.50bp; 60 fixings, 3 turn days dropped, window 2019-03-14..2019-06-11) **Loader reported blocking problems in the window (see check_market_data.py).**

## Curve `effr_fut` (ff_fut)

Fit: 24 quotes (0 dropped, 12 excluded by metadata), 2 IRLS iterations (converged); 25 parcels to 2022-06-12, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 2.3950 (replica 2.3950; stub prior 2.4032 from anchor + spread (D7)). WIRP replica reaches 16 meetings on 24 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2019-06-19 | False | False | 2.329995 | -0.065036 | -0.2601 | -26.01 | 2.33 | -0.001 | 2.301828 | -7.317 | False | 0.005 | False |
| 2019-07-31 | False | False | 2.135815 | -0.259216 | -1.0369 | -77.67 | 2.135 | 0.081 | 2.107648 | -26.735 | False | 0.004 | False |
| 2019-09-18 | False | False | 1.967886 | -0.427145 | -1.7086 | -67.17 | 1.9725 | -0.461 | 1.939719 | -43.528 | False | 0.005 | False |
| 2019-10-30 | False | False | 1.895889 | -0.499141 | -1.9966 | -28.8 | 1.895 | 0.089 | 1.867722 | -50.728 | False | 0.005 | False |
| 2019-12-11 | False | False | 1.75104 | -0.643991 | -2.576 | -57.94 | 1.7555 | -0.446 | 1.722873 | -65.213 | False | 0.004 | False |
| 2020-01-29 | False | False | 1.684842 | -0.710189 | -2.8408 | -26.48 | 1.685 | -0.016 | 1.656675 | -71.833 | False | 0.005 | False |
| 2020-03-18 | False | False | 1.625996 | -0.769034 | -3.0761 | -23.54 | 1.625385 | 0.061 | 1.59783 | -77.717 | False | 0.005 | False |
| 2020-04-29 | False | False | 1.595132 | -0.799899 | -3.1996 | -12.35 | 1.595 | 0.013 | 1.566965 | -80.804 | False | 0.006 | False |
| 2020-06-10 | False | False | 1.54784 | -0.84719 | -3.3888 | -18.92 | 1.55 | -0.216 | 1.519674 | -85.533 | False | 0.008 | False |
| 2020-07-29 | False | False | 1.514614 | -0.880417 | -3.5217 | -13.29 | 1.515 | -0.039 | 1.486447 | -88.855 | False | 0.01 | False |
| 2020-09-16 | False | False | 1.474545 | -0.920486 | -3.6819 | -16.03 | 1.475 | -0.046 | 1.446378 | -92.862 | False | 0.013 | False |
| 2020-11-05 | False | False | 1.456018 | -0.939013 | -3.7561 | -7.41 | 1.457 | -0.098 | 1.427851 | -94.715 | False | 0.023 | False |
| 2020-12-16 | False | False | 1.436347 | -0.958684 | -3.8347 | -7.87 | 1.4322 | 0.415 | 1.40818 | -96.682 | False | 0.023 | False |
| 2021-01-27 | False | False | 1.419467 | -0.975564 | -3.9023 | -6.75 | 1.42 | -0.053 | 1.3913 | -98.37 | False | 0.02 | False |
| 2021-03-17 | False | False | 1.434369 | -0.960662 | -3.8426 | 5.96 | 1.431071 | 0.33 | 1.406202 | -96.88 | False | 0.022 | False |
| 2021-04-28 | False | False | 1.435039 | -0.959992 | -3.84 | 0.27 | 1.435 | 0.004 | 1.406872 | -96.813 | False | 0.022 | False |
| 2021-06-16 | False | False | 1.435039 | -0.959992 | -3.84 | 0.0 |  |  | 1.406872 | -96.813 | True | 0.023 | True |
| 2021-07-28 | False | False | 1.435039 | -0.959992 | -3.84 | 0.0 |  |  | 1.406872 | -96.813 | True | 0.023 | True |
| 2021-09-22 | False | False | 1.435039 | -0.959992 | -3.84 | 0.0 |  |  | 1.406872 | -96.813 | True | 0.024 | True |
| 2021-11-03 | False | False | 1.435039 | -0.959992 | -3.84 | 0.0 |  |  | 1.406872 | -96.813 | True | 0.024 | True |
| 2021-12-15 | False | False | 1.435039 | -0.959992 | -3.84 | 0.0 |  |  | 1.406872 | -96.813 | True | 0.025 | True |
| 2022-01-26 | False | False | 1.435039 | -0.959992 | -3.84 | 0.0 |  |  | 1.406872 | -96.813 | True | 0.025 | True |
| 2022-03-16 | False | False | 1.435039 | -0.959992 | -3.84 | 0.0 |  |  | 1.406872 | -96.813 | True | 0.026 | True |
| 2022-05-04 | False | False | 1.435039 | -0.959992 | -3.84 | 0.0 |  |  | 1.406872 | -96.813 | True | 0.026 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | used | 24 | 0.002 | 0.098 | 0.256 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

| curve | instrument | contract | ticker | status | reason | residual_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2021-06 | FFM21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-07 | FFN21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-08 | FFQ21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-09 | FFU21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-11 | FFX21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-12 | FFZ21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-01 | FFF22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-02 | FFG22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-03 | FFH22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-04 | FFJ22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-05 | FFK22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-10 | FFV21 Comdty | excluded | beyond the strip's reach (first contract without open interest or volume starts 2021-06-01) |  |

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2019-06 | FFM19 Comdty | 2.365 | -0.001 | -0.103 | 0.994 |
| effr_fut | ff_fut | 2019-07 | FFN19 Comdty | 2.33 | 0.001 | 0.597 | 0.999 |
| effr_fut | ff_fut | 2019-11 | FFX19 Comdty | 1.895 | -0.089 | -1.13 | 0.921 |
| effr_fut | ff_fut | 2020-04 | FFJ20 Comdty | 1.625 | 0.003 | 0.046 | 0.93 |
| effr_fut | ff_fut | 2020-05 | FFK20 Comdty | 1.595 | -0.013 | -0.581 | 0.977 |
| effr_fut | ff_fut | 2021-05 | FFK21 Comdty | 1.435 | -0.004 | -3.123 | 0.999 |

### Stale and outside-listing inputs

| curve | flag | instrument | contract | status | detail |
| --- | --- | --- | --- | --- | --- |
| effr_fut | outside_listing | ff_fut | 2022-02 | excluded | loader: FFG22 Comdty|PX_LAST quoted from 2019-02-28, modelled first listing 2019-03-01 |
| effr_fut | outside_listing | ff_fut | 2022-03 | excluded | loader: FFH22 Comdty|PX_LAST quoted from 2019-03-29, modelled first listing 2019-04-01 |
| effr_fut | outside_listing | ff_fut | 2022-04 | excluded | loader: FFJ22 Comdty|PX_LAST quoted from 2019-04-30, modelled first listing 2019-05-01 |
| effr_fut | outside_listing | ff_fut | 2022-05 | excluded | loader: FFK22 Comdty|PX_LAST quoted from 2019-05-31, modelled first listing 2019-06-03 |

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2019-06-12 | 1.0 | False | 0.02 | 2.39503 |  | 2.395 | 0.003 |
| 2019-06-19 | 2019-06-20 | 1.0 | False | 0.005 | 2.329995 | -6.504 | 2.33 | -0.001 |
| 2019-07-31 | 2019-08-01 | 1.0 | False | 0.004 | 2.135815 | -19.418 | 2.135 | 0.081 |
| 2019-09-18 | 2019-09-19 | 1.0 | False | 0.005 | 1.967886 | -16.793 | 1.9725 | -0.461 |
| 2019-10-30 | 2019-10-31 | 1.0 | False | 0.005 | 1.895889 | -7.2 | 1.895 | 0.089 |
| 2019-12-11 | 2019-12-12 | 1.0 | False | 0.004 | 1.75104 | -14.485 | 1.7555 | -0.446 |
| 2020-01-29 | 2020-01-30 | 1.0 | False | 0.005 | 1.684842 | -6.62 | 1.685 | -0.016 |
| 2020-03-18 | 2020-03-19 | 1.0 | False | 0.005 | 1.625996 | -5.885 | 1.625385 | 0.061 |
| 2020-04-29 | 2020-04-30 | 1.0 | False | 0.006 | 1.595132 | -3.086 | 1.595 | 0.013 |
| 2020-06-10 | 2020-06-11 | 1.0 | False | 0.008 | 1.54784 | -4.729 | 1.55 | -0.216 |
| 2020-07-29 | 2020-07-30 | 1.0 | False | 0.01 | 1.514614 | -3.323 | 1.515 | -0.039 |
| 2020-09-16 | 2020-09-17 | 1.0 | False | 0.013 | 1.474545 | -4.007 | 1.475 | -0.046 |
| 2020-11-05 | 2020-11-06 | 1.0 | False | 0.023 | 1.456018 | -1.853 | 1.457 | -0.098 |
| 2020-12-16 | 2020-12-17 | 1.0 | False | 0.023 | 1.436347 | -1.967 | 1.4322 | 0.415 |
| 2021-01-27 | 2021-01-28 | 1.0 | False | 0.02 | 1.419467 | -1.688 | 1.42 | -0.053 |
| 2021-03-17 | 2021-03-18 | 1.0 | False | 0.022 | 1.434369 | 1.49 | 1.431071 | 0.33 |
| 2021-04-28 | 2021-04-29 | 1.0 | False | 0.022 | 1.435039 | 0.067 | 1.435 | 0.004 |
| 2021-06-16 | 2021-06-17 | 0.0 | True | 0.023 | 1.435039 | 0.0 |  |  |
| 2021-07-28 | 2021-07-29 | 0.0 | True | 0.023 | 1.435039 | 0.0 |  |  |
| 2021-09-22 | 2021-09-23 | 0.0 | True | 0.024 | 1.435039 | 0.0 |  |  |
| 2021-11-03 | 2021-11-04 | 0.0 | True | 0.024 | 1.435039 | 0.0 |  |  |
| 2021-12-15 | 2021-12-16 | 0.0 | True | 0.025 | 1.435039 | 0.0 |  |  |
| 2022-01-26 | 2022-01-27 | 0.0 | True | 0.025 | 1.435039 | 0.0 |  |  |
| 2022-03-16 | 2022-03-17 | 0.0 | True | 0.026 | 1.435039 | 0.0 |  |  |
| 2022-05-04 | 2022-05-05 | 0.0 | True | 0.026 | 1.435039 | 0.0 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_fut | ff_fut 2019-06 | 2.364999999999995 | used |
| effr_fut | ff_fut 2019-07 | 2.3299999999999983 | used |
| effr_fut | ff_fut 2019-08 | 2.135000000000005 | used |
| effr_fut | ff_fut 2019-09 | 2.069999999999993 | used |
| effr_fut | ff_fut 2019-10 | 1.9650000000000034 | used |
| effr_fut | ff_fut 2019-11 | 1.894999999999996 | used |
| effr_fut | ff_fut 2019-12 | 1.8050000000000068 | used |
| effr_fut | ff_fut 2020-01 | 1.7450000000000045 | used |
| effr_fut | ff_fut 2020-02 | 1.6850000000000023 | used |
| effr_fut | ff_fut 2020-03 | 1.6599999999999966 | used |
| effr_fut | ff_fut 2020-04 | 1.625 | used |
| effr_fut | ff_fut 2020-05 | 1.5949999999999989 | used |
| effr_fut | ff_fut 2020-06 | 1.5649999999999977 | used |
| effr_fut | ff_fut 2020-07 | 1.5450000000000017 | used |
| effr_fut | ff_fut 2020-08 | 1.5150000000000006 | used |
| effr_fut | ff_fut 2020-09 | 1.4950000000000045 | used |
| effr_fut | ff_fut 2020-10 | 1.4749999999999943 | used |
| effr_fut | ff_fut 2020-11 | 1.4599999999999937 | used |
| effr_fut | ff_fut 2020-12 | 1.4449999999999932 | used |
| effr_fut | ff_fut 2021-01 | 1.4350000000000023 | used |
| effr_fut | ff_fut 2021-02 | 1.4200000000000017 | used |
| effr_fut | ff_fut 2021-03 | 1.4249999999999972 | used |
| effr_fut | ff_fut 2021-04 | 1.4350000000000023 | used |
| effr_fut | ff_fut 2021-05 | 1.4350000000000023 | used |

Replica notes: ff_fut 2019-11: no new parcel; re-solved parcel 4 (2019-10-30); ff_fut 2020-02: no new parcel; re-solved parcel 6 (2020-01-29); ff_fut 2020-05: no new parcel; re-solved parcel 8 (2020-04-29); ff_fut 2020-08: no new parcel; re-solved parcel 10 (2020-07-29); ff_fut 2020-10: no new parcel; re-solved parcel 11 (2020-09-16); ff_fut 2021-02: no new parcel; re-solved parcel 14 (2021-01-27); ff_fut 2021-05: no new parcel; re-solved parcel 16 (2021-04-28)

## Curve `effr_ois` (ois_effr)

Fit: 18 quotes (0 dropped, 0 excluded by metadata), 3 IRLS iterations (converged); 26 parcels to 2022-06-23, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 2.3690 (replica 2.3696; stub prior 2.4032 from anchor + spread (D7)). WIRP replica reaches 8 meetings on 13 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2019-06-19 | False | False | 2.335658 | -0.033342 | -0.1334 | -13.34 | 2.335111 | 0.055 | 2.307491 | -6.751 | False | 0.005 | False |
| 2019-07-31 | False | False | 2.130973 | -0.238026 | -0.9521 | -81.87 | 2.130003 | 0.097 | 2.102806 | -27.219 | False | 0.011 | False |
| 2019-09-18 | False | False | 1.975878 | -0.393122 | -1.5725 | -62.04 | 1.979869 | -0.399 | 1.947711 | -42.729 | False | 0.024 | False |
| 2019-10-30 | False | False | 1.889305 | -0.479694 | -1.9188 | -34.63 | 1.87489 | 1.441 | 1.861138 | -51.386 | False | 0.033 | False |
| 2019-12-11 | False | False | 1.754711 | -0.614288 | -2.4572 | -53.84 | 1.774786 | -2.007 | 1.726544 | -64.846 | False | 0.037 | False |
| 2020-01-29 | False | False | 1.668083 | -0.700916 | -2.8037 | -34.65 | 1.659411 | 0.867 | 1.639917 | -73.508 | False | 0.043 | False |
| 2020-03-18 | False | False | 1.614708 | -0.754291 | -3.0172 | -21.35 | 1.613119 | 0.159 | 1.586542 | -78.846 | False | 0.062 | False |
| 2020-04-29 | False | False | 1.593933 | -0.775067 | -3.1003 | -8.31 | 1.590576 | 0.336 | 1.565766 | -80.923 | False | 0.086 | False |
| 2020-06-10 | False | False | 1.55259 | -0.816409 | -3.2656 | -16.54 |  |  | 1.524424 | -85.058 | False | 0.505 | True |
| 2020-07-29 | False | False | 1.512273 | -0.856726 | -3.4269 | -16.13 |  |  | 1.484106 | -89.089 | True | 0.156 | True |
| 2020-09-16 | False | False | 1.471958 | -0.897041 | -3.5882 | -16.13 |  |  | 1.443791 | -93.121 | True | 0.196 | True |
| 2020-11-05 | False | False | 1.431646 | -0.937353 | -3.7494 | -16.12 |  |  | 1.403479 | -97.152 | True | 0.545 | True |
| 2020-12-16 | False | False | 1.425402 | -0.943597 | -3.7744 | -2.5 |  |  | 1.397236 | -97.776 | True | 0.325 | True |
| 2021-01-27 | False | False | 1.419167 | -0.949832 | -3.7993 | -2.49 |  |  | 1.391001 | -98.4 | True | 0.107 | True |
| 2021-03-17 | False | False | 1.412944 | -0.956055 | -3.8242 | -2.49 |  |  | 1.384777 | -99.022 | True | 0.12 | True |
| 2021-04-28 | False | False | 1.406729 | -0.96227 | -3.8491 | -2.49 |  |  | 1.378563 | -99.644 | True | 0.34 | True |
| 2021-06-16 | False | False | 1.423335 | -0.945665 | -3.7827 | 6.64 |  |  | 1.395168 | -97.983 | True | 0.264 | True |
| 2021-07-28 | False | False | 1.439934 | -0.929065 | -3.7163 | 6.64 |  |  | 1.411768 | -96.323 | True | 0.189 | True |
| 2021-09-22 | False | False | 1.456525 | -0.912474 | -3.6499 | 6.64 |  |  | 1.428359 | -94.664 | True | 0.115 | True |
| 2021-11-03 | False | False | 1.473105 | -0.895894 | -3.5836 | 6.63 |  |  | 1.444938 | -93.006 | True | 0.047 | True |
| 2021-12-15 | False | False | 1.489673 | -0.879327 | -3.5173 | 6.63 |  |  | 1.461506 | -91.349 | True | 0.054 | True |
| 2022-01-26 | False | False | 1.506229 | -0.86277 | -3.4511 | 6.62 |  |  | 1.478063 | -89.694 | True | 0.126 | True |
| 2022-03-16 | False | False | 1.522777 | -0.846222 | -3.3849 | 6.62 |  |  | 1.49461 | -88.039 | True | 0.205 | True |
| 2022-05-04 | False | False | 1.539319 | -0.82968 | -3.3187 | 6.62 |  |  | 1.511153 | -86.385 | True | 0.287 | True |
| 2022-06-15 | False | False | 1.539319 | -0.82968 | -3.3187 | 0.0 |  |  | 1.511153 | -86.385 | True | 0.287 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | used | 18 | -0.0 | 0.058 | 0.136 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

_none_

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | 1W | USSO1Z Curncy | 2.3651 | 0.046 | 0.477 | 0.903 |
| effr_ois | ois_effr | 1Y | USSO1 Curncy | 1.89194 | 0.003 | 0.046 | 0.94 |
| effr_ois | ois_effr | 18M | USSO1F Curncy | 1.76202 | 0.0 | 0.188 | 0.999 |
| effr_ois | ois_effr | 2Y | USSO2 Curncy | 1.68138 | -0.001 | -0.894 | 0.999 |
| effr_ois | ois_effr | 3Y | USSO3 Curncy | 1.619 | 0.0 | 2.569 | 1.0 |

### Stale and outside-listing inputs

_none_

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2019-06-12 | 1.0 | False | 0.006 | 2.368999 |  | 2.369633 | -0.063 |
| 2019-06-19 | 2019-06-20 | 1.0 | False | 0.005 | 2.335658 | -3.334 | 2.335111 | 0.055 |
| 2019-07-31 | 2019-08-01 | 1.0 | False | 0.011 | 2.130973 | -20.468 | 2.130003 | 0.097 |
| 2019-09-18 | 2019-09-19 | 1.0 | False | 0.024 | 1.975878 | -15.51 | 1.979869 | -0.399 |
| 2019-10-30 | 2019-10-31 | 1.0 | False | 0.033 | 1.889305 | -8.657 | 1.87489 | 1.441 |
| 2019-12-11 | 2019-12-12 | 1.0 | False | 0.037 | 1.754711 | -13.459 | 1.774786 | -2.007 |
| 2020-01-29 | 2020-01-30 | 1.0 | False | 0.043 | 1.668083 | -8.663 | 1.659411 | 0.867 |
| 2020-03-18 | 2020-03-19 | 1.0 | False | 0.062 | 1.614708 | -5.337 | 1.613119 | 0.159 |
| 2020-04-29 | 2020-04-30 | 1.0 | False | 0.086 | 1.593933 | -2.078 | 1.590576 | 0.336 |
| 2020-06-10 | 2020-06-11 | 1.0 | False | 0.505 | 1.55259 | -4.134 |  |  |
| 2020-07-29 | 2020-07-30 | 0.3785 | True | 0.156 | 1.512273 | -4.032 |  |  |
| 2020-09-16 | 2020-09-17 | 0.3941 | True | 0.196 | 1.471958 | -4.031 |  |  |
| 2020-11-05 | 2020-11-06 | 0.2283 | True | 0.545 | 1.431646 | -4.031 |  |  |
| 2020-12-16 | 2020-12-17 | 0.2191 | True | 0.325 | 1.425402 | -0.624 |  |  |
| 2021-01-27 | 2021-01-28 | 0.2982 | True | 0.107 | 1.419167 | -0.623 |  |  |
| 2021-03-17 | 2021-03-18 | 0.2191 | True | 0.12 | 1.412944 | -0.622 |  |  |
| 2021-04-28 | 2021-04-29 | 0.2631 | True | 0.34 | 1.406729 | -0.621 |  |  |
| 2021-06-16 | 2021-06-17 | 0.1063 | True | 0.264 | 1.423335 | 1.661 |  |  |
| 2021-07-28 | 2021-07-29 | 0.1889 | True | 0.189 | 1.439934 | 1.66 |  |  |
| 2021-09-22 | 2021-09-23 | 0.1063 | True | 0.115 | 1.456525 | 1.659 |  |  |
| 2021-11-03 | 2021-11-04 | 0.1063 | True | 0.047 | 1.473105 | 1.658 |  |  |
| 2021-12-15 | 2021-12-16 | 0.1063 | True | 0.054 | 1.489673 | 1.657 |  |  |
| 2022-01-26 | 2022-01-27 | 0.1446 | True | 0.126 | 1.506229 | 1.656 |  |  |
| 2022-03-16 | 2022-03-17 | 0.1446 | True | 0.205 | 1.522777 | 1.655 |  |  |
| 2022-05-04 | 2022-05-05 | 0.0964 | True | 0.287 | 1.539319 | 1.654 |  |  |
| 2022-06-15 | 2022-06-16 | 0.0 | True | 0.287 | 1.539319 | 0.0 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_ois | ois_effr 1W | 2.3651 | used |
| effr_ois | ois_effr 1M | 2.344 | used |
| effr_ois | ois_effr 2M | 2.301 | used |
| effr_ois | ois_effr 3M | 2.24335 | used |
| effr_ois | ois_effr 4M | 2.188 | used |
| effr_ois | ois_effr 5M | 2.141 | used |
| effr_ois | ois_effr 6M | 2.098 | used |
| effr_ois | ois_effr 7M | 2.055 | used |
| effr_ois | ois_effr 8M | 2.013 | used |
| effr_ois | ois_effr 9M | 1.978 | used |
| effr_ois | ois_effr 10M | 1.94619 | used |
| effr_ois | ois_effr 11M | 1.918 | used |
| effr_ois | ois_effr 1Y | 1.89194 | used |

Replica notes: ois_effr 3M: no new parcel; re-solved parcel 2 (2019-07-31); ois_effr 6M: no new parcel; re-solved parcel 4 (2019-10-30); ois_effr 9M: no new parcel; re-solved parcel 6 (2020-01-29); ois_effr 1Y: no new parcel; re-solved parcel 8 (2020-04-29)

## FF / OIS basis (bp, fit and replica)

| decision_date | effective_date | parcel | effr_fut_fit | effr_ois_fit | basis_fit_bp | basis_replica_bp |
| --- | --- | --- | --- | --- | --- | --- |
| None | None | stub | 2.395030420599813 | 2.368999224889338 | 2.603 | 2.537 |
| 2019-06-19 | 2019-06-20 | 1 | 2.329995 | 2.335658 | -0.566 | -0.511 |
| 2019-07-31 | 2019-08-01 | 2 | 2.135815 | 2.130973 | 0.484 | 0.5 |
| 2019-09-18 | 2019-09-19 | 3 | 1.967886 | 1.975878 | -0.799 | -0.737 |
| 2019-10-30 | 2019-10-31 | 4 | 1.895889 | 1.889305 | 0.658 | 2.011 |
| 2019-12-11 | 2019-12-12 | 5 | 1.75104 | 1.754711 | -0.367 | -1.929 |
| 2020-01-29 | 2020-01-30 | 6 | 1.684842 | 1.668083 | 1.676 | 2.559 |
| 2020-03-18 | 2020-03-19 | 7 | 1.625996 | 1.614708 | 1.129 | 1.227 |
| 2020-04-29 | 2020-04-30 | 8 | 1.595132 | 1.593933 | 0.12 | 0.442 |
| 2020-06-10 | 2020-06-11 | 9 | 1.54784 | 1.55259 | -0.475 |  |
| 2020-07-29 | 2020-07-30 | 10 | 1.514614 | 1.512273 | 0.234 |  |
| 2020-09-16 | 2020-09-17 | 11 | 1.474545 | 1.471958 | 0.259 |  |
| 2020-11-05 | 2020-11-06 | 12 | 1.456018 | 1.431646 | 2.437 |  |
| 2020-12-16 | 2020-12-17 | 13 | 1.436347 | 1.425402 | 1.094 |  |
| 2021-01-27 | 2021-01-28 | 14 | 1.419467 | 1.419167 | 0.03 |  |
| 2021-03-17 | 2021-03-18 | 15 | 1.434369 | 1.412944 | 2.142 |  |
| 2021-04-28 | 2021-04-29 | 16 | 1.435039 | 1.406729 | 2.831 |  |
| 2021-06-16 | 2021-06-17 | 17 | 1.435039 | 1.423335 | 1.17 |  |
| 2021-07-28 | 2021-07-29 | 18 | 1.435039 | 1.439934 | -0.49 |  |
| 2021-09-22 | 2021-09-23 | 19 | 1.435039 | 1.456525 | -2.149 |  |
| 2021-11-03 | 2021-11-04 | 20 | 1.435039 | 1.473105 | -3.807 |  |
| 2021-12-15 | 2021-12-16 | 21 | 1.435039 | 1.489673 | -5.463 |  |
| 2022-01-26 | 2022-01-27 | 22 | 1.435039 | 1.506229 | -7.119 |  |
| 2022-03-16 | 2022-03-17 | 23 | 1.435039 | 1.522777 | -8.774 |  |
| 2022-05-04 | 2022-05-05 | 24 | 1.435039 | 1.539319 | -10.428 |  |

## Stub

| curve | as_of | current_implied | replica_current_implied | stub_prior | stub_prior_source | anchor | spread | spread_median | spread_winsorised_mean | spread_obs | spread_estimator | spread_note | wirp_reach_meetings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | 2019-06-12 | 2.39503 | 2.395 | 2.403167 | anchor + spread (D7) | 2.375 | 0.02816666666666668 | 0.02499999999999991 | 0.02816666666666668 | 60 | winsorised_mean |  | 16 |
| effr_ois | 2019-06-12 | 2.368999 | 2.369633 | 2.403167 | anchor + spread (D7) | 2.375 | 0.02816666666666668 | 0.02499999999999991 | 0.02816666666666668 | 60 | winsorised_mean |  | 8 |
