#!/usr/bin/env python3
"""Verify Batch 101 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0861", "0862", "0866", "0868", "0869", "0873", "0874", "0968", "0969", "0970"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 101 candidates stay out of the reviewed ledger")
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
        not catalog["dataset_1324_0861"]["isHold"]
        and not catalog["dataset_1324_0866"]["isHold"]
        and not catalog["dataset_1324_0861"]["perSide"]
        and not catalog["dataset_1324_0869"]["perSide"]
        and catalog["dataset_1324_0861"]["primary"] == ["上背"]
        and catalog["dataset_1324_0862"]["primary"] == ["腹肌"]
        and catalog["dataset_1324_0866"]["primary"] == ["腹肌"]
        and catalog["dataset_1324_0868"]["primary"] == ["肱二头肌"]
        and catalog["dataset_1324_0869"]["primary"] == ["三角肌"]
        and catalog["dataset_1324_0873"]["primary"] == ["腹肌"]
        and catalog["dataset_1324_0874"]["primary"] == ["腹肌"]
        and catalog["dataset_1324_0968"]["primary"] == ["肱二头肌"]
        and catalog["dataset_1324_0969"]["primary"] == ["腹肌"]
        and catalog["dataset_1324_0970"]["primary"] == ["背阔肌"],
        "Bilateral cable and band pacing, upper back, abs, biceps, delts, and lats muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND ONE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
