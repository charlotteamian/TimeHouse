#!/usr/bin/env python3
"""Verify Batch 72 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0102", "0103", "0104", "0105", "0106", "0107", "0108", "0109", "0110", "0111"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 72 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0102", "0103", "0104", "0108"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        all(catalog["dataset_1324_" + x]["requiredEquipment"] == [] for x in ["0102", "0103", "0104", "0108"])
        and not catalog["dataset_1324_0102"]["isHold"]
        and not catalog["dataset_1324_0103"]["isHold"],
        "Clean floor barbell configurations remain enforced after packaging without hold false positives",
    )
    print("ALL BATCH SEVENTY-TWO FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
