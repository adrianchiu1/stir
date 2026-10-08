#!/usr/bin/env python
"""Minimal test runner for environments without pytest (pytest works too)."""
import importlib, inspect, sys, traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
failed = passed = 0
for p in sorted((Path(__file__).resolve().parents[1] / "tests").glob("test_*.py")):
    mod = importlib.import_module(f"tests.{p.stem}")
    for name, fn in inspect.getmembers(mod, inspect.isfunction):
        if name.startswith("test_"):
            try:
                fn(); passed += 1; print(f"PASS {p.stem}.{name}")
            except Exception:
                failed += 1; print(f"FAIL {p.stem}.{name}"); traceback.print_exc()
print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
