#!/usr/bin/env python3
"""Verify Batch 90 deferred entries cannot leak into reviewed ledger or active workouts."""
from pathlib import Path

exec(Path("scripts/qa_review_flow.py").read_text().split("\nstop()\noriginal =")[0])
inspected = ["0577", "0578", "0579", "0580", "0581", "0582", "0583", "0584", "0585", "0586"]
stop()
original = b'<?xml version="1.0" encoding="utf-8"?><map />'
(out / "original-prefs.xml").write_bytes(original)

try:
    check(len(known) == 138, "Bundled ledger keeps exact 138 reviewed items with zero auto-approvals")
    check(not any("dataset_1324_" + x in known for x in inspected), "All ten deferred Batch 90 candidates stay out of the reviewed ledger")
    raw = adb(
        "shell", "am", "instrument", "-w",
        "-e", "catalog", ",".join("dataset_1324_" + x for x in ["0577", "0578", "0580", "0582", "0584", "0585", "0586"]),
        "com.restartday.fitness.qa/.UiSnapshot"
    ).decode()
    match = re.search(r"INSTRUMENTATION_RESULT: catalog=(\S+)", raw)
    assert match, raw
    catalog = json.loads(base64.b64decode(match.group(1)))
    (out / "loaded-safety.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    check(
        catalog["dataset_1324_0582"]["perSide"]
        and not catalog["dataset_1324_0578"]["perSide"]
        and not catalog["dataset_1324_0585"]["perSide"]
        and not catalog["dataset_1324_0586"]["isHold"]
        and catalog["dataset_1324_0577"]["primary"] == ["胸肌"]
        and catalog["dataset_1324_0580"]["primary"] == ["斜方肌"]
        and catalog["dataset_1324_0584"]["primary"] == ["三角肌"],
        "Unilateral kneeling leg curl pacing, bilateral deadlift/extension execution, chest press, shrug, and lateral raise muscle groups remain cleanly enforced after packaging",
    )
    print("ALL BATCH NINETY FINAL CHECKS PASSED", flush=True)
finally:
    write_state(original)
    launch()
