#!/usr/bin/env python3
"""Verify Batch 48 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["3132", "1676", "3145", "1677", "3147", "1678", "3156", "1679", "3158", "1680"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 136, "Bundled ledger keeps exact 136 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 48 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["3132", "1676", "1678", "3156", "3158", "1680"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_3132"]["available"]["直立靠背训练凳"]
        and catalog["dataset_1324_1676"]["safeWithRequiredEquipment"]
        and catalog["dataset_1324_1678"]["available"]["哑铃|直立靠背训练凳"]
        and catalog["dataset_1324_3156"]["available"]["哑铃|平板训练凳"]
        and catalog["dataset_1324_3158"]["equipment"] == ["固定器械"]
        and catalog["dataset_1324_1680"]["available"]["哑铃|上斜训练凳"],
        "Required supports and corrected dumbbell/cable equipment constraints remain enforced after packaging",
    )
    print("ALL BATCH FORTY-EIGHT FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
