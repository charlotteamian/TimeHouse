#!/usr/bin/env python3
"""Verify Batch 89 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0552", "0553", "0554", "0562", "0571", "0572", "0573", "0574", "0575", "0576"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 89 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0552", "0554", "0562", "0571", "0573", "0576"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_0554"]["perSide"]
        and not catalog["dataset_1324_0552"]["perSide"]
        and not catalog["dataset_1324_0562"]["perSide"]
        and not catalog["dataset_1324_0571"]["isHold"]
        and catalog["dataset_1324_0573"]["primary"] == ["脊柱"]
        and catalog["dataset_1324_0576"]["primary"] == ["胸肌"],
        "Unilateral windmill pacing, bilateral clean/rotation execution, spine targeting, and chest press muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH EIGHTY-NINE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
