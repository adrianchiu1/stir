"""Instrument models priced from a flat-forward curve (M2).

Every instrument is a window + accrual rule + day count + calendar + quote
convention read from the manifest (CLAUDE.md); nothing here hard-codes a
convention. ``AverageRateFuture`` covers FF (arithmetic average) and the SOFR
futures (SR1 arithmetic, SR3 compounded); ``OvernightIndexSwap`` the EFFR and
SOFR OIS.
"""
from .daycount import accrual_factor, year_fraction
from .futures import AverageRateFuture, BoundInstrument, rate_from_price
from .ois import OvernightIndexSwap

__all__ = ["AverageRateFuture", "BoundInstrument", "OvernightIndexSwap", "accrual_factor", "rate_from_price",
           "year_fraction"]
