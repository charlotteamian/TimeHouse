#!/usr/bin/env python3
"""Verify Batch 122 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["1712", "1713", "1714", "1716", "1717", "1718", "1719", "1720", "1721", "1722"]
quad_ids = {"1713", "1714"}
tricep_ids = {"1718", "1719", "1720", "1721", "1722"}
per_side_ids = {"1712", "1713", "1714"}
bilateral_ids = set(inspected) - per_side_ids
expected_reviewed = len(json.loads(Path("app/src/main/assets/exercise_reviews.json").read_text())["reviewed"])
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == expected_reviewed, f"Bundled ledger keeps exact {expected_reviewed} reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 122 entries stay out of the reviewed ledger")
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
        and catalog["dataset_1324_1712"]["primary"] == ["大腿内收肌群"]
        and all(catalog["dataset_1324_" + x]["primary"] == ["股四头肌"] for x in quad_ids)
        and catalog["dataset_1324_1716"]["primary"] == ["胸肌"]
        and catalog["dataset_1324_1717"]["primary"] == ["背阔肌"]
        and all(catalog["dataset_1324_" + x]["primary"] == ["肱三头肌"] for x in tricep_ids),
        "Unilateral pacing and primary muscles remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND TWENTY-TWO FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
