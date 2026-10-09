"""stircurve — meeting-date aware STIR/OIS curve construction.

M0: reference data (calendars, meetings and effective dates, ECB maintenance
periods, policy rates) and their deterministic updaters. M1: USD market-data
manifest, Bloomberg dump (scripts only) and CSV loader. M2: instrument models,
the flat-forward EFFR front end (robust IRLS, OIS-split prior), policy spread,
per-meeting outputs and the quality battery.

Nothing in this package calls Bloomberg or any AI service.
"""
from pathlib import Path

__version__ = "0.0.1"

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parent
DATA_DIR = REPO_ROOT / "data"
REFDATA_DIR = DATA_DIR / "refdata"
