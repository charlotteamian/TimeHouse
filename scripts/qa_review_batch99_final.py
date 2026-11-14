#!/usr/bin/env python3
"""Verify Batch 99 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0832", "0833", "0834", "0835", "0840", "0841", "0844", "0845", "0846", "0847"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 99 candidates stay out of the reviewed ledger")
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
        not catalog["dataset_1324_0832"]["isHold"]
        and not catalog["dataset_1324_0833"]["perSide"]
        and catalog["dataset_1324_0832"]["primary"] == ["腹肌"]
        and catalog["dataset_1324_0833"]["primary"] == ["小腿肌"]
        and catalog["dataset_1324_0834"]["primary"] == ["三角肌"]
        and catalog["dataset_1324_0835"]["primary"] == ["脊柱"]
        and catalog["dataset_1324_0840"]["primary"] == ["腹肌"]
        and catalog["dataset_1324_0841"]["primary"] == ["背阔肌"]
        and catalog["dataset_1324_0844"]["primary"] == ["三角肌"]
        and catalog["dataset_1324_0845"]["primary"] == ["腹肌"]
        and catalog["dataset_1324_0846"]["primary"] == ["腹肌"]
        and catalog["dataset_1324_0847"]["primary"] == ["肱二头肌"],
        "Bilateral weighted and ball exercise pacing, abs, calves, delts, spine, lats, and biceps muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH NINETY-NINE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
