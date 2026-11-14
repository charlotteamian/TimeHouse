#!/usr/bin/env python3
"""Verify Batch 111 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["1325", "1332", "1333", "1334", "1335", "1336", "1338", "1339", "1341", "1342"]
per_side_ids = {"1332", "1339", "1342"}
bilateral_ids = set(inspected) - per_side_ids
lats_ids = {"1325", "1332", "1339", "1341", "1342"}
spine_ids = {"1333", "1334", "1335", "1336", "1338"}
wall_ids = {"1333", "1334", "1335"}
ball_support_ids = {"1332", "1339"}
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 111 candidates stay out of the reviewed ledger")
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
        and all(catalog["dataset_1324_" + x]["requiredEquipment"] == ["墙面"] for x in wall_ids)
        and all(catalog["dataset_1324_" + x]["requiredEquipment"] == ["瑜伽球"] for x in ball_support_ids)
        and all(catalog["dataset_1324_" + x]["primary"] == ["背阔肌"] for x in lats_ids)
        and all(catalog["dataset_1324_" + x]["primary"] == ["脊柱"] for x in spine_ids),
        "Unilateral pacing, wall/ball supports, and spine/lats muscles remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND ELEVEN FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
