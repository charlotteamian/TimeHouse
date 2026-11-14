#!/usr/bin/env python3
"""Verify Batch 132 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["3305", "3312", "3313", "3562", "3563", "3641", "3642", "3643", "3644", "3666"]
per_side_ids = {"3563"}
bilateral_ids = set(inspected) - per_side_ids
expected_reviewed = len(json.loads(Path("app/src/main/assets/exercise_reviews.json").read_text())["reviewed"])
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == expected_reviewed, f"Bundled ledger keeps exact {expected_reviewed} reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 132 entries stay out of the reviewed ledger")
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
        and catalog["dataset_1324_3563"]["perSide"]
        and all(not catalog["dataset_1324_" + x]["perSide"] for x in bilateral_ids)
        and catalog["dataset_1324_3312"]["requiredEquipment"] == ["单杠"]
        and catalog["dataset_1324_3313"]["requiredEquipment"] == ["双杠"]
        and catalog["dataset_1324_3562"]["requiredEquipment"] == ["平板训练凳"]
        and catalog["dataset_1324_3666"]["requiredEquipment"] == ["跑步机"],
        "Dynamic unilateral/bilateral pacing and supporting equipment remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND THIRTY-TWO FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
