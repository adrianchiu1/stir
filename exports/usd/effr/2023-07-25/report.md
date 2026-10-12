# USD EFFR front end, 2023-07-25

Anchor (target_midpoint) in effect: 5.125. Policy spread (winsorised_mean, D7): -4.67bp (winsorised mean -4.67bp, median -4.50bp; 60 fixings, 3 turn days dropped, window 2023-04-24..2023-07-24) **Loader reported blocking problems in the window (see check_market_data.py).**

## Curve `effr_fut` (ff_fut)

Fit: 20 quotes (0 dropped, 17 excluded by metadata), 2 IRLS iterations (converged); 25 parcels to 2026-07-25, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 5.0942 (replica 5.0925; stub prior 5.0783 from anchor + spread (D7)). WIRP replica reaches 13 meetings on 20 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-07-26 | False | False | 5.324279 | 0.230115 | 0.9205 | 92.05 | 5.325 | -0.072 | 5.370945 | 24.595 | False | 0.004 | False |
| 2023-09-20 | False | False | 5.374675 | 0.280511 | 1.122 | 20.16 | 5.375 | -0.033 | 5.421341 | 29.634 | False | 0.005 | False |
| 2023-11-01 | False | False | 5.441213 | 0.347049 | 1.3882 | 26.62 | 5.442241 | -0.103 | 5.48788 | 36.288 | False | 0.005 | False |
| 2023-12-13 | False | False | 5.408658 | 0.314494 | 1.258 | -13.02 | 5.41 | -0.134 | 5.455324 | 33.032 | False | 0.004 | False |
| 2024-01-31 | False | False | 5.334287 | 0.240123 | 0.9605 | -29.75 | 5.335 | -0.071 | 5.380954 | 25.595 | False | 0.005 | False |
| 2024-03-20 | False | False | 5.204448 | 0.110284 | 0.4411 | -51.94 | 5.205 | -0.055 | 5.251114 | 12.611 | False | 0.006 | False |
| 2024-05-01 | False | False | 5.049906 | -0.044258 | -0.177 | -61.82 | 5.05 | -0.009 | 5.096573 | -2.843 | False | 0.008 | False |
| 2024-06-12 | False | False | 4.869704 | -0.22446 | -0.8978 | -72.08 | 4.87 | -0.03 | 4.916371 | -20.863 | False | 0.01 | False |
| 2024-07-31 | False | False | 4.69001 | -0.404154 | -1.6166 | -71.88 | 4.69 | 0.001 | 4.736676 | -38.832 | False | 0.013 | False |
| 2024-09-18 | False | False | 4.489843 | -0.604321 | -2.4173 | -80.07 | 4.49 | -0.016 | 4.53651 | -58.849 | False | 0.021 | False |
| 2024-11-07 | False | False | 4.282334 | -0.81183 | -3.2473 | -83.0 | 4.281304 | 0.103 | 4.329 | -79.6 | False | 0.024 | False |
| 2024-12-18 | False | False | 4.143386 | -0.950778 | -3.8031 | -55.58 | 4.14704 | -0.365 | 4.190052 | -93.495 | False | 0.023 | False |
| 2025-01-29 | False | False | 4.020034 | -1.07413 | -4.2965 | -49.34 | 4.02 | 0.003 | 4.066701 | -105.83 | False | 0.022 | False |
| 2025-03-19 | False | False | 4.020034 | -1.07413 | -4.2965 | 0.0 |  |  | 4.066701 | -105.83 | True | 0.023 | True |
| 2025-05-07 | False | False | 4.020034 | -1.07413 | -4.2965 | 0.0 |  |  | 4.066701 | -105.83 | True | 0.023 | True |
| 2025-06-18 | False | False | 4.020034 | -1.07413 | -4.2965 | 0.0 |  |  | 4.066701 | -105.83 | True | 0.024 | True |
| 2025-07-30 | False | False | 4.020034 | -1.07413 | -4.2965 | 0.0 |  |  | 4.066701 | -105.83 | True | 0.024 | True |
| 2025-09-17 | False | False | 4.020034 | -1.07413 | -4.2965 | 0.0 |  |  | 4.066701 | -105.83 | True | 0.025 | True |
| 2025-10-29 | False | False | 4.020034 | -1.07413 | -4.2965 | 0.0 |  |  | 4.066701 | -105.83 | True | 0.025 | True |
| 2025-12-10 | False | False | 4.020034 | -1.07413 | -4.2965 | 0.0 |  |  | 4.066701 | -105.83 | True | 0.026 | True |
| 2026-01-28 | False | False | 4.020034 | -1.07413 | -4.2965 | 0.0 |  |  | 4.066701 | -105.83 | True | 0.026 | True |
| 2026-03-18 | False | False | 4.020034 | -1.07413 | -4.2965 | 0.0 |  |  | 4.066701 | -105.83 | True | 0.027 | True |
| 2026-04-29 | False | False | 4.020034 | -1.07413 | -4.2965 | 0.0 |  |  | 4.066701 | -105.83 | True | 0.027 | True |
| 2026-06-17 | False | False | 4.020034 | -1.07413 | -4.2965 | 0.0 |  |  | 4.066701 | -105.83 | True | 0.028 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | used | 20 | -0.017 | 0.114 | 0.321 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

| curve | instrument | contract | ticker | status | reason | residual_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2025-03 | FFH25 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2025-04 | FFJ25 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2025-05 | FFK25 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2025-06 | FFM25 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2025-07 | FFN25 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2025-08 | FFQ25 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2025-09 | FFU25 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2025-10 | FFV25 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2025-11 | FFX25 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2025-12 | FFZ25 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2026-01 | FFF26 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2026-02 | FFG26 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2026-03 | FFH26 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2026-04 | FFJ26 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2026-05 | FFK26 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2026-06 | FFM26 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2026-07 | FFN26 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2023-07 | FFN23 Comdty | 5.12 | 0.001 | 0.01 | 0.908 |
| effr_fut | ff_fut | 2023-10 | FFV23 Comdty | 5.375 | 0.033 | 0.454 | 0.928 |
| effr_fut | ff_fut | 2024-04 | FFJ24 Comdty | 5.205 | 0.055 | 1.087 | 0.949 |
| effr_fut | ff_fut | 2024-05 | FFK24 Comdty | 5.055 | 0.011 | 0.49 | 0.978 |
| effr_fut | ff_fut | 2024-07 | FFN24 Comdty | 4.87 | 0.03 | 0.334 | 0.911 |
| effr_fut | ff_fut | 2025-02 | FFG25 Comdty | 4.02 | -0.003 | -3.314 | 0.999 |

### Stale and outside-listing inputs

_none_

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2023-07-25 | 1.0 | False | 0.074 | 5.094164 |  | 5.0925 | 0.166 |
| 2023-07-26 | 2023-07-27 | 1.0 | False | 0.004 | 5.324279 | 23.011 | 5.325 | -0.072 |
| 2023-09-20 | 2023-09-21 | 1.0 | False | 0.005 | 5.374675 | 5.04 | 5.375 | -0.033 |
| 2023-11-01 | 2023-11-02 | 1.0 | False | 0.005 | 5.441213 | 6.654 | 5.442241 | -0.103 |
| 2023-12-13 | 2023-12-14 | 1.0 | False | 0.004 | 5.408658 | -3.256 | 5.41 | -0.134 |
| 2024-01-31 | 2024-02-01 | 1.0 | False | 0.005 | 5.334287 | -7.437 | 5.335 | -0.071 |
| 2024-03-20 | 2024-03-21 | 1.0 | False | 0.006 | 5.204448 | -12.984 | 5.205 | -0.055 |
| 2024-05-01 | 2024-05-02 | 1.0 | False | 0.008 | 5.049906 | -15.454 | 5.05 | -0.009 |
| 2024-06-12 | 2024-06-13 | 1.0 | False | 0.01 | 4.869704 | -18.02 | 4.87 | -0.03 |
| 2024-07-31 | 2024-08-01 | 1.0 | False | 0.013 | 4.69001 | -17.969 | 4.69 | 0.001 |
| 2024-09-18 | 2024-09-19 | 1.0 | False | 0.021 | 4.489843 | -20.017 | 4.49 | -0.016 |
| 2024-11-07 | 2024-11-08 | 1.0 | False | 0.024 | 4.282334 | -20.751 | 4.281304 | 0.103 |
| 2024-12-18 | 2024-12-19 | 1.0 | False | 0.023 | 4.143386 | -13.895 | 4.14704 | -0.365 |
| 2025-01-29 | 2025-01-30 | 1.0 | False | 0.022 | 4.020034 | -12.335 | 4.02 | 0.003 |
| 2025-03-19 | 2025-03-20 | 0.0 | True | 0.023 | 4.020034 | 0.0 |  |  |
| 2025-05-07 | 2025-05-08 | 0.0 | True | 0.023 | 4.020034 | 0.0 |  |  |
| 2025-06-18 | 2025-06-20 | 0.0 | True | 0.024 | 4.020034 | 0.0 |  |  |
| 2025-07-30 | 2025-07-31 | 0.0 | True | 0.024 | 4.020034 | 0.0 |  |  |
| 2025-09-17 | 2025-09-18 | 0.0 | True | 0.025 | 4.020034 | 0.0 |  |  |
| 2025-10-29 | 2025-10-30 | 0.0 | True | 0.025 | 4.020034 | 0.0 |  |  |
| 2025-12-10 | 2025-12-11 | 0.0 | True | 0.026 | 4.020034 | 0.0 |  |  |
| 2026-01-28 | 2026-01-29 | 0.0 | True | 0.026 | 4.020034 | 0.0 |  |  |
| 2026-03-18 | 2026-03-19 | 0.0 | True | 0.027 | 4.020034 | 0.0 |  |  |
| 2026-04-29 | 2026-04-30 | 0.0 | True | 0.027 | 4.020034 | 0.0 |  |  |
| 2026-06-17 | 2026-06-18 | 0.0 | True | 0.028 | 4.020034 | 0.0 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_fut | ff_fut 2023-07 | 5.1200000000000045 | used |
| effr_fut | ff_fut 2023-08 | 5.325000000000003 | used |
| effr_fut | ff_fut 2023-09 | 5.340000000000003 | used |
| effr_fut | ff_fut 2023-10 | 5.375 | used |
| effr_fut | ff_fut 2023-11 | 5.439999999999998 | used |
| effr_fut | ff_fut 2023-12 | 5.420000000000002 | used |
| effr_fut | ff_fut 2024-01 | 5.409999999999997 | used |
| effr_fut | ff_fut 2024-02 | 5.334999999999994 | used |
| effr_fut | ff_fut 2024-03 | 5.284999999999997 | used |
| effr_fut | ff_fut 2024-04 | 5.204999999999998 | used |
| effr_fut | ff_fut 2024-05 | 5.055000000000007 | used |
| effr_fut | ff_fut 2024-06 | 4.939999999999998 | used |
| effr_fut | ff_fut 2024-07 | 4.8700000000000045 | used |
| effr_fut | ff_fut 2024-08 | 4.689999999999998 | used |
| effr_fut | ff_fut 2024-09 | 4.609999999999999 | used |
| effr_fut | ff_fut 2024-10 | 4.489999999999995 | used |
| effr_fut | ff_fut 2024-11 | 4.329999999999998 | used |
| effr_fut | ff_fut 2024-12 | 4.224999999999994 | used |
| effr_fut | ff_fut 2025-01 | 4.135000000000005 | used |
| effr_fut | ff_fut 2025-02 | 4.019999999999996 | used |

Replica notes: ff_fut 2023-10: no new parcel; re-solved parcel 2 (2023-09-20); ff_fut 2024-01: no new parcel; re-solved parcel 4 (2023-12-13); ff_fut 2024-04: no new parcel; re-solved parcel 6 (2024-03-20); ff_fut 2024-07: no new parcel; re-solved parcel 8 (2024-06-12); ff_fut 2024-10: no new parcel; re-solved parcel 10 (2024-09-18); ff_fut 2025-02: no new parcel; re-solved parcel 13 (2025-01-29)

## Curve `effr_ois` (ois_effr)

Fit: 18 quotes (0 dropped, 0 excluded by metadata), 3 IRLS iterations (converged); 26 parcels to 2026-08-05, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 5.0928 (replica 5.0800; stub prior 5.0783 from anchor + spread (D7)). WIRP replica reaches 8 meetings on 13 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-07-26 | False | False | 5.323653 | 0.230889 | 0.9236 | 92.36 | 5.322903 | 0.075 | 5.37032 | 24.532 | False | 0.002 | False |
| 2023-09-20 | False | False | 5.371906 | 0.279142 | 1.1166 | 19.3 | 5.373381 | -0.148 | 5.418572 | 29.357 | False | 0.013 | False |
| 2023-11-01 | False | False | 5.438714 | 0.34595 | 1.3838 | 26.72 | 5.437185 | 0.153 | 5.485381 | 36.038 | False | 0.024 | False |
| 2023-12-13 | False | False | 5.400192 | 0.307428 | 1.2297 | -15.41 | 5.40068 | -0.049 | 5.446858 | 32.186 | False | 0.027 | False |
| 2024-01-31 | False | False | 5.31913 | 0.226366 | 0.9055 | -32.42 | 5.303185 | 1.595 | 5.365797 | 24.08 | False | 0.033 | False |
| 2024-03-20 | False | False | 5.191369 | 0.098606 | 0.3944 | -51.1 | 5.212047 | -2.068 | 5.238036 | 11.304 | False | 0.047 | False |
| 2024-05-01 | False | False | 5.037602 | -0.055162 | -0.2206 | -61.51 | 5.035039 | 0.256 | 5.084269 | -4.073 | False | 0.059 | False |
| 2024-06-12 | False | False | 4.862733 | -0.230031 | -0.9201 | -69.95 | 4.863748 | -0.101 | 4.9094 | -21.56 | False | 0.058 | False |
| 2024-07-31 | False | False | 4.668809 | -0.423955 | -1.6958 | -77.57 |  |  | 4.715475 | -40.952 | True | 0.034 | True |
| 2024-09-18 | False | False | 4.474897 | -0.617867 | -2.4715 | -77.56 |  |  | 4.521564 | -60.344 | True | 0.018 | True |
| 2024-11-07 | False | False | 4.281002 | -0.811762 | -3.247 | -77.56 |  |  | 4.327669 | -79.733 | True | 0.033 | True |
| 2024-12-18 | False | False | 4.08712 | -1.005644 | -4.0226 | -77.55 |  |  | 4.133787 | -99.121 | True | 0.065 | True |
| 2025-01-29 | False | False | 3.972907 | -1.119856 | -4.4794 | -45.68 |  |  | 4.019574 | -110.543 | True | 0.039 | True |
| 2025-03-19 | False | False | 3.858707 | -1.234057 | -4.9362 | -45.68 |  |  | 3.905374 | -121.963 | True | 0.024 | True |
| 2025-05-07 | False | False | 3.744523 | -1.348241 | -5.393 | -45.67 |  |  | 3.79119 | -133.381 | True | 0.04 | True |
| 2025-06-18 | False | False | 3.630351 | -1.462413 | -5.8497 | -45.67 |  |  | 3.677017 | -144.798 | True | 0.072 | True |
| 2025-07-30 | False | False | 3.592264 | -1.5005 | -6.002 | -15.23 |  |  | 3.638931 | -148.607 | True | 0.059 | True |
| 2025-09-17 | False | False | 3.554189 | -1.538575 | -6.1543 | -15.23 |  |  | 3.600856 | -152.414 | True | 0.051 | True |
| 2025-10-29 | False | False | 3.516135 | -1.576629 | -6.3065 | -15.22 |  |  | 3.562802 | -156.22 | True | 0.042 | True |
| 2025-12-10 | False | False | 3.478106 | -1.614658 | -6.4586 | -15.21 |  |  | 3.524773 | -160.023 | True | 0.034 | True |
| 2026-01-28 | False | False | 3.440105 | -1.652658 | -6.6106 | -15.2 |  |  | 3.486772 | -163.823 | True | 0.032 | True |
| 2026-03-18 | False | False | 3.402131 | -1.690633 | -6.7625 | -15.19 |  |  | 3.448797 | -167.62 | True | 0.045 | True |
| 2026-04-29 | False | False | 3.364177 | -1.728587 | -6.9143 | -15.18 |  |  | 3.410843 | -171.416 | True | 0.071 | True |
| 2026-06-17 | False | False | 3.326235 | -1.766529 | -7.0661 | -15.18 |  |  | 3.372902 | -175.21 | True | 0.106 | True |
| 2026-07-29 | False | False | 3.326235 | -1.766529 | -7.0661 | 0.0 |  |  | 3.372902 | -175.21 | True | 0.106 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | used | 18 | 0.0 | 0.026 | 0.075 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

_none_

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | 9M | USSOI Curncy | 5.45305 | 0.002 | 0.022 | 0.917 |
| effr_ois | ois_effr | 1Y | USSO1 Curncy | 5.38897 | 0.002 | 0.03 | 0.945 |
| effr_ois | ois_effr | 18M | USSO1F Curncy | 5.0767 | -0.0 | -0.016 | 0.998 |
| effr_ois | ois_effr | 2Y | USSO2 Curncy | 4.8095 | -0.0 | -0.384 | 0.999 |
| effr_ois | ois_effr | 3Y | USSO3 Curncy | 4.3982 | -0.001 | -5.622 | 1.0 |

### Stale and outside-listing inputs

_none_

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2023-07-25 | 0.0 | True | 0.243 | 5.092764 |  | 5.08 | 1.276 |
| 2023-07-26 | 2023-07-27 | 1.0 | False | 0.002 | 5.323653 | 23.089 | 5.322903 | 0.075 |
| 2023-09-20 | 2023-09-21 | 1.0 | False | 0.013 | 5.371906 | 4.825 | 5.373381 | -0.148 |
| 2023-11-01 | 2023-11-02 | 1.0 | False | 0.024 | 5.438714 | 6.681 | 5.437185 | 0.153 |
| 2023-12-13 | 2023-12-14 | 1.0 | False | 0.027 | 5.400192 | -3.852 | 5.40068 | -0.049 |
| 2024-01-31 | 2024-02-01 | 1.0 | False | 0.033 | 5.31913 | -8.106 | 5.303185 | 1.595 |
| 2024-03-20 | 2024-03-21 | 1.0 | False | 0.047 | 5.191369 | -12.776 | 5.212047 | -2.068 |
| 2024-05-01 | 2024-05-02 | 1.0 | False | 0.059 | 5.037602 | -15.377 | 5.035039 | 0.256 |
| 2024-06-12 | 2024-06-13 | 1.0 | False | 0.058 | 4.862733 | -17.487 | 4.863748 | -0.101 |
| 2024-07-31 | 2024-08-01 | 0.2964 | True | 0.034 | 4.668809 | -19.392 |  |  |
| 2024-09-18 | 2024-09-19 | 0.3086 | True | 0.018 | 4.474897 | -19.391 |  |  |
| 2024-11-07 | 2024-11-08 | 0.2075 | True | 0.033 | 4.281002 | -19.389 |  |  |
| 2024-12-18 | 2024-12-19 | 0.1885 | True | 0.065 | 4.08712 | -19.388 |  |  |
| 2025-01-29 | 2025-01-30 | 0.2963 | True | 0.039 | 3.972907 | -11.421 |  |  |
| 2025-03-19 | 2025-03-20 | 0.2963 | True | 0.024 | 3.858707 | -11.42 |  |  |
| 2025-05-07 | 2025-05-08 | 0.2282 | True | 0.04 | 3.744523 | -11.418 |  |  |
| 2025-06-18 | 2025-06-20 | 0.1787 | True | 0.072 | 3.630351 | -11.417 |  |  |
| 2025-07-30 | 2025-07-31 | 0.1462 | True | 0.059 | 3.592264 | -3.809 |  |  |
| 2025-09-17 | 2025-09-18 | 0.1074 | True | 0.051 | 3.554189 | -3.807 |  |  |
| 2025-10-29 | 2025-10-30 | 0.1074 | True | 0.042 | 3.516135 | -3.805 |  |  |
| 2025-12-10 | 2025-12-11 | 0.1462 | True | 0.034 | 3.478106 | -3.803 |  |  |
| 2026-01-28 | 2026-01-29 | 0.1462 | True | 0.032 | 3.440105 | -3.8 |  |  |
| 2026-03-18 | 2026-03-19 | 0.1074 | True | 0.045 | 3.402131 | -3.797 |  |  |
| 2026-04-29 | 2026-04-30 | 0.1462 | True | 0.071 | 3.364177 | -3.795 |  |  |
| 2026-06-17 | 2026-06-18 | 0.0927 | True | 0.106 | 3.326235 | -3.794 |  |  |
| 2026-07-29 | 2026-07-30 | 0.0 | True | 0.106 | 3.326235 | 0.0 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_ois | ois_effr 1W | 5.326 | used |
| effr_ois | ois_effr 1M | 5.33475 | used |
| effr_ois | ois_effr 2M | 5.35175 | used |
| effr_ois | ois_effr 3M | 5.3785 | used |
| effr_ois | ois_effr 4M | 5.412 | used |
| effr_ois | ois_effr 5M | 5.4362 | used |
| effr_ois | ois_effr 6M | 5.45395 | used |
| effr_ois | ois_effr 7M | 5.45887 | used |
| effr_ois | ois_effr 8M | 5.4607 | used |
| effr_ois | ois_effr 9M | 5.45305 | used |
| effr_ois | ois_effr 10M | 5.43621 | used |
| effr_ois | ois_effr 11M | 5.41467 | used |
| effr_ois | ois_effr 1Y | 5.38897 | used |

Replica notes: ois_effr 1M: no new parcel; re-solved parcel 1 (2023-07-26); ois_effr 3M: no new parcel; re-solved parcel 2 (2023-09-20); ois_effr 6M: no new parcel; re-solved parcel 4 (2023-12-13); ois_effr 8M: no new parcel; re-solved parcel 5 (2024-01-31); ois_effr 1Y: no new parcel; re-solved parcel 8 (2024-06-12); stub parcel not priced by any instrument (the first one starts after the next effective date): set to the last fixing 5.0800 (2023-07-24)

## FF / OIS basis (bp, fit and replica)

| decision_date | effective_date | parcel | effr_fut_fit | effr_ois_fit | basis_fit_bp | basis_replica_bp |
| --- | --- | --- | --- | --- | --- | --- |
| None | None | stub | 5.094164049626329 | 5.092763897729468 | 0.14 | 1.25 |
| 2023-07-26 | 2023-07-27 | 1 | 5.324279 | 5.323653 | 0.063 | 0.21 |
| 2023-09-20 | 2023-09-21 | 2 | 5.374675 | 5.371906 | 0.277 | 0.162 |
| 2023-11-01 | 2023-11-02 | 3 | 5.441213 | 5.438714 | 0.25 | 0.506 |
| 2023-12-13 | 2023-12-14 | 4 | 5.408658 | 5.400192 | 0.847 | 0.932 |
| 2024-01-31 | 2024-02-01 | 5 | 5.334287 | 5.31913 | 1.516 | 3.181 |
| 2024-03-20 | 2024-03-21 | 6 | 5.204448 | 5.191369 | 1.308 | -0.705 |
| 2024-05-01 | 2024-05-02 | 7 | 5.049906 | 5.037602 | 1.23 | 1.496 |
| 2024-06-12 | 2024-06-13 | 8 | 4.869704 | 4.862733 | 0.697 | 0.625 |
| 2024-07-31 | 2024-08-01 | 9 | 4.69001 | 4.668809 | 2.12 |  |
| 2024-09-18 | 2024-09-19 | 10 | 4.489843 | 4.474897 | 1.495 |  |
| 2024-11-07 | 2024-11-08 | 11 | 4.282334 | 4.281002 | 0.133 |  |
| 2024-12-18 | 2024-12-19 | 12 | 4.143386 | 4.08712 | 5.627 |  |
| 2025-01-29 | 2025-01-30 | 13 | 4.020034 | 3.972907 | 4.713 |  |
| 2025-03-19 | 2025-03-20 | 14 | 4.020034 | 3.858707 | 16.133 |  |
| 2025-05-07 | 2025-05-08 | 15 | 4.020034 | 3.744523 | 27.551 |  |
| 2025-06-18 | 2025-06-20 | 16 | 4.020034 | 3.630351 | 38.968 |  |
| 2025-07-30 | 2025-07-31 | 17 | 4.020034 | 3.592264 | 42.777 |  |
| 2025-09-17 | 2025-09-18 | 18 | 4.020034 | 3.554189 | 46.584 |  |
| 2025-10-29 | 2025-10-30 | 19 | 4.020034 | 3.516135 | 50.39 |  |
| 2025-12-10 | 2025-12-11 | 20 | 4.020034 | 3.478106 | 54.193 |  |
| 2026-01-28 | 2026-01-29 | 21 | 4.020034 | 3.440105 | 57.993 |  |
| 2026-03-18 | 2026-03-19 | 22 | 4.020034 | 3.402131 | 61.79 |  |
| 2026-04-29 | 2026-04-30 | 23 | 4.020034 | 3.364177 | 65.586 |  |
| 2026-06-17 | 2026-06-18 | 24 | 4.020034 | 3.326235 | 69.38 |  |

## Stub

| curve | as_of | current_implied | replica_current_implied | stub_prior | stub_prior_source | anchor | spread | spread_median | spread_winsorised_mean | spread_obs | spread_estimator | spread_note | wirp_reach_meetings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | 2023-07-25 | 5.094164 | 5.0925 | 5.078333 | anchor + spread (D7) | 5.125 | -0.04666666666666656 | -0.04499999999999993 | -0.04666666666666656 | 60 | winsorised_mean |  | 13 |
| effr_ois | 2023-07-25 | 5.092764 | 5.08 | 5.078333 | anchor + spread (D7) | 5.125 | -0.04666666666666656 | -0.04499999999999993 | -0.04666666666666656 | 60 | winsorised_mean |  | 8 |
