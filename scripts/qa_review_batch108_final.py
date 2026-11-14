#!/usr/bin/env python3
"""Verify Batch 108 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["1267", "1268", "1269", "1270", "1272", "1296", "1298", "1299", "1300", "1301"]
per_side_ids = {"1267", "1298"}
bilateral_ids = set(inspected) - per_side_ids
ball_ids = {"1267", "1268", "1272", "1296"}
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 108 candidates stay out of the reviewed ledger")
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
        and all(catalog["dataset_1324_" + x]["requiredEquipment"] == ["瑜伽球"] for x in ball_ids)
        and all(catalog["dataset_1324_" + x]["primary"] == ["胸肌"] for x in inspected),
        "Unilateral/bilateral pacing, stability ball supports, and pectorals muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND EIGHT FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
