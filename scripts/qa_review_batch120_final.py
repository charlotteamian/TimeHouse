#!/usr/bin/env python3
"""Verify Batch 120 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["1634", "1635", "1636", "1637", "1638", "1639", "1640", "1641", "1642", "1643"]
per_side_ids = {"1635", "1640", "1642"}
bilateral_ids = set(inspected) - per_side_ids
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 139, "Bundled ledger keeps exact 139 reviewed items with zero auto-approvals for Batch 120")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 120 candidates stay out of the reviewed ledger")
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
        and catalog["dataset_1324_1634"]["requiredEquipment"] == ["平板训练凳"]
        and catalog["dataset_1324_1635"]["requiredEquipment"] == ["牧师凳"]
        and catalog["dataset_1324_1637"]["requiredEquipment"] == ["瑜伽球"]
        and catalog["dataset_1324_1639"]["requiredEquipment"] == ["牧师凳"]
        and catalog["dataset_1324_1640"]["requiredEquipment"] == ["牧师凳"]
        and catalog["dataset_1324_1641"]["requiredEquipment"] == ["直立靠背训练凳"]
        and catalog["dataset_1324_1642"]["requiredEquipment"] == ["平板训练凳"]
        and catalog["dataset_1324_1643"]["requiredEquipment"] == ["直立靠背训练凳"]
        and all(catalog["dataset_1324_" + x]["primary"] == ["肱二头肌"] for x in inspected),
        "Unilateral pacing, bench/ball supports, and biceps primary muscle remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND TWENTY FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
