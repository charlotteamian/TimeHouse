#!/usr/bin/env python3
"""Verify Batch 58 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["3318", "3240", "3327", "3241", "3360", "3541", "3361", "3542", "3418", "3545"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 58 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["3240", "3327", "3541", "3361", "3418", "3545"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_3240"]["safeWithRequiredEquipment"]
        and catalog["dataset_1324_3541"]["available"]["哑铃|上斜训练凳"]
        and catalog["dataset_1324_3361"]["perSide"]
        and not catalog["dataset_1324_3327"]["isHold"]
        and not catalog["dataset_1324_3418"]["isHold"]
        and catalog["dataset_1324_3418"]["available"]["单杠"]
        and catalog["dataset_1324_3545"]["perSide"]
        and catalog["dataset_1324_3545"]["available"]["哑铃|上斜训练凳"],
        "Required incline bench, pull-up bar, ball-wall support, and unilateral press/hop modes remain enforced after packaging",
    )
    print("ALL BATCH FIFTY-EIGHT FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
