# USD EFFR front end, 2026-10-07

Anchor (target_midpoint) in effect: 3.875. Policy spread (winsorised_mean, D7): 0.50bp (winsorised mean 0.50bp, median 0.50bp; 60 fixings, 3 turn days dropped, window 2026-07-09..2026-10-06)

## Curve `effr_fut` (ff_fut)

Fit: 17 quotes (0 dropped, 20 excluded by metadata), 3 IRLS iterations (converged); 25 parcels to 2029-10-07, 14 synthetic and 0 unscheduled meetings. Current implied O/N rate 3.8808 (replica 3.8809; stub prior 3.8800 from anchor + spread (D7)). WIRP replica reaches 11 meetings on 17 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-10-28 | False | False | 3.926063 | 0.045297 | 0.1812 | 18.12 | 3.925 | 0.106 | 3.921063 | 4.606 | False | 0.005 | False |
| 2026-12-09 | False | False | 4.116696 | 0.235931 | 0.9437 | 76.25 | 4.122273 | -0.558 | 4.111696 | 23.67 | False | 0.005 | False |
| 2027-01-27 | False | False | 4.204069 | 0.323303 | 1.2932 | 34.95 | 4.205 | -0.093 | 4.199069 | 32.407 | False | 0.004 | False |
| 2027-03-17 | False | False | 4.36341 | 0.482644 | 1.9306 | 63.74 | 4.36 | 0.341 | 4.35841 | 48.341 | False | 0.005 | False |
| 2027-04-28 | False | False | 4.454955 | 0.574189 | 2.2968 | 36.62 | 4.455 | -0.005 | 4.449955 | 57.495 | False | 0.005 | False |
| 2027-06-09 | False | False | 4.555886 | 0.67512 | 2.7005 | 40.37 | 4.555 | 0.089 | 4.550886 | 67.589 | False | 0.006 | False |
| 2027-07-28 | False | False | 4.595392 | 0.714626 | 2.8585 | 15.8 | 4.595 | 0.039 | 4.590392 | 71.539 | False | 0.008 | False |
| 2027-09-15 | False | False | 4.640253 | 0.759487 | 3.0379 | 17.94 | 4.645 | -0.475 | 4.635253 | 76.025 | False | 0.015 | False |
| 2027-10-27 | False | False | 4.649111 | 0.768345 | 3.0734 | 3.54 | 4.65 | -0.089 | 4.644111 | 76.911 | False | 0.019 | False |
| 2027-12-08 | False | False | 4.647669 | 0.766904 | 3.0676 | -0.58 | 4.643261 | 0.441 | 4.642669 | 76.767 | False | 0.02 | False |
| 2028-01-26 | True | False | 4.645435 | 0.764669 | 3.0587 | -0.89 | 4.645 | 0.044 | 4.640435 | 76.544 | False | 0.022 | False |
| 2028-03-15 | True | False | 4.645435 | 0.764669 | 3.0587 | 0.0 |  |  | 4.640435 | 76.544 | True | 0.023 | True |
| 2028-04-26 | True | False | 4.645435 | 0.764669 | 3.0587 | 0.0 |  |  | 4.640435 | 76.544 | True | 0.023 | True |
| 2028-06-14 | True | False | 4.645435 | 0.764669 | 3.0587 | 0.0 |  |  | 4.640435 | 76.544 | True | 0.024 | True |
| 2028-07-26 | True | False | 4.645435 | 0.764669 | 3.0587 | 0.0 |  |  | 4.640435 | 76.544 | True | 0.024 | True |
| 2028-09-20 | True | False | 4.645435 | 0.764669 | 3.0587 | 0.0 |  |  | 4.640435 | 76.544 | True | 0.025 | True |
| 2028-10-25 | True | False | 4.645435 | 0.764669 | 3.0587 | 0.0 |  |  | 4.640435 | 76.544 | True | 0.025 | True |
| 2028-12-13 | True | False | 4.645435 | 0.764669 | 3.0587 | 0.0 |  |  | 4.640435 | 76.544 | True | 0.026 | True |
| 2029-01-24 | True | False | 4.645435 | 0.764669 | 3.0587 | 0.0 |  |  | 4.640435 | 76.544 | True | 0.026 | True |
| 2029-03-21 | True | False | 4.645435 | 0.764669 | 3.0587 | 0.0 |  |  | 4.640435 | 76.544 | True | 0.027 | True |
| 2029-04-25 | True | False | 4.645435 | 0.764669 | 3.0587 | 0.0 |  |  | 4.640435 | 76.544 | True | 0.027 | True |
| 2029-06-13 | True | False | 4.645435 | 0.764669 | 3.0587 | 0.0 |  |  | 4.640435 | 76.544 | True | 0.028 | True |
| 2029-07-25 | True | False | 4.645435 | 0.764669 | 3.0587 | 0.0 |  |  | 4.640435 | 76.544 | True | 0.028 | True |
| 2029-09-19 | True | False | 4.645435 | 0.764669 | 3.0587 | 0.0 |  |  | 4.640435 | 76.544 | True | 0.029 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | used | 17 | 0.001 | 0.172 | 0.365 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

| curve | instrument | contract | ticker | status | reason | residual_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2028-03 | FFH28 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2028-04 | FFJ28 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2028-05 | FFK28 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2028-06 | FFM28 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2028-07 | FFN28 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2028-08 | FFQ28 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2028-09 | FFU28 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2028-10 | FFV28 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2028-11 | FFX28 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2028-12 | FFZ28 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2029-01 | FFF29 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2029-02 | FFG29 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2029-03 | FFH29 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2029-04 | FFJ29 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2029-05 | FFK29 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2029-06 | FFM29 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2029-07 | FFN29 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2029-08 | FFQ29 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2029-09 | FFU29 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2029-10 | FFV29 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2026-10 | FFV26 Comdty | 3.885 | -0.0 | -0.138 | 0.999 |
| effr_fut | ff_fut | 2026-11 | FFX26 Comdty | 3.925 | -0.106 | -2.213 | 0.952 |
| effr_fut | ff_fut | 2027-05 | FFK27 Comdty | 4.455 | 0.005 | 0.161 | 0.972 |
| effr_fut | ff_fut | 2027-08 | FFQ27 Comdty | 4.595 | -0.039 | -0.676 | 0.942 |
| effr_fut | ff_fut | 2027-11 | FFX27 Comdty | 4.65 | 0.089 | 2.603 | 0.966 |
| effr_fut | ff_fut | 2028-02 | FFG28 Comdty | 4.645 | -0.044 | -3.749 | 0.988 |

### Stale and outside-listing inputs

_none_

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2026-10-07 | 1.0 | False | 0.007 | 3.880766 |  | 3.880909 | -0.014 |
| 2026-10-28 | 2026-10-29 | 1.0 | False | 0.005 | 3.926063 | 4.53 | 3.925 | 0.106 |
| 2026-12-09 | 2026-12-10 | 1.0 | False | 0.005 | 4.116696 | 19.063 | 4.122273 | -0.558 |
| 2027-01-27 | 2027-01-28 | 1.0 | False | 0.004 | 4.204069 | 8.737 | 4.205 | -0.093 |
| 2027-03-17 | 2027-03-18 | 1.0 | False | 0.005 | 4.36341 | 15.934 | 4.36 | 0.341 |
| 2027-04-28 | 2027-04-29 | 1.0 | False | 0.005 | 4.454955 | 9.154 | 4.455 | -0.005 |
| 2027-06-09 | 2027-06-10 | 1.0 | False | 0.006 | 4.555886 | 10.093 | 4.555 | 0.089 |
| 2027-07-28 | 2027-07-29 | 1.0 | False | 0.008 | 4.595392 | 3.951 | 4.595 | 0.039 |
| 2027-09-15 | 2027-09-16 | 1.0 | False | 0.015 | 4.640253 | 4.486 | 4.645 | -0.475 |
| 2027-10-27 | 2027-10-28 | 1.0 | False | 0.019 | 4.649111 | 0.886 | 4.65 | -0.089 |
| 2027-12-08 | 2027-12-09 | 1.0 | False | 0.02 | 4.647669 | -0.144 | 4.643261 | 0.441 |
| 2028-01-26 (synthetic) | 2028-01-27 | 1.0 | False | 0.022 | 4.645435 | -0.223 | 4.645 | 0.044 |
| 2028-03-15 (synthetic) | 2028-03-16 | 0.0 | True | 0.023 | 4.645435 | 0.0 |  |  |
| 2028-04-26 (synthetic) | 2028-04-27 | 0.0 | True | 0.023 | 4.645435 | 0.0 |  |  |
| 2028-06-14 (synthetic) | 2028-06-15 | 0.0 | True | 0.024 | 4.645435 | 0.0 |  |  |
| 2028-07-26 (synthetic) | 2028-07-27 | 0.0 | True | 0.024 | 4.645435 | 0.0 |  |  |
| 2028-09-20 (synthetic) | 2028-09-21 | 0.0 | True | 0.025 | 4.645435 | 0.0 |  |  |
| 2028-10-25 (synthetic) | 2028-10-26 | 0.0 | True | 0.025 | 4.645435 | 0.0 |  |  |
| 2028-12-13 (synthetic) | 2028-12-14 | 0.0 | True | 0.026 | 4.645435 | 0.0 |  |  |
| 2029-01-24 (synthetic) | 2029-01-25 | 0.0 | True | 0.026 | 4.645435 | 0.0 |  |  |
| 2029-03-21 (synthetic) | 2029-03-22 | 0.0 | True | 0.027 | 4.645435 | 0.0 |  |  |
| 2029-04-25 (synthetic) | 2029-04-26 | 0.0 | True | 0.027 | 4.645435 | 0.0 |  |  |
| 2029-06-13 (synthetic) | 2029-06-14 | 0.0 | True | 0.028 | 4.645435 | 0.0 |  |  |
| 2029-07-25 (synthetic) | 2029-07-26 | 0.0 | True | 0.028 | 4.645435 | 0.0 |  |  |
| 2029-09-19 (synthetic) | 2029-09-20 | 0.0 | True | 0.029 | 4.645435 | 0.0 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_fut | ff_fut 2026-10 | 3.885000000000005 | used |
| effr_fut | ff_fut 2026-11 | 3.924999999999997 | used |
| effr_fut | ff_fut 2026-12 | 4.064999999999998 | used |
| effr_fut | ff_fut 2027-01 | 4.125 | used |
| effr_fut | ff_fut 2027-02 | 4.204999999999998 | used |
| effr_fut | ff_fut 2027-03 | 4.275000000000006 | used |
| effr_fut | ff_fut 2027-04 | 4.3700000000000045 | used |
| effr_fut | ff_fut 2027-05 | 4.454999999999998 | used |
| effr_fut | ff_fut 2027-06 | 4.525000000000006 | used |
| effr_fut | ff_fut 2027-07 | 4.560000000000002 | used |
| effr_fut | ff_fut 2027-08 | 4.594999999999999 | used |
| effr_fut | ff_fut 2027-09 | 4.6200000000000045 | used |
| effr_fut | ff_fut 2027-10 | 4.640000000000001 | used |
| effr_fut | ff_fut 2027-11 | 4.650000000000006 | used |
| effr_fut | ff_fut 2027-12 | 4.644999999999996 | used |
| effr_fut | ff_fut 2028-01 | 4.650000000000006 | used |
| effr_fut | ff_fut 2028-02 | 4.644999999999996 | used |

Replica notes: ff_fut 2027-02: no new parcel; re-solved parcel 3 (2027-01-27); ff_fut 2027-05: no new parcel; re-solved parcel 5 (2027-04-28); ff_fut 2027-08: no new parcel; re-solved parcel 7 (2027-07-28); ff_fut 2027-11: no new parcel; re-solved parcel 9 (2027-10-27); ff_fut 2028-02: no new parcel; re-solved parcel 11 (2028-01-26 (synthetic))

## Curve `effr_ois` (ois_effr)

Fit: 18 quotes (0 dropped, 0 excluded by metadata), 3 IRLS iterations (converged); 25 parcels to 2029-10-18, 14 synthetic and 0 unscheduled meetings. Current implied O/N rate 3.8785 (replica 3.8787; stub prior 3.8800 from anchor + spread (D7)). WIRP replica reaches 8 meetings on 13 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-10-28 | False | False | 3.928067 | 0.049613 | 0.1985 | 19.85 | 3.928169 | -0.01 | 3.923067 | 4.807 | False | 0.007 | False |
| 2026-12-09 | False | False | 4.130954 | 0.2525 | 1.01 | 81.15 | 4.13086 | 0.009 | 4.125954 | 25.095 | False | 0.014 | False |
| 2027-01-27 | False | False | 4.228446 | 0.349992 | 1.4 | 39.0 | 4.228316 | 0.013 | 4.223446 | 34.845 | False | 0.024 | False |
| 2027-03-17 | False | False | 4.391944 | 0.51349 | 2.054 | 65.4 | 4.392168 | -0.022 | 4.386944 | 51.194 | False | 0.039 | False |
| 2027-04-28 | False | False | 4.486481 | 0.608027 | 2.4321 | 37.81 | 4.486008 | 0.047 | 4.481481 | 60.648 | False | 0.043 | False |
| 2027-06-09 | False | False | 4.581112 | 0.702658 | 2.8106 | 37.85 | 4.582565 | -0.145 | 4.576112 | 70.111 | False | 0.044 | False |
| 2027-07-28 | False | False | 4.639778 | 0.761324 | 3.0453 | 23.47 | 4.638683 | 0.11 | 4.634778 | 75.978 | False | 0.057 | False |
| 2027-09-15 | False | False | 4.653858 | 0.775404 | 3.1016 | 5.63 | 4.65356 | 0.03 | 4.648858 | 77.386 | False | 0.098 | False |
| 2027-10-27 | False | False | 4.665255 | 0.786801 | 3.1472 | 4.56 |  |  | 4.660255 | 78.526 | True | 0.051 | True |
| 2027-12-08 | False | False | 4.676648 | 0.798194 | 3.1928 | 4.56 |  |  | 4.671648 | 79.665 | True | 0.019 | True |
| 2028-01-26 | True | False | 4.688036 | 0.809582 | 3.2383 | 4.56 |  |  | 4.683036 | 80.804 | True | 0.054 | True |
| 2028-03-15 | True | False | 4.699419 | 0.820965 | 3.2839 | 4.55 |  |  | 4.694419 | 81.942 | True | 0.106 | True |
| 2028-04-26 | True | False | 4.697019 | 0.818565 | 3.2743 | -0.96 |  |  | 4.692019 | 81.702 | True | 0.055 | True |
| 2028-06-14 | True | False | 4.694619 | 0.816165 | 3.2647 | -0.96 |  |  | 4.689619 | 81.462 | True | 0.026 | True |
| 2028-07-26 | True | False | 4.69222 | 0.813765 | 3.2551 | -0.96 |  |  | 4.68722 | 81.222 | True | 0.064 | True |
| 2028-09-20 | True | False | 4.68982 | 0.811366 | 3.2455 | -0.96 |  |  | 4.68482 | 80.982 | True | 0.119 | True |
| 2028-10-25 | True | False | 4.688828 | 0.810374 | 3.2415 | -0.4 |  |  | 4.683828 | 80.883 | True | 0.092 | True |
| 2028-12-13 | True | False | 4.687836 | 0.809382 | 3.2375 | -0.4 |  |  | 4.682836 | 80.784 | True | 0.068 | True |
| 2029-01-24 | True | False | 4.686845 | 0.808391 | 3.2336 | -0.4 |  |  | 4.681845 | 80.685 | True | 0.046 | True |
| 2029-03-21 | True | False | 4.685855 | 0.807401 | 3.2296 | -0.4 |  |  | 4.680855 | 80.586 | True | 0.032 | True |
| 2029-04-25 | True | False | 4.684866 | 0.806411 | 3.2256 | -0.4 |  |  | 4.679866 | 80.487 | True | 0.042 | True |
| 2029-06-13 | True | False | 4.683877 | 0.805423 | 3.2217 | -0.4 |  |  | 4.678877 | 80.388 | True | 0.071 | True |
| 2029-07-25 | True | False | 4.682889 | 0.804434 | 3.2177 | -0.4 |  |  | 4.677889 | 80.289 | True | 0.108 | True |
| 2029-09-19 | True | False | 4.681901 | 0.803447 | 3.2138 | -0.4 |  |  | 4.676901 | 80.19 | True | 0.151 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | used | 18 | 0.0 | 0.016 | 0.039 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

_none_

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | 11M | USSOK Curncy | 4.3988 | 0.004 | 0.074 | 0.942 |
| effr_ois | ois_effr | 1Y | USSO1 Curncy | 4.4393 | -0.0 | -0.027 | 0.983 |
| effr_ois | ois_effr | 18M | USSO1F Curncy | 4.5345 | 0.0 | 0.063 | 0.997 |
| effr_ois | ois_effr | 2Y | USSO2 Curncy | 4.6137 | 0.0 | 0.001 | 0.999 |
| effr_ois | ois_effr | 3Y | USSO3 Curncy | 4.672 | -0.0 | -0.135 | 1.0 |

### Stale and outside-listing inputs

_none_

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2026-10-07 | 1.0 | False | 0.003 | 3.878454 |  | 3.878744 | -0.029 |
| 2026-10-28 | 2026-10-29 | 1.0 | False | 0.007 | 3.928067 | 4.961 | 3.928169 | -0.01 |
| 2026-12-09 | 2026-12-10 | 1.0 | False | 0.014 | 4.130954 | 20.289 | 4.13086 | 0.009 |
| 2027-01-27 | 2027-01-28 | 1.0 | False | 0.024 | 4.228446 | 9.749 | 4.228316 | 0.013 |
| 2027-03-17 | 2027-03-18 | 1.0 | False | 0.039 | 4.391944 | 16.35 | 4.392168 | -0.022 |
| 2027-04-28 | 2027-04-29 | 1.0 | False | 0.043 | 4.486481 | 9.454 | 4.486008 | 0.047 |
| 2027-06-09 | 2027-06-10 | 1.0 | False | 0.044 | 4.581112 | 9.463 | 4.582565 | -0.145 |
| 2027-07-28 | 2027-07-29 | 1.0 | False | 0.057 | 4.639778 | 5.867 | 4.638683 | 0.11 |
| 2027-09-15 | 2027-09-16 | 1.0 | False | 0.098 | 4.653858 | 1.408 | 4.65356 | 0.03 |
| 2027-10-27 | 2027-10-28 | 0.2461 | True | 0.051 | 4.665255 | 1.14 |  |  |
| 2027-12-08 | 2027-12-09 | 0.335 | True | 0.019 | 4.676648 | 1.139 |  |  |
| 2028-01-26 (synthetic) | 2028-01-27 | 0.335 | True | 0.054 | 4.688036 | 1.139 |  |  |
| 2028-03-15 (synthetic) | 2028-03-16 | 0.1173 | True | 0.106 | 4.699419 | 1.138 |  |  |
| 2028-04-26 (synthetic) | 2028-04-27 | 0.3031 | True | 0.055 | 4.697019 | -0.24 |  |  |
| 2028-06-14 (synthetic) | 2028-06-15 | 0.2227 | True | 0.026 | 4.694619 | -0.24 |  |  |
| 2028-07-26 (synthetic) | 2028-07-27 | 0.3959 | True | 0.064 | 4.69222 | -0.24 |  |  |
| 2028-09-20 (synthetic) | 2028-09-21 | 0.0597 | True | 0.119 | 4.68982 | -0.24 |  |  |
| 2028-10-25 (synthetic) | 2028-10-26 | 0.1461 | True | 0.092 | 4.688828 | -0.099 |  |  |
| 2028-12-13 (synthetic) | 2028-12-14 | 0.1073 | True | 0.068 | 4.687836 | -0.099 |  |  |
| 2029-01-24 (synthetic) | 2029-01-25 | 0.1908 | True | 0.046 | 4.686845 | -0.099 |  |  |
| 2029-03-21 (synthetic) | 2029-03-22 | 0.0746 | True | 0.032 | 4.685855 | -0.099 |  |  |
| 2029-04-25 (synthetic) | 2029-04-26 | 0.1461 | True | 0.042 | 4.684866 | -0.099 |  |  |
| 2029-06-13 (synthetic) | 2029-06-14 | 0.1074 | True | 0.071 | 4.683877 | -0.099 |  |  |
| 2029-07-25 (synthetic) | 2029-07-26 | 0.1908 | True | 0.108 | 4.682889 | -0.099 |  |  |
| 2029-09-19 (synthetic) | 2029-09-20 | 0.022 | True | 0.151 | 4.681901 | -0.099 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_ois | ois_effr 1W | 3.87964 | used |
| effr_ois | ois_effr 1M | 3.90175 | used |
| effr_ois | ois_effr 2M | 3.92452 | used |
| effr_ois | ois_effr 3M | 4.007 | used |
| effr_ois | ois_effr 4M | 4.05745 | used |
| effr_ois | ois_effr 5M | 4.1013 | used |
| effr_ois | ois_effr 6M | 4.1568 | used |
| effr_ois | ois_effr 7M | 4.21059 | used |
| effr_ois | ois_effr 8M | 4.2594 | used |
| effr_ois | ois_effr 9M | 4.30995 | used |
| effr_ois | ois_effr 10M | 4.35575 | used |
| effr_ois | ois_effr 11M | 4.3988 | used |
| effr_ois | ois_effr 1Y | 4.4393 | used |

Replica notes: ois_effr 2M: no new parcel; re-solved parcel 1 (2026-10-28); ois_effr 5M: no new parcel; re-solved parcel 3 (2027-01-27); ois_effr 8M: no new parcel; re-solved parcel 5 (2027-04-28); ois_effr 11M: no new parcel; re-solved parcel 7 (2027-07-28)

## FF / OIS basis (bp, fit and replica)

| decision_date | effective_date | parcel | effr_fut_fit | effr_ois_fit | basis_fit_bp | basis_replica_bp |
| --- | --- | --- | --- | --- | --- | --- |
| None | None | stub | 3.880765794025322 | 3.8784543319769575 | 0.231 | 0.216 |
| 2026-10-28 | 2026-10-29 | 1 | 3.926063 | 3.928067 | -0.2 | -0.317 |
| 2026-12-09 | 2026-12-10 | 2 | 4.116696 | 4.130954 | -1.426 | -0.859 |
| 2027-01-27 | 2027-01-28 | 3 | 4.204069 | 4.228446 | -2.438 | -2.332 |
| 2027-03-17 | 2027-03-18 | 4 | 4.36341 | 4.391944 | -2.853 | -3.217 |
| 2027-04-28 | 2027-04-29 | 5 | 4.454955 | 4.486481 | -3.153 | -3.101 |
| 2027-06-09 | 2027-06-10 | 6 | 4.555886 | 4.581112 | -2.523 | -2.756 |
| 2027-07-28 | 2027-07-29 | 7 | 4.595392 | 4.639778 | -4.439 | -4.368 |
| 2027-09-15 | 2027-09-16 | 8 | 4.640253 | 4.653858 | -1.36 | -0.856 |
| 2027-10-27 | 2027-10-28 | 9 | 4.649111 | 4.665255 | -1.614 |  |
| 2027-12-08 | 2027-12-09 | 10 | 4.647669 | 4.676648 | -2.898 |  |
| 2028-01-26 | 2028-01-27 | 11 | 4.645435 | 4.688036 | -4.26 |  |
| 2028-03-15 | 2028-03-16 | 12 | 4.645435 | 4.699419 | -5.398 |  |
| 2028-04-26 | 2028-04-27 | 13 | 4.645435 | 4.697019 | -5.158 |  |
| 2028-06-14 | 2028-06-15 | 14 | 4.645435 | 4.694619 | -4.918 |  |
| 2028-07-26 | 2028-07-27 | 15 | 4.645435 | 4.69222 | -4.678 |  |
| 2028-09-20 | 2028-09-21 | 16 | 4.645435 | 4.68982 | -4.438 |  |
| 2028-10-25 | 2028-10-26 | 17 | 4.645435 | 4.688828 | -4.339 |  |
| 2028-12-13 | 2028-12-14 | 18 | 4.645435 | 4.687836 | -4.24 |  |
| 2029-01-24 | 2029-01-25 | 19 | 4.645435 | 4.686845 | -4.141 |  |
| 2029-03-21 | 2029-03-22 | 20 | 4.645435 | 4.685855 | -4.042 |  |
| 2029-04-25 | 2029-04-26 | 21 | 4.645435 | 4.684866 | -3.943 |  |
| 2029-06-13 | 2029-06-14 | 22 | 4.645435 | 4.683877 | -3.844 |  |
| 2029-07-25 | 2029-07-26 | 23 | 4.645435 | 4.682889 | -3.745 |  |
| 2029-09-19 | 2029-09-20 | 24 | 4.645435 | 4.681901 | -3.647 |  |

## Stub

| curve | as_of | current_implied | replica_current_implied | stub_prior | stub_prior_source | anchor | spread | spread_median | spread_winsorised_mean | spread_obs | spread_estimator | spread_note | wirp_reach_meetings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | 2026-10-07 | 3.880766 | 3.880909 | 3.88 | anchor + spread (D7) | 3.875 | 0.004999999999999893 | 0.004999999999999893 | 0.004999999999999893 | 60 | winsorised_mean |  | 11 |
| effr_ois | 2026-10-07 | 3.878454 | 3.878744 | 3.88 | anchor + spread (D7) | 3.875 | 0.004999999999999893 | 0.004999999999999893 | 0.004999999999999893 | 60 | winsorised_mean |  | 8 |
