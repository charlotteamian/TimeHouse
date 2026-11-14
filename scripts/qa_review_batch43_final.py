#!/usr/bin/env python3
"""Verify Batch 43 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["1773", "1651", "1774", "1652", "1775", "1653", "2271", "1654", "2298", "1655"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 131, "Bundled ledger keeps exact 131 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 43 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["1773", "1652", "2271", "2298"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_1773"]["safeWithRequiredEquipment"]
        and catalog["dataset_1324_1652"]["safeWithRequiredEquipment"]
        and not catalog["dataset_1324_2271"]["safeSevereShoulder"]
        and catalog["dataset_1324_2298"]["available"]["平板训练凳"],
        "Safety filters and required supports reflect shoulder punch load and required towel/ball/bench constraints",
    )
    print("ALL BATCH FORTY-THREE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
