#!/usr/bin/env python3
"""Verify Batch 27 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0815", "0409", "0816", "0410", "0817", "0411", "0826", "0413", "0858", "0414"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 114, "Bundled ledger keeps exact 114 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 27 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0815", "0410", "0826", "0858", "0414"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        not catalog["dataset_1324_0414"]["safeSevereShoulder"]
        and catalog["dataset_1324_0410"]["knee"] == "MEDIUM"
        and catalog["dataset_1324_0858"]["knee"] == "MEDIUM"
        and catalog["dataset_1324_0414"]["safeWithRequiredEquipment"]
        and catalog["dataset_1324_0858"]["safeWithRequiredEquipment"],
        "Joint stress and safety filters reflect overhead press shoulder load and lunge/sprint knee demands",
    )
    print("ALL BATCH TWENTY-SEVEN FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
