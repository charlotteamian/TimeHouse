#!/usr/bin/env python3
"""Verify Batch 56 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["3297", "2403", "3298", "2470", "3299", "2705", "3300", "2706", "3301", "2796"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 56 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["3297", "2403", "3298", "2796"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_3297"]["available"]["单杠"]
        and catalog["dataset_1324_3297"]["isHold"]
        and catalog["dataset_1324_3298"]["isHold"]
        and catalog["dataset_1324_2403"]["perSide"]
        and catalog["dataset_1324_2796"]["perSide"]
        and catalog["dataset_1324_2796"]["safeWithRequiredEquipment"],
        "Required pull-up bar, stable box, isometric lever/planche, and unilateral curl/step-up rules remain enforced after packaging",
    )
    print("ALL BATCH FIFTY-SIX FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
