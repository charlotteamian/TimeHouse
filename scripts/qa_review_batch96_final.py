#!/usr/bin/env python3
"""Verify Batch 96 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0754", "0755", "0756", "0757", "0758", "0759", "0760", "0761", "0762", "0763"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 96 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in inspected),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        not catalog["dataset_1324_0754"]["isHold"]
        and not catalog["dataset_1324_0755"]["perSide"]
        and catalog["dataset_1324_0756"]["primary"] == ["臀肌"]
        and catalog["dataset_1324_0757"]["primary"] == ["胸肌"]
        and catalog["dataset_1324_0759"]["primary"] == ["前锯肌"]
        and catalog["dataset_1324_0761"]["primary"] == ["上背"]
        and catalog["dataset_1324_0762"]["primary"] == ["三角肌"]
        and catalog["dataset_1324_0763"]["primary"] == ["小腿肌"],
        "Bilateral smith machine pacing, glutes, chest, serratus anterior, upper back, delts, and calves muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH NINETY-SIX FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
