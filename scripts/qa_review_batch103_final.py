#!/usr/bin/env python3
"""Verify Batch 103 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0983", "0984", "0985", "0986", "0987", "0988", "0989", "0990", "0991", "0992"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 103 candidates stay out of the reviewed ledger")
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
        not catalog["dataset_1324_0984"]["isHold"]
        and catalog["dataset_1324_0983"]["perSide"]
        and not catalog["dataset_1324_0984"]["perSide"]
        and catalog["dataset_1324_0986"]["perSide"]
        and catalog["dataset_1324_0987"]["perSide"]
        and catalog["dataset_1324_0988"]["perSide"]
        and catalog["dataset_1324_0989"]["perSide"]
        and catalog["dataset_1324_0990"]["perSide"]
        and not catalog["dataset_1324_0991"]["perSide"]
        and catalog["dataset_1324_0983"]["primary"] == ["背阔肌"]
        and catalog["dataset_1324_0984"]["primary"] == ["臀肌"]
        and catalog["dataset_1324_0985"]["primary"] == ["腹肌"]
        and catalog["dataset_1324_0986"]["primary"] == ["肱二头肌"]
        and catalog["dataset_1324_0987"]["primary"] == ["股四头肌"]
        and catalog["dataset_1324_0988"]["primary"] == ["上背"]
        and catalog["dataset_1324_0989"]["primary"] == ["胸肌"]
        and catalog["dataset_1324_0990"]["primary"] == ["上背"]
        and catalog["dataset_1324_0991"]["primary"] == ["臀肌"]
        and catalog["dataset_1324_0992"]["primary"] == ["腹肌"],
        "Bilateral and unilateral band pacing, lats, glutes, abs, biceps, quads, upper back, and pecs muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED AND THREE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
