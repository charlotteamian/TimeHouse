#!/usr/bin/env python3
"""Verify Batch 91 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0587", "0588", "0589", "0590", "0591", "0592", "0593", "0594", "0595", "0596"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 91 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0587", "0589", "0590", "0591", "0593", "0594", "0596"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_0589"]["perSide"]
        and catalog["dataset_1324_0590"]["perSide"]
        and not catalog["dataset_1324_0587"]["perSide"]
        and not catalog["dataset_1324_0591"]["isHold"]
        and catalog["dataset_1324_0591"]["primary"] == ["肱三头肌"]
        and catalog["dataset_1324_0593"]["primary"] == ["臀肌"]
        and catalog["dataset_1324_0594"]["primary"] == ["小腿肌"]
        and catalog["dataset_1324_0596"]["primary"] == ["胸肌"],
        "Unilateral landmine row and shoulder press pacing, bilateral dip, calf raise, reverse hyperextension and fly muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH NINETY-ONE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
