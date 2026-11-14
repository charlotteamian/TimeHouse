#!/usr/bin/env python3
"""Verify Batch 76 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0162", "0164", "0165", "0167", "0168", "0169", "0170", "0171", "0172", "0173"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 76 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0168", "0169", "0170", "0172"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_0168"]["perSide"]
        and catalog["dataset_1324_0169"]["requiredEquipment"] == ["上斜训练凳"]
        and catalog["dataset_1324_0170"]["requiredEquipment"] == ["瑜伽球"]
        and catalog["dataset_1324_0172"]["requiredEquipment"] == []
        and not catalog["dataset_1324_0169"]["isHold"],
        "Required incline bench and stability ball supports and unilateral rep modes remain enforced after packaging",
    )
    print("ALL BATCH SEVENTY-SIX FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
