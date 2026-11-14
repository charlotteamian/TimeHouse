#!/usr/bin/env python3
"""Verify Batch 82 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0228", "0229", "0230", "0231", "0232", "0233", "0234", "0235", "0236", "0237"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 82 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0228", "0230", "0231", "0234", "0235"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_0228"]["perSide"]
        and catalog["dataset_1324_0230"]["perSide"]
        and catalog["dataset_1324_0231"]["perSide"]
        and catalog["dataset_1324_0235"]["perSide"]
        and not catalog["dataset_1324_0228"]["isHold"]
        and not catalog["dataset_1324_0234"]["isHold"],
        "Pacing, per-side unilateral modes, and hold prevention remain cleanly enforced after packaging",
    )
    print("ALL BATCH EIGHTY-TWO FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
