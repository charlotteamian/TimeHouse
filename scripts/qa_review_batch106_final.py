#!/usr/bin/env python3
"""Verify Batch 106 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["1015", "1016", "1017", "1018", "1022", "1023", "1253", "1254", "1255", "1256"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 106 candidates stay out of the reviewed ledger")
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
        not any(catalog["dataset_1324_" + x]["isHold"] for x in inspected)
        and not any(catalog["dataset_1324_" + x]["perSide"] for x in inspected)
        and catalog["dataset_1324_1254"]["requiredEquipment"] == ["平板训练凳"]
        and catalog["dataset_1324_1255"]["requiredEquipment"] == ["带勾脚的下斜训练凳"]
        and catalog["dataset_1324_1256"]["requiredEquipment"] == ["带勾脚的下斜训练凳"]
        and catalog["dataset_1324_1015"]["primary"] == ["腹肌"]
        and catalog["dataset_1324_1016"]["primary"] == ["前臂"]
        and catalog["dataset_1324_1017"]["primary"] == ["三角肌"]
        and catalog["dataset_1324_1018"]["primary"] == ["斜方肌"]
        and catalog["dataset_1324_1022"]["primary"] == ["三角肌"]
        and catalog["dataset_1324_1023"]["primary"] == ["臀肌"]
        and catalog["dataset_1324_1253"]["primary"] == ["小腿肌"]
        and catalog["dataset_1324_1254"]["primary"] == ["胸肌"]
        and catalog["dataset_1324_1255"]["primary"] == ["背阔肌"]
        and catalog["dataset_1324_1256"]["primary"] == ["胸肌"],
        "Bilateral pacing, bench and decline bench supports, abs, forearms, delts, traps, glutes, calves, lats, and chest muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND SIX FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
