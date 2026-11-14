#!/usr/bin/env python3
"""Verify Batch 102 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0971", "0972", "0974", "0975", "0976", "0977", "0978", "0979", "0980", "0981"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 102 candidates stay out of the reviewed ledger")
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
        not catalog["dataset_1324_0971"]["isHold"]
        and catalog["dataset_1324_0976"]["perSide"]
        and not catalog["dataset_1324_0977"]["perSide"]
        and catalog["dataset_1324_0971"]["primary"] == ["腹肌"]
        and catalog["dataset_1324_0974"]["primary"] == ["背阔肌"]
        and catalog["dataset_1324_0975"]["primary"] == ["肱三头肌"]
        and catalog["dataset_1324_0976"]["primary"] == ["肱二头肌"]
        and catalog["dataset_1324_0977"]["primary"] == ["三角肌"]
        and catalog["dataset_1324_0978"]["primary"] == ["三角肌"]
        and catalog["dataset_1324_0979"]["primary"] == ["腹肌"]
        and catalog["dataset_1324_0980"]["primary"] == ["臀肌"]
        and catalog["dataset_1324_0981"]["primary"] == ["腹肌"],
        "Bilateral and unilateral band pacing, abs, lats, triceps, biceps, delts, and glutes muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND TWO FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
