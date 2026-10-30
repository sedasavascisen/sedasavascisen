"""
mumiso
------
MU-MISO extension: N_t-antenna BS, K single-antenna users, N-element RIS.

The rest of `ris_mu` models a single-antenna BS, where the users share one
surface but the BS cannot separate them at all -- there is no precoder and
no interference term, only K conflicting alignments. This subpackage adds
the transmit array, so interference becomes real and the fairness problem
acquires the structure a multi-user downlink actually has.

The single-antenna code is left untouched: it reproduces the published
results and is not the place to take risks.
"""
