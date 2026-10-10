# USD EFFR front end, 2020-03-03

Anchor (target_midpoint) in effect: 1.625. Policy spread (winsorised_mean, D7): -6.30bp (winsorised mean -6.30bp, median -7.50bp; 59 fixings, 4 turn days dropped, window 2019-11-29..2020-03-02) **Loader reported blocking problems in the window (see check_market_data.py).**

## Curve `effr_fut` (ff_fut)

Fit: 20 quotes (1 dropped, 16 excluded by metadata), 3 IRLS iterations (converged); 26 parcels to 2023-03-03, 0 synthetic and 1 unscheduled meetings. Current implied O/N rate 1.4197 (replica 1.0227; stub prior 1.5620 from anchor + spread (D7)). WIRP replica reaches 14 meetings on 20 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2020-03-03 | False | True | 1.105545 | -0.314106 | -1.2564 | -125.64 | 1.130153 | -2.461 | 1.168511 | -45.649 | False | 0.01 | False |
| 2020-03-18 | False | False | 0.792132 | -0.627519 | -2.5101 | -125.37 | 0.793849 | -0.172 | 0.855098 | -76.99 | False | 0.005 | False |
| 2020-04-29 | False | False | 0.724676 | -0.694975 | -2.7799 | -26.98 | 0.678392 | 4.628 | 0.787642 | -83.736 | False | 0.018 | False |
| 2020-06-10 | False | False | 0.597673 | -0.821979 | -3.2879 | -50.8 | 0.605542 | -0.787 | 0.660639 | -96.436 | False | 0.005 | False |
| 2020-07-29 | False | False | 0.556203 | -0.863448 | -3.4538 | -16.59 | 0.554532 | 0.167 | 0.619169 | -100.583 | False | 0.005 | False |
| 2020-09-16 | False | False | 0.505934 | -0.913717 | -3.6549 | -20.11 | 0.505 | 0.093 | 0.5689 | -105.61 | False | 0.005 | False |
| 2020-11-05 | False | False | 0.493673 | -0.925979 | -3.7039 | -4.9 | 0.493 | 0.067 | 0.556639 | -106.836 | False | 0.005 | False |
| 2020-12-16 | False | False | 0.462835 | -0.956816 | -3.8273 | -12.33 | 0.466133 | -0.33 | 0.525802 | -109.92 | False | 0.005 | False |
| 2021-01-27 | False | False | 0.445848 | -0.973803 | -3.8952 | -6.79 | 0.445 | 0.085 | 0.508814 | -111.619 | False | 0.005 | False |
| 2021-03-17 | False | False | 0.461043 | -0.958608 | -3.8344 | 6.08 | 0.467143 | -0.61 | 0.524009 | -110.099 | False | 0.006 | False |
| 2021-04-28 | False | False | 0.464865 | -0.954786 | -3.8191 | 1.53 | 0.465 | -0.013 | 0.527831 | -109.717 | False | 0.01 | False |
| 2021-06-16 | False | False | 0.484765 | -0.934886 | -3.7395 | 7.96 | 0.486429 | -0.166 | 0.547731 | -107.727 | False | 0.022 | False |
| 2021-07-28 | False | False | 0.491643 | -0.928009 | -3.712 | 2.75 | 0.49 | 0.164 | 0.554609 | -107.039 | False | 0.018 | False |
| 2021-09-22 | False | False | 0.495611 | -0.92404 | -3.6962 | 1.59 | 0.495 | 0.061 | 0.558577 | -106.642 | False | 0.022 | False |
| 2021-11-03 | False | False | 0.495611 | -0.92404 | -3.6962 | 0.0 |  |  | 0.558577 | -106.642 | True | 0.022 | True |
| 2021-12-15 | False | False | 0.495611 | -0.92404 | -3.6962 | 0.0 |  |  | 0.558577 | -106.642 | True | 0.023 | True |
| 2022-01-26 | False | False | 0.495611 | -0.92404 | -3.6962 | 0.0 |  |  | 0.558577 | -106.642 | True | 0.023 | True |
| 2022-03-16 | False | False | 0.495611 | -0.92404 | -3.6962 | 0.0 |  |  | 0.558577 | -106.642 | True | 0.024 | True |
| 2022-05-04 | False | False | 0.495611 | -0.92404 | -3.6962 | 0.0 |  |  | 0.558577 | -106.642 | True | 0.025 | True |
| 2022-06-15 | False | False | 0.495611 | -0.92404 | -3.6962 | 0.0 |  |  | 0.558577 | -106.642 | True | 0.025 | True |
| 2022-07-27 | False | False | 0.495611 | -0.92404 | -3.6962 | 0.0 |  |  | 0.558577 | -106.642 | True | 0.026 | True |
| 2022-09-21 | False | False | 0.495611 | -0.92404 | -3.6962 | 0.0 |  |  | 0.558577 | -106.642 | True | 0.026 | True |
| 2022-11-02 | False | False | 0.495611 | -0.92404 | -3.6962 | 0.0 |  |  | 0.558577 | -106.642 | True | 0.026 | True |
| 2022-12-14 | False | False | 0.495611 | -0.92404 | -3.6962 | 0.0 |  |  | 0.558577 | -106.642 | True | 0.027 | True |
| 2023-02-01 | False | False | 0.495611 | -0.92404 | -3.6962 | 0.0 |  |  | 0.558577 | -106.642 | True | 0.027 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | dropped | 1 | -4.968 | 4.968 | 4.968 |
| effr_fut | ff_fut | used | 19 | 0.004 | 0.119 | 0.23 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

| curve | instrument | contract | ticker | status | reason | residual_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2020-05 | FFK20 Comdty | dropped | leave-one-out residual -4.97bp, over 6.0 x its effective noise 0.50bp (alone pinned a parcel) | -4.968 |
| effr_fut | ff_fut | 2021-11 | FFX21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-12 | FFZ21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-01 | FFF22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
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
| effr_fut | ff_fut | 2020-03 | FFH20 Comdty | 1.015 | -0.018 | -3.308 | 0.995 |
| effr_fut | ff_fut | 2020-04 | FFJ20 Comdty | 0.79 | 0.012 | 4.404 | 0.997 |
| effr_fut | ff_fut | 2020-06 | FFM20 Comdty | 0.64 | -0.001 | -1.455 | 1.0 |
| effr_fut | ff_fut | 2020-07 | FFN20 Comdty | 0.595 | 0.0 | 0.668 | 1.0 |
| effr_fut | ff_fut | 2021-05 | FFK21 Comdty | 0.465 | 0.013 | 0.282 | 0.952 |
| effr_fut | ff_fut | 2021-10 | FFV21 Comdty | 0.495 | -0.061 | -1.364 | 0.955 |

### Stale and outside-listing inputs

| curve | flag | instrument | contract | status | detail |
| --- | --- | --- | --- | --- | --- |
| effr_fut | outside_listing | ff_fut | 2022-10 | excluded | loader: FFV22 Comdty|PX_LAST quoted from 2019-10-31, modelled first listing 2019-11-01 |
| effr_fut | outside_listing | ff_fut | 2022-11 | excluded | loader: FFX22 Comdty|PX_LAST quoted from 2019-11-27, modelled first listing 2019-12-02 |
| effr_fut | outside_listing | ff_fut | 2022-12 | excluded | loader: FFZ22 Comdty|PX_LAST quoted from 2019-12-31, modelled first listing after 2019-12-31 |
| effr_fut | outside_listing | ff_fut | 2023-01 | excluded | loader: FFF23 Comdty|PX_LAST quoted from 2020-01-31, modelled first listing 2020-02-03 |
| effr_fut | outside_listing | ff_fut | 2023-02 | excluded | loader: FFG23 Comdty|PX_LAST quoted from 2020-02-28, modelled first listing 2020-03-02 |

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2020-03-03 | 0.0044 | True | 0.028 | 1.419651 |  | 1.022677 | 39.697 |
| 2020-03-03 (unscheduled) | 2020-03-04 | 0.9956 | False | 0.01 | 1.105545 | -31.411 | 1.130153 | -2.461 |
| 2020-03-18 | 2020-03-19 | 1.0 | False | 0.005 | 0.792132 | -31.341 | 0.793849 | -0.172 |
| 2020-04-29 | 2020-04-30 | 1.0 | False | 0.018 | 0.724676 | -6.746 | 0.678392 | 4.628 |
| 2020-06-10 | 2020-06-11 | 1.0 | False | 0.005 | 0.597673 | -12.7 | 0.605542 | -0.787 |
| 2020-07-29 | 2020-07-30 | 1.0 | False | 0.005 | 0.556203 | -4.147 | 0.554532 | 0.167 |
| 2020-09-16 | 2020-09-17 | 1.0 | False | 0.005 | 0.505934 | -5.027 | 0.505 | 0.093 |
| 2020-11-05 | 2020-11-06 | 1.0 | False | 0.005 | 0.493673 | -1.226 | 0.493 | 0.067 |
| 2020-12-16 | 2020-12-17 | 1.0 | False | 0.005 | 0.462835 | -3.084 | 0.466133 | -0.33 |
| 2021-01-27 | 2021-01-28 | 1.0 | False | 0.005 | 0.445848 | -1.699 | 0.445 | 0.085 |
| 2021-03-17 | 2021-03-18 | 1.0 | False | 0.006 | 0.461043 | 1.52 | 0.467143 | -0.61 |
| 2021-04-28 | 2021-04-29 | 1.0 | False | 0.01 | 0.464865 | 0.382 | 0.465 | -0.013 |
| 2021-06-16 | 2021-06-17 | 1.0 | False | 0.022 | 0.484765 | 1.99 | 0.486429 | -0.166 |
| 2021-07-28 | 2021-07-29 | 1.0 | False | 0.018 | 0.491643 | 0.688 | 0.49 | 0.164 |
| 2021-09-22 | 2021-09-23 | 1.0 | False | 0.022 | 0.495611 | 0.397 | 0.495 | 0.061 |
| 2021-11-03 | 2021-11-04 | 0.0 | True | 0.022 | 0.495611 | 0.0 |  |  |
| 2021-12-15 | 2021-12-16 | 0.0 | True | 0.023 | 0.495611 | 0.0 |  |  |
| 2022-01-26 | 2022-01-27 | 0.0 | True | 0.023 | 0.495611 | 0.0 |  |  |
| 2022-03-16 | 2022-03-17 | 0.0 | True | 0.024 | 0.495611 | 0.0 |  |  |
| 2022-05-04 | 2022-05-05 | 0.0 | True | 0.025 | 0.495611 | 0.0 |  |  |
| 2022-06-15 | 2022-06-16 | 0.0 | True | 0.025 | 0.495611 | 0.0 |  |  |
| 2022-07-27 | 2022-07-28 | 0.0 | True | 0.026 | 0.495611 | 0.0 |  |  |
| 2022-09-21 | 2022-09-22 | 0.0 | True | 0.026 | 0.495611 | 0.0 |  |  |
| 2022-11-02 | 2022-11-03 | 0.0 | True | 0.026 | 0.495611 | 0.0 |  |  |
| 2022-12-14 | 2022-12-15 | 0.0 | True | 0.027 | 0.495611 | 0.0 |  |  |
| 2023-02-01 | 2023-02-02 | 0.0 | True | 0.027 | 0.495611 | 0.0 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_fut | ff_fut 2020-03 | 1.0150000000000006 | used |
| effr_fut | ff_fut 2020-04 | 0.7900000000000063 | used |
| effr_fut | ff_fut 2020-05 | 0.6749999999999972 | used |
| effr_fut | ff_fut 2020-06 | 0.6400000000000006 | used |
| effr_fut | ff_fut 2020-07 | 0.5949999999999989 | used |
| effr_fut | ff_fut 2020-08 | 0.5550000000000068 | used |
| effr_fut | ff_fut 2020-09 | 0.5349999999999966 | used |
| effr_fut | ff_fut 2020-10 | 0.5049999999999955 | used |
| effr_fut | ff_fut 2020-11 | 0.49500000000000455 | used |
| effr_fut | ff_fut 2020-12 | 0.480000000000004 | used |
| effr_fut | ff_fut 2021-01 | 0.45999999999999375 | used |
| effr_fut | ff_fut 2021-02 | 0.4449999999999932 | used |
| effr_fut | ff_fut 2021-03 | 0.4549999999999983 | used |
| effr_fut | ff_fut 2021-04 | 0.45999999999999375 | used |
| effr_fut | ff_fut 2021-05 | 0.4650000000000034 | used |
| effr_fut | ff_fut 2021-06 | 0.4749999999999943 | used |
| effr_fut | ff_fut 2021-07 | 0.48499999999999943 | used |
| effr_fut | ff_fut 2021-08 | 0.4899999999999949 | used |
| effr_fut | ff_fut 2021-09 | 0.49500000000000455 | used |
| effr_fut | ff_fut 2021-10 | 0.49500000000000455 | used |

Replica notes: ff_fut 2020-10: no new parcel; re-solved parcel 6 (2020-09-16); ff_fut 2021-02: no new parcel; re-solved parcel 9 (2021-01-27); ff_fut 2021-05: no new parcel; re-solved parcel 11 (2021-04-28); ff_fut 2021-08: no new parcel; re-solved parcel 13 (2021-07-28); ff_fut 2021-10: no new parcel; re-solved parcel 14 (2021-09-22)

## Curve `effr_ois` (ois_effr)

Fit: 18 quotes (1 dropped, 0 excluded by metadata), 5 IRLS iterations (converged); 26 parcels to 2023-03-15, 0 synthetic and 1 unscheduled meetings. Current implied O/N rate 1.5337 (replica 1.5900; stub prior 1.5620 from anchor + spread (D7)). WIRP replica reaches 9 meetings on 13 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2020-03-03 | False | True | 1.08011 | -0.453575 | -1.8143 | -181.43 | 1.079917 | 0.019 | 1.143076 | -48.192 | False | 0.004 | False |
| 2020-03-18 | False | False | 0.890807 | -0.642878 | -2.5715 | -75.72 | 0.894469 | -0.366 | 0.953773 | -67.123 | False | 0.006 | False |
| 2020-04-29 | False | False | 0.761346 | -0.772339 | -3.0894 | -51.78 | 0.757402 | 0.394 | 0.824312 | -80.069 | False | 0.015 | False |
| 2020-06-10 | False | False | 0.684358 | -0.849327 | -3.3973 | -30.8 | 0.688203 | -0.384 | 0.747324 | -87.768 | False | 0.02 | False |
| 2020-07-29 | False | False | 0.625298 | -0.908387 | -3.6335 | -23.62 | 0.618535 | 0.676 | 0.688264 | -93.674 | False | 0.028 | False |
| 2020-09-16 | False | False | 0.579059 | -0.954626 | -3.8185 | -18.5 | 0.580008 | -0.095 | 0.642025 | -98.297 | False | 0.034 | False |
| 2020-11-05 | False | False | 0.538483 | -0.995203 | -3.9808 | -16.23 | 0.545685 | -0.72 | 0.601449 | -102.355 | False | 0.052 | False |
| 2020-12-16 | False | False | 0.515088 | -1.018597 | -4.0744 | -9.36 | 0.513361 | 0.173 | 0.578054 | -104.695 | False | 0.068 | False |
| 2021-01-27 | False | False | 0.491826 | -1.04186 | -4.1674 | -9.3 | 0.487558 | 0.427 | 0.554792 | -107.021 | False | 0.08 | False |
| 2021-03-17 | False | False | 0.496244 | -1.037441 | -4.1498 | 1.77 |  |  | 0.55921 | -106.579 | True | 0.044 | True |
| 2021-04-28 | False | False | 0.500657 | -1.033028 | -4.1321 | 1.77 |  |  | 0.563623 | -106.138 | True | 0.019 | True |
| 2021-06-16 | False | False | 0.505063 | -1.028623 | -4.1145 | 1.76 |  |  | 0.568029 | -105.697 | True | 0.041 | True |
| 2021-07-28 | False | False | 0.509463 | -1.024222 | -4.0969 | 1.76 |  |  | 0.572429 | -105.257 | True | 0.081 | True |
| 2021-09-22 | False | False | 0.513014 | -1.020671 | -4.0827 | 1.42 |  |  | 0.57598 | -104.902 | True | 0.046 | True |
| 2021-11-03 | False | False | 0.516572 | -1.017114 | -4.0685 | 1.42 |  |  | 0.579538 | -104.546 | True | 0.026 | True |
| 2021-12-15 | False | False | 0.520138 | -1.013547 | -4.0542 | 1.43 |  |  | 0.583104 | -104.19 | True | 0.047 | True |
| 2022-01-26 | False | False | 0.523711 | -1.009974 | -4.0399 | 1.43 |  |  | 0.586677 | -103.832 | True | 0.087 | True |
| 2022-03-16 | False | False | 0.539666 | -0.99402 | -3.9761 | 6.38 |  |  | 0.602632 | -102.237 | True | 0.069 | True |
| 2022-05-04 | False | False | 0.555615 | -0.97807 | -3.9123 | 6.38 |  |  | 0.618581 | -100.642 | True | 0.055 | True |
| 2022-06-15 | False | False | 0.571555 | -0.96213 | -3.8485 | 6.38 |  |  | 0.634521 | -99.048 | True | 0.043 | True |
| 2022-07-27 | False | False | 0.587484 | -0.946201 | -3.7848 | 6.37 |  |  | 0.65045 | -97.455 | True | 0.033 | True |
| 2022-09-21 | False | False | 0.603401 | -0.930284 | -3.7211 | 6.37 |  |  | 0.666367 | -95.863 | True | 0.034 | True |
| 2022-11-02 | False | False | 0.619307 | -0.914379 | -3.6575 | 6.36 |  |  | 0.682273 | -94.273 | True | 0.053 | True |
| 2022-12-14 | False | False | 0.635203 | -0.898482 | -3.5939 | 6.36 |  |  | 0.698169 | -92.683 | True | 0.083 | True |
| 2023-02-01 | False | False | 0.651095 | -0.882591 | -3.5304 | 6.36 |  |  | 0.714061 | -91.094 | True | 0.12 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | dropped | 1 | 33.172 | 33.172 | 33.172 |
| effr_ois | ois_effr | used | 17 | -0.0 | 0.077 | 0.198 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

| curve | instrument | contract | ticker | status | reason | residual_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | 3W | USSO3Z Curncy | dropped | Huber weight 0.020 < 0.2 | 33.172 |

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | 1Y | USSO1 Curncy | 0.657 | -0.011 | -0.443 | 0.974 |
| effr_ois | ois_effr | 18M | USSO1F Curncy | 0.605 | 0.001 | 0.26 | 0.998 |
| effr_ois | ois_effr | 2Y | USSO2 Curncy | 0.584 | -0.001 | -0.503 | 0.999 |
| effr_ois | ois_effr | 3Y | USSO3 Curncy | 0.587 | 0.0 | 2.254 | 1.0 |

### Stale and outside-listing inputs

_none_

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2020-03-03 | 0.0 | True | 0.243 | 1.533685 |  | 1.59 | -5.631 |
| 2020-03-03 (unscheduled) | 2020-03-04 | 1.0 | False | 0.004 | 1.08011 | -45.358 | 1.079917 | 0.019 |
| 2020-03-18 | 2020-03-19 | 1.0 | False | 0.006 | 0.890807 | -18.93 | 0.894469 | -0.366 |
| 2020-04-29 | 2020-04-30 | 1.0 | False | 0.015 | 0.761346 | -12.946 | 0.757402 | 0.394 |
| 2020-06-10 | 2020-06-11 | 1.0 | False | 0.02 | 0.684358 | -7.699 | 0.688203 | -0.384 |
| 2020-07-29 | 2020-07-30 | 1.0 | False | 0.028 | 0.625298 | -5.906 | 0.618535 | 0.676 |
| 2020-09-16 | 2020-09-17 | 1.0 | False | 0.034 | 0.579059 | -4.624 | 0.580008 | -0.095 |
| 2020-11-05 | 2020-11-06 | 1.0 | False | 0.052 | 0.538483 | -4.058 | 0.545685 | -0.72 |
| 2020-12-16 | 2020-12-17 | 1.0 | False | 0.068 | 0.515088 | -2.339 | 0.513361 | 0.173 |
| 2021-01-27 | 2021-01-28 | 1.0 | False | 0.08 | 0.491826 | -2.326 | 0.487558 | 0.427 |
| 2021-03-17 | 2021-03-18 | 0.2361 | True | 0.044 | 0.496244 | 0.442 |  |  |
| 2021-04-28 | 2021-04-29 | 0.3214 | True | 0.019 | 0.500657 | 0.441 |  |  |
| 2021-06-16 | 2021-06-17 | 0.2361 | True | 0.041 | 0.505063 | 0.441 |  |  |
| 2021-07-28 | 2021-07-29 | 0.2352 | True | 0.081 | 0.509463 | 0.44 |  |  |
| 2021-09-22 | 2021-09-23 | 0.2518 | True | 0.046 | 0.513014 | 0.355 |  |  |
| 2021-11-03 | 2021-11-04 | 0.2518 | True | 0.026 | 0.516572 | 0.356 |  |  |
| 2021-12-15 | 2021-12-16 | 0.2518 | True | 0.047 | 0.520138 | 0.357 |  |  |
| 2022-01-26 | 2022-01-27 | 0.2207 | True | 0.087 | 0.523711 | 0.357 |  |  |
| 2022-03-16 | 2022-03-17 | 0.1492 | True | 0.069 | 0.539666 | 1.595 |  |  |
| 2022-05-04 | 2022-05-05 | 0.1096 | True | 0.055 | 0.555615 | 1.595 |  |  |
| 2022-06-15 | 2022-06-16 | 0.1096 | True | 0.043 | 0.571555 | 1.594 |  |  |
| 2022-07-27 | 2022-07-28 | 0.1948 | True | 0.033 | 0.587484 | 1.593 |  |  |
| 2022-09-21 | 2022-09-22 | 0.1096 | True | 0.034 | 0.603401 | 1.592 |  |  |
| 2022-11-02 | 2022-11-03 | 0.1096 | True | 0.053 | 0.619307 | 1.591 |  |  |
| 2022-12-14 | 2022-12-15 | 0.1492 | True | 0.083 | 0.635203 | 1.59 |  |  |
| 2023-02-01 | 2023-02-02 | 0.0636 | True | 0.12 | 0.651095 | 1.589 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_ois | ois_effr 1W | 1.08 | used |
| effr_ois | ois_effr 1M | 0.976 | used |
| effr_ois | ois_effr 2M | 0.9225 | used |
| effr_ois | ois_effr 3M | 0.87 | used |
| effr_ois | ois_effr 4M | 0.828 | used |
| effr_ois | ois_effr 5M | 0.797 | used |
| effr_ois | ois_effr 6M | 0.766 | used |
| effr_ois | ois_effr 7M | 0.746 | used |
| effr_ois | ois_effr 8M | 0.724 | used |
| effr_ois | ois_effr 9M | 0.70385 | used |
| effr_ois | ois_effr 10M | 0.686 | used |
| effr_ois | ois_effr 11M | 0.671 | used |
| effr_ois | ois_effr 1Y | 0.657 | used |

Replica notes: ois_effr 3M: no new parcel; re-solved parcel 3 (2020-04-29); ois_effr 6M: no new parcel; re-solved parcel 5 (2020-07-29); ois_effr 8M: no new parcel; re-solved parcel 6 (2020-09-16); ois_effr 11M: no new parcel; re-solved parcel 8 (2020-12-16); stub parcel not priced by any instrument (the first one starts after the next effective date): set to the last fixing 1.5900 (2020-03-02)

## FF / OIS basis (bp, fit and replica)

| decision_date | effective_date | parcel | effr_fut_fit | effr_ois_fit | basis_fit_bp | basis_replica_bp |
| --- | --- | --- | --- | --- | --- | --- |
| None | None | stub | 1.4196514110918776 | 1.533685447607078 | -11.403 | -56.732 |
| 2020-03-03 | 2020-03-04 | 1 | 1.105545 | 1.08011 | 2.544 | 5.024 |
| 2020-03-18 | 2020-03-19 | 2 | 0.792132 | 0.890807 | -9.867 | -10.062 |
| 2020-04-29 | 2020-04-30 | 3 | 0.724676 | 0.761346 | -3.667 | -7.901 |
| 2020-06-10 | 2020-06-11 | 4 | 0.597673 | 0.684358 | -8.669 | -8.266 |
| 2020-07-29 | 2020-07-30 | 5 | 0.556203 | 0.625298 | -6.91 | -6.4 |
| 2020-09-16 | 2020-09-17 | 6 | 0.505934 | 0.579059 | -7.313 | -7.501 |
| 2020-11-05 | 2020-11-06 | 7 | 0.493673 | 0.538483 | -4.481 | -5.269 |
| 2020-12-16 | 2020-12-17 | 8 | 0.462835 | 0.515088 | -5.225 | -4.723 |
| 2021-01-27 | 2021-01-28 | 9 | 0.445848 | 0.491826 | -4.598 | -4.256 |
| 2021-03-17 | 2021-03-18 | 10 | 0.461043 | 0.496244 | -3.52 |  |
| 2021-04-28 | 2021-04-29 | 11 | 0.464865 | 0.500657 | -3.579 |  |
| 2021-06-16 | 2021-06-17 | 12 | 0.484765 | 0.505063 | -2.03 |  |
| 2021-07-28 | 2021-07-29 | 13 | 0.491643 | 0.509463 | -1.782 |  |
| 2021-09-22 | 2021-09-23 | 14 | 0.495611 | 0.513014 | -1.74 |  |
| 2021-11-03 | 2021-11-04 | 15 | 0.495611 | 0.516572 | -2.096 |  |
| 2021-12-15 | 2021-12-16 | 16 | 0.495611 | 0.520138 | -2.453 |  |
| 2022-01-26 | 2022-01-27 | 17 | 0.495611 | 0.523711 | -2.81 |  |
| 2022-03-16 | 2022-03-17 | 18 | 0.495611 | 0.539666 | -4.405 |  |
| 2022-05-04 | 2022-05-05 | 19 | 0.495611 | 0.555615 | -6.0 |  |
| 2022-06-15 | 2022-06-16 | 20 | 0.495611 | 0.571555 | -7.594 |  |
| 2022-07-27 | 2022-07-28 | 21 | 0.495611 | 0.587484 | -9.187 |  |
| 2022-09-21 | 2022-09-22 | 22 | 0.495611 | 0.603401 | -10.779 |  |
| 2022-11-02 | 2022-11-03 | 23 | 0.495611 | 0.619307 | -12.37 |  |
| 2022-12-14 | 2022-12-15 | 24 | 0.495611 | 0.635203 | -13.959 |  |
| 2023-02-01 | 2023-02-02 | 25 | 0.495611 | 0.651095 | -15.548 |  |

## Stub

| curve | as_of | current_implied | replica_current_implied | stub_prior | stub_prior_source | anchor | spread | spread_median | spread_winsorised_mean | spread_obs | spread_estimator | spread_note | wirp_reach_meetings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | 2020-03-03 | 1.419651 | 1.022677 | 1.562034 | anchor + spread (D7) | 1.625 | -0.0629661016949152 | -0.07499999999999996 | -0.0629661016949152 | 59 | winsorised_mean |  | 14 |
| effr_ois | 2020-03-03 | 1.533685 | 1.59 | 1.562034 | anchor + spread (D7) | 1.625 | -0.0629661016949152 | -0.07499999999999996 | -0.0629661016949152 | 59 | winsorised_mean |  | 9 |
