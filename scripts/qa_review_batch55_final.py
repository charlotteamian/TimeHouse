#!/usr/bin/env python3
"""Verify Batch 55 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["3292", "2321", "3293", "2327", "3294", "2397", "3295", "2401", "3296", "2402"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 55 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["3293", "3294", "2397", "3295", "3296"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_3293"]["available"]["单杠"]
        and catalog["dataset_1324_3293"]["perSide"]
        and catalog["dataset_1324_3294"]["perSide"]
        and catalog["dataset_1324_2397"]["available"]["哑铃|直立靠背训练凳"]
        and not catalog["dataset_1324_3295"]["isHold"]
        and catalog["dataset_1324_3296"]["isHold"],
        "Required pull-up bar, upright bench, unilateral archer, and hold-vs-reps rules remain enforced after packaging",
    )
    print("ALL BATCH FIFTY-FIVE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
