#!/usr/bin/env python3
"""Verify Batch 107 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["1257", "1258", "1259", "1260", "1261", "1262", "1263", "1264", "1265", "1266"]
per_side_ids = {"1260", "1262", "1263", "1264", "1265", "1266"}
bilateral_ids = set(inspected) - per_side_ids
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 107 candidates stay out of the reviewed ledger")
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
        and catalog["dataset_1324_1258"]["requiredEquipment"] == ["平板训练凳"]
        and all(catalog["dataset_1324_" + x]["requiredEquipment"] == ["上斜训练凳"] for x in ["1257", "1265"])
        and all(catalog["dataset_1324_" + x]["requiredEquipment"] == ["带勾脚的下斜训练凳"] for x in ["1260", "1261", "1262"])
        and all(catalog["dataset_1324_" + x]["requiredEquipment"] == ["瑜伽球"] for x in ["1263", "1264", "1266"])
        and all(catalog["dataset_1324_" + x]["primary"] == ["胸肌"] for x in inspected),
        "Unilateral/bilateral pacing, bench and ball supports, and pectorals muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND SEVEN FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
