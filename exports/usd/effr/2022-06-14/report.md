# USD EFFR front end, 2022-06-14

Anchor (target_midpoint) in effect: 0.875. Policy spread (winsorised_mean, D7): -4.50bp (winsorised mean -4.50bp, median -4.50bp; 60 fixings, 3 turn days dropped, window 2022-03-16..2022-06-13) **Loader reported blocking problems in the window (see check_market_data.py).**

## Curve `effr_fut` (ff_fut)

Fit: 23 quotes (0 dropped, 14 excluded by metadata), 9 IRLS iterations (converged); 25 parcels to 2025-06-14, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 0.7373 (replica 0.7217; stub prior 0.8300 from anchor + spread (D7)). WIRP replica reaches 15 meetings on 23 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2022-06-15 | False | False | 1.564094 | 0.826808 | 3.3072 | 330.72 | 1.564444 | -0.035 | 1.609094 | 73.409 | False | 0.006 | False |
| 2022-07-27 | False | False | 2.303489 | 1.566202 | 6.2648 | 295.76 | 2.305 | -0.151 | 2.348489 | 147.349 | False | 0.004 | False |
| 2022-09-21 | False | False | 2.899346 | 2.162059 | 8.6482 | 238.34 | 2.9 | -0.065 | 2.944346 | 206.935 | False | 0.005 | False |
| 2022-11-02 | False | False | 3.371106 | 2.633819 | 10.5353 | 188.7 | 3.371429 | -0.032 | 3.416106 | 254.111 | False | 0.005 | False |
| 2022-12-14 | False | False | 3.68949 | 2.952203 | 11.8088 | 127.35 | 3.69 | -0.051 | 3.73449 | 285.949 | False | 0.004 | False |
| 2023-02-01 | False | False | 3.900957 | 3.16367 | 12.6547 | 84.59 | 3.897407 | 0.355 | 3.945957 | 307.096 | False | 0.005 | False |
| 2023-03-22 | False | False | 4.031904 | 3.294617 | 13.1785 | 52.38 | 4.03 | 0.19 | 4.076904 | 320.19 | False | 0.006 | False |
| 2023-05-03 | False | False | 4.057854 | 3.320567 | 13.2823 | 10.38 | 4.057679 | 0.018 | 4.102854 | 322.785 | False | 0.008 | False |
| 2023-06-14 | False | False | 4.019521 | 3.282234 | 13.1289 | -15.33 | 4.024531 | -0.501 | 4.064521 | 318.952 | False | 0.01 | False |
| 2023-07-26 | False | False | 3.964388 | 3.227101 | 12.9084 | -22.05 | 3.965 | -0.061 | 4.009388 | 313.439 | False | 0.012 | False |
| 2023-09-20 | False | False | 3.879559 | 3.142272 | 12.5691 | -33.93 | 3.88 | -0.044 | 3.924559 | 304.956 | False | 0.021 | False |
| 2023-11-01 | False | False | 3.801703 | 3.064416 | 12.2577 | -31.14 | 3.802414 | -0.071 | 3.846703 | 297.17 | False | 0.022 | False |
| 2023-12-13 | False | False | 3.724057 | 2.986771 | 11.9471 | -31.06 | 3.725 | -0.094 | 3.769057 | 289.406 | False | 0.02 | False |
| 2024-01-31 | False | False | 3.640583 | 2.903296 | 11.6132 | -33.39 | 3.66 | -1.942 | 3.685583 | 281.058 | False | 0.02 | False |
| 2024-03-20 | False | False | 3.529384 | 2.792097 | 11.1684 | -44.48 | 3.54 | -1.062 | 3.574384 | 269.938 | False | 0.022 | False |
| 2024-05-01 | False | False | 3.529384 | 2.792097 | 11.1684 | 0.0 |  |  | 3.574384 | 269.938 | True | 0.022 | True |
| 2024-06-12 | False | False | 3.529384 | 2.792097 | 11.1684 | 0.0 |  |  | 3.574384 | 269.938 | True | 0.023 | True |
| 2024-07-31 | False | False | 3.529384 | 2.792097 | 11.1684 | 0.0 |  |  | 3.574384 | 269.938 | True | 0.023 | True |
| 2024-09-18 | False | False | 3.529384 | 2.792097 | 11.1684 | 0.0 |  |  | 3.574384 | 269.938 | True | 0.024 | True |
| 2024-11-07 | False | False | 3.529384 | 2.792097 | 11.1684 | 0.0 |  |  | 3.574384 | 269.938 | True | 0.024 | True |
| 2024-12-18 | False | False | 3.529384 | 2.792097 | 11.1684 | 0.0 |  |  | 3.574384 | 269.938 | True | 0.025 | True |
| 2025-01-29 | False | False | 3.529384 | 2.792097 | 11.1684 | 0.0 |  |  | 3.574384 | 269.938 | True | 0.025 | True |
| 2025-03-19 | False | False | 3.529384 | 2.792097 | 11.1684 | 0.0 |  |  | 3.574384 | 269.938 | True | 0.026 | True |
| 2025-05-07 | False | False | 3.529384 | 2.792097 | 11.1684 | 0.0 |  |  | 3.574384 | 269.938 | True | 0.026 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | used | 23 | -0.018 | 1.376 | 5.613 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

| curve | instrument | contract | ticker | status | reason | residual_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2024-05 | FFK24 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2024-06 | FFM24 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2024-07 | FFN24 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2024-08 | FFQ24 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2024-09 | FFU24 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2024-10 | FFV24 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2024-11 | FFX24 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2024-12 | FFZ24 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2025-01 | FFF25 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2025-02 | FFG25 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2025-03 | FFH25 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2025-04 | FFJ25 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2025-05 | FFK25 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2025-06 | FFM25 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2022-06 | FFM22 Comdty | 1.19 | -0.087 | -1.022 | 0.915 |
| effr_fut | ff_fut | 2022-07 | FFN22 Comdty | 1.66 | 0.05 | 1.758 | 0.972 |
| effr_fut | ff_fut | 2022-10 | FFV22 Comdty | 2.9 | 0.065 | 1.135 | 0.942 |
| effr_fut | ff_fut | 2023-02 | FFG23 Comdty | 3.89 | -0.34 | -3.952 | 0.914 |
| effr_fut | ff_fut | 2023-04 | FFJ23 Comdty | 4.03 | -0.19 | -9.86 | 0.98 |
| effr_fut | ff_fut | 2023-05 | FFK23 Comdty | 4.055 | -0.034 | -0.61 | 0.944 |
| effr_fut | ff_fut | 2024-04 | FFJ24 Comdty | 3.54 | 1.062 | 20.205 | 0.947 |

### Stale and outside-listing inputs

_none_

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2022-06-14 | 1.0 | False | 0.082 | 0.737287 |  | 0.721667 | 1.562 |
| 2022-06-15 | 2022-06-16 | 1.0 | False | 0.006 | 1.564094 | 82.681 | 1.564444 | -0.035 |
| 2022-07-27 | 2022-07-28 | 1.0 | False | 0.004 | 2.303489 | 73.939 | 2.305 | -0.151 |
| 2022-09-21 | 2022-09-22 | 1.0 | False | 0.005 | 2.899346 | 59.586 | 2.9 | -0.065 |
| 2022-11-02 | 2022-11-03 | 1.0 | False | 0.005 | 3.371106 | 47.176 | 3.371429 | -0.032 |
| 2022-12-14 | 2022-12-15 | 1.0 | False | 0.004 | 3.68949 | 31.838 | 3.69 | -0.051 |
| 2023-02-01 | 2023-02-02 | 1.0 | False | 0.005 | 3.900957 | 21.147 | 3.897407 | 0.355 |
| 2023-03-22 | 2023-03-23 | 1.0 | False | 0.006 | 4.031904 | 13.095 | 4.03 | 0.19 |
| 2023-05-03 | 2023-05-04 | 1.0 | False | 0.008 | 4.057854 | 2.595 | 4.057679 | 0.018 |
| 2023-06-14 | 2023-06-15 | 1.0 | False | 0.01 | 4.019521 | -3.833 | 4.024531 | -0.501 |
| 2023-07-26 | 2023-07-27 | 1.0 | False | 0.012 | 3.964388 | -5.513 | 3.965 | -0.061 |
| 2023-09-20 | 2023-09-21 | 1.0 | False | 0.021 | 3.879559 | -8.483 | 3.88 | -0.044 |
| 2023-11-01 | 2023-11-02 | 1.0 | False | 0.022 | 3.801703 | -7.786 | 3.802414 | -0.071 |
| 2023-12-13 | 2023-12-14 | 1.0 | False | 0.02 | 3.724057 | -7.765 | 3.725 | -0.094 |
| 2024-01-31 | 2024-02-01 | 1.0 | False | 0.02 | 3.640583 | -8.347 | 3.66 | -1.942 |
| 2024-03-20 | 2024-03-21 | 1.0 | False | 0.022 | 3.529384 | -11.12 | 3.54 | -1.062 |
| 2024-05-01 | 2024-05-02 | 0.0 | True | 0.022 | 3.529384 | 0.0 |  |  |
| 2024-06-12 | 2024-06-13 | 0.0 | True | 0.023 | 3.529384 | 0.0 |  |  |
| 2024-07-31 | 2024-08-01 | 0.0 | True | 0.023 | 3.529384 | 0.0 |  |  |
| 2024-09-18 | 2024-09-19 | 0.0 | True | 0.024 | 3.529384 | 0.0 |  |  |
| 2024-11-07 | 2024-11-08 | 0.0 | True | 0.024 | 3.529384 | 0.0 |  |  |
| 2024-12-18 | 2024-12-19 | 0.0 | True | 0.025 | 3.529384 | 0.0 |  |  |
| 2025-01-29 | 2025-01-30 | 0.0 | True | 0.025 | 3.529384 | 0.0 |  |  |
| 2025-03-19 | 2025-03-20 | 0.0 | True | 0.026 | 3.529384 | 0.0 |  |  |
| 2025-05-07 | 2025-05-08 | 0.0 | True | 0.026 | 3.529384 | 0.0 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_fut | ff_fut 2022-06 | 1.1899999999999977 | used |
| effr_fut | ff_fut 2022-07 | 1.6599999999999966 | used |
| effr_fut | ff_fut 2022-08 | 2.305000000000007 | used |
| effr_fut | ff_fut 2022-09 | 2.480000000000004 | used |
| effr_fut | ff_fut 2022-10 | 2.9000000000000057 | used |
| effr_fut | ff_fut 2022-11 | 3.3400000000000034 | used |
| effr_fut | ff_fut 2022-12 | 3.5450000000000017 | used |
| effr_fut | ff_fut 2023-01 | 3.6899999999999977 | used |
| effr_fut | ff_fut 2023-02 | 3.8900000000000006 | used |
| effr_fut | ff_fut 2023-03 | 3.9650000000000034 | used |
| effr_fut | ff_fut 2023-04 | 4.030000000000001 | used |
| effr_fut | ff_fut 2023-05 | 4.055000000000007 | used |
| effr_fut | ff_fut 2023-06 | 4.040000000000006 | used |
| effr_fut | ff_fut 2023-07 | 4.010000000000005 | used |
| effr_fut | ff_fut 2023-08 | 3.9650000000000034 | used |
| effr_fut | ff_fut 2023-09 | 3.9350000000000023 | used |
| effr_fut | ff_fut 2023-10 | 3.8799999999999955 | used |
| effr_fut | ff_fut 2023-11 | 3.805000000000007 | used |
| effr_fut | ff_fut 2023-12 | 3.7549999999999955 | used |
| effr_fut | ff_fut 2024-01 | 3.7249999999999943 | used |
| effr_fut | ff_fut 2024-02 | 3.6599999999999966 | used |
| effr_fut | ff_fut 2024-03 | 3.5450000000000017 | used |
| effr_fut | ff_fut 2024-04 | 3.5400000000000063 | used |

Replica notes: ff_fut 2022-10: no new parcel; re-solved parcel 3 (2022-09-21); ff_fut 2023-01: no new parcel; re-solved parcel 5 (2022-12-14); ff_fut 2023-04: no new parcel; re-solved parcel 7 (2023-03-22); ff_fut 2023-08: no new parcel; re-solved parcel 10 (2023-07-26); ff_fut 2023-10: no new parcel; re-solved parcel 11 (2023-09-20); ff_fut 2024-01: no new parcel; re-solved parcel 13 (2023-12-13); ff_fut 2024-04: no new parcel; re-solved parcel 15 (2024-03-20)

## Curve `effr_ois` (ois_effr)

Fit: 18 quotes (0 dropped, 0 excluded by metadata), 3 IRLS iterations (converged); 26 parcels to 2025-06-25, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 0.8728 (replica 0.8300; stub prior 0.8300 from anchor + spread (D7)). WIRP replica reaches 8 meetings on 13 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2022-06-15 | False | False | 1.557659 | 0.684855 | 2.7394 | 273.94 | 1.560795 | -0.314 | 1.602659 | 72.766 | False | 0.002 | False |
| 2022-07-27 | False | False | 2.292056 | 1.419253 | 5.677 | 293.76 | 2.289463 | 0.259 | 2.337056 | 146.206 | False | 0.008 | False |
| 2022-09-21 | False | False | 2.868002 | 1.995198 | 7.9808 | 230.38 | 2.868374 | -0.037 | 2.913002 | 203.8 | False | 0.023 | False |
| 2022-11-02 | False | False | 3.340402 | 2.467598 | 9.8704 | 188.96 | 3.348467 | -0.806 | 3.385402 | 251.04 | False | 0.031 | False |
| 2022-12-14 | False | False | 3.678401 | 2.805597 | 11.2224 | 135.2 | 3.667479 | 1.092 | 3.723401 | 284.84 | False | 0.034 | False |
| 2023-02-01 | False | False | 3.890834 | 3.01803 | 12.0721 | 84.97 | 3.892006 | -0.117 | 3.935834 | 306.083 | False | 0.046 | False |
| 2023-03-22 | False | False | 4.053316 | 3.180513 | 12.7221 | 64.99 | 4.071269 | -1.795 | 4.098316 | 322.332 | False | 0.062 | False |
| 2023-05-03 | False | False | 4.061122 | 3.188318 | 12.7533 | 3.12 | 4.049594 | 1.153 | 4.106122 | 323.112 | False | 0.066 | False |
| 2023-06-14 | False | False | 4.011077 | 3.138273 | 12.5531 | -20.02 |  |  | 4.056077 | 318.108 | False | 0.296 | True |
| 2023-07-26 | False | False | 3.932257 | 3.059453 | 12.2378 | -31.53 |  |  | 3.977257 | 310.226 | True | 0.103 | True |
| 2023-09-20 | False | False | 3.853438 | 2.980634 | 11.9225 | -31.53 |  |  | 3.898438 | 302.344 | True | 0.094 | True |
| 2023-11-01 | False | False | 3.774621 | 2.901817 | 11.6073 | -31.53 |  |  | 3.819621 | 294.462 | True | 0.285 | True |
| 2023-12-13 | False | False | 3.695805 | 2.823002 | 11.292 | -31.53 |  |  | 3.740805 | 286.581 | True | 0.477 | True |
| 2024-01-31 | False | False | 3.62227 | 2.749467 | 10.9979 | -29.41 |  |  | 3.66727 | 279.227 | True | 0.163 | True |
| 2024-03-20 | False | False | 3.548736 | 2.675932 | 10.7037 | -29.41 |  |  | 3.593736 | 271.874 | True | 0.157 | True |
| 2024-05-01 | False | False | 3.475202 | 2.602398 | 10.4096 | -29.41 |  |  | 3.520202 | 264.52 | True | 0.47 | True |
| 2024-06-12 | False | False | 3.401668 | 2.528865 | 10.1155 | -29.41 |  |  | 3.446668 | 257.167 | True | 0.785 | True |
| 2024-07-31 | False | False | 3.366088 | 2.493285 | 9.9731 | -14.23 |  |  | 3.411088 | 253.609 | True | 0.557 | True |
| 2024-09-18 | False | False | 3.330519 | 2.457715 | 9.8309 | -14.23 |  |  | 3.375519 | 250.052 | True | 0.33 | True |
| 2024-11-07 | False | False | 3.294968 | 2.422165 | 9.6887 | -14.22 |  |  | 3.339968 | 246.497 | True | 0.105 | True |
| 2024-12-18 | False | False | 3.259439 | 2.386636 | 9.5465 | -14.21 |  |  | 3.304439 | 242.944 | True | 0.132 | True |
| 2025-01-29 | False | False | 3.223931 | 2.351128 | 9.4045 | -14.2 |  |  | 3.268931 | 239.393 | True | 0.358 | True |
| 2025-03-19 | False | False | 3.188442 | 2.315639 | 9.2626 | -14.2 |  |  | 3.233442 | 235.844 | True | 0.586 | True |
| 2025-05-07 | False | False | 3.152964 | 2.28016 | 9.1206 | -14.19 |  |  | 3.197964 | 232.296 | True | 0.815 | True |
| 2025-06-18 | False | False | 3.152964 | 2.28016 | 9.1206 | 0.0 |  |  | 3.197964 | 232.296 | True | 0.815 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | used | 18 | 0.0 | 0.106 | 0.314 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

_none_

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | 1Y | USSO1 Curncy | 3.2588 | 0.03 | 0.651 | 0.954 |
| effr_ois | ois_effr | 18M | USSO1F Curncy | 3.481 | -0.0 | -0.023 | 0.998 |
| effr_ois | ois_effr | 2Y | USSO2 Curncy | 3.5302 | 0.0 | 0.364 | 0.999 |
| effr_ois | ois_effr | 3Y | USSO3 Curncy | 3.4673 | -0.001 | -6.385 | 1.0 |

### Stale and outside-listing inputs

_none_

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2022-06-14 | 0.0 | True | 0.243 | 0.872803 |  | 0.83 | 4.28 |
| 2022-06-15 | 2022-06-16 | 1.0 | False | 0.002 | 1.557659 | 68.486 | 1.560795 | -0.314 |
| 2022-07-27 | 2022-07-28 | 1.0 | False | 0.008 | 2.292056 | 73.44 | 2.289463 | 0.259 |
| 2022-09-21 | 2022-09-22 | 1.0 | False | 0.023 | 2.868002 | 57.595 | 2.868374 | -0.037 |
| 2022-11-02 | 2022-11-03 | 1.0 | False | 0.031 | 3.340402 | 47.24 | 3.348467 | -0.806 |
| 2022-12-14 | 2022-12-15 | 1.0 | False | 0.034 | 3.678401 | 33.8 | 3.667479 | 1.092 |
| 2023-02-01 | 2023-02-02 | 1.0 | False | 0.046 | 3.890834 | 21.243 | 3.892006 | -0.117 |
| 2023-03-22 | 2023-03-23 | 1.0 | False | 0.062 | 4.053316 | 16.248 | 4.071269 | -1.795 |
| 2023-05-03 | 2023-05-04 | 1.0 | False | 0.066 | 4.061122 | 0.781 | 4.049594 | 1.153 |
| 2023-06-14 | 2023-06-15 | 1.0 | False | 0.296 | 4.011077 | -5.005 |  |  |
| 2023-07-26 | 2023-07-27 | 0.4697 | True | 0.103 | 3.932257 | -7.882 |  |  |
| 2023-09-20 | 2023-09-21 | 0.2642 | True | 0.094 | 3.853438 | -7.882 |  |  |
| 2023-11-01 | 2023-11-02 | 0.2642 | True | 0.285 | 3.774621 | -7.882 |  |  |
| 2023-12-13 | 2023-12-14 | 0.2555 | True | 0.477 | 3.695805 | -7.882 |  |  |
| 2024-01-31 | 2024-02-01 | 0.3015 | True | 0.163 | 3.62227 | -7.354 |  |  |
| 2024-03-20 | 2024-03-21 | 0.2215 | True | 0.157 | 3.548736 | -7.353 |  |  |
| 2024-05-01 | 2024-05-02 | 0.2215 | True | 0.47 | 3.475202 | -7.353 |  |  |
| 2024-06-12 | 2024-06-13 | 0.1228 | True | 0.785 | 3.401668 | -7.353 |  |  |
| 2024-07-31 | 2024-08-01 | 0.1439 | True | 0.557 | 3.366088 | -3.558 |  |  |
| 2024-09-18 | 2024-09-19 | 0.1498 | True | 0.33 | 3.330519 | -3.557 |  |  |
| 2024-11-07 | 2024-11-08 | 0.1007 | True | 0.105 | 3.294968 | -3.555 |  |  |
| 2024-12-18 | 2024-12-19 | 0.1057 | True | 0.132 | 3.259439 | -3.553 |  |  |
| 2025-01-29 | 2025-01-30 | 0.1439 | True | 0.358 | 3.223931 | -3.551 |  |  |
| 2025-03-19 | 2025-03-20 | 0.1439 | True | 0.586 | 3.188442 | -3.549 |  |  |
| 2025-05-07 | 2025-05-08 | 0.0911 | True | 0.815 | 3.152964 | -3.548 |  |  |
| 2025-06-18 | 2025-06-20 | 0.0 | True | 0.815 | 3.152964 | 0.0 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_ois | ois_effr 1W | 1.556 | used |
| effr_ois | ois_effr 1M | 1.5618 | used |
| effr_ois | ois_effr 2M | 1.789 | used |
| effr_ois | ois_effr 3M | 1.9616 | used |
| effr_ois | ois_effr 4M | 2.16615 | used |
| effr_ois | ois_effr 5M | 2.34915 | used |
| effr_ois | ois_effr 6M | 2.5197 | used |
| effr_ois | ois_effr 7M | 2.6999 | used |
| effr_ois | ois_effr 8M | 2.8403 | used |
| effr_ois | ois_effr 9M | 2.9556 | used |
| effr_ois | ois_effr 10M | 3.07875 | used |
| effr_ois | ois_effr 11M | 3.1715 | used |
| effr_ois | ois_effr 1Y | 3.2588 | used |

Replica notes: ois_effr 1M: no new parcel; re-solved parcel 1 (2022-06-15); ois_effr 3M: no new parcel; re-solved parcel 2 (2022-07-27); ois_effr 6M: no new parcel; re-solved parcel 4 (2022-11-02); ois_effr 9M: no new parcel; re-solved parcel 6 (2023-02-01); ois_effr 1Y: no new parcel; re-solved parcel 8 (2023-05-03); stub parcel not priced by any instrument (the first one starts after the next effective date): set to the last fixing 0.8300 (2022-06-13)

## FF / OIS basis (bp, fit and replica)

| decision_date | effective_date | parcel | effr_fut_fit | effr_ois_fit | basis_fit_bp | basis_replica_bp |
| --- | --- | --- | --- | --- | --- | --- |
| None | None | stub | 0.7372867298686193 | 0.872803448272102 | -13.552 | -10.833 |
| 2022-06-15 | 2022-06-16 | 1 | 1.564094 | 1.557659 | 0.644 | 0.365 |
| 2022-07-27 | 2022-07-28 | 2 | 2.303489 | 2.292056 | 1.143 | 1.554 |
| 2022-09-21 | 2022-09-22 | 3 | 2.899346 | 2.868002 | 3.134 | 3.163 |
| 2022-11-02 | 2022-11-03 | 4 | 3.371106 | 3.340402 | 3.07 | 2.296 |
| 2022-12-14 | 2022-12-15 | 5 | 3.68949 | 3.678401 | 1.109 | 2.252 |
| 2023-02-01 | 2023-02-02 | 6 | 3.900957 | 3.890834 | 1.012 | 0.54 |
| 2023-03-22 | 2023-03-23 | 7 | 4.031904 | 4.053316 | -2.141 | -4.127 |
| 2023-05-03 | 2023-05-04 | 8 | 4.057854 | 4.061122 | -0.327 | 0.808 |
| 2023-06-14 | 2023-06-15 | 9 | 4.019521 | 4.011077 | 0.844 |  |
| 2023-07-26 | 2023-07-27 | 10 | 3.964388 | 3.932257 | 3.213 |  |
| 2023-09-20 | 2023-09-21 | 11 | 3.879559 | 3.853438 | 2.612 |  |
| 2023-11-01 | 2023-11-02 | 12 | 3.801703 | 3.774621 | 2.708 |  |
| 2023-12-13 | 2023-12-14 | 13 | 3.724057 | 3.695805 | 2.825 |  |
| 2024-01-31 | 2024-02-01 | 14 | 3.640583 | 3.62227 | 1.831 |  |
| 2024-03-20 | 2024-03-21 | 15 | 3.529384 | 3.548736 | -1.935 |  |
| 2024-05-01 | 2024-05-02 | 16 | 3.529384 | 3.475202 | 5.418 |  |
| 2024-06-12 | 2024-06-13 | 17 | 3.529384 | 3.401668 | 12.772 |  |
| 2024-07-31 | 2024-08-01 | 18 | 3.529384 | 3.366088 | 16.33 |  |
| 2024-09-18 | 2024-09-19 | 19 | 3.529384 | 3.330519 | 19.886 |  |
| 2024-11-07 | 2024-11-08 | 20 | 3.529384 | 3.294968 | 23.442 |  |
| 2024-12-18 | 2024-12-19 | 21 | 3.529384 | 3.259439 | 26.994 |  |
| 2025-01-29 | 2025-01-30 | 22 | 3.529384 | 3.223931 | 30.545 |  |
| 2025-03-19 | 2025-03-20 | 23 | 3.529384 | 3.188442 | 34.094 |  |
| 2025-05-07 | 2025-05-08 | 24 | 3.529384 | 3.152964 | 37.642 |  |

## Stub

| curve | as_of | current_implied | replica_current_implied | stub_prior | stub_prior_source | anchor | spread | spread_median | spread_winsorised_mean | spread_obs | spread_estimator | spread_note | wirp_reach_meetings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | 2022-06-14 | 0.737287 | 0.721667 | 0.83 | anchor + spread (D7) | 0.875 | -0.045000000000000005 | -0.044999999999999984 | -0.045000000000000005 | 60 | winsorised_mean |  | 15 |
| effr_ois | 2022-06-14 | 0.872803 | 0.83 | 0.83 | anchor + spread (D7) | 0.875 | -0.045000000000000005 | -0.044999999999999984 | -0.045000000000000005 | 60 | winsorised_mean |  | 8 |
