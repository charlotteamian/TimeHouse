#!/usr/bin/env python3
"""Verify Batch 112 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["1343", "1344", "1345", "1347", "1348", "1349", "1350", "1351", "1353", "1354"]
per_side_ids = {"1347"}
bilateral_ids = set(inspected) - per_side_ids
lats_ids = {"1347", "1353"}
upper_back_ids = set(inspected) - lats_ids - {"1343"}
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 112 candidates stay out of the reviewed ledger")
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
        and catalog["dataset_1324_1343"]["primary"] == ["脊柱"]
        and all(catalog["dataset_1324_" + x]["primary"] == ["背阔肌"] for x in lats_ids)
        and all(catalog["dataset_1324_" + x]["primary"] == ["上背"] for x in upper_back_ids),
        "Unilateral pacing and primary muscles remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND TWELVE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
