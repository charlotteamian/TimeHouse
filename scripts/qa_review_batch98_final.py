#!/usr/bin/env python3
"""Verify Batch 98 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0774", "0775", "0776", "0786", "0788", "0796", "0798", "0811", "0818", "0830"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 98 candidates stay out of the reviewed ledger")
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
        not catalog["dataset_1324_0774"]["isHold"]
        and not catalog["dataset_1324_0776"]["perSide"]
        and catalog["dataset_1324_0774"]["primary"] == ["三角肌"]
        and catalog["dataset_1324_0776"]["primary"] == ["股四头肌"]
        and catalog["dataset_1324_0796"]["primary"] == ["腹肌"]
        and catalog["dataset_1324_0798"]["primary"] == ["心肺系统"]
        and catalog["dataset_1324_0811"]["primary"] == ["臀肌"]
        and catalog["dataset_1324_0818"]["primary"] == ["背阔肌"]
        and catalog["dataset_1324_0830"]["primary"] == ["肱三头肌"],
        "Bilateral barbell and smith machine pacing, delts, quads, abs, cardio, glutes, lats, and triceps muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH NINETY-EIGHT FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
