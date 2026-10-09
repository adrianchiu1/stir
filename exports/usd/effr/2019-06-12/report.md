# USD EFFR front end, 2019-06-12

Anchor (target_midpoint) in effect: 2.375. Policy spread (winsorised_mean, D7): none (0 fixings in the window (< 20)); implied policy rates and moves vs target left empty

## Curve `effr_fut` (ff_fut)

Fit: 24 quotes (0 dropped, 12 excluded by metadata), 2 IRLS iterations (converged); 25 parcels to 2022-06-12, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 2.3852 (replica 2.3853; stub prior 2.3700 from last fixing). WIRP replica reaches 16 meetings on 24 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2019-06-19 | False | False | 2.330001 | -0.055243 | -0.221 | -22.1 | 2.33 | 0.0 |  |  | False | 0.005 | False |
| 2019-07-31 | False | False | 2.135815 | -0.249429 | -0.9977 | -77.67 | 2.135 | 0.081 |  |  | False | 0.004 | False |
| 2019-09-18 | False | False | 1.967886 | -0.417358 | -1.6694 | -67.17 | 1.9725 | -0.461 |  |  | False | 0.005 | False |
| 2019-10-30 | False | False | 1.895889 | -0.489355 | -1.9574 | -28.8 | 1.895 | 0.089 |  |  | False | 0.005 | False |
| 2019-12-11 | False | False | 1.75104 | -0.634204 | -2.5368 | -57.94 | 1.7555 | -0.446 |  |  | False | 0.004 | False |
| 2020-01-29 | False | False | 1.684842 | -0.700402 | -2.8016 | -26.48 | 1.685 | -0.016 |  |  | False | 0.005 | False |
| 2020-03-18 | False | False | 1.625996 | -0.759248 | -3.037 | -23.54 | 1.625385 | 0.061 |  |  | False | 0.005 | False |
| 2020-04-29 | False | False | 1.595132 | -0.790112 | -3.1604 | -12.35 | 1.595 | 0.013 |  |  | False | 0.006 | False |
| 2020-06-10 | False | False | 1.54784 | -0.837404 | -3.3496 | -18.92 | 1.55 | -0.216 |  |  | False | 0.008 | False |
| 2020-07-29 | False | False | 1.514614 | -0.87063 | -3.4825 | -13.29 | 1.515 | -0.039 |  |  | False | 0.01 | False |
| 2020-09-16 | False | False | 1.474545 | -0.910699 | -3.6428 | -16.03 | 1.475 | -0.046 |  |  | False | 0.013 | False |
| 2020-11-05 | False | False | 1.456018 | -0.929226 | -3.7169 | -7.41 | 1.457 | -0.098 |  |  | False | 0.023 | False |
| 2020-12-16 | False | False | 1.436347 | -0.948897 | -3.7956 | -7.87 | 1.4322 | 0.415 |  |  | False | 0.023 | False |
| 2021-01-27 | False | False | 1.419467 | -0.965777 | -3.8631 | -6.75 | 1.42 | -0.053 |  |  | False | 0.02 | False |
| 2021-03-17 | False | False | 1.434369 | -0.950875 | -3.8035 | 5.96 | 1.431071 | 0.33 |  |  | False | 0.022 | False |
| 2021-04-28 | False | False | 1.435039 | -0.950205 | -3.8008 | 0.27 | 1.435 | 0.004 |  |  | False | 0.022 | False |
| 2021-06-16 | False | False | 1.435039 | -0.950205 | -3.8008 | 0.0 |  |  |  |  | True | 0.023 | True |
| 2021-07-28 | False | False | 1.435039 | -0.950205 | -3.8008 | 0.0 |  |  |  |  | True | 0.023 | True |
| 2021-09-22 | False | False | 1.435039 | -0.950205 | -3.8008 | 0.0 |  |  |  |  | True | 0.024 | True |
| 2021-11-03 | False | False | 1.435039 | -0.950205 | -3.8008 | 0.0 |  |  |  |  | True | 0.024 | True |
| 2021-12-15 | False | False | 1.435039 | -0.950205 | -3.8008 | 0.0 |  |  |  |  | True | 0.025 | True |
| 2022-01-26 | False | False | 1.435039 | -0.950205 | -3.8008 | 0.0 |  |  |  |  | True | 0.025 | True |
| 2022-03-16 | False | False | 1.435039 | -0.950205 | -3.8008 | 0.0 |  |  |  |  | True | 0.026 | True |
| 2022-05-04 | False | False | 1.435039 | -0.950205 | -3.8008 | 0.0 |  |  |  |  | True | 0.026 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | used | 24 | 0.002 | 0.098 | 0.256 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

| curve | instrument | contract | ticker | status | reason | residual_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2021-06 | FFM21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-07 | FFN21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-08 | FFQ21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-09 | FFU21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-10 | FFV21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-11 | FFX21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2021-12 | FFZ21 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-01 | FFF22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-02 | FFG22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-03 | FFH22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-04 | FFJ22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |
| effr_fut | ff_fut | 2022-05 | FFK22 Comdty | excluded | no open interest and no volume: a derived settlement price, not a quote |  |

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | ff_fut | 2019-06 | FFM19 Comdty | 2.365 | 0.001 | 1.116 | 0.999 |
| effr_fut | ff_fut | 2019-07 | FFN19 Comdty | 2.33 | -0.0 | -0.387 | 1.0 |
| effr_fut | ff_fut | 2019-11 | FFX19 Comdty | 1.895 | -0.089 | -1.13 | 0.921 |
| effr_fut | ff_fut | 2020-04 | FFJ20 Comdty | 1.625 | 0.003 | 0.046 | 0.93 |
| effr_fut | ff_fut | 2020-05 | FFK20 Comdty | 1.595 | -0.013 | -0.581 | 0.977 |
| effr_fut | ff_fut | 2021-05 | FFK21 Comdty | 1.435 | -0.004 | -3.123 | 0.999 |

### Stale and outside-listing inputs

| curve | flag | instrument | contract | status | detail |
| --- | --- | --- | --- | --- | --- |
| effr_fut | missing_fixings | EFFR |  | used | rate dates with no fixing on file, modelled at the nearest earlier fixing or the stub rate: 2019-05-31, 2019-06-03, 2019-06-04, 2019-06-05, 2019-06-06, 2019-06-07, 2019-06-10, 2019-06-11 |

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2019-06-12 | 1.0 | False | 0.008 | 2.385244 |  | 2.385263 | -0.002 |
| 2019-06-19 | 2019-06-20 | 1.0 | False | 0.005 | 2.330001 | -5.524 | 2.33 | 0.0 |
| 2019-07-31 | 2019-08-01 | 1.0 | False | 0.004 | 2.135815 | -19.419 | 2.135 | 0.081 |
| 2019-09-18 | 2019-09-19 | 1.0 | False | 0.005 | 1.967886 | -16.793 | 1.9725 | -0.461 |
| 2019-10-30 | 2019-10-31 | 1.0 | False | 0.005 | 1.895889 | -7.2 | 1.895 | 0.089 |
| 2019-12-11 | 2019-12-12 | 1.0 | False | 0.004 | 1.75104 | -14.485 | 1.7555 | -0.446 |
| 2020-01-29 | 2020-01-30 | 1.0 | False | 0.005 | 1.684842 | -6.62 | 1.685 | -0.016 |
| 2020-03-18 | 2020-03-19 | 1.0 | False | 0.005 | 1.625996 | -5.885 | 1.625385 | 0.061 |
| 2020-04-29 | 2020-04-30 | 1.0 | False | 0.006 | 1.595132 | -3.086 | 1.595 | 0.013 |
| 2020-06-10 | 2020-06-11 | 1.0 | False | 0.008 | 1.54784 | -4.729 | 1.55 | -0.216 |
| 2020-07-29 | 2020-07-30 | 1.0 | False | 0.01 | 1.514614 | -3.323 | 1.515 | -0.039 |
| 2020-09-16 | 2020-09-17 | 1.0 | False | 0.013 | 1.474545 | -4.007 | 1.475 | -0.046 |
| 2020-11-05 | 2020-11-06 | 1.0 | False | 0.023 | 1.456018 | -1.853 | 1.457 | -0.098 |
| 2020-12-16 | 2020-12-17 | 1.0 | False | 0.023 | 1.436347 | -1.967 | 1.4322 | 0.415 |
| 2021-01-27 | 2021-01-28 | 1.0 | False | 0.02 | 1.419467 | -1.688 | 1.42 | -0.053 |
| 2021-03-17 | 2021-03-18 | 1.0 | False | 0.022 | 1.434369 | 1.49 | 1.431071 | 0.33 |
| 2021-04-28 | 2021-04-29 | 1.0 | False | 0.022 | 1.435039 | 0.067 | 1.435 | 0.004 |
| 2021-06-16 | 2021-06-17 | 0.0 | True | 0.023 | 1.435039 | 0.0 |  |  |
| 2021-07-28 | 2021-07-29 | 0.0 | True | 0.023 | 1.435039 | 0.0 |  |  |
| 2021-09-22 | 2021-09-23 | 0.0 | True | 0.024 | 1.435039 | 0.0 |  |  |
| 2021-11-03 | 2021-11-04 | 0.0 | True | 0.024 | 1.435039 | 0.0 |  |  |
| 2021-12-15 | 2021-12-16 | 0.0 | True | 0.025 | 1.435039 | 0.0 |  |  |
| 2022-01-26 | 2022-01-27 | 0.0 | True | 0.025 | 1.435039 | 0.0 |  |  |
| 2022-03-16 | 2022-03-17 | 0.0 | True | 0.026 | 1.435039 | 0.0 |  |  |
| 2022-05-04 | 2022-05-05 | 0.0 | True | 0.026 | 1.435039 | 0.0 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_fut | ff_fut 2019-06 | 2.364999999999995 | used |
| effr_fut | ff_fut 2019-07 | 2.3299999999999983 | used |
| effr_fut | ff_fut 2019-08 | 2.135000000000005 | used |
| effr_fut | ff_fut 2019-09 | 2.069999999999993 | used |
| effr_fut | ff_fut 2019-10 | 1.9650000000000034 | used |
| effr_fut | ff_fut 2019-11 | 1.894999999999996 | used |
| effr_fut | ff_fut 2019-12 | 1.8050000000000068 | used |
| effr_fut | ff_fut 2020-01 | 1.7450000000000045 | used |
| effr_fut | ff_fut 2020-02 | 1.6850000000000023 | used |
| effr_fut | ff_fut 2020-03 | 1.6599999999999966 | used |
| effr_fut | ff_fut 2020-04 | 1.625 | used |
| effr_fut | ff_fut 2020-05 | 1.5949999999999989 | used |
| effr_fut | ff_fut 2020-06 | 1.5649999999999977 | used |
| effr_fut | ff_fut 2020-07 | 1.5450000000000017 | used |
| effr_fut | ff_fut 2020-08 | 1.5150000000000006 | used |
| effr_fut | ff_fut 2020-09 | 1.4950000000000045 | used |
| effr_fut | ff_fut 2020-10 | 1.4749999999999943 | used |
| effr_fut | ff_fut 2020-11 | 1.4599999999999937 | used |
| effr_fut | ff_fut 2020-12 | 1.4449999999999932 | used |
| effr_fut | ff_fut 2021-01 | 1.4350000000000023 | used |
| effr_fut | ff_fut 2021-02 | 1.4200000000000017 | used |
| effr_fut | ff_fut 2021-03 | 1.4249999999999972 | used |
| effr_fut | ff_fut 2021-04 | 1.4350000000000023 | used |
| effr_fut | ff_fut 2021-05 | 1.4350000000000023 | used |

Replica notes: ff_fut 2019-11: no new parcel; re-solved parcel 4 (2019-10-30); ff_fut 2020-02: no new parcel; re-solved parcel 6 (2020-01-29); ff_fut 2020-05: no new parcel; re-solved parcel 8 (2020-04-29); ff_fut 2020-08: no new parcel; re-solved parcel 10 (2020-07-29); ff_fut 2020-10: no new parcel; re-solved parcel 11 (2020-09-16); ff_fut 2021-02: no new parcel; re-solved parcel 14 (2021-01-27); ff_fut 2021-05: no new parcel; re-solved parcel 16 (2021-04-28)

## Curve `effr_ois` (ois_effr)

Fit: 18 quotes (0 dropped, 0 excluded by metadata), 3 IRLS iterations (converged); 26 parcels to 2022-06-23, 0 synthetic and 0 unscheduled meetings. Current implied O/N rate 2.3690 (replica 2.3696; stub prior 2.3700 from last fixing). WIRP replica reaches 9 meetings on 13 quotes.

### Meetings

| decision_date | synthetic | unscheduled | implied_rate | imp_rate_delta | n_moves | pct_move | replica_rate | fit_minus_replica_bp | implied_policy | cumulative_vs_target_bp | under_identified | posterior_sigma_bp | beyond_wirp_reach |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2019-06-19 | False | False | 2.335666 | -0.033315 | -0.1333 | -13.33 | 2.335111 | 0.056 |  |  | False | 0.005 | False |
| 2019-07-31 | False | False | 2.130966 | -0.238015 | -0.9521 | -81.88 | 2.130003 | 0.096 |  |  | False | 0.011 | False |
| 2019-09-18 | False | False | 1.975881 | -0.393099 | -1.5724 | -62.03 | 1.979869 | -0.399 |  |  | False | 0.024 | False |
| 2019-10-30 | False | False | 1.889304 | -0.479677 | -1.9187 | -34.63 | 1.878128 | 1.118 |  |  | False | 0.033 | False |
| 2019-12-11 | False | False | 1.754711 | -0.614269 | -2.4571 | -53.84 | 1.770664 | -1.595 |  |  | False | 0.037 | False |
| 2020-01-29 | False | False | 1.668083 | -0.700897 | -2.8036 | -34.65 | 1.660844 | 0.724 |  |  | False | 0.043 | False |
| 2020-03-18 | False | False | 1.614709 | -0.754272 | -3.0171 | -21.35 | 1.612954 | 0.175 |  |  | False | 0.062 | False |
| 2020-04-29 | False | False | 1.593932 | -0.775048 | -3.1002 | -8.31 | 1.593618 | 0.031 |  |  | False | 0.086 | False |
| 2020-06-10 | False | False | 1.55259 | -0.81639 | -3.2656 | -16.54 | 1.562144 | -0.955 |  |  | False | 0.505 | False |
| 2020-07-29 | False | False | 1.512273 | -0.856708 | -3.4268 | -16.13 |  |  |  |  | True | 0.156 | True |
| 2020-09-16 | False | False | 1.471958 | -0.897023 | -3.5881 | -16.13 |  |  |  |  | True | 0.196 | True |
| 2020-11-05 | False | False | 1.431646 | -0.937335 | -3.7493 | -16.12 |  |  |  |  | True | 0.545 | True |
| 2020-12-16 | False | False | 1.425402 | -0.943578 | -3.7743 | -2.5 |  |  |  |  | True | 0.325 | True |
| 2021-01-27 | False | False | 1.419167 | -0.949813 | -3.7993 | -2.49 |  |  |  |  | True | 0.107 | True |
| 2021-03-17 | False | False | 1.412944 | -0.956036 | -3.8241 | -2.49 |  |  |  |  | True | 0.12 | True |
| 2021-04-28 | False | False | 1.406729 | -0.962251 | -3.849 | -2.49 |  |  |  |  | True | 0.34 | True |
| 2021-06-16 | False | False | 1.423335 | -0.945646 | -3.7826 | 6.64 |  |  |  |  | True | 0.264 | True |
| 2021-07-28 | False | False | 1.439934 | -0.929046 | -3.7162 | 6.64 |  |  |  |  | True | 0.189 | True |
| 2021-09-22 | False | False | 1.456525 | -0.912455 | -3.6498 | 6.64 |  |  |  |  | True | 0.115 | True |
| 2021-11-03 | False | False | 1.473105 | -0.895876 | -3.5835 | 6.63 |  |  |  |  | True | 0.047 | True |
| 2021-12-15 | False | False | 1.489673 | -0.879308 | -3.5172 | 6.63 |  |  |  |  | True | 0.054 | True |
| 2022-01-26 | False | False | 1.506229 | -0.862751 | -3.451 | 6.62 |  |  |  |  | True | 0.126 | True |
| 2022-03-16 | False | False | 1.522777 | -0.846204 | -3.3848 | 6.62 |  |  |  |  | True | 0.205 | True |
| 2022-05-04 | False | False | 1.539319 | -0.829661 | -3.3186 | 6.62 |  |  |  |  | True | 0.287 | True |
| 2022-06-15 | False | False | 1.539319 | -0.829661 | -3.3186 | 0.0 |  |  |  |  | True | 0.287 | True |

### Residuals (bp, quote - model)

| curve | instrument | status | n | mean_bp | rms_bp | max_abs_bp |
| --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | used | 18 | -0.0 | 0.058 | 0.135 |

### Drop list (dropped by the robust fit, excluded by metadata, skipped)

_none_

### High-leverage quotes (each alone pins a parcel; read the leave-one-out residual)

| curve | instrument | contract | ticker | quote_rate | residual_bp | loo_residual_bp | leverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| effr_ois | ois_effr | 1W | USSO1Z Curncy | 2.3651 | 0.048 | 0.492 | 0.903 |
| effr_ois | ois_effr | 1Y | USSO1 Curncy | 1.89194 | 0.003 | 0.046 | 0.94 |
| effr_ois | ois_effr | 18M | USSO1F Curncy | 1.76202 | 0.0 | 0.188 | 0.999 |
| effr_ois | ois_effr | 2Y | USSO2 Curncy | 1.68138 | -0.001 | -0.894 | 0.999 |
| effr_ois | ois_effr | 3Y | USSO3 Curncy | 1.619 | 0.0 | 2.569 | 1.0 |

### Stale and outside-listing inputs

_none_

### Parcels: identification, prior vs fitted vs replica

| parcel | start | identification | under_identified | posterior_sigma_bp | fitted_rate | step_bp | replica_rate | fit_minus_replica_bp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stub | 2019-06-12 | 1.0 | False | 0.006 | 2.368981 |  | 2.369633 | -0.065 |
| 2019-06-19 | 2019-06-20 | 1.0 | False | 0.005 | 2.335666 | -3.331 | 2.335111 | 0.056 |
| 2019-07-31 | 2019-08-01 | 1.0 | False | 0.011 | 2.130966 | -20.47 | 2.130003 | 0.096 |
| 2019-09-18 | 2019-09-19 | 1.0 | False | 0.024 | 1.975881 | -15.508 | 1.979869 | -0.399 |
| 2019-10-30 | 2019-10-31 | 1.0 | False | 0.033 | 1.889304 | -8.658 | 1.878128 | 1.118 |
| 2019-12-11 | 2019-12-12 | 1.0 | False | 0.037 | 1.754711 | -13.459 | 1.770664 | -1.595 |
| 2020-01-29 | 2020-01-30 | 1.0 | False | 0.043 | 1.668083 | -8.663 | 1.660844 | 0.724 |
| 2020-03-18 | 2020-03-19 | 1.0 | False | 0.062 | 1.614709 | -5.337 | 1.612954 | 0.175 |
| 2020-04-29 | 2020-04-30 | 1.0 | False | 0.086 | 1.593932 | -2.078 | 1.593618 | 0.031 |
| 2020-06-10 | 2020-06-11 | 1.0 | False | 0.505 | 1.55259 | -4.134 | 1.562144 | -0.955 |
| 2020-07-29 | 2020-07-30 | 0.3785 | True | 0.156 | 1.512273 | -4.032 |  |  |
| 2020-09-16 | 2020-09-17 | 0.3941 | True | 0.196 | 1.471958 | -4.031 |  |  |
| 2020-11-05 | 2020-11-06 | 0.2283 | True | 0.545 | 1.431646 | -4.031 |  |  |
| 2020-12-16 | 2020-12-17 | 0.2191 | True | 0.325 | 1.425402 | -0.624 |  |  |
| 2021-01-27 | 2021-01-28 | 0.2982 | True | 0.107 | 1.419167 | -0.623 |  |  |
| 2021-03-17 | 2021-03-18 | 0.2191 | True | 0.12 | 1.412944 | -0.622 |  |  |
| 2021-04-28 | 2021-04-29 | 0.2631 | True | 0.34 | 1.406729 | -0.621 |  |  |
| 2021-06-16 | 2021-06-17 | 0.1063 | True | 0.264 | 1.423335 | 1.661 |  |  |
| 2021-07-28 | 2021-07-29 | 0.1889 | True | 0.189 | 1.439934 | 1.66 |  |  |
| 2021-09-22 | 2021-09-23 | 0.1063 | True | 0.115 | 1.456525 | 1.659 |  |  |
| 2021-11-03 | 2021-11-04 | 0.1063 | True | 0.047 | 1.473105 | 1.658 |  |  |
| 2021-12-15 | 2021-12-16 | 0.1063 | True | 0.054 | 1.489673 | 1.657 |  |  |
| 2022-01-26 | 2022-01-27 | 0.1446 | True | 0.126 | 1.506229 | 1.656 |  |  |
| 2022-03-16 | 2022-03-17 | 0.1446 | True | 0.205 | 1.522777 | 1.655 |  |  |
| 2022-05-04 | 2022-05-05 | 0.0964 | True | 0.287 | 1.539319 | 1.654 |  |  |
| 2022-06-15 | 2022-06-16 | 0.0 | True | 0.287 | 1.539319 | 0.0 |  |  |

### WIRP replica inputs

| curve | key | quote | status |
| --- | --- | --- | --- |
| effr_ois | ois_effr 1W | 2.3651 | used |
| effr_ois | ois_effr 1M | 2.344 | used |
| effr_ois | ois_effr 2M | 2.301 | used |
| effr_ois | ois_effr 3M | 2.24335 | used |
| effr_ois | ois_effr 4M | 2.188 | used |
| effr_ois | ois_effr 5M | 2.141 | used |
| effr_ois | ois_effr 6M | 2.098 | used |
| effr_ois | ois_effr 7M | 2.055 | used |
| effr_ois | ois_effr 8M | 2.013 | used |
| effr_ois | ois_effr 9M | 1.978 | used |
| effr_ois | ois_effr 10M | 1.94619 | used |
| effr_ois | ois_effr 11M | 1.918 | used |
| effr_ois | ois_effr 1Y | 1.89194 | used |

Replica notes: ois_effr 3M: no new parcel; re-solved parcel 2 (2019-07-31); ois_effr 7M: no new parcel; re-solved parcel 5 (2019-12-11); ois_effr 9M: no new parcel; re-solved parcel 6 (2020-01-29)

## FF / OIS basis (bp, fit and replica)

| decision_date | effective_date | parcel | effr_fut_fit | effr_ois_fit | basis_fit_bp | basis_replica_bp |
| --- | --- | --- | --- | --- | --- | --- |
| None | None | stub | 2.3852440172811704 | 2.3689805005934583 | 1.626 | 1.563 |
| 2019-06-19 | 2019-06-20 | 1 | 2.330001 | 2.335666 | -0.566 | -0.511 |
| 2019-07-31 | 2019-08-01 | 2 | 2.135815 | 2.130966 | 0.485 | 0.5 |
| 2019-09-18 | 2019-09-19 | 3 | 1.967886 | 1.975881 | -0.8 | -0.737 |
| 2019-10-30 | 2019-10-31 | 4 | 1.895889 | 1.889304 | 0.659 | 1.687 |
| 2019-12-11 | 2019-12-12 | 5 | 1.75104 | 1.754711 | -0.367 | -1.516 |
| 2020-01-29 | 2020-01-30 | 6 | 1.684842 | 1.668083 | 1.676 | 2.416 |
| 2020-03-18 | 2020-03-19 | 7 | 1.625996 | 1.614709 | 1.129 | 1.243 |
| 2020-04-29 | 2020-04-30 | 8 | 1.595132 | 1.593932 | 0.12 | 0.138 |
| 2020-06-10 | 2020-06-11 | 9 | 1.54784 | 1.55259 | -0.475 | -1.214 |
| 2020-07-29 | 2020-07-30 | 10 | 1.514614 | 1.512273 | 0.234 |  |
| 2020-09-16 | 2020-09-17 | 11 | 1.474545 | 1.471958 | 0.259 |  |
| 2020-11-05 | 2020-11-06 | 12 | 1.456018 | 1.431646 | 2.437 |  |
| 2020-12-16 | 2020-12-17 | 13 | 1.436347 | 1.425402 | 1.094 |  |
| 2021-01-27 | 2021-01-28 | 14 | 1.419467 | 1.419167 | 0.03 |  |
| 2021-03-17 | 2021-03-18 | 15 | 1.434369 | 1.412944 | 2.142 |  |
| 2021-04-28 | 2021-04-29 | 16 | 1.435039 | 1.406729 | 2.831 |  |
| 2021-06-16 | 2021-06-17 | 17 | 1.435039 | 1.423335 | 1.17 |  |
| 2021-07-28 | 2021-07-29 | 18 | 1.435039 | 1.439934 | -0.49 |  |
| 2021-09-22 | 2021-09-23 | 19 | 1.435039 | 1.456525 | -2.149 |  |
| 2021-11-03 | 2021-11-04 | 20 | 1.435039 | 1.473105 | -3.807 |  |
| 2021-12-15 | 2021-12-16 | 21 | 1.435039 | 1.489673 | -5.463 |  |
| 2022-01-26 | 2022-01-27 | 22 | 1.435039 | 1.506229 | -7.119 |  |
| 2022-03-16 | 2022-03-17 | 23 | 1.435039 | 1.522777 | -8.774 |  |
| 2022-05-04 | 2022-05-05 | 24 | 1.435039 | 1.539319 | -10.428 |  |

## Stub

| curve | as_of | current_implied | replica_current_implied | stub_prior | stub_prior_source | anchor | spread | spread_median | spread_winsorised_mean | spread_obs | spread_estimator | spread_note | wirp_reach_meetings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| effr_fut | 2019-06-12 | 2.385244 | 2.385263 | 2.37 | last fixing | 2.375 | None | None | None | 0 | winsorised_mean | 0 fixings in the window (< 20) | 16 |
| effr_ois | 2019-06-12 | 2.368981 | 2.369633 | 2.37 | last fixing | 2.375 | None | None | None | 0 | winsorised_mean | 0 fixings in the window (< 20) | 9 |
