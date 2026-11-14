#!/usr/bin/env python3
"""Verify Batch 130 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["3006", "3007", "3010", "3017", "3116", "3117", "3122", "3123", "3124", "3142"]
per_side_ids = {"3007"}
bilateral_ids = set(inspected) - per_side_ids
expected_reviewed = len(json.loads(Path("app/src/main/assets/exercise_reviews.json").read_text())["reviewed"])
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == expected_reviewed, f"Bundled ledger keeps exact {expected_reviewed} reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 130 entries stay out of the reviewed ledger")
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
        and catalog["dataset_1324_3007"]["perSide"]
        and all(not catalog["dataset_1324_" + x]["perSide"] for x in bilateral_ids)
        and catalog["dataset_1324_3007"]["requiredEquipment"] == ["稳固立柱"]
        and catalog["dataset_1324_3124"]["requiredEquipment"] == ["直立靠背训练凳"]
        and all(catalog["dataset_1324_" + x]["requiredEquipment"] == ["平板训练凳"] for x in {"3010", "3117", "3122", "3123"}),
        "Dynamic unilateral/bilateral pacing and supporting equipment remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND THIRTY FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
