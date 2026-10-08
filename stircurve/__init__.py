"""stircurve — meeting-date aware STIR/OIS curve construction.

M0 scope (this version): reference data only — business-day calendars,
central-bank meeting schedules with effective-date rules and cadence
extrapolation, ECB reserve maintenance periods, policy-rate schedules,
and the deterministic updaters that refresh them from public sources.

Nothing in this package calls Bloomberg or any AI service.
"""
from pathlib import Path

__version__ = "0.0.1"

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
DATA_DIR = REPO_ROOT / "data"
REFDATA_DIR = DATA_DIR / "refdata"
