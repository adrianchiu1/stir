"""Load per-currency YAML configs into plain dicts (validated lightly)."""
from __future__ import annotations

import datetime as dt
from pathlib import Path

import yaml

CONFIG_DIR = Path(__file__).resolve().parent
CURRENCIES = ("usd", "eur", "gbp", "jpy")
REQUIRED = ("currency", "bank", "calendar", "meetings", "policy_anchors", "families", "discount_schedule", "default_family_schedule")


def load_config(ccy: str) -> dict:
    p = CONFIG_DIR / f"{ccy.lower()}.yaml"
    with p.open(encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    missing = [k for k in REQUIRED if k not in cfg]
    if missing:
        raise ValueError(f"{p.name}: missing keys {missing}")
    for key in ("discount_schedule", "default_family_schedule", "policy_anchors"):
        for row in cfg[key]:
            row["from"] = dt.date.fromisoformat(str(row["from"]))
    return cfg


def in_effect(schedule: list[dict], day: dt.date, key: str) -> str:
    """Value of ``key`` from the latest schedule row with from <= day."""
    val = None
    for row in sorted(schedule, key=lambda r: r["from"]):
        if row["from"] <= day:
            val = row[key]
    if val is None:
        raise ValueError(f"no schedule row in effect on {day}")
    return val
