#!/usr/bin/env python3
"""Verify Batch 95 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0743", "0744", "0746", "0747", "0748", "0749", "0750", "0751", "0752", "0753"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 95 candidates stay out of the reviewed ledger")
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
        not catalog["dataset_1324_0743"]["isHold"]
        and not catalog["dataset_1324_0744"]["perSide"]
        and catalog["dataset_1324_0746"]["primary"] == ["斜方肌"]
        and catalog["dataset_1324_0747"]["primary"] == ["三角肌"]
        and catalog["dataset_1324_0748"]["primary"] == ["胸肌"]
        and catalog["dataset_1324_0750"]["primary"] == ["股四头肌"]
        and catalog["dataset_1324_0751"]["primary"] == ["肱三头肌"],
        "Bilateral sled and smith machine pacing, traps, delts, chest, quads, and triceps muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH NINETY-FIVE FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
