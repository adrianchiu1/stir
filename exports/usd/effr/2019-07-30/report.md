# USD EFFR front end, 2019-07-30

Anchor (target_midpoint) in effect: 2.375. Policy spread (winsorised_mean, D7): 1.47bp (winsorised mean 1.47bp, median 1.50bp; 60 fixings, 3 turn days dropped, window 2019-04-30..2019-07-29) **Loader reported blocking problems in the window (see check_market_data.py).**

## Curve `effr_fut` (ff_fut)

Fit: 24 quotes (1 dropped, 12 excluded by metadata), 2 IRLS iterations (converged); 26 parcels to 2022-07-30, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 2.4225 (replica 2.4275; stub prior 2.3897 from anchor + spread (D7)). WIRP replica reaches 16 meetings on 24 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2019-07-31 | False | False | 2.109585 | -0.312884 | -1.2515 | -125.15 | 2.1075 | 0.208 | 2.094918 | -28.008 | False | 0.004 | False |
| 2019-09-18 | False | False | 1.939451 | -0.483018 | -1.9321 | -68.05 | 1.95125 | -1.18 | 1.924784 | -45.022 | False | 0.005 | False |
| 2019-10-30 | False | False | 1.845986 | -0.576483 | -2.3059 | -37.39 | 1.845 | 0.099 | 1.831319 | -54.368 | False | 0.005 | False |
| 2019-12-11 | False | False | 1.74695 | -0.675519 | -2.7021 | -39.61 | 1.752 | -0.505 | 1.732283 | -64.272 | False | 0.004 | False |
| 2020-01-29 | False | False | 1.670331 | -0.752137 | -3.0085 | -30.65 | 1.67 | 0.033 | 1.655665 | -71.934 | False | 0.005 | False |
| 2020-03-18 | False | False | 1.606735 | -0.815734 | -3.2629 | -25.44 | 1.610385 | -0.365 | 1.592068 | -78.293 | False | 0.005 | False |
| 2020-04-29 | False | False | 1.565021 | -0.857448 | -3.4298 | -16.69 | 1.565 | 0.002 | 1.550354 | -82.465 | False | 0.005 | False |
| 2020-06-10 | False | False | 1.512188 | -0.91028 | -3.6411 | -21.13 | 1.5125 | -0.031 | 1.497522 | -87.748 | False | 0.006 | False |
| 2020-07-29 | False | False | 1.48011 | -0.942359 | -3.7694 | -12.83 | 1.48 | 0.011 | 1.465443 | -90.956 | False | 0.008 | False |
| 2020-09-16 | False | False | 1.435298 | -0.98717 | -3.9487 | -17.92 | 1.435 | 0.03 | 1.420631 | -95.437 | False | 0.011 | False |
| 2020-11-05 | False | False | 1.415896 | -1.006573 | -4.0263 | -7.76 | 1.417 | -0.11 | 1.401229 | -97.377 | False | 0.018 | False |
| 2020-12-16 | False | False | 1.385145 | -1.037324 | -4.1493 | -12.3 | 1.381867 | 0.328 | 1.370478 | -100.452 | False | 0.021 | False |
| 2021-01-27 | False | False | 1.373317 | -1.049152 | -4.1966 | -4.73 | 1.375 | -0.168 | 1.35865 | -101.635 | False | 0.021 | False |
| 2021-03-17 | False | False | 1.362419 | -1.060049 | -4.2402 | -4.36 | 1.352857 | 0.956 | 1.347752 | -102.725 | False | 0.042 | False |
| 2021-04-28 | False | False | 1.527907 | -0.894562 | -3.5782 | 66.2 | 1.375 | 15.291 | 1.51324 | -86.176 | False | 0.595 | False |
| 2021-06-16 | False | False | 1.486945 | -0.935524 | -3.7421 | -16.38 |  |  | 1.472278 | -90.272 | True | 0.397 | True |
| 2021-07-28 | False | False | 1.445983 | -0.976486 | -3.9059 | -16.38 |  |  | 1.431316 | -94.368 | True | 0.2 | True |
| 2021-09-22 | False | False | 1.40502 | -1.017448 | -4.0698 | -16.38 | 1.405 | 0.002 | 1.390354 | -98.465 | False | 0.022 | False |
| 2021-11-03 | False | False | 1.40502 | -1.017448 | -4.0698 | 0.0 |  |  | 1.390354 | -98.465 | True | 0.023 | True |
| 2021-12-15 | False | False | 1.40502 | -1.017448 | -4.0698 | 0.0 |  |  | 1.390354 | -98.465 | True | 0.023 | True |
| 2022-01-26 | False | False | 1.40502 | -1.017448 | -4.0698 | 0.0 |  |  | 1.390354 | -98.465 | True | 0.024 | True |
| 2022-03-16 | False | False | 1.40502 | -1.017448 | -4.0698 | 0.0 |  |  | 1.390354 | -98.465 | True | 0.024 | True |
| 2022-05-04 | False | False | 1.40502 | -1.017448 | -4.0698 | 0.0 |  |  | 1.390354 | -98.465 | True | 0.025 | True |
| 2022-06-15 | False | False | 1.40502 | -1.017448 | -4.0698 | 0.0 |  |  | 1.390354 | -98.465 | True | 0.025 | True |
| 2022-07-27 | False | False | 1.40502 | -1.017448 | -4.0698 | 0.0 |  |  | 1.390354 | -98.465 | True | 0.026 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | dropped | 1 | -15.291 | 15.291 | 15.291 |
| effr_fut | ff_fut | used | 23 | 0.01 | 0.155 | 0.347 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

| curve | instrument | contract | ticker | status | reason | residual_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2021-05 | FFK21 Comdty | dropped | leave-one-out residual -15.29bp, over 6.0 x its effective noise 2.24bp (alone pinned a parcel) | -15.291 |
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
| effr_fut | ff_fut | 2022-06 | FFM22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2019-07 | FFN19 Comdty | 2.405 | 0.032 | 0.35 | 0.907 |
| effr_fut | ff_fut | 2019-11 | FFX19 Comdty | 1.845 | -0.099 | -1.253 | 0.921 |
| effr_fut | ff_fut | 2020-04 | FFJ20 Comdty | 1.605 | -0.034 | -0.405 | 0.915 |
| effr_fut | ff_fut | 2020-05 | FFK20 Comdty | 1.565 | -0.002 | -0.055 | 0.962 |
| effr_fut | ff_fut | 2020-08 | FFQ20 Comdty | 1.48 | -0.011 | -0.16 | 0.932 |
| effr_fut | ff_fut | 2021-04 | FFJ21 Comdty | 1.375 | 0.155 | 2.136 | 0.927 |
| effr_fut | ff_fut | 2021-10 | FFV21 Comdty | 1.405 | -0.002 | -13.938 | 1.0 |

### Stale and outside-listing inputs

| curve | flag | instrument | contract | status | detail |
| --- | --- | --- | --- | --- | --- |
| effr_fut | outside_listing | ff_fut | 2022-03 | excluded | loader: FFH22 Comdty|PX_LAST quoted from 2019-03-29, modelled first listing 2019-04-01 |
| effr_fut | outside_listing | ff_fut | 2022-04 | excluded | loader: FFJ22 Comdty|PX_LAST quoted from 2019-04-30, modelled first listing 2019-05-01 |
| effr_fut | outside_listing | ff_fut | 2022-05 | excluded | loader: FFK22 Comdty|PX_LAST quoted from 2019-05-31, modelled first listing 2019-06-03 |
| effr_fut | outside_listing | ff_fut | 2022-06 | excluded | loader: FFM22 Comdty|PX_LAST quoted from 2019-06-28, modelled first listing 2019-07-01 |

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2019-07-30 | 1.0 | False | 0.074 | 2.422468 |  | 2.4275 | -0.503 |
| 2019-07-31 | 2019-08-01 | 1.0 | False | 0.004 | 2.109585 | -31.288 | 2.1075 | 0.208 |
| 2019-09-18 | 2019-09-19 | 1.0 | False | 0.005 | 1.939451 | -17.013 | 1.95125 | -1.18 |
| 2019-10-30 | 2019-10-31 | 1.0 | False | 0.005 | 1.845986 | -9.347 | 1.845 | 0.099 |
| 2019-12-11 | 2019-12-12 | 1.0 | False | 0.004 | 1.74695 | -9.904 | 1.752 | -0.505 |
| 2020-01-29 | 2020-01-30 | 1.0 | False | 0.005 | 1.670331 | -7.662 | 1.67 | 0.033 |
| 2020-03-18 | 2020-03-19 | 1.0 | False | 0.005 | 1.606735 | -6.36 | 1.610385 | -0.365 |
| 2020-04-29 | 2020-04-30 | 1.0 | False | 0.005 | 1.565021 | -4.171 | 1.565 | 0.002 |
| 2020-06-10 | 2020-06-11 | 1.0 | False | 0.006 | 1.512188 | -5.283 | 1.5125 | -0.031 |
| 2020-07-29 | 2020-07-30 | 1.0 | False | 0.008 | 1.48011 | -3.208 | 1.48 | 0.011 |
| 2020-09-16 | 2020-09-17 | 1.0 | False | 0.011 | 1.435298 | -4.481 | 1.435 | 0.03 |
| 2020-11-05 | 2020-11-06 | 1.0 | False | 0.018 | 1.415896 | -1.94 | 1.417 | -0.11 |
| 2020-12-16 | 2020-12-17 | 1.0 | False | 0.021 | 1.385145 | -3.075 | 1.381867 | 0.328 |
| 2021-01-27 | 2021-01-28 | 1.0 | False | 0.021 | 1.373317 | -1.183 | 1.375 | -0.168 |
| 2021-03-17 | 2021-03-18 | 1.0 | False | 0.042 | 1.362419 | -1.09 | 1.352857 | 0.956 |
| 2021-04-28 | 2021-04-29 | 1.0 | False | 0.595 | 1.527907 | 16.549 | 1.375 | 15.291 |
| 2021-06-16 | 2021-06-17 | 0.0 | True | 0.397 | 1.486945 | -4.096 |  |  |
| 2021-07-28 | 2021-07-29 | 0.0 | True | 0.2 | 1.445983 | -4.096 |  |  |
| 2021-09-22 | 2021-09-23 | 1.0 | False | 0.022 | 1.40502 | -4.096 | 1.405 | 0.002 |
| 2021-11-03 | 2021-11-04 | 0.0 | True | 0.023 | 1.40502 | 0.0 |  |  |
| 2021-12-15 | 2021-12-16 | 0.0 | True | 0.023 | 1.40502 | 0.0 |  |  |
| 2022-01-26 | 2022-01-27 | 0.0 | True | 0.024 | 1.40502 | 0.0 |  |  |
| 2022-03-16 | 2022-03-17 | 0.0 | True | 0.024 | 1.40502 | 0.0 |  |  |
| 2022-05-04 | 2022-05-05 | 0.0 | True | 0.025 | 1.40502 | 0.0 |  |  |
| 2022-06-15 | 2022-06-16 | 0.0 | True | 0.025 | 1.40502 | 0.0 |  |  |
| 2022-07-27 | 2022-07-28 | 0.0 | True | 0.026 | 1.40502 | 0.0 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_fut | ff_fut 2019-07 | 2.405000000000001 | used |
| effr_fut | ff_fut 2019-08 | 2.1075000000000017 | used |
| effr_fut | ff_fut 2019-09 | 2.0450000000000017 | used |
| effr_fut | ff_fut 2019-10 | 1.9350000000000023 | used |
| effr_fut | ff_fut 2019-11 | 1.8449999999999989 | used |
| effr_fut | ff_fut 2019-12 | 1.7849999999999966 | used |
| effr_fut | ff_fut 2020-01 | 1.7399999999999949 | used |
| effr_fut | ff_fut 2020-02 | 1.6700000000000017 | used |
| effr_fut | ff_fut 2020-03 | 1.644999999999996 | used |
| effr_fut | ff_fut 2020-04 | 1.605000000000004 | used |
| effr_fut | ff_fut 2020-05 | 1.5649999999999977 | used |
| effr_fut | ff_fut 2020-06 | 1.5300000000000011 | used |
| effr_fut | ff_fut 2020-07 | 1.5100000000000051 | used |
| effr_fut | ff_fut 2020-08 | 1.480000000000004 | used |
| effr_fut | ff_fut 2020-09 | 1.4599999999999937 | used |
| effr_fut | ff_fut 2020-10 | 1.4350000000000023 | used |
| effr_fut | ff_fut 2020-11 | 1.4200000000000017 | used |
| effr_fut | ff_fut 2020-12 | 1.4000000000000057 | used |
| effr_fut | ff_fut 2021-01 | 1.3850000000000051 | used |
| effr_fut | ff_fut 2021-02 | 1.375 | used |
| effr_fut | ff_fut 2021-03 | 1.3649999999999949 | used |
| effr_fut | ff_fut 2021-04 | 1.375 | used |
| effr_fut | ff_fut 2021-05 | 1.375 | used |
| effr_fut | ff_fut 2021-10 | 1.4050000000000011 | used |

Replica notes: ff_fut 2019-11: no new parcel; re-solved parcel 3 (2019-10-30); ff_fut 2020-02: no new parcel; re-solved parcel 5 (2020-01-29); ff_fut 2020-05: no new parcel; re-solved parcel 7 (2020-04-29); ff_fut 2020-08: no new parcel; re-solved parcel 9 (2020-07-29); ff_fut 2020-10: no new parcel; re-solved parcel 10 (2020-09-16); ff_fut 2021-02: no new parcel; re-solved parcel 13 (2021-01-27); ff_fut 2021-05: no new parcel; re-solved parcel 15 (2021-04-28)

## Curve `effr_ois` (ois_effr)

Fit: 18 quotes (0 dropped, 0 excluded by metadata), 3 IRLS iterations (converged); 26 parcels to 2022-08-10, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 2.3731 (replica 2.4000; stub prior 2.3897 from anchor + spread (D7)). WIRP replica reaches 8 meetings on 13 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2019-07-31 | False | False | 2.108724 | -0.264417 | -1.0577 | -105.77 | 2.110587 | -0.186 | 2.094057 | -28.094 | False | 0.002 | False |
| 2019-09-18 | False | False | 1.944084 | -0.429057 | -1.7162 | -65.86 | 1.937638 | 0.645 | 1.929417 | -44.558 | False | 0.011 | False |
| 2019-10-30 | False | False | 1.839391 | -0.53375 | -2.135 | -41.88 | 1.8448 | -0.541 | 1.824724 | -55.028 | False | 0.022 | False |
| 2019-12-11 | False | False | 1.745838 | -0.627302 | -2.5092 | -37.42 | 1.738754 | 0.708 | 1.731172 | -64.383 | False | 0.026 | False |
| 2020-01-29 | False | False | 1.678188 | -0.694953 | -2.7798 | -27.06 | 1.689521 | -1.133 | 1.663521 | -71.148 | False | 0.036 | False |
| 2020-03-18 | False | False | 1.599715 | -0.773426 | -3.0937 | -31.39 | 1.594158 | 0.556 | 1.585048 | -78.995 | False | 0.049 | False |
| 2020-04-29 | False | False | 1.582832 | -0.790308 | -3.1612 | -6.75 | 1.583325 | -0.049 | 1.568166 | -80.683 | False | 0.056 | False |
| 2020-06-10 | False | False | 1.522875 | -0.850266 | -3.4011 | -23.98 | 1.519228 | 0.365 | 1.508208 | -86.679 | False | 0.06 | False |
| 2020-07-29 | False | False | 1.477377 | -0.895764 | -3.5831 | -18.2 |  |  | 1.46271 | -91.229 | False | 0.283 | True |
| 2020-09-16 | False | False | 1.450641 | -0.922499 | -3.69 | -10.69 |  |  | 1.435975 | -93.903 | True | 0.097 | True |
| 2020-11-05 | False | False | 1.423918 | -0.949223 | -3.7969 | -10.69 |  |  | 1.409251 | -96.575 | True | 0.095 | True |
| 2020-12-16 | False | False | 1.39721 | -0.975931 | -3.9037 | -10.68 |  |  | 1.382543 | -99.246 | True | 0.281 | True |
| 2021-01-27 | False | False | 1.370513 | -1.002627 | -4.0105 | -10.68 |  |  | 1.355847 | -101.915 | True | 0.468 | True |
| 2021-03-17 | False | False | 1.379364 | -0.993777 | -3.9751 | 3.54 |  |  | 1.364697 | -101.03 | True | 0.168 | True |
| 2021-04-28 | False | False | 1.388216 | -0.984925 | -3.9397 | 3.54 |  |  | 1.373549 | -100.145 | True | 0.139 | True |
| 2021-06-16 | False | False | 1.397069 | -0.976071 | -3.9043 | 3.54 |  |  | 1.382402 | -99.26 | True | 0.438 | True |
| 2021-07-28 | False | False | 1.405924 | -0.967217 | -3.8689 | 3.54 |  |  | 1.391257 | -98.374 | True | 0.74 | True |
| 2021-09-22 | False | False | 1.41126 | -0.961881 | -3.8475 | 2.13 |  |  | 1.396593 | -97.841 | True | 0.528 | True |
| 2021-11-03 | False | False | 1.416593 | -0.956547 | -3.8262 | 2.13 |  |  | 1.401927 | -97.307 | True | 0.317 | True |
| 2021-12-15 | False | False | 1.421923 | -0.951217 | -3.8049 | 2.13 |  |  | 1.407257 | -96.774 | True | 0.109 | True |
| 2022-01-26 | False | False | 1.427249 | -0.945891 | -3.7836 | 2.13 |  |  | 1.412582 | -96.242 | True | 0.112 | True |
| 2022-03-16 | False | False | 1.43257 | -0.940571 | -3.7623 | 2.13 |  |  | 1.417903 | -95.71 | True | 0.321 | True |
| 2022-05-04 | False | False | 1.437886 | -0.935254 | -3.741 | 2.13 |  |  | 1.42322 | -95.178 | True | 0.533 | True |
| 2022-06-15 | False | False | 1.443199 | -0.929942 | -3.7198 | 2.13 |  |  | 1.428532 | -94.647 | True | 0.746 | True |
| 2022-07-27 | False | False | 1.44851 | -0.924631 | -3.6985 | 2.12 |  |  | 1.433843 | -94.116 | True | 0.959 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | used | 18 | -0.0 | 0.107 | 0.354 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

_none_

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | 9M | USSOI Curncy | 1.833 | 0.005 | 0.066 | 0.919 |
| effr_ois | ois_effr | 18M | USSO1F Curncy | 1.659 | -0.001 | -0.235 | 0.998 |
| effr_ois | ois_effr | 2Y | USSO2 Curncy | 1.59566 | -0.0 | -0.136 | 0.999 |
| effr_ois | ois_effr | 3Y | USSO3 Curncy | 1.543 | 0.0 | 0.965 | 1.0 |

### Stale and outside-listing inputs

_none_

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2019-07-30 | 0.0 | True | 0.243 | 2.373141 |  | 2.4 | -2.686 |
| 2019-07-31 | 2019-08-01 | 1.0 | False | 0.002 | 2.108724 | -26.442 | 2.110587 | -0.186 |
| 2019-09-18 | 2019-09-19 | 1.0 | False | 0.011 | 1.944084 | -16.464 | 1.937638 | 0.645 |
| 2019-10-30 | 2019-10-31 | 1.0 | False | 0.022 | 1.839391 | -10.469 | 1.8448 | -0.541 |
| 2019-12-11 | 2019-12-12 | 1.0 | False | 0.026 | 1.745838 | -9.355 | 1.738754 | 0.708 |
| 2020-01-29 | 2020-01-30 | 1.0 | False | 0.036 | 1.678188 | -6.765 | 1.689521 | -1.133 |
| 2020-03-18 | 2020-03-19 | 1.0 | False | 0.049 | 1.599715 | -7.847 | 1.594158 | 0.556 |
| 2020-04-29 | 2020-04-30 | 1.0 | False | 0.056 | 1.582832 | -1.688 | 1.583325 | -0.049 |
| 2020-06-10 | 2020-06-11 | 1.0 | False | 0.06 | 1.522875 | -5.996 | 1.519228 | 0.365 |
| 2020-07-29 | 2020-07-30 | 1.0 | False | 0.283 | 1.477377 | -4.55 |  |  |
| 2020-09-16 | 2020-09-17 | 0.4197 | True | 0.097 | 1.450641 | -2.674 |  |  |
| 2020-11-05 | 2020-11-06 | 0.2822 | True | 0.095 | 1.423918 | -2.672 |  |  |
| 2020-12-16 | 2020-12-17 | 0.2961 | True | 0.281 | 1.39721 | -2.671 |  |  |
| 2021-01-27 | 2021-01-28 | 0.2556 | True | 0.468 | 1.370513 | -2.67 |  |  |
| 2021-03-17 | 2021-03-18 | 0.2216 | True | 0.168 | 1.379364 | 0.885 |  |  |
| 2021-04-28 | 2021-04-29 | 0.3016 | True | 0.139 | 1.388216 | 0.885 |  |  |
| 2021-06-16 | 2021-06-17 | 0.2216 | True | 0.438 | 1.397069 | 0.885 |  |  |
| 2021-07-28 | 2021-07-29 | 0.1669 | True | 0.74 | 1.405924 | 0.885 |  |  |
| 2021-09-22 | 2021-09-23 | 0.108 | True | 0.528 | 1.41126 | 0.534 |  |  |
| 2021-11-03 | 2021-11-04 | 0.108 | True | 0.317 | 1.416593 | 0.533 |  |  |
| 2021-12-15 | 2021-12-16 | 0.108 | True | 0.109 | 1.421923 | 0.533 |  |  |
| 2022-01-26 | 2022-01-27 | 0.147 | True | 0.112 | 1.427249 | 0.533 |  |  |
| 2022-03-16 | 2022-03-17 | 0.147 | True | 0.321 | 1.43257 | 0.532 |  |  |
| 2022-05-04 | 2022-05-05 | 0.108 | True | 0.533 | 1.437886 | 0.532 |  |  |
| 2022-06-15 | 2022-06-16 | 0.108 | True | 0.746 | 1.443199 | 0.531 |  |  |
| 2022-07-27 | 2022-07-28 | 0.001 | True | 0.959 | 1.44851 | 0.531 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_ois | ois_effr 1W | 2.1055 | used |
| effr_ois | ois_effr 1M | 2.1125 | used |
| effr_ois | ois_effr 2M | 2.0817 | used |
| effr_ois | ois_effr 3M | 2.035 | used |
| effr_ois | ois_effr 4M | 1.989 | used |
| effr_ois | ois_effr 5M | 1.949 | used |
| effr_ois | ois_effr 6M | 1.915 | used |
| effr_ois | ois_effr 7M | 1.88678 | used |
| effr_ois | ois_effr 8M | 1.85881 | used |
| effr_ois | ois_effr 9M | 1.833 | used |
| effr_ois | ois_effr 10M | 1.81 | used |
| effr_ois | ois_effr 11M | 1.788 | used |
| effr_ois | ois_effr 1Y | 1.76631 | used |

Replica notes: ois_effr 1M: no new parcel; re-solved parcel 1 (2019-07-31); ois_effr 3M: no new parcel; re-solved parcel 2 (2019-09-18); ois_effr 6M: no new parcel; re-solved parcel 4 (2019-12-11); ois_effr 9M: no new parcel; re-solved parcel 6 (2020-03-18); ois_effr 1Y: no new parcel; re-solved parcel 8 (2020-06-10); stub parcel not priced by any instrument (the first one starts after the next effective date): set to the last fixing 2.4000 (2019-07-29)

## FF / OIS basis (bp, fit and replica)

| decision_date | effective_date | parcel | effr_fut_fit | effr_ois_fit | basis_fit_bp | basis_replica_bp |
| --- | --- | --- | --- | --- | --- | --- |
| None | None | stub | 2.422468487623128 | 2.3731406115613054 | 4.933 | 2.75 |
| 2019-07-31 | 2019-08-01 | 1 | 2.109585 | 2.108724 | 0.086 | -0.309 |
| 2019-09-18 | 2019-09-19 | 2 | 1.939451 | 1.944084 | -0.463 | 1.361 |
| 2019-10-30 | 2019-10-31 | 3 | 1.845986 | 1.839391 | 0.659 | 0.02 |
| 2019-12-11 | 2019-12-12 | 4 | 1.74695 | 1.745838 | 0.111 | 1.325 |
| 2020-01-29 | 2020-01-30 | 5 | 1.670331 | 1.678188 | -0.786 | -1.952 |
| 2020-03-18 | 2020-03-19 | 6 | 1.606735 | 1.599715 | 0.702 | 1.623 |
| 2020-04-29 | 2020-04-30 | 7 | 1.565021 | 1.582832 | -1.781 | -1.832 |
| 2020-06-10 | 2020-06-11 | 8 | 1.512188 | 1.522875 | -1.069 | -0.673 |
| 2020-07-29 | 2020-07-30 | 9 | 1.48011 | 1.477377 | 0.273 |  |
| 2020-09-16 | 2020-09-17 | 10 | 1.435298 | 1.450641 | -1.534 |  |
| 2020-11-05 | 2020-11-06 | 11 | 1.415896 | 1.423918 | -0.802 |  |
| 2020-12-16 | 2020-12-17 | 12 | 1.385145 | 1.39721 | -1.207 |  |
| 2021-01-27 | 2021-01-28 | 13 | 1.373317 | 1.370513 | 0.28 |  |
| 2021-03-17 | 2021-03-18 | 14 | 1.362419 | 1.379364 | -1.694 |  |
| 2021-04-28 | 2021-04-29 | 15 | 1.527907 | 1.388216 | 13.969 |  |
| 2021-06-16 | 2021-06-17 | 16 | 1.486945 | 1.397069 | 8.988 |  |
| 2021-07-28 | 2021-07-29 | 17 | 1.445983 | 1.405924 | 4.006 |  |
| 2021-09-22 | 2021-09-23 | 18 | 1.40502 | 1.41126 | -0.624 |  |
| 2021-11-03 | 2021-11-04 | 19 | 1.40502 | 1.416593 | -1.157 |  |
| 2021-12-15 | 2021-12-16 | 20 | 1.40502 | 1.421923 | -1.69 |  |
| 2022-01-26 | 2022-01-27 | 21 | 1.40502 | 1.427249 | -2.223 |  |
| 2022-03-16 | 2022-03-17 | 22 | 1.40502 | 1.43257 | -2.755 |  |
| 2022-05-04 | 2022-05-05 | 23 | 1.40502 | 1.437886 | -3.287 |  |
| 2022-06-15 | 2022-06-16 | 24 | 1.40502 | 1.443199 | -3.818 |  |
| 2022-07-27 | 2022-07-28 | 25 | 1.40502 | 1.44851 | -4.349 |  |

## Stub

| curve | as_of | current_implied | replica_current_implied | stub_prior | stub_prior_source | anchor | spread | spread_median | spread_winsorised_mean | spread_obs | spread_estimator | spread_note | wirp_reach_meetings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | 2019-07-30 | 2.422468 | 2.4275 | 2.389667 | anchor + spread (D7) | 2.375 | 0.01466666666666668 | 0.015000000000000124 | 0.01466666666666668 | 60 | winsorised_mean |  | 16 |
| effr_ois | 2019-07-30 | 2.373141 | 2.4 | 2.389667 | anchor + spread (D7) | 2.375 | 0.01466666666666668 | 0.015000000000000124 | 0.01466666666666668 | 60 | winsorised_mean |  | 8 |
