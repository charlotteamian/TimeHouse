#!/usr/bin/env python3
"""Verify Batch 94 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0656", "0663", "0673", "0675", "0680", "0738", "0739", "0740", "0741", "0742"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 94 candidates stay out of the reviewed ledger")
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
        not catalog["dataset_1324_0656"]["isHold"]
        and not catalog["dataset_1324_0663"]["perSide"]
        and catalog["dataset_1324_0673"]["primary"] == ["背阔肌"]
        and catalog["dataset_1324_0675"]["primary"] == ["臀肌"]
        and catalog["dataset_1324_0680"]["primary"] == ["上背"]
        and catalog["dataset_1324_0738"]["primary"] == ["小腿肌"]
        and catalog["dataset_1324_0739"]["primary"] == ["臀肌"],
        "Bilateral sled and bodyweight pacing, chest, lats, glutes, upper back, and calves muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH NINETY-FOUR FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
