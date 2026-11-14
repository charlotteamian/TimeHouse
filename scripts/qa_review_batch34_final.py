#!/usr/bin/env python3
"""Verify Batch 34 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["1401", "1277", "1403", "1278", "1405", "1279", "1407", "1280", "1418", "1281"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 123, "Bundled ledger keeps exact 123 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 34 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["1401", "1278", "1403", "1407", "1281"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        not catalog["dataset_1324_1401"]["safeSevereShoulder"]
        and not catalog["dataset_1324_1281"]["safeSevereShoulder"]
        and catalog["dataset_1324_1407"]["knee"] == "MEDIUM"
        and catalog["dataset_1324_1401"]["safeWithRequiredEquipment"]
        and catalog["dataset_1324_1278"]["safeWithRequiredEquipment"],
        "Joint stress and safety filters reflect muscle-up/incline shoulder loads and required dual supports",
    )
    print("ALL BATCH THIRTY-FOUR FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
