#!/usr/bin/env python3
"""Verify Batch 104 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0993", "0994", "0996", "0997", "0998", "0999", "1000", "1001", "1002", "1003"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 104 candidates stay out of the reviewed ledger")
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
        not catalog["dataset_1324_0993"]["isHold"]
        and catalog["dataset_1324_0999"]["perSide"]
        and catalog["dataset_1324_1000"]["perSide"]
        and catalog["dataset_1324_1001"]["perSide"]
        and not catalog["dataset_1324_0993"]["perSide"]
        and catalog["dataset_1324_0993"]["primary"] == ["三角肌"]
        and catalog["dataset_1324_0994"]["primary"] == ["前臂"]
        and catalog["dataset_1324_0996"]["primary"] == ["臀肌"]
        and catalog["dataset_1324_0997"]["primary"] == ["三角肌"]
        and catalog["dataset_1324_0998"]["primary"] == ["肱三头肌"]
        and catalog["dataset_1324_0999"]["primary"] == ["小腿肌"]
        and catalog["dataset_1324_1000"]["primary"] == ["小腿肌"]
        and catalog["dataset_1324_1001"]["primary"] == ["股四头肌"]
        and catalog["dataset_1324_1002"]["primary"] == ["腹肌"]
        and catalog["dataset_1324_1003"]["primary"] == ["臀肌"],
        "Bilateral and unilateral band pacing, delts, forearms, glutes, triceps, calves, quads, and abs muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND FOUR FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
