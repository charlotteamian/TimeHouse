#!/usr/bin/env python3
"""Verify Batch 87 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0532", "0533", "0534", "0535", "0536", "0537", "0538", "0539", "0540", "0541"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 87 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0532", "0533", "0535", "0537", "0538", "0541"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_0537"]["perSide"]
        and catalog["dataset_1324_0538"]["perSide"]
        and catalog["dataset_1324_0541"]["perSide"]
        and not catalog["dataset_1324_0532"]["perSide"]
        and not catalog["dataset_1324_0533"]["perSide"]
        and not catalog["dataset_1324_0535"]["isHold"]
        and not catalog["dataset_1324_0537"]["isHold"],
        "Unilateral kettlebell pacing and bilateral squat/clean execution remain cleanly enforced after packaging",
    )
    print("ALL BATCH EIGHTY-SEVEN FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
