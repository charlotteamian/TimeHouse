#!/usr/bin/env python3
"""Verify Batch 110 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["1314", "1316", "1317", "1318", "1319", "1320", "1321", "1322", "1323", "1324"]
upper_back_ids = set(inspected) - {"1314", "1316"}
incline_ids = {"1317", "1318", "1322"}
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 110 candidates stay out of the reviewed ledger")
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
        not any(catalog["dataset_1324_" + x]["isHold"] or catalog["dataset_1324_" + x]["perSide"] for x in inspected)
        and catalog["dataset_1324_1314"]["requiredEquipment"] == ["墙面"]
        and catalog["dataset_1324_1316"]["requiredEquipment"] == ["平板训练凳"]
        and all(catalog["dataset_1324_" + x]["requiredEquipment"] == ["上斜训练凳"] for x in incline_ids)
        and catalog["dataset_1324_1314"]["primary"] == ["脊柱"]
        and catalog["dataset_1324_1316"]["primary"] == ["背阔肌"]
        and all(catalog["dataset_1324_" + x]["primary"] == ["上背"] for x in upper_back_ids),
        "Wall, bench supports, and spine/lats/upper back primary muscles remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND TEN FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
