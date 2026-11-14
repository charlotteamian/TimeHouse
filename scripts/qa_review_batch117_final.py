#!/usr/bin/env python3
"""Verify Batch 117 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["1439", "1451", "1452", "1456", "1457", "1458", "1461", "1462", "1463", "1464"]
leg_ids = {"1461", "1462", "1463", "1464"}
shoulder_ids = {"1456", "1457"}
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 117 candidates stay out of the reviewed ledger")
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
        and catalog["dataset_1324_1458"]["requiredEquipment"] == ["平板训练凳"]
        and catalog["dataset_1324_1439"]["primary"] == ["斜方肌"]
        and catalog["dataset_1324_1451"]["primary"] == ["肱三头肌"]
        and catalog["dataset_1324_1452"]["primary"] == ["腹肌"]
        and all(catalog["dataset_1324_" + x]["primary"] == ["三角肌"] for x in shoulder_ids)
        and catalog["dataset_1324_1458"]["primary"] == ["肱二头肌"]
        and all(catalog["dataset_1324_" + x]["primary"] == ["臀肌"] for x in leg_ids),
        "Flat bench support and primary muscle mappings remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND SEVENTEEN FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
