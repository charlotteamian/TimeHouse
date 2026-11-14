#!/usr/bin/env python3
"""Verify Batch 115 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["1395", "1396", "1408", "1409", "1410", "1411", "1412", "1413", "1416", "1417"]
calf_ids = {"1395", "1396"}
glute_ids = {"1408", "1409", "1410", "1416", "1417"}
forearm_ids = {"1411", "1412"}
per_side_ids = {"1395", "1410", "1413", "1416", "1417"}
bilateral_ids = set(inspected) - per_side_ids
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 115 candidates stay out of the reviewed ledger")
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
        and catalog["dataset_1324_1396"]["requiredEquipment"] == ["稳固踏台"]
        and catalog["dataset_1324_1411"]["requiredEquipment"] == ["平板训练凳"]
        and catalog["dataset_1324_1412"]["requiredEquipment"] == ["平板训练凳"]
        and all(catalog["dataset_1324_" + x]["primary"] == ["小腿肌"] for x in calf_ids)
        and all(catalog["dataset_1324_" + x]["primary"] == ["臀肌"] for x in glute_ids)
        and all(catalog["dataset_1324_" + x]["primary"] == ["前臂"] for x in forearm_ids)
        and catalog["dataset_1324_1413"]["primary"] == ["肱二头肌"],
        "Unilateral pacing, supports, and primary muscles remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND FIFTEEN FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
