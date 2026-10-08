"""Load + save must reproduce the committed reference files byte for byte,
so an updater --commit only shows real changes in the git diff."""
import tempfile
from pathlib import Path

from stircurve import REFDATA_DIR
from stircurve.refdata.maintenance import (load_maintenance_periods, load_policy_rates, save_maintenance_periods,
                                           save_policy_rates)
from stircurve.refdata.meetings import BANKS, load_meetings, save_meetings


def test_refdata_roundtrip_is_byte_identical():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for bank in BANKS:
            for unsched in (False, True):
                ms = [m for m in load_meetings(bank, True, REFDATA_DIR) if m.scheduled != unsched]
                p = save_meetings(bank, ms, unscheduled=unsched, refdata_dir=tmp)
                assert p.read_bytes() == (REFDATA_DIR / "meetings" / p.name).read_bytes(), p.name
            p = save_policy_rates(bank, load_policy_rates(bank, REFDATA_DIR), tmp)
            assert p.read_bytes() == (REFDATA_DIR / "policy_rates" / p.name).read_bytes(), p.name
        p = save_maintenance_periods(load_maintenance_periods(REFDATA_DIR), tmp)
        assert p.read_bytes() == (REFDATA_DIR / "maintenance_periods" / "ecb.csv").read_bytes()
