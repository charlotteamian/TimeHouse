#!/usr/bin/env python3
"""Verify Batch 116 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["1420", "1425", "1426", "1431", "1432", "1433", "1434", "1435", "1436", "1438"]
glute_ids = {"1420", "1425", "1433", "1434", "1435", "1436"}
lat_ids = {"1431", "1432"}
per_side_ids = {"1425"}
bilateral_ids = set(inspected) - per_side_ids
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 116 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in inspected),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        not any(catalog["dataset_1324_" + x]["isHold"] for x in inspected)
        and all(catalog["dataset_1324_" + x]["perSide"] for x in per_side_ids)
        and all(not catalog["dataset_1324_" + x]["perSide"] for x in bilateral_ids)
        and catalog["dataset_1324_1426"]["requiredEquipment"] == ["平板训练凳"]
        and catalog["dataset_1324_1438"]["requiredEquipment"] == ["平板训练凳"]
        and all(catalog["dataset_1324_" + x]["primary"] == ["臀肌"] for x in glute_ids)
        and catalog["dataset_1324_1426"]["primary"] == ["前臂"]
        and all(catalog["dataset_1324_" + x]["primary"] == ["背阔肌"] for x in lat_ids)
        and catalog["dataset_1324_1438"]["primary"] == ["三角肌"],
        "Unilateral pacing, flat bench supports, and primary muscles remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND SIXTEEN FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
