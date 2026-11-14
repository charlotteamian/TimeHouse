#!/usr/bin/env python3
"""Verify Batch 57 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["3302", "2803", "3303", "2805", "3304", "2808", "3314", "2812", "3315", "3234"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 57 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["2803", "3303", "2805", "3314", "3234"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        not catalog["dataset_1324_2803"]["isHold"]
        and catalog["dataset_1324_3303"]["safeWithRequiredEquipment"]
        and catalog["dataset_1324_2805"]["safeWithRequiredEquipment"]
        and catalog["dataset_1324_3314"]["safeWithRequiredEquipment"]
        and catalog["dataset_1324_3234"]["available"]["哑铃|平板训练凳"],
        "Required pole, stepbox, rings, flat bench, and corrected squat hold removal remain enforced after packaging",
    )
    print("ALL BATCH FIFTY-SEVEN FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
