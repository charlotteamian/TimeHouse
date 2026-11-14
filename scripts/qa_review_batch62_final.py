#!/usr/bin/env python3
"""Verify Batch 62 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["3667", "3669", "3671", "3672", "3679", "3698", "3785"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All seven deferred Batch 62 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["3667", "3669", "3671", "3785"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_3667"]["perSide"]
        and catalog["dataset_1324_3669"]["perSide"]
        and catalog["dataset_1324_3671"]["perSide"]
        and catalog["dataset_1324_3785"]["available"]["稳固踏台"]
        and not catalog["dataset_1324_3785"]["isHold"],
        "Required stable platform and unilateral rep modes remain enforced after packaging",
    )
    print("ALL BATCH SIXTY-TWO FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
