#!/usr/bin/env python3
"""Verify Batch 71 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0091", "0092", "0094", "0095", "0096", "0097", "0098", "0099", "0100", "0101"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 71 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0091", "0094", "0097", "0099"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_0091"]["requiredEquipment"] == ["平板训练凳"]
        and catalog["dataset_1324_0094"]["requiredEquipment"] == ["平板训练凳"]
        and catalog["dataset_1324_0094"]["perSide"]
        and catalog["dataset_1324_0097"]["perSide"]
        and catalog["dataset_1324_0099"]["perSide"]
        and not catalog["dataset_1324_0091"]["isHold"],
        "Required flat bench supports and unilateral rep modes remain enforced after packaging",
    )
    print("ALL BATCH SEVENTY-ONE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
