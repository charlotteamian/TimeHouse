#!/usr/bin/env python3
"""Verify Batch 53 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["3221", "2133", "3222", "2136", "3223", "2137", "3224", "2143", "3231", "2188"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 53 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["2137", "2188", "3221", "3224"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_2137"]["available"]["哑铃|直立靠背训练凳"]
        and catalog["dataset_1324_2188"]["available"]["哑铃|平板训练凳"]
        and catalog["dataset_1324_3221"]["primary"] == ["股四头肌"]
        and catalog["dataset_1324_3224"]["primary"] == ["心肺系统", "股四头肌"],
        "Bench requirements and corrected squats/jumping-jacks classification remain enforced after packaging",
    )
    print("ALL BATCH FIFTY-THREE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
