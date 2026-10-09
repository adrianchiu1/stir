"""Average-rate futures priced from a flat-forward curve.

One class for every futures contract settled on an overnight index over a
reference window: the accrual rule (``arithmetic_average`` for FF and SR1,
``compounded`` for SR3), the fixing calendar, the treatment of non-publication
days, the day count and the quote formula all come from the manifest entry;
the window comes from the contract table (``stircurve.marketdata.contracts``).
Nothing here knows about IMM dates, calendar months or ACT/360.

FF (CBOT Chapter 22): 100 minus the arithmetic average of the daily EFFR over
the calendar month, a non-publication day taking the last published rate.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from ..marketdata.contracts import Contract
from ..marketdata.manifest import Manifest

if TYPE_CHECKING:   # curves import the day counts from this package
    from ..curves.flat_forward import FlatForwardCurve, ParcelGrid, RateDays

ACCRUAL_PIECES = {"arithmetic_average": "calendar_day", "compounded": "business_day"}


def rate_from_price(quote: dict, price: float) -> float:
    """Quoted price -> rate (percent) under the manifest's quote convention."""
    if quote["convention"] == "price" and quote["formula"].replace(" ", "") == "100-rate":
        return 100.0 - price
    if quote["convention"] == "rate":
        return price
    raise ValueError(f"unsupported quote convention {quote}")


@dataclass
class BoundInstrument:
    """An instrument tied to a parcel grid: ``value(x)`` is its model rate (percent)."""
    rate_days: list[RateDays]
    _value: object

    def value(self, x: np.ndarray) -> float:
        return self._value(np.asarray(x, dtype=float))

    @property
    def missing_fixings(self) -> tuple:
        return tuple(sorted({d for rd in self.rate_days for d in rd.missing}))


class AverageRateFuture:
    def __init__(self, m: Manifest, instrument: str, contract: Contract):
        ins = m.instruments[instrument]
        if ins["kind"] != "future":
            raise ValueError(f"{instrument} is not a future")
        acc = ins["accrual"]
        if acc["rule"] not in ACCRUAL_PIECES:
            raise ValueError(f"{instrument}: accrual {acc['rule']!r} is not an overnight average")
        if acc.get("non_publication_days") != "previous_published":
            raise ValueError(f"{instrument}: non-publication rule {acc.get('non_publication_days')!r} not supported")
        self.instrument, self.contract = instrument, contract.contract
        self.accrual = acc["rule"]
        self.calendar = m.calendar(acc["fixing_calendar"])
        self.daycount = ins["daycount"]["name"]
        self.quote = ins["quote"]
        self.start, self.end = contract.ref_start, contract.ref_end

    def rate_from_quote(self, price: float) -> float:
        return rate_from_price(self.quote, price)

    def bind(self, grid: ParcelGrid) -> BoundInstrument:
        rd = grid.rate_days(self.start, self.end, self.calendar, self.daycount, ACCRUAL_PIECES[self.accrual])
        f = rd.average if self.accrual == "arithmetic_average" else rd.compounded
        return BoundInstrument([rd], f)

    def rate(self, curve: FlatForwardCurve) -> float:
        """Model rate (percent); the model price is 100 minus this for a '100 - rate' quote."""
        return self.bind(curve.grid).value(curve.rates)
