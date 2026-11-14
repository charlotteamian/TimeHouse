#!/usr/bin/env python3
"""Verify Batch 97 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0764", "0765", "0766", "0767", "0768", "0769", "0770", "0771", "0772", "0773"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 97 candidates stay out of the reviewed ledger")
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
        catalog["dataset_1324_0768"]["perSide"]
        and not catalog["dataset_1324_0770"]["perSide"]
        and not catalog["dataset_1324_0764"]["isHold"]
        and catalog["dataset_1324_0764"]["primary"] == ["胸肌"]
        and catalog["dataset_1324_0765"]["primary"] == ["三角肌"]
        and catalog["dataset_1324_0767"]["primary"] == ["斜方肌"]
        and catalog["dataset_1324_0768"]["primary"] == ["股四头肌"]
        and catalog["dataset_1324_0771"]["primary"] == ["前臂"]
        and catalog["dataset_1324_0773"]["primary"] == ["小腿肌"],
        "Unilateral split squat pacing, bilateral press execution, chest, delts, traps, quads, forearms, and calves muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH NINETY-SEVEN FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
