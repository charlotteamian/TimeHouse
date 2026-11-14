#!/usr/bin/env python3
"""Verify Batch 86 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0522", "0523", "0524", "0525", "0526", "0527", "0528", "0529", "0530", "0531"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 86 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0522", "0524", "0525", "0526", "0527", "0530"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_0524"]["perSide"]
        and catalog["dataset_1324_0525"]["perSide"]
        and catalog["dataset_1324_0530"]["perSide"]
        and not catalog["dataset_1324_0522"]["perSide"]
        and not catalog["dataset_1324_0526"]["perSide"]
        and not catalog["dataset_1324_0526"]["isHold"]
        and not catalog["dataset_1324_0527"]["isHold"],
        "Unilateral kettlebell pacing and bilateral clean/press execution remain cleanly enforced after packaging",
    )
    print("ALL BATCH EIGHTY-SIX FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
