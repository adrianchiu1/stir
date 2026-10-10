# USD EFFR front end, 2018-09-25

Anchor (target_midpoint) in effect: 1.875. Policy spread (winsorised_mean, D7): 3.95bp (winsorised mean 3.95bp, median 3.50bp; 60 fixings, 3 turn days dropped, window 2018-06-26..2018-09-24) **Loader reported blocking problems in the window (see check_market_data.py).**

## Curve `effr_fut` (ff_fut)

Fit: 27 quotes (0 dropped, 9 excluded by metadata), 3 IRLS iterations (converged); 26 parcels to 2021-09-25, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 1.9438 (replica 1.9450; stub prior 1.9145 from anchor + spread (D7)). WIRP replica reaches 18 meetings on 27 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2018-09-26 | False | False | 2.174944 | 0.231167 | 0.9247 | 92.47 | 2.175 | -0.006 | 2.135444 | 26.044 | False | 0.005 | False |
| 2018-11-08 | False | False | 2.182157 | 0.23838 | 0.9535 | 2.89 | 2.181818 | 0.034 | 2.142657 | 26.766 | False | 0.006 | False |
| 2018-12-19 | False | False | 2.369632 | 0.425855 | 1.7034 | 74.99 | 2.370871 | -0.124 | 2.330132 | 45.513 | False | 0.005 | False |
| 2019-01-30 | False | False | 2.384259 | 0.440481 | 1.7619 | 5.85 | 2.385 | -0.074 | 2.344759 | 46.976 | False | 0.004 | False |
| 2019-03-20 | False | False | 2.544587 | 0.600809 | 2.4032 | 64.13 | 2.545 | -0.041 | 2.505087 | 63.009 | False | 0.005 | False |
| 2019-05-01 | False | False | 2.58126 | 0.637482 | 2.5499 | 14.67 | 2.581167 | 0.009 | 2.54176 | 66.676 | False | 0.005 | False |
| 2019-06-19 | False | False | 2.700039 | 0.756262 | 3.025 | 47.51 | 2.7 | 0.004 | 2.660539 | 78.554 | False | 0.005 | False |
| 2019-07-31 | False | False | 2.724479 | 0.780702 | 3.1228 | 9.78 | 2.725 | -0.052 | 2.684979 | 80.998 | False | 0.005 | False |
| 2019-09-18 | False | False | 2.794286 | 0.850508 | 3.402 | 27.92 | 2.7875 | 0.679 | 2.754786 | 87.979 | False | 0.005 | False |
| 2019-10-30 | False | False | 2.804603 | 0.860826 | 3.4433 | 4.13 | 2.805 | -0.04 | 2.765103 | 89.01 | False | 0.006 | False |
| 2019-12-11 | False | False | 2.849441 | 0.905664 | 3.6227 | 17.94 | 2.84375 | 0.569 | 2.809941 | 93.494 | False | 0.005 | False |
| 2020-01-29 | False | False | 2.849866 | 0.906089 | 3.6244 | 0.17 | 2.85 | -0.013 | 2.810366 | 93.537 | False | 0.008 | False |
| 2020-03-18 | False | False | 2.868955 | 0.925178 | 3.7007 | 7.64 | 2.861923 | 0.703 | 2.829455 | 95.445 | False | 0.019 | False |
| 2020-04-29 | False | False | 2.869662 | 0.925884 | 3.7035 | 0.28 | 2.87 | -0.034 | 2.830162 | 95.516 | False | 0.022 | False |
| 2020-06-10 | False | False | 2.864367 | 0.92059 | 3.6824 | -2.12 | 2.8625 | 0.187 | 2.824867 | 94.987 | False | 0.02 | False |
| 2020-07-29 | False | False | 2.861695 | 0.917918 | 3.6717 | -1.07 | 2.86 | 0.17 | 2.822195 | 94.72 | False | 0.02 | False |
| 2020-09-16 | False | False | 2.851445 | 0.907668 | 3.6307 | -4.1 | 2.85 | 0.145 | 2.811945 | 93.695 | False | 0.021 | False |
| 2020-11-05 | False | False | 2.849712 | 0.905935 | 3.6237 | -0.69 | 2.85 | -0.029 | 2.810212 | 93.521 | False | 0.027 | False |
| 2020-12-16 | False | False | 2.849712 | 0.905935 | 3.6237 | 0.0 |  |  | 2.810212 | 93.521 | True | 0.028 | True |
| 2021-01-27 | False | False | 2.849712 | 0.905935 | 3.6237 | 0.0 |  |  | 2.810212 | 93.521 | True | 0.028 | True |
| 2021-03-17 | False | False | 2.849712 | 0.905935 | 3.6237 | 0.0 |  |  | 2.810212 | 93.521 | True | 0.028 | True |
| 2021-04-28 | False | False | 2.849712 | 0.905935 | 3.6237 | 0.0 |  |  | 2.810212 | 93.521 | True | 0.029 | True |
| 2021-06-16 | False | False | 2.849712 | 0.905935 | 3.6237 | 0.0 |  |  | 2.810212 | 93.521 | True | 0.029 | True |
| 2021-07-28 | False | False | 2.849712 | 0.905935 | 3.6237 | 0.0 |  |  | 2.810212 | 93.521 | True | 0.03 | True |
| 2021-09-22 | False | False | 2.849712 | 0.905935 | 3.6237 | 0.0 |  |  | 2.810212 | 93.521 | True | 0.03 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | used | 27 | -0.021 | 0.132 | 0.353 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

| curve | instrument | contract | ticker | status | reason | residual_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2020-12 | FFZ20 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-01 | FFF21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-02 | FFG21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-03 | FFH21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-04 | FFJ21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-05 | FFK21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-06 | FFM21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-07 | FFN21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-08 | FFQ21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2018-09 | FFU18 Comdty | 1.955 | 0.009 | 0.102 | 0.913 |
| effr_fut | ff_fut | 2018-10 | FFV18 Comdty | 2.175 | 0.006 | 0.202 | 0.972 |
| effr_fut | ff_fut | 2019-01 | FFF19 Comdty | 2.37 | -0.01 | -0.124 | 0.916 |
| effr_fut | ff_fut | 2019-04 | FFJ19 Comdty | 2.545 | 0.041 | 0.505 | 0.918 |
| effr_fut | ff_fut | 2019-07 | FFN19 Comdty | 2.7 | -0.004 | -0.065 | 0.939 |
| effr_fut | ff_fut | 2019-10 | FFV19 Comdty | 2.795 | 0.038 | 0.697 | 0.945 |
| effr_fut | ff_fut | 2019-11 | FFX19 Comdty | 2.805 | 0.04 | 1.084 | 0.963 |
| effr_fut | ff_fut | 2020-01 | FFF20 Comdty | 2.85 | 0.053 | 0.588 | 0.91 |
| effr_fut | ff_fut | 2020-02 | FFG20 Comdty | 2.85 | 0.013 | 0.336 | 0.96 |
| effr_fut | ff_fut | 2020-05 | FFK20 Comdty | 2.87 | 0.034 | 0.485 | 0.93 |
| effr_fut | ff_fut | 2020-11 | FFX20 Comdty | 2.85 | -0.0 | -0.145 | 0.999 |

### Stale and outside-listing inputs

| curve | flag | instrument | contract | status | detail |
| --- | --- | --- | --- | --- | --- |
| effr_fut | outside_listing | ff_fut | 2021-05 | excluded | loader: FFK21 Comdty|PX_LAST quoted from 2018-05-31, modelled first listing 2018-06-01 |
| effr_fut | outside_listing | ff_fut | 2021-06 | excluded | loader: FFM21 Comdty|PX_LAST quoted from 2018-06-29, modelled first listing 2018-07-02 |
| effr_fut | outside_listing | ff_fut | 2021-07 | excluded | loader: FFN21 Comdty|PX_LAST quoted from 2018-07-31, modelled first listing 2018-08-01 |
| effr_fut | outside_listing | ff_fut | 2021-08 | excluded | loader: FFQ21 Comdty|PX_LAST quoted from 2018-08-31, modelled first listing 2018-09-04 |

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2018-09-25 | 1.0 | False | 0.072 | 1.943777 |  | 1.945 | -0.122 |
| 2018-09-26 | 2018-09-27 | 1.0 | False | 0.005 | 2.174944 | 23.117 | 2.175 | -0.006 |
| 2018-11-08 | 2018-11-09 | 1.0 | False | 0.006 | 2.182157 | 0.721 | 2.181818 | 0.034 |
| 2018-12-19 | 2018-12-20 | 1.0 | False | 0.005 | 2.369632 | 18.748 | 2.370871 | -0.124 |
| 2019-01-30 | 2019-01-31 | 1.0 | False | 0.004 | 2.384259 | 1.463 | 2.385 | -0.074 |
| 2019-03-20 | 2019-03-21 | 1.0 | False | 0.005 | 2.544587 | 16.033 | 2.545 | -0.041 |
| 2019-05-01 | 2019-05-02 | 1.0 | False | 0.005 | 2.58126 | 3.667 | 2.581167 | 0.009 |
| 2019-06-19 | 2019-06-20 | 1.0 | False | 0.005 | 2.700039 | 11.878 | 2.7 | 0.004 |
| 2019-07-31 | 2019-08-01 | 1.0 | False | 0.005 | 2.724479 | 2.444 | 2.725 | -0.052 |
| 2019-09-18 | 2019-09-19 | 1.0 | False | 0.005 | 2.794286 | 6.981 | 2.7875 | 0.679 |
| 2019-10-30 | 2019-10-31 | 1.0 | False | 0.006 | 2.804603 | 1.032 | 2.805 | -0.04 |
| 2019-12-11 | 2019-12-12 | 1.0 | False | 0.005 | 2.849441 | 4.484 | 2.84375 | 0.569 |
| 2020-01-29 | 2020-01-30 | 1.0 | False | 0.008 | 2.849866 | 0.042 | 2.85 | -0.013 |
| 2020-03-18 | 2020-03-19 | 1.0 | False | 0.019 | 2.868955 | 1.909 | 2.861923 | 0.703 |
| 2020-04-29 | 2020-04-30 | 1.0 | False | 0.022 | 2.869662 | 0.071 | 2.87 | -0.034 |
| 2020-06-10 | 2020-06-11 | 1.0 | False | 0.02 | 2.864367 | -0.529 | 2.8625 | 0.187 |
| 2020-07-29 | 2020-07-30 | 1.0 | False | 0.02 | 2.861695 | -0.267 | 2.86 | 0.17 |
| 2020-09-16 | 2020-09-17 | 1.0 | False | 0.021 | 2.851445 | -1.025 | 2.85 | 0.145 |
| 2020-11-05 | 2020-11-06 | 1.0 | False | 0.027 | 2.849712 | -0.173 | 2.85 | -0.029 |
| 2020-12-16 | 2020-12-17 | 0.0 | True | 0.028 | 2.849712 | 0.0 |  |  |
| 2021-01-27 | 2021-01-28 | 0.0 | True | 0.028 | 2.849712 | 0.0 |  |  |
| 2021-03-17 | 2021-03-18 | 0.0 | True | 0.028 | 2.849712 | 0.0 |  |  |
| 2021-04-28 | 2021-04-29 | 0.0 | True | 0.029 | 2.849712 | 0.0 |  |  |
| 2021-06-16 | 2021-06-17 | 0.0 | True | 0.029 | 2.849712 | 0.0 |  |  |
| 2021-07-28 | 2021-07-29 | 0.0 | True | 0.03 | 2.849712 | 0.0 |  |  |
| 2021-09-22 | 2021-09-23 | 0.0 | True | 0.03 | 2.849712 | 0.0 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_fut | ff_fut 2018-09 | 1.9549999999999983 | used |
| effr_fut | ff_fut 2018-10 | 2.174999999999997 | used |
| effr_fut | ff_fut 2018-11 | 2.180000000000007 | used |
| effr_fut | ff_fut 2018-12 | 2.2549999999999955 | used |
| effr_fut | ff_fut 2019-01 | 2.3700000000000045 | used |
| effr_fut | ff_fut 2019-02 | 2.385000000000005 | used |
| effr_fut | ff_fut 2019-03 | 2.4399999999999977 | used |
| effr_fut | ff_fut 2019-04 | 2.5450000000000017 | used |
| effr_fut | ff_fut 2019-05 | 2.5799999999999983 | used |
| effr_fut | ff_fut 2019-06 | 2.625 | used |
| effr_fut | ff_fut 2019-07 | 2.700000000000003 | used |
| effr_fut | ff_fut 2019-08 | 2.7249999999999943 | used |
| effr_fut | ff_fut 2019-09 | 2.75 | used |
| effr_fut | ff_fut 2019-10 | 2.7950000000000017 | used |
| effr_fut | ff_fut 2019-11 | 2.805000000000007 | used |
| effr_fut | ff_fut 2019-12 | 2.8299999999999983 | used |
| effr_fut | ff_fut 2020-01 | 2.8499999999999943 | used |
| effr_fut | ff_fut 2020-02 | 2.8499999999999943 | used |
| effr_fut | ff_fut 2020-03 | 2.855000000000004 | used |
| effr_fut | ff_fut 2020-04 | 2.8700000000000045 | used |
| effr_fut | ff_fut 2020-05 | 2.8700000000000045 | used |
| effr_fut | ff_fut 2020-06 | 2.864999999999995 | used |
| effr_fut | ff_fut 2020-07 | 2.864999999999995 | used |
| effr_fut | ff_fut 2020-08 | 2.8599999999999994 | used |
| effr_fut | ff_fut 2020-09 | 2.8599999999999994 | used |
| effr_fut | ff_fut 2020-10 | 2.8499999999999943 | used |
| effr_fut | ff_fut 2020-11 | 2.8499999999999943 | used |

Replica notes: ff_fut 2019-02: no new parcel; re-solved parcel 4 (2019-01-30); ff_fut 2019-04: no new parcel; re-solved parcel 5 (2019-03-20); ff_fut 2019-07: no new parcel; re-solved parcel 7 (2019-06-19); ff_fut 2019-11: no new parcel; re-solved parcel 10 (2019-10-30); ff_fut 2020-02: no new parcel; re-solved parcel 12 (2020-01-29); ff_fut 2020-05: no new parcel; re-solved parcel 14 (2020-04-29); ff_fut 2020-08: no new parcel; re-solved parcel 16 (2020-07-29); ff_fut 2020-10: no new parcel; re-solved parcel 17 (2020-09-16)

## Curve `effr_ois` (ois_effr)

Fit: 18 quotes (0 dropped, 0 excluded by metadata), 3 IRLS iterations (converged); 26 parcels to 2021-10-06, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 1.9296 (replica 1.9300; stub prior 1.9145 from anchor + spread (D7)). WIRP replica reaches 8 meetings on 13 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2018-09-26 | False | False | 2.170471 | 0.240914 | 0.9637 | 96.37 | 2.174038 | -0.357 | 2.130971 | 25.597 | False | 0.002 | False |
| 2018-11-08 | False | False | 2.181326 | 0.251769 | 1.0071 | 4.34 | 2.174349 | 0.698 | 2.141826 | 26.683 | False | 0.011 | False |
| 2018-12-19 | False | False | 2.366737 | 0.43718 | 1.7487 | 74.16 | 2.370954 | -0.422 | 2.327237 | 45.224 | False | 0.02 | False |
| 2019-01-30 | False | False | 2.38478 | 0.455223 | 1.8209 | 7.22 | 2.381086 | 0.369 | 2.34528 | 47.028 | False | 0.024 | False |
| 2019-03-20 | False | False | 2.537994 | 0.608437 | 2.4337 | 61.29 | 2.540757 | -0.276 | 2.498494 | 62.349 | False | 0.036 | False |
| 2019-05-01 | False | False | 2.582595 | 0.653038 | 2.6122 | 17.84 | 2.585686 | -0.309 | 2.543095 | 66.809 | False | 0.039 | False |
| 2019-06-19 | False | False | 2.693448 | 0.763891 | 3.0556 | 44.34 | 2.691376 | 0.207 | 2.653948 | 77.895 | False | 0.054 | False |
| 2019-07-31 | False | False | 2.730723 | 0.801165 | 3.2047 | 14.91 | 2.742889 | -1.217 | 2.691223 | 81.622 | False | 0.068 | False |
| 2019-09-18 | False | False | 2.800383 | 0.870826 | 3.4833 | 27.86 |  |  | 2.760883 | 88.588 | False | 0.307 | True |
| 2019-10-30 | False | False | 2.812815 | 0.883258 | 3.533 | 4.97 |  |  | 2.773315 | 89.831 | True | 0.131 | True |
| 2019-12-11 | False | False | 2.825261 | 0.895704 | 3.5828 | 4.98 |  |  | 2.785761 | 91.076 | True | 0.051 | True |
| 2020-01-29 | False | False | 2.837728 | 0.90817 | 3.6327 | 4.99 |  |  | 2.798228 | 92.323 | True | 0.224 | True |
| 2020-03-18 | False | False | 2.85021 | 0.920653 | 3.6826 | 4.99 |  |  | 2.81071 | 93.571 | True | 0.401 | True |
| 2020-04-29 | False | False | 2.861148 | 0.931591 | 3.7264 | 4.38 |  |  | 2.821648 | 94.665 | True | 0.178 | True |
| 2020-06-10 | False | False | 2.872075 | 0.942518 | 3.7701 | 4.37 |  |  | 2.832575 | 95.757 | True | 0.055 | True |
| 2020-07-29 | False | False | 2.882984 | 0.953427 | 3.8137 | 4.36 |  |  | 2.843484 | 96.848 | True | 0.274 | True |
| 2020-09-16 | False | False | 2.893881 | 0.964324 | 3.8573 | 4.36 |  |  | 2.854381 | 97.938 | True | 0.499 | True |
| 2020-11-05 | False | False | 2.881921 | 0.952364 | 3.8095 | -4.78 |  |  | 2.842421 | 96.742 | True | 0.366 | True |
| 2020-12-16 | False | False | 2.869965 | 0.940408 | 3.7616 | -4.78 |  |  | 2.830465 | 95.547 | True | 0.233 | True |
| 2021-01-27 | False | False | 2.858017 | 0.92846 | 3.7138 | -4.78 |  |  | 2.818517 | 94.352 | True | 0.104 | True |
| 2021-03-17 | False | False | 2.846078 | 0.916521 | 3.6661 | -4.78 |  |  | 2.806578 | 93.158 | True | 0.047 | True |
| 2021-04-28 | False | False | 2.834149 | 0.904592 | 3.6184 | -4.77 |  |  | 2.794649 | 91.965 | True | 0.171 | True |
| 2021-06-16 | False | False | 2.82223 | 0.892673 | 3.5707 | -4.77 |  |  | 2.78273 | 90.773 | True | 0.305 | True |
| 2021-07-28 | False | False | 2.810318 | 0.880761 | 3.523 | -4.76 |  |  | 2.770818 | 89.582 | True | 0.44 | True |
| 2021-09-22 | False | False | 2.798412 | 0.868855 | 3.4754 | -4.76 |  |  | 2.758912 | 88.391 | True | 0.576 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | used | 18 | -0.0 | 0.138 | 0.381 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

_none_

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | 18M | USSO1F Curncy | 2.614 | -0.001 | -0.357 | 0.996 |
| effr_ois | ois_effr | 2Y | USSO2 Curncy | 2.692 | 0.001 | 0.616 | 0.998 |
| effr_ois | ois_effr | 3Y | USSO3 Curncy | 2.756 | -0.0 | -1.727 | 1.0 |

### Stale and outside-listing inputs

_none_

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2018-09-25 | 0.0 | True | 0.243 | 1.929557 |  | 1.93 | -0.044 |
| 2018-09-26 | 2018-09-27 | 1.0 | False | 0.002 | 2.170471 | 24.091 | 2.174038 | -0.357 |
| 2018-11-08 | 2018-11-09 | 1.0 | False | 0.011 | 2.181326 | 1.086 | 2.174349 | 0.698 |
| 2018-12-19 | 2018-12-20 | 1.0 | False | 0.02 | 2.366737 | 18.541 | 2.370954 | -0.422 |
| 2019-01-30 | 2019-01-31 | 1.0 | False | 0.024 | 2.38478 | 1.804 | 2.381086 | 0.369 |
| 2019-03-20 | 2019-03-21 | 1.0 | False | 0.036 | 2.537994 | 15.321 | 2.540757 | -0.276 |
| 2019-05-01 | 2019-05-02 | 1.0 | False | 0.039 | 2.582595 | 4.46 | 2.585686 | -0.309 |
| 2019-06-19 | 2019-06-20 | 1.0 | False | 0.054 | 2.693448 | 11.085 | 2.691376 | 0.207 |
| 2019-07-31 | 2019-08-01 | 1.0 | False | 0.068 | 2.730723 | 3.727 | 2.742889 | -1.217 |
| 2019-09-18 | 2019-09-19 | 1.0 | False | 0.307 | 2.800383 | 6.966 |  |  |
| 2019-10-30 | 2019-10-31 | 0.2664 | True | 0.131 | 2.812815 | 1.243 |  |  |
| 2019-12-11 | 2019-12-12 | 0.3627 | True | 0.051 | 2.825261 | 1.245 |  |  |
| 2020-01-29 | 2020-01-30 | 0.3627 | True | 0.224 | 2.837728 | 1.247 |  |  |
| 2020-03-18 | 2020-03-19 | 0.1547 | True | 0.401 | 2.85021 | 1.248 |  |  |
| 2020-04-29 | 2020-04-30 | 0.2255 | True | 0.178 | 2.861148 | 1.094 |  |  |
| 2020-06-10 | 2020-06-11 | 0.307 | True | 0.055 | 2.872075 | 1.093 |  |  |
| 2020-07-29 | 2020-07-30 | 0.307 | True | 0.274 | 2.882984 | 1.091 |  |  |
| 2020-09-16 | 2020-09-17 | 0.1052 | True | 0.499 | 2.893881 | 1.09 |  |  |
| 2020-11-05 | 2020-11-06 | 0.1023 | True | 0.366 | 2.881921 | -1.196 |  |  |
| 2020-12-16 | 2020-12-17 | 0.1074 | True | 0.233 | 2.869965 | -1.196 |  |  |
| 2021-01-27 | 2021-01-28 | 0.1462 | True | 0.104 | 2.858017 | -1.195 |  |  |
| 2021-03-17 | 2021-03-18 | 0.1074 | True | 0.047 | 2.846078 | -1.194 |  |  |
| 2021-04-28 | 2021-04-29 | 0.1462 | True | 0.171 | 2.834149 | -1.193 |  |  |
| 2021-06-16 | 2021-06-17 | 0.1074 | True | 0.305 | 2.82223 | -1.192 |  |  |
| 2021-07-28 | 2021-07-29 | 0.1909 | True | 0.44 | 2.810318 | -1.191 |  |  |
| 2021-09-22 | 2021-09-23 | 0.001 | True | 0.576 | 2.798412 | -1.191 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_ois | ois_effr 1W | 2.167 | used |
| effr_ois | ois_effr 1M | 2.176 | used |
| effr_ois | ois_effr 2M | 2.178 | used |
| effr_ois | ois_effr 3M | 2.196 | used |
| effr_ois | ois_effr 4M | 2.245 | used |
| effr_ois | ois_effr 5M | 2.2755 | used |
| effr_ois | ois_effr 6M | 2.302 | used |
| effr_ois | ois_effr 7M | 2.343 | used |
| effr_ois | ois_effr 8M | 2.376 | used |
| effr_ois | ois_effr 9M | 2.406 | used |
| effr_ois | ois_effr 10M | 2.442 | used |
| effr_ois | ois_effr 11M | 2.4715 | used |
| effr_ois | ois_effr 1Y | 2.501 | used |

Replica notes: ois_effr 1M: no new parcel; re-solved parcel 1 (2018-09-26); ois_effr 4M: no new parcel; re-solved parcel 3 (2018-12-19); ois_effr 7M: no new parcel; re-solved parcel 5 (2019-03-20); ois_effr 10M: no new parcel; re-solved parcel 7 (2019-06-19); ois_effr 1Y: no new parcel; re-solved parcel 8 (2019-07-31); stub parcel not priced by any instrument (the first one starts after the next effective date): set to the last fixing 1.9300 (2018-09-24)

## FF / OIS basis (bp, fit and replica)

| decision_date | effective_date | parcel | effr_fut_fit | effr_ois_fit | basis_fit_bp | basis_replica_bp |
| --- | --- | --- | --- | --- | --- | --- |
| None | None | stub | 1.94377731750589 | 1.929557098095209 | 1.422 | 1.5 |
| 2018-09-26 | 2018-09-27 | 1 | 2.174944 | 2.170471 | 0.447 | 0.096 |
| 2018-11-08 | 2018-11-09 | 2 | 2.182157 | 2.181326 | 0.083 | 0.747 |
| 2018-12-19 | 2018-12-20 | 3 | 2.369632 | 2.366737 | 0.29 | -0.008 |
| 2019-01-30 | 2019-01-31 | 4 | 2.384259 | 2.38478 | -0.052 | 0.391 |
| 2019-03-20 | 2019-03-21 | 5 | 2.544587 | 2.537994 | 0.659 | 0.424 |
| 2019-05-01 | 2019-05-02 | 6 | 2.58126 | 2.582595 | -0.134 | -0.452 |
| 2019-06-19 | 2019-06-20 | 7 | 2.700039 | 2.693448 | 0.659 | 0.862 |
| 2019-07-31 | 2019-08-01 | 8 | 2.724479 | 2.730723 | -0.624 | -1.789 |
| 2019-09-18 | 2019-09-19 | 9 | 2.794286 | 2.800383 | -0.61 |  |
| 2019-10-30 | 2019-10-31 | 10 | 2.804603 | 2.812815 | -0.821 |  |
| 2019-12-11 | 2019-12-12 | 11 | 2.849441 | 2.825261 | 2.418 |  |
| 2020-01-29 | 2020-01-30 | 12 | 2.849866 | 2.837728 | 1.214 |  |
| 2020-03-18 | 2020-03-19 | 13 | 2.868955 | 2.85021 | 1.874 |  |
| 2020-04-29 | 2020-04-30 | 14 | 2.869662 | 2.861148 | 0.851 |  |
| 2020-06-10 | 2020-06-11 | 15 | 2.864367 | 2.872075 | -0.771 |  |
| 2020-07-29 | 2020-07-30 | 16 | 2.861695 | 2.882984 | -2.129 |  |
| 2020-09-16 | 2020-09-17 | 17 | 2.851445 | 2.893881 | -4.244 |  |
| 2020-11-05 | 2020-11-06 | 18 | 2.849712 | 2.881921 | -3.221 |  |
| 2020-12-16 | 2020-12-17 | 19 | 2.849712 | 2.869965 | -2.025 |  |
| 2021-01-27 | 2021-01-28 | 20 | 2.849712 | 2.858017 | -0.83 |  |
| 2021-03-17 | 2021-03-18 | 21 | 2.849712 | 2.846078 | 0.363 |  |
| 2021-04-28 | 2021-04-29 | 22 | 2.849712 | 2.834149 | 1.556 |  |
| 2021-06-16 | 2021-06-17 | 23 | 2.849712 | 2.82223 | 2.748 |  |
| 2021-07-28 | 2021-07-29 | 24 | 2.849712 | 2.810318 | 3.939 |  |
| 2021-09-22 | 2021-09-23 | 25 | 2.849712 | 2.798412 | 5.13 |  |

## Stub

| curve | as_of | current_implied | replica_current_implied | stub_prior | stub_prior_source | anchor | spread | spread_median | spread_winsorised_mean | spread_obs | spread_estimator | spread_note | wirp_reach_meetings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | 2018-09-25 | 1.943777 | 1.945 | 1.9145 | anchor + spread (D7) | 1.875 | 0.03949999999999993 | 0.03499999999999992 | 0.03949999999999993 | 60 | winsorised_mean |  | 18 |
| effr_ois | 2018-09-25 | 1.929557 | 1.93 | 1.9145 | anchor + spread (D7) | 1.875 | 0.03949999999999993 | 0.03499999999999992 | 0.03949999999999993 | 60 | winsorised_mean |  | 8 |
