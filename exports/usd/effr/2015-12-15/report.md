# USD EFFR front end, 2015-12-15

Anchor (target_midpoint) in effect: 0.125. Policy spread (winsorised_mean, D7): 0.35bp (winsorised mean 0.35bp, median 0.50bp; 60 fixings, 3 turn days dropped, window 2015-09-14..2015-12-14) **Loader reported blocking problems in the window (see check_market_data.py).**

## Curve `effr_fut` (ff_fut)

Fit: 24 quotes (0 dropped, 12 excluded by metadata), 2 IRLS iterations (converged); 25 parcels to 2018-12-15, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 0.1663 (replica 0.1690; stub prior 0.1285 from anchor + spread (D7)). WIRP replica reaches 16 meetings on 24 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2015-12-16 | False | False | 0.311296 | 0.145022 | 0.5801 | 58.01 | 0.311296 | -0.0 | 0.307796 | 18.28 | False | 0.006 | False |
| 2016-01-27 | False | False | 0.340745 | 0.174471 | 0.6979 | 11.78 | 0.34 | 0.075 | 0.337245 | 21.225 | False | 0.005 | False |
| 2016-03-16 | False | False | 0.43749 | 0.271216 | 1.0849 | 38.7 | 0.443333 | -0.584 | 0.43399 | 30.899 | False | 0.005 | False |
| 2016-04-27 | False | False | 0.47045 | 0.304176 | 1.2167 | 13.18 | 0.47 | 0.045 | 0.46695 | 34.195 | False | 0.005 | False |
| 2016-06-15 | False | False | 0.555066 | 0.388793 | 1.5552 | 33.85 | 0.56 | -0.493 | 0.551566 | 42.657 | False | 0.006 | False |
| 2016-07-27 | False | False | 0.600133 | 0.433859 | 1.7354 | 18.03 | 0.6 | 0.013 | 0.596633 | 47.163 | False | 0.006 | False |
| 2016-09-21 | False | False | 0.680167 | 0.513893 | 2.0556 | 32.01 | 0.68 | 0.017 | 0.676667 | 55.167 | False | 0.009 | False |
| 2016-11-02 | False | False | 0.735081 | 0.568808 | 2.2752 | 21.97 | 0.733571 | 0.151 | 0.731581 | 60.658 | False | 0.011 | False |
| 2016-12-14 | False | False | 0.822594 | 0.656321 | 2.6253 | 35.01 | 0.82 | 0.259 | 0.819094 | 69.409 | False | 0.011 | False |
| 2017-02-01 | False | False | 0.880071 | 0.713797 | 2.8552 | 22.99 | 0.882222 | -0.215 | 0.876571 | 75.157 | False | 0.021 | False |
| 2017-03-15 | False | False | 0.962883 | 0.796609 | 3.1864 | 33.12 | 0.965 | -0.212 | 0.959383 | 83.438 | False | 0.02 | False |
| 2017-05-03 | False | False | 1.021191 | 0.854917 | 3.4197 | 23.32 | 1.020357 | 0.083 | 1.017691 | 89.269 | False | 0.023 | False |
| 2017-06-14 | False | False | 1.073206 | 0.906933 | 3.6277 | 20.81 | 1.075937 | -0.273 | 1.069706 | 94.471 | False | 0.023 | False |
| 2017-07-26 | False | False | 1.150629 | 0.984356 | 3.9374 | 30.97 | 1.145 | 0.563 | 1.147129 | 102.213 | False | 0.019 | False |
| 2017-09-20 | False | False | 1.212871 | 1.046597 | 4.1864 | 24.9 | 1.21 | 0.287 | 1.209371 | 108.437 | False | 0.022 | False |
| 2017-11-01 | False | False | 1.266769 | 1.100495 | 4.402 | 21.56 | 1.266897 | -0.013 | 1.263269 | 113.827 | False | 0.023 | False |
| 2017-12-13 | False | False | 1.266769 | 1.100495 | 4.402 | 0.0 |  |  | 1.263269 | 113.827 | True | 0.024 | True |
| 2018-01-31 | False | False | 1.266769 | 1.100495 | 4.402 | 0.0 |  |  | 1.263269 | 113.827 | True | 0.024 | True |
| 2018-03-21 | False | False | 1.266769 | 1.100495 | 4.402 | 0.0 |  |  | 1.263269 | 113.827 | True | 0.025 | True |
| 2018-05-02 | False | False | 1.266769 | 1.100495 | 4.402 | 0.0 |  |  | 1.263269 | 113.827 | True | 0.025 | True |
| 2018-06-13 | False | False | 1.266769 | 1.100495 | 4.402 | 0.0 |  |  | 1.263269 | 113.827 | True | 0.026 | True |
| 2018-08-01 | False | False | 1.266769 | 1.100495 | 4.402 | 0.0 |  |  | 1.263269 | 113.827 | True | 0.026 | True |
| 2018-09-26 | False | False | 1.266769 | 1.100495 | 4.402 | 0.0 |  |  | 1.263269 | 113.827 | True | 0.027 | True |
| 2018-11-08 | False | False | 1.266769 | 1.100495 | 4.402 | 0.0 |  |  | 1.263269 | 113.827 | True | 0.027 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | used | 24 | 0.007 | 0.257 | 0.862 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

| curve | instrument | contract | ticker | status | reason | residual_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2017-12 | FFZ17 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2018-01 | FFF18 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2018-02 | FFG18 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2018-03 | FFH18 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2018-04 | FFJ18 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2018-05 | FFK18 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2018-06 | FFM18 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2018-07 | FFN18 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2018-08 | FFQ18 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2018-09 | FFU18 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2018-10 | FFV18 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2018-11 | FFX18 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2015-12 | FFZ15 Comdty | 0.2225 | 0.018 | 0.198 | 0.91 |
| effr_fut | ff_fut | 2016-01 | FFF16 Comdty | 0.315 | -0.01 | -0.338 | 0.972 |
| effr_fut | ff_fut | 2016-05 | FFK16 Comdty | 0.47 | -0.045 | -0.509 | 0.912 |
| effr_fut | ff_fut | 2016-10 | FFV16 Comdty | 0.68 | -0.017 | -0.258 | 0.935 |
| effr_fut | ff_fut | 2017-10 | FFV17 Comdty | 1.21 | -0.287 | -3.955 | 0.927 |
| effr_fut | ff_fut | 2017-11 | FFX17 Comdty | 1.265 | 0.003 | 5.215 | 0.999 |

### Stale and outside-listing inputs

| curve | flag | instrument | contract | status | detail |
| --- | --- | --- | --- | --- | --- |
| effr_fut | outside_listing | ff_fut | 2018-08 | excluded | loader: FFQ18 Comdty|PX_LAST quoted from 2015-08-31, modelled first listing 2015-09-01 |
| effr_fut | outside_listing | ff_fut | 2018-09 | excluded | loader: FFU18 Comdty|PX_LAST quoted from 2015-09-30, modelled first listing 2015-10-01 |
| effr_fut | outside_listing | ff_fut | 2018-10 | excluded | loader: FFV18 Comdty|PX_LAST quoted from 2015-10-30, modelled first listing 2015-11-02 |
| effr_fut | outside_listing | ff_fut | 2018-11 | excluded | loader: FFX18 Comdty|PX_LAST quoted from 2015-11-16, modelled first listing 2015-12-01 |

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2015-12-15 | 1.0 | False | 0.083 | 0.166274 |  | 0.169028 | -0.275 |
| 2015-12-16 | 2015-12-17 | 1.0 | False | 0.006 | 0.311296 | 14.502 | 0.311296 | -0.0 |
| 2016-01-27 | 2016-01-28 | 1.0 | False | 0.005 | 0.340745 | 2.945 | 0.34 | 0.075 |
| 2016-03-16 | 2016-03-17 | 1.0 | False | 0.005 | 0.43749 | 9.674 | 0.443333 | -0.584 |
| 2016-04-27 | 2016-04-28 | 1.0 | False | 0.005 | 0.47045 | 3.296 | 0.47 | 0.045 |
| 2016-06-15 | 2016-06-16 | 1.0 | False | 0.006 | 0.555066 | 8.462 | 0.56 | -0.493 |
| 2016-07-27 | 2016-07-28 | 1.0 | False | 0.006 | 0.600133 | 4.507 | 0.6 | 0.013 |
| 2016-09-21 | 2016-09-22 | 1.0 | False | 0.009 | 0.680167 | 8.003 | 0.68 | 0.017 |
| 2016-11-02 | 2016-11-03 | 1.0 | False | 0.011 | 0.735081 | 5.491 | 0.733571 | 0.151 |
| 2016-12-14 | 2016-12-15 | 1.0 | False | 0.011 | 0.822594 | 8.751 | 0.82 | 0.259 |
| 2017-02-01 | 2017-02-02 | 1.0 | False | 0.021 | 0.880071 | 5.748 | 0.882222 | -0.215 |
| 2017-03-15 | 2017-03-16 | 1.0 | False | 0.02 | 0.962883 | 8.281 | 0.965 | -0.212 |
| 2017-05-03 | 2017-05-04 | 1.0 | False | 0.023 | 1.021191 | 5.831 | 1.020357 | 0.083 |
| 2017-06-14 | 2017-06-15 | 1.0 | False | 0.023 | 1.073206 | 5.202 | 1.075937 | -0.273 |
| 2017-07-26 | 2017-07-27 | 1.0 | False | 0.019 | 1.150629 | 7.742 | 1.145 | 0.563 |
| 2017-09-20 | 2017-09-21 | 1.0 | False | 0.022 | 1.212871 | 6.224 | 1.21 | 0.287 |
| 2017-11-01 | 2017-11-02 | 1.0 | False | 0.023 | 1.266769 | 5.39 | 1.266897 | -0.013 |
| 2017-12-13 | 2017-12-14 | 0.0 | True | 0.024 | 1.266769 | 0.0 |  |  |
| 2018-01-31 | 2018-02-01 | 0.0 | True | 0.024 | 1.266769 | 0.0 |  |  |
| 2018-03-21 | 2018-03-22 | 0.0 | True | 0.025 | 1.266769 | 0.0 |  |  |
| 2018-05-02 | 2018-05-03 | 0.0 | True | 0.025 | 1.266769 | 0.0 |  |  |
| 2018-06-13 | 2018-06-14 | 0.0 | True | 0.026 | 1.266769 | 0.0 |  |  |
| 2018-08-01 | 2018-08-02 | 0.0 | True | 0.026 | 1.266769 | 0.0 |  |  |
| 2018-09-26 | 2018-09-27 | 0.0 | True | 0.027 | 1.266769 | 0.0 |  |  |
| 2018-11-08 | 2018-11-09 | 0.0 | True | 0.027 | 1.266769 | 0.0 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_fut | ff_fut 2015-12 | 0.2224999999999966 | used |
| effr_fut | ff_fut 2016-01 | 0.3149999999999977 | used |
| effr_fut | ff_fut 2016-02 | 0.3400000000000034 | used |
| effr_fut | ff_fut 2016-03 | 0.39000000000000057 | used |
| effr_fut | ff_fut 2016-04 | 0.4399999999999977 | used |
| effr_fut | ff_fut 2016-05 | 0.46999999999999886 | used |
| effr_fut | ff_fut 2016-06 | 0.5150000000000006 | used |
| effr_fut | ff_fut 2016-07 | 0.5600000000000023 | used |
| effr_fut | ff_fut 2016-08 | 0.5999999999999943 | used |
| effr_fut | ff_fut 2016-09 | 0.625 | used |
| effr_fut | ff_fut 2016-10 | 0.6800000000000068 | used |
| effr_fut | ff_fut 2016-11 | 0.730000000000004 | used |
| effr_fut | ff_fut 2016-12 | 0.7849999999999966 | used |
| effr_fut | ff_fut 2017-01 | 0.8199999999999932 | used |
| effr_fut | ff_fut 2017-02 | 0.8799999999999955 | used |
| effr_fut | ff_fut 2017-03 | 0.9200000000000017 | used |
| effr_fut | ff_fut 2017-04 | 0.9650000000000034 | used |
| effr_fut | ff_fut 2017-05 | 1.0150000000000006 | used |
| effr_fut | ff_fut 2017-06 | 1.0499999999999972 | used |
| effr_fut | ff_fut 2017-07 | 1.0849999999999937 | used |
| effr_fut | ff_fut 2017-08 | 1.144999999999996 | used |
| effr_fut | ff_fut 2017-09 | 1.1800000000000068 | used |
| effr_fut | ff_fut 2017-10 | 1.2099999999999937 | used |
| effr_fut | ff_fut 2017-11 | 1.2650000000000006 | used |

Replica notes: ff_fut 2016-05: no new parcel; re-solved parcel 4 (2016-04-27); ff_fut 2016-08: no new parcel; re-solved parcel 6 (2016-07-27); ff_fut 2016-10: no new parcel; re-solved parcel 7 (2016-09-21); ff_fut 2017-01: no new parcel; re-solved parcel 9 (2016-12-14); ff_fut 2017-04: no new parcel; re-solved parcel 11 (2017-03-15); ff_fut 2017-08: no new parcel; re-solved parcel 14 (2017-07-26); ff_fut 2017-10: no new parcel; re-solved parcel 15 (2017-09-20)

## Curve `effr_ois` (ois_effr)

Fit: 18 quotes (0 dropped, 0 excluded by metadata), 6 IRLS iterations (converged); 26 parcels to 2018-12-26, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 0.1395 (replica 0.1500; stub prior 0.1285 from anchor + spread (D7)). WIRP replica reaches 8 meetings on 13 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2015-12-16 | False | False | 0.31513 | 0.175652 | 0.7026 | 70.26 | 0.316458 | -0.133 | 0.31163 | 18.663 | False | 0.003 | False |
| 2016-01-27 | False | False | 0.344017 | 0.204538 | 0.8182 | 11.55 | 0.342286 | 0.173 | 0.340517 | 21.552 | False | 0.009 | False |
| 2016-03-16 | False | False | 0.441782 | 0.302304 | 1.2092 | 39.11 | 0.443438 | -0.166 | 0.438282 | 31.328 | False | 0.02 | False |
| 2016-04-27 | False | False | 0.467492 | 0.328014 | 1.3121 | 10.28 | 0.468801 | -0.131 | 0.463992 | 33.899 | False | 0.025 | False |
| 2016-06-15 | False | False | 0.548527 | 0.409048 | 1.6362 | 32.41 | 0.54593 | 0.26 | 0.545027 | 42.003 | False | 0.038 | False |
| 2016-07-27 | False | False | 0.601374 | 0.461896 | 1.8476 | 21.14 | 0.599635 | 0.174 | 0.597874 | 47.287 | False | 0.036 | False |
| 2016-09-21 | False | False | 0.658394 | 0.518916 | 2.0757 | 22.81 | 0.674977 | -1.658 | 0.654894 | 52.989 | False | 0.062 | False |
| 2016-11-02 | False | False | 0.739754 | 0.600275 | 2.4011 | 32.54 | 0.744792 | -0.504 | 0.736254 | 61.125 | False | 0.077 | False |
| 2016-12-14 | False | False | 0.840381 | 0.700903 | 2.8036 | 40.25 |  |  | 0.836881 | 71.188 | False | 0.303 | True |
| 2017-02-01 | False | False | 0.887827 | 0.748349 | 2.9934 | 18.98 |  |  | 0.884327 | 75.933 | True | 0.109 | True |
| 2017-03-15 | False | False | 0.935298 | 0.79582 | 3.1833 | 18.99 |  |  | 0.931798 | 80.68 | True | 0.09 | True |
| 2017-05-03 | False | False | 0.982804 | 0.843326 | 3.3733 | 19.0 |  |  | 0.979304 | 85.43 | True | 0.283 | True |
| 2017-06-14 | False | False | 1.030336 | 0.890858 | 3.5634 | 19.01 |  |  | 1.026836 | 90.184 | True | 0.477 | True |
| 2017-07-26 | False | False | 1.112209 | 0.972731 | 3.8909 | 32.75 |  |  | 1.108709 | 98.371 | True | 0.171 | True |
| 2017-09-20 | False | False | 1.194074 | 1.054596 | 4.2184 | 32.75 |  |  | 1.190574 | 106.557 | True | 0.142 | True |
| 2017-11-01 | False | False | 1.275928 | 1.136449 | 4.5458 | 32.74 |  |  | 1.272428 | 114.743 | True | 0.447 | True |
| 2017-12-13 | False | False | 1.357774 | 1.218295 | 4.8732 | 32.74 |  |  | 1.354274 | 122.927 | True | 0.755 | True |
| 2018-01-31 | False | False | 1.387935 | 1.248456 | 4.9938 | 12.06 |  |  | 1.384435 | 125.943 | True | 0.537 | True |
| 2018-03-21 | False | False | 1.418086 | 1.278608 | 5.1144 | 12.06 |  |  | 1.414586 | 128.959 | True | 0.319 | True |
| 2018-05-02 | False | False | 1.448222 | 1.308744 | 5.235 | 12.05 |  |  | 1.444722 | 131.972 | True | 0.105 | True |
| 2018-06-13 | False | False | 1.47834 | 1.338862 | 5.3554 | 12.05 |  |  | 1.47484 | 134.984 | True | 0.122 | True |
| 2018-08-01 | False | False | 1.508439 | 1.368961 | 5.4758 | 12.04 |  |  | 1.504939 | 137.994 | True | 0.338 | True |
| 2018-09-26 | False | False | 1.538522 | 1.399043 | 5.5962 | 12.03 |  |  | 1.535022 | 141.002 | True | 0.557 | True |
| 2018-11-08 | False | False | 1.568595 | 1.429117 | 5.7165 | 12.03 |  |  | 1.565095 | 144.009 | True | 0.776 | True |
| 2018-12-19 | False | False | 1.568595 | 1.429117 | 5.7165 | 0.0 |  |  | 1.565095 | 144.009 | True | 0.776 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | used | 18 | -0.036 | 0.326 | 1.316 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

_none_

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | 1Y | USSO1 Curncy | 0.519 | 0.037 | 0.565 | 0.934 |
| effr_ois | ois_effr | 18M | USSO1F Curncy | 0.65 | -0.002 | -0.799 | 0.998 |
| effr_ois | ois_effr | 2Y | USSO2 Curncy | 0.777 | 0.0 | 0.224 | 0.999 |
| effr_ois | ois_effr | 3Y | USSO3 Curncy | 1.005 | 0.0 | 5.179 | 1.0 |

### Stale and outside-listing inputs

_none_

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2015-12-15 | 0.0 | True | 0.243 | 0.139478 |  | 0.15 | -1.052 |
| 2015-12-16 | 2015-12-17 | 1.0 | False | 0.003 | 0.31513 | 17.565 | 0.316458 | -0.133 |
| 2016-01-27 | 2016-01-28 | 1.0 | False | 0.009 | 0.344017 | 2.889 | 0.342286 | 0.173 |
| 2016-03-16 | 2016-03-17 | 1.0 | False | 0.02 | 0.441782 | 9.777 | 0.443438 | -0.166 |
| 2016-04-27 | 2016-04-28 | 1.0 | False | 0.025 | 0.467492 | 2.571 | 0.468801 | -0.131 |
| 2016-06-15 | 2016-06-16 | 1.0 | False | 0.038 | 0.548527 | 8.103 | 0.54593 | 0.26 |
| 2016-07-27 | 2016-07-28 | 1.0 | False | 0.036 | 0.601374 | 5.285 | 0.599635 | 0.174 |
| 2016-09-21 | 2016-09-22 | 1.0 | False | 0.062 | 0.658394 | 5.702 | 0.674977 | -1.658 |
| 2016-11-02 | 2016-11-03 | 1.0 | False | 0.077 | 0.739754 | 8.136 | 0.744792 | -0.504 |
| 2016-12-14 | 2016-12-15 | 1.0 | False | 0.303 | 0.840381 | 10.063 |  |  |
| 2017-02-01 | 2017-02-02 | 0.2969 | True | 0.109 | 0.887827 | 4.745 |  |  |
| 2017-03-15 | 2017-03-16 | 0.4041 | True | 0.09 | 0.935298 | 4.747 |  |  |
| 2017-05-03 | 2017-05-04 | 0.2969 | True | 0.283 | 0.982804 | 4.751 |  |  |
| 2017-06-14 | 2017-06-15 | 0.1796 | True | 0.477 | 1.030336 | 4.753 |  |  |
| 2017-07-26 | 2017-07-27 | 0.3863 | True | 0.171 | 1.112209 | 8.187 |  |  |
| 2017-09-20 | 2017-09-21 | 0.2173 | True | 0.142 | 1.194074 | 8.186 |  |  |
| 2017-11-01 | 2017-11-02 | 0.2173 | True | 0.447 | 1.275928 | 8.185 |  |  |
| 2017-12-13 | 2017-12-14 | 0.1222 | True | 0.755 | 1.357774 | 8.185 |  |  |
| 2018-01-31 | 2018-02-01 | 0.1431 | True | 0.537 | 1.387935 | 3.016 |  |  |
| 2018-03-21 | 2018-03-22 | 0.1051 | True | 0.319 | 1.418086 | 3.015 |  |  |
| 2018-05-02 | 2018-05-03 | 0.1051 | True | 0.105 | 1.448222 | 3.014 |  |  |
| 2018-06-13 | 2018-06-14 | 0.1431 | True | 0.122 | 1.47834 | 3.012 |  |  |
| 2018-08-01 | 2018-08-02 | 0.1869 | True | 0.338 | 1.508439 | 3.01 |  |  |
| 2018-09-26 | 2018-09-27 | 0.1102 | True | 0.557 | 1.538522 | 3.008 |  |  |
| 2018-11-08 | 2018-11-09 | 0.086 | True | 0.776 | 1.568595 | 3.007 |  |  |
| 2018-12-19 | 2018-12-20 | 0.0 | True | 0.776 | 1.568595 | 0.0 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_ois | ois_effr 1W | 0.31775 | used |
| effr_ois | ois_effr 1M | 0.3165 | used |
| effr_ois | ois_effr 2M | 0.325 | used |
| effr_ois | ois_effr 3M | 0.3305 | used |
| effr_ois | ois_effr 4M | 0.36 | used |
| effr_ois | ois_effr 5M | 0.3785 | used |
| effr_ois | ois_effr 6M | 0.3945 | used |
| effr_ois | ois_effr 7M | 0.417 | used |
| effr_ois | ois_effr 8M | 0.4375 | used |
| effr_ois | ois_effr 9M | 0.457 | used |
| effr_ois | ois_effr 10M | 0.4765 | used |
| effr_ois | ois_effr 11M | 0.495 | used |
| effr_ois | ois_effr 1Y | 0.519 | used |

Replica notes: ois_effr 1M: no new parcel; re-solved parcel 1 (2015-12-16); ois_effr 3M: no new parcel; re-solved parcel 2 (2016-01-27); ois_effr 6M: no new parcel; re-solved parcel 4 (2016-04-27); ois_effr 9M: no new parcel; re-solved parcel 6 (2016-07-27); ois_effr 1Y: no new parcel; re-solved parcel 8 (2016-11-02); stub parcel not priced by any instrument (the first one starts after the next effective date): set to the last fixing 0.1500 (2015-12-14)

## FF / OIS basis (bp, fit and replica)

| decision_date | effective_date | parcel | effr_fut_fit | effr_ois_fit | basis_fit_bp | basis_replica_bp |
| --- | --- | --- | --- | --- | --- | --- |
| None | None | stub | 0.16627380399931777 | 0.13947824269484618 | 2.68 | 1.903 |
| 2015-12-16 | 2015-12-17 | 1 | 0.311296 | 0.31513 | -0.383 | -0.516 |
| 2016-01-27 | 2016-01-28 | 2 | 0.340745 | 0.344017 | -0.327 | -0.229 |
| 2016-03-16 | 2016-03-17 | 3 | 0.43749 | 0.441782 | -0.429 | -0.01 |
| 2016-04-27 | 2016-04-28 | 4 | 0.47045 | 0.467492 | 0.296 | 0.12 |
| 2016-06-15 | 2016-06-16 | 5 | 0.555066 | 0.548527 | 0.654 | 1.407 |
| 2016-07-27 | 2016-07-28 | 6 | 0.600133 | 0.601374 | -0.124 | 0.036 |
| 2016-09-21 | 2016-09-22 | 7 | 0.680167 | 0.658394 | 2.177 | 0.502 |
| 2016-11-02 | 2016-11-03 | 8 | 0.735081 | 0.739754 | -0.467 | -1.122 |
| 2016-12-14 | 2016-12-15 | 9 | 0.822594 | 0.840381 | -1.779 |  |
| 2017-02-01 | 2017-02-02 | 10 | 0.880071 | 0.887827 | -0.776 |  |
| 2017-03-15 | 2017-03-16 | 11 | 0.962883 | 0.935298 | 2.758 |  |
| 2017-05-03 | 2017-05-04 | 12 | 1.021191 | 0.982804 | 3.839 |  |
| 2017-06-14 | 2017-06-15 | 13 | 1.073206 | 1.030336 | 4.287 |  |
| 2017-07-26 | 2017-07-27 | 14 | 1.150629 | 1.112209 | 3.842 |  |
| 2017-09-20 | 2017-09-21 | 15 | 1.212871 | 1.194074 | 1.88 |  |
| 2017-11-01 | 2017-11-02 | 16 | 1.266769 | 1.275928 | -0.916 |  |
| 2017-12-13 | 2017-12-14 | 17 | 1.266769 | 1.357774 | -9.1 |  |
| 2018-01-31 | 2018-02-01 | 18 | 1.266769 | 1.387935 | -12.117 |  |
| 2018-03-21 | 2018-03-22 | 19 | 1.266769 | 1.418086 | -15.132 |  |
| 2018-05-02 | 2018-05-03 | 20 | 1.266769 | 1.448222 | -18.145 |  |
| 2018-06-13 | 2018-06-14 | 21 | 1.266769 | 1.47834 | -21.157 |  |
| 2018-08-01 | 2018-08-02 | 22 | 1.266769 | 1.508439 | -24.167 |  |
| 2018-09-26 | 2018-09-27 | 23 | 1.266769 | 1.538522 | -27.175 |  |
| 2018-11-08 | 2018-11-09 | 24 | 1.266769 | 1.568595 | -30.183 |  |

## Stub

| curve | as_of | current_implied | replica_current_implied | stub_prior | stub_prior_source | anchor | spread | spread_median | spread_winsorised_mean | spread_obs | spread_estimator | spread_note | wirp_reach_meetings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | 2015-12-15 | 0.166274 | 0.169028 | 0.1285 | anchor + spread (D7) | 0.125 | 0.003500000000000003 | 0.0050000000000000044 | 0.003500000000000003 | 60 | winsorised_mean |  | 16 |
| effr_ois | 2015-12-15 | 0.139478 | 0.15 | 0.1285 | anchor + spread (D7) | 0.125 | 0.003500000000000003 | 0.0050000000000000044 | 0.003500000000000003 | 60 | winsorised_mean |  | 8 |
