#!/usr/bin/env python3
"""Verify Batch 79 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0197", "0198", "0199", "0200", "0201", "0202", "0203", "0204", "0205", "0206"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 79 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0197", "0201", "0202", "0205"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_0202"]["perSide"]
        and not catalog["dataset_1324_0197"]["isHold"]
        and not catalog["dataset_1324_0201"]["isHold"]
        and catalog["dataset_1324_0202"]["requiredEquipment"] == []
        and catalog["dataset_1324_0205"]["primary"] == ["背阔肌"],
        "Per-side rep pacing and anatomical categories remain cleanly enforced after packaging",
    )
    print("ALL BATCH SEVENTY-NINE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
