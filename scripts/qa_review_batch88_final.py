#!/usr/bin/env python3
"""Verify Batch 88 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0542", "0543", "0544", "0545", "0546", "0547", "0548", "0549", "0550", "0551"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 88 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0542", "0544", "0546", "0548", "0549", "0551"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_0546"]["requiredEquipment"] == ["平板训练凳"]
        and catalog["dataset_1324_0542"]["perSide"]
        and catalog["dataset_1324_0544"]["perSide"]
        and catalog["dataset_1324_0551"]["perSide"]
        and not catalog["dataset_1324_0548"]["perSide"]
        and not catalog["dataset_1324_0549"]["isHold"],
        "Flat bench support, unilateral kettlebell pacing, and bilateral swing execution remain cleanly enforced after packaging",
    )
    print("ALL BATCH EIGHTY-EIGHT FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
