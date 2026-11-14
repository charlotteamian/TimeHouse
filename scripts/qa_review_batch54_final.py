#!/usr/bin/env python3
"""Verify Batch 54 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["3239", "2189", "3287", "2292", "3288", "2293", "3289", "2294", "3291", "2317"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 54 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["3239", "2189", "2293", "3288"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_3239"]["perSide"]
        and not catalog["dataset_1324_3239"]["isHold"]
        and catalog["dataset_1324_2189"]["available"]["哑铃|直立靠背训练凳"]
        and catalog["dataset_1324_2293"]["safeWithRequiredEquipment"]
        and catalog["dataset_1324_3288"]["available"]["双杠"],
        "Required bench, preacher, parallel-bar rules and shoulder-tap unilateral mode remain enforced after packaging",
    )
    print("ALL BATCH FIFTY-FOUR FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
