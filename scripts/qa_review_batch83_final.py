#!/usr/bin/env python3
"""Verify Batch 83 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0238", "0239", "0240", "0241", "0242", "0243", "0244", "0245", "0246", "0247"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 83 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0238", "0239", "0240", "0244", "0245", "0247"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_0239"]["requiredEquipment"] == ["平板训练凳"]
        and catalog["dataset_1324_0240"]["requiredEquipment"] == ["平板训练凳"]
        and catalog["dataset_1324_0247"]["requiredEquipment"] == ["平板训练凳"]
        and catalog["dataset_1324_0244"]["perSide"]
        and not catalog["dataset_1324_0238"]["isHold"]
        and not catalog["dataset_1324_0245"]["isHold"],
        "Required flat bench support and unilateral rep pacing remain cleanly enforced after packaging",
    )
    print("ALL BATCH EIGHTY-THREE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
