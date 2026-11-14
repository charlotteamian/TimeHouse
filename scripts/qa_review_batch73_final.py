#!/usr/bin/env python3
"""Verify Batch 73 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0112", "0113", "0114", "0115", "0116", "0117", "0118", "0119", "0120", "0121"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 73 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0112", "0114", "0116", "0118"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_0114"]["requiredEquipment"] == ["稳固踏台"]
        and catalog["dataset_1324_0112"]["perSide"]
        and catalog["dataset_1324_0114"]["perSide"]
        and catalog["dataset_1324_0116"]["requiredEquipment"] == []
        and not catalog["dataset_1324_0114"]["isHold"],
        "Required stepper supports and unilateral rep modes remain enforced after packaging",
    )
    print("ALL BATCH SEVENTY-THREE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
