#!/usr/bin/env python3
"""Verify Batch 128 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["2371", "2399", "2404", "2405", "2406", "2407", "2414", "2432", "2459", "2464"]
per_side_ids = {"2399", "2414", "2464"}
bilateral_ids = set(inspected) - per_side_ids
expected_reviewed = len(json.loads(Path("app/src/main/assets/exercise_reviews.json").read_text())["reviewed"])
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == expected_reviewed, f"Bundled ledger keeps exact {expected_reviewed} reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 128 entries stay out of the reviewed ledger")
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
        and all(catalog["dataset_1324_" + x]["perSide"] for x in per_side_ids)
        and all(not catalog["dataset_1324_" + x]["perSide"] for x in bilateral_ids)
        and catalog["dataset_1324_2432"]["requiredEquipment"] == ["平板训练凳"]
        and catalog["dataset_1324_2464"]["primary"] == ["背阔肌"],
        "Dynamic unilateral/bilateral pacing, support equipment, and primary muscles remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND TWENTY-EIGHT FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
