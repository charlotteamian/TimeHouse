#!/usr/bin/env python3
"""Verify Batch 60 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["3533", "3664", "3543", "3888", "3544", "5201", "3552", "3561", "3582", "3636"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 60 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["3664", "3888", "3544", "3561", "3636"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_3664"]["isHold"]
        and catalog["dataset_1324_3664"]["perSide"]
        and catalog["dataset_1324_3888"]["perSide"]
        and catalog["dataset_1324_3544"]["isHold"]
        and catalog["dataset_1324_3561"]["perSide"]
        and catalog["dataset_1324_3636"]["available"]["墙面"]
        and catalog["dataset_1324_3636"]["perSide"],
        "Required wall support, side-bridge holds, and unilateral snatch/march/lunge modes remain enforced after packaging",
    )
    print("ALL BATCH SIXTY FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
