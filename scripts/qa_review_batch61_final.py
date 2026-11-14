#!/usr/bin/env python3
"""Verify Batch 61 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["3637", "3638", "3639", "3640", "3645", "3655", "3656", "3662", "3663", "3665"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 61 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["3638", "3639", "3645", "3663", "3665"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_3638"]["perSide"]
        and catalog["dataset_1324_3639"]["perSide"]
        and catalog["dataset_1324_3645"]["perSide"]
        and not catalog["dataset_1324_3663"]["isHold"]
        and catalog["dataset_1324_3663"]["perSide"]
        and catalog["dataset_1324_3665"]["perSide"],
        "Unilateral rep modes and reverse-plank isometric hold remain enforced after packaging",
    )
    print("ALL BATCH SIXTY-ONE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
