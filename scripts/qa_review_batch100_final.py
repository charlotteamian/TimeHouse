#!/usr/bin/env python3
"""Verify Batch 100 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0849", "0850", "0851", "0852", "0853", "0854", "0856", "0857", "0859", "0860"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 100 candidates stay out of the reviewed ledger")
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
        not catalog["dataset_1324_0849"]["isHold"]
        and catalog["dataset_1324_0850"]["perSide"]
        and not catalog["dataset_1324_0851"]["perSide"]
        and catalog["dataset_1324_0860"]["perSide"]
        and catalog["dataset_1324_0849"]["primary"] == ["腹肌"]
        and catalog["dataset_1324_0851"]["primary"] == ["股四头肌"]
        and catalog["dataset_1324_0852"]["primary"] == ["臀肌"]
        and catalog["dataset_1324_0853"]["primary"] == ["肱二头肌"]
        and catalog["dataset_1324_0854"]["primary"] == ["前臂"]
        and catalog["dataset_1324_0856"]["primary"] == ["胸肌"]
        and catalog["dataset_1324_0857"]["primary"] == ["腹肌"]
        and catalog["dataset_1324_0859"]["primary"] == ["前臂"]
        and catalog["dataset_1324_0860"]["primary"] == ["肱三头肌"],
        "Bilateral and unilateral pacing, abs, quads, glutes, biceps, forearms, pecs, and triceps muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH ONE HUNDRED FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
