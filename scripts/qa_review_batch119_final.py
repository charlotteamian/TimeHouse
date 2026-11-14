#!/usr/bin/env python3
"""Verify Batch 119 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["1616", "1625", "1626", "1627", "1628", "1629", "1630", "1631", "1632", "1633"]
bicep_ids = {"1616", "1627", "1628", "1629", "1630", "1631", "1632", "1633"}
per_side_ids = {"1631", "1633"}
bilateral_ids = set(inspected) - per_side_ids
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 139, "Bundled ledger keeps exact 139 reviewed items with zero auto-approvals for Batch 119")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 119 candidates stay out of the reviewed ledger")
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
        and catalog["dataset_1324_1625"]["requiredEquipment"] == ["上斜训练凳"]
        and catalog["dataset_1324_1626"]["requiredEquipment"] == ["带勾脚的下斜训练凳"]
        and catalog["dataset_1324_1627"]["requiredEquipment"] == ["牧师凳"]
        and catalog["dataset_1324_1628"]["requiredEquipment"] == ["牧师凳"]
        and catalog["dataset_1324_1631"]["requiredEquipment"] == ["平板训练凳"]
        and catalog["dataset_1324_1633"]["requiredEquipment"] == ["牧师凳"]
        and catalog["dataset_1324_1625"]["primary"] == ["肱三头肌"]
        and catalog["dataset_1324_1626"]["primary"] == ["胸肌"]
        and all(catalog["dataset_1324_" + x]["primary"] == ["肱二头肌"] for x in bicep_ids),
        "Unilateral pacing, bench supports, and primary muscles remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND NINETEEN FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
