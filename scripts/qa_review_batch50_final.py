#!/usr/bin/env python3
"""Verify Batch 50 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["3168", "1732", "3193", "1733", "3201", "1734", "3202", "1735", "3203", "1736"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 137, "Bundled ledger keeps exact 137 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 50 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["3168", "3193", "1733", "1735", "1736"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_3168"]["safeWithRequiredEquipment"]
        and catalog["dataset_1324_3193"]["safeWithRequiredEquipment"]
        and catalog["dataset_1324_1733"]["available"]["哑铃|上斜训练凳"]
        and catalog["dataset_1324_1735"]["available"]["哑铃|平板训练凳"]
        and catalog["dataset_1324_1736"]["safeWithRequiredEquipment"],
        "Required TRX, Roman-chair, bench, and exercise-ball supports remain enforced after packaging",
    )
    print("ALL BATCH FIFTY FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
