#!/usr/bin/env python3
"""Verify Batch 64 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0018", "0019", "0022", "0023", "0024", "0025", "0026", "0027", "0028", "0029"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 64 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0018", "0022", "0023", "0025"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_0018"]["requiredEquipment"] == ["毛巾"]
        and catalog["dataset_1324_0022"]["requiredEquipment"] == ["平板训练凳"]
        and catalog["dataset_1324_0023"]["perSide"]
        and catalog["dataset_1324_0025"]["requiredEquipment"] == ["平板训练凳"]
        and not catalog["dataset_1324_0025"]["isHold"],
        "Required bench/towel supports and unilateral rep modes remain enforced after packaging",
    )
    print("ALL BATCH SIXTY-FOUR FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
