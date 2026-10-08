"""Business-day calendars.

Design
------
* Five named calendars: ``us_fed`` (Federal Reserve Banks), ``us_sifma``
  (US government-securities market; SOFR publication days), ``target``
  (TARGET2/T2), ``uk`` (England & Wales bank holidays), ``jp`` (Japan,
  including the 31 Dec / 2-3 Jan banking closures).
* Each calendar = weekend rule + holiday set. The holiday set is the union
  of (a) a rule-based generator in this file and (b) the committed CSV
  ``data/refdata/holidays/<name>.csv`` written by the updaters from official
  sources. Where the two disagree the CSV wins for the dates it covers
  (``source != 'rule'`` rows), so an official publication always overrides
  a rule.
* Date arithmetic: ``adjust`` (following / modified following / preceding),
  ``add_tenor`` with end-of-month handling, ``business_days_between``.

QuantLib calendars are deliberately not a dependency; ``tests/test_calendars``
cross-checks against QuantLib when it is installed.
"""
from __future__ import annotations

import csv
import datetime as dt
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from .. import REFDATA_DIR

MON, TUE, WED, THU, FRI, SAT, SUN = range(7)

CALENDAR_NAMES = ("us_fed", "us_sifma", "target", "uk", "jp")


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def easter_sunday(year: int) -> dt.date:
    """Gregorian Easter (Meeus/Jones/Butcher)."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return dt.date(year, month, day)


def nth_weekday(year: int, month: int, weekday: int, n: int) -> dt.date:
    """n-th (1-based) given weekday of a month; n=-1 means last."""
    if n > 0:
        first = dt.date(year, month, 1)
        offset = (weekday - first.weekday()) % 7
        return first + dt.timedelta(days=offset + 7 * (n - 1))
    last = (dt.date(year + (month == 12), (month % 12) + 1, 1) - dt.timedelta(days=1))
    offset = (last.weekday() - weekday) % 7
    return last - dt.timedelta(days=offset)


def _observed_sunday_to_monday(d: dt.date) -> dt.date:
    return d + dt.timedelta(days=1) if d.weekday() == SUN else d


def _observed_us_federal(d: dt.date) -> dt.date | None:
    """Federal Reserve observance: Sunday -> Monday; Saturday -> not observed."""
    if d.weekday() == SUN:
        return d + dt.timedelta(days=1)
    if d.weekday() == SAT:
        return None
    return d


# ---------------------------------------------------------------------------
# rule-based generators (fallbacks; official CSVs override)
# ---------------------------------------------------------------------------
def rules_us_fed(year: int) -> dict[dt.date, str]:
    """Federal Reserve Bank holidays (Fedwire / EFFR publication days)."""
    fixed = {
        (1, 1): "New Year's Day",
        (7, 4): "Independence Day",
        (11, 11): "Veterans Day",
        (12, 25): "Christmas Day",
    }
    if year >= 2022:
        fixed[(6, 19)] = "Juneteenth"
    out: dict[dt.date, str] = {}
    for (m, d), name in fixed.items():
        obs = _observed_us_federal(dt.date(year, m, d))
        if obs is not None:
            out[obs] = name
    out[nth_weekday(year, 1, MON, 3)] = "Martin Luther King Jr. Day"
    out[nth_weekday(year, 2, MON, 3)] = "Presidents Day"
    out[nth_weekday(year, 5, MON, -1)] = "Memorial Day"
    out[nth_weekday(year, 9, MON, 1)] = "Labor Day"
    out[nth_weekday(year, 10, MON, 2)] = "Columbus Day"
    out[nth_weekday(year, 11, THU, 4)] = "Thanksgiving Day"
    return out


def rules_us_sifma(year: int) -> dict[dt.date, str]:
    """SIFMA recommended full-close days (US Treasury / repo market; SOFR).

    Federal holidays plus Good Friday. SIFMA has at times recommended an
    early close rather than a full close on Good Friday (e.g. when it
    coincides with a payroll release); the official SIFMA CSV written by the
    updater overrides this rule for those years.
    """
    out = dict(rules_us_fed(year))
    out[easter_sunday(year) - dt.timedelta(days=2)] = "Good Friday"
    # Saturday holidays: SIFMA generally recommends the preceding Friday
    # (e.g. 3 Jul 2026). Encoded here; override via CSV if SIFMA differs.
    for m, d, name in ((1, 1, "New Year's Day (observed)"), (7, 4, "Independence Day (observed)"),
                       (11, 11, "Veterans Day (observed)"), (12, 25, "Christmas Day (observed)"),
                       (6, 19, "Juneteenth (observed)")):
        if (m, d) == (6, 19) and year < 2022:
            continue
        day = dt.date(year, m, d)
        if day.weekday() == SAT:
            out[day - dt.timedelta(days=1)] = name
    return out


def rules_target(year: int) -> dict[dt.date, str]:
    """TARGET2 / T2 closing days (stable since 2002)."""
    e = easter_sunday(year)
    return {
        dt.date(year, 1, 1): "New Year's Day",
        e - dt.timedelta(days=2): "Good Friday",
        e + dt.timedelta(days=1): "Easter Monday",
        dt.date(year, 5, 1): "Labour Day",
        dt.date(year, 12, 25): "Christmas Day",
        dt.date(year, 12, 26): "Christmas Holiday",
    }


def rules_uk(year: int) -> dict[dt.date, str]:
    """England & Wales bank holidays. gov.uk JSON (updater) is authoritative."""
    e = easter_sunday(year)
    out: dict[dt.date, str] = {}
    ny = dt.date(year, 1, 1)
    out[ny + dt.timedelta(days={SAT: 2, SUN: 1}.get(ny.weekday(), 0))] = "New Year's Day"
    out[e - dt.timedelta(days=2)] = "Good Friday"
    out[e + dt.timedelta(days=1)] = "Easter Monday"
    # Early May: first Monday, with one-off moves
    if year == 2020:
        out[dt.date(2020, 5, 8)] = "Early May bank holiday (VE Day)"
    elif year == 1995:
        out[dt.date(1995, 5, 8)] = "Early May bank holiday (VE Day)"
    else:
        out[nth_weekday(year, 5, MON, 1)] = "Early May bank holiday"
    # Spring: last Monday in May, with jubilee moves
    if year == 2022:
        out[dt.date(2022, 6, 2)] = "Spring bank holiday"
        out[dt.date(2022, 6, 3)] = "Platinum Jubilee bank holiday"
    elif year == 2012:
        out[dt.date(2012, 6, 4)] = "Spring bank holiday"
        out[dt.date(2012, 6, 5)] = "Diamond Jubilee bank holiday"
    else:
        out[nth_weekday(year, 5, MON, -1)] = "Spring bank holiday"
    out[nth_weekday(year, 8, MON, -1)] = "Summer bank holiday"
    # Christmas / Boxing Day with substitute days
    xmas, box = dt.date(year, 12, 25), dt.date(year, 12, 26)
    if xmas.weekday() == SAT:
        out[dt.date(year, 12, 27)] = "Christmas Day (substitute)"
        out[dt.date(year, 12, 28)] = "Boxing Day (substitute)"
    elif xmas.weekday() == SUN:
        out[dt.date(year, 12, 26)] = "Boxing Day"
        out[dt.date(year, 12, 27)] = "Christmas Day (substitute)"
    elif xmas.weekday() == FRI:
        out[xmas] = "Christmas Day"
        out[dt.date(year, 12, 28)] = "Boxing Day (substitute)"
    else:
        out[xmas] = "Christmas Day"
        out[box] = "Boxing Day"
    one_offs = {
        2011: [(dt.date(2011, 4, 29), "Royal Wedding")],
        2022: [(dt.date(2022, 9, 19), "State Funeral of Queen Elizabeth II")],
        2023: [(dt.date(2023, 5, 8), "Coronation of King Charles III")],
    }
    for d, name in one_offs.get(year, []):
        out[d] = name
    return out


def _jp_equinox(year: int, spring: bool) -> dt.date:
    """Approximate vernal/autumnal equinox day (valid 1980–2099)."""
    if spring:
        day = int(20.8431 + 0.242194 * (year - 1980) - (year - 1980) // 4)
        return dt.date(year, 3, day)
    day = int(23.2488 + 0.242194 * (year - 1980) - (year - 1980) // 4)
    return dt.date(year, 9, day)


def rules_jp(year: int) -> dict[dt.date, str]:
    """Japanese public holidays plus banking closures (31 Dec, 2–3 Jan).

    Cabinet Office CSV (updater) is authoritative for public holidays; this
    generator covers the standard rules and the 2019–2021 one-offs so the
    calendar is usable before the first updater run.
    """
    out: dict[dt.date, str] = {
        dt.date(year, 1, 1): "New Year's Day",
        dt.date(year, 1, 2): "Bank Holiday",
        dt.date(year, 1, 3): "Bank Holiday",
        dt.date(year, 12, 31): "Bank Holiday",
        nth_weekday(year, 1, MON, 2): "Coming of Age Day",
        dt.date(year, 2, 11): "National Foundation Day",
        _jp_equinox(year, True): "Vernal Equinox Day",
        dt.date(year, 4, 29): "Showa Day",
        dt.date(year, 5, 3): "Constitution Memorial Day",
        dt.date(year, 5, 4): "Greenery Day",
        dt.date(year, 5, 5): "Children's Day",
        nth_weekday(year, 9, MON, 3): "Respect for the Aged Day",
        _jp_equinox(year, False): "Autumnal Equinox Day",
        dt.date(year, 11, 3): "Culture Day",
        dt.date(year, 11, 23): "Labour Thanksgiving Day",
    }
    # Emperor's Birthday: 23 Dec until 2018, none in 2019, 23 Feb from 2020
    if year <= 2018:
        out[dt.date(year, 12, 23)] = "Emperor's Birthday"
    elif year >= 2020:
        out[dt.date(year, 2, 23)] = "Emperor's Birthday"
    # Marine Day, Mountain Day, Sports Day with Olympic-year moves
    marine = {2020: dt.date(2020, 7, 23), 2021: dt.date(2021, 7, 22)}.get(year, nth_weekday(year, 7, MON, 3))
    out[marine] = "Marine Day"
    if year >= 2016:
        mountain = {2020: dt.date(2020, 8, 10), 2021: dt.date(2021, 8, 8)}.get(year, dt.date(year, 8, 11))
        out[mountain] = "Mountain Day"
    sports = {2020: dt.date(2020, 7, 24), 2021: dt.date(2021, 7, 23)}.get(year, nth_weekday(year, 10, MON, 2))
    out[sports] = "Sports Day" if year >= 2020 else "Health and Sports Day"
    if year == 2019:
        out[dt.date(2019, 5, 1)] = "Enthronement Day"
        out[dt.date(2019, 10, 22)] = "Enthronement Ceremony"
    # Substitute holidays: a public holiday on Sunday moves to the next
    # non-holiday weekday. Bank-only closures (2-3 Jan, 31 Dec) do not.
    public = {d: n for d, n in out.items() if n != "Bank Holiday"}
    for d, name in list(public.items()):
        if d.weekday() == SUN:
            sub = d + dt.timedelta(days=1)
            while sub in public:
                sub += dt.timedelta(days=1)
            out[sub] = f"{name} (substitute)"
            public[sub] = out[sub]
    # Citizens' holiday: a weekday sandwiched between two public holidays
    days = sorted(public)
    for a, b in zip(days, days[1:]):
        if (b - a).days == 2:
            mid = a + dt.timedelta(days=1)
            if mid.weekday() < SAT and mid not in out:
                out[mid] = "Citizens' Holiday"
    return out


RULES = {
    "us_fed": rules_us_fed,
    "us_sifma": rules_us_sifma,
    "target": rules_target,
    "uk": rules_uk,
    "jp": rules_jp,
}


# ---------------------------------------------------------------------------
# Calendar object
# ---------------------------------------------------------------------------
@dataclass
class Calendar:
    name: str
    holidays: dict[dt.date, str] = field(default_factory=dict)
    weekend: tuple[int, ...] = (SAT, SUN)

    # --- construction -------------------------------------------------------
    @classmethod
    def from_rules(cls, name: str, years: Iterable[int]) -> "Calendar":
        rule = RULES[name]
        hol: dict[dt.date, str] = {}
        for y in years:
            hol.update(rule(y))
        return cls(name, hol)

    @classmethod
    def load(cls, name: str, years: Iterable[int] = range(2005, 2036),
             refdata_dir: Path = REFDATA_DIR) -> "Calendar":
        """Rules for ``years`` merged with the committed CSV (CSV wins)."""
        cal = cls.from_rules(name, years)
        path = refdata_dir / "holidays" / f"{name}.csv"
        if path.exists():
            with path.open(newline="", encoding="utf-8") as fh:
                for row in csv.DictReader(fh):
                    d = dt.date.fromisoformat(row["date"])
                    if row.get("is_holiday", "1") in ("0", "false", "False"):
                        cal.holidays.pop(d, None)   # explicit override: working day
                    else:
                        cal.holidays[d] = row.get("name", "")
        return cal

    # --- queries ------------------------------------------------------------
    def is_business_day(self, d: dt.date) -> bool:
        return d.weekday() not in self.weekend and d not in self.holidays

    def adjust(self, d: dt.date, convention: str = "following") -> dt.date:
        """following | modified_following | preceding | unadjusted."""
        if convention == "unadjusted" or self.is_business_day(d):
            return d
        if convention == "preceding":
            return self.previous_business_day(d)
        nxt = self.next_business_day(d)
        if convention == "modified_following" and nxt.month != d.month:
            return self.previous_business_day(d)
        return nxt

    def next_business_day(self, d: dt.date, include: bool = False) -> dt.date:
        x = d if include else d + dt.timedelta(days=1)
        while not self.is_business_day(x):
            x += dt.timedelta(days=1)
        return x

    def previous_business_day(self, d: dt.date, include: bool = False) -> dt.date:
        x = d if include else d - dt.timedelta(days=1)
        while not self.is_business_day(x):
            x -= dt.timedelta(days=1)
        return x

    def advance_business_days(self, d: dt.date, n: int) -> dt.date:
        x = d
        step = 1 if n >= 0 else -1
        for _ in range(abs(n)):
            x = self.next_business_day(x) if step > 0 else self.previous_business_day(x)
        return x

    def business_days_between(self, start: dt.date, end: dt.date) -> int:
        """Count business days in [start, end)."""
        n, x = 0, start
        while x < end:
            n += self.is_business_day(x)
            x += dt.timedelta(days=1)
        return n

    def business_days(self, start: dt.date, end: dt.date) -> list[dt.date]:
        """All business days in [start, end]."""
        out, x = [], start
        while x <= end:
            if self.is_business_day(x):
                out.append(x)
            x += dt.timedelta(days=1)
        return out

    # --- tenor arithmetic ---------------------------------------------------
    def add_tenor(self, d: dt.date, tenor: str, convention: str = "modified_following",
                  eom: bool = True) -> dt.date:
        """Add a tenor such as '1W', '3M', '1Y', '15M', '1Y3M', '2D'.

        End-of-month rule: if ``d`` is the last business day of its month and
        the tenor is in months/years, the result is the last business day of
        the target month (ISDA EOM convention).
        """
        months, days, weeks = parse_tenor(tenor)
        x = d
        if weeks:
            x = x + dt.timedelta(weeks=weeks)
        if days:
            x = self.advance_business_days(x, days)
        if months:
            is_eom = eom and self.is_business_day(d) and self.next_business_day(d).month != d.month
            x = add_months(x, months)
            if is_eom:
                x = end_of_month(x)
                return self.adjust(x, "preceding")
        return self.adjust(x, convention)

    # --- io -----------------------------------------------------------------
    def write_csv(self, path: Path, source: str | dict[dt.date, str] = "rule") -> None:
        """``source``: one label for every row, or a per-date mapping (missing dates: 'rule')."""
        with path.open("w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh, lineterminator="\n")
            w.writerow(["date", "name", "calendar", "source"])
            for d in sorted(self.holidays):
                src = source.get(d, "rule") if isinstance(source, dict) else source
                w.writerow([d.isoformat(), self.holidays[d], self.name, src])


# ---------------------------------------------------------------------------
# plain-date helpers
# ---------------------------------------------------------------------------
def parse_tenor(tenor: str) -> tuple[int, int, int]:
    """Return (months, business_days, weeks) for tenors like '1Y3M', '2W', '3D', 'ON'."""
    t = tenor.strip().upper()
    if t in ("ON", "O/N", "TN", "T/N"):
        return 0, 1, 0
    months = days = weeks = 0
    num = ""
    for ch in t:
        if ch.isdigit():
            num += ch
        else:
            n = int(num or 0)
            num = ""
            if ch == "Y":
                months += 12 * n
            elif ch == "M":
                months += n
            elif ch == "W":
                weeks += n
            elif ch == "D":
                days += n
            else:
                raise ValueError(f"bad tenor {tenor!r}")
    if num:
        raise ValueError(f"bad tenor {tenor!r}")
    return months, days, weeks


def add_months(d: dt.date, months: int) -> dt.date:
    y, m = divmod(d.month - 1 + months, 12)
    y += d.year
    m += 1
    last = (dt.date(y + (m == 12), (m % 12) + 1, 1) - dt.timedelta(days=1)).day
    return dt.date(y, m, min(d.day, last))


def end_of_month(d: dt.date) -> dt.date:
    return dt.date(d.year + (d.month == 12), (d.month % 12) + 1, 1) - dt.timedelta(days=1)


def third_wednesday(year: int, month: int) -> dt.date:
    """IMM date."""
    return nth_weekday(year, month, WED, 3)
