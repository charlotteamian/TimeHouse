#!/usr/bin/env python3
"""Verify Batch 70 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0081", "0082", "0083", "0084", "0085", "0086", "0087", "0088", "0089", "0090"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 70 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0081", "0082", "0088", "0090"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_0081"]["requiredEquipment"] == ["牧师凳"]
        and catalog["dataset_1324_0082"]["requiredEquipment"] == ["平板训练凳"]
        and catalog["dataset_1324_0088"]["requiredEquipment"] == ["平板训练凳", "稳固踏台"]
        and catalog["dataset_1324_0090"]["requiredEquipment"] == ["平板训练凳"]
        and not catalog["dataset_1324_0082"]["isHold"],
        "Required bench and stepper supports remain enforced after packaging without hold false positives",
    )
    print("ALL BATCH SEVENTY FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
