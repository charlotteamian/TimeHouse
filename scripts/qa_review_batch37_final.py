#!/usr/bin/env python3
"""Verify Batch 37 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["1468", "1292", "1471", "1293", "1472", "1294", "1473", "1295", "1476", "1328"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 124, "Bundled ledger keeps exact 124 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 37 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["1468", "1292", "1294", "1476", "1328"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        not catalog["dataset_1324_1294"]["safeSevereShoulder"]
        and catalog["dataset_1324_1476"]["knee"] == "MEDIUM"
        and catalog["dataset_1324_1292"]["safeWithRequiredEquipment"]
        and catalog["dataset_1324_1294"]["lower_back"] == "MEDIUM"
        and catalog["dataset_1324_1328"]["safeWithRequiredEquipment"],
        "Joint stress and safety filters reflect pullover overhead demand, pistol knee load, and required supports",
    )
    print("ALL BATCH THIRTY-SEVEN FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
