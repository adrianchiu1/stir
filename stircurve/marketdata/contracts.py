"""Contract-table generator: every listed futures contract with its reference
window, last trade date and settlement rule, from the manifest and the
committed calendars.

Rules are named in the manifest (``reference_window.rule``, ``last_trade.rule``,
...) and implemented here once; calendars always come from the manifest, so
nothing here assumes ACT/360, IMM dates or a US calendar.

Listing: on any day the exchange lists the nearest N contracts of the cycle
that have not passed their last trade date (N from the listing schedule in
force that day: ``months`` for monthly cycles, ``quarterly`` + ``serial`` for
the March cycle plus serial months; with ``serial_listed_until: reference_start``
the nearest serials are those whose reference period has not started). A contract is first listed on the first
such day it is among them: the business day after a contract expires, or a
schedule change. Contracts already listed when the first schedule row starts
get that date as a lower bound (``first_listed_lower_bound``) unless that row is
the product's launch (``launch: true``).
"""
from __future__ import annotations

import datetime as dt
from dataclasses import asdict, dataclass

import pandas as pd

from ..refdata.calendars import add_months, third_wednesday
from .manifest import Manifest, _date

QUARTERLY_MONTHS = (3, 6, 9, 12)


@dataclass(frozen=True)
class Contract:
    instrument: str
    contract: str                 # 'YYYY-MM' contract month as the exchange names it
    bbg_ticker: str               # canonical (two-digit year)
    cycle: str                    # monthly | quarterly | serial
    ref_start: dt.date            # inclusive
    ref_end: dt.date              # exclusive
    ref_end_inclusive: dt.date
    accrual_days: int
    last_trade: dt.date
    final_settlement: dt.date
    first_listed: dt.date
    first_listed_lower_bound: bool
    listing_verified: bool
    first_quote: dt.date          # max(first_listed, instrument first_date)
    last_quote: dt.date           # last trade, or the conversion date for converted contracts
    converted_on: dt.date | None
    settlement_rule: str


def _cal_name(ins: dict, name: str) -> str:
    return ins["exchange_calendar"] if name == "exchange" else name


def reference_window(m: Manifest, ins: dict, year: int, month: int) -> tuple[dt.date, dt.date]:
    rw = ins["reference_window"]
    rule = rw["rule"]
    if rule == "calendar_month":
        return dt.date(year, month, 1), add_months(dt.date(year, month, 1), 1)
    if rule == "imm_to_imm":
        start = third_wednesday(year, month)
        end_month = add_months(dt.date(year, month, 1), rw["months"])
        return start, third_wednesday(end_month.year, end_month.month)
    if rule == "imm_plus_tenor":
        start = third_wednesday(year, month)
        cal = m.calendar("+".join(rw["calendars"]))
        end = cal.add_tenor(start, rw["tenor"], convention=rw["adjust"], eom=False)
        return start, end
    raise ValueError(f"unknown reference_window rule {rule!r}")


def last_trade_date(m: Manifest, ins: dict, year: int, month: int, window: tuple[dt.date, dt.date]) -> dt.date:
    lt = ins["last_trade"]
    cal = m.calendar(_cal_name(ins, lt["calendar"]))
    rule = lt["rule"]
    if rule == "last_business_day_of_month":
        return cal.previous_business_day(add_months(dt.date(year, month, 1), 1))
    if rule == "business_days_before_window_end":
        return cal.advance_business_days(window[1], -lt["n"])
    if rule == "business_days_before_imm":
        return cal.advance_business_days(third_wednesday(year, month), -lt["n"])
    raise ValueError(f"unknown last_trade rule {rule!r}")


def final_settlement_date(m: Manifest, ins: dict, window: tuple[dt.date, dt.date], last_trade: dt.date) -> dt.date:
    fs = ins["final_settlement"]
    rule = fs["rule"]
    if rule == "publication_of_last_day_rate":
        # the rate applying to the window's last day is the last published one;
        # it is published on the next publication day
        cal = m.calendar(_cal_name(ins, fs["calendar"]))
        return cal.next_business_day(cal.previous_business_day(window[1]))
    if rule == "last_trade_day":
        return last_trade
    raise ValueError(f"unknown final_settlement rule {rule!r}")


def settlement_text(ins: dict) -> str:
    acc = ins["accrual"]
    how = {"arithmetic_average": "arithmetic average of daily", "compounded": "daily compounded",
           "term_fixing": "fixing of"}[acc["rule"]]
    return (f"100 - {how} {ins['index']} ({acc['fixing_calendar']}; {ins['daycount']['name']}) "
            f"over [ref_start, ref_end); final settlement: {ins['final_settlement']['rule']}")


def _cycle_kind(ins: dict, month: int) -> str:
    if ins["cycle"] == "monthly":
        return "monthly"
    return "quarterly" if month in QUARTERLY_MONTHS else "serial"


def _months(first: dt.date, last: dt.date):
    y, mo = first.year, first.month
    while (y, mo) <= (last.year, last.month):
        yield y, mo
        y, mo = (y + 1, 1) if mo == 12 else (y, mo + 1)


def listed_contracts(m: Manifest, instrument: str, until: dt.date, listing: str = "listing") -> list[Contract]:
    """Every contract of ``instrument`` first listed on or before ``until``.

    ``listing="dump_listing"`` uses the instrument's generous request horizon
    (what the Bloomberg dump asks for) instead of the exchange listing schedule."""
    ins = m.instruments[instrument]
    rows = ins.get(listing, ins["listing"])
    schedule = sorted(({**r, "from": _date(r["from"])} for r in rows), key=lambda r: r["from"])
    excal = m.calendar(ins["exchange_calendar"])
    horizon = max(max(r.get("months", 0), 3 * r.get("quarterly", 0) + 3) for r in schedule)
    start = add_months(schedule[0]["from"].replace(day=1), -12)
    end = add_months(until.replace(day=1), horizon + 3)

    # every candidate contract month with its dates
    cand = []
    for y, mo in _months(start, end):
        window = reference_window(m, ins, y, mo)
        cand.append((y, mo, window, last_trade_date(m, ins, y, mo, window)))
    cand.sort(key=lambda c: (c[3], c[0], c[1]))

    serial_by_start = ins.get("serial_listed_until") == "reference_start"

    def listed_on(day: dt.date, row: dict) -> list[tuple[int, int]]:
        alive = [(y, mo) for y, mo, _, lt in cand if lt >= day]
        if ins["cycle"] == "monthly":
            return alive[: row["months"]]
        q = [c for c in alive if c[1] in QUARTERLY_MONTHS][: row["quarterly"]]
        serial = [(y, mo) for y, mo, w, lt in cand if mo not in QUARTERLY_MONTHS
                  and (w[0] >= day if serial_by_start else lt >= day)]
        return q + serial[: row.get("serial", 0)]

    def row_on(day: dt.date) -> dict:
        return [r for r in schedule if r["from"] <= day][-1]

    events = {r["from"] for r in schedule}
    events |= {excal.next_business_day(lt) for *_, lt in cand if lt >= schedule[0]["from"]}
    if serial_by_start:
        events |= {excal.next_business_day(w[0]) for _, mo, w, _ in cand
                   if mo not in QUARTERLY_MONTHS and w[0] >= schedule[0]["from"]}
    first_seen: dict[tuple[int, int], tuple[dt.date, bool]] = {}
    for day in sorted(e for e in events if e <= until):
        row = row_on(day)
        for c in listed_on(day, row):
            if c not in first_seen:
                first_seen[c] = (day, bool(row.get("verified")))

    cessation = ins.get("cessation")
    first_date = _date(ins["first_date"])
    last_date = _date(ins.get("last_date"))
    out = []
    for y, mo, window, lt in cand:
        if (y, mo) not in first_seen:
            continue
        listed, verified = first_seen[(y, mo)]
        converted = None
        last_quote = lt
        if cessation and lt > _date(cessation["applies_if_last_trade_after"]):
            converted = _date(cessation["converted_on"])
            last_quote = converted
        if last_date and last_quote > last_date:
            last_quote = last_date
        out.append(Contract(
            instrument=instrument, contract=f"{y}-{mo:02d}", bbg_ticker=m.future_ticker(instrument, y, mo),
            cycle=_cycle_kind(ins, mo), ref_start=window[0], ref_end=window[1],
            ref_end_inclusive=window[1] - dt.timedelta(days=1), accrual_days=(window[1] - window[0]).days,
            last_trade=lt, final_settlement=final_settlement_date(m, ins, window, lt),
            first_listed=listed, first_listed_lower_bound=(listed == schedule[0]["from"] and not schedule[0].get("launch")),
            listing_verified=verified, first_quote=max(listed, first_date), last_quote=last_quote,
            converted_on=converted, settlement_rule=settlement_text(ins)))
    return out


def contract_table(m: Manifest, start: dt.date, end: dt.date, instruments: list[str] | None = None,
                   listing: str = "listing") -> pd.DataFrame:
    """Every futures contract quoted at some point in [start, end] (first_quote <= end,
    last_quote >= start), one row each, sorted by instrument and last trade."""
    rows = []
    for name in instruments or list(m.futures()):
        for c in listed_contracts(m, name, end, listing):
            if c.first_quote <= end and c.last_quote >= start and c.first_quote <= c.last_quote:
                rows.append(asdict(c))
    cols = list(Contract.__dataclass_fields__)
    df = pd.DataFrame(rows, columns=cols)
    return df.sort_values(["instrument", "last_trade", "contract"], ignore_index=True)
