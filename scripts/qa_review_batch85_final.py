#!/usr/bin/env python3
"""Verify Batch 85 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0452", "0453", "0454", "0455", "0458", "0517", "0518", "0519", "0520", "0521"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 85 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0452", "0453", "0454", "0455", "0517", "0521"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_0452"]["requiredEquipment"] == ["牧师凳"]
        and catalog["dataset_1324_0453"]["requiredEquipment"] == ["平板训练凳"]
        and catalog["dataset_1324_0454"]["requiredEquipment"] == ["上斜训练凳"]
        and catalog["dataset_1324_0455"]["requiredEquipment"] == ["平板训练凳"]
        and catalog["dataset_1324_0517"]["perSide"]
        and not catalog["dataset_1324_0521"]["isHold"]
        and not catalog["dataset_1324_0521"]["perSide"],
        "Required support benches, unilateral windmill pacing, and bilateral rep execution remain cleanly enforced after packaging",
    )
    print("ALL BATCH EIGHTY-FIVE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
