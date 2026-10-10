# USD EFFR front end, 2020-03-16

Anchor (target_midpoint) in effect: 0.125. Policy spread (winsorised_mean, D7): -5.73bp (winsorised mean -5.73bp, median -7.00bp; 60 fixings, 3 turn days dropped, window 2019-12-12..2020-03-13) **Loader reported blocking problems in the window (see check_market_data.py).**

## Curve `effr_fut` (ff_fut)

Fit: 23 quotes (1 dropped, 13 excluded by metadata), 3 IRLS iterations (converged); 24 parcels to 2023-03-16, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 0.1514 (replica 0.1516; stub prior 0.0677 from anchor + spread (D7)). WIRP replica reaches 15 meetings on 23 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2020-04-29 | False | False | 0.105343 | -0.046089 | -0.1844 | -18.44 | 0.105 | 0.034 | 0.162677 | 3.768 | False | 0.005 | False |
| 2020-06-10 | False | False | 0.080786 | -0.070646 | -0.2826 | -9.82 | 0.0825 | -0.171 | 0.13812 | 1.312 | False | 0.004 | False |
| 2020-07-29 | False | False | 0.079961 | -0.071471 | -0.2859 | -0.33 | 0.08 | -0.004 | 0.137295 | 1.229 | False | 0.005 | False |
| 2020-09-16 | False | False | 0.079997 | -0.071436 | -0.2857 | 0.01 | 0.08 | -0.0 | 0.13733 | 1.233 | False | 0.005 | False |
| 2020-11-05 | False | False | 0.09208 | -0.059353 | -0.2374 | 4.83 | 0.092 | 0.008 | 0.149413 | 2.441 | False | 0.006 | False |
| 2020-12-16 | False | False | 0.097777 | -0.053656 | -0.2146 | 2.28 | 0.0982 | -0.042 | 0.15511 | 3.011 | False | 0.005 | False |
| 2021-01-27 | False | False | 0.115468 | -0.035964 | -0.1439 | 7.08 | 0.115 | 0.047 | 0.172802 | 4.78 | False | 0.005 | False |
| 2021-03-17 | False | False | 0.133888 | -0.017544 | -0.0702 | 7.37 | 0.137143 | -0.325 | 0.191221 | 6.622 | False | 0.006 | False |
| 2021-04-28 | False | False | 0.160143 | 0.008711 | 0.0348 | 10.5 | 0.16 | 0.014 | 0.217477 | 9.248 | False | 0.009 | False |
| 2021-06-16 | False | False | 0.175191 | 0.023758 | 0.095 | 6.02 | 0.181429 | -0.624 | 0.232524 | 10.752 | False | 0.014 | False |
| 2021-07-28 | False | False | 0.178092 | 0.026659 | 0.1066 | 1.16 | 0.18 | -0.191 | 0.235425 | 11.042 | False | 0.018 | False |
| 2021-09-22 | False | False | 0.19432 | 0.042887 | 0.1715 | 6.49 | 0.195 | -0.068 | 0.251653 | 12.665 | False | 0.022 | False |
| 2021-11-03 | False | False | 0.195381 | 0.043949 | 0.1758 | 0.42 | 0.195 | 0.038 | 0.252714 | 12.771 | False | 0.025 | False |
| 2021-12-15 | False | False | 0.21306 | 0.061628 | 0.2465 | 7.07 | 0.214375 | -0.131 | 0.270393 | 14.539 | False | 0.047 | False |
| 2022-01-26 | False | False | 0.133615 | -0.017818 | -0.0713 | -31.78 | 0.12525 | 0.836 | 0.190948 | 6.595 | False | 0.276 | False |
| 2022-03-16 | False | False | 0.133615 | -0.017818 | -0.0713 | 0.0 |  |  | 0.190948 | 6.595 | True | 0.276 | True |
| 2022-05-04 | False | False | 0.133615 | -0.017818 | -0.0713 | 0.0 |  |  | 0.190948 | 6.595 | True | 0.276 | True |
| 2022-06-15 | False | False | 0.133615 | -0.017818 | -0.0713 | 0.0 |  |  | 0.190948 | 6.595 | True | 0.276 | True |
| 2022-07-27 | False | False | 0.133615 | -0.017818 | -0.0713 | 0.0 |  |  | 0.190948 | 6.595 | True | 0.276 | True |
| 2022-09-21 | False | False | 0.133615 | -0.017818 | -0.0713 | 0.0 |  |  | 0.190948 | 6.595 | True | 0.276 | True |
| 2022-11-02 | False | False | 0.133615 | -0.017818 | -0.0713 | 0.0 |  |  | 0.190948 | 6.595 | True | 0.276 | True |
| 2022-12-14 | False | False | 0.133615 | -0.017818 | -0.0713 | 0.0 |  |  | 0.190948 | 6.595 | True | 0.276 | True |
| 2023-02-01 | False | False | 0.133615 | -0.017818 | -0.0713 | 0.0 |  |  | 0.190948 | 6.595 | True | 0.276 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | dropped | 1 | -4.49 | 4.49 | 4.49 |
| effr_fut | ff_fut | used | 22 | 0.012 | 0.101 | 0.283 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

| curve | instrument | contract | ticker | status | reason | residual_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2020-04 | FFJ20 Comdty | dropped | leave-one-out residual -4.49bp, over 6.0 x its effective noise 0.50bp (alone pinned a parcel) | -4.49 |
| effr_fut | ff_fut | 2022-02 | FFG22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-03 | FFH22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-04 | FFJ22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-05 | FFK22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-06 | FFM22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-07 | FFN22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-08 | FFQ22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-09 | FFU22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-10 | FFV22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-11 | FFX22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-12 | FFZ22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2023-01 | FFF23 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2023-02 | FFG23 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2020-03 | FFH20 Comdty | 0.655 | 0.007 | 4.216 | 0.998 |
| effr_fut | ff_fut | 2020-05 | FFK20 Comdty | 0.105 | -0.034 | -0.5 | 0.931 |
| effr_fut | ff_fut | 2021-05 | FFK21 Comdty | 0.16 | -0.014 | -0.361 | 0.96 |
| effr_fut | ff_fut | 2021-07 | FFN21 Comdty | 0.175 | -0.047 | -0.615 | 0.923 |
| effr_fut | ff_fut | 2021-10 | FFV21 Comdty | 0.195 | 0.068 | 1.493 | 0.954 |
| effr_fut | ff_fut | 2021-11 | FFX21 Comdty | 0.195 | -0.027 | -1.284 | 0.979 |
| effr_fut | ff_fut | 2021-12 | FFZ21 Comdty | 0.205 | 0.049 | 0.745 | 0.934 |
| effr_fut | ff_fut | 2022-01 | FFF22 Comdty | 0.2 | -0.025 | -1.425 | 0.983 |

### Stale and outside-listing inputs

| curve | flag | instrument | contract | status | detail |
| --- | --- | --- | --- | --- | --- |
| effr_fut | outside_listing | ff_fut | 2022-11 | excluded | loader: FFX22 Comdty|PX_LAST quoted from 2019-11-27, modelled first listing 2019-12-02 |
| effr_fut | outside_listing | ff_fut | 2022-12 | excluded | loader: FFZ22 Comdty|PX_LAST quoted from 2019-12-31, modelled first listing after 2019-12-31 |
| effr_fut | outside_listing | ff_fut | 2023-01 | excluded | loader: FFF23 Comdty|PX_LAST quoted from 2020-01-31, modelled first listing 2020-02-03 |
| effr_fut | outside_listing | ff_fut | 2023-02 | excluded | loader: FFG23 Comdty|PX_LAST quoted from 2020-02-28, modelled first listing 2020-03-02 |

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2020-03-16 | 1.0 | False | 0.01 | 0.151432 |  | 0.151563 | -0.013 |
| 2020-04-29 | 2020-04-30 | 1.0 | False | 0.005 | 0.105343 | -4.609 | 0.105 | 0.034 |
| 2020-06-10 | 2020-06-11 | 1.0 | False | 0.004 | 0.080786 | -2.456 | 0.0825 | -0.171 |
| 2020-07-29 | 2020-07-30 | 1.0 | False | 0.005 | 0.079961 | -0.083 | 0.08 | -0.004 |
| 2020-09-16 | 2020-09-17 | 1.0 | False | 0.005 | 0.079997 | 0.004 | 0.08 | -0.0 |
| 2020-11-05 | 2020-11-06 | 1.0 | False | 0.006 | 0.09208 | 1.208 | 0.092 | 0.008 |
| 2020-12-16 | 2020-12-17 | 1.0 | False | 0.005 | 0.097777 | 0.57 | 0.0982 | -0.042 |
| 2021-01-27 | 2021-01-28 | 1.0 | False | 0.005 | 0.115468 | 1.769 | 0.115 | 0.047 |
| 2021-03-17 | 2021-03-18 | 1.0 | False | 0.006 | 0.133888 | 1.842 | 0.137143 | -0.325 |
| 2021-04-28 | 2021-04-29 | 1.0 | False | 0.009 | 0.160143 | 2.626 | 0.16 | 0.014 |
| 2021-06-16 | 2021-06-17 | 1.0 | False | 0.014 | 0.175191 | 1.505 | 0.181429 | -0.624 |
| 2021-07-28 | 2021-07-29 | 1.0 | False | 0.018 | 0.178092 | 0.29 | 0.18 | -0.191 |
| 2021-09-22 | 2021-09-23 | 1.0 | False | 0.022 | 0.19432 | 1.623 | 0.195 | -0.068 |
| 2021-11-03 | 2021-11-04 | 1.0 | False | 0.025 | 0.195381 | 0.106 | 0.195 | 0.038 |
| 2021-12-15 | 2021-12-16 | 1.0 | False | 0.047 | 0.21306 | 1.768 | 0.214375 | -0.131 |
| 2022-01-26 | 2022-01-27 | 1.0 | False | 0.276 | 0.133615 | -7.945 | 0.12525 | 0.836 |
| 2022-03-16 | 2022-03-17 | 0.0 | True | 0.276 | 0.133615 | 0.0 |  |  |
| 2022-05-04 | 2022-05-05 | 0.0 | True | 0.276 | 0.133615 | 0.0 |  |  |
| 2022-06-15 | 2022-06-16 | 0.0 | True | 0.276 | 0.133615 | 0.0 |  |  |
| 2022-07-27 | 2022-07-28 | 0.0 | True | 0.276 | 0.133615 | 0.0 |  |  |
| 2022-09-21 | 2022-09-22 | 0.0 | True | 0.276 | 0.133615 | 0.0 |  |  |
| 2022-11-02 | 2022-11-03 | 0.0 | True | 0.276 | 0.133615 | 0.0 |  |  |
| 2022-12-14 | 2022-12-15 | 0.0 | True | 0.276 | 0.133615 | 0.0 |  |  |
| 2023-02-01 | 2023-02-02 | 0.0 | True | 0.276 | 0.133615 | 0.0 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_fut | ff_fut 2020-03 | 0.6550000000000011 | used |
| effr_fut | ff_fut 2020-04 | 0.10500000000000398 | used |
| effr_fut | ff_fut 2020-05 | 0.10500000000000398 | used |
| effr_fut | ff_fut 2020-06 | 0.09000000000000341 | used |
| effr_fut | ff_fut 2020-07 | 0.0799999999999983 | used |
| effr_fut | ff_fut 2020-08 | 0.0799999999999983 | used |
| effr_fut | ff_fut 2020-09 | 0.0799999999999983 | used |
| effr_fut | ff_fut 2020-10 | 0.0799999999999983 | used |
| effr_fut | ff_fut 2020-11 | 0.09000000000000341 | used |
| effr_fut | ff_fut 2020-12 | 0.09499999999999886 | used |
| effr_fut | ff_fut 2021-01 | 0.09999999999999432 | used |
| effr_fut | ff_fut 2021-02 | 0.11499999999999488 | used |
| effr_fut | ff_fut 2021-03 | 0.125 | used |
| effr_fut | ff_fut 2021-04 | 0.13500000000000512 | used |
| effr_fut | ff_fut 2021-05 | 0.1599999999999966 | used |
| effr_fut | ff_fut 2021-06 | 0.1700000000000017 | used |
| effr_fut | ff_fut 2021-07 | 0.17499999999999716 | used |
| effr_fut | ff_fut 2021-08 | 0.18000000000000682 | used |
| effr_fut | ff_fut 2021-09 | 0.18000000000000682 | used |
| effr_fut | ff_fut 2021-10 | 0.19499999999999318 | used |
| effr_fut | ff_fut 2021-11 | 0.19499999999999318 | used |
| effr_fut | ff_fut 2021-12 | 0.2049999999999983 | used |
| effr_fut | ff_fut 2022-01 | 0.20000000000000284 | used |

Replica notes: ff_fut 2020-05: no new parcel; re-solved parcel 1 (2020-04-29); ff_fut 2020-08: no new parcel; re-solved parcel 3 (2020-07-29); ff_fut 2020-10: no new parcel; re-solved parcel 4 (2020-09-16); ff_fut 2021-02: no new parcel; re-solved parcel 7 (2021-01-27); ff_fut 2021-05: no new parcel; re-solved parcel 9 (2021-04-28); ff_fut 2021-08: no new parcel; re-solved parcel 11 (2021-07-28); ff_fut 2021-10: no new parcel; re-solved parcel 12 (2021-09-22)

## Curve `effr_ois` (ois_effr)

Fit: 18 quotes (0 dropped, 0 excluded by metadata), 12 IRLS iterations (converged); 25 parcels to 2023-03-29, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 0.1186 (replica 0.1150; stub prior 0.0677 from anchor + spread (D7)). WIRP replica reaches 7 meetings on 13 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2020-04-29 | False | False | 0.083715 | -0.034902 | -0.1396 | -13.96 | 0.086177 | -0.246 | 0.141048 | 1.605 | False | 0.011 | False |
| 2020-06-10 | False | False | 0.084591 | -0.034026 | -0.1361 | 0.35 | 0.085587 | -0.1 | 0.141924 | 1.692 | False | 0.019 | False |
| 2020-07-29 | False | False | 0.063886 | -0.054731 | -0.2189 | -8.28 | 0.065007 | -0.112 | 0.121219 | -0.378 | False | 0.025 | False |
| 2020-09-16 | False | False | 0.075121 | -0.043495 | -0.174 | 4.49 | 0.072722 | 0.24 | 0.132454 | 0.745 | False | 0.034 | False |
| 2020-11-05 | False | False | 0.074652 | -0.043965 | -0.1759 | -0.19 | 0.076964 | -0.231 | 0.131985 | 0.698 | False | 0.05 | False |
| 2020-12-16 | False | False | 0.113716 | -0.0049 | -0.0196 | 15.63 | 0.110832 | 0.288 | 0.17105 | 4.605 | False | 0.056 | False |
| 2021-01-27 | False | False | 0.080754 | -0.037863 | -0.1515 | -13.18 | 0.081358 | -0.06 | 0.138087 | 1.309 | False | 0.054 | False |
| 2021-03-17 | False | False | 0.084076 | -0.034541 | -0.1382 | 1.33 |  |  | 0.141409 | 1.641 | True | 0.55 | True |
| 2021-04-28 | False | False | 0.109589 | -0.009028 | -0.0361 | 10.21 |  |  | 0.166922 | 4.192 | True | 0.201 | True |
| 2021-06-16 | False | False | 0.135107 | 0.01649 | 0.066 | 10.21 |  |  | 0.19244 | 6.744 | True | 0.152 | True |
| 2021-07-28 | False | False | 0.160629 | 0.042013 | 0.1681 | 10.21 |  |  | 0.217963 | 9.296 | True | 0.501 | True |
| 2021-09-22 | False | False | 0.195853 | 0.077236 | 0.3089 | 14.09 |  |  | 0.253186 | 12.819 | True | 0.304 | True |
| 2021-11-03 | False | False | 0.231071 | 0.112454 | 0.4498 | 14.09 |  |  | 0.288404 | 16.34 | True | 0.108 | True |
| 2021-12-15 | False | False | 0.26628 | 0.147664 | 0.5907 | 14.08 |  |  | 0.323613 | 19.861 | True | 0.098 | True |
| 2022-01-26 | False | False | 0.301481 | 0.182864 | 0.7315 | 14.08 |  |  | 0.358814 | 23.381 | True | 0.294 | True |
| 2022-03-16 | False | False | 0.336675 | 0.218059 | 0.8722 | 14.08 |  |  | 0.394009 | 26.901 | True | 0.492 | True |
| 2022-05-04 | False | False | 0.346801 | 0.228185 | 0.9127 | 4.05 |  |  | 0.404135 | 27.913 | True | 0.353 | True |
| 2022-06-15 | False | False | 0.356924 | 0.238308 | 0.9532 | 4.05 |  |  | 0.414258 | 28.926 | True | 0.214 | True |
| 2022-07-27 | False | False | 0.367043 | 0.248426 | 0.9937 | 4.05 |  |  | 0.424376 | 29.938 | True | 0.078 | True |
| 2022-09-21 | False | False | 0.377155 | 0.258538 | 1.0342 | 4.04 |  |  | 0.434488 | 30.949 | True | 0.076 | True |
| 2022-11-02 | False | False | 0.387261 | 0.268644 | 1.0746 | 4.04 |  |  | 0.444594 | 31.959 | True | 0.212 | True |
| 2022-12-14 | False | False | 0.397361 | 0.278745 | 1.115 | 4.04 |  |  | 0.454695 | 32.969 | True | 0.353 | True |
| 2023-02-01 | False | False | 0.407459 | 0.288843 | 1.1554 | 4.04 |  |  | 0.464793 | 33.979 | True | 0.495 | True |
| 2023-03-22 | False | False | 0.407459 | 0.288843 | 1.1554 | 0.0 |  |  | 0.464793 | 33.979 | True | 0.495 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | used | 18 | -0.074 | 0.536 | 2.062 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

_none_

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | 9M | USSOI Curncy | 0.083 | -0.002 | -0.023 | 0.928 |
| effr_ois | ois_effr | 18M | USSO1F Curncy | 0.099 | -0.001 | -0.318 | 0.998 |
| effr_ois | ois_effr | 2Y | USSO2 Curncy | 0.136 | 0.0 | 0.159 | 0.999 |
| effr_ois | ois_effr | 3Y | USSO3 Curncy | 0.215 | 0.0 | 1.377 | 1.0 |

### Stale and outside-listing inputs

_none_

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2020-03-16 | 1.0 | False | 0.003 | 0.118616 |  | 0.114994 | 0.362 |
| 2020-04-29 | 2020-04-30 | 1.0 | False | 0.011 | 0.083715 | -3.49 | 0.086177 | -0.246 |
| 2020-06-10 | 2020-06-11 | 1.0 | False | 0.019 | 0.084591 | 0.088 | 0.085587 | -0.1 |
| 2020-07-29 | 2020-07-30 | 1.0 | False | 0.025 | 0.063886 | -2.07 | 0.065007 | -0.112 |
| 2020-09-16 | 2020-09-17 | 1.0 | False | 0.034 | 0.075121 | 1.124 | 0.072722 | 0.24 |
| 2020-11-05 | 2020-11-06 | 1.0 | False | 0.05 | 0.074652 | -0.047 | 0.076964 | -0.231 |
| 2020-12-16 | 2020-12-17 | 1.0 | False | 0.056 | 0.113716 | 3.906 | 0.110832 | 0.288 |
| 2021-01-27 | 2021-01-28 | 1.0 | False | 0.054 | 0.080754 | -3.296 | 0.081358 | -0.06 |
| 2021-03-17 | 2021-03-18 | 0.202 | True | 0.55 | 0.084076 | 0.332 |  |  |
| 2021-04-28 | 2021-04-29 | 0.2749 | True | 0.201 | 0.109589 | 2.551 |  |  |
| 2021-06-16 | 2021-06-17 | 0.202 | True | 0.152 | 0.135107 | 2.552 |  |  |
| 2021-07-28 | 2021-07-29 | 0.322 | True | 0.501 | 0.160629 | 2.552 |  |  |
| 2021-09-22 | 2021-09-23 | 0.2291 | True | 0.304 | 0.195853 | 3.522 |  |  |
| 2021-11-03 | 2021-11-04 | 0.2291 | True | 0.108 | 0.231071 | 3.522 |  |  |
| 2021-12-15 | 2021-12-16 | 0.2291 | True | 0.098 | 0.26628 | 3.521 |  |  |
| 2022-01-26 | 2022-01-27 | 0.3118 | True | 0.294 | 0.301481 | 3.52 |  |  |
| 2022-03-16 | 2022-03-17 | 0.1355 | True | 0.492 | 0.336675 | 3.519 |  |  |
| 2022-05-04 | 2022-05-05 | 0.1037 | True | 0.353 | 0.346801 | 1.013 |  |  |
| 2022-06-15 | 2022-06-16 | 0.1037 | True | 0.214 | 0.356924 | 1.012 |  |  |
| 2022-07-27 | 2022-07-28 | 0.1843 | True | 0.078 | 0.367043 | 1.012 |  |  |
| 2022-09-21 | 2022-09-22 | 0.1037 | True | 0.076 | 0.377155 | 1.011 |  |  |
| 2022-11-02 | 2022-11-03 | 0.1037 | True | 0.212 | 0.387261 | 1.011 |  |  |
| 2022-12-14 | 2022-12-15 | 0.1411 | True | 0.353 | 0.397361 | 1.01 |  |  |
| 2023-02-01 | 2023-02-02 | 0.1244 | True | 0.495 | 0.407459 | 1.01 |  |  |
| 2023-03-22 | 2023-03-23 | 0.0 | True | 0.495 | 0.407459 | 0.0 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_ois | ois_effr 1W | 0.126 | used |
| effr_ois | ois_effr 1M | 0.115 | used |
| effr_ois | ois_effr 2M | 0.1065 | used |
| effr_ois | ois_effr 3M | 0.1015 | used |
| effr_ois | ois_effr 4M | 0.096 | used |
| effr_ois | ois_effr 5M | 0.091 | used |
| effr_ois | ois_effr 6M | 0.087 | used |
| effr_ois | ois_effr 7M | 0.085 | used |
| effr_ois | ois_effr 8M | 0.084 | used |
| effr_ois | ois_effr 9M | 0.083 | used |
| effr_ois | ois_effr 10M | 0.086 | used |
| effr_ois | ois_effr 11M | 0.087 | used |
| effr_ois | ois_effr 1Y | 0.086 | used |

Replica notes: ois_effr 1M: no new parcel; re-solved parcel 0 (stub); ois_effr 4M: no new parcel; re-solved parcel 2 (2020-06-10); ois_effr 6M: no new parcel; re-solved parcel 3 (2020-07-29); ois_effr 9M: no new parcel; re-solved parcel 5 (2020-11-05); ois_effr 1Y: no new parcel; re-solved parcel 7 (2021-01-27)

## FF / OIS basis (bp, fit and replica)

| decision_date | effective_date | parcel | effr_fut_fit | effr_ois_fit | basis_fit_bp | basis_replica_bp |
| --- | --- | --- | --- | --- | --- | --- |
| None | None | stub | 0.1514323951599591 | 0.11861636339806264 | 3.282 | 3.657 |
| 2020-04-29 | 2020-04-30 | 1 | 0.105343 | 0.083715 | 2.163 | 1.882 |
| 2020-06-10 | 2020-06-11 | 2 | 0.080786 | 0.084591 | -0.38 | -0.309 |
| 2020-07-29 | 2020-07-30 | 3 | 0.079961 | 0.063886 | 1.608 | 1.499 |
| 2020-09-16 | 2020-09-17 | 4 | 0.079997 | 0.075121 | 0.488 | 0.728 |
| 2020-11-05 | 2020-11-06 | 5 | 0.09208 | 0.074652 | 1.743 | 1.504 |
| 2020-12-16 | 2020-12-17 | 6 | 0.097777 | 0.113716 | -1.594 | -1.263 |
| 2021-01-27 | 2021-01-28 | 7 | 0.115468 | 0.080754 | 3.471 | 3.364 |
| 2021-03-17 | 2021-03-18 | 8 | 0.133888 | 0.084076 | 4.981 |  |
| 2021-04-28 | 2021-04-29 | 9 | 0.160143 | 0.109589 | 5.055 |  |
| 2021-06-16 | 2021-06-17 | 10 | 0.175191 | 0.135107 | 4.008 |  |
| 2021-07-28 | 2021-07-29 | 11 | 0.178092 | 0.160629 | 1.746 |  |
| 2021-09-22 | 2021-09-23 | 12 | 0.19432 | 0.195853 | -0.153 |  |
| 2021-11-03 | 2021-11-04 | 13 | 0.195381 | 0.231071 | -3.569 |  |
| 2021-12-15 | 2021-12-16 | 14 | 0.21306 | 0.26628 | -5.322 |  |
| 2022-01-26 | 2022-01-27 | 15 | 0.133615 | 0.301481 | -16.787 |  |
| 2022-03-16 | 2022-03-17 | 16 | 0.133615 | 0.336675 | -20.306 |  |
| 2022-05-04 | 2022-05-05 | 17 | 0.133615 | 0.346801 | -21.319 |  |
| 2022-06-15 | 2022-06-16 | 18 | 0.133615 | 0.356924 | -22.331 |  |
| 2022-07-27 | 2022-07-28 | 19 | 0.133615 | 0.367043 | -23.343 |  |
| 2022-09-21 | 2022-09-22 | 20 | 0.133615 | 0.377155 | -24.354 |  |
| 2022-11-02 | 2022-11-03 | 21 | 0.133615 | 0.387261 | -25.365 |  |
| 2022-12-14 | 2022-12-15 | 22 | 0.133615 | 0.397361 | -26.375 |  |
| 2023-02-01 | 2023-02-02 | 23 | 0.133615 | 0.407459 | -27.384 |  |

## Stub

| curve | as_of | current_implied | replica_current_implied | stub_prior | stub_prior_source | anchor | spread | spread_median | spread_winsorised_mean | spread_obs | spread_estimator | spread_note | wirp_reach_meetings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | 2020-03-16 | 0.151432 | 0.151563 | 0.067667 | anchor + spread (D7) | 0.125 | -0.05733333333333328 | -0.06999999999999995 | -0.05733333333333328 | 60 | winsorised_mean |  | 15 |
| effr_ois | 2020-03-16 | 0.118616 | 0.114994 | 0.067667 | anchor + spread (D7) | 0.125 | -0.05733333333333328 | -0.06999999999999995 | -0.05733333333333328 | 60 | winsorised_mean |  | 7 |
