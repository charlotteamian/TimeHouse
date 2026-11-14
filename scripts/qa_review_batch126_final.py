#!/usr/bin/env python3
"""Verify Batch 126 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["2205", "2206", "2207", "2208", "2209", "2285", "2286", "2287", "2288", "2289"]
expected_reviewed = len(json.loads(Path("app/src/main/assets/exercise_reviews.json").read_text())["reviewed"])
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == expected_reviewed, f"Bundled ledger keeps exact {expected_reviewed} reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 126 entries stay out of the reviewed ledger")
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
        and catalog["dataset_1324_2208"]["primary"] == ["脊柱"]
        and catalog["dataset_1324_2288"]["primary"] == ["前臂"]
        and catalog["dataset_1324_2289"]["primary"] == ["小腿肌"],
        "Dynamic bilateral pacing and localized anatomy remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND TWENTY-SIX FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
