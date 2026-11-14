#!/usr/bin/env python3
"""Verify Batch 63 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0007", "0009", "0010", "0011", "0012", "0013", "0014", "0015", "0016", "0017"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 63 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0007", "0010", "0012", "0016"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_0007"]["perSide"]
        and catalog["dataset_1324_0010"]["requiredEquipment"] == ["单杠"]
        and catalog["dataset_1324_0012"]["perSide"]
        and catalog["dataset_1324_0016"]["perSide"]
        and not catalog["dataset_1324_0010"]["isHold"],
        "Required pull-up bar support and unilateral rep modes remain enforced after packaging",
    )
    print("ALL BATCH SIXTY-THREE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
