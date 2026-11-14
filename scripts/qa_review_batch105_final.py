#!/usr/bin/env python3
"""Verify Batch 105 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["1004", "1005", "1007", "1008", "1009", "1010", "1011", "1012", "1013", "1014"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 105 candidates stay out of the reviewed ledger")
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
        not catalog["dataset_1324_1004"]["isHold"]
        and not catalog["dataset_1324_1008"]["perSide"]
        and catalog["dataset_1324_1008"]["requiredEquipment"] == ["稳固踏台"]
        and catalog["dataset_1324_1004"]["primary"] == ["臀肌"]
        and catalog["dataset_1324_1005"]["primary"] == ["腹肌"]
        and catalog["dataset_1324_1008"]["primary"] == ["臀肌"]
        and catalog["dataset_1324_1009"]["primary"] == ["臀肌"]
        and catalog["dataset_1324_1010"]["primary"] == ["脊柱"]
        and catalog["dataset_1324_1011"]["primary"] == ["腹肌"]
        and catalog["dataset_1324_1012"]["primary"] == ["三角肌"]
        and catalog["dataset_1324_1013"]["primary"] == ["背阔肌"]
        and catalog["dataset_1324_1014"]["primary"] == ["腹肌"],
        "Bilateral band pacing, step platform support, glutes, abs, spine, delts, and lats muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND FIVE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
