#!/usr/bin/env python3
"""Verify Batch 114 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["1378", "1383", "1384", "1385", "1388", "1389", "1391", "1392", "1393", "1394"]
per_side_ids = {"1378", "1384", "1388", "1389", "1392", "1393"}
bilateral_ids = set(inspected) - per_side_ids
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 114 candidates stay out of the reviewed ledger")
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
        and catalog["dataset_1324_1394"]["requiredEquipment"] == ["稳固踏台"]
        and all(catalog["dataset_1324_" + x]["primary"] == ["小腿肌"] for x in inspected),
        "Unilateral pacing, step box support, and calves primary muscle remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND FOURTEEN FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
