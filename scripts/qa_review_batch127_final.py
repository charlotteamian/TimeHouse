#!/usr/bin/env python3
"""Verify Batch 127 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["2297", "2311", "2315", "2318", "2328", "2330", "2331", "2334", "2335", "2364"]
calf_ids = {"2315", "2334", "2335"}
expected_reviewed = len(json.loads(Path("app/src/main/assets/exercise_reviews.json").read_text())["reviewed"])
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == expected_reviewed, f"Bundled ledger keeps exact {expected_reviewed} reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 127 entries stay out of the reviewed ledger")
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
        and all(catalog["dataset_1324_" + x]["primary"] == ["小腿肌"] for x in calf_ids)
        and catalog["dataset_1324_2311"]["equipment"] == ["登阶机"]
        and catalog["dataset_1324_2334"]["equipment"] == ["雪橇机"],
        "Dynamic bilateral pacing, localized equipment, and primary muscles remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND TWENTY-SEVEN FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
