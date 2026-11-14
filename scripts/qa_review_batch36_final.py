#!/usr/bin/env python3
"""Verify Batch 36 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["1429", "1287", "1430", "1288", "1460", "1289", "1466", "1290", "1467", "1291"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 124, "Bundled ledger keeps exact 124 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 36 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["1429", "1430", "1460", "1290", "1291"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        not catalog["dataset_1324_1429"]["safeSevereShoulder"]
        and not catalog["dataset_1324_1430"]["safeSevereShoulder"]
        and catalog["dataset_1324_1460"]["knee"] == "MEDIUM"
        and catalog["dataset_1324_1430"]["safeWithRequiredEquipment"]
        and catalog["dataset_1324_1290"]["safeWithRequiredEquipment"],
        "Joint stress and safety filters reflect pull-up/dip/ball-press shoulder loads and lunge knee demands",
    )
    print("ALL BATCH THIRTY-SIX FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
