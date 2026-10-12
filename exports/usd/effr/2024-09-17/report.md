# USD EFFR front end, 2024-09-17

Anchor (target_midpoint) in effect: 5.375. Policy spread (winsorised_mean, D7): -4.50bp (winsorised mean -4.50bp, median -4.50bp; 60 fixings, 3 turn days dropped, window 2024-06-17..2024-09-16)

## Curve `effr_fut` (ff_fut)

Fit: 18 quotes (0 dropped, 19 excluded by metadata), 3 IRLS iterations (converged); 26 parcels to 2027-09-17, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 5.4180 (replica 5.4275; stub prior 5.3300 from anchor + spread (D7)). WIRP replica reaches 12 meetings on 18 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024-09-18 | False | False | 4.919803 | -0.498158 | -1.9926 | -199.26 | 4.92 | -0.02 | 4.964803 | -41.02 | False | 0.005 | False |
| 2024-11-07 | False | False | 4.551036 | -0.866925 | -3.4677 | -147.51 | 4.548261 | 0.278 | 4.596036 | -77.896 | False | 0.005 | False |
| 2024-12-18 | False | False | 4.160471 | -1.25749 | -5.03 | -156.23 | 4.17087 | -1.04 | 4.205471 | -116.953 | False | 0.005 | False |
| 2025-01-29 | False | False | 3.784783 | -1.633178 | -6.5327 | -150.28 | 3.785 | -0.022 | 3.829783 | -154.522 | False | 0.004 | False |
| 2025-03-19 | False | False | 3.450094 | -1.967867 | -7.8715 | -133.88 | 3.45 | 0.009 | 3.495094 | -187.991 | False | 0.005 | False |
| 2025-05-07 | False | False | 3.222719 | -2.195242 | -8.781 | -90.95 | 3.223958 | -0.124 | 3.267719 | -210.728 | False | 0.006 | False |
| 2025-06-18 | False | False | 3.047291 | -2.370671 | -9.4827 | -70.17 | 3.03589 | 1.14 | 3.092291 | -228.271 | False | 0.007 | False |
| 2025-07-30 | False | False | 2.954988 | -2.462974 | -9.8519 | -36.92 | 2.955 | -0.001 | 2.999988 | -237.501 | False | 0.009 | False |
| 2025-09-17 | False | False | 2.887097 | -2.530864 | -10.1235 | -27.16 | 2.885769 | 0.133 | 2.932097 | -244.29 | False | 0.022 | False |
| 2025-10-29 | False | False | 2.850766 | -2.567195 | -10.2688 | -14.53 | 2.85 | 0.077 | 2.895766 | -247.923 | False | 0.022 | False |
| 2025-12-10 | False | False | 2.82408 | -2.593881 | -10.3755 | -10.67 | 2.827857 | -0.378 | 2.86908 | -250.592 | False | 0.02 | False |
| 2026-01-28 | False | False | 2.799844 | -2.618117 | -10.4725 | -9.69 | 2.8 | -0.016 | 2.844844 | -253.016 | False | 0.022 | False |
| 2026-03-18 | False | False | 2.799844 | -2.618117 | -10.4725 | 0.0 |  |  | 2.844844 | -253.016 | True | 0.023 | True |
| 2026-04-29 | False | False | 2.799844 | -2.618117 | -10.4725 | 0.0 |  |  | 2.844844 | -253.016 | True | 0.023 | True |
| 2026-06-17 | False | False | 2.799844 | -2.618117 | -10.4725 | 0.0 |  |  | 2.844844 | -253.016 | True | 0.024 | True |
| 2026-07-29 | False | False | 2.799844 | -2.618117 | -10.4725 | 0.0 |  |  | 2.844844 | -253.016 | True | 0.024 | True |
| 2026-09-16 | False | False | 2.799844 | -2.618117 | -10.4725 | 0.0 |  |  | 2.844844 | -253.016 | True | 0.025 | True |
| 2026-10-28 | False | False | 2.799844 | -2.618117 | -10.4725 | 0.0 |  |  | 2.844844 | -253.016 | True | 0.025 | True |
| 2026-12-09 | False | False | 2.799844 | -2.618117 | -10.4725 | 0.0 |  |  | 2.844844 | -253.016 | True | 0.026 | True |
| 2027-01-27 | False | False | 2.799844 | -2.618117 | -10.4725 | 0.0 |  |  | 2.844844 | -253.016 | True | 0.026 | True |
| 2027-03-17 | False | False | 2.799844 | -2.618117 | -10.4725 | 0.0 |  |  | 2.844844 | -253.016 | True | 0.027 | True |
| 2027-04-28 | False | False | 2.799844 | -2.618117 | -10.4725 | 0.0 |  |  | 2.844844 | -253.016 | True | 0.027 | True |
| 2027-06-09 | False | False | 2.799844 | -2.618117 | -10.4725 | 0.0 |  |  | 2.844844 | -253.016 | True | 0.028 | True |
| 2027-07-28 | False | False | 2.799844 | -2.618117 | -10.4725 | 0.0 |  |  | 2.844844 | -253.016 | True | 0.028 | True |
| 2027-09-15 | False | False | 2.799844 | -2.618117 | -10.4725 | 0.0 |  |  | 2.844844 | -253.016 | True | 0.029 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | used | 18 | -0.01 | 0.142 | 0.34 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

| curve | instrument | contract | ticker | status | reason | residual_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2026-03 | FFH26 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2026-05 | FFK26 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2026-06 | FFM26 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2026-07 | FFN26 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2026-08 | FFQ26 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2026-09 | FFU26 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2026-10 | FFV26 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2026-11 | FFX26 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2026-12 | FFZ26 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2027-01 | FFF27 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2027-02 | FFG27 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2027-03 | FFH27 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2027-04 | FFJ27 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2027-05 | FFK27 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2027-06 | FFM27 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2027-07 | FFN27 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2027-08 | FFQ27 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2027-09 | FFU27 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2026-04 | FFJ26 Comdty | excluded | beyond the strip's reach (first contract without open interest or volume starts 2026-03-01) |  |

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2024-09 | FFU24 Comdty | 5.1725 | 0.071 | 0.83 | 0.914 |
| effr_fut | ff_fut | 2024-10 | FFV24 Comdty | 4.92 | 0.02 | 0.636 | 0.969 |
| effr_fut | ff_fut | 2025-07 | FFN25 Comdty | 3.045 | 0.069 | 1.167 | 0.941 |
| effr_fut | ff_fut | 2025-08 | FFQ25 Comdty | 2.955 | 0.001 | 0.029 | 0.958 |
| effr_fut | ff_fut | 2025-11 | FFX25 Comdty | 2.85 | -0.077 | -1.198 | 0.936 |
| effr_fut | ff_fut | 2026-02 | FFG26 Comdty | 2.8 | 0.016 | 4.183 | 0.996 |

### Stale and outside-listing inputs

_none_

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2024-09-17 | 1.0 | False | 0.077 | 5.417961 |  | 5.4275 | -0.954 |
| 2024-09-18 | 2024-09-19 | 1.0 | False | 0.005 | 4.919803 | -49.816 | 4.92 | -0.02 |
| 2024-11-07 | 2024-11-08 | 1.0 | False | 0.005 | 4.551036 | -36.877 | 4.548261 | 0.278 |
| 2024-12-18 | 2024-12-19 | 1.0 | False | 0.005 | 4.160471 | -39.057 | 4.17087 | -1.04 |
| 2025-01-29 | 2025-01-30 | 1.0 | False | 0.004 | 3.784783 | -37.569 | 3.785 | -0.022 |
| 2025-03-19 | 2025-03-20 | 1.0 | False | 0.005 | 3.450094 | -33.469 | 3.45 | 0.009 |
| 2025-05-07 | 2025-05-08 | 1.0 | False | 0.006 | 3.222719 | -22.738 | 3.223958 | -0.124 |
| 2025-06-18 | 2025-06-20 | 1.0 | False | 0.007 | 3.047291 | -17.543 | 3.03589 | 1.14 |
| 2025-07-30 | 2025-07-31 | 1.0 | False | 0.009 | 2.954988 | -9.23 | 2.955 | -0.001 |
| 2025-09-17 | 2025-09-18 | 1.0 | False | 0.022 | 2.887097 | -6.789 | 2.885769 | 0.133 |
| 2025-10-29 | 2025-10-30 | 1.0 | False | 0.022 | 2.850766 | -3.633 | 2.85 | 0.077 |
| 2025-12-10 | 2025-12-11 | 1.0 | False | 0.02 | 2.82408 | -2.669 | 2.827857 | -0.378 |
| 2026-01-28 | 2026-01-29 | 1.0 | False | 0.022 | 2.799844 | -2.424 | 2.8 | -0.016 |
| 2026-03-18 | 2026-03-19 | 0.0 | True | 0.023 | 2.799844 | 0.0 |  |  |
| 2026-04-29 | 2026-04-30 | 0.0 | True | 0.023 | 2.799844 | 0.0 |  |  |
| 2026-06-17 | 2026-06-18 | 0.0 | True | 0.024 | 2.799844 | 0.0 |  |  |
| 2026-07-29 | 2026-07-30 | 0.0 | True | 0.024 | 2.799844 | 0.0 |  |  |
| 2026-09-16 | 2026-09-17 | 0.0 | True | 0.025 | 2.799844 | 0.0 |  |  |
| 2026-10-28 | 2026-10-29 | 0.0 | True | 0.025 | 2.799844 | 0.0 |  |  |
| 2026-12-09 | 2026-12-10 | 0.0 | True | 0.026 | 2.799844 | 0.0 |  |  |
| 2027-01-27 | 2027-01-28 | 0.0 | True | 0.026 | 2.799844 | 0.0 |  |  |
| 2027-03-17 | 2027-03-18 | 0.0 | True | 0.027 | 2.799844 | 0.0 |  |  |
| 2027-04-28 | 2027-04-29 | 0.0 | True | 0.027 | 2.799844 | 0.0 |  |  |
| 2027-06-09 | 2027-06-10 | 0.0 | True | 0.028 | 2.799844 | 0.0 |  |  |
| 2027-07-28 | 2027-07-29 | 0.0 | True | 0.028 | 2.799844 | 0.0 |  |  |
| 2027-09-15 | 2027-09-16 | 0.0 | True | 0.029 | 2.799844 | 0.0 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_fut | ff_fut 2024-09 | 5.172499999999999 | used |
| effr_fut | ff_fut 2024-10 | 4.920000000000002 | used |
| effr_fut | ff_fut 2024-11 | 4.635000000000005 | used |
| effr_fut | ff_fut 2024-12 | 4.390000000000001 | used |
| effr_fut | ff_fut 2025-01 | 4.135000000000005 | used |
| effr_fut | ff_fut 2025-02 | 3.7849999999999966 | used |
| effr_fut | ff_fut 2025-03 | 3.655000000000001 | used |
| effr_fut | ff_fut 2025-04 | 3.450000000000003 | used |
| effr_fut | ff_fut 2025-05 | 3.2750000000000057 | used |
| effr_fut | ff_fut 2025-06 | 3.155000000000001 | used |
| effr_fut | ff_fut 2025-07 | 3.0450000000000017 | used |
| effr_fut | ff_fut 2025-08 | 2.9549999999999983 | used |
| effr_fut | ff_fut 2025-09 | 2.924999999999997 | used |
| effr_fut | ff_fut 2025-10 | 2.885000000000005 | used |
| effr_fut | ff_fut 2025-11 | 2.8499999999999943 | used |
| effr_fut | ff_fut 2025-12 | 2.8349999999999937 | used |
| effr_fut | ff_fut 2026-01 | 2.819999999999993 | used |
| effr_fut | ff_fut 2026-02 | 2.799999999999997 | used |

Replica notes: ff_fut 2025-02: no new parcel; re-solved parcel 4 (2025-01-29); ff_fut 2025-04: no new parcel; re-solved parcel 5 (2025-03-19); ff_fut 2025-08: no new parcel; re-solved parcel 8 (2025-07-30); ff_fut 2025-11: no new parcel; re-solved parcel 10 (2025-10-29); ff_fut 2026-02: no new parcel; re-solved parcel 12 (2026-01-28)

## Curve `effr_ois` (ois_effr)

Fit: 18 quotes (0 dropped, 0 excluded by metadata), 3 IRLS iterations (converged); 26 parcels to 2027-09-29, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 5.3059 (replica 5.3300; stub prior 5.3300 from anchor + spread (D7)). WIRP replica reaches 8 meetings on 13 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024-09-18 | False | False | 4.920568 | -0.385348 | -1.5414 | -154.14 | 4.917902 | 0.267 | 4.965568 | -40.943 | False | 0.002 | False |
| 2024-11-07 | False | False | 4.550709 | -0.755207 | -3.0208 | -147.94 | 4.55403 | -0.332 | 4.595709 | -77.929 | False | 0.011 | False |
| 2024-12-18 | False | False | 4.16157 | -1.144346 | -4.5774 | -155.66 | 4.161755 | -0.019 | 4.20657 | -116.843 | False | 0.02 | False |
| 2025-01-29 | False | False | 3.788094 | -1.517822 | -6.0713 | -149.39 | 3.788104 | -0.001 | 3.833094 | -154.191 | False | 0.024 | False |
| 2025-03-19 | False | False | 3.447072 | -1.858843 | -7.4354 | -136.41 | 3.446788 | 0.028 | 3.492072 | -188.293 | False | 0.032 | False |
| 2025-05-07 | False | False | 3.212825 | -2.093091 | -8.3724 | -93.7 | 3.212912 | -0.009 | 3.257825 | -211.718 | False | 0.044 | False |
| 2025-06-18 | False | False | 3.049712 | -2.256204 | -9.0248 | -65.24 | 3.049608 | 0.01 | 3.094712 | -228.029 | False | 0.055 | False |
| 2025-07-30 | False | False | 2.942661 | -2.363255 | -9.453 | -42.82 | 2.941212 | 0.145 | 2.987661 | -238.734 | False | 0.053 | False |
| 2025-09-17 | False | False | 2.869538 | -2.436378 | -9.7455 | -29.25 |  |  | 2.914538 | -246.046 | False | 0.327 | True |
| 2025-10-29 | False | False | 2.845605 | -2.460311 | -9.8412 | -9.57 |  |  | 2.890605 | -248.44 | True | 0.122 | True |
| 2025-12-10 | False | False | 2.821684 | -2.484232 | -9.9369 | -9.57 |  |  | 2.866684 | -250.832 | True | 0.087 | True |
| 2026-01-28 | False | False | 2.79778 | -2.508136 | -10.0325 | -9.56 |  |  | 2.84278 | -253.222 | True | 0.29 | True |
| 2026-03-18 | False | False | 2.773889 | -2.532027 | -10.1281 | -9.56 |  |  | 2.818889 | -255.611 | True | 0.495 | True |
| 2026-04-29 | False | False | 2.77912 | -2.526796 | -10.1072 | 2.09 |  |  | 2.82412 | -255.088 | True | 0.185 | True |
| 2026-06-17 | False | False | 2.78435 | -2.521566 | -10.0863 | 2.09 |  |  | 2.82935 | -254.565 | True | 0.13 | True |
| 2026-07-29 | False | False | 2.789579 | -2.516337 | -10.0653 | 2.09 |  |  | 2.834579 | -254.042 | True | 0.439 | True |
| 2026-09-16 | False | False | 2.794807 | -2.511108 | -10.0444 | 2.09 |  |  | 2.839807 | -253.519 | True | 0.749 | True |
| 2026-10-28 | False | False | 2.796392 | -2.509524 | -10.0381 | 0.63 |  |  | 2.841392 | -253.361 | True | 0.545 | True |
| 2026-12-09 | False | False | 2.797976 | -2.50794 | -10.0318 | 0.63 |  |  | 2.842976 | -253.202 | True | 0.341 | True |
| 2027-01-27 | False | False | 2.799558 | -2.506357 | -10.0254 | 0.63 |  |  | 2.844558 | -253.044 | True | 0.139 | True |
| 2027-03-17 | False | False | 2.80114 | -2.504776 | -10.0191 | 0.63 |  |  | 2.84614 | -252.886 | True | 0.075 | True |
| 2027-04-28 | False | False | 2.80272 | -2.503196 | -10.0128 | 0.63 |  |  | 2.84772 | -252.728 | True | 0.275 | True |
| 2027-06-09 | False | False | 2.804299 | -2.501617 | -10.0065 | 0.63 |  |  | 2.849299 | -252.57 | True | 0.479 | True |
| 2027-07-28 | False | False | 2.805877 | -2.500039 | -10.0002 | 0.63 |  |  | 2.850877 | -252.412 | True | 0.684 | True |
| 2027-09-15 | False | False | 2.807454 | -2.498462 | -9.9938 | 0.63 |  |  | 2.852454 | -252.255 | True | 0.89 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | used | 18 | -0.0 | 0.139 | 0.499 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

_none_

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | 9M | USSOI Curncy | 4.07635 | 0.0 | 0.006 | 0.939 |
| effr_ois | ois_effr | 18M | USSO1F Curncy | 3.5075 | -0.001 | -0.369 | 0.998 |
| effr_ois | ois_effr | 2Y | USSO2 Curncy | 3.34485 | 0.0 | 0.027 | 0.999 |
| effr_ois | ois_effr | 3Y | USSO3 Curncy | 3.18205 | 0.0 | 0.29 | 1.0 |

### Stale and outside-listing inputs

_none_

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2024-09-17 | 0.0 | True | 0.243 | 5.305916 |  | 5.33 | -2.408 |
| 2024-09-18 | 2024-09-19 | 1.0 | False | 0.002 | 4.920568 | -38.535 | 4.917902 | 0.267 |
| 2024-11-07 | 2024-11-08 | 1.0 | False | 0.011 | 4.550709 | -36.986 | 4.55403 | -0.332 |
| 2024-12-18 | 2024-12-19 | 1.0 | False | 0.02 | 4.16157 | -38.914 | 4.161755 | -0.019 |
| 2025-01-29 | 2025-01-30 | 1.0 | False | 0.024 | 3.788094 | -37.348 | 3.788104 | -0.001 |
| 2025-03-19 | 2025-03-20 | 1.0 | False | 0.032 | 3.447072 | -34.102 | 3.446788 | 0.028 |
| 2025-05-07 | 2025-05-08 | 1.0 | False | 0.044 | 3.212825 | -23.425 | 3.212912 | -0.009 |
| 2025-06-18 | 2025-06-20 | 1.0 | False | 0.055 | 3.049712 | -16.311 | 3.049608 | 0.01 |
| 2025-07-30 | 2025-07-31 | 1.0 | False | 0.053 | 2.942661 | -10.705 | 2.941212 | 0.145 |
| 2025-09-17 | 2025-09-18 | 1.0 | False | 0.327 | 2.869538 | -7.312 |  |  |
| 2025-10-29 | 2025-10-30 | 0.2687 | True | 0.122 | 2.845605 | -2.393 |  |  |
| 2025-12-10 | 2025-12-11 | 0.3657 | True | 0.087 | 2.821684 | -2.392 |  |  |
| 2026-01-28 | 2026-01-29 | 0.3657 | True | 0.29 | 2.79778 | -2.39 |  |  |
| 2026-03-18 | 2026-03-19 | 0.2113 | True | 0.495 | 2.773889 | -2.389 |  |  |
| 2026-04-29 | 2026-04-30 | 0.2878 | True | 0.185 | 2.77912 | 0.523 |  |  |
| 2026-06-17 | 2026-06-18 | 0.2114 | True | 0.13 | 2.78435 | 0.523 |  |  |
| 2026-07-29 | 2026-07-30 | 0.2878 | True | 0.439 | 2.789579 | 0.523 |  |  |
| 2026-09-16 | 2026-09-17 | 0.0899 | True | 0.749 | 2.794807 | 0.523 |  |  |
| 2026-10-28 | 2026-10-29 | 0.1079 | True | 0.545 | 2.796392 | 0.158 |  |  |
| 2026-12-09 | 2026-12-10 | 0.1468 | True | 0.341 | 2.797976 | 0.158 |  |  |
| 2027-01-27 | 2027-01-28 | 0.1468 | True | 0.139 | 2.799558 | 0.158 |  |  |
| 2027-03-17 | 2027-03-18 | 0.1079 | True | 0.075 | 2.80114 | 0.158 |  |  |
| 2027-04-28 | 2027-04-29 | 0.1079 | True | 0.275 | 2.80272 | 0.158 |  |  |
| 2027-06-09 | 2027-06-10 | 0.1468 | True | 0.479 | 2.804299 | 0.158 |  |  |
| 2027-07-28 | 2027-07-29 | 0.1468 | True | 0.684 | 2.805877 | 0.158 |  |  |
| 2027-09-15 | 2027-09-16 | 0.001 | True | 0.89 | 2.807454 | 0.158 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_ois | ois_effr 1W | 4.9212 | used |
| effr_ois | ois_effr 1M | 4.92795 | used |
| effr_ois | ois_effr 2M | 4.8731 | used |
| effr_ois | ois_effr 3M | 4.782 | used |
| effr_ois | ois_effr 4M | 4.63232 | used |
| effr_ois | ois_effr 5M | 4.507 | used |
| effr_ois | ois_effr 6M | 4.408 | used |
| effr_ois | ois_effr 7M | 4.274 | used |
| effr_ois | ois_effr 8M | 4.178 | used |
| effr_ois | ois_effr 9M | 4.07635 | used |
| effr_ois | ois_effr 10M | 3.982 | used |
| effr_ois | ois_effr 11M | 3.904 | used |
| effr_ois | ois_effr 1Y | 3.8315 | used |

Replica notes: ois_effr 1M: no new parcel; re-solved parcel 1 (2024-09-18); ois_effr 3M: no new parcel; re-solved parcel 2 (2024-11-07); ois_effr 6M: no new parcel; re-solved parcel 4 (2025-01-29); ois_effr 9M: no new parcel; re-solved parcel 6 (2025-05-07); ois_effr 1Y: no new parcel; re-solved parcel 8 (2025-07-30); stub parcel not priced by any instrument (the first one starts after the next effective date): set to the last fixing 5.3300 (2024-09-16)

## FF / OIS basis (bp, fit and replica)

| decision_date | effective_date | parcel | effr_fut_fit | effr_ois_fit | basis_fit_bp | basis_replica_bp |
| --- | --- | --- | --- | --- | --- | --- |
| None | None | stub | 5.417961235656814 | 5.305915743733883 | 11.205 | 9.75 |
| 2024-09-18 | 2024-09-19 | 1 | 4.919803 | 4.920568 | -0.076 | 0.21 |
| 2024-11-07 | 2024-11-08 | 2 | 4.551036 | 4.550709 | 0.033 | -0.577 |
| 2024-12-18 | 2024-12-19 | 3 | 4.160471 | 4.16157 | -0.11 | 0.911 |
| 2025-01-29 | 2025-01-30 | 4 | 3.784783 | 3.788094 | -0.331 | -0.31 |
| 2025-03-19 | 2025-03-20 | 5 | 3.450094 | 3.447072 | 0.302 | 0.321 |
| 2025-05-07 | 2025-05-08 | 6 | 3.222719 | 3.212825 | 0.989 | 1.105 |
| 2025-06-18 | 2025-06-20 | 7 | 3.047291 | 3.049712 | -0.242 | -1.372 |
| 2025-07-30 | 2025-07-31 | 8 | 2.954988 | 2.942661 | 1.233 | 1.379 |
| 2025-09-17 | 2025-09-18 | 9 | 2.887097 | 2.869538 | 1.756 |  |
| 2025-10-29 | 2025-10-30 | 10 | 2.850766 | 2.845605 | 0.516 |  |
| 2025-12-10 | 2025-12-11 | 11 | 2.82408 | 2.821684 | 0.24 |  |
| 2026-01-28 | 2026-01-29 | 12 | 2.799844 | 2.79778 | 0.206 |  |
| 2026-03-18 | 2026-03-19 | 13 | 2.799844 | 2.773889 | 2.596 |  |
| 2026-04-29 | 2026-04-30 | 14 | 2.799844 | 2.77912 | 2.072 |  |
| 2026-06-17 | 2026-06-18 | 15 | 2.799844 | 2.78435 | 1.549 |  |
| 2026-07-29 | 2026-07-30 | 16 | 2.799844 | 2.789579 | 1.027 |  |
| 2026-09-16 | 2026-09-17 | 17 | 2.799844 | 2.794807 | 0.504 |  |
| 2026-10-28 | 2026-10-29 | 18 | 2.799844 | 2.796392 | 0.345 |  |
| 2026-12-09 | 2026-12-10 | 19 | 2.799844 | 2.797976 | 0.187 |  |
| 2027-01-27 | 2027-01-28 | 20 | 2.799844 | 2.799558 | 0.029 |  |
| 2027-03-17 | 2027-03-18 | 21 | 2.799844 | 2.80114 | -0.13 |  |
| 2027-04-28 | 2027-04-29 | 22 | 2.799844 | 2.80272 | -0.288 |  |
| 2027-06-09 | 2027-06-10 | 23 | 2.799844 | 2.804299 | -0.445 |  |
| 2027-07-28 | 2027-07-29 | 24 | 2.799844 | 2.805877 | -0.603 |  |
| 2027-09-15 | 2027-09-16 | 25 | 2.799844 | 2.807454 | -0.761 |  |

## Stub

| curve | as_of | current_implied | replica_current_implied | stub_prior | stub_prior_source | anchor | spread | spread_median | spread_winsorised_mean | spread_obs | spread_estimator | spread_note | wirp_reach_meetings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | 2024-09-17 | 5.417961 | 5.4275 | 5.33 | anchor + spread (D7) | 5.375 | -0.04499999999999993 | -0.04499999999999993 | -0.04499999999999993 | 60 | winsorised_mean |  | 12 |
| effr_ois | 2024-09-17 | 5.305916 | 5.33 | 5.33 | anchor + spread (D7) | 5.375 | -0.04499999999999993 | -0.04499999999999993 | -0.04499999999999993 | 60 | winsorised_mean |  | 8 |
