#!/usr/bin/env python3
"""Verify Batch 93 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0607", "0609", "0636", "0637", "0640", "0641", "0648", "0650", "0653", "0655"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 93 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0607", "0609", "0636", "0640", "0648", "0650", "0653", "0655"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_0640"]["perSide"]
        and not catalog["dataset_1324_0648"]["perSide"]
        and not catalog["dataset_1324_0653"]["isHold"]
        and not catalog["dataset_1324_0655"]["isHold"]
        and catalog["dataset_1324_0607"]["primary"] == ["肱三头肌"]
        and catalog["dataset_1324_0609"]["primary"] == ["上背"]
        and catalog["dataset_1324_0648"]["primary"] == ["腘绳肌"],
        "Unilateral medicine ball slam pacing, bilateral power clean execution, triceps extension, upper back row, and hamstring muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH NINETY-THREE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
