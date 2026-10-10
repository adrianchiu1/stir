# USD EFFR front end, 2014-09-16

Anchor (target_midpoint) in effect: 0.125. Policy spread (winsorised_mean, D7): -3.28bp (winsorised mean -3.28bp, median -3.50bp; 60 fixings, 3 turn days dropped, window 2014-06-17..2014-09-15)

## Curve `effr_fut` (ff_fut)

Fit: 27 quotes (0 dropped, 9 excluded by metadata), 3 IRLS iterations (converged); 25 parcels to 2017-09-16, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 0.0960 (replica 0.1022; stub prior 0.0922 from anchor + spread (D7)). WIRP replica reaches 18 meetings on 27 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2014-09-17 | False | False | 0.089845 | -0.006143 | -0.0246 | -2.46 | 0.089655 | 0.019 | 0.122678 | -0.232 | False | 0.021 | False |
| 2014-10-29 | False | False | 0.095606 | -0.000382 | -0.0015 | 2.3 | 0.095 | 0.061 | 0.128439 | 0.344 | False | 0.006 | False |
| 2014-12-17 | False | False | 0.103734 | 0.007746 | 0.031 | 3.25 | 0.106071 | -0.234 | 0.136567 | 1.157 | False | 0.006 | False |
| 2015-01-28 | False | False | 0.120318 | 0.02433 | 0.0973 | 6.63 | 0.12 | 0.032 | 0.153151 | 2.815 | False | 0.014 | False |
| 2015-03-18 | False | False | 0.188549 | 0.092561 | 0.3702 | 27.29 | 0.191538 | -0.299 | 0.221383 | 9.638 | False | 0.006 | False |
| 2015-04-29 | False | False | 0.233612 | 0.137624 | 0.5505 | 18.02 | 0.235 | -0.139 | 0.266445 | 14.144 | False | 0.005 | False |
| 2015-06-17 | False | False | 0.358969 | 0.262981 | 1.0519 | 50.14 | 0.350385 | 0.858 | 0.391803 | 26.68 | False | 0.006 | False |
| 2015-07-29 | False | False | 0.435322 | 0.339334 | 1.3573 | 30.54 | 0.435 | 0.032 | 0.468155 | 34.316 | False | 0.006 | False |
| 2015-09-17 | False | False | 0.581989 | 0.486001 | 1.944 | 58.67 | 0.585 | -0.301 | 0.614823 | 48.982 | False | 0.01 | False |
| 2015-10-28 | False | False | 0.669435 | 0.573447 | 2.2938 | 34.98 | 0.67 | -0.056 | 0.702268 | 57.727 | False | 0.007 | False |
| 2015-12-16 | False | False | 0.817273 | 0.721285 | 2.8851 | 59.14 | 0.814667 | 0.261 | 0.850107 | 72.511 | False | 0.008 | False |
| 2016-01-27 | False | False | 0.910264 | 0.814276 | 3.2571 | 37.2 | 0.91 | 0.026 | 0.943098 | 81.81 | False | 0.011 | False |
| 2016-03-16 | False | False | 1.053434 | 0.957446 | 3.8298 | 57.27 | 1.054667 | -0.123 | 1.086267 | 96.127 | False | 0.018 | False |
| 2016-04-27 | False | False | 1.170561 | 1.074573 | 4.2983 | 46.85 | 1.17 | 0.056 | 1.203394 | 107.839 | False | 0.019 | False |
| 2016-06-15 | False | False | 1.306553 | 1.210564 | 4.8423 | 54.4 | 1.31 | -0.345 | 1.339386 | 121.439 | False | 0.023 | False |
| 2016-07-27 | False | False | 1.456002 | 1.360014 | 5.4401 | 59.78 | 1.445 | 1.1 | 1.488835 | 136.384 | False | 0.019 | False |
| 2016-09-21 | False | False | 1.599745 | 1.503757 | 6.015 | 57.5 | 1.595 | 0.475 | 1.632579 | 150.758 | False | 0.022 | False |
| 2016-11-02 | False | False | 1.701745 | 1.605757 | 6.423 | 40.8 | 1.702143 | -0.04 | 1.734579 | 160.958 | False | 0.024 | False |
| 2016-12-14 | False | False | 1.701745 | 1.605757 | 6.423 | 0.0 |  |  | 1.734579 | 160.958 | True | 0.024 | True |
| 2017-02-01 | False | False | 1.701745 | 1.605757 | 6.423 | 0.0 |  |  | 1.734579 | 160.958 | True | 0.025 | True |
| 2017-03-15 | False | False | 1.701745 | 1.605757 | 6.423 | 0.0 |  |  | 1.734579 | 160.958 | True | 0.025 | True |
| 2017-05-03 | False | False | 1.701745 | 1.605757 | 6.423 | 0.0 |  |  | 1.734579 | 160.958 | True | 0.026 | True |
| 2017-06-14 | False | False | 1.701745 | 1.605757 | 6.423 | 0.0 |  |  | 1.734579 | 160.958 | True | 0.026 | True |
| 2017-07-26 | False | False | 1.701745 | 1.605757 | 6.423 | 0.0 |  |  | 1.734579 | 160.958 | True | 0.027 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | used | 27 | 0.004 | 0.393 | 1.588 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

| curve | instrument | contract | ticker | status | reason | residual_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2016-12 | FFZ16 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2017-01 | FFF17 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2017-02 | FFG17 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2017-03 | FFH17 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2017-04 | FFJ17 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2017-05 | FFK17 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2017-06 | FFM17 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2017-07 | FFN17 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2017-08 | FFQ17 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2015-04 | FFJ15 Comdty | 0.19 | -0.005 | -0.32 | 0.984 |
| effr_fut | ff_fut | 2015-08 | FFQ15 Comdty | 0.435 | -0.032 | -0.355 | 0.909 |
| effr_fut | ff_fut | 2016-02 | FFG16 Comdty | 0.91 | -0.026 | -0.404 | 0.935 |
| effr_fut | ff_fut | 2016-10 | FFV16 Comdty | 1.595 | -0.475 | -8.164 | 0.942 |
| effr_fut | ff_fut | 2016-11 | FFX16 Comdty | 1.695 | 0.005 | 9.531 | 0.999 |

### Stale and outside-listing inputs

| curve | flag | instrument | contract | status | detail |
| --- | --- | --- | --- | --- | --- |
| effr_fut | stale | ff_fut | 2014-09 | used | unchanged 22 observations |
| effr_fut | stale | ff_fut | 2014-10 | used | unchanged 22 observations |
| effr_fut | stale | ff_fut | 2015-02 | used | unchanged 18 observations |
| effr_fut | stale | ff_fut | 2015-03 | used | unchanged 7 observations |

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2014-09-16 | 1.0 | False | 0.191 | 0.095988 |  | 0.102241 | -0.625 |
| 2014-09-17 | 2014-09-18 | 1.0 | False | 0.021 | 0.089845 | -0.614 | 0.089655 | 0.019 |
| 2014-10-29 | 2014-10-30 | 1.0 | False | 0.006 | 0.095606 | 0.576 | 0.095 | 0.061 |
| 2014-12-17 | 2014-12-18 | 1.0 | False | 0.006 | 0.103734 | 0.813 | 0.106071 | -0.234 |
| 2015-01-28 | 2015-01-29 | 1.0 | False | 0.014 | 0.120318 | 1.658 | 0.12 | 0.032 |
| 2015-03-18 | 2015-03-19 | 1.0 | False | 0.006 | 0.188549 | 6.823 | 0.191538 | -0.299 |
| 2015-04-29 | 2015-04-30 | 1.0 | False | 0.005 | 0.233612 | 4.506 | 0.235 | -0.139 |
| 2015-06-17 | 2015-06-18 | 1.0 | False | 0.006 | 0.358969 | 12.536 | 0.350385 | 0.858 |
| 2015-07-29 | 2015-07-30 | 1.0 | False | 0.006 | 0.435322 | 7.635 | 0.435 | 0.032 |
| 2015-09-17 | 2015-09-18 | 1.0 | False | 0.01 | 0.581989 | 14.667 | 0.585 | -0.301 |
| 2015-10-28 | 2015-10-29 | 1.0 | False | 0.007 | 0.669435 | 8.745 | 0.67 | -0.056 |
| 2015-12-16 | 2015-12-17 | 1.0 | False | 0.008 | 0.817273 | 14.784 | 0.814667 | 0.261 |
| 2016-01-27 | 2016-01-28 | 1.0 | False | 0.011 | 0.910264 | 9.299 | 0.91 | 0.026 |
| 2016-03-16 | 2016-03-17 | 1.0 | False | 0.018 | 1.053434 | 14.317 | 1.054667 | -0.123 |
| 2016-04-27 | 2016-04-28 | 1.0 | False | 0.019 | 1.170561 | 11.713 | 1.17 | 0.056 |
| 2016-06-15 | 2016-06-16 | 1.0 | False | 0.023 | 1.306553 | 13.599 | 1.31 | -0.345 |
| 2016-07-27 | 2016-07-28 | 1.0 | False | 0.019 | 1.456002 | 14.945 | 1.445 | 1.1 |
| 2016-09-21 | 2016-09-22 | 1.0 | False | 0.022 | 1.599745 | 14.374 | 1.595 | 0.475 |
| 2016-11-02 | 2016-11-03 | 1.0 | False | 0.024 | 1.701745 | 10.2 | 1.702143 | -0.04 |
| 2016-12-14 | 2016-12-15 | 0.0 | True | 0.024 | 1.701745 | 0.0 |  |  |
| 2017-02-01 | 2017-02-02 | 0.0 | True | 0.025 | 1.701745 | 0.0 |  |  |
| 2017-03-15 | 2017-03-16 | 0.0 | True | 0.025 | 1.701745 | 0.0 |  |  |
| 2017-05-03 | 2017-05-04 | 0.0 | True | 0.026 | 1.701745 | 0.0 |  |  |
| 2017-06-14 | 2017-06-15 | 0.0 | True | 0.026 | 1.701745 | 0.0 |  |  |
| 2017-07-26 | 2017-07-27 | 0.0 | True | 0.027 | 1.701745 | 0.0 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_fut | ff_fut 2014-09 | 0.09000000000000341 | used |
| effr_fut | ff_fut 2014-10 | 0.09000000000000341 | used |
| effr_fut | ff_fut 2014-11 | 0.09499999999999886 | used |
| effr_fut | ff_fut 2014-12 | 0.09999999999999432 | used |
| effr_fut | ff_fut 2015-01 | 0.10500000000000398 | used |
| effr_fut | ff_fut 2015-02 | 0.12000000000000455 | used |
| effr_fut | ff_fut 2015-03 | 0.15000000000000568 | used |
| effr_fut | ff_fut 2015-04 | 0.18999999999999773 | used |
| effr_fut | ff_fut 2015-05 | 0.23499999999999943 | used |
| effr_fut | ff_fut 2015-06 | 0.2849999999999966 | used |
| effr_fut | ff_fut 2015-07 | 0.3649999999999949 | used |
| effr_fut | ff_fut 2015-08 | 0.4350000000000023 | used |
| effr_fut | ff_fut 2015-09 | 0.5 | used |
| effr_fut | ff_fut 2015-10 | 0.5900000000000034 | used |
| effr_fut | ff_fut 2015-11 | 0.6700000000000017 | used |
| effr_fut | ff_fut 2015-12 | 0.7399999999999949 | used |
| effr_fut | ff_fut 2016-01 | 0.8299999999999983 | used |
| effr_fut | ff_fut 2016-02 | 0.9099999999999966 | used |
| effr_fut | ff_fut 2016-03 | 0.980000000000004 | used |
| effr_fut | ff_fut 2016-04 | 1.0649999999999977 | used |
| effr_fut | ff_fut 2016-05 | 1.1700000000000017 | used |
| effr_fut | ff_fut 2016-06 | 1.2399999999999949 | used |
| effr_fut | ff_fut 2016-07 | 1.3250000000000028 | used |
| effr_fut | ff_fut 2016-08 | 1.4449999999999932 | used |
| effr_fut | ff_fut 2016-09 | 1.5150000000000006 | used |
| effr_fut | ff_fut 2016-10 | 1.5949999999999989 | used |
| effr_fut | ff_fut 2016-11 | 1.6949999999999932 | used |

Replica notes: ff_fut 2015-02: no new parcel; re-solved parcel 4 (2015-01-28); ff_fut 2015-05: no new parcel; re-solved parcel 6 (2015-04-29); ff_fut 2015-08: no new parcel; re-solved parcel 8 (2015-07-29); ff_fut 2015-11: no new parcel; re-solved parcel 10 (2015-10-28); ff_fut 2016-02: no new parcel; re-solved parcel 12 (2016-01-27); ff_fut 2016-05: no new parcel; re-solved parcel 14 (2016-04-27); ff_fut 2016-08: no new parcel; re-solved parcel 16 (2016-07-27); ff_fut 2016-10: no new parcel; re-solved parcel 17 (2016-09-21)

## Curve `effr_ois` (ois_effr)

Fit: 18 quotes (0 dropped, 0 excluded by metadata), 4 IRLS iterations (converged); 26 parcels to 2017-09-27, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 0.0919 (replica 0.0900; stub prior 0.0922 from anchor + spread (D7)). WIRP replica reaches 8 meetings on 13 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2014-09-17 | False | False | 0.088057 | -0.003868 | -0.0155 | -1.55 | 0.090497 | -0.244 | 0.12089 | -0.411 | False | 0.002 | False |
| 2014-10-29 | False | False | 0.095705 | 0.00378 | 0.0151 | 3.06 | 0.093269 | 0.244 | 0.128538 | 0.354 | False | 0.009 | False |
| 2014-12-17 | False | False | 0.098408 | 0.006483 | 0.0259 | 1.08 | 0.095731 | 0.268 | 0.131241 | 0.624 | False | 0.02 | False |
| 2015-01-28 | False | False | 0.128041 | 0.036116 | 0.1445 | 11.85 | 0.12825 | -0.021 | 0.160875 | 3.587 | False | 0.025 | False |
| 2015-03-18 | False | False | 0.158943 | 0.067018 | 0.2681 | 12.36 | 0.161786 | -0.284 | 0.191776 | 6.678 | False | 0.037 | False |
| 2015-04-29 | False | False | 0.249015 | 0.15709 | 0.6284 | 36.03 | 0.248642 | 0.037 | 0.281848 | 15.685 | False | 0.039 | False |
| 2015-06-17 | False | False | 0.396134 | 0.304209 | 1.2168 | 58.85 | 0.394865 | 0.127 | 0.428968 | 30.397 | False | 0.054 | False |
| 2015-07-29 | False | False | 0.384621 | 0.292696 | 1.1708 | -4.61 | 0.384684 | -0.006 | 0.417455 | 29.245 | False | 0.053 | False |
| 2015-09-17 | False | False | 0.556264 | 0.464339 | 1.8574 | 68.66 |  |  | 0.589097 | 46.41 | True | 0.398 | True |
| 2015-10-28 | False | False | 0.669989 | 0.578064 | 2.3123 | 45.49 |  |  | 0.702822 | 57.782 | True | 0.144 | True |
| 2015-12-16 | False | False | 0.783699 | 0.691774 | 2.7671 | 45.48 |  |  | 0.816532 | 69.153 | True | 0.114 | True |
| 2016-01-27 | False | False | 0.89739 | 0.805465 | 3.2219 | 45.48 |  |  | 0.930223 | 80.522 | True | 0.367 | True |
| 2016-03-16 | False | False | 1.011066 | 0.919141 | 3.6766 | 45.47 |  |  | 1.043899 | 91.89 | True | 0.621 | True |
| 2016-04-27 | False | False | 1.14771 | 1.055785 | 4.2231 | 54.66 |  |  | 1.180543 | 105.554 | True | 0.229 | True |
| 2016-06-15 | False | False | 1.284367 | 1.192442 | 4.7698 | 54.66 |  |  | 1.3172 | 119.22 | True | 0.168 | True |
| 2016-07-27 | False | False | 1.421036 | 1.329111 | 5.3164 | 54.67 |  |  | 1.453869 | 132.887 | True | 0.56 | True |
| 2016-09-21 | False | False | 1.536837 | 1.444912 | 5.7796 | 46.32 |  |  | 1.56967 | 144.467 | True | 0.437 | True |
| 2016-11-02 | False | False | 1.652604 | 1.560679 | 6.2427 | 46.31 |  |  | 1.685437 | 156.044 | True | 0.315 | True |
| 2016-12-14 | False | False | 1.768311 | 1.676386 | 6.7055 | 46.28 |  |  | 1.801145 | 167.614 | True | 0.194 | True |
| 2017-02-01 | False | False | 1.883944 | 1.792019 | 7.1681 | 46.25 |  |  | 1.916777 | 179.178 | True | 0.076 | True |
| 2017-03-15 | False | False | 1.999497 | 1.907572 | 7.6303 | 46.22 |  |  | 2.03233 | 190.733 | True | 0.063 | True |
| 2017-05-03 | False | False | 2.114975 | 2.02305 | 8.0922 | 46.19 |  |  | 2.147808 | 202.281 | True | 0.182 | True |
| 2017-06-14 | False | False | 2.230394 | 2.138469 | 8.5539 | 46.17 |  |  | 2.263227 | 213.823 | True | 0.306 | True |
| 2017-07-26 | False | False | 2.345778 | 2.253854 | 9.0154 | 46.15 |  |  | 2.378612 | 225.361 | True | 0.432 | True |
| 2017-09-20 | False | False | 2.345778 | 2.253854 | 9.0154 | 0.0 |  |  | 2.378612 | 225.361 | True | 0.432 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | used | 18 | -0.0 | 0.083 | 0.244 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

_none_

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | 18M | USSO1F Curncy | 0.379 | 0.002 | 1.252 | 0.999 |
| effr_ois | ois_effr | 2Y | USSO2 Curncy | 0.5935 | -0.002 | -3.171 | 0.999 |
| effr_ois | ois_effr | 3Y | USSO3 Curncy | 1.042 | 0.002 | 19.792 | 1.0 |

### Stale and outside-listing inputs

_none_

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2014-09-16 | 0.0 | True | 0.243 | 0.091925 |  | 0.09 | 0.192 |
| 2014-09-17 | 2014-09-18 | 1.0 | False | 0.002 | 0.088057 | -0.387 | 0.090497 | -0.244 |
| 2014-10-29 | 2014-10-30 | 1.0 | False | 0.009 | 0.095705 | 0.765 | 0.093269 | 0.244 |
| 2014-12-17 | 2014-12-18 | 1.0 | False | 0.02 | 0.098408 | 0.27 | 0.095731 | 0.268 |
| 2015-01-28 | 2015-01-29 | 1.0 | False | 0.025 | 0.128041 | 2.963 | 0.12825 | -0.021 |
| 2015-03-18 | 2015-03-19 | 1.0 | False | 0.037 | 0.158943 | 3.09 | 0.161786 | -0.284 |
| 2015-04-29 | 2015-04-30 | 1.0 | False | 0.039 | 0.249015 | 9.007 | 0.248642 | 0.037 |
| 2015-06-17 | 2015-06-18 | 1.0 | False | 0.054 | 0.396134 | 14.712 | 0.394865 | 0.127 |
| 2015-07-29 | 2015-07-30 | 1.0 | False | 0.053 | 0.384621 | -1.151 | 0.384684 | -0.006 |
| 2015-09-17 | 2015-09-18 | 0.2038 | True | 0.398 | 0.556264 | 17.164 |  |  |
| 2015-10-28 | 2015-10-29 | 0.2911 | True | 0.144 | 0.669989 | 11.372 |  |  |
| 2015-12-16 | 2015-12-17 | 0.2139 | True | 0.114 | 0.783699 | 11.371 |  |  |
| 2016-01-27 | 2016-01-28 | 0.2911 | True | 0.367 | 0.89739 | 11.369 |  |  |
| 2016-03-16 | 2016-03-17 | 0.1944 | True | 0.621 | 1.011066 | 11.368 |  |  |
| 2016-04-27 | 2016-04-28 | 0.2775 | True | 0.229 | 1.14771 | 13.664 |  |  |
| 2016-06-15 | 2016-06-16 | 0.2039 | True | 0.168 | 1.284367 | 13.666 |  |  |
| 2016-07-27 | 2016-07-28 | 0.3247 | True | 0.56 | 1.421036 | 13.667 |  |  |
| 2016-09-21 | 2016-09-22 | 0.1073 | True | 0.437 | 1.536837 | 11.58 |  |  |
| 2016-11-02 | 2016-11-03 | 0.1073 | True | 0.315 | 1.652604 | 11.577 |  |  |
| 2016-12-14 | 2016-12-15 | 0.1461 | True | 0.194 | 1.768311 | 11.571 |  |  |
| 2017-02-01 | 2017-02-02 | 0.1073 | True | 0.076 | 1.883944 | 11.563 |  |  |
| 2017-03-15 | 2017-03-16 | 0.1461 | True | 0.063 | 1.999497 | 11.555 |  |  |
| 2017-05-03 | 2017-05-04 | 0.1073 | True | 0.182 | 2.114975 | 11.548 |  |  |
| 2017-06-14 | 2017-06-15 | 0.1073 | True | 0.306 | 2.230394 | 11.542 |  |  |
| 2017-07-26 | 2017-07-27 | 0.1708 | True | 0.432 | 2.345778 | 11.538 |  |  |
| 2017-09-20 | 2017-09-21 | 0.0 | True | 0.432 | 2.345778 | 0.0 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_ois | ois_effr 1W | 0.087 | used |
| effr_ois | ois_effr 1M | 0.0905 | used |
| effr_ois | ois_effr 2M | 0.091 | used |
| effr_ois | ois_effr 3M | 0.092 | used |
| effr_ois | ois_effr 4M | 0.093 | used |
| effr_ois | ois_effr 5M | 0.1 | used |
| effr_ois | ois_effr 6M | 0.1025 | used |
| effr_ois | ois_effr 7M | 0.1115 | used |
| effr_ois | ois_effr 8M | 0.124 | used |
| effr_ois | ois_effr 9M | 0.138 | used |
| effr_ois | ois_effr 10M | 0.165 | used |
| effr_ois | ois_effr 11M | 0.185 | used |
| effr_ois | ois_effr 1Y | 0.2015 | used |

Replica notes: ois_effr 1M: no new parcel; re-solved parcel 1 (2014-09-17); ois_effr 3M: no new parcel; re-solved parcel 2 (2014-10-29); ois_effr 6M: no new parcel; re-solved parcel 4 (2015-01-28); ois_effr 9M: no new parcel; re-solved parcel 6 (2015-04-29); ois_effr 1Y: no new parcel; re-solved parcel 8 (2015-07-29); stub parcel not priced by any instrument (the first one starts after the next effective date): set to the last fixing 0.0900 (2014-09-15)

## FF / OIS basis (bp, fit and replica)

| decision_date | effective_date | parcel | effr_fut_fit | effr_ois_fit | basis_fit_bp | basis_replica_bp |
| --- | --- | --- | --- | --- | --- | --- |
| None | None | stub | 0.09598807093675464 | 0.0919249079593322 | 0.406 | 1.224 |
| 2014-09-17 | 2014-09-18 | 1 | 0.089845 | 0.088057 | 0.179 | -0.084 |
| 2014-10-29 | 2014-10-30 | 2 | 0.095606 | 0.095705 | -0.01 | 0.173 |
| 2014-12-17 | 2014-12-18 | 3 | 0.103734 | 0.098408 | 0.533 | 1.034 |
| 2015-01-28 | 2015-01-29 | 4 | 0.120318 | 0.128041 | -0.772 | -0.825 |
| 2015-03-18 | 2015-03-19 | 5 | 0.188549 | 0.158943 | 2.961 | 2.975 |
| 2015-04-29 | 2015-04-30 | 6 | 0.233612 | 0.249015 | -1.54 | -1.364 |
| 2015-06-17 | 2015-06-18 | 7 | 0.358969 | 0.396134 | -3.717 | -4.448 |
| 2015-07-29 | 2015-07-30 | 8 | 0.435322 | 0.384621 | 5.07 | 5.032 |
| 2015-09-17 | 2015-09-18 | 9 | 0.581989 | 0.556264 | 2.573 |  |
| 2015-10-28 | 2015-10-29 | 10 | 0.669435 | 0.669989 | -0.055 |  |
| 2015-12-16 | 2015-12-17 | 11 | 0.817273 | 0.783699 | 3.357 |  |
| 2016-01-27 | 2016-01-28 | 12 | 0.910264 | 0.89739 | 1.287 |  |
| 2016-03-16 | 2016-03-17 | 13 | 1.053434 | 1.011066 | 4.237 |  |
| 2016-04-27 | 2016-04-28 | 14 | 1.170561 | 1.14771 | 2.285 |  |
| 2016-06-15 | 2016-06-16 | 15 | 1.306553 | 1.284367 | 2.219 |  |
| 2016-07-27 | 2016-07-28 | 16 | 1.456002 | 1.421036 | 3.497 |  |
| 2016-09-21 | 2016-09-22 | 17 | 1.599745 | 1.536837 | 6.291 |  |
| 2016-11-02 | 2016-11-03 | 18 | 1.701745 | 1.652604 | 4.914 |  |
| 2016-12-14 | 2016-12-15 | 19 | 1.701745 | 1.768311 | -6.657 |  |
| 2017-02-01 | 2017-02-02 | 20 | 1.701745 | 1.883944 | -18.22 |  |
| 2017-03-15 | 2017-03-16 | 21 | 1.701745 | 1.999497 | -29.775 |  |
| 2017-05-03 | 2017-05-04 | 22 | 1.701745 | 2.114975 | -41.323 |  |
| 2017-06-14 | 2017-06-15 | 23 | 1.701745 | 2.230394 | -52.865 |  |
| 2017-07-26 | 2017-07-27 | 24 | 1.701745 | 2.345778 | -64.403 |  |

## Stub

| curve | as_of | current_implied | replica_current_implied | stub_prior | stub_prior_source | anchor | spread | spread_median | spread_winsorised_mean | spread_obs | spread_estimator | spread_note | wirp_reach_meetings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | 2014-09-16 | 0.095988 | 0.102241 | 0.092167 | anchor + spread (D7) | 0.125 | -0.03283333333333333 | -0.035 | -0.03283333333333333 | 60 | winsorised_mean |  | 18 |
| effr_ois | 2014-09-16 | 0.091925 | 0.09 | 0.092167 | anchor + spread (D7) | 0.125 | -0.03283333333333333 | -0.035 | -0.03283333333333333 | 60 | winsorised_mean |  | 8 |
